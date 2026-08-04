#!/usr/bin/env python3
"""Extract source-grounded Calc skills from explicit OSWorld-Human tasks."""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from benchmark_construction.llm import LLMConfig, OpenAICompatibleAsyncClient
from benchmark_construction.osworld_human import (
    load_source_manifest,
    load_source_task,
    resolve_task_paths,
    verify_manifest_sources,
)
from benchmark_construction.pricing import DEFAULT_PRICING_PATH, PricingTable
from benchmark_construction.skill_extraction import extract_skills, write_skill_pool


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract English app-operation skills for the 3-task Calc pilot."
    )
    parser.add_argument(
        "--source-manifest",
        type=Path,
        default=None,
        help="Self-contained manifest with instruction and single_actions.",
    )
    parser.add_argument(
        "--source-root",
        type=Path,
        default=None,
        help="Optional OSWorld-Human root for raw-file verification or direct loading.",
    )
    parser.add_argument("--task-id", action="append")
    parser.add_argument("--app", default="libreoffice_calc")
    parser.add_argument("--model", default="gpt-5.6-terra")
    parser.add_argument("--base-url", default=None)
    parser.add_argument("--api-key-env", default="OPENAI_API_KEY")
    parser.add_argument("--concurrency", type=int, default=3)
    parser.add_argument(
        "--response-format",
        choices=("json_schema", "json_object", "text"),
        default="json_schema",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("results/expert_skill_learning/pilot_skill_pool.json"),
    )
    parser.add_argument(
        "--call-log",
        type=Path,
        default=Path("results/expert_skill_learning/llm_calls.jsonl"),
    )
    parser.add_argument(
        "--pricing",
        type=Path,
        default=DEFAULT_PRICING_PATH,
        help=(
            "Token pricing JSON. The default is OpenAI direct standard short-context "
            "pricing; compatible providers should supply their own table."
        ),
    )
    return parser.parse_args()


async def run(args: argparse.Namespace) -> None:
    if args.source_manifest:
        if args.task_id:
            raise SystemExit("Do not combine --source-manifest with --task-id")
        tasks = load_source_manifest(args.source_manifest, expected_app=args.app)
        if args.source_root:
            verify_manifest_sources(args.source_manifest, args.source_root)
    else:
        if args.source_root is None or not args.task_id:
            raise SystemExit(
                "Provide --source-manifest, or provide --source-root with three --task-id values"
            )
        if len(args.task_id) != 3:
            raise SystemExit("The current pilot requires exactly three --task-id values")
        paths = resolve_task_paths(args.source_root, args.task_id)
        tasks = [load_source_task(path, expected_app=args.app) for path in paths]
    if len(tasks) != 3:
        raise SystemExit("The current pilot source must contain exactly three tasks")
    config = LLMConfig(
        model=args.model,
        base_url=args.base_url,
        api_key_env=args.api_key_env,
        concurrency=args.concurrency,
        response_format=args.response_format,
    )
    client = OpenAICompatibleAsyncClient(
        config,
        call_log=args.call_log,
        pricing=PricingTable.from_path(args.pricing),
    )
    records = await extract_skills(tasks, client)
    write_skill_pool(args.output, records)
    print(f"Wrote {len(records)} skills to {args.output}")
    print(f"Per-attempt call log: {args.call_log}")


def main() -> int:
    asyncio.run(run(parse_args()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
