#!/usr/bin/env python3
"""Generate coverage-oriented reference-task candidates for human review."""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from benchmark_construction.llm import LLMConfig, OpenAICompatibleAsyncClient
from benchmark_construction.osworld_human import load_source_manifest
from benchmark_construction.pricing import DEFAULT_PRICING_PATH, PricingTable
from benchmark_construction.reference_generation import (
    generate_reference_tasks,
    load_skill_pool,
    write_reference_generation,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate same-app 2-5 skill reference tasks for the Calc pilot."
    )
    parser.add_argument(
        "--skill-pool",
        type=Path,
        required=True,
        help="Validated atomic skill_pool.json.",
    )
    parser.add_argument(
        "--source-manifest",
        type=Path,
        required=True,
        help="Source instructions used only for similarity avoidance.",
    )
    parser.add_argument("--app", default="libreoffice_calc")
    parser.add_argument("--pilot-id", default="calc-reference-task-pilot-v1")
    parser.add_argument("--seed", type=int, default=20260804)
    parser.add_argument("--max-attempts", type=int, default=24)
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
        default=Path("results/expert_skill_learning/reference_tasks.json"),
    )
    parser.add_argument(
        "--run-output",
        type=Path,
        default=Path(
            "results/expert_skill_learning/reference_task_generation_run.json"
        ),
    )
    parser.add_argument(
        "--call-log",
        type=Path,
        default=Path("results/expert_skill_learning/reference_task_llm_calls.jsonl"),
    )
    parser.add_argument("--pricing", type=Path, default=DEFAULT_PRICING_PATH)
    return parser.parse_args()


async def run(args: argparse.Namespace) -> int:
    skills = load_skill_pool(args.skill_pool, expected_app=args.app)
    source_tasks = load_source_manifest(
        args.source_manifest, expected_app=args.app
    )
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
    result = await generate_reference_tasks(
        skills,
        source_tasks,
        client,
        seed=args.seed,
        max_attempts=args.max_attempts,
    )
    write_reference_generation(
        args.output,
        args.run_output,
        result,
        pilot_id=args.pilot_id,
        app=args.app,
        seed=args.seed,
        model=args.model,
        skill_pool_path=args.skill_pool,
    )
    print(f"Wrote {len(result.candidates)} candidates to {args.output}")
    print(f"Generation metadata: {args.run_output}")
    print(f"Per-attempt call log: {args.call_log}")
    if result.unresolved_skill_ids:
        print(f"Unresolved skills: {len(result.unresolved_skill_ids)}")
        return 2
    print(f"Candidate coverage complete for {len(result.all_skill_ids)} skills")
    return 0


def main() -> int:
    return asyncio.run(run(parse_args()))


if __name__ == "__main__":
    raise SystemExit(main())
