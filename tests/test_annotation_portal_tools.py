import hashlib
import importlib.util
import io
import json
import shutil
from pathlib import Path

import pytest

from benchmark_construction.annotation_portal.catalog import ReloadingTaskCatalog


REPO_ROOT = Path(__file__).parents[1]


def _load_script(name):
    path = REPO_ROOT / "scripts/python" / name
    spec = importlib.util.spec_from_file_location(name.removesuffix(".py"), path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class _DownloadS3:
    def __init__(self, objects):
        self.objects = objects

    def get_object(self, *, Bucket, Key):
        return {"Body": io.BytesIO(self.objects[(Bucket, Key)])}

    def download_file(self, bucket, key, filename):
        Path(filename).write_bytes(self.objects[(bucket, key)])


def test_verified_downloader_accepts_complete_run_and_rejects_traversal(tmp_path):
    module = _load_script("download_annotation_results.py")
    video = b"verified-video"
    sha = hashlib.sha256(video).hexdigest()
    complete_key = "reference-annotations/alice/task-1/run-1/COMPLETE.json"
    manifest = {
        "schema_version": "1.0",
        "username": "alice",
        "task_id": "task-1",
        "run_id": "run-1",
        "files": [{"path": "recording.mp4", "size": len(video), "sha256": sha}],
    }
    s3 = _DownloadS3(
        {
            ("bucket", complete_key): json.dumps(manifest).encode(),
            ("bucket", complete_key.removesuffix("COMPLETE.json") + "recording.mp4"): video,
        }
    )

    destination = module.download_run(
        s3,
        bucket="bucket",
        complete_key=complete_key,
        output_dir=tmp_path,
        video_only=True,
        overwrite=False,
    )

    assert (destination / "recording.mp4").read_bytes() == video
    assert json.loads((destination / "COMPLETE.json").read_text())["run_id"] == "run-1"

    unsafe = dict(manifest)
    unsafe["run_id"] = "run-2"
    unsafe["files"] = [{"path": "../escape", "size": 0, "sha256": sha}]
    unsafe_key = "reference-annotations/alice/task-1/run-2/COMPLETE.json"
    s3.objects[("bucket", unsafe_key)] = json.dumps(unsafe).encode()
    with pytest.raises(ValueError, match="Unsafe manifest path"):
        module.download_run(
            s3,
            bucket="bucket",
            complete_key=unsafe_key,
            output_dir=tmp_path,
            video_only=False,
            overwrite=False,
        )
    assert not (tmp_path / "alice/task-1/run-2").exists()


def test_pilot_snapshot_is_deterministic_and_assignments_are_validated(tmp_path):
    module = _load_script("publish_annotation_batch.py")
    pilot = REPO_ROOT / "evaluation_examples/expert_skill_learning/pilot"
    first = tmp_path / "first.tar.gz"
    second = tmp_path / "second.tar.gz"

    assert module.build_snapshot(pilot, first) == module.build_snapshot(pilot, second)
    assignments = module.load_assignments(
        REPO_ROOT
        / "evaluation_examples/expert_skill_learning/annotation_portal/assignments.example.json",
        {f"reference-task-r01-{index:03d}" for index in range(1, 5)},
    )
    assert assignments


def test_reloading_catalog_switches_to_new_immutable_symlink_target(tmp_path):
    source = REPO_ROOT / "evaluation_examples/expert_skill_learning/pilot"
    first = tmp_path / "pilot-a"
    second = tmp_path / "pilot-b"
    shutil.copytree(source, first)
    shutil.copytree(source, second)
    packages_path = second / "reference_packages.json"
    packages = json.loads(packages_path.read_text(encoding="utf-8"))
    packages["reference_packages"][0]["task_instruction"] = "Updated immutable task."
    packages_path.write_text(json.dumps(packages), encoding="utf-8")
    live = tmp_path / "live-pilot"
    live.symlink_to(first, target_is_directory=True)
    catalog = ReloadingTaskCatalog(live, allow_pending=True)

    original = catalog.get("reference-task-r01-001")
    live.unlink()
    live.symlink_to(second, target_is_directory=True)
    updated = catalog.get("reference-task-r01-001")

    assert original.instruction != updated.instruction
    assert updated.instruction == "Updated immutable task."
    assert original.catalog_version != updated.catalog_version
