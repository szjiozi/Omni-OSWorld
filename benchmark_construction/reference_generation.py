"""Generate coverage-oriented reference-task candidates from atomic skills."""

from __future__ import annotations

import difflib
import json
import random
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

from .llm import JSONRequest, JSONResult, OpenAICompatibleAsyncClient
from .models import SkillRecord, SourceTask
from .prompts import load_prompt, render_prompt
from .schema import load_schema, validate_payload


PROMPT_ROOT = (
    Path(__file__).resolve().parents[1]
    / "evaluation_examples"
    / "expert_skill_learning"
    / "prompts"
)
REFERENCE_RESPONSE_SCHEMA = "reference-task-candidate.schema.json"
SIMILARITY_CHECKLIST = (
    "The artifact, domain, object names, values, and layout differ materially "
    "from every source task.",
    "The instruction is a natural task rather than a list of skill names or UI steps.",
    "No distinctive source literal or complete ordered source solution is reproduced.",
    "Every required skill is necessary to complete the task rather than "
    "decorative or optional.",
)


@dataclass(frozen=True)
class SkillSample:
    """A same-application group proposed for one reference task."""

    app: str
    skills: tuple[SkillRecord, ...]

    def __post_init__(self) -> None:
        if not 2 <= len(self.skills) <= 5:
            raise ValueError("A reference task must sample 2-5 skills")
        ids = self.skill_ids
        if len(set(ids)) != len(ids):
            raise ValueError("A reference-task sample cannot repeat a skill")
        if any(skill.app != self.app for skill in self.skills):
            raise ValueError("All sampled skills must use the same application")

    @property
    def skill_ids(self) -> tuple[str, ...]:
        return tuple(skill.skill_id for skill in self.skills)


@dataclass(frozen=True)
class ReferenceGenerationResult:
    candidates: tuple[dict[str, Any], ...]
    attempts: tuple[dict[str, Any], ...]
    all_skill_ids: tuple[str, ...]
    covered_skill_ids: tuple[str, ...]
    unresolved_skill_ids: tuple[str, ...]


def load_skill_pool(
    path: Path, *, expected_app: str | None = None
) -> list[SkillRecord]:
    """Load locally trusted skill records and validate their persisted schema."""

    document = json.loads(path.read_text(encoding="utf-8"))
    entries = document.get("skills")
    if not isinstance(entries, list) or not entries:
        raise ValueError(f"{path} has no skills list")

    records: list[SkillRecord] = []
    seen_ids: set[str] = set()
    schema = load_schema("skill-record.schema.json")
    for entry in entries:
        validate_payload(entry, schema)
        source = entry["source"]
        record = SkillRecord(
            skill_id=entry["skill_id"],
            app=entry["app"],
            name=entry["name"],
            procedure=tuple(entry["procedure"]),
            efficiency_tip=entry["efficiency_tip"],
            source_task_id=source["task_id"],
            source_action_ids=tuple(source["action_ids"]),
        )
        if record.skill_id in seen_ids:
            raise ValueError(f"Duplicate skill ID in {path}: {record.skill_id}")
        if expected_app is not None and record.app != expected_app:
            raise ValueError(
                f"Skill {record.skill_id} has app {record.app!r}; "
                f"expected {expected_app!r}"
            )
        seen_ids.add(record.skill_id)
        records.append(record)
    return records


class SeededCoverageSampler:
    """Randomly group uncovered skills while making the run reproducible."""

    def __init__(
        self,
        skills: Sequence[SkillRecord],
        *,
        seed: int,
        blocked_groups: Sequence[Sequence[str]] = (),
    ) -> None:
        if len(skills) < 2:
            raise ValueError("Reference-task generation requires at least two skills")
        apps = {skill.app for skill in skills}
        if len(apps) != 1:
            raise ValueError("Run one SeededCoverageSampler per application")
        ids = [skill.skill_id for skill in skills]
        if len(set(ids)) != len(ids):
            raise ValueError("Skill IDs must be unique")
        self._skills = {skill.skill_id: skill for skill in skills}
        self._all_ids = tuple(ids)
        self._app = next(iter(apps))
        self._random = random.Random(seed)
        self._used_groups = {frozenset(group) for group in blocked_groups}
        unknown_blocked = set().union(*self._used_groups).difference(self._skills)
        if unknown_blocked:
            raise ValueError(
                f"Blocked groups contain unknown skill IDs: {sorted(unknown_blocked)}"
            )

    def _new_group(self, anchor: str, preferred: set[str]) -> tuple[str, ...]:
        max_size = min(5, len(self._all_ids))
        for _ in range(200):
            size = self._random.randint(2, max_size)
            preferred_others = sorted(preferred.difference({anchor}))
            fallback = sorted(set(self._all_ids).difference({anchor}, preferred))
            self._random.shuffle(preferred_others)
            self._random.shuffle(fallback)
            selected = [anchor]
            selected.extend((preferred_others + fallback)[: size - 1])
            key = frozenset(selected)
            if len(selected) == size and key not in self._used_groups:
                self._used_groups.add(key)
                return tuple(selected)
        raise RuntimeError("Could not sample a new 2-5 skill combination")

    def sample_wave(
        self,
        uncovered_skill_ids: set[str],
        *,
        limit: int,
    ) -> list[SkillSample]:
        unknown = uncovered_skill_ids.difference(self._skills)
        if unknown:
            raise ValueError(f"Unknown uncovered skill IDs: {sorted(unknown)}")
        if limit < 1:
            return []

        pending = set(uncovered_skill_ids)
        samples: list[SkillSample] = []
        while pending and len(samples) < limit:
            anchor = self._random.choice(sorted(pending))
            group_ids = self._new_group(anchor, pending)
            pending.difference_update(group_ids)
            skills = tuple(self._skills[skill_id] for skill_id in group_ids)
            samples.append(SkillSample(app=self._app, skills=skills))
        return samples


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


