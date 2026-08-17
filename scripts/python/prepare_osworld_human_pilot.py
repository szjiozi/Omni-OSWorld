#!/usr/bin/env python3
"""Materialize the three pinned OSWorld-Human Pilot tasks."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from benchmark_construction.osworld_human import prepare_pilot_suite


REPO_ROOT = Path(__file__).resolve().parents[2]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-manifest",
        type=Path,
        default=REPO_ROOT
        / "evaluation_examples/expert_skill_learning/pilot/source_tasks.json",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=REPO_ROOT
        / "results/expert_skill_learning/osworld_human_pilot",
    )
    parser.add_argument(
        "--local-osworld-task-root",
        type=Path,
        default=REPO_ROOT / "evaluation_examples/examples",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    manifest = prepare_pilot_suite(
        args.source_manifest,
        args.output_root,
        local_osworld_task_root=args.local_osworld_task_root,
    )
    print(manifest["suite_path"])


if __name__ == "__main__":
    main()
