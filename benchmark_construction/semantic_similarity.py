"""Embedding-based semantic similarity with auditable OpenAI-compatible calls."""

from __future__ import annotations

import json
import math
import os
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

from .llm import JsonlCallLogger, _field
from .models import SourceTask
from .pricing import PricingTable


@dataclass(frozen=True)
class EmbeddingConfig:
    model: str = "text-embedding-3-small"
    base_url: str | None = None
    api_key_env: str = "OPENAI_API_KEY"
    dimensions: int | None = None

    def __post_init__(self) -> None:
        if self.dimensions is not None and self.dimensions < 1:
            raise ValueError("dimensions must be positive")


@dataclass(frozen=True)
class EmbeddingBatchResult:
    request_id: str
    model: str
    vectors: tuple[tuple[float, ...], ...]
    input_tokens: int
    estimated_cost_usd: float | None


class OpenAIEmbeddingAsyncClient:
    def __init__(
        self,
        config: EmbeddingConfig,
        *,
        call_log: Path,
        pricing: PricingTable | None = None,
        client: Any | None = None,
    ) -> None:
        self.config = config
        self.pricing = pricing or PricingTable.from_path()
        self.logger = JsonlCallLogger(call_log)
        self._client = client or self._build_client()

    def _build_client(self) -> Any:
        try:
            from openai import AsyncOpenAI
        except ImportError as exc:
            raise RuntimeError("AsyncOpenAI is unavailable") from exc
        api_key = os.environ.get(self.config.api_key_env)
        if not api_key:
            raise RuntimeError(
                f"Required API key environment variable is not set: "
                f"{self.config.api_key_env}"
            )
        kwargs: dict[str, Any] = {"api_key": api_key}
        if self.config.base_url:
            kwargs["base_url"] = self.config.base_url
        return AsyncOpenAI(**kwargs)

    async def embed(self, texts: Sequence[str]) -> EmbeddingBatchResult:
        if not texts or any(
            not isinstance(text, str) or not text.strip() for text in texts
        ):
            raise ValueError("Embedding input must contain non-empty strings")
        request_id = str(uuid.uuid4())
        timestamp = datetime.now(timezone.utc).isoformat()
        started = time.monotonic()
        kwargs: dict[str, Any] = {
            "model": self.config.model,
            "input": list(texts),
            "encoding_format": "float",
        }
        if self.config.dimensions is not None:
            kwargs["dimensions"] = self.config.dimensions
        try:
            response = await self._client.embeddings.create(**kwargs)
            data = sorted(
                _field(response, "data", []),
                key=lambda item: _field(item, "index", 0),
            )
            vectors = tuple(
                tuple(float(value) for value in _field(item, "embedding", []))
                for item in data
            )
            if len(vectors) != len(texts) or any(not vector for vector in vectors):
                raise ValueError("Embedding response does not match the input batch")
            usage = _field(response, "usage", {}) or {}
            input_tokens = int(
                _field(
                    usage,
                    "prompt_tokens",
                    _field(usage, "total_tokens", 0),
                )
                or 0
            )
            cost = self.pricing.estimate_embedding_usd(
                self.config.model, input_tokens
            )
            await self.logger.append(
                {
                    "request_id": request_id,
                    "timestamp": timestamp,
                    "operation": "embeddings.create",
                    "model": self.config.model,
                    "status": "success",
                    "input_count": len(texts),
                    "input_tokens": input_tokens,
                    "dimensions": len(vectors[0]),
                    "latency_seconds": round(time.monotonic() - started, 6),
                    "estimated_cost_usd": cost,
                    "pricing_known": cost is not None,
                    "pricing_version": self.pricing.document.get("version"),
                }
            )
            return EmbeddingBatchResult(
                request_id=request_id,
                model=self.config.model,
                vectors=vectors,
                input_tokens=input_tokens,
                estimated_cost_usd=cost,
            )
        except Exception as exc:
            await self.logger.append(
                {
                    "request_id": request_id,
                    "timestamp": timestamp,
                    "operation": "embeddings.create",
                    "model": self.config.model,
                    "status": "failed",
                    "input_count": len(texts),
                    "latency_seconds": round(time.monotonic() - started, 6),
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                }
            )
            raise


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    if len(left) != len(right) or not left:
        raise ValueError("Cosine inputs must have the same non-zero dimensions")
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(value * value for value in left))
    right_norm = math.sqrt(sum(value * value for value in right))
    if left_norm == 0 or right_norm == 0:
        raise ValueError("Cosine inputs must have non-zero norms")
    return dot / (left_norm * right_norm)


async def score_semantic_similarity(
    candidate_instructions: Sequence[str],
    source_tasks: Sequence[SourceTask],
    client: OpenAIEmbeddingAsyncClient,
) -> tuple[list[dict[str, Any]], EmbeddingBatchResult]:
    if not candidate_instructions:
        raise ValueError("At least one candidate instruction is required")
    if not source_tasks:
        raise ValueError("At least one source task is required")
    texts = list(candidate_instructions) + [
        task.instruction for task in source_tasks
    ]
    batch = await client.embed(texts)
    split = len(candidate_instructions)
    candidate_vectors = batch.vectors[:split]
    source_vectors = batch.vectors[split:]
    reports: list[dict[str, Any]] = []
    for vector in candidate_vectors:
        scores = [
            {
                "task_id": task.task_id,
                "cosine_similarity": round(
                    cosine_similarity(vector, source_vector), 6
                ),
            }
            for task, source_vector in zip(source_tasks, source_vectors)
        ]
        most_similar = max(scores, key=lambda item: item["cosine_similarity"])
        reports.append(
            {
                "model": batch.model,
                "most_similar_source_task_id": most_similar["task_id"],
                "max_cosine_similarity": most_similar["cosine_similarity"],
                "by_source_task": scores,
                "embedding_request_id": batch.request_id,
            }
        )
    return reports, batch
