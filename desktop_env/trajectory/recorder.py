"""Thread-safe, append-only recording for normalized OSWorld trajectories."""

from __future__ import annotations

import json
import os
import threading
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from desktop_env.trajectory.schema import SCHEMA_VERSION, validate_document

_EMPTY_LATENCY = {
    "model": 0.0,
    "grounding": 0.0,
    "environment": 0.0,
    "settle": 0.0,
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _json_default(value: Any) -> str:
    return str(value)


class TrajectoryRecorder:
    """Write normalized events and one atomic episode manifest."""

    def __init__(
        self,
        output_dir: str | os.PathLike[str],
        *,
        task_id: str,
        actor: str,
        episode_id: str | None = None,
        validate_events: bool = False,
    ) -> None:
        if actor not in {"human", "agent"}:
            raise ValueError("actor must be 'human' or 'agent'")

        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.task_id = task_id
        self.actor = actor
        self.episode_id = episode_id or str(uuid.uuid4())
        self.validate_events = validate_events
        self.events_path = self.output_dir / "events.jsonl"
        self.manifest_path = self.output_dir / "episode_manifest.json"
        self._event_id = 0
        self._started_at = _utc_now()
        self._started_ns = time.monotonic_ns()
        self._timings_ns: dict[str, int] = {}
        self._lock = threading.Lock()
        self._finalized = False

    @staticmethod
    def now_ns() -> int:
        return time.monotonic_ns()

    def add_timing(self, name: str, elapsed_ns: int) -> None:
        if elapsed_ns < 0:
            raise ValueError("elapsed_ns must be non-negative")
        with self._lock:
            self._timings_ns[name] = self._timings_ns.get(name, 0) + elapsed_ns

    def record_event(
        self,
        event_type: str,
        *,
        group_id: int | None = None,
        started_ns: int | None = None,
        finished_ns: int | None = None,
        semantic_action: Mapping[str, Any] | None = None,
        raw_action: Any = None,
        latency_ms: Mapping[str, float] | None = None,
        observation_ref: str | None = None,
        a11y_ref: str | None = None,
        window: Mapping[str, Any] | None = None,
        outcome: str = "ok",
        error: str | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        if self._finalized:
            raise RuntimeError("Cannot record an event after finalize()")

        started = started_ns if started_ns is not None else self.now_ns()
        finished = finished_ns if finished_ns is not None else self.now_ns()
        if finished < started:
            raise ValueError("finished_ns must not be earlier than started_ns")

        event_latency = dict(_EMPTY_LATENCY)
        if latency_ms:
            unknown = set(latency_ms) - set(event_latency)
            if unknown:
                raise ValueError(f"Unknown latency fields: {sorted(unknown)}")
            event_latency.update({key: float(value) for key, value in latency_ms.items()})

        with self._lock:
            event = {
                "schema_version": SCHEMA_VERSION,
                "episode_id": self.episode_id,
                "task_id": self.task_id,
                "actor": self.actor,
                "event_id": self._event_id,
                "group_id": group_id,
                "event_type": event_type,
                "timestamps_ns": {
                    "started": started,
                    "finished": finished,
                },
                "latency_ms": event_latency,
                "outcome": outcome,
                "error": error,
            }
            if semantic_action is not None:
                event["semantic_action"] = dict(semantic_action)
            if raw_action is not None:
                event["raw_action"] = raw_action
            if observation_ref is not None:
                event["observation_ref"] = observation_ref
            if a11y_ref is not None:
                event["a11y_ref"] = a11y_ref
            if window is not None:
                event["window"] = dict(window)
            if metadata is not None:
                event["metadata"] = dict(metadata)

            if self.validate_events:
                validate_document(event, "trajectory_event")

            with self.events_path.open("a", encoding="utf-8") as event_file:
                event_file.write(
                    json.dumps(event, ensure_ascii=False, default=_json_default)
                )
                event_file.write("\n")
            self._event_id += 1
            return event

    def finalize(
        self,
        *,
        status: str,
        result: float | int | None,
        artifacts: Mapping[str, str] | None = None,
        error: str | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        if status not in {"completed", "failed", "interrupted"}:
            raise ValueError("Unsupported episode status")

        with self._lock:
            if self._finalized:
                with self.manifest_path.open("r", encoding="utf-8") as manifest_file:
                    return json.load(manifest_file)

            finished_ns = self.now_ns()
            manifest = {
                "schema_version": SCHEMA_VERSION,
                "episode_id": self.episode_id,
                "task_id": self.task_id,
                "actor": self.actor,
                "status": status,
                "result": result,
                "error": error,
                "started_at": self._started_at,
                "finished_at": _utc_now(),
                "event_count": self._event_id,
                "timing_policy": {
                    "clock": "time.monotonic_ns",
                    "execution_window": (
                        "first actionable observation through final environment action"
                    ),
                    "excluded_from_execution": [
                        "environment_setup",
                        "initial_settle",
                        "post_action_settle",
                        "evaluation",
                        "recording_finalize",
                    ],
                },
                "timings_ms": {
                    key: value / 1_000_000
                    for key, value in sorted(self._timings_ns.items())
                },
                "wall_clock_ms": (finished_ns - self._started_ns) / 1_000_000,
                "artifacts": dict(artifacts or {}),
                "metadata": dict(metadata or {}),
            }

            tmp_path = self.manifest_path.with_suffix(".json.tmp")
            with tmp_path.open("w", encoding="utf-8") as manifest_file:
                json.dump(
                    manifest,
                    manifest_file,
                    indent=2,
                    ensure_ascii=False,
                    default=_json_default,
                )
                manifest_file.write("\n")
            os.replace(tmp_path, self.manifest_path)
            self._finalized = True
            return manifest
