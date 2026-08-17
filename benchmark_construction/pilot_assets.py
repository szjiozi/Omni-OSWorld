"""Prefetch OSWorld task assets into its existing per-task cache layout."""

from __future__ import annotations

import hashlib
import json
import os
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable


@dataclass(frozen=True)
class PilotAsset:
    task_id: str
    kind: str
    url: str
    cache_path: Path


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _setup_cache_name(url: str, guest_path: str) -> str:
    return f"{uuid.uuid5(uuid.NAMESPACE_URL, url)}_{Path(guest_path).name}"


def discover_pilot_assets(
    suite_path: Path,
    task_root: Path,
    cache_root: Path,
) -> list[PilotAsset]:
    suite = json.loads(suite_path.read_text(encoding="utf-8"))
    assets: list[PilotAsset] = []
    for app, task_ids in suite.items():
        for task_id in task_ids:
            task_path = task_root / "examples" / app / f"{task_id}.json"
            task = json.loads(task_path.read_text(encoding="utf-8"))
            if task.get("id") != task_id:
                raise ValueError(f"Task ID mismatch in {task_path}")
            task_cache = cache_root / task_id
            for config in task.get("config", []):
                if config.get("type") != "download":
                    continue
                for item in config["parameters"]["files"]:
                    assets.append(
                        PilotAsset(
                            task_id,
                            "setup",
                            item["url"],
                            task_cache
                            / _setup_cache_name(item["url"], item["path"]),
                        )
                    )
            expected = task.get("evaluator", {}).get("expected")
            expected_items = expected if isinstance(expected, list) else [expected]
            for item in expected_items:
                if not item or item.get("type") != "cloud_file":
                    continue
                if item.get("multi"):
                    urls = item["path"]
                    dests = item["dest"]
                else:
                    urls = [item["path"]]
                    dests = [item["dest"]]
                for url, dest in zip(urls, dests):
                    assets.append(
                        PilotAsset(task_id, "expected", url, task_cache / dest)
                    )
    destinations = [asset.cache_path for asset in assets]
    if len(destinations) != len(set(destinations)):
        raise ValueError("Pilot assets contain duplicate cache destinations")
    return assets


def _download_via_environment(url: str, destination: Path) -> None:
    import requests

    with requests.get(url, stream=True, timeout=(30, 300)) as response:
        response.raise_for_status()
        with destination.open("wb") as output:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    output.write(chunk)


def prefetch_pilot_assets(
    assets: list[PilotAsset],
    *,
    manifest_path: Path,
    fetch: Callable[[str, Path], None] = _download_via_environment,
) -> dict:
    records = []
    for asset in assets:
        asset.cache_path.parent.mkdir(parents=True, exist_ok=True)
        downloaded = not asset.cache_path.is_file() or asset.cache_path.stat().st_size == 0
        if downloaded:
            temporary = asset.cache_path.with_name(f".{asset.cache_path.name}.tmp")
            try:
                fetch(asset.url, temporary)
                if not temporary.is_file() or temporary.stat().st_size == 0:
                    raise ValueError(f"Downloaded asset is empty: {asset.url}")
                os.replace(temporary, asset.cache_path)
            finally:
                if temporary.exists():
                    temporary.unlink()
        records.append(
            {
                "task_id": asset.task_id,
                "kind": asset.kind,
                "url": asset.url,
                "cache_path": str(asset.cache_path.resolve()),
                "size_bytes": asset.cache_path.stat().st_size,
                "sha256": _sha256(asset.cache_path),
                "downloaded": downloaded,
            }
        )
    manifest = {
        "schema_version": "1.0",
        "status": "completed",
        "experiment_status": "engineering_pilot",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "network_policy": "requests environment proxy/default routing",
        "asset_count": len(records),
        "assets": records,
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_manifest = manifest_path.with_name(f".{manifest_path.name}.tmp")
    temporary_manifest.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary_manifest, manifest_path)
    return manifest