def build_reference_task_request(
    sample: SkillSample,
    source_tasks: Sequence[SourceTask],
    all_skills: Sequence[SkillRecord],
    *,
    prompt_root: Path = PROMPT_ROOT,
) -> JSONRequest:
    """Build a structured request without exposing source setup/evaluator fields."""

    source_instructions = [
        task.instruction for task in source_tasks if task.app == sample.app
    ]
    if not source_instructions:
        raise ValueError(f"No source instructions available for app {sample.app}")
    sampled_ids = set(sample.skill_ids)
    unsampled_skills = [
        {"skill_id": skill.skill_id, "name": skill.name}
        for skill in all_skills
        if skill.app == sample.app and skill.skill_id not in sampled_ids
    ]
    system_prompt = load_prompt(prompt_root / "generate_reference_task.system.txt")
    user_template = load_prompt(prompt_root / "generate_reference_task.user.txt")
    user_prompt = render_prompt(
        user_template,
        {
            "APP": sample.app,
            "SAMPLED_SKILLS": json.dumps(
                _skill_cards(sample), indent=2, ensure_ascii=False
            ),
            "UNSAMPLED_SKILLS": json.dumps(
                unsampled_skills, indent=2, ensure_ascii=False
            ),
            "SOURCE_INSTRUCTIONS": json.dumps(
                source_instructions, indent=2, ensure_ascii=False
            ),
        },
    )
    return JSONRequest(
        prompt_name="generate_reference_task.v1",
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        response_schema=load_schema(REFERENCE_RESPONSE_SCHEMA),
        schema_name="reference_task_candidate",
    )


def validate_reference_response(sample: SkillSample, response: dict[str, Any]) -> None:
    """Enforce sampled-skill coverage locally instead of trusting model IDs."""

    validate_payload(response, load_schema(REFERENCE_RESPONSE_SCHEMA))
    if response["decision"] != "candidate":
        if response["instruction"].strip():
            raise ValueError("A rejected combination must have an empty instruction")
        if response["required_skill_ids"]:
            raise ValueError("A rejected combination must not return skill IDs")
        if not response["rejection_reason"].strip():
            raise ValueError("A rejected combination must explain the rejection")
        return
    if not response["instruction"].strip():
        raise ValueError("A candidate must contain a non-empty instruction")
    if response["rejection_reason"].strip():
        raise ValueError("A candidate must have an empty rejection_reason")
    expected = set(sample.skill_ids)
    returned = set(response["required_skill_ids"])
    if returned != expected or len(response["required_skill_ids"]) != len(expected):
        missing = sorted(expected.difference(returned))
        unexpected = sorted(returned.difference(expected))
        raise ValueError(
            f"Candidate skill IDs differ from the sampled set; "
            f"missing={missing}, unexpected={unexpected}, "
            f"returned_count={len(response['required_skill_ids'])}"
        )


def _normalized_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.casefold()).strip()


def _source_contribution(
    sample: SkillSample,
    all_skills: Sequence[SkillRecord],
) -> dict[str, Any]:
    counts = Counter(skill.source_task_id for skill in sample.skills)
    source_pool_counts = Counter(skill.source_task_id for skill in all_skills)
    total = len(sample.skills)
    dominant_task_id, dominant_count = counts.most_common(1)[0]
    return {
        "by_source_task": [
            {
                "task_id": task_id,
                "skill_count": count,
                "skill_fraction": round(count / total, 6),
            }
            for task_id, count in sorted(counts.items())
        ],
        "dominant_source_task_id": dominant_task_id,
        "dominant_source_skill_fraction": round(dominant_count / total, 6),
        "complete_source_skill_sets_included": sorted(
            task_id
            for task_id, count in counts.items()
            if count == source_pool_counts[task_id]
        ),
    }


def _similarity_reference(
    instruction: str,
    source_tasks: Sequence[SourceTask],
) -> dict[str, Any]:
    normalized = _normalized_text(instruction)
    if not source_tasks:
        raise ValueError(
            "At least one source task is required for similarity reference"
        )
    scores = [
        (
            task.task_id,
            difflib.SequenceMatcher(
                None, normalized, _normalized_text(task.instruction)
            ).ratio(),
        )
        for task in source_tasks
    ]
    task_id, ratio = max(scores, key=lambda item: item[1])
    return {
        "most_similar_source_task_id": task_id,
        "instruction_sequence_similarity": round(ratio, 6),
        "exact_source_instruction_match": ratio == 1.0,
    }


