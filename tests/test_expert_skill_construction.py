import asyncio
import json
from pathlib import Path
import re
from types import SimpleNamespace

import pytest

from benchmark_construction.llm import (
    JSONRequest,
    JSONResult,
    LLMConfig,
    MediaInput,
    OpenAICompatibleAsyncClient,
    UnsupportedMediaError,
)
from benchmark_construction.artifact_generation import (
    load_artifact_blueprints,
    validate_artifact_blueprint,
)
from benchmark_construction.models import SourceTask
from benchmark_construction.osworld_human import (
    load_source_manifest,
    load_source_task,
    resolve_task_paths,
    verify_manifest_sources,
)
from benchmark_construction.pricing import PricingTable, TokenUsage
from benchmark_construction.reference_generation import (
    SeededCoverageSampler,
    SkillSample,
    build_reference_task_request,
    generate_reference_tasks,
    load_skill_pool,
    validate_reference_response,
)
from benchmark_construction.reference_packages import (
    SkillSample as PackageSkillSample,
    build_reference_package_request,
    validate_reference_package_response,
)
from benchmark_construction.reference_review import (
    compute_review_state,
    load_reference_reviews,
    write_reference_review_template,
)
from benchmark_construction.schema import load_schema
from benchmark_construction.semantic_similarity import (
    EmbeddingBatchResult,
    cosine_similarity,
    score_semantic_similarity,
)
from benchmark_construction.skill_extraction import (
    attach_skill_provenance,
    build_skill_request,
)


def _source_task() -> SourceTask:
    return SourceTask(
        task_id="calc-task-1",
        app="libreoffice_calc",
        instruction="Fill the totals column using a formula.",
        single_steps=(
            "`CLICK` cell J2",
            "`TYPE` =Sheet1.A2*Sheet1.I2",
            "`DRAG_TO` the fill handle down the column",
        ),
    )


def test_source_task_prompt_payload_is_strictly_bounded():
    task = _source_task()

    assert task.prompt_payload() == {
        "instruction": task.instruction,
        "single_steps": list(task.single_steps),
    }
    assert "task_id" not in task.prompt_payload()
    assert "app" not in task.prompt_payload()


def test_calc_reference_guidance_distinguishes_sheet_column_and_row_markers():
    request = build_skill_request(_source_task())

    assert "`$Sheet1.A2` fixes the source sheet" in request.system_prompt
    assert "`$Sheet1.$A2` additionally fixes column A" in request.system_prompt
    assert "does not rename the worksheet" in request.system_prompt
    assert "exactly one independently reusable application technique" in request.system_prompt
    assert "formula construction, number formatting" in request.system_prompt
    assert "indices are non-contiguous" in request.system_prompt
    assert "Each source action index may belong to at most one skill" in request.system_prompt
    assert "Atomic does not mean turning every source action into a skill" in request.system_prompt
    assert "clicking OK" in request.system_prompt
    assert "Every skill name must describe an app-general technique" in request.system_prompt


def test_osworld_human_loader_reads_only_required_fields(tmp_path):
    task_path = tmp_path / "libreoffice_calc" / "calc-task-1.json"
    task_path.parent.mkdir()
    task_path.write_text(
        json.dumps(
            {
                "id": "calc-task-1",
                "snapshot": "libreoffice_calc",
                "instruction": "Format the selected cells.",
                "config": [{"secret_setup_detail": "must not reach the prompt"}],
                "evaluator": {"hidden": "must not reach the prompt"},
                "human-ground-truth": {
                    "single-action": ["`CLICK` Format", "`CLICK` Currency"],
                    "grouped-action": [["grouped sentinel"]],
                },
            }
        ),
        encoding="utf-8",
    )

    resolved = resolve_task_paths(tmp_path, ["calc-task-1"])
    task = load_source_task(resolved[0], expected_app="libreoffice_calc")
    request = build_skill_request(task)

    assert task.task_id == "calc-task-1"
    assert task.single_steps == ("`CLICK` Format", "`CLICK` Currency")
    assert "secret_setup_detail" not in request.user_prompt
    assert "grouped sentinel" not in request.user_prompt
    assert "hidden" not in request.user_prompt
    assert "calc-task-1" not in request.user_prompt


