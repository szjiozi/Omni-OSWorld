import json
import struct
from pathlib import Path
from types import SimpleNamespace

import pytest

from benchmark_construction.reference_recording import (
    GUEST_RECORDING,
    GUEST_RECORDING_STDERR,
    _START_SOURCE,
    calibrate_recording_timeline,
    collect_guest_reference_recording,
    mp4_duration_seconds,
    start_guest_reference_recording,
    stop_guest_reference_recording,
    validate_recording_duration,
)


def _mp4_with_duration(seconds: float, timescale: int = 1000) -> bytes:
    duration = round(seconds * timescale)
    return (
        b"prefix"
        + b"mvhd"
        + b"\x00\x00\x00\x00"
        + b"\x00" * 8
        + struct.pack(">I", timescale)
        + struct.pack(">I", duration)
        + b"suffix"
    )


class _FakeController:
    def __init__(self):
        self.commands = []
        self.files = {
            GUEST_RECORDING: _mp4_with_duration(12.0),
            GUEST_RECORDING_STDERR: b"warning log\n",
        }

    def execute_python_command(self, command):
        self.commands.append(command)
        if "reference-recording-start" in command:
            return {"output": "4321"}
        if "reference-recording-stop" in command:
            return {
                "output": json.dumps(
                    {"stop_monotonic_ns": 13_000_000_000, "size": 1234}
                )
            }
        return {"output": ""}

    def get_file(self, path):
        return self.files.get(path)


def test_guest_reference_recorder_starts_stops_and_collects(tmp_path):
    controller = _FakeController()
    env = SimpleNamespace(controller=controller)
    video_path = tmp_path / "recording_raw.mp4"
    stderr_path = tmp_path / "recording_capture.ffmpeg.log"

    assert start_guest_reference_recording(env) == 4321
    assert stop_guest_reference_recording(env) == 13_000_000_000
    collect_guest_reference_recording(env, video_path, stderr_path)

    assert video_path.read_bytes() == controller.files[GUEST_RECORDING]
    assert stderr_path.read_bytes() == b"warning log\n"
    assert len(controller.commands) == 2


def test_reference_recorder_cannot_block_on_an_unread_stderr_pipe():
    assert '"ultrafast"' in _START_SOURCE
    assert "stderr=stderr" in _START_SOURCE
    assert "stderr=subprocess.PIPE" not in _START_SOURCE


def test_reference_recorder_waits_for_ffmpeg_first_frame_before_ready():
    assert '"-progress"' in _START_SOURCE
    assert '"first_frame_monotonic_ns"' in _START_SOURCE
    assert '"ffmpeg_progress_first_frame"' in _START_SOURCE
    assert "did not produce its first frame within 30 seconds" in _START_SOURCE


def test_mp4_duration_parser_and_integrity_check(tmp_path):
    video_path = tmp_path / "recording_raw.mp4"
    video_path.write_bytes(_mp4_with_duration(12.0))

    assert mp4_duration_seconds(video_path) == 12.0
    result = validate_recording_duration(
        video_path,
        start_monotonic_ns=1_000_000_000,
        stop_monotonic_ns=14_000_000_000,
    )

    assert result["expected_seconds"] == 13.0
    assert result["actual_seconds"] == 12.0
    assert result["missing_seconds"] == 1.0


def test_recording_integrity_check_rejects_truncation(tmp_path):
    video_path = tmp_path / "recording_raw.mp4"
    video_path.write_bytes(_mp4_with_duration(277.8))

    with pytest.raises(RuntimeError, match="77.200s missing"):
        validate_recording_duration(
            video_path,
            start_monotonic_ns=0,
            stop_monotonic_ns=355_000_000_000,
        )


def test_recording_timeline_calibrates_variable_ffmpeg_startup_gap():
    timeline = calibrate_recording_timeline(
        provisional_start_monotonic_ns=972_130_000_000,
        stop_monotonic_ns=1_085_055_201_996,
        actual_duration_seconds=111.0,
    )

    assert timeline.calibrated_video_start_monotonic_ns == 974_055_201_996
    assert timeline.alignment_correction_ms == pytest.approx(1925.201996)
    assert timeline.to_dict()["alignment_method"] == "stop_minus_mp4_duration"


@pytest.mark.parametrize("duration", [0.0, -1.0, float("inf"), float("nan")])
def test_recording_timeline_rejects_invalid_duration(duration):
    with pytest.raises(ValueError, match="positive and finite"):
        calibrate_recording_timeline(
            provisional_start_monotonic_ns=1_000_000_000,
            stop_monotonic_ns=2_000_000_000,
            actual_duration_seconds=duration,
        )
