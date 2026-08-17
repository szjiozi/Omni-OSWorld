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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", default="osworld-dev")
    parser.add_argument("--region", default="ap-east-1")
    parser.add_argument("--stack-name", default="osworld-annotation-portal")
    parser.add_argument("--bucket")
    parser.add_argument("--prefix", default="reference-annotations")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--username")
    parser.add_argument("--task-id")
    parser.add_argument("--run-id")
    parser.add_argument("--video-only", action="store_true")
    parser.add_argument("--include-discarded", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def stack_bucket(cloudformation: Any, stack_name: str) -> str:
    stack = cloudformation.describe_stacks(StackName=stack_name)["Stacks"][0]
    outputs = {
        row["OutputKey"]: row["OutputValue"] for row in stack.get("Outputs", [])
    }
    return outputs["AnnotationBucketName"]


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
    bucket = args.bucket or stack_bucket(
        session.client("cloudformation"), args.stack_name
    )
    downloaded: list[Path] = []
    skipped_discarded = 0
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
        if not args.include_discarded and _discarded(
            s3, bucket=bucket, complete_key=complete_key
        ):
            skipped_discarded += 1
            continue
        downloaded.append(
            download_run(
                s3,
                bucket=bucket,
                complete_key=complete_key,
                output_dir=args.output_dir.resolve(),
                video_only=args.video_only,
                overwrite=args.overwrite,
            )
        )
    print(
        json.dumps(
            {
                "bucket": bucket,
                "downloaded": [str(path) for path in downloaded],
                "downloaded_count": len(downloaded),
                "skipped_discarded": skipped_discarded,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
