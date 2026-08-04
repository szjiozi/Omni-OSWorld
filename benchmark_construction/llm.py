"""Async OpenAI-compatible JSON generation with auditable per-attempt logs."""

from __future__ import annotations

import asyncio
import hashlib
import json
import os
import threading
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .pricing import PricingTable, TokenUsage
from .schema import validate_payload


@dataclass(frozen=True)
class MediaInput:
    """Reserved multimodal input contract; video is not sent by this backend yet."""

    kind: str
    uri: str

    def __post_init__(self) -> None:
        if self.kind not in {"image", "video"}:
            raise ValueError("MediaInput.kind must be image or video")
        if not self.uri:
            raise ValueError("MediaInput.uri must not be empty")


@dataclass(frozen=True)
class LLMConfig:
    model: str = "gpt-5.6-terra"
    base_url: str | None = None
    api_key_env: str = "OPENAI_API_KEY"
    concurrency: int = 4
    max_retries: int = 3
    response_format: str = "json_schema"

    def __post_init__(self) -> None:
        if self.concurrency < 1:
            raise ValueError("concurrency must be at least 1")
        if self.max_retries < 0:
            raise ValueError("max_retries must be non-negative")
        if self.response_format not in {"json_schema", "json_object", "text"}:
            raise ValueError("Unsupported response_format")


@dataclass(frozen=True)
class JSONRequest:
    prompt_name: str
    system_prompt: str
    user_prompt: str
    response_schema: dict[str, Any]
    schema_name: str
    media: tuple[MediaInput, ...] = field(default_factory=tuple)
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    @property
    def prompt_sha256(self) -> str:
        content = f"{self.system_prompt}\n\0\n{self.user_prompt}".encode("utf-8")
        return hashlib.sha256(content).hexdigest()


@dataclass(frozen=True)
class JSONResult:
    request_id: str
    model: str
    data: dict[str, Any]
    usage: TokenUsage
    estimated_cost_usd: float | None


class UnsupportedMediaError(ValueError):
    pass


class JsonlCallLogger:
    def __init__(self, path: Path) -> None:
        self.path = path
        self._lock = threading.Lock()

    async def append(self, record: dict[str, Any]) -> None:
        line = json.dumps(record, ensure_ascii=False, sort_keys=True)
        with self._lock:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("a", encoding="utf-8") as stream:
                stream.write(line + "\n")


def _field(value: Any, name: str, default: Any = None) -> Any:
    if isinstance(value, dict):
        return value.get(name, default)
    return getattr(value, name, default)


def _usage_from_response(response: Any) -> TokenUsage:
    usage = _field(response, "usage", {})
    input_tokens = int(
        _field(usage, "prompt_tokens", _field(usage, "input_tokens", 0)) or 0
    )
    output_tokens = int(
        _field(usage, "completion_tokens", _field(usage, "output_tokens", 0)) or 0
    )
    details = _field(usage, "prompt_tokens_details", {}) or {}
    cached = int(_field(details, "cached_tokens", 0) or 0)
    return TokenUsage(input_tokens, output_tokens, cached)


def _content_from_response(response: Any) -> str:
    choices = _field(response, "choices", [])
    if not choices:
        raise ValueError("LLM response has no choices")
    message = _field(choices[0], "message", {})
    content = _field(message, "content")
    if not isinstance(content, str) or not content.strip():
        raise ValueError("LLM response has no text content")
    return content


def _is_retryable(exc: Exception) -> bool:
    status_code = getattr(exc, "status_code", None)
    if isinstance(status_code, int) and 400 <= status_code < 500:
        return status_code in {408, 409, 429}
    return True


