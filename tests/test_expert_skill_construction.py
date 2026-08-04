import asyncio
import json
from pathlib import Path
import re
from types import SimpleNamespace

import pytest

from benchmark_construction.llm import (
    JSONRequest,
    LLMConfig,
    MediaInput,
    OpenAICompatibleAsyncClient,
    UnsupportedMediaError,
)
from benchmark_construction.models import SourceTask
from benchmark_construction.osworld_human import (
    load_source_manifest,
    load_source_task,
    resolve_task_paths,
    verify_manifest_sources,
)
from benchmark_construction.pricing import PricingTable, TokenUsage
from benchmark_construction.schema import load_schema
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
