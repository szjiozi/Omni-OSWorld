#!/usr/bin/env python3
"""Run the OSWorld multi-annotator portal in explicit local or AWS mode."""

from __future__ import annotations

import argparse
from contextlib import asynccontextmanager
import json
import os
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from benchmark_construction.annotation_portal.app import PortalWebConfig, create_app
from benchmark_construction.annotation_portal.auth import (
    CognitoIdentityProvider,
    PasswordChallengeManager,
    PortalSessionManager,
    StaticIdentityProvider,
)
from benchmark_construction.annotation_portal.aws_workspace import (
    AWSReferenceWorkspaceController,
    AWSWorkspaceSettings,
)
from benchmark_construction.annotation_portal.catalog import ReloadingTaskCatalog
from benchmark_construction.annotation_portal.models import TaskAssignment
from benchmark_construction.annotation_portal.service import (
    AnnotationPortalService,
    FakeWorkspaceController,
    WorkspaceJanitor,
)
from benchmark_construction.annotation_portal.storage import S3BundlePublisher
from benchmark_construction.annotation_portal.store import (
    DynamoPortalStore,
    MemoryPortalStore,
)


PILOT_ROOT = REPO_ROOT / "evaluation_examples/expert_skill_learning/pilot"
STATIC_DIR = REPO_ROOT / "benchmark_construction/annotation_portal/static"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("local", "aws"), required=True)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--pilot-root", type=Path, default=PILOT_ROOT)
    parser.add_argument("--assignments", type=Path, required=True)
    parser.add_argument("--allow-pending", action="store_true")
    parser.add_argument(
        "--local-credentials",
        type=Path,
        help="Untracked JSON credentials file; required only in local mode.",
    )
    return parser.parse_args()


def _required_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _live_pilot_root(path: Path) -> Path:
    """Return an absolute path without resolving the live snapshot symlink."""

    return path.expanduser().absolute()


def _seed_assignments(store, path: Path) -> None:
    document = _load_json(path)
    rows = document.get("assignments")
    if not isinstance(rows, list):
        raise SystemExit(f"{path} must contain an assignments list")
    for row in rows:
        username = row.get("username", "").strip()
        task_ids = row.get("task_ids")
        if not username or not isinstance(task_ids, list) or not task_ids:
            raise SystemExit(f"Invalid assignment row in {path}: {row!r}")
        for task_id in task_ids:
            store.put_assignment(TaskAssignment(task_id=task_id, username=username))


def _local_components(args, catalog):
    if args.local_credentials is None:
        raise SystemExit("--local-credentials is required in local mode")
    credentials_doc = _load_json(args.local_credentials)
    credentials = credentials_doc.get("users")
    if not isinstance(credentials, dict) or not credentials:
        raise SystemExit("Local credentials JSON must contain a non-empty users object")
    admin_usernames = frozenset(credentials_doc.get("admin_usernames", []))
    store = MemoryPortalStore()
    controller = FakeWorkspaceController(
        REPO_ROOT / "results/annotation_portal_local"
    )
    provider = StaticIdentityProvider(credentials, admin_usernames=admin_usernames)
    publisher = None
    return store, controller, provider, publisher, False


def _aws_components(args, catalog):
    import boto3

    region = _required_env("AWS_REGION")
    session = boto3.Session(region_name=region)
    store = DynamoPortalStore(
        session.client("dynamodb"),
        table_name=_required_env("PORTAL_DYNAMODB_TABLE"),
    )
    admin_usernames = frozenset(
        item.strip()
        for item in _required_env("PORTAL_ADMIN_USERNAMES").split(",")
        if item.strip()
    )
    provider = CognitoIdentityProvider(
        session.client("cognito-idp"),
        client_id=_required_env("PORTAL_COGNITO_CLIENT_ID"),
        admin_usernames=admin_usernames,
    )
    settings = AWSWorkspaceSettings(
        region=region,
        subnet_id=_required_env("AWS_SUBNET_ID"),
        security_group_id=_required_env("AWS_SECURITY_GROUP_ID"),
        ami_id=_required_env("AWS_AMI_ID"),
        result_root=Path(
            os.getenv(
                "PORTAL_RESULT_ROOT", str(REPO_ROOT / "results/reference_annotations")
            )
        ),
        instance_type=os.getenv("AWS_INSTANCE_TYPE", "t3.xlarge"),
        instance_profile_name=os.getenv("AWS_EC2_INSTANCE_PROFILE_NAME") or None,
    )
    controller = AWSReferenceWorkspaceController(settings)
    publisher = S3BundlePublisher(
        session.client("s3"),
        bucket=_required_env("PORTAL_S3_BUCKET"),
        root_prefix=os.getenv("PORTAL_S3_PREFIX", "reference-annotations"),
    )
    return store, controller, provider, publisher, True


def build_app(args: argparse.Namespace):
    pilot_root = _live_pilot_root(args.pilot_root)
    catalog = ReloadingTaskCatalog(pilot_root, allow_pending=args.allow_pending)
    catalog.all()
    if args.mode == "local":
        store, controller, provider, publisher, cookie_secure = _local_components(
            args, catalog
        )
        region = "local"
    else:
        store, controller, provider, publisher, cookie_secure = _aws_components(
            args, catalog
        )
        region = os.environ["AWS_REGION"]
    _seed_assignments(store, args.assignments.resolve())
    sessions = PortalSessionManager(store)
    service = AnnotationPortalService(
        store=store,
        catalog=catalog,
        controller=controller,
        task_config_dir=pilot_root / "task_configs",
        region=region,
        publisher=publisher,
        max_active=4,
    )
    janitor = WorkspaceJanitor(service)

    @asynccontextmanager
    async def lifespan(_app):
        janitor.start()
        try:
            yield
        finally:
            janitor.stop()

    app = create_app(
        config=PortalWebConfig(static_dir=STATIC_DIR, cookie_secure=cookie_secure),
        identity_provider=provider,
        session_manager=sessions,
        challenge_manager=PasswordChallengeManager(),
        service=service,
        lifespan=lifespan,
    )
    return app


def main() -> int:
    args = parse_args()
    if not 1 <= args.port <= 65535:
        raise SystemExit("--port must be between 1 and 65535")
    if args.mode == "aws" and args.host not in {"0.0.0.0", "::"}:
        raise SystemExit("AWS mode must use --host 0.0.0.0 or ::")
    import uvicorn

    uvicorn.run(build_app(args), host=args.host, port=args.port, proxy_headers=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
