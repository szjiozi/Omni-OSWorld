import json
import uuid
from pathlib import Path

from benchmark_construction.pilot_assets import (
    discover_pilot_assets,
    prefetch_pilot_assets,
)


def test_discovers_and_prefetches_setup_and_expected_assets(tmp_path: Path):
    task_id = "task-1"
    task_root = tmp_path / "tasks"
    task_dir = task_root / "examples" / "libreoffice_calc"
    task_dir.mkdir(parents=True)
    suite = {"libreoffice_calc": [task_id]}
    suite_path = task_root / "suite.json"
    suite_path.write_text(json.dumps(suite), encoding="utf-8")
    source_url = "https://example.test/source.xlsx"
    expected_url = "https://example.test/expected.xlsx"
    task = {
        "id": task_id,
        "config": [
            {
                "type": "download",
                "parameters": {
                    "files": [
                        {"url": source_url, "path": "/home/user/source.xlsx"}
                    ]
                },
            }
        ],
        "evaluator": {
            "expected": {
                "type": "cloud_file",
                "path": expected_url,
                "dest": "gold.xlsx",
            }
        },
    }
    (task_dir / f"{task_id}.json").write_text(json.dumps(task), encoding="utf-8")

    assets = discover_pilot_assets(suite_path, task_root, tmp_path / "cache")
    setup_name = f"{uuid.uuid5(uuid.NAMESPACE_URL, source_url)}_source.xlsx"
    assert [asset.cache_path.name for asset in assets] == [setup_name, "gold.xlsx"]

    fetched = []

    def fake_fetch(url, destination):
        fetched.append(url)
        destination.write_bytes(url.encode())

    manifest = prefetch_pilot_assets(
        assets,
        manifest_path=tmp_path / "assets.json",
        fetch=fake_fetch,
    )
    assert fetched == [source_url, expected_url]
    assert manifest["asset_count"] == 2
    assert all(record["size_bytes"] > 0 for record in manifest["assets"])

    second = prefetch_pilot_assets(
        assets,
        manifest_path=tmp_path / "assets.json",
        fetch=lambda *_: (_ for _ in ()).throw(AssertionError("unexpected fetch")),
    )
    assert not any(record["downloaded"] for record in second["assets"])
