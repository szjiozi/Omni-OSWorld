#!/usr/bin/env python3
"""Generate or resume reviewable reference packages with semantic similarity."""

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
from benchmark_construction.reference_generation import load_skill_pool
from benchmark_construction.reference_packages import (
    generate_reference_packages,
    write_reference_packages,
)
from benchmark_construction.reference_review import (
    compute_review_state,
    load_reference_packages,
    load_reference_reviews,
    write_reference_review_template,
)
from benchmark_construction.semantic_similarity import (
    EmbeddingConfig,
    OpenAIEmbeddingAsyncClient,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate Calc reference task/artifact/operator packages."
    )
    parser.add_argument("--skill-pool", type=Path, required=True)
    parser.add_argument("--source-manifest", type=Path, required=True)
    parser.add_argument("--previous-packages", type=Path, action="append")
    parser.add_argument("--reviews", type=Path)
    parser.add_argument("--app", default="libreoffice_calc")
    parser.add_argument("--pilot-id", default="calc-reference-package-pilot-v2")
    parser.add_argument("--generation-round", type=int, default=1)
    parser.add_argument("--seed", type=int, default=20260805)
    parser.add_argument("--max-attempts", type=int, default=24)
    parser.add_argument(
        "--max-candidates",
        type=int,
        default=20,
        help="Maximum accepted candidate packages in this generation round.",
    )
    parser.add_argument(
        "--task-id-prefix",
        default="reference-task",
        help="Prefix before -rNN-NNN in generated reference task IDs.",
    )
    parser.add_argument(
        "--initial-covered-packages",
        type=Path,
        action="append",
        help=(
            "Packages with already completed annotations; their required skills "
            "start this run covered without being regenerated."
        ),
    )
    parser.add_argument("--model", default="gpt-5.6-terra")
    parser.add_argument("--embedding-model", default="text-embedding-3-small")
    parser.add_argument("--skip-semantic-similarity", action="store_true")
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
        default=Path("results/expert_skill_learning/reference_packages.json"),
    )
    parser.add_argument(
        "--run-output",
        type=Path,
        default=Path(
            "results/expert_skill_learning/reference_package_generation_run.json"
        ),
    )
    parser.add_argument(
        "--call-log",
        type=Path,
        default=Path(
            "results/expert_skill_learning/reference_package_llm_calls.jsonl"
        ),
    )
    parser.add_argument(
        "--embedding-call-log",
        type=Path,
        default=Path(
            "results/expert_skill_learning/semantic_similarity_calls.jsonl"
        ),
    )
    parser.add_argument(
        "--reviews-output",
        type=Path,
        default=Path(
            "results/expert_skill_learning/reference_package_reviews.json"
        ),
        help=(
            "Create or extend a human-fillable review form without overwriting "
            "existing review entries."
        ),
    )
    parser.add_argument("--pricing", type=Path, default=DEFAULT_PRICING_PATH)
    return parser.parse_args()


async def run(args: argparse.Namespace) -> int:
    if bool(args.previous_packages) != bool(args.reviews):
        raise SystemExit(
            "Use --previous-packages and --reviews together when resuming."
        )
    skills = load_skill_pool(args.skill_pool, expected_app=args.app)
    source_tasks = load_source_manifest(
        args.source_manifest, expected_app=args.app
    )
    initial_uncovered = None
    blocked_groups = ()
    revisions = ()
    if args.initial_covered_packages:
        legacy_packages = load_reference_packages(args.initial_covered_packages)
        skill_ids = {skill.skill_id for skill in skills}
        initial_covered = {
            skill_id
            for package in legacy_packages
            for skill_id in package["required_skill_ids"]
        }
        unknown = initial_covered.difference(skill_ids)
        if unknown:
            raise SystemExit(
                "Initial covered packages reference unknown skills: "
                + ", ".join(sorted(unknown))
            )
        initial_uncovered = [
            skill.skill_id
            for skill in skills
            if skill.skill_id not in initial_covered
        ]
    if args.previous_packages:
        packages = load_reference_packages(args.previous_packages)
        reviews = load_reference_reviews(args.reviews)
        state = compute_review_state(skills, packages, reviews)
        if state.pending_reference_task_ids:
            raise SystemExit(
                "Review every previous package before resuming; pending IDs: "
                + ", ".join(state.pending_reference_task_ids)
            )
        initial_uncovered = state.unresolved_skill_ids
        blocked_groups = state.blocked_groups
        revisions = state.revisions

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
    semantic_client = None
    if not args.skip_semantic_similarity:
        semantic_client = OpenAIEmbeddingAsyncClient(
            EmbeddingConfig(
                model=args.embedding_model,
                base_url=args.base_url,
                api_key_env=args.api_key_env,
            ),
            call_log=args.embedding_call_log,
            pricing=pricing,
        )
    result = await generate_reference_packages(
        skills,
        source_tasks,
        client,
        seed=args.seed,
        generation_round=args.generation_round,
        max_attempts=args.max_attempts,
        max_candidates=args.max_candidates,
        task_id_prefix=args.task_id_prefix,
        initial_uncovered_skill_ids=initial_uncovered,
        blocked_groups=blocked_groups,
        revisions=revisions,
        semantic_client=semantic_client,
    )
    write_reference_packages(
        args.output,
        args.run_output,
        result,
        pilot_id=args.pilot_id,
        app=args.app,
        seed=args.seed,
        generation_round=args.generation_round,
        model=args.model,
        skill_pool_path=args.skill_pool,
    )
    added_reviews = write_reference_review_template(
        args.reviews_output, result.packages
    )
    print(f"Wrote {len(result.packages)} packages to {args.output}")
    print(f"Generation metadata: {args.run_output}")
    print(
        f"Review form: {args.reviews_output} "
        f"({added_reviews} new entries)"
    )
    if result.unresolved_skill_ids:
        print(f"Unresolved candidate skills: {len(result.unresolved_skill_ids)}")
        return 2
    print(f"Candidate coverage complete for {len(result.all_skill_ids)} skills")
    return 0


def main() -> int:
    return asyncio.run(run(parse_args()))


if __name__ == "__main__":
    raise SystemExit(main())
