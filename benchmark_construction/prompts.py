"""Load and render version-controlled text prompts."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Mapping


PLACEHOLDER = re.compile(r"{{([A-Z0-9_]+)}}")


def load_prompt(path: Path) -> str:
    if path.suffix != ".txt":
        raise ValueError(f"Prompt files must use .txt: {path}")
    return path.read_text(encoding="utf-8").strip()


def render_prompt(template: str, values: Mapping[str, str]) -> str:
    expected = set(PLACEHOLDER.findall(template))
    missing = expected.difference(values)
    extra = set(values).difference(expected)
    if missing:
        raise ValueError(f"Missing prompt values: {sorted(missing)}")
    if extra:
        raise ValueError(f"Unexpected prompt values: {sorted(extra)}")

    rendered = template
    for key, value in values.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", value)
    unresolved = PLACEHOLDER.findall(rendered)
    if unresolved:
        raise ValueError(f"Unresolved prompt placeholders: {sorted(set(unresolved))}")
    return rendered
