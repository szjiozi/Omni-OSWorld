#!/usr/bin/env python3
"""Sync durable Portal task reviews into local per-task review.json files."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
DEFAULT_DATASET = REPO_ROOT / "evaluation_examples/expert_skill_learning/calc_full_v1"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", default="osworld-dev")
    parser.add_argument("--region", default="ap-east-1")
    parser.add_argument("--stack-name", default="osworld-annotation-portal")
    parser.add_argument("--dataset-root", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--dataset-round", default="round_01")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace a different non-empty local review with the newer Portal review.",
    )
    return parser.parse_args()


def _stack_outputs(client: Any, stack_name: str) -> dict[str, str]:
    stack = client.describe_stacks(StackName=stack_name)["Stacks"][0]
    return {
        row["OutputKey"]: row["OutputValue"] for row in stack.get("Outputs", [])
    }


def load_online_reviews(dynamodb: Any, table_name: str) -> dict[str, dict[str, Any]]:
    from boto3.dynamodb.types import TypeDeserializer, TypeSerializer

    serializer = TypeSerializer()
    deserializer = TypeDeserializer()
    scan: dict[str, Any] = {
        "TableName": table_name,
        "FilterExpression": "entity = :entity",
        "ExpressionAttributeValues": {
            ":entity": serializer.serialize("task_review")
        },
    }
    latest: dict[str, dict[str, Any]] = {}
    while True:
        response = dynamodb.scan(**scan)
        for raw in response.get("Items", []):
            item = {
                key: deserializer.deserialize(value) for key, value in raw.items()
            }
            current = latest.get(item["task_id"])
            if current is None or item["updated_at"] > current["updated_at"]:
                latest[item["task_id"]] = item
        last_key = response.get("LastEvaluatedKey")
        if not last_key:
            break
        scan["ExclusiveStartKey"] = last_key
    return latest


def _is_blank_review(review: dict[str, Any]) -> bool:
    return not any(
        (
            review.get("decision"),
            review.get("reason_codes"),
            review.get("revision_instructions"),
            review.get("reviewer"),
            review.get("notes"),
        )
    )


def sync_reviews(
    reviews: dict[str, dict[str, Any]],
    *,
    packet_root: Path,
    overwrite: bool,
) -> list[Path]:
    from benchmark_construction.reference_review import (
        validate_reference_review_form,
    )

    written: list[Path] = []
    for task_id, record in sorted(reviews.items()):
        destination = packet_root / task_id / "review.json"
        if not destination.is_file():
            continue
        review = dict(record["review"])
        validate_reference_review_form(review)
        if review["reference_task_id"] != task_id:
            raise ValueError(f"Portal review ID mismatch for {task_id}")
        existing = json.loads(destination.read_text(encoding="utf-8"))
        if existing == review:
            continue
        if not _is_blank_review(existing) and not overwrite:
            raise FileExistsError(
                f"Refusing to replace non-empty local review: {destination}; "
                "rerun with --overwrite after checking the Portal version"
            )
        descriptor, temporary_name = tempfile.mkstemp(
            dir=destination.parent,
            prefix=f".{destination.name}.",
            suffix=".tmp",
        )
        temporary = Path(temporary_name)
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
                json.dump(review, stream, indent=2, ensure_ascii=False)
                stream.write("\n")
            temporary.replace(destination)
        finally:
            temporary.unlink(missing_ok=True)
        written.append(destination)
    return written


def main() -> int:
    args = parse_args()
    import boto3

    session = boto3.Session(profile_name=args.profile, region_name=args.region)
    outputs = _stack_outputs(session.client("cloudformation"), args.stack_name)
    reviews = load_online_reviews(
        session.client("dynamodb"), outputs["StateTableName"]
    )
    packet_root = (
        args.dataset_root.resolve() / "review_packets" / args.dataset_round
    )
    written = sync_reviews(reviews, packet_root=packet_root, overwrite=args.overwrite)
    print(
        json.dumps(
            {
                "online_review_count": len(reviews),
                "updated_local_review_count": len(written),
                "packet_root": str(packet_root),
                "updated_files": [str(path) for path in written],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
