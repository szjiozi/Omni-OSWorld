"""Stateful AWS-backed workspace controller for reference annotation."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import shutil
import threading
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping
from collections.abc import Callable

from benchmark_construction.aws_annotation import (
    wait_for_novnc_ready,
    wait_for_osworld_api,
)
from benchmark_construction.key_overlay import (
    burn_key_overlay_in_guest,
    guest_recording_start_monotonic_ns,
    parse_timestamped_pointer_events,
    parse_timestamped_xinput,
    render_key_overlay_ass,
    start_guest_key_capture,
    stop_guest_key_capture,
    write_key_events,
    write_pointer_events,
)
from benchmark_construction.reference_recording import (
    calibrate_recording_timeline,
    collect_guest_reference_recording,
    start_guest_reference_recording,
    stop_guest_reference_recording,
    validate_recording_duration,
)

from .models import WorkspaceSession
from .service import PreparedWorkspace


@dataclass(frozen=True)
class AWSWorkspaceSettings:
    region: str
    subnet_id: str
    security_group_id: str
    ami_id: str
    result_root: Path
    resource_project: str = "OSWorld-Expert-Skill-Learning"
    instance_type: str = "t3.xlarge"
    instance_profile_name: str | None = None
    ttl_minutes: int = 180

    def apply_environment(self) -> None:
        values = {
            "AWS_REGION": self.region,
            "AWS_DEFAULT_REGION": self.region,
            "AWS_CONNECTION_MODE": "private",
            "AWS_SUBNET_ID": self.subnet_id,
            "AWS_SECURITY_GROUP_ID": self.security_group_id,
            "AWS_AMI_ID": self.ami_id,
            "AWS_RESOURCE_PROJECT": self.resource_project,
            "AWS_RESOURCE_ROLE": "AnnotationWorker",
            "AWS_INSTANCE_TYPE": self.instance_type,
            "DEFAULT_TTL_MINUTES": str(self.ttl_minutes),
        }
        if self.instance_profile_name:
            values["AWS_EC2_INSTANCE_PROFILE_NAME"] = self.instance_profile_name
        for name, value in values.items():
            os.environ[name] = value


@dataclass
class _Runtime:
    workspace: WorkspaceSession
    env: Any
    task: dict[str, Any]
    output_dir: Path
    recorder: Any
    artifacts: dict[str, str]
    lock: threading.RLock = field(default_factory=threading.RLock)
    input_started: bool = False
    recording_started: bool = False
    video_start_monotonic_ns: int | None = None


class AWSReferenceWorkspaceController:
    """Keep each live DesktopEnv in the gateway process between UI actions."""

    def __init__(self, settings: AWSWorkspaceSettings) -> None:
        self.settings = settings
        self._lock = threading.RLock()
        self._runtimes: dict[str, _Runtime] = {}

    def prepare(
        self, workspace: WorkspaceSession, *, task_config_path: Path
    ) -> PreparedWorkspace:
        self.settings.apply_environment()
        task = _load_task_config(task_config_path)
        if task["id"] != workspace.task_id:
            raise ValueError("Task config ID does not match workspace task ID")
        output_dir = self.settings.result_root / workspace.task_id / workspace.session_id
        output_dir.mkdir(parents=True, exist_ok=False)
        _copy_preparation_artifacts(task_config_path, task, output_dir)

        from desktop_env.desktop_env import DesktopEnv
        from desktop_env.trajectory import TrajectoryRecorder

        recorder = TrajectoryRecorder(
            output_dir,
            task_id=workspace.task_id,
            actor="human",
            episode_id=workspace.session_id,
        )
        artifacts = {
            "normalized_trajectory": "events.jsonl",
            "manifest": "episode_manifest.json",
            "task_config": "reference_task_config.json",
            "initial_artifact": "initial_artifact.xlsx",
        }
        env = None
        try:
            env = DesktopEnv(
                provider_name="aws",
                region=self.settings.region,
                os_type="Ubuntu",
                action_space="pyautogui",
                require_a11y_tree=False,
                setup_only=True,
            )
            wait_for_osworld_api(env.vm_ip, port=env.server_port)
            wait_for_novnc_ready(env.vm_ip, 5910)
            started_ns = recorder.now_ns()
            observation = env.reset(task_config=task)
            recorder.add_timing("environment_setup", recorder.now_ns() - started_ns)
            initial_ref = _save_observation(
                output_dir, recorder, observation, stem="initial_state", kind="initial"
            )
            if initial_ref:
                artifacts["initial_state"] = initial_ref
            runtime = _Runtime(
                workspace=workspace,
                env=env,
                task=task,
                output_dir=output_dir,
                recorder=recorder,
                artifacts=artifacts,
            )
            with self._lock:
                if workspace.session_id in self._runtimes:
                    raise RuntimeError("Workspace runtime already exists")
                self._runtimes[workspace.session_id] = runtime
            return PreparedWorkspace(
                instance_id=env.path_to_vm,
                private_ip=env.vm_ip,
                output_dir=output_dir,
            )
        except Exception as exc:
            recorder.finalize(
                status="failed",
                result=None,
                artifacts=artifacts,
                error=f"{type(exc).__name__}: {exc}",
            )
            if env is not None:
                env.close()
            raise

    def start_recording(self, workspace: WorkspaceSession) -> None:
        runtime = self._runtime(workspace.session_id)
        with runtime.lock:
            if runtime.recording_started:
                return
            observation = runtime.env._get_obs()
            start_ref = _save_observation(
                runtime.output_dir,
                runtime.recorder,
                observation,
                stem="recording_start",
                kind="recording_start",
            )
            if start_ref:
                runtime.artifacts["recording_start"] = start_ref
            if not start_guest_key_capture(runtime.env):
                raise RuntimeError("Guest input capture did not become ready")
            runtime.input_started = True
            runtime.artifacts.update(
                {
                    "input_events": "input_events.xinput.log",
                    "timestamped_input_events": "input_events.timestamped.jsonl",
                    "input_keymap": "input_keymap.xmodmap",
                }
            )
            started_ns = runtime.recorder.now_ns()
            start_guest_reference_recording(runtime.env)
            runtime.recording_started = True
            runtime.video_start_monotonic_ns = guest_recording_start_monotonic_ns(
                runtime.env
            )
            _write_json(
                runtime.output_dir / "input_timing.json",
                {
                    "schema_version": "1.0",
                    "clock": "guest_monotonic_ns",
                    "video_start_monotonic_ns": runtime.video_start_monotonic_ns,
                    "provisional_video_start_monotonic_ns": (
                        runtime.video_start_monotonic_ns
                    ),
                    "alignment_status": "provisional",
                },
            )
            runtime.artifacts["input_timing"] = "input_timing.json"
            runtime.recorder.record_event(
                "annotation_control",
                started_ns=started_ns,
                finished_ns=runtime.recorder.now_ns(),
                metadata={"state": "recording_started"},
            )

    def stop_and_finalize(
        self,
        workspace: WorkspaceSession,
        *,
        progress: Callable[[str, str], None] | None = None,
    ) -> Path:
        runtime = self._runtime(workspace.session_id)
        with runtime.lock:
            try:
                self._finalize_recording(runtime, progress=progress)
                return runtime.output_dir
            except Exception as exc:
                runtime.recorder.finalize(
                    status="failed",
                    result=None,
                    artifacts=runtime.artifacts,
                    error=f"{type(exc).__name__}: {exc}",
                    metadata={"instance_id": runtime.env.path_to_vm},
                )
                raise

    def _finalize_recording(
        self,
        runtime: _Runtime,
        *,
        progress: Callable[[str, str], None] | None = None,
    ) -> None:
        if not runtime.recording_started or runtime.video_start_monotonic_ns is None:
            raise RuntimeError("Recording was not started")
        notify = progress or (lambda _stage, _message: None)
        notify("stopping_capture", "Stopping the screen and input-event capture.")
        stopped_ns = runtime.recorder.now_ns()
        finalize_started = runtime.recorder.now_ns()
        video_stop_monotonic_ns = stop_guest_reference_recording(runtime.env)
        runtime.recording_started = False
        captured = stop_guest_key_capture(runtime.env, runtime.output_dir)
        runtime.input_started = False
        if not captured:
            raise RuntimeError("Guest input events could not be retrieved")

        notify("collecting_video", "Collecting and validating the raw screen recording.")
        raw_path = runtime.output_dir / "recording_raw.mp4"
        log_path = runtime.output_dir / "recording_capture.ffmpeg.log"
        collect_guest_reference_recording(runtime.env, raw_path, log_path)
        duration = validate_recording_duration(
            raw_path,
            start_monotonic_ns=runtime.video_start_monotonic_ns,
            stop_monotonic_ns=video_stop_monotonic_ns,
        )
        timeline = calibrate_recording_timeline(
            provisional_start_monotonic_ns=runtime.video_start_monotonic_ns,
            stop_monotonic_ns=video_stop_monotonic_ns,
            actual_duration_seconds=duration["actual_seconds"],
        )
        calibrated_start_ns = timeline.calibrated_video_start_monotonic_ns
        _write_json(
            runtime.output_dir / "input_timing.json",
            {
                "schema_version": "1.0",
                "clock": "guest_monotonic_ns",
                "video_start_monotonic_ns": calibrated_start_ns,
                "alignment_status": "calibrated",
                **timeline.to_dict(),
            },
        )
        runtime.artifacts["recording_raw"] = raw_path.name
        if log_path.is_file():
            runtime.artifacts["recording_capture_log"] = log_path.name

        timestamped_text = (
            runtime.output_dir / "input_events.timestamped.jsonl"
        ).read_text(encoding="utf-8")
        keymap_text = (runtime.output_dir / "input_keymap.xmodmap").read_text(
            encoding="utf-8"
        )
        key_events = parse_timestamped_xinput(
            timestamped_text,
            keymap_text,
            video_start_monotonic_ns=calibrated_start_ns,
        )
        pointer_events = parse_timestamped_pointer_events(
            timestamped_text,
            video_start_monotonic_ns=calibrated_start_ns,
        )
        write_key_events(runtime.output_dir / "key_events.jsonl", key_events)
        write_pointer_events(runtime.output_dir / "pointer_events.jsonl", pointer_events)
        runtime.artifacts["key_events"] = "key_events.jsonl"
        runtime.artifacts["pointer_events"] = "pointer_events.jsonl"
        overlay_path = runtime.output_dir / "key_overlay.ass"
        overlay_path.write_text(
            render_key_overlay_ass(key_events, pointer_events=pointer_events),
            encoding="utf-8",
        )
        runtime.artifacts["key_overlay"] = overlay_path.name
        notify("rendering_video", "Rendering visible keyboard and pointer overlays.")
        recording_path = runtime.output_dir / "recording.mp4"
        burn_key_overlay_in_guest(runtime.env, overlay_path, recording_path)
        runtime.artifacts["recording"] = recording_path.name

        notify("saving_artifact", "Saving the final workbook and result artifacts.")
        final_artifact = runtime.output_dir / "final_artifact.xlsx"
        guest_path = runtime.task["reference_annotation"]["guest_artifact_path"]
        _save_guest_workbook(runtime.env, guest_path, final_artifact)
        runtime.artifacts["final_artifact"] = final_artifact.name
        final_ref = _save_observation(
            runtime.output_dir,
            runtime.recorder,
            runtime.env._get_obs(),
            stem="final_state",
            kind="final",
        )
        if final_ref:
            runtime.artifacts["final_state"] = final_ref
        runtime.recorder.add_timing(
            "recording_finalize", runtime.recorder.now_ns() - finalize_started
        )
        runtime.recorder.record_event(
            "annotation_control",
            started_ns=stopped_ns,
            finished_ns=runtime.recorder.now_ns(),
            metadata={"state": "recording_stopped"},
        )
        notify("finalizing_manifest", "Writing and validating the annotation manifest.")
        runtime.recorder.finalize(
            status="completed",
            result=None,
            artifacts=runtime.artifacts,
            metadata={
                "instance_id": runtime.env.path_to_vm,
                "aws_region": self.settings.region,
                "connection_mode": "private_gateway",
                "input_events_captured": True,
                "key_overlay_enabled": True,
                "key_overlay_event_count": len(key_events),
                "pointer_overlay_event_count": len(pointer_events),
                "recording_capture_preset": "ultrafast",
                "recording_duration": duration,
                "recording_timeline": timeline.to_dict(),
                "preferred_reference_video": "recording.mp4",
            },
        )

    def terminate(self, workspace: WorkspaceSession) -> None:
        with self._lock:
            runtime = self._runtimes.pop(workspace.session_id, None)
        if runtime is None:
            if workspace.instance_id:
                import boto3

                boto3.client("ec2", region_name=workspace.region).terminate_instances(
                    InstanceIds=[workspace.instance_id]
                )
            return
        with runtime.lock:
            if runtime.input_started:
                try:
                    stop_guest_key_capture(runtime.env, runtime.output_dir)
                except Exception:
                    pass
            if runtime.recording_started:
                try:
                    stop_guest_reference_recording(runtime.env)
                    collect_guest_reference_recording(
                        runtime.env,
                        runtime.output_dir / "recording_raw.mp4",
                        runtime.output_dir / "recording_capture.ffmpeg.log",
                    )
                except Exception:
                    pass
            runtime.env.close()

    def _runtime(self, session_id: str) -> _Runtime:
        with self._lock:
            runtime = self._runtimes.get(session_id)
        if runtime is None:
            raise KeyError(f"No live runtime for workspace {session_id}")
        return runtime


def _load_task_config(path: Path) -> dict[str, Any]:
    task = copy.deepcopy(json.loads(path.read_text(encoding="utf-8")))
    if "evaluator" in task:
        raise ValueError("Reference annotation configs must not contain an evaluator")
    steps = task.get("config")
    if not isinstance(steps, list) or [step.get("type") for step in steps] != [
        "upload_file",
        "open",
    ]:
        raise ValueError("Task config must contain exactly upload_file then open")
    files = steps[0].get("parameters", {}).get("files", [])
    if len(files) != 1:
        raise ValueError("Task config must upload exactly one file")
    local_path = Path(files[0]["local_path"])
    if not local_path.is_absolute():
        repository_candidate = Path.cwd() / local_path
        snapshot_candidate = path.parent.parent / "artifacts" / task["id"] / local_path.name
        local_path = (
            repository_candidate if repository_candidate.is_file() else snapshot_candidate
        )
    files[0]["local_path"] = str(local_path.resolve())
    if steps[1].get("parameters", {}).get("path") != files[0].get("path"):
        raise ValueError("The open action must target the uploaded artifact")
    if task.get("snapshot") != "libreoffice_calc":
        raise ValueError("Only libreoffice_calc reference annotation is supported")
    expected_hash = task["reference_annotation"]["artifact_sha256"]
    if _sha256(local_path) != expected_hash:
        raise ValueError("Initial artifact SHA256 does not match task config")
    return task


def _copy_preparation_artifacts(
    task_config_path: Path, task: Mapping[str, Any], output_dir: Path
) -> None:
    shutil.copy2(task_config_path, output_dir / "reference_task_config.json")
    artifact = Path(task["config"][0]["parameters"]["files"][0]["local_path"])
    shutil.copy2(artifact, output_dir / "initial_artifact.xlsx")
    _write_json(
        output_dir / "operator_guide.json",
        task["reference_annotation"]["operator_guide"],
    )


def _save_observation(
    output_dir: Path,
    recorder: Any,
    observation: Mapping[str, Any],
    *,
    stem: str,
    kind: str,
) -> str | None:
    screenshot_ref = None
    if observation.get("screenshot"):
        screenshot_ref = f"{stem}.png"
        (output_dir / screenshot_ref).write_bytes(observation["screenshot"])
    now_ns = recorder.now_ns()
    recorder.record_event(
        "observation",
        started_ns=now_ns,
        finished_ns=now_ns,
        observation_ref=screenshot_ref,
        metadata={"kind": kind},
    )
    return screenshot_ref


def _save_guest_workbook(env: Any, guest_path: str, output_path: Path) -> None:
    result = env.controller.execute_python_command(
        "import pyautogui,time; pyautogui.hotkey('ctrl','s'); time.sleep(3)"
    )
    if not result:
        raise RuntimeError("Could not send Ctrl+S to LibreOffice Calc")
    content = env.controller.get_file(guest_path)
    if not content or not content.startswith(b"PK"):
        raise RuntimeError("Could not retrieve a valid final XLSX workbook")
    output_path.write_bytes(content)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
