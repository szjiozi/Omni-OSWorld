"""Versioned token-price lookup and deterministic cost estimation."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PRICING_PATH = (
    REPO_ROOT
    / "evaluation_examples"
    / "expert_skill_learning"
    / "pricing"
    / "openai_standard_short_context_2026-08-04.json"
)


@dataclass(frozen=True)
class TokenUsage:
    input_tokens: int
    output_tokens: int
    cached_input_tokens: int = 0

    def __post_init__(self) -> None:
        if min(self.input_tokens, self.output_tokens, self.cached_input_tokens) < 0:
            raise ValueError("Token counts must be non-negative")
        if self.cached_input_tokens > self.input_tokens:
            raise ValueError("cached_input_tokens cannot exceed input_tokens")


class PricingTable:
    def __init__(self, document: dict[str, Any]) -> None:
        self.document = document
        self.models = document.get("models", {})

    @classmethod
    def from_path(cls, path: Path = DEFAULT_PRICING_PATH) -> "PricingTable":
        return cls(json.loads(path.read_text(encoding="utf-8")))

    def estimate_usd(self, model: str, usage: TokenUsage) -> float | None:
        rates = self.models.get(model)
        if rates is None:
            return None
        uncached = usage.input_tokens - usage.cached_input_tokens
        total = (
            uncached * rates["input_per_million"]
            + usage.cached_input_tokens * rates["cached_input_per_million"]
            + usage.output_tokens * rates["output_per_million"]
        ) / 1_000_000
        return round(total, 12)