def test_frozen_source_manifest_is_self_contained_and_matches_raw_sources():
    repo_root = Path(__file__).resolve().parents[1]
    manifest = (
        repo_root
        / "evaluation_examples"
        / "expert_skill_learning"
        / "pilot"
        / "source_tasks.json"
    )

    tasks = load_source_manifest(manifest, expected_app="libreoffice_calc")

    assert len(tasks) == 3
    assert sum(len(task.single_steps) for task in tasks) == 40
    assert all(task.prompt_payload()["single_steps"] for task in tasks)
    raw_root = Path("/private/tmp/osworld-human-inspect")
    if raw_root.exists():
        verify_manifest_sources(manifest, raw_root)


def test_skill_provenance_is_injected_locally_and_action_ids_are_checked():
    task = _source_task()
    response = {
        "skills": [
            {
                "name": "Fill a relative formula down a column",
                "procedure": [
                    "Enter the formula in the first destination row.",
                    "For example, use =Sheet1.A2*Sheet1.I2 in J2, then drag "
                    "the fill handle so the row number advances automatically.",
                ],
                "efficiency_tip": "Verify one formula, then fill the remaining rows.",
                "action_ids": [2, 1],
            }
        ]
    }

    records = attach_skill_provenance(task, response)

    assert len(records) == 1
    assert records[0].skill_id == "calc-task-1.skill-01"
    assert records[0].source_task_id == "calc-task-1"
    assert records[0].source_action_ids == (1, 2)
    assert "Efficiency tip:" in records[0].description

    response["skills"][0]["action_ids"] = [3]
    with pytest.raises(ValueError, match="only has 3 actions"):
        attach_skill_provenance(task, response)


def test_skill_provenance_rejects_action_ids_shared_by_multiple_skills():
    task = _source_task()
    response = {
        "skills": [
            {
                "name": "Build a formula",
                "procedure": ["Enter a relative formula, such as =A1+B1."],
                "efficiency_tip": "Enter it once.",
                "action_ids": [0, 1],
            },
            {
                "name": "Fill a formula",
                "procedure": ["Drag the fill handle, such as from C1 to C10."],
                "efficiency_tip": "Fill the range in one drag.",
                "action_ids": [1, 2],
            },
        ]
    }

    with pytest.raises(ValueError, match="multiple skills: \\[1\\]"):
        attach_skill_provenance(task, response)


def test_all_expert_skill_json_schemas_are_valid():
    for name in (
        "skill-extraction-response.schema.json",
        "skill-record.schema.json",
        "reference-task-candidate.schema.json",
        "reference-task-review.schema.json",
        "reference-package-candidate.schema.json",
        "reference-package-review.schema.json",
        "calc-artifact-blueprint.schema.json",
    ):
        assert load_schema(name)["$schema"].endswith("2020-12/schema")


