"""Read the public OSWorld-Human task format without exposing extra fields."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Iterable

from .models import SourceTask


def _manifest_task(entry: dict, app: str, *, path: Path) -> SourceTask:
    single_steps = entry.get("single_actions")
    if not isinstance(single_steps, list):
        raise ValueError(f"{path} task {entry.get('task_id')} has no single_actions list")
    declared_count = entry.get("single_action_count")
    if declared_count != len(single_steps):
        raise ValueError(
            f"{path} task {entry.get('task_id')} declares {declared_count} actions "
            f"but contains {len(single_steps)}"
        )
    return SourceTask(
        task_id=entry.get("task_id", ""),
        app=app,
        instruction=entry.get("instruction", ""),
        single_steps=tuple(single_steps),
    )


def load_source_manifest(
    path: Path,
    *,
    expected_app: str | None = None,
) -> list[SourceTask]:
    """Load a self-contained Pilot source manifest without an external clone."""

    document = json.loads(path.read_text(encoding="utf-8"))
    app = document.get("app")
    if expected_app is not None and app != expected_app:
        raise ValueError(f"{path} has app {app!r}; expected {expected_app!r}")
    entries = document.get("tasks")
    if not isinstance(entries, list) or not entries:
        raise ValueError(f"{path} has no tasks list")
    return [_manifest_task(entry, app or "", path=path) for entry in entries]


def verify_manifest_sources(path: Path, source_root: Path) -> None:
    """Verify pinned raw files and their copied instruction/actions when available."""

    document = json.loads(path.read_text(encoding="utf-8"))
    app = document.get("app", "")
    for entry in document.get("tasks", []):
        relative_path = entry.get("source_file")
        expected_sha256 = entry.get("source_sha256")
        if not relative_path or not expected_sha256:
            raise ValueError(f"Manifest task {entry.get('task_id')} lacks source verification")
        source_path = source_root / relative_path
        digest = hashlib.sha256(source_path.read_bytes()).hexdigest()
        if digest != expected_sha256:
            raise ValueError(f"SHA256 mismatch for {source_path}")
        raw_task = load_source_task(source_path, expected_app=app)
        copied_task = _manifest_task(entry, app, path=path)
        if raw_task != copied_task:
            raise ValueError(f"Copied source content differs for {entry.get('task_id')}")


def load_source_task(path: Path, *, expected_app: str | None = None) -> SourceTask:
    data = json.loads(path.read_text(encoding="utf-8"))
    app = data.get("snapshot")
    if expected_app is not None and app != expected_app:
        raise ValueError(
            f"{path} has snapshot {app!r}; expected {expected_app!r}"
        )

    ground_truth = data.get("human-ground-truth")
    if not isinstance(ground_truth, dict):
        raise ValueError(f"{path} has no human-ground-truth object")
    single_steps = ground_truth.get("single-action")
    if not isinstance(single_steps, list):
        raise ValueError(f"{path} has no human-ground-truth.single-action list")

    return SourceTask(
        task_id=data.get("id", ""),
        app=app or "",
        instruction=data.get("instruction", ""),
        single_steps=tuple(single_steps),
    )


def resolve_task_paths(source_root: Path, task_ids: Iterable[str]) -> list[Path]:
    """Resolve explicit task IDs without silently selecting arbitrary pilot tasks."""

    paths: list[Path] = []
    for task_id in task_ids:
        matches = sorted(source_root.glob(f"**/{task_id}.json"))
        if not matches:
            raise FileNotFoundError(f"No OSWorld-Human task found for {task_id}")
        if len(matches) > 1:
            raise ValueError(f"Multiple OSWorld-Human files found for {task_id}: {matches}")
        paths.append(matches[0])
    return paths
