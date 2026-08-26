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


class _FinalSelectionDynamo:
    def __init__(self, pages):
        from boto3.dynamodb.types import TypeSerializer

        serializer = TypeSerializer()
        self.pages = [
            {
                "Items": [
                    {key: serializer.serialize(value) for key, value in item.items()}
                    for item in page
                ],
                **(
                    {"LastEvaluatedKey": {"pk": {"S": "next"}}}
                    if index < len(pages) - 1
                    else {}
                ),
            }
            for index, page in enumerate(pages)
        ]
        self.calls = []

    def scan(self, **kwargs):
        self.calls.append(kwargs)
        return self.pages[len(self.calls) - 1]


class _AssignmentDynamo:
    def __init__(self, rows):
        from boto3.dynamodb.types import TypeSerializer

        serializer = TypeSerializer()
        self.items = {
            (username, task_id): {
                key: serializer.serialize(value)
                for key, value in {
                    "pk": f"USER#{username}",
                    "sk": f"ASSIGNMENT#{task_id}",
                    "entity": "assignment",
                    "username": username,
                    "task_id": task_id,
                    "assigned_at": "2026-01-01T00:00:00+00:00",
                }.items()
            }
            for username, task_id in rows
        }

    def query(self, **kwargs):
        from boto3.dynamodb.types import TypeDeserializer

        deserialize = TypeDeserializer().deserialize
        owner = deserialize(kwargs["ExpressionAttributeValues"][":pk"]).removeprefix(
            "USER#"
        )
        return {
            "Items": [raw for (username, _), raw in self.items.items() if username == owner]
        }

    def delete_item(self, *, Key, **_kwargs):
        from boto3.dynamodb.types import TypeDeserializer

        deserialize = TypeDeserializer().deserialize
        username = deserialize(Key["pk"]).removeprefix("USER#")
        task_id = deserialize(Key["sk"]).removeprefix("ASSIGNMENT#")
        self.items.pop((username, task_id))

    def put_item(self, *, Item, **_kwargs):
        from boto3.dynamodb.types import TypeDeserializer

        deserialize = TypeDeserializer().deserialize
        username = deserialize(Item["username"])
        task_id = deserialize(Item["task_id"])
        self.items[(username, task_id)] = Item


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
    review = {
        "reference_task_id": "task-1",
        "decision": "approved",
        "reason_codes": [],
        "revision_instructions": [],
        "reviewer": "alice",
        "notes": "Ready for annotation.",
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
        review=review,
    )

    assert (destination / "recording.mp4").read_bytes() == video
    assert json.loads((destination / "COMPLETE.json").read_text())["run_id"] == "run-1"
    assert json.loads((destination / "review.json").read_text()) == review

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


def test_downloader_reads_paginated_final_selections_with_filters():
    module = _load_script("download_annotation_results.py")
    dynamodb = _FinalSelectionDynamo(
        [
            [{"username": "alice", "task_id": "task-1", "session_id": "run-1"}],
            [{"username": "alice", "task_id": "task-2", "session_id": "run-2"}],
        ]
    )

    selections = module.final_selections(
        dynamodb,
        table_name="portal-state",
        username="alice",
    )

    assert selections == {
        ("alice", "task-1"): "run-1",
        ("alice", "task-2"): "run-2",
    }
    assert len(dynamodb.calls) == 2
    assert "username = :username" in dynamodb.calls[0]["FilterExpression"]
    assert dynamodb.calls[1]["ExclusiveStartKey"] == {"pk": {"S": "next"}}


def test_downloader_defaults_to_final_only_and_all_runs_is_explicit(monkeypatch):
    module = _load_script("download_annotation_results.py")
    monkeypatch.setattr(module.sys, "argv", ["download_annotation_results.py"])
    assert module.parse_args().final_only is True

    monkeypatch.setattr(
        module.sys, "argv", ["download_annotation_results.py", "--all-runs"]
    )
    assert module.parse_args().final_only is False