def test_frozen_pilot_skill_pool_partitions_all_source_actions():
    pilot_root = (
        Path(__file__).resolve().parents[1]
        / "evaluation_examples"
        / "expert_skill_learning"
        / "pilot"
    )
    source_manifest = json.loads(
        (pilot_root / "source_tasks.json").read_text(encoding="utf-8")
    )
    pool = json.loads((pilot_root / "skill_pool.json").read_text(encoding="utf-8"))
    skills = pool["skills"]

    assert len(skills) == 12
    assert all(skill["app"] == "libreoffice_calc" for skill in skills)
    assert all(len(skill["procedure"]) >= 2 for skill in skills)
    assert all(
        re.search(r"for example|such as", " ".join(skill["procedure"]), re.I)
        for skill in skills
    )
    assert not any(
        re.search(r"gross profit|weekend|invoice", skill["name"], re.I)
        for skill in skills
    )

    expected_groups = {
        "035f41ba-6653-43ab-aa63-c86d449d62e5": [
            [0, 1],
            [2],
            [3, 4, 9, 10],
            [5],
            [8],
        ],
        "8b1ce5f2-59d2-4dcc-b0b0-666a714b9a14": [
            [0, 1, 2, 3, 4, 5, 6, 7, 14],
            [8, 9, 10, 11, 12, 13],
        ],
        "1954cced-e748-45c4-9c26-9855b97fbc5e": [
            [0, 1, 2],
            [3, 4],
            [5, 6],
            [7, 8, 9, 10],
            [11, 12, 13],
        ],
    }
    expected_unassigned = {
        "035f41ba-6653-43ab-aa63-c86d449d62e5": [6, 7],
        "8b1ce5f2-59d2-4dcc-b0b0-666a714b9a14": [],
        "1954cced-e748-45c4-9c26-9855b97fbc5e": [],
    }

    for task in source_manifest["tasks"]:
        task_skills = [
            skill
            for skill in skills
            if skill["source"]["task_id"] == task["task_id"]
        ]
        groups = [skill["source"]["action_ids"] for skill in task_skills]
        action_ids = [action_id for group in groups for action_id in group]
        assert groups == expected_groups[task["task_id"]]
        assert len(action_ids) == len(set(action_ids))
        assert sorted(
            set(range(task["single_action_count"])).difference(action_ids)
        ) == expected_unassigned[task["task_id"]]


def _pilot_construction_inputs():
    pilot_root = (
        Path(__file__).resolve().parents[1]
        / "evaluation_examples"
        / "expert_skill_learning"
        / "pilot"
    )
    skills = load_skill_pool(
        pilot_root / "skill_pool.json", expected_app="libreoffice_calc"
    )
    tasks = load_source_manifest(
        pilot_root / "source_tasks.json", expected_app="libreoffice_calc"
    )
    return skills, tasks


def test_seeded_reference_sampler_is_reproducible_and_covers_input_skills():
    skills, _ = _pilot_construction_inputs()
    all_ids = {skill.skill_id for skill in skills}
    first = SeededCoverageSampler(skills, seed=20260804)
    second = SeededCoverageSampler(skills, seed=20260804)

    first_groups = [sample.skill_ids for sample in first.sample_wave(all_ids, limit=20)]
    second_groups = [
        sample.skill_ids for sample in second.sample_wave(all_ids, limit=20)
    ]

    assert first_groups == second_groups
    assert first_groups == [
        (
            "035f41ba-6653-43ab-aa63-c86d449d62e5.skill-04",
            "035f41ba-6653-43ab-aa63-c86d449d62e5.skill-05",
            "1954cced-e748-45c4-9c26-9855b97fbc5e.skill-01",
        ),
        (
            "035f41ba-6653-43ab-aa63-c86d449d62e5.skill-02",
            "1954cced-e748-45c4-9c26-9855b97fbc5e.skill-02",
            "1954cced-e748-45c4-9c26-9855b97fbc5e.skill-04",
            "035f41ba-6653-43ab-aa63-c86d449d62e5.skill-03",
            "8b1ce5f2-59d2-4dcc-b0b0-666a714b9a14.skill-02",
        ),
        (
            "8b1ce5f2-59d2-4dcc-b0b0-666a714b9a14.skill-01",
            "1954cced-e748-45c4-9c26-9855b97fbc5e.skill-03",
            "1954cced-e748-45c4-9c26-9855b97fbc5e.skill-05",
            "035f41ba-6653-43ab-aa63-c86d449d62e5.skill-01",
            "8b1ce5f2-59d2-4dcc-b0b0-666a714b9a14.skill-02",
        ),
    ]
    assert all(2 <= len(group) <= 5 for group in first_groups)
    assert set().union(*(set(group) for group in first_groups)) == all_ids


