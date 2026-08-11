"""Append-only human review state and approved-coverage computation."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

from .models import SkillRecord
from .reference_generation import SkillSample
from .reference_packages import RevisionSample
from .schema import load_schema, validate_payload


@dataclass(frozen=True)
class ReviewState:
    approved_reference_task_ids: tuple[str, ...]
    revision_reference_task_ids: tuple[str, ...]
    rejected_reference_task_ids: tuple[str, ...]
    pending_reference_task_ids: tuple[str, ...]
    approved_skill_ids: tuple[str, ...]
    unresolved_skill_ids: tuple[str, ...]
    blocked_groups: tuple[tuple[str, ...], ...]
    revisions: tuple[RevisionSample, ...]


def load_reference_packages(paths: Sequence[Path]) -> list[dict[str, Any]]:
    packages: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for path in paths:
        document = json.loads(path.read_text(encoding="utf-8"))
        entries = document.get("reference_packages")
        if not isinstance(entries, list):
            raise ValueError(f"{path} has no reference_packages list")
        for package in entries:
            task_id = package.get("reference_task_id")
            if not isinstance(task_id, str) or not task_id:
                raise ValueError(f"{path} contains a package without an ID")
            if task_id in seen_ids:
                raise ValueError(f"Duplicate reference task ID: {task_id}")
            seen_ids.add(task_id)
            packages.append(package)
    return packages


def validate_reference_review_form(review: dict[str, Any]) -> None:
    schema = load_schema("reference-package-review.schema.json")
    validate_payload(review, schema)
    task_id = review["reference_task_id"]
    decision = review["decision"]
    if decision == "":
        if (
            review["reason_codes"]
            or review["revision_instructions"]
            or review["reviewer"].strip()
            or review["notes"].strip()
        ):
            raise ValueError(
                f"Pending review {task_id} must keep reviewer fields empty"
            )
        return
    if not review["reviewer"].strip():
        raise ValueError(f"Completed review {task_id} requires a reviewer")
    if decision == "revision_requested" and not review["revision_instructions"]:
        raise ValueError("revision_requested requires revision_instructions")
    if decision != "revision_requested" and review["revision_instructions"]:
        raise ValueError("Only revision_requested may contain revision_instructions")
    if decision == "rejected" and not (
        review["reason_codes"] or review["notes"].strip()
    ):
        raise ValueError("A rejected package must explain the rejection")


def load_reference_review_forms(path: Path) -> list[dict[str, Any]]:
    """Load every review form, including still-empty pending entries."""

    document = json.loads(path.read_text(encoding="utf-8"))
    entries = document.get("reviews")
    if not isinstance(entries, list):
        raise ValueError(f"{path} has no reviews list")
    seen_ids: set[str] = set()
    for review in entries:
        validate_reference_review_form(review)
        task_id = review["reference_task_id"]
        if task_id in seen_ids:
            raise ValueError(f"Multiple reviews for the same package: {task_id}")
        seen_ids.add(task_id)
    return entries


def load_reference_reviews(path: Path) -> list[dict[str, Any]]:
    """Load semantically valid, completed reviews only."""

    return [
        review for review in load_reference_review_forms(path) if review["decision"]
    ]


def write_reference_review_template(
    path: Path,
    packages: Sequence[dict[str, Any]],
) -> int:
    """Add one blank, human-fillable review form for each missing package."""

    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        document = json.loads(path.read_text(encoding="utf-8"))
        entries = document.get("reviews")
        if not isinstance(entries, list):
            raise ValueError(f"{path} has no reviews list")
    else:
        document = {"schema_version": "1.0", "reviews": []}
        entries = document["reviews"]

    existing_ids: set[str] = set()
    schema = load_schema("reference-package-review.schema.json")
    for review in entries:
        validate_payload(review, schema)
        task_id = review["reference_task_id"]
        if task_id in existing_ids:
            raise ValueError(f"Multiple reviews for the same package: {task_id}")
        existing_ids.add(task_id)

    added = 0
    for package in packages:
        task_id = package["reference_task_id"]
        if task_id in existing_ids:
            continue
        entries.append(
            {
                "reference_task_id": task_id,
                "decision": "",
                "reason_codes": [],
                "revision_instructions": [],
                "reviewer": "",
                "notes": "",
            }
        )
        existing_ids.add(task_id)
        added += 1

    path.write_text(
        json.dumps(document, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return added


def compute_review_state(
    skills: Sequence[SkillRecord],
    packages: Sequence[dict[str, Any]],
    reviews: Sequence[dict[str, Any]],
) -> ReviewState:
    skill_by_id = {skill.skill_id: skill for skill in skills}
    package_by_id = {package["reference_task_id"]: package for package in packages}
    review_by_id = {review["reference_task_id"]: review for review in reviews}
    unknown_reviews = set(review_by_id).difference(package_by_id)
    if unknown_reviews:
        raise ValueError(
            f"Reviews reference unknown packages: {sorted(unknown_reviews)}"
        )

    approved_tasks: list[str] = []
    revision_tasks: list[str] = []
    rejected_tasks: list[str] = []
    pending_tasks: list[str] = []
    approved_skills: set[str] = set()
    blocked_groups: list[tuple[str, ...]] = []
    revisions: list[RevisionSample] = []

    for task_id, package in package_by_id.items():
        skill_ids = tuple(package["required_skill_ids"])
        unknown_skills = set(skill_ids).difference(skill_by_id)
        if unknown_skills:
            raise ValueError(
                f"Package {task_id} references unknown skills: {sorted(unknown_skills)}"
            )
        review = review_by_id.get(task_id)
        if review is None:
            pending_tasks.append(task_id)
            continue
        decision = review["decision"]
        if decision == "approved":
            approved_tasks.append(task_id)
            approved_skills.update(skill_ids)
        elif decision == "revision_requested":
            revision_tasks.append(task_id)
            revisions.append(
                RevisionSample(
                    sample=SkillSample(
                        app=package["app"],
                        skills=tuple(skill_by_id[item] for item in skill_ids),
                    ),
                    parent_reference_task_id=task_id,
                    feedback=tuple(review["revision_instructions"]),
                )
            )
        else:
            rejected_tasks.append(task_id)
            blocked_groups.append(skill_ids)

    all_skill_ids = tuple(skill_by_id)
    unresolved = tuple(
        skill_id for skill_id in all_skill_ids if skill_id not in approved_skills
    )
    approved = tuple(
        skill_id for skill_id in all_skill_ids if skill_id in approved_skills
    )
    return ReviewState(
        approved_reference_task_ids=tuple(approved_tasks),
        revision_reference_task_ids=tuple(revision_tasks),
        rejected_reference_task_ids=tuple(rejected_tasks),
        pending_reference_task_ids=tuple(pending_tasks),
        approved_skill_ids=approved,
        unresolved_skill_ids=unresolved,
        blocked_groups=tuple(blocked_groups),
        revisions=tuple(revisions),
    )


def write_coverage_state(path: Path, state: ReviewState) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    document = {
        "schema_version": "1.0",
        "approved_reference_task_ids": list(state.approved_reference_task_ids),
        "revision_reference_task_ids": list(state.revision_reference_task_ids),
        "rejected_reference_task_ids": list(state.rejected_reference_task_ids),
        "pending_reference_task_ids": list(state.pending_reference_task_ids),
        "approved_skill_ids": list(state.approved_skill_ids),
        "unresolved_skill_ids": list(state.unresolved_skill_ids),
        "approved_coverage_complete": not state.unresolved_skill_ids,
        "blocked_skill_combinations": [list(group) for group in state.blocked_groups],
    }
    path.write_text(
        json.dumps(document, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
