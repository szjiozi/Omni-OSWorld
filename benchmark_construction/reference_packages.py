"""Generate task, artifact, and operator-guide packages for human videos."""

from __future__ import annotations

import difflib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

from .llm import JSONRequest, JSONResult, OpenAICompatibleAsyncClient
from .models import SkillRecord, SourceTask
from .prompts import load_prompt, render_prompt
from .reference_generation import (
    PROMPT_ROOT,
    SIMILARITY_CHECKLIST,
    SeededCoverageSampler,
    SkillSample,
    _source_contribution,
)
from .schema import load_schema, validate_payload
from .semantic_similarity import (
    EmbeddingBatchResult,
    OpenAIEmbeddingAsyncClient,
    score_semantic_similarity,
)


PACKAGE_RESPONSE_SCHEMA = "reference-package-candidate.schema.json"


@dataclass(frozen=True)
class RevisionSample:
    sample: SkillSample
    parent_reference_task_id: str
    feedback: tuple[str, ...]


@dataclass(frozen=True)
class ReferencePackageGenerationResult:
    packages: tuple[dict[str, Any], ...]
    attempts: tuple[dict[str, Any], ...]
    all_skill_ids: tuple[str, ...]
    candidate_covered_skill_ids: tuple[str, ...]
    unresolved_skill_ids: tuple[str, ...]
    semantic_batch: EmbeddingBatchResult | None


def _skill_cards(sample: SkillSample) -> list[dict[str, Any]]:
    return [
        {
            "skill_id": skill.skill_id,
            "name": skill.name,
            "procedure": list(skill.procedure),
            "efficiency_tip": skill.efficiency_tip,
        }
        for skill in sample.skills
    ]


def build_reference_package_request(
    sample: SkillSample,
    source_tasks: Sequence[SourceTask],
    *,
    review_feedback: Sequence[str] = (),
    prompt_root: Path = PROMPT_ROOT,
) -> JSONRequest:
    source_instructions = [
        task.instruction for task in source_tasks if task.app == sample.app
    ]
    if not source_instructions:
        raise ValueError(f"No source instructions available for app {sample.app}")
    system_prompt = load_prompt(
        prompt_root / "generate_reference_package.system.txt"
    )
    user_template = load_prompt(
        prompt_root / "generate_reference_package.user.txt"
    )
    user_prompt = render_prompt(
        user_template,
        {
            "APP": sample.app,
            "SAMPLED_SKILLS": json.dumps(
                _skill_cards(sample), indent=2, ensure_ascii=False
            ),
            "SOURCE_INSTRUCTIONS": json.dumps(
                source_instructions, indent=2, ensure_ascii=False
            ),
            "REVIEW_FEEDBACK": json.dumps(
                list(review_feedback), indent=2, ensure_ascii=False
            ),
        },
    )
    return JSONRequest(
        prompt_name="generate_reference_package.v2",
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        response_schema=load_schema(PACKAGE_RESPONSE_SCHEMA),
        schema_name="reference_package_candidate",
    )


def validate_reference_package_response(
    sample: SkillSample, response: dict[str, Any]
) -> None:
    validate_payload(response, load_schema(PACKAGE_RESPONSE_SCHEMA))
    if response["decision"] == "rejected_combination":
        if response["task_instruction"].strip():
            raise ValueError("A rejected package must have an empty task instruction")
        if response["required_skill_ids"]:
            raise ValueError("A rejected package must not return skill IDs")
        if (
            response["artifact_spec"] is not None
            or response["operator_guide"] is not None
        ):
            raise ValueError("A rejected package must not contain package components")
        if response["expected_incidental_operations"]:
            raise ValueError(
                "A rejected package must not contain incidental operations"
            )
        if not response["rejection_reason"].strip():
            raise ValueError("A rejected package must explain the rejection")
        return

    if not response["task_instruction"].strip():
        raise ValueError("A candidate package must contain a task instruction")
    if response["rejection_reason"].strip():
        raise ValueError("A candidate package must have an empty rejection reason")
    if response["artifact_spec"] is None or response["operator_guide"] is None:
        raise ValueError("A candidate package must contain artifact and operator guides")

    expected = set(sample.skill_ids)
    returned_ids = response["required_skill_ids"]
    if set(returned_ids) != expected or len(returned_ids) != len(expected):
        raise ValueError("Candidate package skill IDs differ from the sampled set")
    guide_ids = [
        item["skill_id"]
        for item in response["operator_guide"]["recommended_demonstration"]
    ]
    if set(guide_ids) != expected or len(guide_ids) != len(expected):
        raise ValueError(
            "Operator guide must contain exactly one item per sampled skill"
        )

    artifact = response["artifact_spec"]
    sheet_names = [sheet["name"].strip() for sheet in artifact["sheets"]]
    if any(not name or len(name) > 31 for name in sheet_names):
        raise ValueError("Artifact sheet names must be non-empty and at most 31 chars")
    if len(set(sheet_names)) != len(sheet_names):
        raise ValueError("Artifact sheet names must be unique")
    for sheet in artifact["sheets"]:
        columns = [column["name"].strip() for column in sheet["columns"]]
        if any(not name for name in columns) or len(set(columns)) != len(columns):
            raise ValueError("Artifact column names must be non-empty and unique")