def _attempt_record(
    attempt_index: int,
    sample: SkillSample,
    request: JSONRequest,
    result: JSONResult,
) -> dict[str, Any]:
    return {
        "attempt": attempt_index,
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


async def generate_reference_tasks(
    skills: Sequence[SkillRecord],
    source_tasks: Sequence[SourceTask],
    client: OpenAICompatibleAsyncClient,
    *,
    seed: int,
    max_attempts: int = 24,
) -> ReferenceGenerationResult:
    """Generate candidates until every skill is covered or attempts are exhausted."""

    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")
    sampler = SeededCoverageSampler(skills, seed=seed)
    all_skill_ids = tuple(skill.skill_id for skill in skills)
    uncovered = set(all_skill_ids)
    candidates: list[dict[str, Any]] = []
    attempts: list[dict[str, Any]] = []

    while uncovered and len(attempts) < max_attempts:
        remaining_budget = max_attempts - len(attempts)
        samples = sampler.sample_wave(uncovered, limit=remaining_budget)
        requests = [
            build_reference_task_request(sample, source_tasks, skills)
            for sample in samples
        ]
        results = await client.generate_many(requests)
        for sample, request, result in zip(samples, requests, results):
            validate_reference_response(sample, result.data)
            attempt_index = len(attempts) + 1
            attempts.append(_attempt_record(attempt_index, sample, request, result))
            if result.data["decision"] != "candidate":
                continue

            instruction = result.data["instruction"]
            reference_task_id = f"reference-task-{len(candidates) + 1:03d}"
            candidates.append(
                {
                    "reference_task_id": reference_task_id,
                    "app": sample.app,
                    "instruction": instruction,
                    "required_skill_ids": list(sample.skill_ids),
                    "review_status": "pending",
                    "source_contribution": _source_contribution(sample, skills),
                    "similarity_reference": _similarity_reference(
                        instruction,
                        [task for task in source_tasks if task.app == sample.app],
                    ),
                    "generation": {
                        "attempt": attempt_index,
                        "request_id": result.request_id,
                        "prompt_sha256": request.prompt_sha256,
                    },
                }
            )
            uncovered.difference_update(sample.skill_ids)

    covered = tuple(skill_id for skill_id in all_skill_ids if skill_id not in uncovered)
    unresolved = tuple(skill_id for skill_id in all_skill_ids if skill_id in uncovered)
    return ReferenceGenerationResult(
        candidates=tuple(candidates),
        attempts=tuple(attempts),
        all_skill_ids=all_skill_ids,
        covered_skill_ids=covered,
        unresolved_skill_ids=unresolved,
    )


def write_reference_generation(
    output_path: Path,
    run_path: Path,
    result: ReferenceGenerationResult,
    *,
    pilot_id: str,
    app: str,
    seed: int,
    model: str,
    skill_pool_path: Path,
) -> None:
    """Persist review candidates separately from model/cost attempt metadata."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    run_path.parent.mkdir(parents=True, exist_ok=True)
    candidate_document = {
        "schema_version": "1.0",
        "pilot_id": pilot_id,
        "app": app,
        "skill_pool": str(skill_pool_path),
        "candidate_coverage": {
            "all_skill_ids": list(result.all_skill_ids),
            "covered_skill_ids": list(result.covered_skill_ids),
            "unresolved_skill_ids": list(result.unresolved_skill_ids),
            "complete": not result.unresolved_skill_ids,
            "note": "Candidate coverage is not approved human-review coverage.",
        },
        "human_similarity_checklist": list(SIMILARITY_CHECKLIST),
        "reference_tasks": list(result.candidates),
    }
    total_cost = sum(
        attempt["estimated_cost_usd"]
        for attempt in result.attempts
        if attempt["estimated_cost_usd"] is not None
    )
    run_document = {
        "schema_version": "1.0",
        "pilot_id": pilot_id,
        "seed": seed,
        "model": model,
        "status": "complete" if not result.unresolved_skill_ids else "unresolved",
        "attempt_count": len(result.attempts),
        "candidate_count": len(result.candidates),
        "rejection_count": sum(
            attempt["decision"] == "rejected_combination"
            for attempt in result.attempts
        ),
        "input_tokens": sum(item["input_tokens"] for item in result.attempts),
        "cached_input_tokens": sum(
            item["cached_input_tokens"] for item in result.attempts
        ),
        "output_tokens": sum(item["output_tokens"] for item in result.attempts),
        "estimated_cost_usd": round(total_cost, 12),
        "pricing_complete": all(
            item["estimated_cost_usd"] is not None for item in result.attempts
        ),
        "unresolved_skill_ids": list(result.unresolved_skill_ids),
        "attempts": list(result.attempts),
    }
    output_path.write_text(
        json.dumps(candidate_document, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    run_path.write_text(
        json.dumps(run_document, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
