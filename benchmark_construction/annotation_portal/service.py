"""Application service coordinating tasks, workspaces, recording, and upload."""

from __future__ import annotations

import logging
import threading
from datetime import UTC, datetime, timedelta
import uuid
from concurrent.futures import Executor, ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol
from collections.abc import Callable

from .catalog import AnnotationTask, TaskCatalog
from .models import (
    ACTIVE_WORKSPACE_STATUSES,
    UserIdentity,
    UserRole,
    WorkspaceSession,
    WorkspaceStatus,
    utc_now_iso,
)
from .storage import PrivateObjectStream, S3BundlePublisher
from .store import PortalStore


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class PreparedWorkspace:
    instance_id: str
    private_ip: str
    output_dir: Path


class WorkspaceController(Protocol):
    def prepare(
        self, workspace: WorkspaceSession, *, task_config_path: Path
    ) -> PreparedWorkspace: ...

    def start_recording(self, workspace: WorkspaceSession) -> None: ...

    def stop_and_finalize(
        self,
        workspace: WorkspaceSession,
        *,
        progress: Callable[[str, str], None] | None = None,
    ) -> Path: ...

    def terminate(self, workspace: WorkspaceSession) -> None: ...


class InlineExecutor:
    """Deterministic executor for tests."""

    def submit(self, fn, /, *args, **kwargs):
        fn(*args, **kwargs)
        return None


class FakeWorkspaceController:
    """Local smoke-test controller with no cloud side effects."""

    def __init__(self, output_root: Path):
        self.output_root = output_root
        self.calls: list[tuple[str, str]] = []

    def prepare(
        self, workspace: WorkspaceSession, *, task_config_path: Path
    ) -> PreparedWorkspace:
        if not task_config_path.is_file():
            raise FileNotFoundError(task_config_path)
        output_dir = self.output_root / workspace.session_id
        output_dir.mkdir(parents=True, exist_ok=True)
        self.calls.append(("prepare", workspace.session_id))
        return PreparedWorkspace(
            instance_id=f"local-{workspace.session_id}",
            private_ip="127.0.0.1",
            output_dir=output_dir,
        )

    def start_recording(self, workspace: WorkspaceSession) -> None:
        self.calls.append(("start", workspace.session_id))

    def stop_and_finalize(
        self,
        workspace: WorkspaceSession,
        *,
        progress: Callable[[str, str], None] | None = None,
    ) -> Path:
        self.calls.append(("stop", workspace.session_id))
        if progress:
            progress("rendering_video", "Generating the annotated reference video.")
        output_dir = self.output_root / workspace.session_id
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "recording.mp4").write_bytes(b"local-smoke-video")
        return output_dir

    def terminate(self, workspace: WorkspaceSession) -> None:
        self.calls.append(("terminate", workspace.session_id))


