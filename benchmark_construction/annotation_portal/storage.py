"""Atomic-ish private S3 publication for completed annotation bundles."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


_CONTENT_TYPES = {
    ".ass": "text/plain",
    ".json": "application/json",
    ".jsonl": "application/x-ndjson",
    ".log": "text/plain",
    ".mp4": "video/mp4",
    ".png": "image/png",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
}


@dataclass(frozen=True)
class PublishedBundle:
    bucket: str
    prefix: str
    complete_key: str
    files: tuple[dict[str, Any], ...]


@dataclass(frozen=True)
class PrivateObjectStream:
    body: Any
    content_length: int
    content_type: str
    content_range: str | None
    etag: str | None

    @property
    def status_code(self) -> int:
        return 206 if self.content_range else 200


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


class S3BundlePublisher:
    """Upload files first and write COMPLETE.json only after verification."""

    def __init__(self, client: Any, *, bucket: str, root_prefix: str):
        self.client = client
        self.bucket = bucket
        self.root_prefix = root_prefix.strip("/")

    def publish(
        self,
        bundle_dir: Path,
        *,
        username: str,
        task_id: str,
        run_id: str,
    ) -> PublishedBundle:
        bundle_dir = bundle_dir.resolve()
        files = sorted(path for path in bundle_dir.rglob("*") if path.is_file())
        if not files:
            raise ValueError(f"Annotation bundle is empty: {bundle_dir}")
        prefix = "/".join(
            part
            for part in (self.root_prefix, username, task_id, run_id)
            if part
        )
        manifest_files: list[dict[str, Any]] = []
        for path in files:
            relative = path.relative_to(bundle_dir).as_posix()
            if relative == "COMPLETE.json":
                continue
            sha256 = file_sha256(path)
            key = f"{prefix}/{relative}"
            self.client.upload_file(
                str(path),
                self.bucket,
                key,
                ExtraArgs={
                    "ContentType": _CONTENT_TYPES.get(
                        path.suffix.lower(), "application/octet-stream"
                    ),
                    "Metadata": {"sha256": sha256},
                    "ServerSideEncryption": "AES256",
                },
            )
            head = self.client.head_object(Bucket=self.bucket, Key=key)
            remote_sha256 = head.get("Metadata", {}).get("sha256")
            if remote_sha256 != sha256:
                raise RuntimeError(f"S3 SHA256 verification failed for {relative}")
            manifest_files.append(
                {"path": relative, "size": path.stat().st_size, "sha256": sha256}
            )

        complete_key = f"{prefix}/COMPLETE.json"
        complete_body = json.dumps(
            {
                "schema_version": "1.0",
                "username": username,
                "task_id": task_id,
                "run_id": run_id,
                "files": manifest_files,
            },
            sort_keys=True,
            indent=2,
        ).encode("utf-8")
        self.client.put_object(
            Bucket=self.bucket,
            Key=complete_key,
            Body=complete_body,
            ContentType="application/json",
            ServerSideEncryption="AES256",
        )
        return PublishedBundle(
            bucket=self.bucket,
            prefix=prefix,
            complete_key=complete_key,
            files=tuple(manifest_files),
        )

    def open_recording(
        self, output_prefix: str, *, byte_range: str | None = None
    ) -> PrivateObjectStream:
        bucket, prefix = self._parse_output_prefix(output_prefix)
        parameters = {"Bucket": bucket, "Key": f"{prefix}/recording.mp4"}
        if byte_range:
            if not re.fullmatch(r"bytes=(?:\d+-\d*|\d*-\d+)", byte_range):
                raise ValueError("Invalid video byte range")
            parameters["Range"] = byte_range
        response = self.client.get_object(**parameters)
        return PrivateObjectStream(
            body=response["Body"],
            content_length=int(response["ContentLength"]),
            content_type="video/mp4",
            content_range=response.get("ContentRange"),
            etag=response.get("ETag"),
        )

    def mark_discarded(self, output_prefix: str, *, discarded: bool) -> None:
        bucket, prefix = self._parse_output_prefix(output_prefix)
        status = "discarded" if discarded else "active"
        for row in self._list_objects(bucket, prefix):
            self.client.put_object_tagging(
                Bucket=bucket,
                Key=row["Key"],
                Tagging={"TagSet": [{"Key": "AnnotationStatus", "Value": status}]},
            )

    def permanently_delete(self, output_prefix: str) -> None:
        bucket, prefix = self._parse_output_prefix(output_prefix)
        key_marker = None
        version_marker = None
        while True:
            kwargs: dict[str, Any] = {"Bucket": bucket, "Prefix": f"{prefix}/"}
            if key_marker:
                kwargs["KeyMarker"] = key_marker
            if version_marker:
                kwargs["VersionIdMarker"] = version_marker
            response = self.client.list_object_versions(**kwargs)
            objects = [
                {"Key": row["Key"], "VersionId": row["VersionId"]}
                for group in ("Versions", "DeleteMarkers")
                for row in response.get(group, [])
            ]
            for start in range(0, len(objects), 1000):
                self.client.delete_objects(
                    Bucket=bucket,
                    Delete={"Objects": objects[start : start + 1000], "Quiet": True},
                )
            if not response.get("IsTruncated"):
                break
            key_marker = response.get("NextKeyMarker")
            version_marker = response.get("NextVersionIdMarker")

    def _list_objects(self, bucket: str, prefix: str) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        continuation = None
        while True:
            kwargs: dict[str, Any] = {"Bucket": bucket, "Prefix": f"{prefix}/"}
            if continuation:
                kwargs["ContinuationToken"] = continuation
            response = self.client.list_objects_v2(**kwargs)
            rows.extend(response.get("Contents", []))
            if not response.get("IsTruncated"):
                return rows
            continuation = response["NextContinuationToken"]

    def _parse_output_prefix(self, output_prefix: str) -> tuple[str, str]:
        parsed = urlparse(output_prefix)
        if parsed.scheme != "s3" or parsed.netloc != self.bucket:
            raise ValueError("Workspace output is not in the configured annotation bucket")
        prefix = parsed.path.strip("/")
        root = f"{self.root_prefix}/" if self.root_prefix else ""
        if not prefix.startswith(root) or not prefix:
            raise ValueError("Workspace output is outside the annotation prefix")
        return parsed.netloc, prefix
