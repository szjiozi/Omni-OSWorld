#!/usr/bin/env python3
"""Validate the formal W1 PowerPoint Web task and its evaluator gates."""

from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path
from typing import Any

from desktop_env.evaluators.pptx_animation import (
    compare_pptx_animation_timelines,
    compare_pptx_static_content,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
TASK_ROOT = REPO_ROOT / "evaluation_examples" / "powerpoint_web"
TASK_ID = "5f24d8c2-4779-4f6d-9b8c-6e3bc97ed441"
DEFAULT_TASK = TASK_ROOT / "examples" / "powerpoint_web" / f"{TASK_ID}.json"


def _repo_path(raw_path: str) -> Path:
    path = Path(raw_path)
    return path if path.is_absolute() else REPO_ROOT / path


def validate(task_path: Path = DEFAULT_TASK) -> dict[str, Any]:
    task = json.loads(task_path.read_text(encoding="utf-8"))
    if task["id"] != TASK_ID:
        raise ValueError("unexpected W1 task id")
    if task["snapshot"] != "chrome":
        raise ValueError("W1 PowerPoint Web task must use the chrome snapshot")
    if task["evaluator"]["func"] != [
        "compare_pptx_static_content",
        "compare_pptx_animation_timelines",
    ]:
        raise ValueError("unexpected W1 evaluator composition")
    if task["evaluator"].get("conj") != "and":
        raise ValueError("W1 evaluator gates must use conjunction")

    initial = _repo_path(task["evaluator"]["expected"][0]["path"])
    gold = _repo_path(task["evaluator"]["expected"][1]["path"])
    video = _repo_path(task["video_learning"]["demo_video"]["path"])
    for artifact in (initial, gold, video):
        if not artifact.is_file():
            raise FileNotFoundError(artifact)

    with zipfile.ZipFile(initial) as package:
        if package.testzip() is not None:
            raise ValueError("initial PPTX contains a corrupt member")
    with zipfile.ZipFile(gold) as package:
        if package.testzip() is not None:
            raise ValueError("gold PPTX contains a corrupt member")
    if b"ftyp" not in video.read_bytes()[:32]:
        raise ValueError("demo video is not an MP4 file")

    initial_design = float(
        compare_pptx_static_content(
            str(initial),
            str(initial),
        )
    )
    gold_design = float(
        compare_pptx_static_content(
            str(gold),
            str(initial),
        )
    )
    initial_animation = compare_pptx_animation_timelines(
        str(initial),
        str(gold),
        duration_tolerance_ms=50,
    )
    gold_animation = compare_pptx_animation_timelines(
        str(gold),
        str(gold),
        duration_tolerance_ms=50,
    )
    if initial_design != 1.0 or gold_design != 1.0:
        raise AssertionError("content/layout/color preservation gate failed")
    if initial_animation != 0.0 or gold_animation != 1.0:
        raise AssertionError("animation timeline gate is not discriminative")

    return {
        "status": "passed",
        "task_id": task["id"],
        "initial_design_score": initial_design,
        "gold_design_score": gold_design,
        "initial_animation_score": initial_animation,
        "gold_animation_score": gold_animation,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", type=Path, default=DEFAULT_TASK)
    args = parser.parse_args()
    print(json.dumps(validate(args.task), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
