from pathlib import Path

from scripts.python.manual_explore import REPO_ROOT, _load_task


def test_load_phase0_task_resolves_host_local_paths():
    task = _load_task(
        Path(
            "evaluation_examples/video_learning/examples/libreoffice_impress/"
            "0f4e50c1-0c2c-4f83-9ea9-48f7b67e1001.json"
        )
    )

    uploaded = task["config"][0]["parameters"]["files"]
    assert all(Path(item["local_path"]).is_absolute() for item in uploaded)
    assert Path(task["evaluator"]["expected"]["path"]).is_absolute()
    assert str(REPO_ROOT) in uploaded[0]["local_path"]
