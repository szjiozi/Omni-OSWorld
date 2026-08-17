#!/usr/bin/env python3
"""Prefetch the engineering pilot's OSWorld source and evaluator assets."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from benchmark_construction.pilot_assets import (
    discover_pilot_assets,
    prefetch_pilot_assets,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
PILOT_ROOT = REPO_ROOT / "results/expert_skill_learning/osworld_human_pilot"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--suite",
        type=Path,
        default=PILOT_ROOT / "test_osworld_human_pilot.json",
    )
    parser.add_argument("--task-root", type=Path, default=PILOT_ROOT)
    parser.add_argument("--cache-root", type=Path, default=REPO_ROOT / "cache")
    parser.add_argument(
        "--manifest",
        type=Path,
        default=REPO_ROOT
        / "results/expert_skill_learning/qwen37_engineering_pilot/assets.json",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    assets = discover_pilot_assets(args.suite, args.task_root, args.cache_root)
    manifest = prefetch_pilot_assets(assets, manifest_path=args.manifest)
    print(f"{args.manifest} ({manifest['asset_count']} assets)")


if __name__ == "__main__":
    main()
