"""DashScope video-to-skill induction for the engineering Pilot."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import tempfile
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from http import HTTPStatus
from pathlib import Path
from typing import Any, Callable

from .schema import load_schema, validate_payload


@dataclass(frozen=True)
class ReferenceVideo:
    video_id: str
    path: Path

    def __post_init__(self) -> None:
        if not self.video_id:
            raise ValueError("Reference video ID must not be empty")
        if not self.path.is_file():
            raise FileNotFoundError(self.path)

    @property
    def sha256(self) -> str:
        digest = hashlib.sha256()
        with self.path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()


@dataclass(frozen=True)
class VideoInductionConfig:
    model: str = "qwen3.7-plus-2026-05-26"
    fps: float = 1.0
    max_pixels: int = 1_048_576
    max_tokens: int = 8192
    seed: int = 20260812
    max_retries: int = 2

    def __post_init__(self) -> None:
        if not 0.1 <= self.fps <= 10:
            raise ValueError("fps must be between 0.1 and 10")
        if self.max_pixels < 4096:
            raise ValueError("max_pixels must be at least 4096")
        if self.max_tokens < 1 or self.max_retries < 0:
            raise ValueError("max_tokens must be positive and retries non-negative")


def _field(value: Any, name: str, default: Any = None) -> Any:
    if isinstance(value, dict):
        return value.get(name, default)
    return getattr(value, name, default)


def _extract_response_text(response: Any) -> str:
    output = _field(response, "output", {})
    choices = _field(output, "choices", [])
    if not choices:
        raise ValueError("DashScope response has no choices")
    message = _field(choices[0], "message", {})
    content = _field(message, "content", [])
    if isinstance(content, str):
        text = content
    else:
        text = "".join(
            str(_field(part, "text", ""))
            for part in content
            if _field(part, "text") is not None
        )
    if not text.strip():
        raise ValueError("DashScope response has no text")
    return text.strip()


def _parse_json_text(text: str) -> dict:
    stripped = text.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        stripped = "\n".join(lines).strip()
    try:
        payload = json.loads(stripped)
    except json.JSONDecodeError:
        start = stripped.find("{")
        end = stripped.rfind("}")
        if start < 0 or end <= start:
            raise
        payload = json.loads(stripped[start : end + 1])
    if not isinstance(payload, dict):
        raise ValueError("Video skill response must be a JSON object")
    return payload


def _usage(response: Any) -> dict[str, int]:
    usage = _field(response, "usage", {}) or {}
    input_details = _field(usage, "input_tokens_details", {}) or {}
    return {
        "input_tokens": int(
            _field(usage, "input_tokens", _field(usage, "prompt_tokens", 0)) or 0
        ),
        "output_tokens": int(
            _field(usage, "output_tokens", _field(usage, "completion_tokens", 0))
            or 0
        ),
        "image_tokens": int(_field(input_details, "image_tokens", 0) or 0),
        "text_tokens": int(_field(input_details, "text_tokens", 0) or 0),
    }


def estimate_qwen37_cost_cny(input_tokens: int, output_tokens: int) -> float:
    """Estimate mainland list-price cost for the pinned Qwen3.7 Plus model."""

    if max(input_tokens, output_tokens) < 0:
        raise ValueError("Token counts must be non-negative")
    if input_tokens <= 256_000:
        input_rate, output_rate = 2.0, 8.0
    else:
        input_rate, output_rate = 6.0, 24.0
    return round(
        (input_tokens * input_rate + output_tokens * output_rate) / 1_000_000,
        8,
    )


def discover_reference_videos(root: Path) -> list[ReferenceVideo]:
    paths = sorted(root.glob("reference-task-*/*/recording.mp4"))
    by_id: dict[str, Path] = {}
    for path in paths:
        video_id = path.parent.parent.name
        if video_id in by_id:
            raise ValueError(f"Multiple recordings found for {video_id}")
        by_id[video_id] = path
    if len(by_id) != 4:
        raise ValueError(f"Expected exactly 4 reference recordings, found {len(by_id)}")
    return [ReferenceVideo(video_id, by_id[video_id]) for video_id in sorted(by_id)]


def _default_call(**kwargs: Any) -> Any:
    try:
        import dashscope
        from dashscope import MultiModalConversation
    except ImportError as exc:
        raise RuntimeError(
            "DashScope SDK is unavailable. Update osworld-aws-dev from "
            "environment.aws-dev.yml."
        ) from exc
    base_url = os.environ.get("DASHSCOPE_BASE_URL")
    if base_url:
        dashscope.base_http_api_url = base_url
    return MultiModalConversation.call(**kwargs)


def induce_video_skills(
    videos: list[ReferenceVideo],
    *,
    system_prompt: str,
    user_prompt_template: str,
    config: VideoInductionConfig,
    call: Callable[..., Any] | None = None,
    raw_response_sink: Callable[[str], None] | None = None,
) -> tuple[dict, dict, str]:
    if len(videos) != 4 or len({video.video_id for video in videos}) != 4:
        raise ValueError("Video induction requires four unique reference videos")
    video_ids = [video.video_id for video in videos]
    user_prompt = user_prompt_template.format(
        video_ids_json=json.dumps(video_ids, ensure_ascii=False)
    )
    prompt_sha256 = hashlib.sha256(
        f"{system_prompt}\n\0\n{user_prompt}".encode("utf-8")
    ).hexdigest()
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if call is None and not api_key:
        raise RuntimeError("DASHSCOPE_API_KEY is not set")
    caller = call or _default_call
    response = None
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="osworld-reference-videos-") as temp_dir:
        staged_paths = []
        for index, video in enumerate(videos, start=1):
            staged_path = Path(temp_dir) / f"reference-video-{index:02d}.mp4"
            shutil.copy2(video.path, staged_path)
            staged_paths.append(staged_path)
        messages = [
            {"role": "system", "content": [{"text": system_prompt}]},
            {
                "role": "user",
                "content": [
                    *[
                        {
                            "video": str(staged_path.resolve()),
                            "fps": config.fps,
                            "max_pixels": config.max_pixels,
                        }
                        for staged_path in staged_paths
                    ],
                    {"text": user_prompt},
                ],
            },
        ]
        for attempt in range(config.max_retries + 1):
            response = caller(
                api_key=api_key,
                model=config.model,
                messages=messages,
                max_tokens=config.max_tokens,
                temperature=0.01,
                seed=config.seed,
                enable_thinking=False,
                vl_high_resolution_images=False,
            )
            status_code = _field(response, "status_code", HTTPStatus.OK)
            if status_code in (None, HTTPStatus.OK, 200):
                break
            if status_code not in {408, 429, 500, 502, 503, 504}:
                raise RuntimeError(
                    f"DashScope request failed: {status_code} "
                    f"{_field(response, 'code', '')} {_field(response, 'message', '')}"
                )
            if attempt == config.max_retries:
                raise RuntimeError(
                    f"DashScope request failed after retries: {status_code}"
                )
            time.sleep(1.5 * (attempt + 1))
    if response is None:
        raise RuntimeError("DashScope returned no response")

    raw_text = _extract_response_text(response)
    if raw_response_sink is not None:
        raw_response_sink(raw_text)
    payload = _parse_json_text(raw_text)
    validate_payload(payload, load_schema("video-skill-induction-response.schema.json"))
    allowed_video_ids = set(video_ids)
    for skill in payload["skills"]:
        for evidence in skill["evidence"]:
            if evidence["video_id"] not in allowed_video_ids:
                raise ValueError(
                    f"Unknown evidence video ID: {evidence['video_id']}"
                )
            if evidence["end_seconds"] < evidence["start_seconds"]:
                raise ValueError("Evidence end_seconds precedes start_seconds")

    learned_skills = {
        "schema_version": "1.0",
        "status": "engineering_pilot",
        "app": "libreoffice_calc",
        "model": config.model,
        "skills": [
            {"skill_id": f"induced-skill-{index:02d}", **skill}
            for index, skill in enumerate(payload["skills"], start=1)
        ],
    }
    usage = _usage(response)
    run = {
        "schema_version": "1.0",
        "status": "completed",
        "experiment_status": "engineering_pilot",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model": config.model,
        "seed": config.seed,
        "fps": config.fps,
        "max_pixels": config.max_pixels,
        "max_tokens": config.max_tokens,
        "enable_thinking": False,
        "prompt_sha256": prompt_sha256,
        "request_id": _field(response, "request_id"),
        "latency_seconds": round(time.monotonic() - started, 6),
        "usage": usage,
        "estimated_cost_cny": estimate_qwen37_cost_cny(
            usage["input_tokens"], usage["output_tokens"]
        ),
        "pricing": {
            "currency": "CNY",
            "as_of": "2026-08-12",
            "source": "https://help.aliyun.com/zh/model-studio/model-pricing",
        },
        "videos": [
            {
                "video_id": video.video_id,
                "path": str(video.path),
                "sha256": video.sha256,
                "size_bytes": video.path.stat().st_size,
            }
            for video in videos
        ],
    }
    return learned_skills, run, raw_text


def write_induction_outputs(
    output_dir: Path,
    learned_skills: dict,
    run: dict,
    raw_text: str,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    documents = {
        "learned_skills.json": json.dumps(
            learned_skills, ensure_ascii=False, indent=2, sort_keys=True
        )
        + "\n",
        "skill_induction_run.json": json.dumps(
            run, ensure_ascii=False, indent=2, sort_keys=True
        )
        + "\n",
        "raw_response.txt": raw_text + "\n",
    }
    for name, content in documents.items():
        path = output_dir / name
        temporary = path.with_name(f".{path.name}.tmp")
        temporary.write_text(content, encoding="utf-8")
        os.replace(temporary, path)
