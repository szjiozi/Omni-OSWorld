"""Read the public OSWorld-Human task format without exposing extra fields."""

from __future__ import annotations

import hashlib
import json
import os
import urllib.request
from pathlib import Path
from typing import Callable, Iterable

from .models import SourceTask


OSWORLD_HUMAN_RAW_URL = (
    "https://raw.githubusercontent.com/WukLab/osworld-human/{commit}/{source_file}"
)


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


def vendor_osworld_human_app(
    source_root: Path,
    output_root: Path,
    *,
    app: str,
    source_repository: str,
    source_commit: str,
) -> dict:
    """Copy one upstream app directory byte-for-byte and derive a frozen manifest."""

    source_app_root = source_root / app
    source_paths = sorted(source_app_root.glob("*.json"))
    if not source_paths:
        raise ValueError(f"No JSON tasks found under {source_app_root}")
    destination_root = output_root / "source" / "osworld_human" / source_commit
    destination_app_root = destination_root / app
    tasks: list[dict] = []
    checksum_lines: list[str] = []
    seen_ids: set[str] = set()
    for source_path in source_paths:
        payload = source_path.read_bytes()
        document = json.loads(payload)
        task_id = document.get("id")
        if not isinstance(task_id, str) or not task_id:
            raise ValueError(f"{source_path} has no task ID")
        if task_id in seen_ids:
            raise ValueError(f"Duplicate task ID in upstream source: {task_id}")
        if source_path.stem != task_id:
            raise ValueError(f"Filename does not match task ID: {source_path}")
        if document.get("snapshot") != app:
            raise ValueError(f"{source_path} is not a {app} task")
        ground_truth = document.get("human-ground-truth")
        if not isinstance(ground_truth, dict):
            raise ValueError(f"{source_path} has no human-ground-truth object")
        single_actions = ground_truth.get("single-action")
        grouped_actions = ground_truth.get("grouped-action")
        if not isinstance(single_actions, list) or not single_actions:
            raise ValueError(f"{source_path} has no single-action annotations")
        if not isinstance(grouped_actions, list) or not grouped_actions:
            raise ValueError(f"{source_path} has no grouped-action annotations")

        destination = destination_app_root / source_path.name
        if destination.exists() and destination.read_bytes() != payload:
            raise ValueError(
                f"Refusing to overwrite non-identical vendored source: {destination}"
            )
        if not destination.exists():
            _write_bytes_atomic(destination, payload)
        digest = _sha256_bytes(payload)
        relative_source_file = f"{app}/{source_path.name}"
        checksum_lines.append(f"{digest}  {relative_source_file}")
        tasks.append(
            {
                "task_id": task_id,
                "source_file": relative_source_file,
                "source_sha256": digest,
                "instruction": document.get("instruction", ""),
                "single_action_count": len(single_actions),
                "single_actions": single_actions,
                "grouped_action_count": len(grouped_actions),
            }
        )
        seen_ids.add(task_id)

    upstream_readme = source_root / "README.md"
    if upstream_readme.is_file():
        readme_payload = upstream_readme.read_bytes()
        vendored_readme = destination_root / "README.md"
        if vendored_readme.exists() and vendored_readme.read_bytes() != readme_payload:
            raise ValueError(
                f"Refusing to overwrite non-identical upstream README: {vendored_readme}"
            )
        if not vendored_readme.exists():
            _write_bytes_atomic(vendored_readme, readme_payload)

    provenance = {
        "schema_version": "1.0",
        "source_repository": source_repository,
        "source_commit": source_commit,
        "app": app,
        "task_count": len(tasks),
        "copy_policy": "byte-for-byte",
        "license_file_present_at_source_root": (source_root / "LICENSE").is_file(),
    }
    _write_json_atomic(destination_root / "PROVENANCE.json", provenance)
    _write_bytes_atomic(
        destination_root / "SHA256SUMS",
        ("\n".join(checksum_lines) + "\n").encode("utf-8"),
    )
    manifest = {
        "schema_version": "1.1",
        "dataset_id": f"{app}-full-v1",
        "app": app,
        "language": "en",
        "source_repository": source_repository,
        "source_commit": source_commit,
        "selection_policy": f"All {app} tasks at the pinned source commit.",
        "vendored_source_root": str(destination_root),
        "tasks": tasks,
    }
    _write_json_atomic(output_root / "source_tasks.json", manifest)
    return manifest


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _write_bytes_atomic(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_bytes(payload)
    os.replace(temporary, path)


def _write_json_atomic(path: Path, payload: dict) -> None:
    data = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)
    _write_bytes_atomic(path, (data + "\n").encode("utf-8"))


def _default_fetch(url: str) -> bytes:
    with urllib.request.urlopen(url, timeout=60) as response:
        return response.read()


