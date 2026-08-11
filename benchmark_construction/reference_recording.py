"""Reference-annotation recording helpers that run directly in the guest."""

from __future__ import annotations

import base64
import json
import os
import struct
from pathlib import Path
from typing import Any


GUEST_RECORDING = "/tmp/recording.mp4"
GUEST_RECORDING_PID = "/tmp/osworld-reference-recording.pid"
GUEST_RECORDING_STDERR = "/tmp/osworld-reference-recording.ffmpeg.log"


_START_SOURCE = r"""
import os
import pathlib
import re
import subprocess
import time

recording = pathlib.Path("/tmp/recording.mp4")
pid_path = pathlib.Path("/tmp/osworld-reference-recording.pid")
stderr_path = pathlib.Path("/tmp/osworld-reference-recording.ffmpeg.log")
for path in (recording, pid_path, stderr_path):
    path.unlink(missing_ok=True)

env = dict(os.environ, DISPLAY=":0")
display_info = subprocess.check_output(
    ["xdpyinfo"], env=env, text=True, stderr=subprocess.STDOUT
)
match = re.search(r"dimensions:\s+(\d+)x(\d+)", display_info)
if not match:
    raise RuntimeError("Could not determine X11 display dimensions")
width, height = match.groups()
stderr = open(stderr_path, "wb", buffering=0)
proc = subprocess.Popen(
    [
        "ffmpeg",
        "-y",
        "-loglevel",
        "warning",
        "-f",
        "x11grab",
        "-draw_mouse",
        "1",
        "-framerate",
        "30",
        "-video_size",
        f"{width}x{height}",
        "-i",
        ":0.0",
        "-c:v",
        "libx264",
        "-preset",
        "ultrafast",
        "-crf",
        "23",
        "-pix_fmt",
        "yuv420p",
        "-r",
        "30",
        str(recording),
    ],
    stdout=subprocess.DEVNULL,
    stderr=stderr,
    start_new_session=True,
    env=env,
)
pid_path.write_text(str(proc.pid), encoding="utf-8")
time.sleep(2)
if proc.poll() is not None:
    stderr.close()
    message = stderr_path.read_text(encoding="utf-8", errors="replace")[-2000:]
    raise RuntimeError(f"Reference ffmpeg exited during startup: {message}")
print(proc.pid)
""".strip()


_STOP_SOURCE = r"""
import json
import os
import pathlib
import signal
import time

pid_path = pathlib.Path("/tmp/osworld-reference-recording.pid")
recording = pathlib.Path("/tmp/recording.mp4")
pid = int(pid_path.read_text(encoding="utf-8"))
stop_ns = time.monotonic_ns()
try:
    os.kill(pid, signal.SIGINT)
except ProcessLookupError:
    pass
for _ in range(300):
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        break
    time.sleep(0.05)
else:
    os.kill(pid, signal.SIGKILL)
    raise RuntimeError("Reference ffmpeg did not stop within 15 seconds")
if not recording.is_file() or recording.stat().st_size == 0:
    raise RuntimeError("Reference ffmpeg produced no recording")
print(json.dumps({"stop_monotonic_ns": stop_ns, "size": recording.stat().st_size}))
""".strip()


def _execute_source(env: Any, source: str, label: str) -> str:
    encoded = base64.b64encode(source.encode("utf-8")).decode("ascii")
    result = env.controller.execute_python_command(
        "import base64; "
        f"exec(compile(base64.b64decode({encoded!r}),{label!r},'exec'))"
    )
    output = result.get("output", "").strip() if result else ""
    if not output:
        raise RuntimeError(f"Guest {label} command returned no output")
    return output


def start_guest_reference_recording(env: Any) -> int:
    """Start a low-overhead recorder whose stderr cannot block FFmpeg."""

    output = _execute_source(env, _START_SOURCE, "<reference-recording-start>")
    if not output.isdigit():
        raise RuntimeError(f"Guest reference recorder returned invalid PID: {output}")
    return int(output)


def stop_guest_reference_recording(env: Any) -> int:
    """Stop the recorder immediately and return the guest monotonic stop time."""

    output = _execute_source(env, _STOP_SOURCE, "<reference-recording-stop>")
    try:
        result = json.loads(output)
        stop_ns = result["stop_monotonic_ns"]
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        raise RuntimeError(
            f"Guest reference recorder returned invalid stop data: {output}"
        ) from exc
    if not isinstance(stop_ns, int) or stop_ns < 0:
        raise RuntimeError("Guest reference recorder returned an invalid stop time")
    return stop_ns


def collect_guest_reference_recording(
    env: Any,
    video_path: Path,
    stderr_path: Path,
) -> None:
    """Retrieve the stopped raw MP4 and its bounded FFmpeg diagnostic log."""

    video = env.controller.get_file(GUEST_RECORDING)
    if not video:
        raise RuntimeError("Could not retrieve guest reference recording")
    video_path.write_bytes(video)
    stderr = env.controller.get_file(GUEST_RECORDING_STDERR)
    if stderr is not None:
        stderr_path.write_bytes(stderr)


def mp4_duration_seconds(path: Path) -> float:
    """Read the movie-header duration without requiring local ffprobe."""

    data = path.read_bytes()
    marker = data.find(b"mvhd")
    if marker < 0 or marker + 24 > len(data):
        raise ValueError(f"MP4 movie header is missing or truncated: {path}")
    version = data[marker + 4]
    if version == 0:
        timescale = struct.unpack(">I", data[marker + 16 : marker + 20])[0]
        duration = struct.unpack(">I", data[marker + 20 : marker + 24])[0]
    elif version == 1 and marker + 40 <= len(data):
        timescale = struct.unpack(">I", data[marker + 28 : marker + 32])[0]
        duration = struct.unpack(">Q", data[marker + 32 : marker + 40])[0]
    else:
        raise ValueError(f"Unsupported MP4 movie-header version: {version}")
    if timescale == 0:
        raise ValueError("MP4 movie-header timescale is zero")
    return duration / timescale


def validate_recording_duration(
    path: Path,
    *,
    start_monotonic_ns: int,
    stop_monotonic_ns: int,
    tolerance_seconds: float = 5.0,
) -> dict[str, float]:
    """Fail closed when the MP4 is materially shorter than its guest window."""

    if stop_monotonic_ns <= start_monotonic_ns:
        raise ValueError("Recording stop time must be after start time")
    expected = (stop_monotonic_ns - start_monotonic_ns) / 1_000_000_000
    actual = mp4_duration_seconds(path)
    missing = expected - actual
    if missing > tolerance_seconds:
        raise RuntimeError(
            "Reference recording is truncated: "
            f"expected about {expected:.3f}s, got {actual:.3f}s "
            f"({missing:.3f}s missing)"
        )
    return {
        "expected_seconds": expected,
        "actual_seconds": actual,
        "missing_seconds": missing,
    }
