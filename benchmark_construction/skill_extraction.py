"""Build skill-extraction requests and attach trusted local provenance."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .llm import JSONRequest, OpenAICompatibleAsyncClient
from .models import SkillRecord, SourceTask
from .prompts import load_prompt, render_prompt
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
    system_prompt = load_prompt(prompt_root / "extract_skills.system.txt")
    user_template = load_prompt(prompt_root / "extract_skills.user.txt")
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
        prompt_name="extract_skills.v1",
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


def write_skill_pool(path: Path, records: list[SkillRecord]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    document = {"schema_version": "1.0", "skills": [item.to_dict() for item in records]}
    path.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
