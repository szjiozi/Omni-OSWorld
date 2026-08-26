"""Create self-contained, per-task packets for reference-package review."""

from __future__ import annotations

import hashlib
import html
import json
import os
import re
import shlex
import shutil
import tempfile
from pathlib import Path
from typing import Any, Iterable, Sequence

from .osworld_human import load_source_manifest
from .reference_generation import load_skill_pool
from .reference_applications import get_reference_application
from .reference_review import (
    compute_review_state,
    load_reference_packages,
    load_reference_review_forms,
    validate_reference_review_form,
    write_coverage_state,
)
from .reviewer_guide_generation import (
    load_reviewer_guides,
    sha256_text,
    validate_reviewer_guide,
)


PACKET_SCHEMA_VERSION = "1.0"
SAFE_TASK_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


def _blank_review(task_id: str) -> dict[str, Any]:
    return {
        "reference_task_id": task_id,
        "decision": "",
        "reason_codes": [],
        "revision_instructions": [],
        "reviewer": "",
        "notes": "",
    }


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _json_fingerprint(value: Any) -> str:
    payload = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        dir=path.parent, prefix=f".{path.name}.", suffix=".tmp"
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(content)
        temporary.replace(path)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def _atomic_write_json(path: Path, value: Any) -> None:
    _atomic_write(
        path,
        json.dumps(value, indent=2, ensure_ascii=False) + "\n",
    )


def _atomic_copy(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        dir=destination.parent, prefix=f".{destination.name}.", suffix=".tmp"
    )
    os.close(descriptor)
    temporary = Path(temporary_name)
    try:
        shutil.copy2(source, temporary)
        temporary.replace(destination)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def _resolve_repo_path(repo_root: Path, value: str | Path) -> Path:
    path = Path(value)
    resolved = (path if path.is_absolute() else repo_root / path).resolve()
    try:
        resolved.relative_to(repo_root.resolve())
    except ValueError as exc:
        raise ValueError(
            f"Packet input must remain inside the repository: {path}"
        ) from exc
    return resolved


def _repo_relative(repo_root: Path, path: Path) -> str:
    return path.resolve().relative_to(repo_root.resolve()).as_posix()


def _entries_by_id(path: Path, key: str, label: str) -> dict[str, dict[str, Any]]:
    document = json.loads(path.read_text(encoding="utf-8"))
    entries = document.get(key)
    if not isinstance(entries, list):
        raise ValueError(f"{path} has no {key} list")
    result: dict[str, dict[str, Any]] = {}
    for entry in entries:
        task_id = entry.get("reference_task_id")
        if not isinstance(task_id, str) or not task_id:
            raise ValueError(f"{path} contains a {label} without a task ID")
        if task_id in result:
            raise ValueError(f"Duplicate {label} task ID: {task_id}")
        result[task_id] = entry
    return result


def _select_packages(
    packages: Sequence[dict[str, Any]], task_id: str | None
) -> list[dict[str, Any]]:
    if task_id is None:
        return list(packages)
    matches = [item for item in packages if item["reference_task_id"] == task_id]
    if len(matches) != 1:
        raise ValueError(f"Unknown reference task ID: {task_id}")
    return matches


def _source_evidence(
    required_skills: Sequence[dict[str, Any]], source_by_id: dict[str, Any]
) -> list[dict[str, Any]]:
    evidence: list[dict[str, Any]] = []
    skill_ids_by_source: dict[str, list[str]] = {}
    action_ids_by_source: dict[str, set[int]] = {}
    for skill in required_skills:
        source = skill["source"]
        source_id = source["task_id"]
        skill_ids_by_source.setdefault(source_id, []).append(skill["skill_id"])
        action_ids_by_source.setdefault(source_id, set()).update(source["action_ids"])

    for source_id in sorted(skill_ids_by_source):
        if source_id not in source_by_id:
            raise ValueError(
                f"Required skill references unknown source task {source_id}"
            )
        source_task = source_by_id[source_id]
        action_ids = sorted(action_ids_by_source[source_id])
        invalid = [item for item in action_ids if item >= len(source_task.single_steps)]
        if invalid:
            raise ValueError(
                f"Source task {source_id} has no actions at indices {invalid}"
            )
        evidence.append(
            {
                "task_id": source_id,
                "instruction": source_task.instruction,
                "required_skill_ids": skill_ids_by_source[source_id],
                "referenced_actions": [
                    {
                        "action_id": action_id,
                        "action": source_task.single_steps[action_id],
                    }
                    for action_id in action_ids
                ],
                "single_actions": list(source_task.single_steps),
            }
        )
    return evidence


def _markdown_list(items: Iterable[str], *, empty: str = "None.") -> list[str]:
    values = list(items)
    return [f"- {item}" for item in values] if values else [empty]


def _render_similarity(package: dict[str, Any]) -> list[str]:
    similarity = package.get("similarity_reference", {})
    lexical = similarity.get("lexical", {})
    semantic = similarity.get("semantic", {})
    lines = [
        "| Measure | Maximum | Most similar source task |",
        "| --- | ---: | --- |",
        (
            "| Lexical sequence similarity | "
            f"{lexical.get('max_sequence_similarity', 'n/a')} | "
            f"{lexical.get('most_similar_source_task_id', 'n/a')} |"
        ),
        (
            "| Semantic cosine similarity | "
            f"{semantic.get('max_cosine_similarity', 'n/a')} | "
            f"{semantic.get('most_similar_source_task_id', 'n/a')} |"
        ),
    ]
    return lines


