#!/usr/bin/env python3
"""Run an inspectable OSWorld environment and optionally collect a human demo."""

from __future__ import annotations

import argparse
import copy
import json
import signal
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Start OSWorld for manual interaction. With --task-config, capture "
            "an aligned human demonstration and run the task evaluator."
        )
    )
    parser.add_argument(
        "--provider-name",
        "--provider_name",
        dest="provider_name",
        default="docker",
        help="OSWorld provider to use (default: docker).",
    )
    parser.add_argument(
        "--path-to-vm",
        "--path_to_vm",
        dest="path_to_vm",
        default=None,
        help="Optional existing VM image or provider-specific VM path.",
    )
    parser.add_argument(
        "--os-type",
        "--os_type",
        dest="os_type",
        default="Ubuntu",
        choices=("Ubuntu", "Windows"),
        help="Guest operating system (default: Ubuntu).",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Start a local hypervisor without its native GUI.",
    )
    parser.add_argument(
        "--ssh-host",
        default=None,
        help=(
            "SSH config alias for the machine running this script. When supplied, "
            "print a copy-pasteable noVNC tunnel command."
        ),
    )
    parser.add_argument(
        "--local-vnc-port",
        type=int,
        default=8006,
        help="Local Mac port to use in the suggested SSH tunnel (default: 8006).",
    )
    parser.add_argument(
        "--task-config",
        "--task_config",
        type=Path,
        default=None,
        help="Optional OSWorld task JSON to initialize, record, and evaluate.",
    )
    parser.add_argument(
        "--result-dir",
        "--result_dir",
        type=Path,
        default=Path("results_human_examine"),
        help="Root directory for recorded artifacts.",
    )
    parser.add_argument(
        "--sample-interval",
        type=float,
        default=1.0,
        help="Seconds between aligned screenshot samples; 0 disables sampling.",
    )
    parser.add_argument(
        "--no-recording",
        action="store_true",
        help="Do not record an MP4 of the desktop.",
    )
    parser.add_argument(
        "--no-input-events",
        action="store_true",
        help="Do not try to collect guest X11 keyboard/mouse events.",
    )
    parser.add_argument(
        "--require-a11y-tree",
        action="store_true",
        help="Include the accessibility tree in OSWorld observations.",
    )
    return parser.parse_args()


def _format_url_host(host: str) -> str:
    host = host.strip("[]")
    return f"[{host}]" if ":" in host else host


def print_access_instructions(env: Any, args: argparse.Namespace) -> None:
    provider = args.provider_name.lower()
    vm_host = str(env.vm_ip)

    print("\nOSWorld is ready.")
    print(f"Provider: {provider}")
    print(f"VM/controller host: {vm_host}")
    print(f"OSWorld server port: {env.server_port}")
    print(f"VNC port reported by provider: {env.vnc_port}")

    if provider in {"vmware", "virtualbox"} and not args.headless:
        print("\nUse the VMware/VirtualBox window for direct manual interaction.")
        print("The environment remains running until this script exits.")
        return

    if vm_host in {"localhost", "127.0.0.1", "::1"}:
        if args.ssh_host:
            print("\nOn your Mac, open a second terminal and run:")
            print(
                f"  ssh -N -L {args.local_vnc_port}:127.0.0.1:{env.vnc_port} "
                f"{args.ssh_host}"
            )
            print("\nThen open this URL on your Mac:")
            print(f"  http://127.0.0.1:{args.local_vnc_port}")
        else:
            print("\nOpen this URL on the machine running the script:")
            print(f"  http://127.0.0.1:{env.vnc_port}")
        return

    if provider in {"aws", "aliyun", "volcengine", "fastvm"}:
        print("\nOpen the provider's noVNC URL:")
        print(f"  http://{_format_url_host(vm_host)}:5910/vnc.html")
        return

    print("\nTry the provider-reported VNC endpoint:")
    print(f"  http://{_format_url_host(vm_host)}:{env.vnc_port}")