def _normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value.casefold()).strip()


def _lexical_similarity(
    instruction: str, source_tasks: Sequence[SourceTask]
) -> dict[str, Any]:
    normalized = _normalize(instruction)
    scores = [
        {
            "task_id": task.task_id,
            "sequence_similarity": round(
                difflib.SequenceMatcher(
                    None, normalized, _normalize(task.instruction)
                ).ratio(),
                6,
            ),
        }
        for task in source_tasks
    ]
    best = max(scores, key=lambda item: item["sequence_similarity"])
    return {
        "most_similar_source_task_id": best["task_id"],
        "max_sequence_similarity": best["sequence_similarity"],
        "exact_source_instruction_match": best["sequence_similarity"] == 1.0,
        "by_source_task": scores,
    }


def _attempt_record(
    attempt_index: int,
    sample: SkillSample,
    request: JSONRequest,
    result: JSONResult,
    *,
    kind: str,
    parent_reference_task_id: str | None,
) -> dict[str, Any]:
    return {
        "attempt": attempt_index,
        "kind": kind,
        "parent_reference_task_id": parent_reference_task_id,
        "sampled_skill_ids": list(sample.skill_ids),
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


async def generate_reference_packages(
    skills: Sequence[SkillRecord],
    source_tasks: Sequence[SourceTask],
    client: OpenAICompatibleAsyncClient,
    *,
    seed: int,
    generation_round: int = 1,
    max_attempts: int = 24,
    initial_uncovered_skill_ids: Sequence[str] | None = None,
    blocked_groups: Sequence[Sequence[str]] = (),
    revisions: Sequence[RevisionSample] = (),
    semantic_client: OpenAIEmbeddingAsyncClient | None = None,
) -> ReferencePackageGenerationResult:
    if generation_round < 1 or max_attempts < 1:
        raise ValueError("generation_round and max_attempts must be positive")
    skill_by_id = {skill.skill_id: skill for skill in skills}
    all_skill_ids = tuple(skill_by_id)
    uncovered = set(
        all_skill_ids
        if initial_uncovered_skill_ids is None
        else initial_uncovered_skill_ids
    )
    unknown = uncovered.difference(skill_by_id)
    if unknown:
        raise ValueError(f"Unknown initial uncovered skills: {sorted(unknown)}")

    revision_groups = [revision.sample.skill_ids for revision in revisions]
    sampler = SeededCoverageSampler(
        skills,
        seed=seed,
        blocked_groups=[*blocked_groups, *revision_groups],
    )
    packages: list[dict[str, Any]] = []
    attempts: list[dict[str, Any]] = []

    async def process_jobs(
        jobs: Sequence[tuple[SkillSample, Sequence[str], str, str | None]]
    ) -> None:
        requests = [
            build_reference_package_request(
                sample, source_tasks, review_feedback=feedback
            )
            for sample, feedback, _, _ in jobs
        ]
        results = await client.generate_many(requests)
        for job, request, result in zip(jobs, requests, results):
            sample, _, kind, parent_id = job
            validate_reference_package_response(sample, result.data)
            attempt_index = len(attempts) + 1
            attempts.append(
                _attempt_record(
                    attempt_index,
                    sample,
                    request,
                    result,
                    kind=kind,
                    parent_reference_task_id=parent_id,
                )
            )
            if result.data["decision"] != "candidate":
                continue
            task_id = (
                f"reference-task-r{generation_round:02d}-"
                f"{len(packages) + 1:03d}"
            )
            source_for_app = [
                task for task in source_tasks if task.app == sample.app
            ]
            packages.append(
                {
                    "reference_task_id": task_id,
                    "generation_round": generation_round,
                    "parent_reference_task_id": parent_id,
                    "app": sample.app,
                    "task_instruction": result.data["task_instruction"],
                    "required_skill_ids": list(sample.skill_ids),
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
                        "kind": kind,
                        "request_id": result.request_id,
                        "prompt_sha256": request.prompt_sha256,
                    },
                }
            )
            uncovered.difference_update(sample.skill_ids)

    revision_jobs = [
        (
            revision.sample,
            revision.feedback,
            "revision",
            revision.parent_reference_task_id,
        )
        for revision in revisions
        if set(revision.sample.skill_ids).intersection(uncovered)
    ]
    if revision_jobs:
        await process_jobs(revision_jobs[:max_attempts])

    while uncovered and len(attempts) < max_attempts:
        samples = sampler.sample_wave(
            uncovered, limit=max_attempts - len(attempts)
        )
        await process_jobs(
            [(sample, (), "new_combination", None) for sample in samples]
        )

    semantic_batch: EmbeddingBatchResult | None = None
    if packages and semantic_client is not None:
        source_for_app = [
            task for task in source_tasks if task.app == packages[0]["app"]
        ]
        reports, semantic_batch = await score_semantic_similarity(
            [package["task_instruction"] for package in packages],
            source_for_app,
            semantic_client,
        )
        for package, report in zip(packages, reports):
            package["similarity_reference"]["semantic"] = report

    covered = tuple(
        skill_id for skill_id in all_skill_ids if skill_id not in uncovered
    )
    unresolved = tuple(
        skill_id for skill_id in all_skill_ids if skill_id in uncovered
    )
    return ReferencePackageGenerationResult(
        packages=tuple(packages),
        attempts=tuple(attempts),
        all_skill_ids=all_skill_ids,
        candidate_covered_skill_ids=covered,
        unresolved_skill_ids=unresolved,
        semantic_batch=semantic_batch,
    )


