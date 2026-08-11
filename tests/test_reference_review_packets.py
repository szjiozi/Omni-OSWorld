import json
import shutil
from pathlib import Path

import pytest

from benchmark_construction.reference_review_packets import (
    collect_packet_reviews,
    export_review_packets,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
PILOT_ROOT = REPO_ROOT / "evaluation_examples/expert_skill_learning/pilot"


def _export(packet_root: Path, *, force: bool = False) -> list[str]:
    return export_review_packets(
        repo_root=REPO_ROOT,
        skill_pool_path=PILOT_ROOT / "skill_pool.json",
        packages_path=PILOT_ROOT / "reference_packages.json",
        source_tasks_path=PILOT_ROOT / "source_tasks.json",
        reviews_path=PILOT_ROOT / "reference_package_reviews.json",
        artifact_manifest_path=PILOT_ROOT / "artifacts/artifact_manifest.json",
        task_config_manifest_path=PILOT_ROOT / "task_config_manifest.json",
        output_root=packet_root,
        force=force,
    )


def test_export_builds_self_contained_packets_with_source_evidence(tmp_path):
    packet_root = tmp_path / "review_packets"

    task_ids = _export(packet_root)

    assert task_ids == [
        "reference-task-r01-001",
        "reference-task-r01-002",
        "reference-task-r01-003",
        "reference-task-r01-004",
    ]
    task_dir = packet_root / task_ids[0]
    context = json.loads((task_dir / "context.json").read_text(encoding="utf-8"))
    review = json.loads((task_dir / "review.json").read_text(encoding="utf-8"))
    task_markdown = (task_dir / "TASK.md").read_text(encoding="utf-8")

    assert len(context["required_skills"]) == 3
    assert all(item["referenced_actions"] for item in context["source_evidence"])
    assert all(item["single_actions"] for item in context["source_evidence"])
    assert review["decision"] == ""
    assert "Workshop Enrollment Queue" in task_markdown
    assert "Directly referenced source actions" in task_markdown
    assert "artifact/previews/Enrollment_Log.png" in task_markdown
    assert (task_dir / "artifact/initial_artifact.xlsx").is_file()
    assert (task_dir / "artifact/previews/Enrollment_Log.png").is_file()
    assert (task_dir / "task_config.json").is_file()
    assert task_ids[0] in (packet_root / "index.md").read_text(encoding="utf-8")


def test_export_preserves_local_review_and_force_resets_stale_review(tmp_path):
    packet_root = tmp_path / "review_packets"
    _export(packet_root)
    task_dir = packet_root / "reference-task-r01-001"
    review_path = task_dir / "review.json"
    review = json.loads(review_path.read_text(encoding="utf-8"))
    review.update(
        {
            "decision": "approved",
            "reviewer": "reviewer-test",
            "notes": "The packet is feasible and covers all required skills.",
        }
    )
    review_path.write_text(json.dumps(review), encoding="utf-8")

    _export(packet_root)
    assert json.loads(review_path.read_text(encoding="utf-8"))["decision"] == "approved"

    manifest_path = task_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["context_fingerprint"] = "stale"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    with pytest.raises(ValueError, match="changed after review"):
        _export(packet_root)

    _export(packet_root, force=True)
    reset_review = json.loads(review_path.read_text(encoding="utf-8"))
    assert reset_review["decision"] == ""
    assert reset_review["reviewer"] == ""


def test_collect_merges_packet_reviews_and_recomputes_coverage(tmp_path):
    packet_root = tmp_path / "review_packets"
    _export(packet_root)
    task_id = "reference-task-r01-001"
    review_path = packet_root / task_id / "review.json"
    review = json.loads(review_path.read_text(encoding="utf-8"))
    review.update(
        {
            "decision": "approved",
            "reviewer": "reviewer-test",
            "notes": "The packet is natural, feasible, and sufficiently distinct.",
        }
    )
    review_path.write_text(json.dumps(review), encoding="utf-8")
    central_reviews = tmp_path / "reference_package_reviews.json"
    shutil.copy2(PILOT_ROOT / "reference_package_reviews.json", central_reviews)
    coverage_path = tmp_path / "coverage_state.json"

    summary = collect_packet_reviews(
        repo_root=REPO_ROOT,
        skill_pool_path=PILOT_ROOT / "skill_pool.json",
        packages_path=PILOT_ROOT / "reference_packages.json",
        source_tasks_path=PILOT_ROOT / "source_tasks.json",
        reviews_path=central_reviews,
        artifact_manifest_path=PILOT_ROOT / "artifacts/artifact_manifest.json",
        task_config_manifest_path=PILOT_ROOT / "task_config_manifest.json",
        coverage_path=coverage_path,
        packet_root=packet_root,
    )

    central = json.loads(central_reviews.read_text(encoding="utf-8"))
    merged = {item["reference_task_id"]: item for item in central["reviews"]}
    coverage = json.loads(coverage_path.read_text(encoding="utf-8"))
    assert merged[task_id]["decision"] == "approved"
    assert summary["approved_skill_count"] == 3
    assert len(summary["pending_reference_task_ids"]) == 3
    assert coverage["approved_reference_task_ids"] == [task_id]


def test_collect_rejects_edits_outside_review_json(tmp_path):
    packet_root = tmp_path / "review_packets"
    _export(packet_root)
    task_id = "reference-task-r01-001"
    task_markdown = packet_root / task_id / "TASK.md"
    task_markdown.write_text("tampered\n", encoding="utf-8")
    central_reviews = tmp_path / "reference_package_reviews.json"
    shutil.copy2(PILOT_ROOT / "reference_package_reviews.json", central_reviews)

    with pytest.raises(ValueError, match="Only review.json is editable"):
        collect_packet_reviews(
            repo_root=REPO_ROOT,
            skill_pool_path=PILOT_ROOT / "skill_pool.json",
            packages_path=PILOT_ROOT / "reference_packages.json",
            source_tasks_path=PILOT_ROOT / "source_tasks.json",
            reviews_path=central_reviews,
            artifact_manifest_path=PILOT_ROOT / "artifacts/artifact_manifest.json",
            task_config_manifest_path=PILOT_ROOT / "task_config_manifest.json",
            coverage_path=tmp_path / "coverage_state.json",
            packet_root=packet_root,
            task_id=task_id,
        )