def test_reference_prompt_separates_sampled_cards_from_unsampled_constraints():
    skills, tasks = _pilot_construction_inputs()
    sample = SkillSample(app="libreoffice_calc", skills=tuple(skills[:2]))

    request = build_reference_task_request(sample, tasks, skills)

    assert skills[0].skill_id in request.user_prompt
    assert skills[1].skill_id in request.user_prompt
    assert skills[2].skill_id in request.user_prompt
    assert skills[2].name in request.user_prompt
    assert "Gross profit column" in request.user_prompt
    assert "required_skill_ids must contain exactly" in request.system_prompt
    assert "not a step-by-step UI solution" in request.system_prompt
    assert "Do not make any listed unsampled skill" in request.system_prompt


def _reference_package_response(skills):
    skill_ids = [skill.skill_id for skill in skills]
    return {
        "decision": "candidate",
        "task_instruction": "Prepare the synthetic operations workbook for review.",
        "required_skill_ids": skill_ids,
        "artifact_spec": {
            "artifact_type": "xlsx",
            "domain": "operations",
            "workbook_title": "Operations Review",
            "sheets": [
                {
                    "name": "Records",
                    "purpose": "Source records",
                    "columns": [
                        {"name": "Record ID", "data_type": "text"},
                        {"name": "Amount", "data_type": "currency"},
                    ],
                    "row_count": 5,
                }
            ],
            "initial_state": ["Five source records are present."],
            "must_not_be_completed": ["The target operation is incomplete."],
            "generation_notes": ["Use synthetic identifiers."],
        },
        "operator_guide": {
            "recommended_demonstration": [
                {
                    "skill_id": skill.skill_id,
                    "operation_intent": f"Demonstrate {skill.name}.",
                    "visible_success_signal": "The intended worksheet change is visible.",
                    "efficiency_tip": skill.efficiency_tip,
                }
                for skill in skills
            ],
            "allowed_variation": "Equivalent efficient methods are allowed.",
            "recording_start_state": "The initial workbook is open.",
            "recording_end_state": "All required skills are visible.",
        },
        "expected_incidental_operations": [
            {
                "operation": "Select the target range",
                "reason": "The sampled operation needs a target.",
                "category": "scaffolding",
            }
        ],
        "rejection_reason": "",
    }


def test_reference_package_prompt_and_local_skill_guide_validation():
    skills, tasks = _pilot_construction_inputs()
    sample = PackageSkillSample(
        app="libreoffice_calc", skills=tuple(skills[:2])
    )

    request = build_reference_package_request(sample, tasks)
    response = _reference_package_response(skills[:2])
    validate_reference_package_response(sample, response)

    assert "Sampled mandatory skill cards" in request.user_prompt
    assert "Other pool skills" not in request.user_prompt
    assert "small number of incidental" in request.system_prompt
    assert "artifact_spec" in request.system_prompt

    response["operator_guide"]["recommended_demonstration"][1][
        "skill_id"
    ] = skills[2].skill_id
    with pytest.raises(ValueError, match="exactly one item"):
        validate_reference_package_response(sample, response)


class _FakeEmbeddingClient:
    async def embed(self, texts):
        vectors = []
        for index, _ in enumerate(texts):
            vectors.append((1.0, float(index), 0.5))
        return EmbeddingBatchResult(
            request_id="embedding-request",
            model="fake-embedding-model",
            vectors=tuple(vectors),
            input_tokens=42,
            estimated_cost_usd=0.000001,
        )


def test_embedding_cosine_similarity_and_source_ranking():
    _, tasks = _pilot_construction_inputs()

    reports, batch = asyncio.run(
        score_semantic_similarity(
            ["Prepare a workbook report."], tasks, _FakeEmbeddingClient()
        )
    )

    assert cosine_similarity([1, 0], [1, 0]) == pytest.approx(1.0)
    assert batch.input_tokens == 42
    assert reports[0]["model"] == "fake-embedding-model"
    assert len(reports[0]["by_source_task"]) == 3


