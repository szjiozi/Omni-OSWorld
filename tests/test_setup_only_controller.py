from types import SimpleNamespace

import pytest

from desktop_env.controllers.setup_only import SetupOnlyController
from desktop_env.desktop_env import DesktopEnv


def _response():
    return SimpleNamespace(raise_for_status=lambda: None)


def test_setup_only_controller_uploads_then_opens(monkeypatch, tmp_path):
    artifact = tmp_path / "initial.xlsx"
    artifact.write_bytes(b"PK-xlsx")
    calls = []

    def post(url, **kwargs):
        calls.append((url, kwargs))
        return _response()

    monkeypatch.setattr("desktop_env.controllers.setup_only.requests.post", post)
    controller = SetupOnlyController("203.0.113.7")

    assert controller.setup(
        [
            {
                "type": "upload_file",
                "parameters": {
                    "files": [
                        {
                            "local_path": str(artifact),
                            "path": "/home/user/Desktop/initial.xlsx",
                        }
                    ]
                },
            },
            {
                "type": "open",
                "parameters": {"path": "/home/user/Desktop/initial.xlsx"},
            },
        ]
    )
    assert calls[0][0].endswith("/setup/upload")
    assert calls[0][1]["data"]["file_path"].endswith("initial.xlsx")
    assert calls[1][0].endswith("/setup/open_file")
    assert calls[1][1]["json"] == {
        "path": "/home/user/Desktop/initial.xlsx"
    }


def test_setup_only_controller_rejects_extra_actions():
    controller = SetupOnlyController("203.0.113.7")

    with pytest.raises(ValueError, match="Unsupported setup-only action"):
        controller.setup([{"type": "execute", "parameters": {}}])


def test_desktop_env_accepts_setup_only_task_without_evaluator(tmp_path):
    env = DesktopEnv.__new__(DesktopEnv)
    env.cache_dir_base = str(tmp_path)

    env._set_task_info(
        {
            "id": "reference-task",
            "instruction": "Open the workbook.",
            "config": [],
        }
    )

    assert env.evaluator is None
    assert env.instruction == "Open the workbook."
    with pytest.raises(RuntimeError, match="does not define an evaluator"):
        env.evaluate()
