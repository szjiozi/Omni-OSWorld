import json
import sys
import types
from types import SimpleNamespace

import pytest

if sys.version_info < (3, 12):
    pytest.skip(
        "OSWorld requires Python >=3.12; the default runner cannot import here",
        allow_module_level=True,
    )

sys.modules.setdefault(
    "wrapt_timeout_decorator",
    types.ModuleType("wrapt_timeout_decorator"),
)

import lib_run_single


class _FakeController:
    def start_recording(self):
        return None

    def end_recording(self, dest):
        with open(dest, "wb") as recording_file:
            recording_file.write(b"fake-mp4")


class _FakeEnv:
    vm_ip = "localhost"

    def __init__(self):
        self.controller = _FakeController()
        self._screenshot = b"\x89PNG\r\n\x1a\nfake"

    def reset(self, task_config):
        return self._get_obs()

    def _get_obs(self):
        return {
            "screenshot": self._screenshot,
            "accessibility_tree": "<root/>",
        }

    def step(self, action, pause):
        return self._get_obs(), 0.0, action == "DONE", {"done": action == "DONE"}

    def evaluate(self):
        return 1.0


class _FakeAgent:
    def reset(self, *args, **kwargs):
        return None

    def predict(self, instruction, obs):
        return {"plan": "finish"}, ["DONE"]


def _read_jsonl(path):
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
    ]


def test_default_runner_keeps_raw_trajectory_and_writes_manifest(
    tmp_path,
    monkeypatch,
):
    monkeypatch.setattr(lib_run_single.time, "sleep", lambda _seconds: None)
    monkeypatch.setattr(
        lib_run_single,
        "log_task_completion",
        lambda *args, **kwargs: None,
    )
    scores = []

    lib_run_single.run_single_example(
        _FakeAgent(),
        _FakeEnv(),
        {"id": "task-1"},
        1,
        "Finish the task",
        SimpleNamespace(sleep_after_execution=0),
        str(tmp_path),
        scores,
    )

    assert scores == [1.0]
    assert len(_read_jsonl(tmp_path / "traj.jsonl")) == 1
    events = _read_jsonl(tmp_path / "events.jsonl")
    assert [event["event_type"] for event in events] == [
        "observation",
        "plan",
        "action",
        "result",
    ]
    manifest = json.loads(
        (tmp_path / "episode_manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["status"] == "completed"
    assert manifest["result"] == 1.0
    assert "execution" in manifest["timings_ms"]
    assert (tmp_path / "recording.mp4").exists()


def test_default_runner_writes_failed_manifest(tmp_path, monkeypatch):
    class FailingAgent(_FakeAgent):
        def predict(self, instruction, obs):
            raise RuntimeError("model unavailable")

    monkeypatch.setattr(lib_run_single.time, "sleep", lambda _seconds: None)

    with pytest.raises(RuntimeError, match="model unavailable"):
        lib_run_single.run_single_example(
            FailingAgent(),
            _FakeEnv(),
            {"id": "task-2"},
            1,
            "Finish the task",
            SimpleNamespace(sleep_after_execution=0),
            str(tmp_path),
            [],
        )

    manifest = json.loads(
        (tmp_path / "episode_manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["status"] == "failed"
    assert "model unavailable" in manifest["error"]
