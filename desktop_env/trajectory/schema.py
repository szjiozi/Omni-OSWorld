"""Helpers for loading and validating the video-learning JSON schemas."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "1.0"
SCHEMA_NAMES = {
    "task": "task-extension.schema.json",
    "skill": "skill-ir.schema.json",
    "trajectory_event": "trajectory-event.schema.json",
}
SCHEMA_DIR = (
    Path(__file__).resolve().parents[2]
    / "evaluation_examples"
    / "video_learning"
    / "schemas"
)


@lru_cache(maxsize=None)
def load_schema(name: str) -> dict[str, Any]:
    """Load one bundled schema by its stable short name."""
    try:
        filename = SCHEMA_NAMES[name]
    except KeyError as exc:
        supported = ", ".join(sorted(SCHEMA_NAMES))
        raise ValueError(f"Unknown schema {name!r}; expected one of: {supported}") from exc

    with (SCHEMA_DIR / filename).open("r", encoding="utf-8") as schema_file:
        return json.load(schema_file)


def validate_document(document: Any, schema_name: str) -> None:
    """Validate a document and raise ``jsonschema.ValidationError`` on failure."""
    from jsonschema import Draft202012Validator, FormatChecker

    validator = Draft202012Validator(
        load_schema(schema_name),
        format_checker=FormatChecker(),
    )
    validator.validate(document)