def _render_task_detail_markdown(
    package: dict[str, Any],
    required_skills: Sequence[dict[str, Any]],
    source_evidence: Sequence[dict[str, Any]],
    preview_names: Sequence[str],
    review: dict[str, Any],
) -> str:
    task_id = package["reference_task_id"]
    profile = get_reference_application(package.get("app", "libreoffice_calc"))
    artifact_spec = package.get("artifact_spec", {})
    guide = package.get("operator_guide", {})
    title = artifact_spec.get(profile.title_field) or task_id
    lines = [
        f"# {title}",
        "",
        f"- Reference task: `{task_id}`",
        f"- Application: `{package.get('app', '')}`",
        f"- Review decision: `{review['decision'] or 'pending'}`",
        "",
        "## Task instruction",
        "",
        package.get("task_instruction", ""),
        "",
        "## Required skills",
        "",
    ]
    evidence_by_id = {item["task_id"]: item for item in source_evidence}
    for index, skill in enumerate(required_skills, start=1):
        source = skill["source"]
        evidence = evidence_by_id[source["task_id"]]
        referenced = {
            item["action_id"]: item["action"] for item in evidence["referenced_actions"]
        }
        lines.extend(
            [
                f"### {index}. {skill['name']}",
                "",
                f"Skill ID: `{skill['skill_id']}`",
                "",
                "Procedure:",
                "",
            ]
        )
        lines.extend(
            f"{step_index}. {step}"
            for step_index, step in enumerate(skill["procedure"], start=1)
        )
        lines.extend(
            [
                "",
                f"Efficiency tip: {skill['efficiency_tip']}",
                "",
                f"Source task: `{source['task_id']}`",
                "",
                f"Source instruction: {evidence['instruction']}",
                "",
                "Directly referenced source actions:",
                "",
            ]
        )
        lines.extend(
            f"- Action {action_id}: <code>{html.escape(referenced[action_id])}</code>"
            for action_id in source["action_ids"]
        )
        lines.append("")

    lines.extend(
        [
            "## Initial artifact",
            "",
            f"- Domain: {artifact_spec.get('domain', '')}",
            f"- {profile.artifact_label}: "
            f"[{profile.packet_artifact_filename}]"
            f"(artifact/{profile.packet_artifact_filename})",
            f"- Blueprint: [artifact_blueprint.json](artifact/artifact_blueprint.json)",
            f"- QA report: [artifact_qa.json](artifact/artifact_qa.json)",
            "",
            "Initial state:",
            "",
        ]
    )
    lines.extend(_markdown_list(artifact_spec.get("initial_state", [])))
    lines.extend(["", "Artifact construction requirements:", ""])
    lines.extend(_markdown_list(artifact_spec.get("generation_notes", [])))
    sheets = artifact_spec.get("sheets", [])
    if sheets:
        lines.extend(
            [
                "",
                "| Sheet | Rows | Purpose | Columns |",
                "| --- | ---: | --- | --- |",
            ]
        )
        for sheet in sheets:
            columns = ", ".join(
                f"{column.get('name', '')} ({column.get('data_type', '')})"
                for column in sheet.get("columns", [])
            )
            lines.append(
                f"| {sheet.get('name', '')} | {sheet.get('row_count', '')} | "
                f"{sheet.get('purpose', '')} | {columns} |"
            )
    slides = artifact_spec.get("slides", [])
    if slides:
        lines.extend(
            [
                "",
                "| Slide | Layout | Purpose | Editable objects |",
                "| ---: | --- | --- | --- |",
            ]
        )
        for slide in slides:
            objects = ", ".join(
                f"{item.get('semantic_id', '')} ({item.get('type', '')})"
                for item in slide.get("object_plan", [])
            )
            lines.append(
                f"| {slide.get('slide_number', '')} | {slide.get('layout', '')} | "
                f"{slide.get('purpose', '')} | {objects} |"
            )
    lines.extend(["", "Must remain incomplete before recording:", ""])
    lines.extend(_markdown_list(artifact_spec.get("must_not_be_completed", [])))
    if preview_names:
        lines.extend(["", "Artifact previews:", ""])
        for preview_name in preview_names:
            lines.extend(
                [
                    f"### {Path(preview_name).stem.replace('_', ' ')}",
                    "",
                    f"![{preview_name}](artifact/previews/{preview_name})",
                    "",
                ]
            )

    lines.extend(["## Operator guide", ""])
    for index, item in enumerate(guide.get("recommended_demonstration", []), start=1):
        lines.extend(
            [
                f"### Demonstration {index}",
                "",
                f"- Skill: `{item.get('skill_id', '')}`",
                f"- Intent: {item.get('operation_intent', '')}",
                f"- Efficiency: {item.get('efficiency_tip', '')}",
                f"- Visible success: {item.get('visible_success_signal', '')}",
                "",
            ]
        )
    lines.extend(
        [
            f"Recording start: {guide.get('recording_start_state', '')}",
            "",
            f"Recording end: {guide.get('recording_end_state', '')}",
            "",
            f"Allowed variation: {guide.get('allowed_variation', '')}",
            "",
            "## Expected incidental operations",
            "",
        ]
    )
    incidental = package.get("expected_incidental_operations", [])
    if incidental:
        for item in incidental:
            lines.append(
                f"- **{item.get('category', '')}:** {item.get('operation', '')} "
                f"Reason: {item.get('reason', '')}"
            )
    else:
        lines.append("None.")
    lines.extend(["", "## Source-similarity audit", ""])
    lines.extend(_render_similarity(package))
    lines.extend(
        [
            "",
            "Scores are reviewer aids, not automatic acceptance thresholds. Compare the "
            "task with the source instructions and actions above for solution leakage.",
            "",
            "## Review this package",
            "",
            "Check that every required skill is necessary and observable, the task is "
            "natural and not a source-solution reproduction, incidental operations are "
            "limited, the artifact matches its specification, and the guide remains "
            "helpful without prescribing one click-by-click trajectory.",
            "",
            "1. Inspect the task, required skills, source evidence, artifact, and guide.",
            "2. Fill [review.json](review.json) using `approved`, "
            "`revision_requested`, or `rejected`.",
            "3. From the repository root, collect all completed forms:",
            "",
            "```bash",
            "python scripts/python/manage_reference_review_packets.py collect",
            "```",
            "",
            "Detailed field guidance is in " "[`reviewer.md`](../../../reviewer.md).",
            "",
            "## Start annotation after approval",
            "",
            "```bash",
            "python scripts/python/record_reference_task.py \\",
            f"  --reference-task-id {task_id}",
            "```",
            "",
            "The ordinary launcher reads the collected central review file and refuses "
            "pending, revision-requested, or rejected tasks.",
        ]
    )
    return "\n".join(lines) + "\n"