def write_reference_packages(
    output_path: Path,
    run_path: Path,
    result: ReferencePackageGenerationResult,
    *,
    pilot_id: str,
    app: str,
    seed: int,
    generation_round: int,
    model: str,
    skill_pool_path: Path,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    run_path.parent.mkdir(parents=True, exist_ok=True)
    output_document = {
        "schema_version": "2.0",
        "pilot_id": pilot_id,
        "generation_round": generation_round,
        "app": app,
        "skill_pool": str(skill_pool_path),
        "candidate_coverage": {
            "all_skill_ids": list(result.all_skill_ids),
            "covered_skill_ids": list(result.candidate_covered_skill_ids),
            "unresolved_skill_ids": list(result.unresolved_skill_ids),
            "complete": not result.unresolved_skill_ids,
            "note": "Candidate coverage is not approved human-review coverage.",
        },
        "human_similarity_checklist": list(SIMILARITY_CHECKLIST),
        "reference_packages": list(result.packages),
    }
    generation_cost = sum(
        item["estimated_cost_usd"]
        for item in result.attempts
        if item["estimated_cost_usd"] is not None
    )
    embedding_cost = (
        result.semantic_batch.estimated_cost_usd
        if result.semantic_batch is not None
        else None
    )
    run_document = {
        "schema_version": "2.0",
        "pilot_id": pilot_id,
        "generation_round": generation_round,
        "seed": seed,
        "model": model,
        "status": "complete" if not result.unresolved_skill_ids else "unresolved",
        "attempt_count": len(result.attempts),
        "candidate_count": len(result.packages),
        "rejection_count": sum(
            item["decision"] == "rejected_combination"
            for item in result.attempts
        ),
        "generation_input_tokens": sum(
            item["input_tokens"] for item in result.attempts
        ),
        "generation_output_tokens": sum(
            item["output_tokens"] for item in result.attempts
        ),
        "generation_estimated_cost_usd": round(generation_cost, 12),
        "semantic_similarity": (
            {
                "model": result.semantic_batch.model,
                "request_id": result.semantic_batch.request_id,
                "input_tokens": result.semantic_batch.input_tokens,
                "estimated_cost_usd": embedding_cost,
            }
            if result.semantic_batch is not None
            else None
        ),
        "total_estimated_cost_usd": (
            round(generation_cost + embedding_cost, 12)
            if embedding_cost is not None
            else None
        ),
        "unresolved_skill_ids": list(result.unresolved_skill_ids),
        "attempts": list(result.attempts),
    }
    output_path.write_text(
        json.dumps(output_document, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    run_path.write_text(
        json.dumps(run_document, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