def test_review_state_recomputes_global_approved_coverage_after_rejection():
    skills, _ = _pilot_construction_inputs()
    packages = [
        {
            "reference_task_id": "task-a",
            "app": "libreoffice_calc",
            "required_skill_ids": [skills[0].skill_id, skills[1].skill_id],
        },
        {
            "reference_task_id": "task-b",
            "app": "libreoffice_calc",
            "required_skill_ids": [skills[1].skill_id, skills[2].skill_id],
        },
        {
            "reference_task_id": "task-c",
            "app": "libreoffice_calc",
            "required_skill_ids": [skills[3].skill_id, skills[4].skill_id],
        },
    ]
    reviews = [
        {
            "reference_task_id": "task-a",
            "decision": "rejected",
            "reason_codes": ["unnatural_combination"],
            "revision_instructions": [],
            "reviewer": "reviewer-1",
            "notes": "Regenerate this combination.",
        },
        {
            "reference_task_id": "task-b",
            "decision": "approved",
            "reason_codes": [],
            "revision_instructions": [],
            "reviewer": "reviewer-1",
            "notes": "Natural and feasible.",
        },
        {
            "reference_task_id": "task-c",
            "decision": "revision_requested",
            "reason_codes": ["artifact_too_complex"],
            "revision_instructions": ["Use one source sheet only."],
            "reviewer": "reviewer-1",
            "notes": "Keep the same skills but simplify the artifact.",
        },
    ]

    state = compute_review_state(skills, packages, reviews)

    assert skills[1].skill_id in state.approved_skill_ids
    assert skills[2].skill_id in state.approved_skill_ids
    assert skills[0].skill_id in state.unresolved_skill_ids
    assert state.blocked_groups == (
        (skills[0].skill_id, skills[1].skill_id),
    )
    assert state.revision_reference_task_ids == ("task-c",)
    assert state.revisions[0].parent_reference_task_id == "task-c"
    assert state.revisions[0].feedback == ("Use one source sheet only.",)


def test_review_template_prefills_fields_and_treats_blanks_as_pending(tmp_path):
    packages = [
        {"reference_task_id": "task-a"},
        {"reference_task_id": "task-b"},
    ]
    review_path = tmp_path / "reviews.json"

    assert write_reference_review_template(review_path, packages) == 2
    document = json.loads(review_path.read_text(encoding="utf-8"))
    assert document["reviews"] == [
        {
            "reference_task_id": "task-a",
            "decision": "",
            "reason_codes": [],
            "revision_instructions": [],
            "reviewer": "",
            "notes": "",
        },
        {
            "reference_task_id": "task-b",
            "decision": "",
            "reason_codes": [],
            "revision_instructions": [],
            "reviewer": "",
            "notes": "",
        },
    ]
    assert load_reference_reviews(review_path) == []

    document["reviews"][0].update(
        {
            "decision": "approved",
            "reviewer": "reviewer-1",
            "notes": "Keep this package.",
        }
    )
    review_path.write_text(json.dumps(document), encoding="utf-8")
    completed = load_reference_reviews(review_path)
    assert [review["reference_task_id"] for review in completed] == ["task-a"]
    assert write_reference_review_template(review_path, packages) == 0


def test_artifact_blueprint_matches_package_spec_and_preserves_incomplete_state():
    skills, _ = _pilot_construction_inputs()
    package = _reference_package_response(skills[:2])
    package["reference_task_id"] = "task-a"
    blueprint = {
        "workbook_title": "Operations Review",
        "sheets": [
            {
                "name": "Records",
                "headers": ["Record ID", "Amount"],
                "column_types": ["text", "currency"],
                "column_number_formats": ["@", "$#,##0.00"],
                "rows": [
                    {"values": [f"REC-{index:03d}", str(index * 10)]}
                    for index in range(1, 6)
                ],
                "formulas": [],
                "freeze_header_row": True,
                "autofilter_range": None,
            }
        ],
        "manual_setup_steps": [],
    }

    validate_artifact_blueprint(package, blueprint)
    blueprint["sheets"][0]["rows"][0]["values"] = ["REC-001"]
    with pytest.raises(ValueError, match="wrong width"):
        validate_artifact_blueprint(package, blueprint)


