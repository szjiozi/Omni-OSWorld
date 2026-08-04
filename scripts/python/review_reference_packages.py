#!/usr/bin/env python3
"""Validate human reviews and compute global approved skill coverage."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from benchmark_construction.reference_generation import load_skill_pool
from benchmark_construction.reference_review import (
    compute_review_state,
    load_reference_packages,
    load_reference_reviews,
    write_coverage_state,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compute approved coverage from append-only package reviews."
    )
    parser.add_argument("--skill-pool", type=Path, required=True)
    parser.add_argument("--packages", type=Path, action="append", required=True)
    parser.add_argument("--reviews", type=Path, required=True)
    parser.add_argument("--app", default="libreoffice_calc")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("results/expert_skill_learning/coverage_state.json"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    skills = load_skill_pool(args.skill_pool, expected_app=args.app)
    packages = load_reference_packages(args.packages)
    reviews = load_reference_reviews(args.reviews)
    state = compute_review_state(skills, packages, reviews)
    write_coverage_state(args.output, state)
    print(f"Approved skills: {len(state.approved_skill_ids)}/{len(skills)}")
    print(f"Unresolved skills: {len(state.unresolved_skill_ids)}")
    print(f"Coverage state: {args.output}")
    return 0 if not state.unresolved_skill_ids else 2


if __name__ == "__main__":
    raise SystemExit(main())