def _render_reviewer_guide(guide: dict[str, Any]) -> list[str]:
    lines = [
        "### 中文详细参考方案",
        "",
        "> 以下是一个可以参考的操作 guide。标注者可以根据实际 LibreOffice "
        "界面采用等价操作。",
        "",
        guide["overview"],
        "",
        "#### 启动后的初始状态检查",
        "",
    ]
    lines.extend(f"- {item}" for item in guide["starting_state_checks"])
    for step in guide["steps"]:
        lines.extend(
            [
                "",
                f"#### 第 {step['step_number']} 步：{step['title']}",
                "",
            ]
        )
        lines.extend(
            f"{index}. {instruction}"
            for index, instruction in enumerate(step["instructions"], start=1)
        )
        skill_ids = step["skill_ids"]
        lines.extend(
            [
                "",
                "- 对应 skills："
                + (
                    ", ".join(f"`{skill_id}`" for skill_id in skill_ids)
                    if skill_ids
                    else "无；这是准备或检查步骤。"
                ),
                f"- 高效操作：{step['efficiency_tip']}",
                f"- 完成标志：{step['visible_success_signal']}",
            ]
        )
    lines.extend(["", "#### 最终结果检查", ""])
    lines.extend(f"- {item}" for item in guide["final_verification"])
    return lines


def _render_source_similarity_review(
    package: dict[str, Any],
    required_skills: Sequence[dict[str, Any]],
    source_evidence: Sequence[dict[str, Any]],
) -> list[str]:
    lines = ["## Source-task similarity review", ""]
    lines.extend(_render_similarity(package))
    lines.extend(
        [
            "",
            "Similarity scores are reviewer aids, not automatic acceptance thresholds. "
            "Inspect the contributing source tasks and their complete ordered actions below.",
        ]
    )
    skill_by_id = {item["skill_id"]: item for item in required_skills}
    for evidence in source_evidence:
        source_id = evidence["task_id"]
        source_skills = [
            skill_by_id[skill_id] for skill_id in evidence["required_skill_ids"]
        ]
        action_to_skills: dict[int, list[dict[str, Any]]] = {}
        for skill in source_skills:
            for action_id in skill["source"]["action_ids"]:
                action_to_skills.setdefault(action_id, []).append(skill)
        lines.extend(
            [
                "",
                f"### Source task `{source_id}`",
                "",
                "Original instruction:",
                "",
                f"> {evidence['instruction']}",
                "",
                "Required skills derived from this source task:",
                "",
            ]
        )
        lines.extend(
            f"- **{skill['name']}** — `{skill['skill_id']}`"
            for skill in source_skills
        )
        lines.extend(
            [
                "",
                "Complete ordered single-action sequence:",
                "",
                "| Action | Related required skill | Original single action |",
                "| ---: | --- | --- |",
            ]
        )
        for action_id, action in enumerate(evidence["single_actions"]):
            related_skills = action_to_skills.get(action_id, [])
            escaped_action = html.escape(action).replace("|", "&#124;")
            if related_skills:
                related = "<br>".join(
                    "<strong>★ "
                    + html.escape(skill["name"])
                    + "</strong><br><code>"
                    + html.escape(skill["skill_id"])
                    + "</code>"
                    for skill in related_skills
                )
                action_cell = f"<strong><code>{escaped_action}</code></strong>"
            else:
                related = ""
                action_cell = f"<code>{escaped_action}</code>"
            lines.append(f"| {action_id} | {related} | {action_cell} |")
    return lines