def wait_until_stopped() -> None:
    if sys.stdin.isatty():
        input("\nPress Enter to stop, evaluate, and clean up...\n")
        return

    print("\nNo interactive terminal detected. Press Ctrl-C or send SIGTERM to stop.")
    while True:
        time.sleep(3600)


def _handle_stop_signal(_signum, _frame) -> None:
    raise KeyboardInterrupt


def _load_task(path: Path) -> dict[str, Any]:
    task_path = path if path.is_absolute() else REPO_ROOT / path
    with task_path.open("r", encoding="utf-8") as task_file:
        task = json.load(task_file)

    task = copy.deepcopy(task)
    for setup_step in task.get("config", []):
        if setup_step.get("type") != "upload_file":
            continue
        for file_config in setup_step.get("parameters", {}).get("files", []):
            local_path = Path(file_config["local_path"])
            if not local_path.is_absolute():
                file_config["local_path"] = str(REPO_ROOT / local_path)

    evaluator = task.get("evaluator", {})
    for key in ("expected", "result"):
        getter = evaluator.get(key)
        getters = getter if isinstance(getter, list) else [getter]
        for getter_config in getters:
            if not getter_config or getter_config.get("type") != "local_file":
                continue
            local_path = Path(getter_config["path"])
            if not local_path.is_absolute():
                getter_config["path"] = str(REPO_ROOT / local_path)
    return task


def _episode_output_dir(root: Path, task_id: str) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output_root = root if root.is_absolute() else REPO_ROOT / root
    output_dir = output_root / task_id / timestamp
    output_dir.mkdir(parents=True, exist_ok=False)
    return output_dir


def _save_observation(
    output_dir: Path,
    recorder: Any,
    obs: dict[str, Any],
    *,
    stem: str,
    kind: str,
) -> tuple[str | None, str | None]:
    screenshot_ref = None
    a11y_ref = None
    if obs.get("screenshot"):
        screenshot_ref = f"{stem}.png"
        (output_dir / screenshot_ref).write_bytes(obs["screenshot"])
    if obs.get("accessibility_tree"):
        a11y_ref = f"{stem}.xml"
        (output_dir / a11y_ref).write_text(
            obs["accessibility_tree"],
            encoding="utf-8",
        )

    now_ns = recorder.now_ns()
    recorder.record_event(
        "observation",
        started_ns=now_ns,
        finished_ns=now_ns,
        observation_ref=screenshot_ref,
        a11y_ref=a11y_ref,
        metadata={"kind": kind},
    )
    return screenshot_ref, a11y_ref


def _start_guest_input_recorder(env: Any) -> bool:
    log_path = "/tmp/osworld-human-input.log"
    pid_path = "/tmp/osworld-human-input.pid"
    command = (
        "import os, subprocess; "
        f"log_path={log_path!r}; pid_path={pid_path!r}; "
        "stream=open(log_path, 'w', buffering=1); "
        "proc=subprocess.Popen("
        "['stdbuf', '-oL', 'xinput', 'test-xi2', '--root'], "
        "stdout=stream, stderr=subprocess.STDOUT, "
        "env=dict(os.environ, DISPLAY=':0')); "
        "open(pid_path, 'w').write(str(proc.pid)); "
        "print(proc.pid)"
    )
    result = env.controller.execute_python_command(command)
    return bool(result and result.get("output", "").strip())


def _stop_guest_input_recorder(env: Any, output_dir: Path) -> bool:
    command = (
        "import os, signal, time; "
        "pid=int(open('/tmp/osworld-human-input.pid').read()); "
        "os.kill(pid, signal.SIGTERM); "
        "time.sleep(0.5)"
    )
    env.controller.execute_python_command(command)
    content = env.controller.get_file("/tmp/osworld-human-input.log")
    if content is None:
        return False
    (output_dir / "input_events.xinput.log").write_bytes(content)
    return True


