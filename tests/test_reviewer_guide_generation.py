import json

import pytest

from benchmark_construction.reviewer_guide_generation import (
    ReviewerGuideJob,
    ReviewerGuideResult,
    build_reviewer_guide_request,
    load_reviewer_guides,
    sha256_text,
    validate_reviewer_guide,
    write_reviewer_guides,
)


def _guide(task_id="reference-task-1"):
    return {
        "reference_task_id": task_id,
        "language": "zh-CN",
        "overview": "使用 Calc 高效完成新的工作簿任务。",
        "starting_state_checks": ["确认初始工作表和数据已经显示。"],
        "steps": [
            {
                "step_number": 1,
                "title": "完成公式",
                "instructions": ["选择目标单元格并输入所需公式。"],
                "skill_ids": ["skill-1"],
                "efficiency_tip": "先完成第一行，再使用填充柄。",
                "visible_success_signal": "结果列显示正确数值。",
            },
            {
                "step_number": 2,
                "title": "检查结果",
                "instructions": ["检查结果区域没有错误值。"],
                "skill_ids": ["skill-2"],
                "efficiency_tip": "一次检查完整区域。",
                "visible_success_signal": "所有目标单元格都有结果。",
            },
        ],
        "final_verification": ["确认任务要求的结果全部存在。"],
    }


def test_reviewer_guide_request_uses_complete_task_detail(tmp_path):
    detail_path = tmp_path / "TASK_DETAIL.md"
    detail_path.write_text(
        "# Full detail\n\n## Expected incidental operations\n\nHidden from final view.",
        encoding="utf-8",
    )
    job = ReviewerGuideJob(
        "reference-task-1", ("skill-1", "skill-2"), detail_path
    )

    request = build_reviewer_guide_request(
        job, detail_path.read_text(encoding="utf-8")
    )

    assert "# Full detail" in request.user_prompt
    assert "Expected incidental operations" in request.user_prompt
    assert '"skill-1"' in request.user_prompt
    assert "provenance for human similarity review only" in request.system_prompt
    assert "annotation environment uses the English LibreOffice UI" in request.system_prompt
    assert "点击 `Format`，选择 `Format Cells...`" in request.system_prompt
    assert request.prompt_name == "generate_reviewer_guide.v2"


def test_reviewer_guide_validation_requires_exact_skill_coverage():
    guide = _guide()
    validate_reviewer_guide("reference-task-1", ["skill-1", "skill-2"], guide)

    guide["steps"][1]["skill_ids"] = []
    with pytest.raises(ValueError, match="does not cover required skills"):
        validate_reviewer_guide(
            "reference-task-1", ["skill-1", "skill-2"], guide
        )


def test_reviewer_guide_rejects_translated_visible_ui_labels():
    guide = _guide()
    guide["steps"][0]["instructions"] = [
        "右键单击选区，然后选择“设置单元格格式”。"
    ]

    with pytest.raises(ValueError, match="Chinese visible UI label"):
        validate_reviewer_guide(
            "reference-task-1", ["skill-1", "skill-2"], guide
        )

    guide["steps"][0]["instructions"] = [
        "右键单击选区，然后选择 `Format Cells...`。"
    ]
    validate_reviewer_guide("reference-task-1", ["skill-1", "skill-2"], guide)


def test_reviewer_guide_round_trip_records_task_detail_hash(tmp_path):
    detail = "# TASK_DETAIL\n"
    result = ReviewerGuideResult(
        reference_task_id="reference-task-1",
        task_detail_sha256=sha256_text(detail),
        guide=_guide(),
        request_id="request-1",
        prompt_sha256="1" * 64,
        model="test-model",
        input_tokens=10,
        output_tokens=20,
        estimated_cost_usd=0.01,
    )
    output = tmp_path / "reviewer_guides.json"

    write_reviewer_guides(output, [result])
    loaded = load_reviewer_guides(output)

    assert loaded["reference-task-1"]["task_detail_sha256"] == sha256_text(
        detail
    )
    assert json.loads(output.read_text(encoding="utf-8"))["totals"] == {
        "calls": 1,
        "input_tokens": 10,
        "output_tokens": 20,
        "estimated_cost_usd": 0.01,
        "pricing_complete": True,
    }