def test_pilot_snapshot_is_deterministic_and_assignments_are_validated(tmp_path):
    module = _load_script("publish_annotation_batch.py")
    pilot = REPO_ROOT / "evaluation_examples/expert_skill_learning/pilot"
    first = tmp_path / "first.tar.gz"
    second = tmp_path / "second.tar.gz"

    assert module.build_snapshot(pilot, first) == module.build_snapshot(pilot, second)
    assignments = module.load_assignments(
        REPO_ROOT
        / "evaluation_examples/expert_skill_learning/annotation_portal/assignments.example.json",
        {
            f"reference-task-calc-full-r01-{index:03d}"
            for index in range(1, 21)
        },
    )
    assert len(assignments) == 20


def test_calc_full_round_is_staged_into_portal_layout(tmp_path):
    module = _load_script("publish_annotation_batch.py")
    dataset = REPO_ROOT / "evaluation_examples/expert_skill_learning/calc_full_v1"
    staged = module.stage_dataset_round(dataset, "round_01", tmp_path / "pilot")

    catalog = module.TaskCatalog.load(
        packages_path=staged / "reference_packages.json",
        skills_path=staged / "skill_pool.json",
        reviews_path=staged / "reference_package_reviews.json",
        allow_pending=True,
    )

    assert len(catalog.all()) == 20
    assert (
        staged / "review_packets/reference-task-calc-full-r01-001/TASK.md"
    ).is_file()
    assert (
        staged / "task_configs/reference-task-calc-full-r01-020.json"
    ).is_file()
    for index in range(1, 21):
        task_id = f"reference-task-calc-full-r01-{index:03d}"
        config_path = staged / "task_configs" / f"{task_id}.json"
        config = json.loads(config_path.read_text(encoding="utf-8"))
        artifact = staged / "artifacts" / task_id / "initial_artifact.xlsx"
        assert artifact.is_file()
        assert module.file_sha256(artifact) == config["reference_annotation"][
            "artifact_sha256"
        ]


def test_assignment_replacement_removes_old_tasks_for_target_users():
    module = _load_script("publish_annotation_batch.py")
    dynamodb = _AssignmentDynamo(
        [("alice", "old-task"), ("alice", "keep-task"), ("bob", "unrelated-task")]
    )

    deleted = module.put_assignments(
        dynamodb,
        "portal-state",
        [("alice", "keep-task"), ("alice", "new-task")],
        replace=True,
    )

    assert deleted == 1
    assert set(dynamodb.items) == {
        ("alice", "keep-task"),
        ("alice", "new-task"),
        ("bob", "unrelated-task"),
    }


def test_online_reviews_sync_into_blank_local_review_json(tmp_path):
    module = _load_script("sync_annotation_portal_reviews.py")
    task_id = "reference-task-calc-full-r01-001"
    packet = tmp_path / task_id
    packet.mkdir()
    blank = {
        "reference_task_id": task_id,
        "decision": "",
        "reason_codes": [],
        "revision_instructions": [],
        "reviewer": "",
        "notes": "",
    }
    (packet / "review.json").write_text(json.dumps(blank), encoding="utf-8")
    approved = {
        **blank,
        "decision": "approved",
        "reviewer": "annotator-hk-1",
        "notes": "The task is natural and ready for annotation.",
    }

    written = module.sync_reviews(
        {task_id: {"review": approved}},
        packet_root=tmp_path,
        overwrite=False,
    )

    assert written == [packet / "review.json"]
    assert json.loads((packet / "review.json").read_text())["decision"] == "approved"


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


def test_portal_entrypoint_preserves_live_pilot_symlink(tmp_path):
    runner = _load_script("run_annotation_portal.py")
    snapshot = tmp_path / "snapshot" / "pilot"
    snapshot.mkdir(parents=True)
    live = tmp_path / "live-pilot"
    live.symlink_to(snapshot, target_is_directory=True)

    normalized = runner._live_pilot_root(live)

    assert normalized == live.absolute()
    assert normalized.is_symlink()
    assert normalized.resolve() == snapshot.resolve()