def _start_screenshot_sampler(
    env: Any,
    output_dir: Path,
    recorder: Any,
    interval: float,
) -> tuple[threading.Event, threading.Thread | None, list[str]]:
    stop_event = threading.Event()
    errors: list[str] = []
    if interval <= 0:
        return stop_event, None, errors

    frames_dir = output_dir / "frames"
    frames_dir.mkdir(exist_ok=True)

    def sample() -> None:
        index = 0
        while not stop_event.wait(interval):
            started_ns = recorder.now_ns()
            try:
                screenshot = env.controller.get_screenshot()
                finished_ns = recorder.now_ns()
                if not screenshot:
                    raise RuntimeError("controller returned no screenshot")
                filename = f"{index:06d}_{started_ns}.png"
                (frames_dir / filename).write_bytes(screenshot)
                recorder.record_event(
                    "observation",
                    started_ns=started_ns,
                    finished_ns=finished_ns,
                    observation_ref=f"frames/{filename}",
                    latency_ms={
                        "environment": (finished_ns - started_ns) / 1_000_000
                    },
                    metadata={"kind": "periodic_sample"},
                )
                index += 1
            except Exception as exc:  # noqa: BLE001 - preserve the human session.
                errors.append(f"{type(exc).__name__}: {exc}")

    thread = threading.Thread(
        target=sample,
        name="osworld-screenshot-sampler",
        daemon=True,
    )
    thread.start()
    return stop_event, thread, errors