class AnnotationPortalService:
    def __init__(
        self,
        *,
        store: PortalStore,
        catalog: TaskCatalog,
        controller: WorkspaceController,
        task_config_dir: Path,
        region: str,
        max_active: int = 4,
        publisher: S3BundlePublisher | None = None,
        executor: Executor | InlineExecutor | None = None,
    ) -> None:
        self.store = store
        self.catalog = catalog
        self.controller = controller
        self.task_config_dir = task_config_dir
        self.region = region
        self.max_active = max_active
        self.publisher = publisher
        self.executor = executor or ThreadPoolExecutor(
            max_workers=max_active, thread_name_prefix="annotation-portal"
        )

    def tasks_for(self, identity: UserIdentity) -> list[dict[str, Any]]:
        allowed = self._allowed_task_ids(identity)
        return [
            task.to_public_dict()
            for task in self.catalog.all()
            if allowed is None or task.task_id in allowed
        ]

    def task_for(self, identity: UserIdentity, task_id: str) -> AnnotationTask:
        task = self.catalog.get(task_id)
        allowed = self._allowed_task_ids(identity)
        if allowed is not None and task_id not in allowed:
            raise PermissionError(f"{task_id} is not assigned to {identity.username}")
        return task

    def task_file(self, identity: UserIdentity, task_id: str, relative: str) -> Path:
        task = self.task_for(identity, task_id)
        root = task.packet_dir.resolve()
        candidate = (root / relative).resolve()
        if not candidate.is_relative_to(root) or not candidate.is_file():
            raise FileNotFoundError(relative)
        return candidate

    def launch(self, identity: UserIdentity, task_id: str) -> WorkspaceSession:
        task = self.task_for(identity, task_id)
        task_config_path = (
            task.task_config_path
            if task.task_config_path.is_file()
            else self.task_config_dir / f"{task_id}.json"
        )
        workspace = WorkspaceSession(
            session_id=uuid.uuid4().hex,
            task_id=task_id,
            username=identity.username,
            region=self.region,
            task_config_path=str(task_config_path),
            catalog_version=task.catalog_version,
            progress_stage="provisioning",
            progress_message="Provisioning a clean OSWorld desktop.",
        )
        self.store.create_workspace(workspace, max_active=self.max_active)
        self.executor.submit(self._prepare, workspace.session_id)
        return self.store.get_workspace(workspace.session_id) or workspace

    def _prepare(self, session_id: str) -> None:
        workspace = self._require_workspace(session_id)
        try:
            prepared = self.controller.prepare(
                workspace,
                task_config_path=(
                    Path(workspace.task_config_path)
                    if workspace.task_config_path
                    else self.task_config_dir / f"{workspace.task_id}.json"
                ),
            )
            self.store.update_workspace(
                session_id,
                expected={WorkspaceStatus.PROVISIONING},
                status=WorkspaceStatus.READY,
                instance_id=prepared.instance_id,
                private_ip=prepared.private_ip,
                output_prefix=str(prepared.output_dir),
                ready_at=utc_now_iso(),
                progress_stage="ready",
                progress_message="The private desktop is ready.",
            )
        except Exception as exc:
            logger.exception("Workspace preparation failed for %s", session_id)
            try:
                self.controller.terminate(workspace)
            except Exception:
                logger.exception("Workspace cleanup failed for %s", session_id)
            self.store.update_workspace(
                session_id,
                expected={WorkspaceStatus.PROVISIONING},
                status=WorkspaceStatus.FAILED,
                error=f"{type(exc).__name__}: {exc}",
            )

    def start_recording(
        self, identity: UserIdentity, session_id: str
    ) -> WorkspaceSession:
        workspace = self._owned_workspace(identity, session_id)
        if workspace.status == WorkspaceStatus.RECORDING:
            return workspace
        self.controller.start_recording(workspace)
        return self.store.update_workspace(
            session_id,
            expected={WorkspaceStatus.READY},
            status=WorkspaceStatus.RECORDING,
            recording_started_at=utc_now_iso(),
            progress_stage="recording",
            progress_message="Reference video recording is active.",
        )

    def stop_recording(
        self, identity: UserIdentity, session_id: str
    ) -> WorkspaceSession:
        workspace = self._owned_workspace(identity, session_id)
        if workspace.status in {
            WorkspaceStatus.FINALIZING,
            WorkspaceStatus.UPLOADING,
            WorkspaceStatus.SUBMITTED,
        }:
            return workspace
        workspace = self.store.update_workspace(
            session_id,
            expected={WorkspaceStatus.RECORDING},
            status=WorkspaceStatus.FINALIZING,
            progress_stage="stopping_capture",
            progress_message="Stopping the screen and input-event capture.",
        )
        self.executor.submit(self._finalize, workspace.session_id)
        return self._require_workspace(session_id)

    def _finalize(self, session_id: str) -> None:
        workspace = self._require_workspace(session_id)
        terminated = False
        try:
            def progress(stage: str, message: str) -> None:
                self.store.update_workspace(
                    session_id,
                    expected={WorkspaceStatus.FINALIZING},
                    status=WorkspaceStatus.FINALIZING,
                    progress_stage=stage,
                    progress_message=message,
                )

            bundle_dir = self.controller.stop_and_finalize(
                workspace,
                progress=progress,
            )
            workspace = self.store.update_workspace(
                session_id,
                expected={WorkspaceStatus.FINALIZING},
                status=WorkspaceStatus.UPLOADING,
                output_prefix=str(bundle_dir),
                progress_stage="uploading_bundle",
                progress_message="Uploading and verifying the private result bundle.",
            )
            remote_prefix = str(bundle_dir)
            if self.publisher is not None:
                published = self.publisher.publish(
                    bundle_dir,
                    username=workspace.username,
                    task_id=workspace.task_id,
                    run_id=workspace.session_id,
                )
                remote_prefix = f"s3://{published.bucket}/{published.prefix}"
            workspace = self.store.update_workspace(
                session_id,
                expected={WorkspaceStatus.UPLOADING},
                status=WorkspaceStatus.UPLOADING,
                output_prefix=remote_prefix,
                progress_stage="terminating_worker",
                progress_message="Upload verified. Terminating the annotation worker.",
            )
            self.controller.terminate(workspace)
            terminated = True
            self.store.update_workspace(
                session_id,
                expected={WorkspaceStatus.UPLOADING},
                status=WorkspaceStatus.SUBMITTED,
                output_prefix=remote_prefix,
                submitted_at=utc_now_iso(),
                progress_stage="submitted",
                progress_message="Submission complete and worker terminated.",
            )
        except Exception as exc:
            logger.exception("Workspace finalization failed for %s", session_id)
            current = self._require_workspace(session_id)
            if current.status in {
                WorkspaceStatus.FINALIZING,
                WorkspaceStatus.UPLOADING,
            }:
                self.store.update_workspace(
                    session_id,
                    expected={current.status},
                    status=WorkspaceStatus.FAILED,
                    error=f"{type(exc).__name__}: {exc}",
                )
        finally:
            if not terminated:
                try:
                    self.controller.terminate(workspace)
                except Exception:
                    logger.exception("Workspace termination failed for %s", session_id)

    def current_workspace(self, identity: UserIdentity) -> WorkspaceSession | None:
        return self.store.active_workspace_for_user(identity.username)

    def terminate_ready_workspace(
        self, identity: UserIdentity, session_id: str
    ) -> WorkspaceSession:
        workspace = self._owned_workspace(identity, session_id)
        if workspace.status == WorkspaceStatus.TERMINATED:
            return workspace
        if workspace.status != WorkspaceStatus.READY:
            raise RuntimeError(
                "Only a ready workspace can be closed without submitting"
            )
        self.controller.terminate(workspace)
        return self.store.update_workspace(
            session_id,
            expected={WorkspaceStatus.READY},
            status=WorkspaceStatus.TERMINATED,
            progress_stage="terminated",
            progress_message="Workspace closed without a recording submission.",
        )

    def workspace(self, identity: UserIdentity, session_id: str) -> WorkspaceSession:
        return self._owned_workspace(identity, session_id)

    def submissions_for(self, identity: UserIdentity) -> list[dict[str, Any]]:
        username = None if identity.role == UserRole.ADMIN else identity.username
        return [
            workspace.to_dict()
            for workspace in self.store.workspaces_for_user(username)
            if workspace.status
            in {
                WorkspaceStatus.SUBMITTED,
                WorkspaceStatus.DISCARDED,
                WorkspaceStatus.DELETED,
            }
        ]

    def recording_stream(
        self,
        identity: UserIdentity,
        session_id: str,
        *,
        byte_range: str | None = None,
    ) -> PrivateObjectStream:
        workspace = self._owned_workspace(identity, session_id)
        if workspace.status != WorkspaceStatus.SUBMITTED:
            raise ValueError("Only active submissions can be previewed")
        if self.publisher is None or not workspace.output_prefix:
            raise RuntimeError("Private recording storage is not configured")
        return self.publisher.open_recording(
            workspace.output_prefix,
            byte_range=byte_range,
        )

    def discard_submission(
        self, identity: UserIdentity, session_id: str
    ) -> WorkspaceSession:
        workspace = self._owned_workspace(identity, session_id)
        if workspace.status == WorkspaceStatus.DISCARDED:
            return workspace
        if self.publisher is None or not workspace.output_prefix:
            raise RuntimeError("Private recording storage is not configured")
        self.publisher.mark_discarded(workspace.output_prefix, discarded=True)
        return self.store.update_workspace(
            session_id,
            expected={WorkspaceStatus.SUBMITTED},
            status=WorkspaceStatus.DISCARDED,
            discarded_at=utc_now_iso(),
            progress_stage="discarded",
            progress_message="Discarded; recoverable for seven days.",
        )

    def restore_submission(
        self, identity: UserIdentity, session_id: str
    ) -> WorkspaceSession:
        workspace = self._owned_workspace(identity, session_id)
        if workspace.status == WorkspaceStatus.SUBMITTED:
            return workspace
        if self.publisher is None or not workspace.output_prefix:
            raise RuntimeError("Private recording storage is not configured")
        self.publisher.mark_discarded(workspace.output_prefix, discarded=False)
        return self.store.update_workspace(
            session_id,
            expected={WorkspaceStatus.DISCARDED},
            status=WorkspaceStatus.SUBMITTED,
            discarded_at=None,
            progress_stage="submitted",
            progress_message="Submission restored.",
        )

    def purge_discarded(self, *, now: datetime | None = None, days: int = 7) -> list[str]:
        if self.publisher is None:
            return []
        cutoff = (now or datetime.now(UTC)) - timedelta(days=days)
        purged: list[str] = []
        for workspace in self.store.workspaces_for_user(None):
            if workspace.status != WorkspaceStatus.DISCARDED or not workspace.discarded_at:
                continue
            if datetime.fromisoformat(workspace.discarded_at) > cutoff:
                continue
            if workspace.output_prefix:
                self.publisher.permanently_delete(workspace.output_prefix)
            self.store.update_workspace(
                workspace.session_id,
                expected={WorkspaceStatus.DISCARDED},
                status=WorkspaceStatus.DELETED,
                deleted_at=utc_now_iso(),
                progress_stage="deleted",
                progress_message="Discarded result permanently deleted after retention.",
            )
            purged.append(workspace.session_id)
        return purged

    def _allowed_task_ids(self, identity: UserIdentity) -> set[str] | None:
        if identity.role == UserRole.ADMIN:
            return None
        return {
            assignment.task_id
            for assignment in self.store.assignments_for(identity.username)
        }

    def _require_workspace(self, session_id: str) -> WorkspaceSession:
        workspace = self.store.get_workspace(session_id)
        if workspace is None:
            raise KeyError(session_id)
        return workspace

    def _owned_workspace(
        self, identity: UserIdentity, session_id: str
    ) -> WorkspaceSession:
        workspace = self._require_workspace(session_id)
        if identity.role != UserRole.ADMIN and workspace.username != identity.username:
            raise PermissionError("Workspace belongs to another annotator")
        return workspace

    def expire_workspace(self, session_id: str, *, reason: str) -> WorkspaceSession:
        workspace = self._require_workspace(session_id)
        if workspace.status not in ACTIVE_WORKSPACE_STATUSES:
            return workspace
        try:
            self.controller.terminate(workspace)
        finally:
            return self.store.update_workspace(
                session_id,
                expected={workspace.status},
                status=WorkspaceStatus.EXPIRED,
                error=reason,
            )


