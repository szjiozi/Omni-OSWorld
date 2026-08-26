from __future__ import annotations

import hashlib
from pathlib import Path

from benchmark_construction.artifact_generation import (
    validate_artifact_blueprint,
)
from benchmark_construction.models import SkillRecord, SourceTask
from benchmark_construction.reference_annotation import (
    assemble_osworld_annotation_config,
    validate_annotation_blueprint,
)
from benchmark_construction.reference_applications import (
    get_reference_application,
)
from benchmark_construction.reference_generation import SkillSample
from benchmark_construction.reference_packages import (
    build_reference_package_request,
    validate_reference_package_response,
)
from benchmark_construction.reviewer_guide_generation import (
    ReviewerGuideJob,
    build_reviewer_guide_request,
)
from benchmark_construction.skill_extraction import build_skill_request
from benchmark_construction.reference_generation import load_skill_pool
from benchmark_construction.skill_readiness import eligible_skill_ids
from benchmark_construction.schema import load_schema, validate_payload


APP = "libreoffice_impress"


def _skill(index: int) -> SkillRecord:
    return SkillRecord(
        skill_id=f"source.skill-{index:02d}",
        app=APP,
        name=f"Impress skill {index}",
        procedure=("Select an editable object.", "Apply the requested operation."),
        efficiency_tip="Use the relevant sidebar control.",
        source_task_id="source",
        source_action_ids=(index - 1,),
    )


def _artifact_spec() -> dict:
    theme = {
        "primary_color": "2C5F2D",
        "secondary_color": "97BC62",
        "accent_color": "F2B134",
        "background_color": "F7F7F2",
        "title_font": "Liberation Sans",
        "body_font": "Liberation Sans",
    }
    return {
        "artifact_type": "pptx",
        "domain": "Community programs",
        "presentation_title": "Community Program Review",
        "slide_size": "wide",
        "theme": theme,
        "slides": [
            {
                "slide_number": 1,
                "purpose": "Introduce the review",
                "layout": "title_content",
                "object_plan": [
                    {
                        "semantic_id": "review_title",
                        "type": "text",
                        "purpose": "Presentation title",
                        "editable": True,
                    }
                ],
            },
            {
                "slide_number": 2,
                "purpose": "Compare participation",
                "layout": "data_story",
                "object_plan": [
                    {
                        "semantic_id": "participation_chart",
                        "type": "chart",
                        "purpose": "Participation comparison",
                        "editable": True,
                    }
                ],
            },
        ],
        "initial_state": ["Two coherent slides exist."],
        "must_not_be_completed": ["The requested formatting remains incomplete."],
        "generation_notes": ["Use editable static objects."],
    }


def _style() -> dict:
    return {
        "fill_color": "FFFFFF",
        "line_color": "D9E0E7",
        "text_color": "1F2937",
        "font_face": "Liberation Sans",
        "font_size": 18,
        "bold": False,
        "italic": False,
        "underline": False,
        "align": "left",
        "valign": "mid",
    }


def _content(**overrides) -> dict:
    content = {
        "text": None,
        "shape_kind": None,
        "image_kind": None,
        "rows": [],
        "categories": [],
        "series": [],
    }
    content.update(overrides)
    return content


def _package() -> dict:
    return {
        "reference_task_id": "reference-task-impress-r01-001",
        "app": APP,
        "task_instruction": "Format the title and update the comparison chart.",
        "required_skill_ids": ["source.skill-01", "source.skill-02"],
        "artifact_spec": _artifact_spec(),
        "operator_guide": {
            "recommended_demonstration": [
                {
                    "skill_id": "source.skill-01",
                    "operation_intent": "Format the title.",
                    "visible_success_signal": "The title has the requested style.",
                    "efficiency_tip": "Select the title once.",
                },
                {
                    "skill_id": "source.skill-02",
                    "operation_intent": "Update the chart.",
                    "visible_success_signal": "The chart shows the requested result.",
                    "efficiency_tip": "Edit the existing chart.",
                },
            ],
            "allowed_variation": "Equivalent English-UI paths are allowed.",
            "recording_start_state": "The presentation is open.",
            "recording_end_state": "The two requested edits are visible.",
        },
        "expected_incidental_operations": [],
    }


def _blueprint() -> dict:
    spec = _artifact_spec()
    return {
        "presentation_title": spec["presentation_title"],
        "slide_size": spec["slide_size"],
        "theme": spec["theme"],
        "slides": [
            {
                "slide_number": 1,
                "purpose": "Introduce the review",
                "background_color": "F7F7F2",
                "objects": [
                    {
                        "semantic_id": "review_title",
                        "type": "text",
                        "x": 0.7,
                        "y": 0.6,
                        "w": 7.0,
                        "h": 0.8,
                        "content": _content(text="Community Program Review"),
                        "style": _style(),
                    }
                ],
            },
            {
                "slide_number": 2,
                "purpose": "Compare participation",
                "background_color": "FFFFFF",
                "objects": [
                    {
                        "semantic_id": "participation_chart",
                        "type": "chart",
                        "x": 0.8,
                        "y": 1.4,
                        "w": 7.0,
                        "h": 4.5,
                        "content": _content(
                            categories=["Arts", "Sports"],
                            series=[{"name": "Participants", "values": [42, 58]}],
                        ),
                        "style": _style(),
                    }
                ],
            },
        ],
        "manual_setup_steps": [],
    }


