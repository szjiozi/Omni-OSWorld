#!/usr/bin/env python3
"""Append the Impress v2 and deferred smoke tasks to a Portal pilot snapshot."""

from __future__ import annotations

import argparse
import copy
import json
import shutil
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from benchmark_construction.annotation_portal.aws_workspace import _load_task_config
from benchmark_construction.annotation_portal.catalog import TaskCatalog
from benchmark_construction.reference_annotation import assemble_osworld_annotation_config


DATASET_ROOT = REPO_ROOT / "evaluation_examples/expert_skill_learning/impress_full_v1"
V2_ROOT = DATASET_ROOT / "generated_v2/round_01"
SMOKE_ROOT = DATASET_ROOT / "smoke_tests/deferred_adapter_20260915"
SKILLS_PATH = DATASET_ROOT / "generated_v2/skill_pool.json"


def _read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _write(path: Path, document: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _smoke_task_markdown(package: dict, skills: dict[str, dict], artifact: dict) -> str:
    task_id = package["reference_task_id"]
    lines = [
        f"# {task_id}",
        "",
        "- Application: `libreoffice_impress`",
        "- Review decision: `pending`",
        "- Batch: deferred-skill adapter smoke test",
        "",
        "## Task instruction",
        "",
        package["task_instruction"],
        "",
        "## Required skills",
        "",
    ]
    for skill_id in package["required_skill_ids"]:
        skill = skills[skill_id]
        lines.extend(
            [
                f"### {skill['name']}",
                "",
                f"Skill ID: `{skill_id}`",
                "",
                "Procedure:",
                "",
                *[f"{index}. {step}" for index, step in enumerate(skill["procedure"], 1)],
                "",
                f"Efficiency tip: {skill['efficiency_tip']}",
                f"Source: `{skill['source']['task_id']}`",
                "",
            ]
        )
    specification = package["artifact_spec"]
    lines.extend(
        [
            "## Initial artifact requirements",
            "",
            f"- Domain: {specification['domain']}",
            f"- Presentation title: {specification['presentation_title']}",
            f"- Slide count: {len(specification['slides'])}",
            "",
            "Initial state:",
            "",
            *[f"- {item}" for item in specification["initial_state"]],
            "",
            "Must not already be completed:",
            "",
            *[f"- {item}" for item in specification["must_not_be_completed"]],
            "",
        ]
    )
    lines.extend(["## Initial state preview", "", "![Slides](artifact/previews/contact-sheet.png)", ""])
    lines.extend(["## Operator guide", ""])
    for index, item in enumerate(package["operator_guide"]["recommended_demonstration"], 1):
        lines.extend(
            [
                f"### Demonstration {index}",
                "",
                f"- Skill: `{item['skill_id']}`",
                f"- Intent: {item['operation_intent']}",
                f"- Visible success: {item['visible_success_signal']}",
                f"- Efficiency tip: {item['efficiency_tip']}",
                "",
            ]
        )
    lines.extend(
        [
            f"Allowed variation: {package['operator_guide']['allowed_variation']}",
            "",
            f"Recording start: {package['operator_guide']['recording_start_state']}",
            "",
            f"Recording end: {package['operator_guide']['recording_end_state']}",
            "",
            "## Artifact and review",
            "",
            "[Initial presentation](artifact/initial_artifact.pptx)",
            "",
            "[Review form](review.json)",
            "",
        ]
    )
    if artifact.get("expected_outputs"):
        lines.extend(["Expected output files:", ""])
        lines.extend(
            f"- `{item['guest_path']}` ({item['role']})"
            for item in artifact["expected_outputs"]
        )
        lines.append("")
    similarity = package.get("similarity_reference", {}).get("lexical", {})
    if similarity:
        lines.extend(
            [
                "## Similarity reference (human review aid)",
                "",
                f"- Closest source task: `{similarity['most_similar_source_task_id']}`",
                f"- Sequence similarity: {similarity['max_sequence_similarity']}",
                "",
            ]
        )
    return "\n".join(lines)


def merge_batch(base_root: Path, output_root: Path) -> dict:
    """Copy an immutable live snapshot, then add nine distinct Impress tasks."""
    if output_root.exists():
        raise FileExistsError(output_root)
    shutil.copytree(base_root, output_root)
    package_path = output_root / "reference_packages.json"
    review_path = output_root / "reference_package_reviews.json"
    skill_path = output_root / "skill_pool.json"
    packages_doc = _read(package_path)
    reviews_doc = _read(review_path)
    skills_doc = _read(skill_path)
    old_ids = {item["reference_task_id"] for item in packages_doc["reference_packages"]}
    if old_ids != {item["reference_task_id"] for item in reviews_doc["reviews"]}:
        raise ValueError("Base snapshot package and review IDs differ")
    skills = {item["skill_id"]: item for item in skills_doc["skills"]}
    for skill in _read(SKILLS_PATH)["skills"]:
        old = skills.get(skill["skill_id"])
        if old is not None and old != skill:
            raise ValueError(f"Skill definition conflict: {skill['skill_id']}")
        if old is None:
            skills_doc["skills"].append(skill)
            skills[skill["skill_id"]] = skill

    added: list[str] = []
    for source_root in (V2_ROOT, SMOKE_ROOT):
        source_packages = _read(source_root / "reference_packages.json")["reference_packages"]
        source_reviews = _read(source_root / "reference_package_reviews.json")["reviews"]
        reviews_by_id = {item["reference_task_id"]: item for item in source_reviews}
        artifacts_by_id = {
            item["reference_task_id"]: item
            for item in _read(source_root / "artifacts/artifact_manifest.json")["artifacts"]
        }
        for package in source_packages:
            task_id = package["reference_task_id"]
            if task_id in old_ids or task_id in added:
                raise ValueError(f"Existing task would be overwritten: {task_id}")
            if task_id not in reviews_by_id or task_id not in artifacts_by_id:
                raise ValueError(f"Missing review or artifact for {task_id}")
            if any(skill_id not in skills for skill_id in package["required_skill_ids"]):
                raise ValueError(f"Unknown required skill in {task_id}")
            packet = output_root / "review_packets" / task_id
            artifact_dir = output_root / "artifacts" / task_id
            config_path = output_root / "task_configs" / f"{task_id}.json"
            if any(path.exists() for path in (packet, artifact_dir, config_path)):
                raise ValueError(f"Existing task files would be overwritten: {task_id}")
            artifact = artifacts_by_id[task_id]
            shutil.copytree(source_root / "artifacts" / task_id, artifact_dir)
            if source_root == V2_ROOT:
                shutil.copytree(source_root / "review_packets" / task_id, packet)
                shutil.copy2(source_root / "task_configs" / f"{task_id}.json", config_path)
            else:
                packet.mkdir(parents=True)
                shutil.copytree(artifact_dir, packet / "artifact")
                (packet / "TASK.md").write_text(
                    _smoke_task_markdown(package, skills, artifact), encoding="utf-8"
                )
                _write(packet / "review.json", reviews_by_id[task_id])
                blueprint = {
                    "snapshot": "libreoffice_impress",
                    "artifact_slot": "initial_artifact",
                    "guest_filename": "initial_artifact.pptx",
                    "open_after_upload": True,
                    "ready_state_checks": [
                        "Confirm the supplied presentation is open in LibreOffice Impress."
                    ],
                    "setup_notes": artifact.get("manual_setup_steps", [])[:6],
                }
                config = assemble_osworld_annotation_config(
                    package, artifact, blueprint, repo_root=REPO_ROOT
                )
                _write(config_path, config)
                _write(packet / "task_config.json", config)
                # The Portal resolves uploads from artifacts/<task-id>/<basename>.
                for supporting in artifact.get("supporting_files", []):
                    source = REPO_ROOT / supporting["local_path"]
                    target = artifact_dir / source.name
                    if target.exists():
                        raise ValueError(f"Supporting file basename collision: {target}")
                    shutil.copy2(source, target)
            packages_doc["reference_packages"].append(copy.deepcopy(package))
            reviews_doc["reviews"].append(copy.deepcopy(reviews_by_id[task_id]))
            added.append(task_id)

    _write(package_path, packages_doc)
    _write(review_path, reviews_doc)
    _write(skill_path, skills_doc)
    catalog = TaskCatalog.load(
        packages_path=package_path,
        skills_path=skill_path,
        reviews_path=review_path,
        allow_pending=True,
    )
    for task_id in added:
        _load_task_config(output_root / "task_configs" / f"{task_id}.json")
    return {
        "old_task_count": len(old_ids),
        "new_task_ids": added,
        "total_task_count": len(catalog.all()),
        "catalog_version": catalog.all()[0].catalog_version,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(merge_batch(args.base_root, args.output_root), indent=2))


if __name__ == "__main__":
    main()
