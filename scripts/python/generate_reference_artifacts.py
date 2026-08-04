#!/usr/bin/env python3
"""Generate Calc blueprints with an LLM and optionally build verified XLSX files."""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from benchmark_construction.artifact_generation import (
    generate_artifact_blueprints,
    load_artifact_blueprints,
    write_artifact_blueprints,
)
from benchmark_construction.llm import LLMConfig, OpenAICompatibleAsyncClient
from benchmark_construction.pricing import DEFAULT_PRICING_PATH, PricingTable
from benchmark_construction.reference_review import load_reference_packages


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate artifact blueprints and real XLSX files."
    )
    parser.add_argument("--packages", type=Path, action="append")
    parser.add_argument(
        "--blueprints-input",
        type=Path,
        help="Build existing validated blueprints without making LLM calls.",
    )
    parser.add_argument("--reference-task-id", action="append")
    parser.add_argument("--model", default="gpt-5.6-terra")
    parser.add_argument("--base-url", default=None)
    parser.add_argument("--api-key-env", default="OPENAI_API_KEY")
    parser.add_argument("--concurrency", type=int, default=3)
    parser.add_argument(
        "--blueprints-output",
        type=Path,
        default=Path("results/expert_skill_learning/artifact_blueprints.json"),
    )
    parser.add_argument(
        "--call-log",
        type=Path,
        default=Path("results/expert_skill_learning/artifact_llm_calls.jsonl"),
    )
    parser.add_argument("--pricing", type=Path, default=DEFAULT_PRICING_PATH)
    parser.add_argument("--build-output-dir", type=Path)
    parser.add_argument("--node", default="node")
    parser.add_argument(
        "--node-modules",
        type=Path,
        help="Directory containing @oai/artifact-tool for XLSX building.",
    )
    return parser.parse_args()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_artifacts(
    blueprint_results,
    output_dir: Path,
    *,
    node: str,
    node_modules: Path | None,
) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    builder_source = REPO_ROOT / "scripts" / "js" / "build_reference_artifact.mjs"
    manifest_entries = []
    with tempfile.TemporaryDirectory(prefix="reference-artifact-builder-") as tmp:
        runtime = Path(tmp)
        builder = runtime / builder_source.name
        shutil.copy2(builder_source, builder)
        if node_modules is not None:
            os.symlink(node_modules.resolve(), runtime / "node_modules")
        for result in blueprint_results:
            task_dir = output_dir / result.reference_task_id
            task_dir.mkdir(parents=True, exist_ok=True)
            blueprint_path = task_dir / "artifact_blueprint.json"
            blueprint_path.write_text(
                json.dumps(result.blueprint, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            workbook_path = task_dir / "initial_artifact.xlsx"
            preview_dir = task_dir / "previews"
            qa_path = task_dir / "artifact_qa.json"
            subprocess.run(
                [
                    node,
                    str(builder),
                    str(blueprint_path),
                    str(workbook_path),
                    str(preview_dir),
                    str(qa_path),
                ],
                check=True,
            )
            manifest_entries.append(
                {
                    "reference_task_id": result.reference_task_id,
                    "artifact_path": str(workbook_path),
                    "artifact_sha256": _sha256(workbook_path),
                    "blueprint_path": str(blueprint_path),
                    "qa_path": str(qa_path),
                    "manual_setup_required": bool(
                        result.blueprint["manual_setup_steps"]
                    ),
                    "manual_setup_steps": result.blueprint[
                        "manual_setup_steps"
                    ],
                }
            )
    manifest = {"schema_version": "1.0", "artifacts": manifest_entries}
    manifest_path = output_dir / "artifact_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return manifest


async def run(args: argparse.Namespace) -> int:
    if args.blueprints_input is not None:
        if args.packages:
            raise SystemExit("Use either --blueprints-input or --packages, not both")
        if args.build_output_dir is None:
            raise SystemExit("--blueprints-input requires --build-output-dir")
        results = load_artifact_blueprints(args.blueprints_input)
        build_artifacts(
            results,
            args.build_output_dir,
            node=args.node,
            node_modules=args.node_modules,
        )
        print(f"Built {len(results)} XLSX artifacts under {args.build_output_dir}")
        return 0
    if not args.packages:
        raise SystemExit("--packages is required when generating blueprints")
    packages = load_reference_packages(args.packages)
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
    client = OpenAICompatibleAsyncClient(
        LLMConfig(
            model=args.model,
            base_url=args.base_url,
            api_key_env=args.api_key_env,
            concurrency=args.concurrency,
        ),
        call_log=args.call_log,
        pricing=PricingTable.from_path(args.pricing),
    )
    results = await generate_artifact_blueprints(packages, client)
    write_artifact_blueprints(args.blueprints_output, results)
    print(f"Wrote {len(results)} blueprints to {args.blueprints_output}")
    if args.build_output_dir:
        build_artifacts(
            results,
            args.build_output_dir,
            node=args.node,
            node_modules=args.node_modules,
        )
        print(f"Built XLSX artifacts under {args.build_output_dir}")
    return 0


def main() -> int:
    return asyncio.run(run(parse_args()))


if __name__ == "__main__":
    raise SystemExit(main())
