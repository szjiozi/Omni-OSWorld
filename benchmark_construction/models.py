"""Small, dependency-free data contracts used by benchmark construction."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


def _require_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value.strip()


@dataclass(frozen=True)
class SourceTask:
    """The only source content exposed to the construction LLM."""

    task_id: str
    app: str
    instruction: str
    single_steps: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_text(self.task_id, "task_id")
        _require_text(self.app, "app")
        _require_text(self.instruction, "instruction")
        if not self.single_steps:
            raise ValueError("single_steps must not be empty")
        for index, step in enumerate(self.single_steps):
            _require_text(step, f"single_steps[{index}]")

    def prompt_payload(self) -> dict[str, Any]:
        """Return the strict LLM input boundary: instruction and single steps."""

        return {
            "instruction": self.instruction,
            "single_steps": list(self.single_steps),
        }


@dataclass(frozen=True)
class SkillRecord:
    """A source-grounded app-operation skill shown to human annotators."""

    skill_id: str
    app: str
    name: str
    procedure: tuple[str, ...]
    efficiency_tip: str
    source_task_id: str
    source_action_ids: tuple[int, ...]

    def __post_init__(self) -> None:
        _require_text(self.skill_id, "skill_id")
        _require_text(self.app, "app")
        _require_text(self.name, "name")
        _require_text(self.efficiency_tip, "efficiency_tip")
        _require_text(self.source_task_id, "source_task_id")
        if not self.procedure:
            raise ValueError("procedure must not be empty")
        for index, step in enumerate(self.procedure):
            _require_text(step, f"procedure[{index}]")
        if not self.source_action_ids:
            raise ValueError("source_action_ids must not be empty")
        if any(not isinstance(index, int) or index < 0 for index in self.source_action_ids):
            raise ValueError("source_action_ids must contain non-negative integers")
        if tuple(sorted(set(self.source_action_ids))) != self.source_action_ids:
            raise ValueError("source_action_ids must be sorted and unique")

    @property
    def description(self) -> str:
        """Render the structured guide as a compact human-readable description."""

        numbered = " ".join(
            f"{index}. {step}" for index, step in enumerate(self.procedure, start=1)
        )
        return f"{numbered} Efficiency tip: {self.efficiency_tip}"

    def to_dict(self) -> dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "app": self.app,
            "name": self.name,
            "procedure": list(self.procedure),
            "efficiency_tip": self.efficiency_tip,
            "source": {
                "task_id": self.source_task_id,
                "action_ids": list(self.source_action_ids),
            },
        }
