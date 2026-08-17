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
from benchmark_construction.reference_generation import load_skill_pool
from benchmark_construction.skill_extraction import (
    extract_skills,
    extract_skills_checkpointed,
    write_skill_pool,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract source-grounded app-operation skills from Calc tasks."
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
    parser.add_argument(
        "--existing-skill-pool",
        type=Path,
        help="Reuse records for source task IDs already present in this pool.",
    )
    parser.add_argument(
        "--checkpoint-dir",
        type=Path,
        help="Write one durable extraction response per source task.",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Reuse checkpoint files whose prompt hash still matches.",
    )
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
                "Provide --source-manifest, or provide --source-root with --task-id values"
            )
        paths = resolve_task_paths(args.source_root, args.task_id)
        tasks = [load_source_task(path, expected_app=args.app) for path in paths]
    if not tasks:
        raise SystemExit("No source tasks selected")
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
    existing_records = (
        load_skill_pool(args.existing_skill_pool, expected_app=args.app)
        if args.existing_skill_pool
        else []
    )
    selected_ids = {task.task_id for task in tasks}
    unknown_existing = {
        record.source_task_id for record in existing_records
    }.difference(selected_ids)
    if unknown_existing:
        raise SystemExit(
            "Existing skill pool contains source tasks absent from the manifest: "
            + ", ".join(sorted(unknown_existing))
        )
    existing_source_ids = {record.source_task_id for record in existing_records}
    pending_tasks = [task for task in tasks if task.task_id not in existing_source_ids]
    if args.checkpoint_dir:
        extracted, outcomes = await extract_skills_checkpointed(
            pending_tasks,
            client,
            checkpoint_dir=args.checkpoint_dir,
            resume=args.resume,
        )
    else:
        if args.resume:
            raise SystemExit("--resume requires --checkpoint-dir")
        extracted = await extract_skills(pending_tasks, client)
        outcomes = [
            {
                "task_id": task.task_id,
                "decision": "skills_extracted",
                "decision_reason": "",
                "skill_ids": [
                    record.skill_id
                    for record in extracted
                    if record.source_task_id == task.task_id
                ],
                "checkpoint": None,
                "reused_checkpoint": False,
            }
            for task in pending_tasks
        ]
    outcome_by_id = {item["task_id"]: item for item in outcomes}
    for task in tasks:
        if task.task_id in existing_source_ids:
            outcome_by_id[task.task_id] = {
                "task_id": task.task_id,
                "decision": "skills_extracted",
                "decision_reason": "",
                "skill_ids": [
                    record.skill_id
                    for record in existing_records
                    if record.source_task_id == task.task_id
                ],
                "checkpoint": None,
                "reused_checkpoint": False,
                "reused_existing_skill_pool": True,
            }
    combined = [*existing_records, *extracted]
    ordered_outcomes = [outcome_by_id[task.task_id] for task in tasks]
    write_skill_pool(
        args.output,
        combined,
        source_task_outcomes=ordered_outcomes,
    )
    records = combined
    print(f"Wrote {len(records)} skills to {args.output}")
    print(
        f"Reused {len(existing_source_ids)} source task(s); "
        f"extracted {len(pending_tasks)} source task(s)"
    )
    print(f"Per-attempt call log: {args.call_log}")


def main() -> int:
    asyncio.run(run(parse_args()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
