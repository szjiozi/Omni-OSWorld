import json
from argparse import Namespace

import pytest

from mm_agents.qwen3vl_agent import (
    Qwen3VLAgent,
    _build_skill_context,
    _recent_action_lines,
)
from scripts.python.run_multienv_qwen3vl import validate_condition


def _artifact():
    return {
        "schema_version": "1.0",
        "status": "engineering_pilot",
        "app": "libreoffice_calc",
        "model": "qwen3.7-plus-2026-05-26",
        "private_provenance": "must-not-enter-the-prompt",
        "skills": [
            {
                "skill_id": "induced-skill-01",
                "name": "Fill a contiguous range",
                "when_to_use": "When the same formula pattern applies to a range.",
                "procedure": ["Select the source cell.", "Drag the fill handle."],
                "efficiency_tip": "Use one drag instead of repeated entry.",
                "verification": "Inspect the destination formulas.",
                "evidence": [
                    {
                        "video_id": "reference-task-private",
                        "start_seconds": 1,
                        "end_seconds": 2,
                        "observation": "Private reference detail.",
                    }
                ],
            }
        ],
    }


def test_recent_action_lines_keeps_the_latest_window():
    assert _recent_action_lines(["a", "b", "c", "d"], 2) == [
        "Step 3: c",
        "Step 4: d",
    ]
    assert _recent_action_lines(["a"], 0) == []


def test_skill_context_excludes_provenance_and_reference_evidence():
    context = _build_skill_context(_artifact())
    skills = json.loads(context)

    assert skills[0]["name"] == "Fill a contiguous range"
    assert "evidence" not in skills[0]
    assert "private_provenance" not in context
    assert "reference-task-private" not in context


def test_skill_context_rejects_non_pilot_artifact():
    artifact = _artifact()
    artifact["status"] = "production"

    with pytest.raises(ValueError, match="engineering_pilot"):
        _build_skill_context(artifact)


def test_agent_records_usage_and_accepts_vm_ip_on_reset():
    agent = Qwen3VLAgent(skill_artifact=_artifact())
    response = {
        "request_id": "request-1",
        "usage": {"input_tokens": 1000, "output_tokens": 100},
    }

    agent._record_call_metadata(response, agent.model, "dashscope")
    assert agent.last_call_metadata["request_id"] == "request-1"
    assert agent.model_usage == {
        "calls": 1,
        "input_tokens": 1000,
        "output_tokens": 100,
        "estimated_cost_cny": 0.0028,
    }

    agent.reset(vm_ip="127.0.0.1")
    assert agent.model_usage["calls"] == 0
    assert agent.last_call_metadata == {}


def test_runner_condition_requires_exactly_one_skill_artifact_mode():
    common = {"history_n": 4, "max_steps": 50}
    validate_condition(
        Namespace(condition="baseline", skill_artifact=None, **common)
    )
    validate_condition(
        Namespace(
            condition="learned_skills",
            skill_artifact="learned_skills.json",
            **common,
        )
    )

    with pytest.raises(ValueError, match="must not receive"):
        validate_condition(
            Namespace(
                condition="baseline",
                skill_artifact="learned_skills.json",
                **common,
            )
        )
    with pytest.raises(ValueError, match="requires"):
        validate_condition(
            Namespace(condition="learned_skills", skill_artifact=None, **common)
        )
