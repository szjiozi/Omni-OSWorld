"""Load annotator-facing task and skill context from construction artifacts."""

from __future__ import annotations

import json
import hashlib
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import quote

from markdown_it import MarkdownIt


@dataclass(frozen=True)
class AnnotationTask:
    task_id: str
    app: str
    instruction: str
    operator_guide: dict[str, Any]
    skills: tuple[dict[str, Any], ...]
    review_decision: str
    task_markdown_html: str = ""
    packet_dir: Path = Path(".")
    task_config_path: Path = Path(".")
    catalog_version: str = "unknown"

    def to_public_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "app": self.app,
            "instruction": self.instruction,
            "operator_guide": self.operator_guide,
            "skills": list(self.skills),
            "review_decision": self.review_decision,
            "task_markdown_html": self.task_markdown_html,
            "catalog_version": self.catalog_version,
        }


class TaskCatalog:
    def __init__(self, tasks: list[AnnotationTask]):
        self._tasks = {task.task_id: task for task in tasks}
        if len(self._tasks) != len(tasks):
            raise ValueError("Duplicate task IDs in annotation catalog")

    def get(self, task_id: str) -> AnnotationTask:
        try:
            return self._tasks[task_id]
        except KeyError as exc:
            raise KeyError(f"Unknown reference task: {task_id}") from exc

    def all(self) -> list[AnnotationTask]:
        return sorted(self._tasks.values(), key=lambda task: task.task_id)

    @classmethod
    def load(
        cls,
        *,
        packages_path: Path,
        skills_path: Path,
        reviews_path: Path,
        allow_pending: bool = False,
    ) -> "TaskCatalog":
        package_bytes = packages_path.read_bytes()
        skill_bytes = skills_path.read_bytes()
        review_bytes = reviews_path.read_bytes()
        packages_doc = json.loads(package_bytes)
        skills_doc = json.loads(skill_bytes)
        reviews_doc = json.loads(review_bytes)
        root = packages_path.parent.resolve()
        version_digest = hashlib.sha256(package_bytes + skill_bytes + review_bytes)
        skill_by_id = {item["skill_id"]: item for item in skills_doc["skills"]}
        decision_by_id = {
            item["reference_task_id"]: item["decision"]
            for item in reviews_doc["reviews"]
        }
        tasks: list[AnnotationTask] = []
        for package in packages_doc["reference_packages"]:
            task_id = package["reference_task_id"]
            decision = decision_by_id.get(task_id, "")
            if decision != "approved" and not (allow_pending and decision == ""):
                continue
            required_ids = package["required_skill_ids"]
            missing = [skill_id for skill_id in required_ids if skill_id not in skill_by_id]
            if missing:
                raise ValueError(f"{task_id} references missing skills: {missing}")
            packet_dir = root / "review_packets" / task_id
            markdown_path = packet_dir / "TASK.md"
            task_config_path = root / "task_configs" / f"{task_id}.json"
            if not markdown_path.is_file():
                raise FileNotFoundError(markdown_path)
            if not task_config_path.is_file():
                raise FileNotFoundError(task_config_path)
            markdown_text = markdown_path.read_text(encoding="utf-8")
            version_digest.update(task_id.encode("utf-8"))
            version_digest.update(markdown_text.encode("utf-8"))
            version_digest.update(task_config_path.read_bytes())
            tasks.append(
                AnnotationTask(
                    task_id=task_id,
                    app=package["app"],
                    instruction=package["task_instruction"],
                    operator_guide=package["operator_guide"],
                    skills=tuple(skill_by_id[skill_id] for skill_id in required_ids),
                    review_decision=decision or "pending",
                    task_markdown_html=_render_task_markdown(markdown_text, task_id),
                    packet_dir=packet_dir,
                    task_config_path=task_config_path,
                    catalog_version="pending",
                )
            )
        catalog_version = version_digest.hexdigest()
        return cls(
            [
                AnnotationTask(
                    **{
                        **task.__dict__,
                        "catalog_version": catalog_version,
                    }
                )
                for task in tasks
            ]
        )


class ReloadingTaskCatalog:
    """Atomically reload a catalog when an immutable pilot symlink changes."""

    def __init__(self, pilot_root: Path, *, allow_pending: bool = False):
        self.pilot_root = pilot_root
        self.allow_pending = allow_pending
        self._lock = threading.RLock()
        self._resolved_root: Path | None = None
        self._catalog: TaskCatalog | None = None

    def _current(self) -> TaskCatalog:
        resolved = self.pilot_root.resolve()
        with self._lock:
            if self._catalog is None or resolved != self._resolved_root:
                self._catalog = TaskCatalog.load(
                    packages_path=resolved / "reference_packages.json",
                    skills_path=resolved / "skill_pool.json",
                    reviews_path=resolved / "reference_package_reviews.json",
                    allow_pending=self.allow_pending,
                )
                self._resolved_root = resolved
            return self._catalog

    def get(self, task_id: str) -> AnnotationTask:
        return self._current().get(task_id)

    def all(self) -> list[AnnotationTask]:
        return self._current().all()


def _render_task_markdown(markdown_text: str, task_id: str) -> str:
    markdown_text = markdown_text.replace("<code>", "").replace("</code>", "")
    parser = MarkdownIt("commonmark", {"html": False, "linkify": False}).enable("table")
    tokens = parser.parse(markdown_text)
    prefix = f"/api/tasks/{quote(task_id, safe='')}/files/"
    for token in tokens:
        children = token.children or []
        for child in children:
            attribute = "src" if child.type == "image" else "href"
            if child.type not in {"image", "link_open"}:
                continue
            target = child.attrGet(attribute) or ""
            if not target or target.startswith("#"):
                continue
            if child.type == "link_open" and target == "review.json":
                child.attrSet(
                    attribute,
                    f"/api/tasks/{quote(task_id, safe='')}/review.json?download=true",
                )
                continue
            if ":" in target.split("/", 1)[0] or target.startswith("/"):
                child.attrSet(attribute, "#")
                continue
            parts = Path(target).parts
            if ".." in parts:
                child.attrSet(attribute, "#")
            else:
                child.attrSet(attribute, prefix + target)
    return parser.renderer.render(tokens, parser.options, {})
