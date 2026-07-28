import json

import pytest

from desktop_env.trajectory import TrajectoryRecorder, validate_document


def test_recorder_writes_valid_event_and_atomic_manifest(tmp_path):
    recorder = TrajectoryRecorder(
        tmp_path,
        task_id="task-1",
        actor="agent",
        episode_id="b659748a-23b6-4e7d-98f5-4a00ff7dd552",
        validate_events=True,
    )
    recorder.add_timing("model", 2_000_000)
    event = recorder.record_event(
        "action",
        group_id=0,
        started_ns=10,
        finished_ns=20,
        semantic_action={"verb": "click", "target": "button.save", "args": {}},
        raw_action="pyautogui.click(10, 10)",
        latency_ms={"model": 2.0, "environment": 3.0},
        observation_ref="frames/000001.png",
    )

    validate_document(event, "trajectory_event")
    manifest = recorder.finalize(
        status="completed",
        result=1.0,
        artifacts={"recording": "recording.mp4"},
    )

    recorded = [
        json.loads(line)
        for line in (tmp_path / "events.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    assert recorded == [event]
    assert manifest["event_count"] == 1
    assert manifest["timings_ms"]["model"] == 2.0
    assert json.loads(
        (tmp_path / "episode_manifest.json").read_text(encoding="utf-8")
    )["status"] == "completed"
    assert not (tmp_path / "episode_manifest.json.tmp").exists()


def test_recorder_rejects_events_after_finalize(tmp_path):
    recorder = TrajectoryRecorder(tmp_path, task_id="task-1", actor="human")
    recorder.finalize(status="interrupted", result=None)

    with pytest.raises(RuntimeError):
        recorder.record_event("observation")
