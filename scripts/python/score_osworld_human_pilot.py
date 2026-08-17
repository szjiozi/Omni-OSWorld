#!/usr/bin/env python3
"""Score one three-task result condition with OSWorld-Human WES."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from benchmark_construction.osworld_human_scoring import (
    score_pilot,
    write_score_report,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_TASK_ROOT = REPO_ROOT / "results/expert_skill_learning/osworld_human_pilot"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--task-root", type=Path, default=DEFAULT_TASK_ROOT)
    parser.add_argument(
        "--suite",
        type=Path,
        default=DEFAULT_TASK_ROOT / "test_osworld_human_pilot.json",
    )
    parser.add_argument("--max-steps-scoring", type=int, default=50)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = score_pilot(
        task_root=args.task_root,
        suite_path=args.suite,
        run_root=args.run_root,
        max_steps_scoring=args.max_steps_scoring,
    )
    write_score_report(args.output, report)
    print(args.output)


if __name__ == "__main__":
    main()
