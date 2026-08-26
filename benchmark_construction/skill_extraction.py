"""Build skill-extraction requests and attach trusted local provenance."""

from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path
from typing import Any

from .llm import JSONRequest, OpenAICompatibleAsyncClient
from .models import SkillRecord, SourceTask
from .prompts import load_prompt, render_prompt
from .reference_applications import get_reference_application
from .schema import load_schema, validate_payload


PROMPT_ROOT = (
    Path(__file__).resolve().parents[1]
    / "evaluation_examples"
    / "expert_skill_learning"
    / "prompts"
)


def build_skill_request(
    task: SourceTask,
    *,
    prompt_root: Path = PROMPT_ROOT,
) -> JSONRequest:
    profile = get_reference_application(task.app)
    stem = profile.skill_prompt_stem
    system_prompt = load_prompt(prompt_root / f"{stem}.system.txt")
    user_template = load_prompt(prompt_root / f"{stem}.user.txt")
    indexed_steps = "\n".join(
        f"[{index}] {step}" for index, step in enumerate(task.single_steps)
    )
    user_prompt = render_prompt(
        user_template,
        {
            "TASK_INSTRUCTION": task.instruction,
            "SINGLE_STEPS": indexed_steps,
        },
    )
    return JSONRequest(
        prompt_name=f"{stem}.v1",
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        response_schema=load_schema("skill-extraction-response.schema.json"),
        schema_name="skill_extraction_response",
    )


def attach_skill_provenance(
    task: SourceTask,
    response: dict[str, Any],
) -> list[SkillRecord]:
    validate_payload(response, load_schema("skill-extraction-response.schema.json"))
    decision = response["decision"]
    reason = response["decision_reason"].strip()
    if decision == "skills_extracted":
        if reason:
            raise ValueError("skills_extracted must have an empty decision_reason")
        if not response["skills"]:
            raise ValueError("skills_extracted must return at least one skill")
    else:
        if not reason:
            raise ValueError("no_reusable_skill must explain the decision")
        if response["skills"]:
            raise ValueError("no_reusable_skill must return an empty skills array")
        return []
    records: list[SkillRecord] = []
    claimed_action_ids: set[int] = set()
    for index, skill in enumerate(response["skills"], start=1):
        action_ids = tuple(sorted(set(skill["action_ids"])))
        if action_ids[-1] >= len(task.single_steps):
            raise ValueError(
                f"Skill {index} references action {action_ids[-1]}, but task "
                f"{task.task_id} only has {len(task.single_steps)} actions"
            )
        overlaps = claimed_action_ids.intersection(action_ids)
        if overlaps:
            raise ValueError(
                f"Task {task.task_id} assigns action IDs to multiple skills: "
                f"{sorted(overlaps)}"
            )
        claimed_action_ids.update(action_ids)
        record = SkillRecord(
            skill_id=f"{task.task_id}.skill-{index:02d}",
            app=task.app,
            name=skill["name"],
            procedure=tuple(skill["procedure"]),
            efficiency_tip=skill["efficiency_tip"],
            source_task_id=task.task_id,
            source_action_ids=action_ids,
        )
        validate_payload(record.to_dict(), load_schema("skill-record.schema.json"))
        records.append(record)
    return records


async def extract_skills(
    tasks: list[SourceTask],
    client: OpenAICompatibleAsyncClient,
) -> list[SkillRecord]:
    requests = [build_skill_request(task) for task in tasks]
    results = await client.generate_many(requests)
    records: list[SkillRecord] = []
    for task, result in zip(tasks, results):
        records.extend(attach_skill_provenance(task, result.data))
    return records


def _write_json_atomic(path: Path, document: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(
        json.dumps(document, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


async def extract_skills_checkpointed(
    tasks: list[SourceTask],
    client: OpenAICompatibleAsyncClient,
    *,
    checkpoint_dir: Path,
    resume: bool,
) -> tuple[list[SkillRecord], list[dict[str, Any]]]:
    """Extract each task independently and retain every successful result."""

    async def process(task: SourceTask) -> tuple[list[SkillRecord], dict[str, Any]]:
        request = build_skill_request(task)
        checkpoint = checkpoint_dir / f"{task.task_id}.json"
        if resume and checkpoint.is_file():
            document = json.loads(checkpoint.read_text(encoding="utf-8"))
            if document.get("task_id") != task.task_id:
                raise ValueError(f"Checkpoint task ID mismatch: {checkpoint}")
            if document.get("prompt_sha256") != request.prompt_sha256:
                raise ValueError(f"Checkpoint prompt differs from current prompt: {checkpoint}")
            response = document.get("response")
            if not isinstance(response, dict):
                raise ValueError(f"Checkpoint has no response object: {checkpoint}")
            records = attach_skill_provenance(task, response)
            return records, {
                "task_id": task.task_id,
                "decision": response["decision"],
                "decision_reason": response["decision_reason"],
                "skill_ids": [record.skill_id for record in records],
                "checkpoint": str(checkpoint),
                "reused_checkpoint": True,
            }

        result = await client.generate_json(request)
        records = attach_skill_provenance(task, result.data)
        _write_json_atomic(
            checkpoint,
            {
                "schema_version": "1.0",
                "task_id": task.task_id,
                "app": task.app,
                "single_action_count": len(task.single_steps),
                "prompt_sha256": request.prompt_sha256,
                "request_id": result.request_id,
                "model": result.model,
                "usage": {
                    "input_tokens": result.usage.input_tokens,
                    "cached_input_tokens": result.usage.cached_input_tokens,
                    "output_tokens": result.usage.output_tokens,
                    "estimated_cost_usd": result.estimated_cost_usd,
                },
                "response": result.data,
            },
        )
        return records, {
            "task_id": task.task_id,
            "decision": result.data["decision"],
            "decision_reason": result.data["decision_reason"],
            "skill_ids": [record.skill_id for record in records],
            "checkpoint": str(checkpoint),
            "reused_checkpoint": False,
        }

    results = await asyncio.gather(
        *(process(task) for task in tasks), return_exceptions=True
    )
    failures = [item for item in results if isinstance(item, BaseException)]
    if failures:
        messages = "; ".join(f"{type(item).__name__}: {item}" for item in failures)
        raise RuntimeError(
            f"{len(failures)} skill-extraction task(s) failed; successful "
            f"checkpoints were retained: {messages}"
        )
    records: list[SkillRecord] = []
    outcomes: list[dict[str, Any]] = []
    for item in results:
        task_records, outcome = item
        records.extend(task_records)
        outcomes.append(outcome)
    return records, outcomes


def write_skill_pool(
    path: Path,
    records: list[SkillRecord],
    *,
    source_task_outcomes: list[dict[str, Any]] | None = None,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    document: dict[str, Any] = {
        "schema_version": "1.1" if source_task_outcomes is not None else "1.0",
        "skills": [item.to_dict() for item in records],
    }
    if source_task_outcomes is not None:
        document["source_task_outcomes"] = source_task_outcomes
    _write_json_atomic(path, document)
