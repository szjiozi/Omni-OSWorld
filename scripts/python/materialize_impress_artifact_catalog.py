#!/usr/bin/env python3
"""Materialize trusted source/native artifacts for deferred Impress skills."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from benchmark_construction.impress_artifact_catalog import (
    load_frozen_source_tasks,
    load_impress_artifact_catalog,
    materialize_impress_artifact_catalog,
)


DEFAULT_ROOT = REPO_ROOT / "evaluation_examples/expert_skill_learning/impress_full_v1"
DEFAULT_CATALOG = DEFAULT_ROOT / "deferred_skill_artifact_catalog.json"
DEFAULT_SCHEMA = (
    REPO_ROOT
    / "evaluation_examples/expert_skill_learning/schemas/impress-deferred-artifact-catalog.schema.json"
)
DEFAULT_SKILLS = DEFAULT_ROOT / "generated_v2/skill_pool.json"
DEFAULT_READINESS = DEFAULT_ROOT / "generated_v2/skill_readiness_policy.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--skills", type=Path, default=DEFAULT_SKILLS)
    parser.add_argument("--readiness", type=Path, default=DEFAULT_READINESS)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_ROOT / "materialized_deferred_artifacts",
    )
    parser.add_argument(
        "--allow-external-relationships",
        action="store_true",
        help="Allow linked resources in source PPTX files after reporting them.",
    )
    return parser.parse_args()


def _load_ids(args: argparse.Namespace) -> tuple[set[str], set[str]]:
    skills = json.loads(args.skills.read_text(encoding="utf-8"))["skills"]
    known = {item["skill_id"] for item in skills}
    readiness = json.loads(args.readiness.read_text(encoding="utf-8"))
    deferred = {item["skill_id"] for item in readiness["overrides"]}
    return known, deferred


def main() -> int:
    args = parse_args()
    known, deferred = _load_ids(args)
    catalog = load_impress_artifact_catalog(
        args.catalog,
        schema_path=args.schema,
        known_skill_ids=known,
        required_skill_ids=deferred,
    )
    source_manifest = REPO_ROOT / catalog["source_manifest"]
    source_tasks = load_frozen_source_tasks(source_manifest, repo_root=REPO_ROOT)
    manifest = materialize_impress_artifact_catalog(
        catalog,
        source_tasks,
        args.output_dir,
        allow_external_relationships=args.allow_external_relationships,
    )
    print(
        f"Materialized {len(manifest['strategies'])} Impress artifact strategies "
        f"under {args.output_dir}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
