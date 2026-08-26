#!/usr/bin/env python3
"""Launch and record one human reference task on an OSWorld AWS desktop."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import shutil
import signal
import sys
import time
from pathlib import Path
from typing import Any
from urllib.parse import urlencode


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from benchmark_construction.aws_annotation import (
    active_project_instance_ids,
    arm_guest_termination_backstop,
    discover_public_ipv4,
    refresh_annotation_ingress,
    resolve_annotation_aws_resources,
    start_ssm_ssh_forward,
    wait_for_novnc_ready,
    wait_for_osworld_api,
    wait_for_ssm_online,
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
from benchmark_construction.reference_annotation import (
    load_artifact_manifest,
    load_review_decisions,
    require_launchable_review,
)
from benchmark_construction.reference_applications import get_reference_application
from benchmark_construction.reference_recording import (
    calibrate_recording_timeline,
    collect_guest_reference_recording,
    start_guest_reference_recording,
    stop_guest_reference_recording,
    validate_recording_duration,
)
from benchmark_construction.reference_review import load_reference_packages
from scripts.python.manual_explore import (
    _episode_output_dir,
    _save_observation,
    _start_screenshot_sampler,
)


PILOT_ROOT = REPO_ROOT / "evaluation_examples/expert_skill_learning/pilot"
DEFAULT_PROJECT_TAG = "OSWorld-Expert-Skill-Learning"
NOVNC_PREVIEW_SETTINGS = (
    ("autoconnect", "true"),
    ("resize", "scale"),
    ("quality", "0"),
    ("compression", "9"),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Start an approved reference task on AWS. Press Enter once to "
            "begin recording and a second time to stop, collect, and terminate."
        )
    )
    parser.add_argument("--reference-task-id", required=True)
    parser.add_argument(
        "--task-config-dir", type=Path, default=PILOT_ROOT / "task_configs"
    )
    parser.add_argument(
        "--packages",
        type=Path,
        action="append",
        default=None,
    )
    parser.add_argument(
        "--reviews",
        type=Path,
        default=PILOT_ROOT / "reference_package_reviews.json",
    )
    parser.add_argument(
        "--artifact-manifest",
        type=Path,
        default=PILOT_ROOT / "artifacts/artifact_manifest.json",
    )
    parser.add_argument("--allow-pending", action="store_true")
    parser.add_argument(
        "--result-dir",
        type=Path,
        default=Path("results/reference_annotations"),
    )
    parser.add_argument(
        "--sample-interval",
        type=float,
        default=0.0,
        help=(
            "Seconds between optional diagnostic screenshots. Reference "
            "annotation disables periodic screenshots by default so they do "
            "not compete with noVNC; pass a positive value to opt in."
        ),
    )
    parser.add_argument("--aws-profile", default="osworld-dev")
    parser.add_argument(
        "--aws-region", default=os.getenv("AWS_ANNOTATION_REGION", "ap-east-1")
    )
    parser.add_argument(
        "--aws-connection-mode",
        choices=("auto", "public", "ssm"),
        default="auto",
        help="Use SSM tunnels automatically in Hong Kong, or force one mode.",
    )
    parser.add_argument(
        "--no-refresh-security-group",
        action="store_true",
        help="Do not replace annotation-port ingress with the current public /32.",
    )
    parser.add_argument(
        "--no-input-events",
        action="store_true",
        help="Record video and screenshots without the guest xinput log.",
    )
    parser.add_argument(
        "--no-key-overlay",
        action="store_true",
        help=(
            "Keep recording.mp4 free of keyboard and pointer overlays "
            "(debug only)."
        ),
    )
    parser.add_argument(
        "--require-a11y-tree",
        action="store_true",
        help="Include accessibility trees in start/final observations.",
    )
    return parser.parse_args()


def _validate_recording_options(args: argparse.Namespace) -> None:
    if args.sample_interval < 0:
        raise SystemExit("--sample-interval must be non-negative")
    if args.no_input_events and not args.no_key_overlay:
        raise SystemExit(
            "--no-input-events requires --no-key-overlay because the overlay "
            "depends on captured key events"
        )


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else REPO_ROOT / path


def _load_task_config(path: Path) -> dict[str, Any]:
    resolved = _resolve(path)
    task = json.loads(resolved.read_text(encoding="utf-8"))
    task = copy.deepcopy(task)
    if "evaluator" in task:
        raise ValueError("Reference annotation configs must not contain an evaluator")
    steps = task.get("config")
    if not isinstance(steps, list) or [step.get("type") for step in steps] != [
        "upload_file",
        "open",
    ]:
        raise ValueError(
            "Reference annotation config must contain exactly upload_file then open"
        )
    files = steps[0].get("parameters", {}).get("files", [])
    if len(files) != 1:
        raise ValueError("Reference annotation config must upload exactly one file")
    local_path = Path(files[0]["local_path"])
    files[0]["local_path"] = str(_resolve(local_path).resolve())
    if steps[1].get("parameters", {}).get("path") != files[0].get("path"):
        raise ValueError("The open action must target the uploaded artifact")
    get_reference_application(task.get("snapshot", ""))
    return task


def _select_by_id(
    items: list[dict[str, Any]], task_id: str, label: str
) -> dict[str, Any]:
    matches = [item for item in items if item.get("reference_task_id") == task_id]
    if len(matches) != 1:
        raise ValueError(f"Expected one {label} for {task_id}, found {len(matches)}")
    return matches[0]


def _write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _print_aws_access(env: Any, novnc_url: str) -> None:
    print("\nOSWorld is ready.")
    print(f"Instance ID: {env.path_to_vm}")
    print(f"noVNC: {novnc_url}")
    print("noVNC password: osworld-public-evaluation")
    print("noVNC preview: low bandwidth; recording remains 1920x1080")


def _novnc_preview_url(host: str, port: int) -> str:
    return f"http://{host}:{port}/vnc.html?{urlencode(NOVNC_PREVIEW_SETTINGS)}"


def _print_operator_guide(task: dict[str, Any], review_status: str) -> None:
    annotation = task["reference_annotation"]
    guide = annotation["operator_guide"]
    print("\n" + "=" * 78)
    print(f"REFERENCE TASK: {task['id']}")
    print(f"REVIEW STATUS: {review_status}")
    print("\nTASK INSTRUCTION")
    print(task["instruction"])
    print("\nVERIFY BEFORE RECORDING")
    for item in annotation["ready_state_checks"]:
        print(f"  - {item}")
    if annotation["setup_notes"]:
        print("\nSETUP NOTES")
        for item in annotation["setup_notes"]:
            print(f"  - {item}")
    print("\nRECOMMENDED DEMONSTRATION")
    for index, item in enumerate(guide["recommended_demonstration"], start=1):
        print(f"  {index}. {item['operation_intent']}")
        print(f"     Efficiency: {item['efficiency_tip']}")
        print(f"     Success: {item['visible_success_signal']}")
    print("\nALLOWED VARIATION")
    print(guide["allowed_variation"])
    print("\nEXPECTED END STATE")
    print(guide["recording_end_state"])
    print("=" * 78)


def _configure_aws(args: argparse.Namespace) -> dict[str, Any]:
    resources = resolve_annotation_aws_resources(os.environ, args.aws_region)
    requested_mode = getattr(args, "aws_connection_mode", "auto")
    connection_mode = (
        "ssm"
        if requested_mode == "auto" and args.aws_region == "ap-east-1"
        else "public" if requested_mode == "auto" else requested_mode
    )
    os.environ["AWS_PROFILE"] = args.aws_profile
    os.environ["AWS_REGION"] = args.aws_region
    os.environ["AWS_DEFAULT_REGION"] = args.aws_region
    os.environ["AWS_CONNECTION_MODE"] = "public"
    os.environ["AWS_RESOURCE_PROJECT"] = DEFAULT_PROJECT_TAG
    os.environ["AWS_SUBNET_ID"] = resources.subnet_id
    os.environ["AWS_SECURITY_GROUP_ID"] = resources.security_group_id
    if resources.ami_id:
        os.environ["AWS_AMI_ID"] = resources.ami_id
    else:
        os.environ.pop("AWS_AMI_ID", None)

    import boto3

    session = boto3.Session(profile_name=args.aws_profile, region_name=args.aws_region)
    session.client("sts").get_caller_identity()
    ec2_client = session.client("ec2")
    if resources.ami_id:
        images = ec2_client.describe_images(ImageIds=[resources.ami_id]).get(
            "Images", []
        )
        if len(images) != 1 or images[0].get("State") != "available":
            state = images[0].get("State") if images else "missing"
            raise RuntimeError(
                f"Annotation AMI {resources.ami_id} is not available: {state}"
            )
    active_instances = active_project_instance_ids(ec2_client, DEFAULT_PROJECT_TAG)
    if active_instances:
        raise RuntimeError(
            "An OSWorld reference annotation instance is already active: "
            + ", ".join(active_instances)
        )
    result: dict[str, Any] = {
        "aws_profile": args.aws_profile,
        "aws_region": args.aws_region,
        "official_ami": resources.ami_id is None,
        "official_ami_source": True,
        "ami_id": resources.ami_id or resources.source_ami_id,
        "ami_source_id": resources.source_ami_id,
        "ami_distribution": resources.ami_distribution,
        "connection_mode": connection_mode,
        "resource_project": DEFAULT_PROJECT_TAG,
        "subnet_id": resources.subnet_id,
        "security_group_id": resources.security_group_id,
    }
    if connection_mode == "public" and not args.no_refresh_security_group:
        public_ip = discover_public_ipv4()
        network_result = refresh_annotation_ingress(
            ec2_client, resources.security_group_id, public_ip
        )
        result["network"] = {
            "security_group_refreshed": True,
            "ports": network_result["ports"],
            "cidr": network_result["cidr"],
        }
    else:
        result["network"] = {
            "refresh_skipped": True,
            "reason": (
                "ssm_tunnel_does_not_require_public_ingress"
                if connection_mode == "ssm"
                else "requested"
            ),
        }
    return result


def _retarget_env_to_local_api(env: Any, local_port: int) -> None:
    from desktop_env.controllers.python import PythonController
    from desktop_env.controllers.setup_only import SetupOnlyController
    from desktop_env.network import add_no_proxy_host

    env.vm_ip = "127.0.0.1"
    env.server_port = local_port
    add_no_proxy_host(env.vm_ip)
    env.controller = PythonController(vm_ip=env.vm_ip, server_port=local_port)
    env.setup_controller = SetupOnlyController(
        vm_ip=env.vm_ip,
        server_port=local_port,
        cache_dir=env.cache_dir_base,
    )


def _save_guest_workbook(env: Any, guest_path: str, output_path: Path) -> None:
    """Backward-compatible Calc wrapper used by tests and older callers."""

    _save_guest_artifact(
        env, guest_path, output_path, app="libreoffice_calc"
    )


def _save_guest_artifact(
    env: Any, guest_path: str, output_path: Path, *, app: str
) -> None:
    profile = get_reference_application(app)
    result = env.controller.execute_python_command(
        "import pyautogui,time; pyautogui.hotkey('ctrl','s'); time.sleep(3)"
    )
    if not result:
        raise RuntimeError(f"Could not send Ctrl+S to {profile.app}")
    content = env.controller.get_file(guest_path)
    if not content:
        raise RuntimeError(f"Could not retrieve final artifact from {guest_path}")
    if not content.startswith(b"PK"):
        raise RuntimeError(
            f"Retrieved final artifact is not a {profile.artifact_type.upper()} ZIP package"
        )
    output_path.write_bytes(content)


def _handle_stop_signal(_signum, _frame) -> None:
    raise KeyboardInterrupt


def main() -> int:
    args = parse_args()
    if not sys.stdin.isatty():
        raise SystemExit(
            "An interactive terminal is required for the two Enter prompts"
        )
    _validate_recording_options(args)

    task_id = args.reference_task_id
    package_paths = args.packages or [PILOT_ROOT / "reference_packages.json"]
    packages = load_reference_packages([_resolve(path) for path in package_paths])
    package = _select_by_id(packages, task_id, "reference package")
    profile = get_reference_application(package.get("app", "libreoffice_calc"))
    decisions = load_review_decisions(_resolve(args.reviews))
    review_status = require_launchable_review(
        task_id, decisions, allow_pending=args.allow_pending
    )
    artifact_by_id = load_artifact_manifest(_resolve(args.artifact_manifest))
    if task_id not in artifact_by_id:
        raise ValueError(f"No artifact manifest entry for {task_id}")
    artifact_entry = artifact_by_id[task_id]
    config_path = _resolve(args.task_config_dir) / f"{task_id}.json"
    task = _load_task_config(config_path)
    if task.get("id") != task_id:
        raise ValueError("Task config ID does not match --reference-task-id")
    if task.get("snapshot") != profile.app:
        raise ValueError("Task config application differs from reference package")
    annotation = task["reference_annotation"]
    if annotation["artifact_sha256"] != artifact_entry["artifact_sha256"]:
        raise ValueError("Task config and artifact manifest SHA256 values differ")

    original_artifact = Path(task["config"][0]["parameters"]["files"][0]["local_path"])
    expected_artifact = _resolve(Path(artifact_entry["artifact_path"])).resolve()
    if original_artifact != expected_artifact:
        raise ValueError("Task config artifact path differs from the artifact manifest")
    actual_hash = _sha256(original_artifact)
    if actual_hash != artifact_entry["artifact_sha256"]:
        raise ValueError(
            f"Initial artifact SHA256 mismatch: expected "
            f"{artifact_entry['artifact_sha256']}, got {actual_hash}"
        )
    aws_metadata = _configure_aws(args)
    output_dir = _episode_output_dir(args.result_dir, task_id)
    shutil.copy2(config_path, output_dir / "reference_task_config.json")
    shutil.copy2(original_artifact, output_dir / profile.packet_artifact_filename)
    _write_json(output_dir / "reference_package.json", package)
    _write_json(output_dir / "artifact_manifest_entry.json", artifact_entry)
    _write_json(
        output_dir / "reference_review.json",
        {"reference_task_id": task_id, "decision": review_status},
    )

    from desktop_env.desktop_env import DesktopEnv
    from desktop_env.trajectory import TrajectoryRecorder

    recorder = TrajectoryRecorder(output_dir, task_id=task_id, actor="human")
    artifacts: dict[str, str] = {
        "normalized_trajectory": "events.jsonl",
        "manifest": "episode_manifest.json",
        "task_config": "reference_task_config.json",
        "reference_package": "reference_package.json",
        "initial_artifact": profile.packet_artifact_filename,
    }
    env = None
    recording_started = False
    input_started = False
    video_start_monotonic_ns = None
    video_stop_monotonic_ns = None
    recording_duration_metadata: dict[str, float] = {}
    recording_timeline_metadata: dict[str, int | float | str] = {}
    key_overlay_event_count = 0
    pointer_overlay_event_count = 0
    sampler_stop = None
    sampler_thread = None
    sampler_errors: list[str] = []
    completed = False
    ssm_tunnels = []
    try:
        print("AWS preflight passed. Starting a clean OSWorld Ubuntu instance...")
        env = DesktopEnv(
            provider_name="aws",
            region=args.aws_region,
            os_type="Ubuntu",
            action_space="pyautogui",
            require_a11y_tree=args.require_a11y_tree,
            setup_only=True,
        )
        if aws_metadata["connection_mode"] == "ssm":
            import boto3

            print("Waiting for the instance to become available through SSM...")
            ssm_client = boto3.Session(
                profile_name=args.aws_profile, region_name=args.aws_region
            ).client("ssm")
            aws_metadata["ssm_ready_seconds"] = wait_for_ssm_online(
                ssm_client, env.path_to_vm
            )
            guest_ttl_minutes = int(os.getenv("DEFAULT_TTL_MINUTES", "180"))
            arm_guest_termination_backstop(
                ssm_client,
                env.path_to_vm,
                ttl_minutes=guest_ttl_minutes,
            )
            aws_metadata["guest_termination_backstop_minutes"] = guest_ttl_minutes
            multiplexed_tunnel = start_ssm_ssh_forward(
                ssm_client,
                env.path_to_vm,
                profile=args.aws_profile,
                region=args.aws_region,
            )
            ssm_tunnels.append(multiplexed_tunnel)
            _retarget_env_to_local_api(env, multiplexed_tunnel.api_port)
            novnc_url = _novnc_preview_url(
                "127.0.0.1", multiplexed_tunnel.novnc_port
            )
            aws_metadata["local_tunnel_ports"] = {
                "api": multiplexed_tunnel.api_port,
                "novnc": multiplexed_tunnel.novnc_port,
            }
        else:
            novnc_url = _novnc_preview_url(env.vm_ip, 5910)
        aws_metadata["novnc_preview"] = dict(NOVNC_PREVIEW_SETTINGS)
        print("Waiting for the OSWorld guest API to accept setup requests...")
        aws_metadata["service_ready_seconds"] = wait_for_osworld_api(
            env.vm_ip, port=env.server_port
        )
        novnc_ready_seconds = wait_for_novnc_ready(
            "127.0.0.1" if aws_metadata["connection_mode"] == "ssm" else env.vm_ip,
            (
                multiplexed_tunnel.novnc_port
                if aws_metadata["connection_mode"] == "ssm"
                else 5910
            ),
        )
        aws_metadata["novnc_ready_seconds"] = novnc_ready_seconds
        if novnc_ready_seconds > 3:
            print(
                f"noVNC is functional but slow ({novnc_ready_seconds:.1f}s readiness); "
                "the first browser load can take 10-30 seconds."
            )
        reset_started = recorder.now_ns()
        obs = env.reset(task_config=task)
        recorder.add_timing("environment_setup", recorder.now_ns() - reset_started)
        initial_ref, initial_a11y = _save_observation(
            output_dir,
            recorder,
            obs,
            stem="initial_state",
            kind="initial",
        )
        if initial_ref:
            artifacts["initial_state"] = initial_ref
        if initial_a11y:
            artifacts["initial_a11y"] = initial_a11y

        _print_aws_access(env, novnc_url)
        _print_operator_guide(task, review_status)
        input("\nInspect the desktop. Press Enter to START recording...\n")

        start_obs = env._get_obs()
        start_ref, start_a11y = _save_observation(
            output_dir,
            recorder,
            start_obs,
            stem="recording_start",
            kind="recording_start",
        )
        if start_ref:
            artifacts["recording_start"] = start_ref
        if start_a11y:
            artifacts["recording_start_a11y"] = start_a11y
        if not args.no_input_events:
            input_started = start_guest_key_capture(env)
            if input_started:
                artifacts["input_events"] = "input_events.xinput.log"
                artifacts["timestamped_input_events"] = "input_events.timestamped.jsonl"
                artifacts["input_keymap"] = "input_keymap.xmodmap"
            elif not args.no_key_overlay:
                raise RuntimeError(
                    "Key capture is required for formal reference-video recording"
                )
            else:
                print("Warning: xinput recording is unavailable; continuing.")
        started_ns = recorder.now_ns()
        start_guest_reference_recording(env)
        recording_started = True
        if input_started:
            video_start_monotonic_ns = guest_recording_start_monotonic_ns(env)
            _write_json(
                output_dir / "input_timing.json",
                {
                    "schema_version": "1.0",
                    "clock": "guest_monotonic_ns",
                    "video_start_monotonic_ns": video_start_monotonic_ns,
                    "provisional_video_start_monotonic_ns": (
                        video_start_monotonic_ns
                    ),
                    "alignment_status": "provisional",
                },
            )
            artifacts["input_timing"] = "input_timing.json"
        sampler_stop, sampler_thread, sampler_errors = _start_screenshot_sampler(
            env, output_dir, recorder, args.sample_interval
        )
        recorder.record_event(
            "annotation_control",
            started_ns=started_ns,
            finished_ns=recorder.now_ns(),
            metadata={"state": "recording_started"},
        )
        print("\nRECORDING IS ACTIVE. The guide remains above in this terminal.")
        input("Complete the task, then press Enter to STOP recording...\n")

        stopped_ns = recorder.now_ns()
        if sampler_stop is not None:
            sampler_stop.set()
        if sampler_thread is not None:
            sampler_thread.join(timeout=max(5.0, args.sample_interval * 2))
        finalize_started = recorder.now_ns()
        raw_recording_path = output_dir / "recording_raw.mp4"
        recording_log_path = output_dir / "recording_capture.ffmpeg.log"
        video_stop_monotonic_ns = stop_guest_reference_recording(env)
        recording_started = False
        capture_retrieved = False
        if input_started:
            capture_retrieved = stop_guest_key_capture(env, output_dir)
            if not capture_retrieved:
                for name in (
                    "input_events",
                    "timestamped_input_events",
                    "input_keymap",
                ):
                    artifacts.pop(name, None)
                sampler_errors.append("input-event logs could not be retrieved")
            input_started = False
        collect_guest_reference_recording(
            env,
            raw_recording_path,
            recording_log_path,
        )
        recorder.add_timing("recording_finalize", recorder.now_ns() - finalize_started)
        if not raw_recording_path.is_file() or raw_recording_path.stat().st_size == 0:
            raise RuntimeError("OSWorld did not return recording_raw.mp4")
        if video_start_monotonic_ns is None or video_stop_monotonic_ns is None:
            raise RuntimeError("Guest recording timing was not captured")
        recording_duration_metadata = validate_recording_duration(
            raw_recording_path,
            start_monotonic_ns=video_start_monotonic_ns,
            stop_monotonic_ns=video_stop_monotonic_ns,
        )
        timeline = calibrate_recording_timeline(
            provisional_start_monotonic_ns=video_start_monotonic_ns,
            stop_monotonic_ns=video_stop_monotonic_ns,
            actual_duration_seconds=recording_duration_metadata["actual_seconds"],
        )
        calibrated_video_start_monotonic_ns = (
            timeline.calibrated_video_start_monotonic_ns
        )
        recording_timeline_metadata = timeline.to_dict()
        if capture_retrieved:
            _write_json(
                output_dir / "input_timing.json",
                {
                    "schema_version": "1.0",
                    "clock": "guest_monotonic_ns",
                    "video_start_monotonic_ns": (
                        calibrated_video_start_monotonic_ns
                    ),
                    "alignment_status": "calibrated",
                    **recording_timeline_metadata,
                },
            )
        artifacts["recording_raw"] = raw_recording_path.name
        if recording_log_path.is_file():
            artifacts["recording_capture_log"] = recording_log_path.name
        recorder.record_event(
            "annotation_control",
            started_ns=stopped_ns,
            finished_ns=recorder.now_ns(),
            metadata={"state": "recording_stopped"},
        )

        recording_path = output_dir / "recording.mp4"
        if capture_retrieved and video_start_monotonic_ns is not None:
            timestamped_text = (
                output_dir / "input_events.timestamped.jsonl"
            ).read_text(encoding="utf-8")
            keymap_text = (output_dir / "input_keymap.xmodmap").read_text(
                encoding="utf-8"
            )
            key_events = parse_timestamped_xinput(
                timestamped_text,
                keymap_text,
                video_start_monotonic_ns=calibrated_video_start_monotonic_ns,
            )
            key_overlay_event_count = len(key_events)
            write_key_events(output_dir / "key_events.jsonl", key_events)
            artifacts["key_events"] = "key_events.jsonl"
            pointer_events = parse_timestamped_pointer_events(
                timestamped_text,
                video_start_monotonic_ns=calibrated_video_start_monotonic_ns,
                keymap_text=keymap_text,
            )
            pointer_overlay_event_count = len(pointer_events)
            write_pointer_events(
                output_dir / "pointer_events.jsonl", pointer_events
            )
            artifacts["pointer_events"] = "pointer_events.jsonl"
            if not args.no_key_overlay:
                overlay_path = output_dir / "key_overlay.ass"
                overlay_path.write_text(
                    render_key_overlay_ass(
                        key_events, pointer_events=pointer_events
                    ),
                    encoding="utf-8",
                )
                artifacts["key_overlay"] = overlay_path.name
                burn_key_overlay_in_guest(env, overlay_path, recording_path)
            else:
                shutil.copy2(raw_recording_path, recording_path)
        elif not args.no_key_overlay:
            raise RuntimeError(
                "The raw video was saved, but required key events were unavailable"
            )
        else:
            shutil.copy2(raw_recording_path, recording_path)
        if not recording_path.is_file() or recording_path.stat().st_size == 0:
            raise RuntimeError("Could not create the default recording.mp4")
        artifacts["recording"] = recording_path.name

        final_path = output_dir / profile.final_artifact_filename
        _save_guest_artifact(
            env,
            annotation["guest_artifact_path"],
            final_path,
            app=profile.app,
        )
        artifacts["final_artifact"] = final_path.name
        final_obs = env._get_obs()
        final_ref, final_a11y = _save_observation(
            output_dir,
            recorder,
            final_obs,
            stem="final_state",
            kind="final",
        )
        if final_ref:
            artifacts["final_state"] = final_ref
        if final_a11y:
            artifacts["final_a11y"] = final_a11y
        recorder.finalize(
            status="completed",
            result=None,
            artifacts=artifacts,
            metadata={
                **aws_metadata,
                "instance_id": env.path_to_vm,
                "review_status": review_status,
                "sample_errors": sampler_errors,
                "input_events_captured": "input_events" in artifacts,
                "key_overlay_enabled": not args.no_key_overlay,
                "key_overlay_event_count": key_overlay_event_count,
                "pointer_overlay_event_count": pointer_overlay_event_count,
                "recording_capture_preset": "ultrafast",
                "recording_duration": recording_duration_metadata,
                "recording_timeline": recording_timeline_metadata,
                "preferred_reference_video": "recording.mp4",
            },
        )
        completed = True
        print(f"Reference annotation bundle saved to: {output_dir}")
        return 0
    except KeyboardInterrupt:
        print("\nAnnotation interrupted; preserving available artifacts.")
        if not completed:
            recorder.finalize(
                status="interrupted",
                result=None,
                artifacts=artifacts,
                metadata={**aws_metadata, "sample_errors": sampler_errors},
            )
        return 130
    except Exception as exc:
        recorder.record_event(
            "result", outcome="error", error=f"{type(exc).__name__}: {exc}"
        )
        recorder.finalize(
            status="failed",
            result=None,
            artifacts=artifacts,
            error=f"{type(exc).__name__}: {exc}",
            metadata={**aws_metadata, "sample_errors": sampler_errors},
        )
        raise
    finally:
        if sampler_stop is not None:
            sampler_stop.set()
        if sampler_thread is not None and sampler_thread.is_alive():
            sampler_thread.join(timeout=5)
        if env is not None and input_started:
            try:
                stop_guest_key_capture(env, output_dir)
            except Exception:
                pass
        if env is not None and recording_started:
            try:
                stop_guest_reference_recording(env)
                collect_guest_reference_recording(
                    env,
                    output_dir / "recording_raw.mp4",
                    output_dir / "recording_capture.ffmpeg.log",
                )
            except Exception:
                pass
        for tunnel in reversed(ssm_tunnels):
            tunnel.close()
        if env is not None:
            print("Terminating the AWS annotation instance...")
            env.close()
            print("AWS instance terminated; TTL remains the failure backstop.")


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, _handle_stop_signal)
    raise SystemExit(main())