def _render_task_markdown(
    package: dict[str, Any],
    required_skills: Sequence[dict[str, Any]],
    source_evidence: Sequence[dict[str, Any]],
    preview_names: Sequence[str],
    review: dict[str, Any],
    reviewer_guide: dict[str, Any],
    collect_command: str,
    reviewer_doc_link: str,
) -> str:
    task_id = package["reference_task_id"]
    profile = get_reference_application(package.get("app", "libreoffice_calc"))
    artifact_spec = package.get("artifact_spec", {})
    operator_guide = package.get("operator_guide", {})
    title = artifact_spec.get(profile.title_field) or task_id
    natural_task_label = (
        "natural Calc task" if profile.app == "libreoffice_calc" else "natural Impress task"
    )
    artifact_noun = "workbook" if profile.app == "libreoffice_calc" else "presentation"
    artifact_contents = "data" if profile.app == "libreoffice_calc" else "content"
    lines = [
        f"# {title}",
        "",
        f"- Reference task: `{task_id}`",
        f"- Application: `{package.get('app', '')}`",
        f"- Review decision: `{review['decision'] or 'pending'}`",
        "",
        "## Task instruction",
        "",
        package.get("task_instruction", ""),
        "",
        "## Required skills",
        "",
    ]
    evidence_by_id = {item["task_id"]: item for item in source_evidence}
    for index, skill in enumerate(required_skills, start=1):
        source = skill["source"]
        evidence = evidence_by_id[source["task_id"]]
        referenced = {
            item["action_id"]: item["action"] for item in evidence["referenced_actions"]
        }
        lines.extend(
            [
                f"### {index}. {skill['name']}",
                "",
                f"Skill ID: `{skill['skill_id']}`",
                "",
                "Procedure:",
                "",
            ]
        )
        lines.extend(
            f"{step_index}. {step}"
            for step_index, step in enumerate(skill["procedure"], start=1)
        )
        lines.extend(
            [
                "",
                f"Efficiency tip: {skill['efficiency_tip']}",
                "",
                f"Source task: `{source['task_id']}`",
                "",
                f"Source instruction: {evidence['instruction']}",
                "",
                "Directly referenced source actions:",
                "",
            ]
        )
        lines.extend(
            f"- Action {action_id}: <code>{html.escape(referenced[action_id])}</code>"
            for action_id in source["action_ids"]
        )
        lines.append("")

    if preview_names:
        lines.extend(["## Initial state preview", ""])
        for preview_name in preview_names:
            lines.extend(
                [
                    f"### {Path(preview_name).stem.replace('_', ' ')}",
                    "",
                    f"![{preview_name}](artifact/previews/{preview_name})",
                    "",
                ]
            )

    lines.extend(["## Operator guide", "", "### Existing operation-intent guide", ""])
    for index, item in enumerate(
        operator_guide.get("recommended_demonstration", []), start=1
    ):
        lines.extend(
            [
                f"#### Demonstration {index}",
                "",
                f"- Skill: `{item.get('skill_id', '')}`",
                f"- Intent: {item.get('operation_intent', '')}",
                f"- Efficiency: {item.get('efficiency_tip', '')}",
                f"- Visible success: {item.get('visible_success_signal', '')}",
                "",
            ]
        )
    lines.extend(
        [
            f"Recording start: {operator_guide.get('recording_start_state', '')}",
            "",
            f"Recording end: {operator_guide.get('recording_end_state', '')}",
            "",
            f"Allowed variation: {operator_guide.get('allowed_variation', '')}",
            "",
        ]
    )
    lines.extend(_render_reviewer_guide(reviewer_guide))
    lines.extend([""])
    lines.extend(
        _render_source_similarity_review(package, required_skills, source_evidence)
    )
    lines.extend(
        [
            "",
            "## Review this package",
            "",
            "Before choosing a decision, complete all three checks:",
            "",
            "- [ ] **Task naturalness and skill necessity:** Is the reference task a "
            f"{natural_task_label}, and is every listed required skill genuinely necessary "
            "and observable when solving it?",
            "- [ ] **Initial artifact correctness:** Launch the environment and confirm "
            f"that the {artifact_noun} opens correctly, contains the {artifact_contents} needed by the "
            "instruction, and has not already completed the requested results.",
            "- [ ] **Source-task similarity:** Compare the reference task with the source "
            "instructions and complete single-action sequences above. Confirm that it is "
            "not merely an entity, field, or value substitution and does not reproduce a "
            "source task's complete ordered solution.",
            "",
            "Use `approved` when all checks pass. Use `revision_requested` when the "
            "package is fixable and provide concrete revision instructions. Use "
            "`rejected` when the combination is fundamentally unnatural, infeasible, or "
            "too similar to a source task.",
            "",
            "Fill [review.json](review.json), then collect completed forms from the "
            "repository root:",
            "",
            "```bash",
            collect_command,
            "```",
            "",
            f"Detailed field guidance is in [`reviewer.md`]({reviewer_doc_link}).",
        ]
    )
    return "\n".join(lines) + "\n"


def _input_descriptor(repo_root: Path, role: str, path: Path) -> dict[str, str]:
    return {
        "role": role,
        "path": _repo_relative(repo_root, path),
        "sha256": _sha256(path),
    }


def _packet_review(packet_dir: Path) -> dict[str, Any] | None:
    path = packet_dir / "review.json"
    if not path.exists():
        return None
    review = json.loads(path.read_text(encoding="utf-8"))
    validate_reference_review_form(review)
    return review