def main() -> int:
    args = parse_args()

    if not 1 <= args.local_vnc_port <= 65535:
        raise SystemExit("--local-vnc-port must be between 1 and 65535")
    if args.sample_interval < 0:
        raise SystemExit("--sample-interval must be non-negative")

    # Import after parsing so --help works before heavy dependencies are installed.
    from desktop_env.desktop_env import DesktopEnv
    from desktop_env.trajectory import TrajectoryRecorder, validate_document

    env = None
    recorder = None
    output_dir = None
    recording_started = False
    input_recorder_started = False
    sampler_stop = None
    sampler_thread = None
    sampler_errors: list[str] = []
    result = None
    interrupted = False
    task = _load_task(args.task_config) if args.task_config else None
    task_id = task["id"] if task else "manual-exploration"
    if task and "video_learning" in task:
        validate_document(task, "task")
    output_dir = _episode_output_dir(args.result_dir, task_id)
    recorder = TrajectoryRecorder(output_dir, task_id=task_id, actor="human")
    artifacts: dict[str, str] = {
        "normalized_trajectory": "events.jsonl",
        "manifest": "episode_manifest.json",
    }

    try:
        print("Starting OSWorld environment...")
        env = DesktopEnv(
            provider_name=args.provider_name,
            path_to_vm=args.path_to_vm,
            os_type=args.os_type,
            action_space="pyautogui",
            headless=args.headless,
            require_a11y_tree=args.require_a11y_tree,
        )

        print("Checking that the desktop is responsive...")
        reset_started_ns = recorder.now_ns()
        obs = env.reset(task_config=task)
        recorder.add_timing(
            "environment_setup",
            recorder.now_ns() - reset_started_ns,
        )
        screenshot_ref, a11y_ref = _save_observation(
            output_dir,
            recorder,
            obs,
            stem="initial_state",
            kind="initial",
        )
        if screenshot_ref:
            artifacts["initial_state"] = screenshot_ref
        if a11y_ref:
            artifacts["initial_a11y"] = a11y_ref

        if not args.no_recording:
            env.controller.start_recording()
            recording_started = True
            artifacts["recording"] = "recording.mp4"

        if not args.no_input_events:
            try:
                input_recorder_started = _start_guest_input_recorder(env)
                if input_recorder_started:
                    artifacts["input_events"] = "input_events.xinput.log"
                else:
                    print(
                        "Warning: guest input-event recording is unavailable; "
                        "continuing with screenshots and video."
                    )
            except Exception as exc:  # noqa: BLE001 - preserve the human session.
                print(f"Warning: could not start guest input recorder: {exc}")

        sampler_stop, sampler_thread, sampler_errors = _start_screenshot_sampler(
            env,
            output_dir,
            recorder,
            args.sample_interval,
        )
        print_access_instructions(env, args)
        try:
            wait_until_stopped()
        except KeyboardInterrupt:
            print("\nStop requested.")
            interrupted = True

        sampler_stop.set()
        if sampler_thread is not None:
            sampler_thread.join(timeout=max(5.0, args.sample_interval * 2))

        if input_recorder_started:
            if not _stop_guest_input_recorder(env, output_dir):
                artifacts.pop("input_events", None)
                sampler_errors.append("input-event log could not be retrieved")
            input_recorder_started = False

        final_obs = env._get_obs()
        final_screenshot, final_a11y = _save_observation(
            output_dir,
            recorder,
            final_obs,
            stem="final_state",
            kind="final",
        )
        if final_screenshot:
            artifacts["final_state"] = final_screenshot
        if final_a11y:
            artifacts["final_a11y"] = final_a11y

        if task:
            evaluation_started_ns = recorder.now_ns()
            result = env.evaluate()
            evaluation_finished_ns = recorder.now_ns()
            recorder.add_timing(
                "evaluation",
                evaluation_finished_ns - evaluation_started_ns,
            )
            (output_dir / "result.txt").write_text(
                f"{result}\n",
                encoding="utf-8",
            )
            artifacts["result"] = "result.txt"
            recorder.record_event(
                "result",
                started_ns=evaluation_started_ns,
                finished_ns=evaluation_finished_ns,
                outcome="ok",
                metadata={"score": result},
            )
            print(f"Evaluator result: {result}")

        if recording_started:
            finalize_started_ns = recorder.now_ns()
            env.controller.end_recording(str(output_dir / "recording.mp4"))
            recorder.add_timing(
                "recording_finalize",
                recorder.now_ns() - finalize_started_ns,
            )
            recording_started = False

        recorder.finalize(
            status="interrupted" if interrupted else "completed",
            result=result,
            artifacts=artifacts,
            metadata={
                "provider": args.provider_name,
                "task_config": str(args.task_config) if args.task_config else None,
                "sample_errors": sampler_errors,
                "input_events_captured": "input_events" in artifacts,
            },
        )
        print(f"Artifacts: {output_dir}")
        return 130 if interrupted else 0
    except KeyboardInterrupt:
        print("\nStop requested.")
        interrupted = True
        recorder.record_event(
            "result",
            outcome="skipped",
            metadata={"reason": "interrupted"},
        )
        recorder.finalize(
            status="interrupted",
            result=result,
            artifacts=artifacts,
            metadata={"sample_errors": sampler_errors},
        )
        return 130
    except Exception as exc:
        recorder.record_event(
            "result",
            outcome="error",
            error=f"{type(exc).__name__}: {exc}",
        )
        recorder.finalize(
            status="failed",
            result=result,
            artifacts=artifacts,
            error=f"{type(exc).__name__}: {exc}",
            metadata={"sample_errors": sampler_errors},
        )
        raise
    finally:
        if sampler_stop is not None:
            sampler_stop.set()
        if sampler_thread is not None and sampler_thread.is_alive():
            sampler_thread.join(timeout=5)
        if env is not None and input_recorder_started:
            try:
                _stop_guest_input_recorder(env, output_dir)
            except Exception:
                pass
        if env is not None and recording_started:
            try:
                env.controller.end_recording(str(output_dir / "recording.mp4"))
            except Exception:
                pass
        if env is not None:
            print("Stopping OSWorld environment...")
            env.close()
            print("Environment stopped.")


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, _handle_stop_signal)
    raise SystemExit(main())
