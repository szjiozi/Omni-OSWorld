#!/usr/bin/env python3
"""Generate constrained blueprints and safe OSWorld annotation configs."""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from benchmark_construction.llm import LLMConfig, OpenAICompatibleAsyncClient
from benchmark_construction.pricing import DEFAULT_PRICING_PATH, PricingTable
from benchmark_construction.reference_annotation import (
    generate_annotation_blueprints,
    load_annotation_blueprints,
    load_artifact_manifest,
    write_annotation_blueprints,
    write_annotation_configs,
)
from benchmark_construction.reference_review import load_reference_packages


PILOT_ROOT = REPO_ROOT / "evaluation_examples/expert_skill_learning/pilot"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate LLM setup blueprints, then inject trusted artifact paths "
            "and standard OSWorld upload/open actions."
        )
    )
    parser.add_argument(
        "--packages",
        type=Path,
        action="append",
        default=None,
        help="Reference package JSON; may be repeated.",
    )
    parser.add_argument(
        "--artifact-manifest",
        type=Path,
        default=PILOT_ROOT / "artifacts/artifact_manifest.json",
    )
    parser.add_argument("--reference-task-id", action="append")
    parser.add_argument(
        "--blueprints-input",
        type=Path,
        help="Assemble already generated blueprints without an LLM call.",
    )
    parser.add_argument("--model", default="gpt-5.6-terra")
    parser.add_argument("--base-url", default=None)
    parser.add_argument("--api-key-env", default="OPENAI_API_KEY")
    parser.add_argument("--concurrency", type=int, default=4)
    parser.add_argument(
        "--response-format",
        choices=("json_schema", "json_object", "text"),
        default="json_schema",
    )
    parser.add_argument(
        "--blueprints-output",
        type=Path,
        default=PILOT_ROOT / "annotation_setup_blueprints.json",
    )
    parser.add_argument(
        "--configs-output-dir",
        type=Path,
        default=PILOT_ROOT / "task_configs",
    )
    parser.add_argument(
        "--config-manifest-output",
        type=Path,
        default=PILOT_ROOT / "task_config_manifest.json",
    )
    parser.add_argument(
        "--call-log",
        type=Path,
        default=Path(
            "results/expert_skill_learning/annotation_config_llm_calls.jsonl"
        ),
    )
    parser.add_argument("--pricing", type=Path, default=DEFAULT_PRICING_PATH)
    return parser.parse_args()


async def run(args: argparse.Namespace) -> int:
    package_paths = args.packages or [PILOT_ROOT / "reference_packages.json"]
    packages = load_reference_packages(package_paths)
    artifact_by_id = load_artifact_manifest(args.artifact_manifest)

    if args.reference_task_id:
        selected = set(args.reference_task_id)
        packages = [
            package
            for package in packages
            if package["reference_task_id"] in selected
        ]
        missing = selected.difference(
            package["reference_task_id"] for package in packages
        )
        if missing:
            raise SystemExit(f"Unknown reference task IDs: {sorted(missing)}")
    if not packages:
        raise SystemExit("No reference packages selected")

    if args.blueprints_input:
        all_blueprints = load_annotation_blueprints(args.blueprints_input)
        selected_ids = {
            package["reference_task_id"] for package in packages
        }
        blueprints = [
            item
            for item in all_blueprints
            if item.reference_task_id in selected_ids
        ]
        found = {item.reference_task_id for item in blueprints}
        if found != selected_ids:
            raise SystemExit(
                "Blueprint input is missing task IDs: "
                f"{sorted(selected_ids.difference(found))}"
            )
    else:
        pricing = PricingTable.from_path(args.pricing)
        client = OpenAICompatibleAsyncClient(
            LLMConfig(
                model=args.model,
                base_url=args.base_url,
                api_key_env=args.api_key_env,
                concurrency=args.concurrency,
                response_format=args.response_format,
            ),
            call_log=args.call_log,
            pricing=pricing,
        )
        blueprints = await generate_annotation_blueprints(
            packages, artifact_by_id, client
        )
        write_annotation_blueprints(args.blueprints_output, blueprints)
        print(
            f"Wrote {len(blueprints)} annotation setup blueprints to "
            f"{args.blueprints_output}"
        )

    entries = write_annotation_configs(
        args.configs_output_dir,
        args.config_manifest_output,
        packages,
        artifact_by_id,
        blueprints,
        repo_root=REPO_ROOT,
    )
    print(
        f"Wrote {len(entries)} OSWorld task configs under "
        f"{args.configs_output_dir}"
    )
    print(f"Config manifest: {args.config_manifest_output}")
    return 0


def main() -> int:
    return asyncio.run(run(parse_args()))


if __name__ == "__main__":
    raise SystemExit(main())
