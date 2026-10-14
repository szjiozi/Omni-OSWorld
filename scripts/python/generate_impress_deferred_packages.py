#!/usr/bin/env python3
"""Generate Impress packages backed by trusted deferred-skill artifact strategies."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from benchmark_construction.llm import (
    JSONRequest,
    LLMConfig,
    OpenAICompatibleAsyncClient,
)
from benchmark_construction.osworld_human import load_source_manifest
from benchmark_construction.pricing import DEFAULT_PRICING_PATH, PricingTable
from benchmark_construction.reference_generation import (
    PROMPT_ROOT,
    SkillSample,
    load_skill_pool,
)
from benchmark_construction.reference_packages import (
    ReferencePackageGenerationResult,
    _lexical_similarity,
    _source_contribution,
    _skill_cards,
    validate_reference_package_response,
    write_reference_packages,
)
from benchmark_construction.reference_review import (
    compute_review_state,
    load_reference_packages,
    load_reference_reviews,
    write_reference_review_template,
)
from benchmark_construction.schema import load_schema
from benchmark_construction.prompts import load_prompt, render_prompt


DEFAULT_ROOT = REPO_ROOT / "evaluation_examples/expert_skill_learning/impress_full_v1"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-pool", type=Path, required=True)
    parser.add_argument("--source-manifest", type=Path, required=True)
    parser.add_argument(
        "--catalog",
        type=Path,
        default=DEFAULT_ROOT / "deferred_skill_artifact_catalog.json",
    )
    parser.add_argument(
        "--generation-plan",
        type=Path,
        default=DEFAULT_ROOT / "deferred_skill_generation_plan.json",
    )
    parser.add_argument("--materialized-strategies", type=Path, required=True)
    parser.add_argument("--previous-packages", type=Path, action="append")
    parser.add_argument("--reviews", type=Path)
    parser.add_argument("--generation-round", type=int, required=True)
    parser.add_argument(
        "--generation-group-id",
        action="append",
        help="Generate only the named deferred group; repeatable for smoke tests.",
    )
    parser.add_argument("--max-candidates", type=int, default=20)
    parser.add_argument("--task-id-prefix", default="reference-task-impress-full")
    parser.add_argument("--pilot-id", default="impress-reference-package-full-v2")
    parser.add_argument("--seed", type=int, default=20260805)
    parser.add_argument("--model", default="gpt-5.6-terra")
    parser.add_argument("--base-url", default=None)
    parser.add_argument("--api-key-env", default="OPENAI_API_KEY")
    parser.add_argument("--concurrency", type=int, default=4)
    parser.add_argument("--semantic-retries", type=int, default=2)
    parser.add_argument("--pricing", type=Path, default=DEFAULT_PRICING_PATH)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--run-output", type=Path, required=True)
    parser.add_argument("--call-log", type=Path, required=True)
    parser.add_argument("--reviews-output", type=Path, required=True)
    return parser.parse_args()


def _strategy_prompt_view(strategy: dict) -> dict:
    return {
        "strategy_id": strategy["strategy_id"],
        "skill_ids": strategy["skill_ids"],
        "source_task_id": strategy["source_task_id"],
        "native_profile": strategy["native_profile"],
        "setup_profiles": strategy["setup_profiles"],
        "expected_outputs": strategy["expected_outputs"],
        "adaptation_requirements": strategy["adaptation_requirements"],
        "validation_requirements": strategy["validation_requirements"],
    }


def _materialized_prompt_view(strategy: dict) -> dict:
    assets = []
    for asset in strategy["assets"]:
        validation = asset.get("validation", {})
        pptx = validation.get("pptx")
        assets.append(
            {
                "role": asset["role"],
                "guest_path": asset["guest_path"],
                "filename": Path(asset["local_path"]).name,
                "pptx_inspection": pptx,
            }
        )
    return {"strategy_id": strategy["strategy_id"], "assets": assets}


def _build_request(
    sample: SkillSample,
    source_tasks,
    strategies: list[dict],
    materialized: list[dict],
) -> JSONRequest:
    system_prompt = load_prompt(
        PROMPT_ROOT / "generate_impress_deferred_reference_package.system.txt"
    )
    template = load_prompt(
        PROMPT_ROOT / "generate_impress_deferred_reference_package.user.txt"
    )
    prompt = render_prompt(
        template,
        {
            "APP": sample.app,
            "SAMPLED_SKILLS": json.dumps(
                _skill_cards(sample), indent=2, ensure_ascii=False
            ),
            "ARTIFACT_STRATEGIES": json.dumps(
                [_strategy_prompt_view(item) for item in strategies],
                indent=2,
                ensure_ascii=False,
            ),
            "MATERIALIZED_ARTIFACTS": json.dumps(
                [_materialized_prompt_view(item) for item in materialized],
                indent=2,
                ensure_ascii=False,
            ),
            "SOURCE_INSTRUCTIONS": json.dumps(
                [task.instruction for task in source_tasks if task.app == sample.app],
                indent=2,
                ensure_ascii=False,
            ),
        },
    )
    return JSONRequest(
        prompt_name="generate_impress_deferred_reference_package.v1",
        system_prompt=system_prompt,
        user_prompt=prompt,
        response_schema=load_schema("reference-package-impress-candidate.schema.json"),
        schema_name="reference_package_candidate",
    )


def _load_plan(args: argparse.Namespace, skills) -> tuple[list[dict], dict, dict]:
    catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
    plan = json.loads(args.generation_plan.read_text(encoding="utf-8"))
    materialized = json.loads(args.materialized_strategies.read_text(encoding="utf-8"))
    skill_ids = {skill.skill_id for skill in skills}
    strategy_by_id = {item["strategy_id"]: item for item in catalog["entries"]}
    materialized_by_id = {
        item["strategy_id"]: item for item in materialized["strategies"]
    }
    deferred = {
        skill_id for item in catalog["entries"] for skill_id in item["skill_ids"]
    }
    covered_deferred: set[str] = set()
    group_ids: set[str] = set()
    for group in plan["groups"]:
        group_id = group["generation_group_id"]
        if group_id in group_ids:
            raise ValueError(f"Duplicate deferred generation group: {group_id}")
        group_ids.add(group_id)
        if not 2 <= len(group["skill_ids"]) <= 5:
            raise ValueError(f"Deferred group must contain 2-5 skills: {group_id}")
        unknown_skills = set(group["skill_ids"]) - skill_ids
        if unknown_skills:
            raise ValueError(
                f"Deferred group has unknown skills: {sorted(unknown_skills)}"
            )
        if len(group["artifact_strategy_ids"]) != len(
            set(group["artifact_strategy_ids"])
        ):
            raise ValueError(
                f"Deferred group has duplicate artifact strategies: {group_id}"
            )
        for strategy_id in group["artifact_strategy_ids"]:
            if (
                strategy_id not in strategy_by_id
                or strategy_id not in materialized_by_id
            ):
                raise ValueError(
                    f"Deferred group has unavailable strategy: {strategy_id}"
                )
        covered_deferred.update(set(group["skill_ids"]) & deferred)
    if covered_deferred != deferred:
        raise ValueError(
            "Deferred generation plan does not cover the catalog exactly: "
            f"missing={sorted(deferred - covered_deferred)}"
        )
    return plan["groups"], strategy_by_id, materialized_by_id


async def run(args: argparse.Namespace) -> int:
    if bool(args.previous_packages) != bool(args.reviews):
        raise SystemExit("Use --previous-packages and --reviews together")
    if args.max_candidates < 1 or args.max_candidates > 20:
        raise SystemExit("--max-candidates must be between 1 and 20")
    skills = load_skill_pool(args.skill_pool, expected_app="libreoffice_impress")
    skill_by_id = {skill.skill_id: skill for skill in skills}
    source_tasks = load_source_manifest(
        args.source_manifest, expected_app="libreoffice_impress"
    )
    initially_covered: set[str] = set()
    if args.previous_packages:
        previous = load_reference_packages(args.previous_packages)
        reviews = load_reference_reviews(args.reviews)
        state = compute_review_state(skills, previous, reviews)
        if state.pending_reference_task_ids:
            raise SystemExit(
                "Review every previous package before generating the deferred round; pending IDs: "
                + ", ".join(state.pending_reference_task_ids)
            )
        initially_covered.update(state.approved_skill_ids)

    groups, catalog_by_id, materialized_by_id = _load_plan(args, skills)
    if args.generation_group_id:
        requested_groups = set(args.generation_group_id)
        available_groups = {item["generation_group_id"] for item in groups}
        unknown_groups = requested_groups - available_groups
        if unknown_groups:
            raise SystemExit(
                "Unknown deferred generation groups: "
                + ", ".join(sorted(unknown_groups))
            )
        groups = [
            item for item in groups if item["generation_group_id"] in requested_groups
        ]
    catalog_deferred = {
        skill_id for entry in catalog_by_id.values() for skill_id in entry["skill_ids"]
    }
    needed_groups = [
        group
        for group in groups
        if set(group["skill_ids"]) & (catalog_deferred - initially_covered)
    ]
    if len(needed_groups) > args.max_candidates:
        needed_groups = needed_groups[: args.max_candidates]

    jobs = []
    for group in needed_groups:
        sample = SkillSample(
            app="libreoffice_impress",
            skills=tuple(skill_by_id[item] for item in group["skill_ids"]),
        )
        strategies = [catalog_by_id[item] for item in group["artifact_strategy_ids"]]
        materialized = [
            materialized_by_id[item] for item in group["artifact_strategy_ids"]
        ]
        jobs.append(
            (
                group,
                sample,
                _build_request(sample, source_tasks, strategies, materialized),
            )
        )

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
    initial_results = (
        await client.generate_many([item[2] for item in jobs]) if jobs else []
    )
    attempts = []
    packages = []
    candidate_covered: set[str] = set()
    source_for_app = [
        task for task in source_tasks if task.app == "libreoffice_impress"
    ]
    for (group, sample, base_request), initial_result in zip(jobs, initial_results):
        request = base_request
        result = initial_result
        for retry in range(args.semantic_retries + 1):
            try:
                validate_reference_package_response(sample, result.data)
                break
            except ValueError as exc:
                if retry >= args.semantic_retries:
                    raise
                request = JSONRequest(
                    prompt_name=base_request.prompt_name,
                    system_prompt=base_request.system_prompt,
                    user_prompt=base_request.user_prompt
                    + "\n\nReturn a complete corrected response. Local validation failed: "
                    + str(exc),
                    response_schema=base_request.response_schema,
                    schema_name=base_request.schema_name,
                )
                result = await client.generate_json(request)
        attempt_index = len(attempts) + 1
        attempts.append(
            {
                "attempt": attempt_index,
                "kind": "deferred_artifact_strategy",
                "parent_reference_task_id": None,
                "sampled_skill_ids": list(sample.skill_ids),
                "artifact_strategy_ids": group["artifact_strategy_ids"],
                "decision": result.data["decision"],
                "rejection_reason": result.data["rejection_reason"],
                "request_id": result.request_id,
                "prompt_sha256": request.prompt_sha256,
                "model": result.model,
                "input_tokens": result.usage.input_tokens,
                "cached_input_tokens": result.usage.cached_input_tokens,
                "output_tokens": result.usage.output_tokens,
                "estimated_cost_usd": result.estimated_cost_usd,
            }
        )
        if result.data["decision"] != "candidate":
            continue
        task_id = (
            f"{args.task_id_prefix}-r{args.generation_round:02d}-"
            f"{len(packages) + 1:03d}"
        )
        packages.append(
            {
                "reference_task_id": task_id,
                "generation_round": args.generation_round,
                "parent_reference_task_id": None,
                "app": "libreoffice_impress",
                "task_instruction": result.data["task_instruction"],
                "required_skill_ids": list(sample.skill_ids),
                "artifact_strategy_ids": group["artifact_strategy_ids"],
                "artifact_spec": result.data["artifact_spec"],
                "operator_guide": result.data["operator_guide"],
                "expected_incidental_operations": result.data[
                    "expected_incidental_operations"
                ],
                "review_status": "pending",
                "source_contribution": _source_contribution(sample, skills),
                "similarity_reference": {
                    "lexical": _lexical_similarity(
                        result.data["task_instruction"], source_for_app
                    ),
                    "semantic": None,
                },
                "generation": {
                    "attempt": attempt_index,
                    "kind": "deferred_artifact_strategy",
                    "request_id": result.request_id,
                    "prompt_sha256": request.prompt_sha256,
                },
            }
        )
        candidate_covered.update(sample.skill_ids)

    all_ids = tuple(skill.skill_id for skill in skills)
    unresolved = set(all_ids) - initially_covered - candidate_covered
    result = ReferencePackageGenerationResult(
        packages=tuple(packages),
        attempts=tuple(attempts),
        all_skill_ids=all_ids,
        initial_covered_skill_ids=tuple(
            item for item in all_ids if item in initially_covered
        ),
        candidate_covered_skill_ids=tuple(
            item for item in all_ids if item in candidate_covered
        ),
        unresolved_skill_ids=tuple(item for item in all_ids if item in unresolved),
        generation_eligible_skill_ids=tuple(
            item for item in all_ids if item in catalog_deferred
        ),
        generation_deferred_skill_ids=tuple(
            item for item in all_ids if item not in catalog_deferred
        ),
        semantic_batch=None,
    )
    write_reference_packages(
        args.output,
        args.run_output,
        result,
        pilot_id=args.pilot_id,
        app="libreoffice_impress",
        seed=args.seed,
        generation_round=args.generation_round,
        model=args.model,
        skill_pool_path=args.skill_pool,
    )
    added = write_reference_review_template(args.reviews_output, result.packages)
    print(f"Wrote {len(packages)} deferred Impress packages; added {added} reviews")
    return 0 if not (catalog_deferred - initially_covered - candidate_covered) else 2


def main() -> int:
    return asyncio.run(run(parse_args()))


if __name__ == "__main__":
    raise SystemExit(main())