def _validate_raw_human_task(
    payload: bytes,
    entry: dict,
    *,
    expected_app: str,
) -> dict:
    expected_digest = entry.get("source_sha256")
    actual_digest = _sha256_bytes(payload)
    if actual_digest != expected_digest:
        raise ValueError(
            f"SHA256 mismatch for OSWorld-Human task {entry.get('task_id')}: "
            f"expected {expected_digest}, got {actual_digest}"
        )
    document = json.loads(payload)
    if document.get("id") != entry.get("task_id"):
        raise ValueError("OSWorld-Human task ID does not match the source manifest")
    if document.get("snapshot") != expected_app:
        raise ValueError("OSWorld-Human task snapshot does not match the pilot app")
    if document.get("instruction") != entry.get("instruction"):
        raise ValueError("OSWorld-Human instruction differs from the frozen source manifest")
    ground_truth = document.get("human-ground-truth")
    if not isinstance(ground_truth, dict):
        raise ValueError("OSWorld-Human task has no human-ground-truth object")
    single = ground_truth.get("single-action")
    grouped = ground_truth.get("grouped-action")
    if single != entry.get("single_actions"):
        raise ValueError("OSWorld-Human single actions differ from the frozen manifest")
    if not isinstance(grouped, list) or not grouped:
        raise ValueError("OSWorld-Human task has no grouped-action annotations")
    if not all(isinstance(group, list) and group for group in grouped):
        raise ValueError("OSWorld-Human grouped actions must be non-empty lists")
    return document


def prepare_pilot_suite(
    source_manifest_path: Path,
    output_root: Path,
    *,
    local_osworld_task_root: Path | None = None,
    fetch: Callable[[str], bytes] | None = None,
) -> dict:
    """Materialize the pinned OSWorld-Human Pilot tasks without mutating OSWorld.

    Existing valid cached task files are reused. The returned manifest records any
    top-level differences from the local OSWorld task copies so instruction drift
    cannot be hidden.
    """

    source_manifest = json.loads(source_manifest_path.read_text(encoding="utf-8"))
    app = source_manifest.get("app")
    commit = source_manifest.get("source_commit")
    repository = source_manifest.get("source_repository")
    entries = source_manifest.get("tasks")
    if not app or not commit or not repository or not isinstance(entries, list):
        raise ValueError("Source manifest lacks app, repository, commit, or tasks")

    fetch_bytes = fetch or _default_fetch
    task_records: list[dict] = []
    suite_ids: list[str] = []
    for entry in entries:
        task_id = entry.get("task_id")
        source_file = entry.get("source_file")
        if not task_id or not source_file:
            raise ValueError("Source manifest task lacks task_id or source_file")
        destination = output_root / "examples" / source_file
        if destination.exists():
            payload = destination.read_bytes()
            try:
                document = _validate_raw_human_task(
                    payload, entry, expected_app=app
                )
            except ValueError:
                payload = fetch_bytes(
                    OSWORLD_HUMAN_RAW_URL.format(
                        commit=commit,
                        source_file=source_file,
                    )
                )
                document = _validate_raw_human_task(
                    payload, entry, expected_app=app
                )
                _write_bytes_atomic(destination, payload)
        else:
            payload = fetch_bytes(
                OSWORLD_HUMAN_RAW_URL.format(
                    commit=commit,
                    source_file=source_file,
                )
            )
            document = _validate_raw_human_task(payload, entry, expected_app=app)
            _write_bytes_atomic(destination, payload)

        differing_fields: list[str] = []
        local_sha256 = None
        if local_osworld_task_root is not None:
            local_path = local_osworld_task_root / source_file
            if not local_path.exists():
                raise FileNotFoundError(f"Local OSWorld task is missing: {local_path}")
            local_payload = local_path.read_bytes()
            local_sha256 = _sha256_bytes(local_payload)
            local_document = json.loads(local_payload)
            comparable_keys = set(document) | set(local_document)
            comparable_keys.discard("human-ground-truth")
            differing_fields = sorted(
                key
                for key in comparable_keys
                if document.get(key) != local_document.get(key)
            )

        ground_truth = document["human-ground-truth"]
        task_records.append(
            {
                "task_id": task_id,
                "app": app,
                "source_file": source_file,
                "source_sha256": entry["source_sha256"],
                "materialized_path": str(destination),
                "single_action_count": len(ground_truth["single-action"]),
                "grouped_action_count": len(ground_truth["grouped-action"]),
                "local_osworld_sha256": local_sha256,
                "local_osworld_differing_fields": differing_fields,
            }
        )
        suite_ids.append(task_id)

    suite = {app: suite_ids}
    suite_path = output_root / "test_osworld_human_pilot.json"
    _write_json_atomic(suite_path, suite)
    manifest = {
        "schema_version": "1.0",
        "pilot_id": source_manifest.get("pilot_id"),
        "status": "engineering_pilot",
        "source_repository": repository,
        "source_commit": commit,
        "source_manifest": str(source_manifest_path),
        "suite_path": str(suite_path),
        "test_config_base_dir": str(output_root),
        "tasks": task_records,
    }
    _write_json_atomic(output_root / "osworld_human_pilot_manifest.json", manifest)
    return manifest
