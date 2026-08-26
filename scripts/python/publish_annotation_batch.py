#!/usr/bin/env python3
"""Publish an immutable pilot snapshot and assignments without restarting the portal."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import shlex
import shutil
import sys
import tarfile
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from benchmark_construction.annotation_portal.catalog import TaskCatalog


DEFAULT_PILOT = REPO_ROOT / "evaluation_examples/expert_skill_learning/pilot"
DEFAULT_ASSIGNMENTS = REPO_ROOT / (
    "evaluation_examples/expert_skill_learning/annotation_portal/assignments.example.json"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", default="osworld-dev")
    parser.add_argument("--region", default="ap-east-1")
    parser.add_argument("--stack-name", default="osworld-annotation-portal")
    parser.add_argument("--pilot-root", type=Path, default=DEFAULT_PILOT)
    parser.add_argument(
        "--dataset-root",
        type=Path,
        help="Dataset root with generated/<round> and review_packets/<round>.",
    )
    parser.add_argument("--dataset-round", default="round_01")
    parser.add_argument("--assignments", type=Path, default=DEFAULT_ASSIGNMENTS)
    parser.add_argument(
        "--replace-assignments",
        action="store_true",
        help="Delete stale assignments for every username in the new assignment file.",
    )
    parser.add_argument("--allow-pending", action="store_true")
    return parser.parse_args()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _archive_filter(info: tarfile.TarInfo) -> tarfile.TarInfo | None:
    if any(part in {"__pycache__", ".DS_Store"} for part in Path(info.name).parts):
        return None
    if info.issym() or info.islnk():
        raise ValueError(f"Pilot snapshot must not contain links: {info.name}")
    info.uid = info.gid = 0
    info.uname = info.gname = "root"
    info.mtime = 0
    return info


def build_snapshot(pilot_root: Path, output_path: Path) -> str:
    with output_path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed:
            with tarfile.open(fileobj=compressed, mode="w", format=tarfile.PAX_FORMAT) as archive:
                archive.add(
                    pilot_root,
                    arcname="pilot",
                    recursive=True,
                    filter=_archive_filter,
                )
    return file_sha256(output_path)


def stage_dataset_round(dataset_root: Path, round_name: str, destination: Path) -> Path:
    """Normalize a full-dataset round into the immutable Portal pilot layout."""

    dataset_root = dataset_root.resolve()
    generated = dataset_root / "generated"
    round_root = generated / round_name
    packet_root = dataset_root / "review_packets" / round_name
    artifact_root = round_root / "artifacts"
    sources = {
        "reference_packages.json": round_root / "reference_packages.json",
        "reference_package_reviews.json": round_root / "reference_package_reviews.json",
        "skill_pool.json": generated / "skill_pool.json",
    }
    for source in (*sources.values(), packet_root, artifact_root):
        if not source.exists():
            raise FileNotFoundError(source)
    destination.mkdir(parents=True, exist_ok=False)
    for name, source in sources.items():
        shutil.copy2(source, destination / name)
    normalized_packets = destination / "review_packets"
    shutil.copytree(packet_root, normalized_packets)
    normalized_artifacts = destination / "artifacts"
    shutil.copytree(artifact_root, normalized_artifacts)
    task_configs = destination / "task_configs"
    task_configs.mkdir()
    package_doc = json.loads(sources["reference_packages.json"].read_text(encoding="utf-8"))
    task_ids = [item["reference_task_id"] for item in package_doc["reference_packages"]]
    if len(task_ids) != len(set(task_ids)):
        raise ValueError("Dataset round contains duplicate reference task IDs")
    for task_id in task_ids:
        packet = normalized_packets / task_id
        for required in ("TASK.md", "review.json", "task_config.json"):
            if not (packet / required).is_file():
                raise FileNotFoundError(packet / required)
        task_config = packet / "task_config.json"
        config_doc = json.loads(task_config.read_text(encoding="utf-8"))
        configured_files = config_doc.get("config", [{}])[0].get("parameters", {}).get(
            "files", []
        )
        if len(configured_files) != 1:
            raise ValueError(f"{task_config} must upload exactly one artifact")
        artifact = normalized_artifacts / task_id / Path(
            configured_files[0]["local_path"]
        ).name
        if not artifact.is_file():
            raise FileNotFoundError(artifact)
        expected_hash = config_doc.get("reference_annotation", {}).get(
            "artifact_sha256"
        )
        if not expected_hash or file_sha256(artifact) != expected_hash:
            raise ValueError(f"Initial artifact SHA256 mismatch for {task_id}")
        shutil.copy2(task_config, task_configs / f"{task_id}.json")
    return destination


def stack_outputs(cloudformation: Any, stack_name: str) -> dict[str, str]:
    stack = cloudformation.describe_stacks(StackName=stack_name)["Stacks"][0]
    return {
        row["OutputKey"]: row["OutputValue"] for row in stack.get("Outputs", [])
    }


def load_assignments(path: Path, known_task_ids: set[str]) -> list[tuple[str, str]]:
    document = json.loads(path.read_text(encoding="utf-8"))
    result: list[tuple[str, str]] = []
    for row in document.get("assignments", []):
        username = row.get("username", "").strip()
        task_ids = row.get("task_ids")
        if not username or not isinstance(task_ids, list) or not task_ids:
            raise ValueError(f"Invalid assignment row: {row!r}")
        unknown = sorted(set(task_ids) - known_task_ids)
        if unknown:
            raise ValueError(f"Assignments reference unpublished tasks: {unknown}")
        result.extend((username, task_id) for task_id in task_ids)
    return result


def install_snapshot(
    ssm: Any,
    *,
    instance_id: str,
    bucket: str,
    key: str,
    sha256: str,
    allow_pending: bool,
) -> None:
    archive_path = f"/tmp/osworld-pilot-{sha256}.tar.gz"
    destination = f"/opt/osworld/published-pilots/{sha256}"
    download_code = (
        "import boto3; "
        f"boto3.client('s3').download_file({bucket!r}, {key!r}, {archive_path!r})"
    )
    validation_code = (
        "from pathlib import Path; "
        "from benchmark_construction.annotation_portal.catalog import TaskCatalog; "
        "from benchmark_construction.annotation_portal.aws_workspace import "
        "_load_task_config; "
        f"root=Path({(destination + '/pilot')!r}); "
        "TaskCatalog.load(packages_path=root/'reference_packages.json', "
        "skills_path=root/'skill_pool.json', "
        "reviews_path=root/'reference_package_reviews.json', "
        f"allow_pending={allow_pending!r}); "
        "[_load_task_config(path) for path in "
        "sorted((root/'task_configs').glob('*.json'))]"
    )
    commands = [
        "set -eu",
        f"/usr/bin/python3 -c {shlex.quote(download_code)}",
        f"printf '%s  %s\\n' {shlex.quote(sha256)} {shlex.quote(archive_path)} | sha256sum --check --strict",
        f"install -d -m 0755 {shlex.quote(destination)}",
        f"tar --extract --gzip --file {shlex.quote(archive_path)} --directory {shlex.quote(destination)}",
        f"cd /opt/osworld && /opt/osworld/.venv/bin/python -c {shlex.quote(validation_code)}",
        f"chown -R osworld:osworld {shlex.quote(destination)}",
        f"ln -sfnT {shlex.quote(destination + '/pilot')} /opt/osworld/live-pilot",
    ]
    response = ssm.send_command(
        InstanceIds=[instance_id],
        DocumentName="AWS-RunShellScript",
        Comment=f"Publish annotation pilot {sha256[:12]}",
        Parameters={"commands": commands},
    )
    command_id = response["Command"]["CommandId"]
    waiter_error = None
    try:
        ssm.get_waiter("command_executed").wait(
            CommandId=command_id,
            InstanceId=instance_id,
            WaiterConfig={"Delay": 5, "MaxAttempts": 120},
        )
    except Exception as exc:
        waiter_error = exc
    result = ssm.get_command_invocation(CommandId=command_id, InstanceId=instance_id)
    if result.get("Status") != "Success":
        detail = result.get("StandardErrorContent") or result.get("StandardOutputContent", "")
        raise RuntimeError(f"Pilot snapshot installation failed: {detail[-4000:]}") from waiter_error


def put_assignments(
    dynamodb: Any,
    table_name: str,
    rows: list[tuple[str, str]],
    *,
    replace: bool = False,
) -> int:
    from boto3.dynamodb.types import TypeDeserializer, TypeSerializer

    serializer = TypeSerializer()
    deserializer = TypeDeserializer()
    desired = set(rows)
    deleted = 0
    if replace:
        for username in sorted({username for username, _ in rows}):
            query: dict[str, Any] = {
                "TableName": table_name,
                "KeyConditionExpression": "pk = :pk AND begins_with(sk, :prefix)",
                "ExpressionAttributeValues": {
                    ":pk": serializer.serialize(f"USER#{username}"),
                    ":prefix": serializer.serialize("ASSIGNMENT#"),
                },
            }
            while True:
                response = dynamodb.query(**query)
                for raw in response.get("Items", []):
                    item = {key: deserializer.deserialize(value) for key, value in raw.items()}
                    if (username, item["task_id"]) in desired:
                        continue
                    dynamodb.delete_item(
                        TableName=table_name,
                        Key={"pk": raw["pk"], "sk": raw["sk"]},
                    )
                    deleted += 1
                last_key = response.get("LastEvaluatedKey")
                if not last_key:
                    break
                query["ExclusiveStartKey"] = last_key
    for username, task_id in rows:
        item = {
            "pk": f"USER#{username}",
            "sk": f"ASSIGNMENT#{task_id}",
            "entity": "assignment",
            "username": username,
            "task_id": task_id,
            "assigned_at": datetime.now(UTC).isoformat(),
        }
        dynamodb.put_item(
            TableName=table_name,
            Item={key: serializer.serialize(value) for key, value in item.items()},
        )
    return deleted


def main() -> int:
    args = parse_args()
    import boto3

    session = boto3.Session(profile_name=args.profile, region_name=args.region)
    outputs = stack_outputs(session.client("cloudformation"), args.stack_name)
    with tempfile.TemporaryDirectory(prefix="osworld-pilot-") as temp_dir:
        temporary_root = Path(temp_dir)
        pilot_root = (
            stage_dataset_round(
                args.dataset_root,
                args.dataset_round,
                temporary_root / "staged-pilot",
            )
            if args.dataset_root
            else args.pilot_root.resolve()
        )
        catalog = TaskCatalog.load(
            packages_path=pilot_root / "reference_packages.json",
            skills_path=pilot_root / "skill_pool.json",
            reviews_path=pilot_root / "reference_package_reviews.json",
            allow_pending=args.allow_pending,
        )
        task_ids = {task.task_id for task in catalog.all()}
        assignments = load_assignments(args.assignments.resolve(), task_ids)
        archive = temporary_root / "pilot.tar.gz"
        digest = build_snapshot(pilot_root, archive)
        bucket = outputs["AnnotationBucketName"]
        key = f"task-batches/pilot-{digest}.tar.gz"
        s3 = session.client("s3")
        s3.upload_file(
            str(archive),
            bucket,
            key,
            ExtraArgs={"Metadata": {"sha256": digest}, "ServerSideEncryption": "AES256"},
        )
        if s3.head_object(Bucket=bucket, Key=key).get("Metadata", {}).get("sha256") != digest:
            raise RuntimeError("Uploaded pilot snapshot metadata verification failed")
        install_snapshot(
            session.client("ssm"),
            instance_id=outputs["GatewayInstanceId"],
            bucket=bucket,
            key=key,
            sha256=digest,
            allow_pending=args.allow_pending,
        )
    deleted_assignments = put_assignments(
        session.client("dynamodb"),
        outputs["StateTableName"],
        assignments,
        replace=args.replace_assignments,
    )
    print(
        json.dumps(
            {
                "catalog_version": digest,
                "task_count": len(task_ids),
                "assignment_count": len(assignments),
                "deleted_assignment_count": deleted_assignments,
                "gateway_restarted": False,
                "s3_uri": f"s3://{bucket}/{key}",
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
