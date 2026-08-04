"""JSON Schema loading and validation helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA_ROOT = (
    REPO_ROOT / "evaluation_examples" / "expert_skill_learning" / "schemas"
)


def load_schema(name: str, *, schema_root: Path = DEFAULT_SCHEMA_ROOT) -> dict[str, Any]:
    path = schema_root / name
    schema = json.loads(path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return schema


def validate_payload(payload: Any, schema: dict[str, Any]) -> None:
    Draft202012Validator(schema).validate(payload)
