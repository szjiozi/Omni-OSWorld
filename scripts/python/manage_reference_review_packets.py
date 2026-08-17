#!/usr/bin/env python3
"""Export and collect self-contained reference-task review packets."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from benchmark_construction.reference_review_packets import (
    collect_packet_reviews,
    export_review_packets,
    export_task_details,
)


PILOT_ROOT = REPO_ROOT / "evaluation_examples/expert_skill_learning/pilot"


def _shared_paths(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--skill-pool", type=Path, default=PILOT_ROOT / "skill_pool.json"
    )
    parser.add_argument(
        "--packages", type=Path, default=PILOT_ROOT / "reference_packages.json"
    )
    parser.add_argument(
        "--reviews", type=Path, default=PILOT_ROOT / "reference_package_reviews.json"
    )
    parser.add_argument(
        "--packet-root", type=Path, default=PILOT_ROOT / "review_packets"
    )
    parser.add_argument(
        "--task-detail-root", type=Path, default=PILOT_ROOT / "task_details"
    )
    parser.add_argument(
        "--reviewer-guides", type=Path, default=PILOT_ROOT / "reviewer_guides.json"
    )
    parser.add_argument("--task-id")
    parser.add_argument(
        "--source-tasks", type=Path, default=PILOT_ROOT / "source_tasks.json"
    )
    parser.add_argument(
        "--artifact-manifest",
        type=Path,
        default=PILOT_ROOT / "artifacts/artifact_manifest.json",
    )
    parser.add_argument(
        "--task-config-manifest",
        type=Path,
        default=PILOT_ROOT / "task_config_manifest.json",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Manage one self-contained review directory per reference task."
    )
    commands = parser.add_subparsers(dest="command", required=True)
    details = commands.add_parser(
        "details", help="Render the full TASK_DETAIL.md inputs for guide generation."
    )
    _shared_paths(details)

    export = commands.add_parser("export", help="Build or refresh review packets.")
    _shared_paths(export)
    export.add_argument(
        "--force",
        action="store_true",
        help="Refresh changed reviewed packets and reset their local reviews.",
    )

    collect = commands.add_parser(
        "collect", help="Validate packet reviews and merge them centrally."
    )
    _shared_paths(collect)
    collect.add_argument(
        "--coverage", type=Path, default=PILOT_ROOT / "coverage_state.json"
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.command == "details":
        task_ids = export_task_details(
            repo_root=REPO_ROOT,
            skill_pool_path=args.skill_pool,
            packages_path=args.packages,
            source_tasks_path=args.source_tasks,
            reviews_path=args.reviews,
            artifact_manifest_path=args.artifact_manifest,
            task_config_manifest_path=args.task_config_manifest,
            output_root=args.task_detail_root,
            task_id=args.task_id,
        )
        print(f"Rendered {len(task_ids)} task detail document(s): {', '.join(task_ids)}")
        print(f"Task detail root: {args.task_detail_root}")
        return 0

    if args.command == "export":
        task_ids = export_review_packets(
            repo_root=REPO_ROOT,
            skill_pool_path=args.skill_pool,
            packages_path=args.packages,
            source_tasks_path=args.source_tasks,
            reviews_path=args.reviews,
            artifact_manifest_path=args.artifact_manifest,
            task_config_manifest_path=args.task_config_manifest,
            task_detail_root=args.task_detail_root,
            reviewer_guides_path=args.reviewer_guides,
            output_root=args.packet_root,
            task_id=args.task_id,
            force=args.force,
        )
        print(f"Exported {len(task_ids)} review packet(s): {', '.join(task_ids)}")
        print(f"Packet index: {args.packet_root / 'index.md'}")
        return 0

    summary = collect_packet_reviews(
        repo_root=REPO_ROOT,
        skill_pool_path=args.skill_pool,
        packages_path=args.packages,
        source_tasks_path=args.source_tasks,
        reviews_path=args.reviews,
        artifact_manifest_path=args.artifact_manifest,
        task_config_manifest_path=args.task_config_manifest,
        task_detail_root=args.task_detail_root,
        reviewer_guides_path=args.reviewer_guides,
        coverage_path=args.coverage,
        packet_root=args.packet_root,
        task_id=args.task_id,
    )
    print(
        "Collected review packets: "
        + ", ".join(summary["collected_reference_task_ids"])
    )
    print(
        f"Approved skills: {summary['approved_skill_count']}/"
        f"{summary['total_skill_count']}"
    )
    print(
        "Pending tasks: " + (", ".join(summary["pending_reference_task_ids"]) or "none")
    )
    print(f"Central reviews: {args.reviews}")
    print(f"Coverage state: {args.coverage}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