def test_impress_profile_routes_app_contracts() -> None:
    profile = get_reference_application(APP)
    assert profile.artifact_type == "pptx"
    assert profile.packet_artifact_filename == "initial_artifact.pptx"
    assert profile.package_schema == "reference-package-impress-candidate.schema.json"


def test_impress_skill_and_package_requests_use_impress_prompts() -> None:
    source = SourceTask(
        task_id="source",
        app=APP,
        instruction="Move an image.",
        single_steps=("`CLICK` image", "`DRAG_TO` right side"),
    )
    skill_request = build_skill_request(source)
    assert skill_request.prompt_name == "extract_impress_skills.v1"

    sample = SkillSample(app=APP, skills=(_skill(1), _skill(2)))
    package_request = build_reference_package_request(sample, [source])
    assert package_request.prompt_name == "generate_impress_reference_package.v2"
    assert package_request.response_schema["properties"]["artifact_spec"][
        "properties"
    ]["artifact_type"]["const"] == "pptx"


def test_impress_package_and_artifact_blueprint_validate() -> None:
    sample = SkillSample(app=APP, skills=(_skill(1), _skill(2)))
    response = {
        "decision": "candidate",
        **_package(),
        "rejection_reason": "",
    }
    response.pop("reference_task_id")
    response.pop("app")
    validate_reference_package_response(sample, response)
    validate_artifact_blueprint(_package(), _blueprint())


def test_impress_blueprint_schema_allows_thirteen_editable_objects() -> None:
    blueprint = _blueprint()
    template = blueprint["slides"][0]["objects"][0]
    blueprint["slides"][0]["objects"] = [
        {
            **template,
            "semantic_id": f"editable_object_{index}",
            "x": 0.1 * index,
        }
        for index in range(13)
    ]

    validate_payload(
        blueprint,
        load_schema("impress-artifact-blueprint.schema.json"),
    )


def test_impress_annotation_config_uses_pptx(tmp_path: Path) -> None:
    artifact = tmp_path / "initial_artifact.pptx"
    artifact.write_bytes(b"PK\x03\x04synthetic")
    digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
    package = _package()
    manifest = {
        "reference_task_id": package["reference_task_id"],
        "artifact_path": artifact.name,
        "artifact_sha256": digest,
        "manual_setup_required": False,
        "manual_setup_steps": [],
    }
    blueprint = {
        "snapshot": APP,
        "artifact_slot": "initial_artifact",
        "guest_filename": "community_review.pptx",
        "open_after_upload": True,
        "ready_state_checks": ["Confirm the two-slide presentation is open."],
        "setup_notes": [],
    }
    validate_annotation_blueprint(blueprint, expected_app=APP)
    config = assemble_osworld_annotation_config(
        package, manifest, blueprint, repo_root=tmp_path
    )
    assert config["snapshot"] == APP
    assert config["related_apps"] == [APP]
    assert config["config"][0]["parameters"]["files"][0]["path"].endswith(
        ".pptx"
    )


def test_impress_reviewer_guide_request_uses_impress_prompt(tmp_path: Path) -> None:
    detail = tmp_path / "TASK_DETAIL.md"
    detail.write_text("# Detail\n\nImpress task detail.\n")
    job = ReviewerGuideJob(
        reference_task_id="reference-task-impress-r01-001",
        required_skill_ids=("source.skill-01", "source.skill-02"),
        task_detail_path=detail,
        app=APP,
    )
    request = build_reviewer_guide_request(job, detail.read_text())
    assert request.prompt_name == "generate_impress_reviewer_guide.v3"


def test_impress_pilot_readiness_keeps_deferred_skills_unselected() -> None:
    root = Path("evaluation_examples/expert_skill_learning/impress_full_v1")
    skills = load_skill_pool(root / "generated/skill_pool.json", expected_app=APP)
    eligible = eligible_skill_ids(
        root / "skill_readiness_policy.json",
        skills,
        expected_app=APP,
        statuses=["pilot_static"],
    )
    assert len(skills) == 66
    assert len(eligible) == 46
    assert "c59742c0-4323-4b9d-8a02-723c251deaa0.skill-01" not in eligible
    assert "04578141-1d42-4146-b9cf-6fab4ce5fd74.skill-01" in eligible
