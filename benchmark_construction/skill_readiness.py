"""Load explicit per-skill generation readiness without changing coverage."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Sequence

from .models import SkillRecord
from .schema import load_schema, validate_payload


def eligible_skill_ids(
    path: Path,
    skills: Sequence[SkillRecord],
    *,
    expected_app: str,
    statuses: Sequence[str],
) -> tuple[str, ...]:
    document = json.loads(path.read_text(encoding="utf-8"))
    validate_payload(document, load_schema("skill-readiness-policy.schema.json"))
    if document["app"] != expected_app:
        raise ValueError(
            f"Skill readiness app {document['app']!r}; expected {expected_app!r}"
        )
    skill_ids = {skill.skill_id for skill in skills}
    overrides = document["overrides"]
    override_ids = [item["skill_id"] for item in overrides]
    if len(override_ids) != len(set(override_ids)):
        raise ValueError("Skill readiness policy repeats a skill ID")
    unknown = set(override_ids).difference(skill_ids)
    if unknown:
        raise ValueError(f"Skill readiness policy has unknown IDs: {sorted(unknown)}")
    status_by_id = {
        item["skill_id"]: item["status"] for item in document["overrides"]
    }
    allowed = set(statuses)
    return tuple(
        skill.skill_id
        for skill in skills
        if status_by_id.get(skill.skill_id, document["default_status"]) in allowed
    )