def test_frozen_artifact_blueprints_can_be_loaded_without_llm(tmp_path):
    blueprint_path = tmp_path / "blueprints.json"
    blueprint_path.write_text(
        json.dumps(
            {
                "blueprints": [
                    {
                        "reference_task_id": "task-a",
                        "blueprint": {
                            "workbook_title": "Operations Review",
                            "sheets": [
                                {
                                    "name": "Records",
                                    "headers": ["Record ID"],
                                    "column_types": ["text"],
                                    "column_number_formats": ["@"],
                                    "rows": [
                                        {"values": [f"REC-{index:03d}"]}
                                        for index in range(1, 6)
                                    ],
                                    "formulas": [],
                                    "freeze_header_row": True,
                                    "autofilter_range": None,
                                }
                            ],
                            "manual_setup_steps": [],
                        },
                        "generation": {
                            "request_id": "req-a",
                            "prompt_sha256": "abc",
                            "model": "test-model",
                            "input_tokens": 1,
                            "output_tokens": 2,
                            "estimated_cost_usd": 0.001,
                        },
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    results = load_artifact_blueprints(blueprint_path)
    assert results[0].reference_task_id == "task-a"
    assert results[0].blueprint["sheets"][0]["autofilter_range"] is None


def test_task_four_keeps_hourly_rate_plain_for_currency_skill_demo():
    pilot_root = (
        Path(__file__).resolve().parents[1]
        / "evaluation_examples"
        / "expert_skill_learning"
        / "pilot"
    )
    results = load_artifact_blueprints(pilot_root / "artifact_blueprints.json")
    task = next(
        item
        for item in results
        if item.reference_task_id == "reference-task-r01-004"
    )
    service_log = task.blueprint["sheets"][0]

    assert service_log["headers"][4:6] == ["Hourly Rate", "Billed Charge"]
    assert service_log["column_number_formats"][4:6] == ["0.00", "General"]


def test_reference_response_must_return_exact_sampled_skill_ids():
    skills, _ = _pilot_construction_inputs()
    sample = SkillSample(app="libreoffice_calc", skills=tuple(skills[:2]))
    response = {
        "decision": "candidate",
        "instruction": (
            "Create a small worksheet report and format its calculated result."
        ),
        "required_skill_ids": [skills[0].skill_id, skills[2].skill_id],
        "rejection_reason": "",
    }

    with pytest.raises(ValueError, match="missing=.*unexpected="):
        validate_reference_response(sample, response)


class _AcceptingReferenceClient:
    async def generate_many(self, requests):
        results = []
        for request in requests:
            sampled_section = request.user_prompt.split(
                "Sampled skill cards:\n", 1
            )[1].split("\n\nOther pool skills", 1)[0]
            skill_ids = re.findall(r'"skill_id": "([^"]+)"', sampled_section)
            response = {
                "decision": "candidate",
                "instruction": (
                    "Prepare a project-tracking workbook that demonstrates all required "
                    "spreadsheet operations on a newly chosen artifact."
                ),
                "required_skill_ids": skill_ids,
                "rejection_reason": "",
            }
            results.append(
                JSONResult(
                    request_id=request.request_id,
                    model="fake-construction-model",
                    data=response,
                    usage=TokenUsage(input_tokens=100, output_tokens=20),
                    estimated_cost_usd=0.001,
                )
            )
        return results


class _RejectFirstWaveReferenceClient(_AcceptingReferenceClient):
    def __init__(self):
        self.batch = 0

    async def generate_many(self, requests):
        self.batch += 1
        if self.batch > 1:
            return await super().generate_many(requests)
        return [
            JSONResult(
                request_id=request.request_id,
                model="fake-construction-model",
                data={
                    "decision": "rejected_combination",
                    "instruction": "",
                    "required_skill_ids": [],
                    "rejection_reason": "The sampled operations are not natural together.",
                },
                usage=TokenUsage(input_tokens=100, output_tokens=20),
                estimated_cost_usd=0.001,
            )
            for request in requests
        ]


def test_reference_generation_reaches_candidate_coverage_and_tracks_review_metadata():
    skills, tasks = _pilot_construction_inputs()

    result = asyncio.run(
        generate_reference_tasks(
            skills,
            tasks,
            _AcceptingReferenceClient(),
            seed=20260804,
            max_attempts=12,
        )
    )

    assert not result.unresolved_skill_ids
    assert set(result.covered_skill_ids) == {skill.skill_id for skill in skills}
    assert result.candidates
    assert all(item["review_status"] == "pending" for item in result.candidates)
    assert all("source_contribution" in item for item in result.candidates)
    assert all("similarity_reference" in item for item in result.candidates)


def test_reference_generation_returns_rejected_skills_to_uncovered_pool():
    skills, tasks = _pilot_construction_inputs()

    result = asyncio.run(
        generate_reference_tasks(
            skills,
            tasks,
            _RejectFirstWaveReferenceClient(),
            seed=20260804,
            max_attempts=12,
        )
    )

    assert not result.unresolved_skill_ids
    assert any(
        attempt["decision"] == "rejected_combination"
        for attempt in result.attempts
    )
    assert len(result.attempts) > len(result.candidates)


def test_frozen_reference_candidates_cover_every_skill_but_remain_pending_review():
    pilot_root = (
        Path(__file__).resolve().parents[1]
        / "evaluation_examples"
        / "expert_skill_learning"
        / "pilot"
    )
    skill_pool = json.loads(
        (pilot_root / "skill_pool.json").read_text(encoding="utf-8")
    )
    candidates = json.loads(
        (pilot_root / "reference_tasks.json").read_text(encoding="utf-8")
    )
    run = json.loads(
        (pilot_root / "reference_task_generation_run.json").read_text(
            encoding="utf-8"
        )
    )

    all_skill_ids = {skill["skill_id"] for skill in skill_pool["skills"]}
    tasks = candidates["reference_tasks"]
    covered = {
        skill_id for task in tasks for skill_id in task["required_skill_ids"]
    }

    assert len(tasks) == 3
    assert covered == all_skill_ids
    assert candidates["candidate_coverage"]["complete"] is True
    assert candidates["candidate_coverage"]["unresolved_skill_ids"] == []
    assert all(2 <= len(task["required_skill_ids"]) <= 5 for task in tasks)
    assert all(task["review_status"] == "pending" for task in tasks)
    assert not any(
        task["similarity_reference"]["exact_source_instruction_match"]
        for task in tasks
    )
    assert run["estimated_cost_usd"] == pytest.approx(0.03798)
    assert run["quality_review"]["human_approval_complete"] is False


def test_pricing_estimates_uncached_cached_and_output_tokens():
    pricing = PricingTable.from_path()
    usage = TokenUsage(
        input_tokens=2000,
        cached_input_tokens=200,
        output_tokens=1000,
    )

    assert pricing.estimate_usd("gpt-5.6-terra", usage) == pytest.approx(0.01564)
    assert pricing.estimate_usd("unknown-compatible-model", usage) is None


class _FakeCompletions:
    def __init__(self, response):
        self.response = response
        self.calls = []

    async def create(self, **kwargs):
        self.calls.append(kwargs)
        return self.response


class _PermanentRequestError(Exception):
    status_code = 400


class _FailingCompletions:
    def __init__(self):
        self.calls = 0

    async def create(self, **kwargs):
        self.calls += 1
        raise _PermanentRequestError("invalid response schema")


class _FakeClient:
    def __init__(self, response):
        self.completions = _FakeCompletions(response)
        self.chat = SimpleNamespace(completions=self.completions)


class _FailingClient:
    def __init__(self):
        self.completions = _FailingCompletions()
        self.chat = SimpleNamespace(completions=self.completions)


def test_async_client_validates_json_and_logs_each_attempt(tmp_path):
    response = SimpleNamespace(
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(
                    content=json.dumps(
                        {
                            "skills": [
                                {
                                    "name": "Use a fill handle",
                                    "procedure": ["Enter one value, then drag the handle."],
                                    "efficiency_tip": "Fill the range in one operation.",
                                    "action_ids": [0],
                                }
                            ]
                        }
                    )
                )
            )
        ],
        usage=SimpleNamespace(
            prompt_tokens=100,
            completion_tokens=50,
            prompt_tokens_details=SimpleNamespace(cached_tokens=10),
        ),
    )
    fake = _FakeClient(response)
    log_path = tmp_path / "calls.jsonl"
    client = OpenAICompatibleAsyncClient(
        LLMConfig(max_retries=0),
        call_log=log_path,
        client=fake,
    )
    request = JSONRequest(
        prompt_name="test",
        system_prompt="system",
        user_prompt="user",
        response_schema=load_schema("skill-extraction-response.schema.json"),
        schema_name="skill_extraction_response",
    )

    result = asyncio.run(client.generate_json(request))

    assert result.usage == TokenUsage(100, 50, 10)
    assert result.estimated_cost_usd is not None
    assert fake.completions.calls[0]["response_format"]["type"] == "json_schema"
    log = json.loads(log_path.read_text(encoding="utf-8"))
    assert log["status"] == "success"
    assert log["request_id"] == request.request_id
    assert log["prompt_sha256"] == request.prompt_sha256
    assert log["input_tokens"] == 100


def test_invalid_paid_response_logs_usage_before_retry_failure(tmp_path):
    response = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content="not json"))],
        usage=SimpleNamespace(
            prompt_tokens=100,
            completion_tokens=20,
            prompt_tokens_details=SimpleNamespace(cached_tokens=0),
        ),
    )
    log_path = tmp_path / "calls.jsonl"
    client = OpenAICompatibleAsyncClient(
        LLMConfig(max_retries=0),
        call_log=log_path,
        client=_FakeClient(response),
    )
    request = JSONRequest(
        prompt_name="invalid-json",
        system_prompt="system",
        user_prompt="user",
        response_schema={"type": "object"},
        schema_name="invalid_json",
    )

    with pytest.raises(json.JSONDecodeError):
        asyncio.run(client.generate_json(request))

    log = json.loads(log_path.read_text(encoding="utf-8"))
    assert log["status"] == "failed"
    assert log["input_tokens"] == 100
    assert log["output_tokens"] == 20
    assert log["estimated_cost_usd"] is not None


