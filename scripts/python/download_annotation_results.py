#!/usr/bin/env python3
"""Download complete private annotation runs and verify their manifests."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import uuid
from pathlib import Path, PurePosixPath
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = REPO_ROOT / "results/reference_annotations/portal"
DEFAULT_DATASET = REPO_ROOT / "evaluation_examples/expert_skill_learning/calc_full_v1"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", default="osworld-dev")
    parser.add_argument("--region", default="ap-east-1")
    parser.add_argument("--stack-name", default="osworld-annotation-portal")
    parser.add_argument("--bucket")
    parser.add_argument("--state-table")
    parser.add_argument("--prefix", default="reference-annotations")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--dataset-root", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--dataset-round", default="round_01")
    parser.add_argument("--username")
    parser.add_argument("--task-id")
    parser.add_argument("--run-id")
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument(
        "--final-only",
        dest="final_only",
        action="store_true",
        default=True,
        help="Download only runs selected as final in the Portal (default).",
    )
    selection.add_argument(
        "--all-runs",
        dest="final_only",
        action="store_false",
        help="Download every matching complete, non-discarded run.",
    )
    parser.add_argument("--video-only", action="store_true")
    parser.add_argument("--include-discarded", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument(
        "--overwrite-reviews",
        action="store_true",
        help="Replace different non-empty local review.json files after validation.",
    )
    return parser.parse_args()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def stack_outputs(cloudformation: Any, stack_name: str) -> dict[str, str]:
    stack = cloudformation.describe_stacks(StackName=stack_name)["Stacks"][0]
    return {
        row["OutputKey"]: row["OutputValue"] for row in stack.get("Outputs", [])
    }


def final_selections(
    dynamodb: Any,
    *,
    table_name: str,
    username: str | None = None,
    task_id: str | None = None,
) -> dict[tuple[str, str], str]:
    from boto3.dynamodb.types import TypeDeserializer, TypeSerializer

    serializer = TypeSerializer()
    deserializer = TypeDeserializer()
    values: dict[str, Any] = {":entity": "final_submission"}
    filters = ["entity = :entity"]
    if username:
        values[":username"] = username
        filters.append("username = :username")
    if task_id:
        values[":task_id"] = task_id
        filters.append("task_id = :task_id")
    scan: dict[str, Any] = {
        "TableName": table_name,
        "FilterExpression": " AND ".join(filters),
        "ExpressionAttributeValues": {
            key: serializer.serialize(value) for key, value in values.items()
        },
        "ProjectionExpression": "username, task_id, session_id",
    }
    result: dict[tuple[str, str], str] = {}
    while True:
        response = dynamodb.scan(**scan)
        for raw in response.get("Items", []):
            item = {key: deserializer.deserialize(value) for key, value in raw.items()}
            result[(item["username"], item["task_id"])] = item["session_id"]
        last_key = response.get("LastEvaluatedKey")
        if not last_key:
            return result
        scan["ExclusiveStartKey"] = last_key


def list_complete_keys(s3: Any, *, bucket: str, prefix: str) -> list[str]:
    paginator = s3.get_paginator("list_objects_v2")
    keys: list[str] = []
    for page in paginator.paginate(Bucket=bucket, Prefix=f"{prefix.strip('/')}/"):
        keys.extend(
            row["Key"]
            for row in page.get("Contents", [])
            if row["Key"].endswith("/COMPLETE.json")
        )
    return sorted(keys)


def _safe_relative(value: str) -> PurePosixPath:
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or value in {"", "."}:
        raise ValueError(f"Unsafe manifest path: {value!r}")
    return path


def _discarded(s3: Any, *, bucket: str, complete_key: str) -> bool:
    response = s3.get_object_tagging(Bucket=bucket, Key=complete_key)
    tags = {row["Key"]: row["Value"] for row in response.get("TagSet", [])}
    return tags.get("AnnotationStatus") == "discarded"


def download_run(
    s3: Any,
    *,
    bucket: str,
    complete_key: str,
    output_dir: Path,
    video_only: bool,
    overwrite: bool,
    review: dict[str, Any] | None = None,
) -> Path:
    complete = s3.get_object(Bucket=bucket, Key=complete_key)["Body"].read()
    manifest = json.loads(complete)
    required = {"username", "task_id", "run_id", "files"}
    if not required.issubset(manifest):
        raise ValueError(f"Incomplete marker schema: {complete_key}")
    destination = output_dir / manifest["username"] / manifest["task_id"] / manifest["run_id"]
    if destination.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {destination}")
    temporary = destination.parent / f".{destination.name}.partial-{uuid.uuid4().hex}"
    temporary.mkdir(parents=True, exist_ok=False)
    run_prefix = complete_key.removesuffix("/COMPLETE.json")
    try:
        selected = manifest["files"]
        if video_only:
            selected = [row for row in selected if row["path"] == "recording.mp4"]
            if not selected:
                raise ValueError(f"recording.mp4 is missing from {complete_key}")
        for row in selected:
            relative = _safe_relative(row["path"])
            target = temporary.joinpath(*relative.parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            s3.download_file(bucket, f"{run_prefix}/{relative.as_posix()}", str(target))
            if target.stat().st_size != int(row["size"]):
                raise RuntimeError(f"Size verification failed for {relative}")
            if file_sha256(target) != row["sha256"]:
                raise RuntimeError(f"SHA256 verification failed for {relative}")
        if review is not None:
            from benchmark_construction.reference_review import (
                validate_reference_review_form,
            )

            validate_reference_review_form(review)
            if review["reference_task_id"] != manifest["task_id"]:
                raise ValueError(
                    f"Portal review ID mismatch for {manifest['task_id']}"
                )
            (temporary / "review.json").write_text(
                json.dumps(review, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
        (temporary / "COMPLETE.json").write_bytes(complete)
        if destination.exists():
            shutil.rmtree(destination)
        temporary.replace(destination)
        return destination
    except Exception:
        shutil.rmtree(temporary, ignore_errors=True)
        raise


def main() -> int:
    args = parse_args()
    import boto3

    session = boto3.Session(profile_name=args.profile, region_name=args.region)
    s3 = session.client("s3")
    outputs: dict[str, str] = {}
    if not args.bucket or not args.state_table:
        outputs = stack_outputs(session.client("cloudformation"), args.stack_name)
    bucket = args.bucket or outputs["AnnotationBucketName"]
    state_table = args.state_table or outputs["StateTableName"]
    dynamodb = session.client("dynamodb")
    from scripts.python.sync_annotation_portal_reviews import (
        load_online_reviews,
        sync_reviews,
    )

    online_reviews = load_online_reviews(dynamodb, state_table)
    selections = (
        final_selections(
            dynamodb,
            table_name=state_table,
            username=args.username,
            task_id=args.task_id,
        )
        if args.final_only
        else {}
    )
    downloaded: list[Path] = []
    skipped_discarded = 0
    skipped_not_final = 0
    review_snapshot_count = 0
    downloaded_task_ids: set[str] = set()
    for complete_key in list_complete_keys(
        s3, bucket=bucket, prefix=args.prefix
    ):
        parts = PurePosixPath(complete_key).parts
        if len(parts) < 5:
            continue
        username, task_id, run_id = parts[-4:-1]
        if args.username and username != args.username:
            continue
        if args.task_id and task_id != args.task_id:
            continue
        if args.run_id and run_id != args.run_id:
            continue
        if args.final_only and selections.get((username, task_id)) != run_id:
            skipped_not_final += 1
            continue
        if not args.include_discarded and _discarded(
            s3, bucket=bucket, complete_key=complete_key
        ):
            skipped_discarded += 1
            continue
        review_record = online_reviews.get(task_id)
        downloaded_path = download_run(
            s3,
            bucket=bucket,
            complete_key=complete_key,
            output_dir=args.output_dir.resolve(),
            video_only=args.video_only,
            overwrite=args.overwrite,
            review=(dict(review_record["review"]) if review_record else None),
        )
        downloaded.append(downloaded_path)
        downloaded_task_ids.add(task_id)
        if review_record:
            review_snapshot_count += 1
    selected_reviews = {
        task_id: online_reviews[task_id]
        for task_id in downloaded_task_ids
        if task_id in online_reviews
    }
    synced_reviews = sync_reviews(
        selected_reviews,
        packet_root=(
            args.dataset_root.resolve() / "review_packets" / args.dataset_round
        ),
        overwrite=args.overwrite_reviews,
    )
    print(
        json.dumps(
            {
                "bucket": bucket,
                "downloaded": [str(path) for path in downloaded],
                "downloaded_count": len(downloaded),
                "selection_mode": "final_only" if args.final_only else "all_runs",
                "selected_final_count": len(selections),
                "skipped_not_final": skipped_not_final,
                "skipped_discarded": skipped_discarded,
                "review_snapshot_count": review_snapshot_count,
                "downloaded_without_review_count": (
                    len(downloaded) - review_snapshot_count
                ),
                "synced_local_review_count": len(synced_reviews),
                "synced_local_reviews": [str(path) for path in synced_reviews],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
