#!/usr/bin/env python3
"""Generate Chinese novice guides from frozen TASK_DETAIL.md documents."""

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
from benchmark_construction.reference_review import load_reference_packages
from benchmark_construction.reviewer_guide_generation import (
    ReviewerGuideJob,
    generate_reviewer_guides,
    write_reviewer_guides,
)


PILOT_ROOT = REPO_ROOT / "evaluation_examples/expert_skill_learning/pilot"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--packages",
        type=Path,
        action="append",
        default=None,
        help="Reference package JSON; may be repeated.",
    )
    parser.add_argument(
        "--task-detail-root",
        type=Path,
        default=PILOT_ROOT / "task_details",
    )
    parser.add_argument("--reference-task-id", action="append")
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
        "--output",
        type=Path,
        default=PILOT_ROOT / "reviewer_guides.json",
    )
    parser.add_argument(
        "--call-log",
        type=Path,
        default=Path("results/expert_skill_learning/reviewer_guide_llm_calls.jsonl"),
    )
    parser.add_argument("--pricing", type=Path, default=DEFAULT_PRICING_PATH)
    return parser.parse_args()


async def run(args: argparse.Namespace) -> int:
    package_paths = args.packages or [PILOT_ROOT / "reference_packages.json"]
    packages = load_reference_packages(package_paths)
    if args.reference_task_id:
        selected = set(args.reference_task_id)
        packages = [
            package
            for package in packages
            if package["reference_task_id"] in selected
        ]
        found = {package["reference_task_id"] for package in packages}
        missing = selected.difference(found)
        if missing:
            raise SystemExit(f"Unknown reference task IDs: {sorted(missing)}")
    if not packages:
        raise SystemExit("No reference packages selected")

    jobs = []
    for package in packages:
        task_id = package["reference_task_id"]
        detail_path = args.task_detail_root / task_id / "TASK_DETAIL.md"
        if not detail_path.is_file():
            raise SystemExit(
                f"Missing {detail_path}; run manage_reference_review_packets.py "
                "details first"
            )
        jobs.append(
            ReviewerGuideJob(
                reference_task_id=task_id,
                required_skill_ids=tuple(package["required_skill_ids"]),
                task_detail_path=detail_path,
            )
        )

    client = OpenAICompatibleAsyncClient(
        LLMConfig(
            model=args.model,
            base_url=args.base_url,
            api_key_env=args.api_key_env,
            concurrency=args.concurrency,
            response_format=args.response_format,
        ),
        call_log=args.call_log,
        pricing=PricingTable.from_path(args.pricing),
    )
    results = await generate_reviewer_guides(jobs, client)
    write_reviewer_guides(args.output, results)
    print(f"Wrote {len(results)} reviewer guides to {args.output}")
    print(f"Per-attempt call log: {args.call_log}")
    return 0


def main() -> int:
    return asyncio.run(run(parse_args()))


if __name__ == "__main__":
    raise SystemExit(main())
