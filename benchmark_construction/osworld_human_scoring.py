"""Subset-safe OSWorld-Human WES scoring for the expert-skill Pilot."""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class TaskScore:
    task_id: str
    app: str
    result: float
    agent_steps: int
    human_single_steps: int
    human_grouped_steps: int
    single_wes_plus: float
    single_wes_minus: float
    single_wes: float
    grouped_wes_plus: float
    grouped_wes_minus: float
    grouped_wes: float


def compute_wes(
    *,
    result: float,
    human_steps: int,
    agent_steps: int,
    max_steps: int,
) -> tuple[float, float, float]:
    """Match the public OSWorld-Human task-level WES formula."""

    if not 0 <= result <= 1:
        raise ValueError("OSWorld result must be between 0 and 1")
    if min(human_steps, agent_steps, max_steps) < 1:
        raise ValueError("Human, agent, and maximum step counts must be positive")
    if agent_steps > max_steps:
        max_steps = agent_steps
    wes_plus = result * human_steps / agent_steps
    wes_minus = -((1 - result) * agent_steps / max_steps)
    return wes_plus, wes_minus, wes_plus + wes_minus


def _count_trajectory_steps(path: Path) -> int:
    count = 0
    with path.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, start=1):
            if not line.strip():
                continue
            try:
                json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON at {path}:{line_number}") from exc
            count += 1
    if count == 0:
        raise ValueError(f"Trajectory has no steps: {path}")
    return count


def _find_task_result(run_root: Path, app: str, task_id: str) -> Path:
    direct = run_root / app / task_id
    if (direct / "traj.jsonl").exists() and (direct / "result.txt").exists():
        return direct
    matches = sorted(
        path
        for path in run_root.rglob(task_id)
        if path.is_dir()
        and (path / "traj.jsonl").exists()
        and (path / "result.txt").exists()
    )
    if not matches:
        raise FileNotFoundError(f"No completed result found for {app}/{task_id}")
    if len(matches) > 1:
        raise ValueError(f"Multiple completed results found for {app}/{task_id}: {matches}")
    return matches[0]


def score_pilot(
    *,
    task_root: Path,
    suite_path: Path,
    run_root: Path,
    max_steps_scoring: int,
) -> dict:
    if max_steps_scoring < 1:
        raise ValueError("max_steps_scoring must be positive")
    suite = json.loads(suite_path.read_text(encoding="utf-8"))
    task_scores: list[TaskScore] = []
    for app, task_ids in suite.items():
        for task_id in task_ids:
            task_path = task_root / "examples" / app / f"{task_id}.json"
            task = json.loads(task_path.read_text(encoding="utf-8"))
            ground_truth = task.get("human-ground-truth", {})
            single = ground_truth.get("single-action")
            grouped = ground_truth.get("grouped-action")
            if not isinstance(single, list) or not isinstance(grouped, list):
                raise ValueError(f"Missing OSWorld-Human annotations in {task_path}")

            result_dir = _find_task_result(run_root, app, task_id)
            agent_steps = _count_trajectory_steps(result_dir / "traj.jsonl")
            result_text = (result_dir / "result.txt").read_text(encoding="utf-8")
            result = float(result_text.splitlines()[0].strip())
            single_score = compute_wes(
                result=result,
                human_steps=len(single),
                agent_steps=agent_steps,
                max_steps=max_steps_scoring,
            )
            grouped_score = compute_wes(
                result=result,
                human_steps=len(grouped),
                agent_steps=agent_steps,
                max_steps=max_steps_scoring,
            )
            task_scores.append(
                TaskScore(
                    task_id=task_id,
                    app=app,
                    result=result,
                    agent_steps=agent_steps,
                    human_single_steps=len(single),
                    human_grouped_steps=len(grouped),
                    single_wes_plus=single_score[0],
                    single_wes_minus=single_score[1],
                    single_wes=single_score[2],
                    grouped_wes_plus=grouped_score[0],
                    grouped_wes_minus=grouped_score[1],
                    grouped_wes=grouped_score[2],
                )
            )
    if not task_scores:
        raise ValueError("Pilot suite has no tasks")

    count = len(task_scores)
    return {
        "schema_version": "1.0",
        "status": "engineering_pilot",
        "max_steps_scoring": max_steps_scoring,
        "task_count": count,
        "aggregate": {
            "osworld_score": sum(score.result for score in task_scores) / count,
            "single_action_wes_plus": sum(
                score.single_wes_plus for score in task_scores
            )
            / count,
            "grouped_action_wes_plus": sum(
                score.grouped_wes_plus for score in task_scores
            )
            / count,
            "wes_minus": sum(score.single_wes_minus for score in task_scores)
            / count,
        },
        "tasks": [asdict(score) for score in task_scores],
    }


def write_score_report(path: Path, report: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)