def _prepare_packet_data(
    *,
    repo_root: Path,
    package: dict[str, Any],
    skill_by_id: dict[str, dict[str, Any]],
    source_by_id: dict[str, Any],
    artifact_by_id: dict[str, dict[str, Any]],
    config_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    task_id = package["reference_task_id"]
    if task_id not in artifact_by_id:
        raise ValueError(f"No artifact manifest entry exists for {task_id}")
    if task_id not in config_by_id:
        raise ValueError(f"No task config manifest entry exists for {task_id}")
    try:
        required_skills = [skill_by_id[item] for item in package["required_skill_ids"]]
    except KeyError as exc:
        raise ValueError(
            f"Package {task_id} references unknown skill {exc.args[0]}"
        ) from exc
    evidence = _source_evidence(required_skills, source_by_id)
    artifact_entry = artifact_by_id[task_id]
    config_entry = config_by_id[task_id]
    artifact_path = _resolve_repo_path(repo_root, artifact_entry["artifact_path"])
    blueprint_path = _resolve_repo_path(repo_root, artifact_entry["blueprint_path"])
    qa_path = _resolve_repo_path(repo_root, artifact_entry["qa_path"])
    task_config_path = _resolve_repo_path(repo_root, config_entry["task_config_path"])
    for required_path in (artifact_path, blueprint_path, qa_path, task_config_path):
        if not required_path.is_file():
            raise FileNotFoundError(required_path)
    if _sha256(artifact_path) != artifact_entry["artifact_sha256"]:
        raise ValueError(f"Artifact SHA256 mismatch for {task_id}")
    preview_paths = sorted(
        path
        for path in (artifact_path.parent / "previews").glob("*")
        if path.is_file() and path.name != ".DS_Store"
    )
    input_files = [
        _input_descriptor(repo_root, "artifact", artifact_path),
        _input_descriptor(repo_root, "artifact_blueprint", blueprint_path),
        _input_descriptor(repo_root, "artifact_qa", qa_path),
        _input_descriptor(repo_root, "task_config", task_config_path),
    ]
    input_files.extend(
        _input_descriptor(repo_root, "artifact_preview", path) for path in preview_paths
    )
    context_seed = {
        "package": package,
        "required_skills": required_skills,
        "source_evidence": evidence,
        "artifact_entry": artifact_entry,
        "task_config_entry": config_entry,
        "input_files": input_files,
    }
    return {
        "package": package,
        "skills": required_skills,
        "evidence": evidence,
        "artifact_entry": artifact_entry,
        "config_entry": config_entry,
        "artifact_path": artifact_path,
        "blueprint_path": blueprint_path,
        "qa_path": qa_path,
        "task_config_path": task_config_path,
        "preview_paths": preview_paths,
        "input_files": input_files,
        "fingerprint": _json_fingerprint(context_seed),
    }


def export_task_details(
    *,
    repo_root: Path,
    skill_pool_path: Path,
    packages_path: Path,
    source_tasks_path: Path,
    reviews_path: Path,
    artifact_manifest_path: Path,
    task_config_manifest_path: Path,
    output_root: Path,
    task_id: str | None = None,
) -> list[str]:
    """Render the former full TASK.md as immutable LLM input documents."""

    repo_root = repo_root.resolve()
    skills = load_skill_pool(skill_pool_path)
    skill_by_id = {skill.skill_id: skill.to_dict() for skill in skills}
    source_by_id = {
        task.task_id: task for task in load_source_manifest(source_tasks_path)
    }
    all_packages = load_reference_packages([packages_path])
    packages = _select_packages(all_packages, task_id)
    reviews = {
        item["reference_task_id"]: item
        for item in load_reference_review_forms(reviews_path)
    }
    artifact_by_id = _entries_by_id(
        artifact_manifest_path, "artifacts", "artifact manifest entry"
    )
    config_by_id = _entries_by_id(
        task_config_manifest_path, "task_configs", "task config manifest entry"
    )
    output_root.mkdir(parents=True, exist_ok=True)
    exported: list[str] = []
    for package in packages:
        current_id = package["reference_task_id"]
        if current_id not in reviews:
            raise ValueError(f"No central review form exists for {current_id}")
        item = _prepare_packet_data(
            repo_root=repo_root,
            package=package,
            skill_by_id=skill_by_id,
            source_by_id=source_by_id,
            artifact_by_id=artifact_by_id,
            config_by_id=config_by_id,
        )
        detail = _render_task_detail_markdown(
            package,
            item["skills"],
            item["evidence"],
            [path.name for path in item["preview_paths"]],
            reviews[current_id],
        )
        _atomic_write(output_root / current_id / "TASK_DETAIL.md", detail)
        exported.append(current_id)
    return exported


def _add_reviewer_guide(
    *,
    packet_data: dict[str, Any],
    task_detail_path: Path,
    guide_entry: dict[str, Any],
) -> None:
    package = packet_data["package"]
    task_id = package["reference_task_id"]
    detail = task_detail_path.read_text(encoding="utf-8")
    actual_detail_hash = sha256_text(detail)
    if guide_entry["task_detail_sha256"] != actual_detail_hash:
        raise ValueError(
            f"Reviewer guide for {task_id} is stale because TASK_DETAIL.md changed"
        )
    validate_reviewer_guide(
        task_id, package["required_skill_ids"], guide_entry["guide"]
    )
    input_files = list(packet_data["input_files"])
    context_seed = {
        "package": package,
        "required_skills": packet_data["skills"],
        "source_evidence": packet_data["evidence"],
        "artifact_entry": packet_data["artifact_entry"],
        "task_config_entry": packet_data["config_entry"],
        "reviewer_guide": guide_entry,
        "input_files": input_files,
    }
    packet_data.update(
        {
            "task_detail_path": task_detail_path,
            "reviewer_guide_entry": guide_entry,
            "input_files": input_files,
            "fingerprint": _json_fingerprint(context_seed),
        }
    )


def export_review_packets(
    *,
    repo_root: Path,
    skill_pool_path: Path,
    packages_path: Path,
    source_tasks_path: Path,
    reviews_path: Path,
    artifact_manifest_path: Path,
    task_config_manifest_path: Path,
    task_detail_root: Path,
    reviewer_guides_path: Path,
    output_root: Path,
    task_id: str | None = None,
    force: bool = False,
) -> list[str]:
    """Export deterministic task packets while preserving local review edits."""

    repo_root = repo_root.resolve()
    skills = load_skill_pool(skill_pool_path)
    skill_by_id = {skill.skill_id: skill.to_dict() for skill in skills}
    source_tasks = load_source_manifest(source_tasks_path)
    source_by_id = {task.task_id: task for task in source_tasks}
    all_packages = load_reference_packages([packages_path])
    packages = _select_packages(all_packages, task_id)
    central_reviews = {
        item["reference_task_id"]: item
        for item in load_reference_review_forms(reviews_path)
    }
    artifact_by_id = _entries_by_id(
        artifact_manifest_path, "artifacts", "artifact manifest entry"
    )
    config_by_id = _entries_by_id(
        task_config_manifest_path, "task_configs", "task config manifest entry"
    )
    reviewer_guides = load_reviewer_guides(reviewer_guides_path)
    output_root.mkdir(parents=True, exist_ok=True)
    coverage_path = reviews_path.with_name("coverage_state.json")
    collect_command = _collect_command(
        skill_pool_path=skill_pool_path,
        packages_path=packages_path,
        source_tasks_path=source_tasks_path,
        reviews_path=reviews_path,
        artifact_manifest_path=artifact_manifest_path,
        task_config_manifest_path=task_config_manifest_path,
        task_detail_root=task_detail_root,
        reviewer_guides_path=reviewer_guides_path,
        coverage_path=coverage_path,
        packet_root=output_root,
    )

    prepared: list[dict[str, Any]] = []
    for package in packages:
        current_id = package["reference_task_id"]
        if not SAFE_TASK_ID.fullmatch(current_id):
            raise ValueError(f"Unsafe reference task ID: {current_id!r}")
        if current_id not in central_reviews:
            raise ValueError(f"No central review form exists for {current_id}")
        if current_id not in reviewer_guides:
            raise ValueError(f"No reviewer guide exists for {current_id}")
        packet_data = _prepare_packet_data(
            repo_root=repo_root,
            package=package,
            skill_by_id=skill_by_id,
            source_by_id=source_by_id,
            artifact_by_id=artifact_by_id,
            config_by_id=config_by_id,
        )
        task_detail_path = (
            task_detail_root / current_id / "TASK_DETAIL.md"
        ).resolve()
        if not task_detail_path.is_file():
            raise FileNotFoundError(task_detail_path)
        _add_reviewer_guide(
            packet_data=packet_data,
            task_detail_path=task_detail_path,
            guide_entry=reviewer_guides[current_id],
        )
        fingerprint = packet_data["fingerprint"]
        packet_dir = output_root / current_id
        existing_review = _packet_review(packet_dir)
        existing_manifest_path = packet_dir / "manifest.json"
        old_fingerprint = None
        if existing_manifest_path.exists():
            old_fingerprint = json.loads(
                existing_manifest_path.read_text(encoding="utf-8")
            ).get("context_fingerprint")
        stale_completed = (
            old_fingerprint != fingerprint
            and existing_review is not None
            and bool(existing_review["decision"])
        )
        if stale_completed and not force:
            raise ValueError(
                f"Packet {current_id} changed after review. Re-run export with "
                "--force to reset its per-task review before re-reviewing."
            )
        if stale_completed and force:
            review = _blank_review(current_id)
        else:
            review = existing_review or central_reviews[current_id]
        packet_data.update({"packet_dir": packet_dir, "review": review})
        prepared.append(packet_data)

    exported: list[str] = []
    for item in prepared:
        package = item["package"]
        current_id = package["reference_task_id"]
        profile = get_reference_application(
            package.get("app", "libreoffice_calc")
        )
        packet_dir = item["packet_dir"]
        artifact_dir = packet_dir / "artifact"
        packet_artifact = artifact_dir / profile.packet_artifact_filename
        _atomic_copy(item["artifact_path"], packet_artifact)
        _atomic_copy(item["blueprint_path"], artifact_dir / "artifact_blueprint.json")
        _atomic_copy(item["qa_path"], artifact_dir / "artifact_qa.json")
        for preview_path in item["preview_paths"]:
            _atomic_copy(preview_path, artifact_dir / "previews" / preview_path.name)
        _atomic_copy(item["task_config_path"], packet_dir / "task_config.json")
        _atomic_copy(item["task_detail_path"], packet_dir / "TASK_DETAIL.md")

        context = {
            "schema_version": PACKET_SCHEMA_VERSION,
            "reference_task_id": current_id,
            "package": package,
            "required_skills": item["skills"],
            "source_evidence": item["evidence"],
            "reviewer_guide": item["reviewer_guide_entry"],
            "artifact": {
                "manifest_entry": item["artifact_entry"],
                "packet_path": f"artifact/{profile.packet_artifact_filename}",
            },
            "task_config": {
                "manifest_entry": item["config_entry"],
                "packet_path": "task_config.json",
            },
        }
        _atomic_write_json(packet_dir / "context.json", context)
        _atomic_write_json(packet_dir / "review.json", item["review"])
        _atomic_write(
            packet_dir / "TASK.md",
            _render_task_markdown(
                package,
                item["skills"],
                item["evidence"],
                [path.name for path in item["preview_paths"]],
                item["review"],
                item["reviewer_guide_entry"]["guide"],
                collect_command,
                Path(
                    os.path.relpath(
                        repo_root
                        / "evaluation_examples/expert_skill_learning/reviewer.md",
                        packet_dir,
                    )
                ).as_posix(),
            ),
        )

        generated_files = [
            packet_dir / "TASK.md",
            packet_dir / "TASK_DETAIL.md",
            packet_dir / "context.json",
            packet_dir / "task_config.json",
            packet_artifact,
            artifact_dir / "artifact_blueprint.json",
            artifact_dir / "artifact_qa.json",
            *(artifact_dir / "previews" / path.name for path in item["preview_paths"]),
        ]
        manifest = {
            "schema_version": PACKET_SCHEMA_VERSION,
            "generated_by": "scripts/python/manage_reference_review_packets.py export",
            "reference_task_id": current_id,
            "context_fingerprint": item["fingerprint"],
            "inputs": item["input_files"],
            "generated_files": [
                {
                    "path": path.relative_to(packet_dir).as_posix(),
                    "sha256": _sha256(path),
                }
                for path in generated_files
            ],
            "editable_review": {
                "path": "review.json",
                "excluded_from_generated_file_hashes": True,
            },
        }
        _atomic_write_json(packet_dir / "manifest.json", manifest)
        exported.append(current_id)

    available_ids = [
        package["reference_task_id"]
        for package in all_packages
        if (output_root / package["reference_task_id"] / "TASK.md").is_file()
    ]
    _write_index(output_root, all_packages, available_ids, collect_command)
    return exported


def _collect_command(
    *,
    skill_pool_path: Path,
    packages_path: Path,
    source_tasks_path: Path,
    reviews_path: Path,
    artifact_manifest_path: Path,
    task_config_manifest_path: Path,
    task_detail_root: Path,
    reviewer_guides_path: Path,
    coverage_path: Path,
    packet_root: Path,
) -> str:
    options = [
        ("--skill-pool", skill_pool_path),
        ("--packages", packages_path),
        ("--source-tasks", source_tasks_path),
        ("--reviews", reviews_path),
        ("--artifact-manifest", artifact_manifest_path),
        ("--task-config-manifest", task_config_manifest_path),
        ("--task-detail-root", task_detail_root),
        ("--reviewer-guides", reviewer_guides_path),
        ("--coverage", coverage_path),
        ("--packet-root", packet_root),
    ]
    lines = ["python scripts/python/manage_reference_review_packets.py collect \\"]
    for index, (name, value) in enumerate(options):
        suffix = " \\" if index < len(options) - 1 else ""
        lines.append(f"  {name} {shlex.quote(str(value))}{suffix}")
    return "\n".join(lines)


def _write_index(
    output_root: Path,
    packages: Sequence[dict[str, Any]],
    exported_ids: Sequence[str],
    collect_command: str,
) -> None:
    exported = set(exported_ids)
    rows = [
        "# Reference task review packets",
        "",
        "Open one task directory at a time, read `TASK.md`, and fill only its "
        "`review.json` file.",
        "",
        "| Task | Artifact | Local review |",
        "| --- | --- | --- |",
    ]
    for package in packages:
        task_id = package["reference_task_id"]
        if task_id not in exported:
            continue
        review = _packet_review(output_root / task_id) or _blank_review(task_id)
        profile = get_reference_application(
            package.get("app", "libreoffice_calc")
        )
        title = package.get("artifact_spec", {}).get(profile.title_field, task_id)
        rows.append(
            f"| [{task_id}]({task_id}/TASK.md) | {title} | "
            f"{review['decision'] or 'pending'} |"
        )
    rows.extend(
        [
            "",
            "After reviewing tasks, run:",
            "",
            "```bash",
            collect_command,
            "```",
            "",
        ]
    )
    _atomic_write(output_root / "index.md", "\n".join(rows))


def collect_packet_reviews(
    *,
    repo_root: Path,
    skill_pool_path: Path,
    packages_path: Path,
    source_tasks_path: Path,
    reviews_path: Path,
    artifact_manifest_path: Path,
    task_config_manifest_path: Path,
    task_detail_root: Path,
    reviewer_guides_path: Path,
    coverage_path: Path,
    packet_root: Path,
    task_id: str | None = None,
) -> dict[str, Any]:
    """Merge validated per-task review forms into the central review document."""

    skills = load_skill_pool(skill_pool_path)
    skill_by_id = {skill.skill_id: skill.to_dict() for skill in skills}
    source_by_id = {
        source.task_id: source for source in load_source_manifest(source_tasks_path)
    }
    packages = load_reference_packages([packages_path])
    artifact_by_id = _entries_by_id(
        artifact_manifest_path, "artifacts", "artifact manifest entry"
    )
    config_by_id = _entries_by_id(
        task_config_manifest_path, "task_configs", "task config manifest entry"
    )
    reviewer_guides = load_reviewer_guides(reviewer_guides_path)
    selected = _select_packages(packages, task_id)
    package_ids = [item["reference_task_id"] for item in packages]
    central_by_id = {
        item["reference_task_id"]: item
        for item in load_reference_review_forms(reviews_path)
    }
    unknown_central = set(central_by_id).difference(package_ids)
    if unknown_central:
        raise ValueError(
            f"Central reviews reference unknown tasks: {sorted(unknown_central)}"
        )

    merged = dict(central_by_id)
    collected: list[str] = []
    for package in selected:
        current_id = package["reference_task_id"]
        if current_id not in reviewer_guides:
            raise ValueError(f"No reviewer guide exists for {current_id}")
        packet_dir = packet_root / current_id
        review = _packet_review(packet_dir)
        if review is None:
            raise FileNotFoundError(packet_dir / "review.json")
        if review["reference_task_id"] != current_id:
            raise ValueError(
                f"Packet directory {current_id} contains review for "
                f"{review['reference_task_id']}"
            )
        manifest_path = packet_dir / "manifest.json"
        if not manifest_path.exists():
            raise FileNotFoundError(manifest_path)
        expected = _prepare_packet_data(
            repo_root=repo_root,
            package=package,
            skill_by_id=skill_by_id,
            source_by_id=source_by_id,
            artifact_by_id=artifact_by_id,
            config_by_id=config_by_id,
        )
        task_detail_path = (
            task_detail_root / current_id / "TASK_DETAIL.md"
        ).resolve()
        if not task_detail_path.is_file():
            raise FileNotFoundError(task_detail_path)
        _add_reviewer_guide(
            packet_data=expected,
            task_detail_path=task_detail_path,
            guide_entry=reviewer_guides[current_id],
        )
        _verify_packet_manifest(
            repo_root,
            packet_dir,
            current_id,
            expected_fingerprint=expected["fingerprint"],
            expected_inputs=expected["input_files"],
        )
        merged[current_id] = review
        collected.append(current_id)

    ordered_reviews = [
        merged.get(current_id, _blank_review(current_id)) for current_id in package_ids
    ]
    document = {"schema_version": "1.0", "reviews": ordered_reviews}
    temporary_reviews = reviews_path.with_name(f".{reviews_path.name}.validation.tmp")
    try:
        _atomic_write_json(temporary_reviews, document)
        load_reference_review_forms(temporary_reviews)
    finally:
        temporary_reviews.unlink(missing_ok=True)
    completed = [review for review in ordered_reviews if review["decision"]]
    state = compute_review_state(skills, packages, completed)
    _atomic_write_json(reviews_path, document)
    temporary_coverage = coverage_path.with_name(f".{coverage_path.name}.tmp")
    try:
        write_coverage_state(temporary_coverage, state)
        temporary_coverage.replace(coverage_path)
    finally:
        temporary_coverage.unlink(missing_ok=True)
    return {
        "collected_reference_task_ids": collected,
        "approved_reference_task_ids": list(state.approved_reference_task_ids),
        "revision_reference_task_ids": list(state.revision_reference_task_ids),
        "rejected_reference_task_ids": list(state.rejected_reference_task_ids),
        "pending_reference_task_ids": list(state.pending_reference_task_ids),
        "approved_skill_count": len(state.approved_skill_ids),
        "total_skill_count": len(skills),
    }


def _verify_packet_manifest(
    repo_root: Path,
    packet_dir: Path,
    expected_task_id: str,
    *,
    expected_fingerprint: str,
    expected_inputs: Sequence[dict[str, str]],
) -> None:
    manifest_path = packet_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("reference_task_id") != expected_task_id:
        raise ValueError(f"Manifest task ID mismatch in {manifest_path}")
    if manifest.get("context_fingerprint") != expected_fingerprint:
        raise ValueError(
            f"Packet {expected_task_id} is stale because its task-specific inputs changed"
        )
    if manifest.get("inputs") != list(expected_inputs):
        raise ValueError(f"Packet input manifest changed unexpectedly: {manifest_path}")
    for entry in manifest.get("inputs", []):
        path = _resolve_repo_path(repo_root, entry["path"])
        if not path.is_file() or _sha256(path) != entry["sha256"]:
            raise ValueError(
                f"Packet {expected_task_id} is stale because input changed: {path}"
            )
    packet_root = packet_dir.resolve()
    for entry in manifest.get("generated_files", []):
        path = (packet_dir / entry["path"]).resolve()
        try:
            path.relative_to(packet_root)
        except ValueError as exc:
            raise ValueError(f"Unsafe generated packet path: {entry['path']}") from exc
        if not path.is_file() or _sha256(path) != entry["sha256"]:
            raise ValueError(
                f"Generated packet file changed unexpectedly: {path}. "
                "Only review.json is editable."
            )