class WorkspaceJanitor:
    def __init__(
        self,
        service: AnnotationPortalService,
        *,
        ready_idle_minutes: int = 45,
        hard_ttl_minutes: int = 180,
        interval_seconds: int = 60,
    ) -> None:
        self.service = service
        self.ready_idle = timedelta(minutes=ready_idle_minutes)
        self.hard_ttl = timedelta(minutes=hard_ttl_minutes)
        self.interval_seconds = interval_seconds
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._thread = threading.Thread(
            target=self._run, name="annotation-workspace-janitor", daemon=True
        )
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=5)

    def run_once(self, *, now: datetime | None = None) -> list[str]:
        current_time = now or datetime.now(UTC)
        expired: list[str] = []
        for workspace in self.service.store.active_workspaces():
            created = datetime.fromisoformat(workspace.created_at)
            reason = None
            if current_time - created >= self.hard_ttl:
                reason = "Workspace exceeded the 180-minute hard TTL"
            elif workspace.status == WorkspaceStatus.READY and workspace.ready_at:
                ready = datetime.fromisoformat(workspace.ready_at)
                if current_time - ready >= self.ready_idle:
                    reason = "Ready workspace was idle for 45 minutes"
            if reason:
                try:
                    self.service.expire_workspace(workspace.session_id, reason=reason)
                    expired.append(workspace.session_id)
                except Exception:
                    logger.exception("Could not expire workspace %s", workspace.session_id)
        try:
            self.service.purge_discarded(now=current_time)
        except Exception:
            logger.exception("Could not purge expired discarded submissions")
        return expired

    def _run(self) -> None:
        while not self._stop.wait(self.interval_seconds):
            self.run_once()
