import hashlib
import json
from pathlib import Path

import pytest

from benchmark_construction.osworld_human import prepare_pilot_suite
from benchmark_construction.osworld_human_scoring import compute_wes, score_pilot


def _raw_task(task_id="task-1"):
    return {
        "id": task_id,
        "snapshot": "libreoffice_calc",
        "instruction": "Original OSWorld instruction.",
        "config": [],
        "evaluator": {"func": "compare_table"},
        "human-ground-truth": {
            "single-action": ["click", "type", "save"],
            "grouped-action": [["click", "type"], ["save"]],
        },
    }


def test_prepare_pilot_suite_verifies_sha_and_records_local_instruction_diff(tmp_path):
    raw = json.dumps(_raw_task(), separators=(",", ":")).encode()
    source_manifest = {
        "pilot_id": "pilot",
        "app": "libreoffice_calc",
        "source_repository": "https://github.com/WukLab/osworld-human",
        "source_commit": "abc123",
        "tasks": [
            {
                "task_id": "task-1",
                "source_file": "libreoffice_calc/task-1.json",
                "source_sha256": hashlib.sha256(raw).hexdigest(),
                "instruction": "Original OSWorld instruction.",
                "single_actions": ["click", "type", "save"],
            }
        ],
    }
    source_path = tmp_path / "source.json"
    source_path.write_text(json.dumps(source_manifest), encoding="utf-8")
    local_root = tmp_path / "local"
    local_path = local_root / "libreoffice_calc/task-1.json"
    local_path.parent.mkdir(parents=True)
    local_task = _raw_task()
    local_task.pop("human-ground-truth")
    local_task["instruction"] = "Locally clarified instruction."
    local_path.write_text(json.dumps(local_task), encoding="utf-8")

    manifest = prepare_pilot_suite(
        source_path,
        tmp_path / "output",
        local_osworld_task_root=local_root,
        fetch=lambda _url: raw,
    )

    assert manifest["status"] == "engineering_pilot"
    assert manifest["tasks"][0]["single_action_count"] == 3
    assert manifest["tasks"][0]["grouped_action_count"] == 2
    assert manifest["tasks"][0]["local_osworld_differing_fields"] == [
        "instruction"
    ]
    materialized = Path(manifest["tasks"][0]["materialized_path"])
    assert materialized.read_bytes() == raw


def test_prepare_pilot_suite_rejects_unpinned_payload(tmp_path):
    raw = json.dumps(_raw_task()).encode()
    source_path = tmp_path / "source.json"
    source_path.write_text(
        json.dumps(
            {
                "pilot_id": "pilot",
                "app": "libreoffice_calc",
                "source_repository": "repo",
                "source_commit": "commit",
                "tasks": [
                    {
                        "task_id": "task-1",
                        "source_file": "libreoffice_calc/task-1.json",
                        "source_sha256": "0" * 64,
                        "instruction": "Original OSWorld instruction.",
                        "single_actions": ["click", "type", "save"],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="SHA256 mismatch"):
        prepare_pilot_suite(source_path, tmp_path / "output", fetch=lambda _: raw)


def test_compute_wes_matches_official_task_formula():
    assert compute_wes(
        result=1.0, human_steps=10, agent_steps=20, max_steps=50
    ) == (0.5, 0.0, 0.5)
    assert compute_wes(
        result=0.0, human_steps=10, agent_steps=20, max_steps=50
    ) == (0.0, -0.4, -0.4)


def test_score_pilot_uses_only_traj_jsonl_and_subset_denominator(tmp_path):
    task_root = tmp_path / "tasks"
    task_path = task_root / "examples/libreoffice_calc/task-1.json"
    task_path.parent.mkdir(parents=True)
    task_path.write_text(json.dumps(_raw_task()), encoding="utf-8")
    suite_path = task_root / "suite.json"
    suite_path.write_text(
        json.dumps({"libreoffice_calc": ["task-1"]}), encoding="utf-8"
    )
    result_dir = tmp_path / "runs/libreoffice_calc/task-1"
    result_dir.mkdir(parents=True)
    result_dir.joinpath("traj.jsonl").write_text(
        "\n".join(json.dumps({"step": i}) for i in range(1, 7)) + "\n",
        encoding="utf-8",
    )
    result_dir.joinpath("events.jsonl").write_text(
        "\n".join(json.dumps({"event": i}) for i in range(100)),
        encoding="utf-8",
    )
    result_dir.joinpath("result.txt").write_text("1.0\n", encoding="utf-8")

    report = score_pilot(
        task_root=task_root,
        suite_path=suite_path,
        run_root=tmp_path / "runs",
        max_steps_scoring=50,
    )

    assert report["task_count"] == 1
    assert report["aggregate"]["osworld_score"] == 1.0
    assert report["aggregate"]["single_action_wes_plus"] == 0.5
    assert report["aggregate"]["grouped_action_wes_plus"] == pytest.approx(1 / 3)
    assert report["tasks"][0]["agent_steps"] == 6
