"""Dependency-free state contracts for the annotation portal."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(UTC).isoformat()


class UserRole(StrEnum):
    ANNOTATOR = "annotator"
    ADMIN = "admin"


class WorkspaceStatus(StrEnum):
    ASSIGNED = "assigned"
    PROVISIONING = "provisioning"
    READY = "ready"
    RECORDING = "recording"
    FINALIZING = "finalizing"
    UPLOADING = "uploading"
    SUBMITTED = "submitted"
    DISCARDED = "discarded"
    DELETED = "deleted"
    FAILED = "failed"
    EXPIRED = "expired"
    TERMINATED = "terminated"


ACTIVE_WORKSPACE_STATUSES = frozenset(
    {
        WorkspaceStatus.PROVISIONING,
        WorkspaceStatus.READY,
        WorkspaceStatus.RECORDING,
        WorkspaceStatus.FINALIZING,
        WorkspaceStatus.UPLOADING,
    }
)
TERMINAL_WORKSPACE_STATUSES = frozenset(
    {
        WorkspaceStatus.SUBMITTED,
        WorkspaceStatus.DISCARDED,
        WorkspaceStatus.DELETED,
        WorkspaceStatus.FAILED,
        WorkspaceStatus.EXPIRED,
        WorkspaceStatus.TERMINATED,
    }
)


@dataclass(frozen=True)
class UserIdentity:
    username: str
    role: UserRole = UserRole.ANNOTATOR


@dataclass(frozen=True)
class TaskAssignment:
    task_id: str
    username: str
    assigned_at: str = field(default_factory=utc_now_iso)


@dataclass(frozen=True)
class TaskReviewRecord:
    """Durable online review bound to one immutable task catalog version."""

    catalog_version: str
    task_id: str
    username: str
    review: dict[str, Any]
    updated_at: str = field(default_factory=utc_now_iso)


@dataclass(frozen=True)
class PortalSession:
    """Server-side login session; only its token hash is persisted."""

    token_hash: str
    username: str
    role: UserRole
    expires_at_epoch: int
    created_at: str = field(default_factory=utc_now_iso)


@dataclass(frozen=True)
class WorkspaceSession:
    session_id: str
    task_id: str
    username: str
    region: str
    status: WorkspaceStatus = WorkspaceStatus.PROVISIONING
    instance_id: str | None = None
    private_ip: str | None = None
    output_prefix: str | None = None
    task_config_path: str | None = None
    catalog_version: str | None = None
    progress_stage: str | None = None
    progress_message: str | None = None
    error: str | None = None
    created_at: str = field(default_factory=utc_now_iso)
    updated_at: str = field(default_factory=utc_now_iso)
    ready_at: str | None = None
    recording_started_at: str | None = None
    submitted_at: str | None = None
    discarded_at: str | None = None
    deleted_at: str | None = None

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["status"] = self.status.value
        return result

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "WorkspaceSession":
        fields = dict(value)
        fields["status"] = WorkspaceStatus(fields["status"])
        return cls(**fields)