def test_permanent_client_error_is_not_retried(tmp_path):
    fake = _FailingClient()
    client = OpenAICompatibleAsyncClient(
        LLMConfig(max_retries=3),
        call_log=tmp_path / "calls.jsonl",
        client=fake,
    )
    request = JSONRequest(
        prompt_name="invalid-schema",
        system_prompt="system",
        user_prompt="user",
        response_schema={"type": "object"},
        schema_name="invalid_schema",
    )

    with pytest.raises(_PermanentRequestError):
        asyncio.run(client.generate_json(request))

    assert fake.completions.calls == 1
    logs = (tmp_path / "calls.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(logs) == 1


def test_video_interface_fails_explicitly_for_current_text_backend(tmp_path):
    fake = _FakeClient(None)
    client = OpenAICompatibleAsyncClient(
        LLMConfig(max_retries=0),
        call_log=tmp_path / "calls.jsonl",
        client=fake,
    )
    request = JSONRequest(
        prompt_name="future-video-test",
        system_prompt="system",
        user_prompt="user",
        response_schema={"type": "object"},
        schema_name="future_video",
        media=(MediaInput("video", "reference.mp4"),),
    )

    with pytest.raises(UnsupportedMediaError, match="text only"):
        asyncio.run(client.generate_json(request))
