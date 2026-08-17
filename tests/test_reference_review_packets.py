import json
import shutil
from pathlib import Path

import pytest

from benchmark_construction.reference_review_packets import (
    collect_packet_reviews,
    export_review_packets,
    export_task_details,
)
from benchmark_construction.reviewer_guide_generation import sha256_text


REPO_ROOT = Path(__file__).resolve().parents[1]
PILOT_ROOT = REPO_ROOT / "evaluation_examples/expert_skill_learning/pilot"


def _detail_root(packet_root: Path) -> Path:
    return packet_root.parent / "task_details"


def _guides_path(packet_root: Path) -> Path:
    return packet_root.parent / "reviewer_guides.json"


def _prepare_test_guides(packet_root: Path) -> None:
    detail_root = _detail_root(packet_root)
    export_task_details(
        repo_root=REPO_ROOT,
        skill_pool_path=PILOT_ROOT / "skill_pool.json",
        packages_path=PILOT_ROOT / "reference_packages.json",
        source_tasks_path=PILOT_ROOT / "source_tasks.json",
        reviews_path=PILOT_ROOT / "reference_package_reviews.json",
        artifact_manifest_path=PILOT_ROOT / "artifacts/artifact_manifest.json",
        task_config_manifest_path=PILOT_ROOT / "task_config_manifest.json",
        output_root=detail_root,
    )
    packages = json.loads(
        (PILOT_ROOT / "reference_packages.json").read_text(encoding="utf-8")
    )["reference_packages"]
    guides = []
    for package in packages:
        task_id = package["reference_task_id"]
        detail = (detail_root / task_id / "TASK_DETAIL.md").read_text(
            encoding="utf-8"
        )
        skill_ids = package["required_skill_ids"]
        guides.append(
            {
                "reference_task_id": task_id,
                "task_detail_sha256": sha256_text(detail),
                "guide": {
                    "reference_task_id": task_id,
                    "language": "zh-CN",
                    "overview": "这是一份面向 LibreOffice Calc 新手的参考操作方案。",
                    "starting_state_checks": ["确认工作簿已经打开并显示初始数据。"],
                    "steps": [
                        {
                            "step_number": 1,
                            "title": "完成任务要求",
                            "instructions": ["按照任务要求依次完成表格操作。"],
                            "skill_ids": skill_ids,
                            "efficiency_tip": "先确认目标区域，再集中完成相关设置。",
                            "visible_success_signal": "工作簿显示任务要求的最终结果。",
                        }
                    ],
                    "final_verification": ["检查所有要求的结果都已正确显示。"],
                },
                "generation": {
                    "request_id": "test-request",
                    "prompt_sha256": "0" * 64,
                    "model": "test-model",
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "estimated_cost_usd": None,
                },
            }
        )
    _guides_path(packet_root).write_text(
        json.dumps({"schema_version": "1.0", "guides": guides}),
        encoding="utf-8",
    )


def _export(packet_root: Path, *, force: bool = False) -> list[str]:
    _prepare_test_guides(packet_root)
    return export_review_packets(
        repo_root=REPO_ROOT,
        skill_pool_path=PILOT_ROOT / "skill_pool.json",
        packages_path=PILOT_ROOT / "reference_packages.json",
        source_tasks_path=PILOT_ROOT / "source_tasks.json",
        reviews_path=PILOT_ROOT / "reference_package_reviews.json",
        artifact_manifest_path=PILOT_ROOT / "artifacts/artifact_manifest.json",
        task_config_manifest_path=PILOT_ROOT / "task_config_manifest.json",
        task_detail_root=_detail_root(packet_root),
        reviewer_guides_path=_guides_path(packet_root),
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
    task_detail = (task_dir / "TASK_DETAIL.md").read_text(encoding="utf-8")

    assert len(context["required_skills"]) == 3
    assert all(item["referenced_actions"] for item in context["source_evidence"])
    assert all(item["single_actions"] for item in context["source_evidence"])
    assert review["decision"] == ""
    assert "Workshop Enrollment Queue" in task_markdown
    assert "Directly referenced source actions" in task_markdown
    assert "## Initial artifact" not in task_markdown
    assert "## Expected incidental operations" not in task_markdown
    assert "## Start annotation after approval" not in task_markdown
    assert "## Initial state preview" in task_markdown
    assert "### 中文详细参考方案" in task_markdown
    assert "## Source-task similarity review" in task_markdown
    assert "Complete ordered single-action sequence" in task_markdown
    assert "★ Create a formula-based conditional formatting rule" in task_markdown
    assert "Task naturalness and skill necessity" in task_markdown
    assert "## Initial artifact" in task_detail
    assert "## Expected incidental operations" in task_detail
    assert "## Start annotation after approval" in task_detail
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
        task_detail_root=_detail_root(packet_root),
        reviewer_guides_path=_guides_path(packet_root),
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
            task_detail_root=_detail_root(packet_root),
            reviewer_guides_path=_guides_path(packet_root),
            coverage_path=tmp_path / "coverage_state.json",
            packet_root=packet_root,
            task_id=task_id,
        )