class OpenAICompatibleAsyncClient:
    def __init__(
        self,
        config: LLMConfig,
        *,
        call_log: Path,
        pricing: PricingTable | None = None,
        client: Any | None = None,
    ) -> None:
        self.config = config
        self.pricing = pricing or PricingTable.from_path()
        self.logger = JsonlCallLogger(call_log)
        self._semaphore: asyncio.Semaphore | None = None
        self._client = client or self._build_client()

    def _get_semaphore(self) -> asyncio.Semaphore:
        # Construct inside the active event loop for Python 3.9 compatibility.
        if self._semaphore is None:
            self._semaphore = asyncio.Semaphore(self.config.concurrency)
        return self._semaphore

    def _build_client(self) -> Any:
        try:
            from openai import AsyncOpenAI
        except ImportError as exc:
            raise RuntimeError(
                "AsyncOpenAI is unavailable. Update the local development "
                "environment from environment.aws-dev.yml."
            ) from exc
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

    def _messages(self, request: JSONRequest) -> list[dict[str, Any]]:
        if request.media:
            kinds = sorted({item.kind for item in request.media})
            raise UnsupportedMediaError(
                "The Chat Completions construction backend currently accepts text "
                f"only; received media kinds {kinds}. The interface is reserved for "
                "a future native-video or video-to-frames adapter."
            )
        return [
            {"role": "system", "content": request.system_prompt},
            {"role": "user", "content": request.user_prompt},
        ]

    def _response_format(self, request: JSONRequest) -> dict[str, Any] | None:
        if self.config.response_format == "json_schema":
            return {
                "type": "json_schema",
                "json_schema": {
                    "name": request.schema_name,
                    "strict": True,
                    "schema": request.response_schema,
                },
            }
        if self.config.response_format == "json_object":
            return {"type": "json_object"}
        return None

    async def generate_json(self, request: JSONRequest) -> JSONResult:
        messages = self._messages(request)
        async with self._get_semaphore():
            for attempt in range(self.config.max_retries + 1):
                started = time.monotonic()
                timestamp = datetime.now(timezone.utc).isoformat()
                usage: TokenUsage | None = None
                cost: float | None = None
                try:
                    kwargs: dict[str, Any] = {
                        "model": self.config.model,
                        "messages": messages,
                    }
                    response_format = self._response_format(request)
                    if response_format is not None:
                        kwargs["response_format"] = response_format
                    response = await self._client.chat.completions.create(**kwargs)
                    usage = _usage_from_response(response)
                    cost = self.pricing.estimate_usd(self.config.model, usage)
                    payload = json.loads(_content_from_response(response))
                    validate_payload(payload, request.response_schema)
                    await self.logger.append(
                        {
                            "request_id": request.request_id,
                            "attempt": attempt + 1,
                            "timestamp": timestamp,
                            "prompt_name": request.prompt_name,
                            "prompt_sha256": request.prompt_sha256,
                            "model": self.config.model,
                            "status": "success",
                            "latency_seconds": round(time.monotonic() - started, 6),
                            "input_tokens": usage.input_tokens,
                            "cached_input_tokens": usage.cached_input_tokens,
                            "output_tokens": usage.output_tokens,
                            "estimated_cost_usd": cost,
                            "pricing_known": cost is not None,
                            "pricing_version": self.pricing.document.get("version"),
                        }
                    )
                    return JSONResult(
                        request_id=request.request_id,
                        model=self.config.model,
                        data=payload,
                        usage=usage,
                        estimated_cost_usd=cost,
                    )
                except Exception as exc:
                    await self.logger.append(
                        {
                            "request_id": request.request_id,
                            "attempt": attempt + 1,
                            "timestamp": timestamp,
                            "prompt_name": request.prompt_name,
                            "prompt_sha256": request.prompt_sha256,
                            "model": self.config.model,
                            "status": "failed",
                            "latency_seconds": round(time.monotonic() - started, 6),
                            "error_type": type(exc).__name__,
                            "error": str(exc),
                            "input_tokens": usage.input_tokens if usage else None,
                            "cached_input_tokens": (
                                usage.cached_input_tokens if usage else None
                            ),
                            "output_tokens": usage.output_tokens if usage else None,
                            "estimated_cost_usd": cost,
                            "pricing_known": cost is not None,
                            "pricing_version": self.pricing.document.get("version"),
                        }
                    )
                    if attempt >= self.config.max_retries or not _is_retryable(exc):
                        raise
                    await asyncio.sleep(min(8.0, 0.5 * (2**attempt)))
        raise AssertionError("unreachable")

    async def generate_many(self, requests: list[JSONRequest]) -> list[JSONResult]:
        return list(await asyncio.gather(*(self.generate_json(item) for item in requests)))
