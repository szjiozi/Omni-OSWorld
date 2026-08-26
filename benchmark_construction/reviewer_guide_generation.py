"""Generate Chinese novice guides from frozen TASK_DETAIL.md documents."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

from .llm import JSONRequest, OpenAICompatibleAsyncClient
from .prompts import load_prompt, render_prompt
from .reference_applications import get_reference_application
from .reference_generation import PROMPT_ROOT
from .schema import load_schema, validate_payload


REVIEWER_GUIDE_SCHEMA = "reference-reviewer-guide.schema.json"
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
CHINESE_PATTERN = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
CHINESE_QUOTED_UI_ACTION = re.compile(
    r"(?:点击|单击|双击|右键单击|选择|打开|进入|切换到|从)"
    r"[^。；\n]{0,32}[“\"]([^”\"]*[\u3400-\u4dbf\u4e00-\u9fff][^”\"]*)[”\"]"
)
CHART_DATA_ROLE_PATTERN = re.compile(
    r"(?:分类标签|分类轴|数据系列|数值系列|`Categories`|`Y-Values`)"
)
CHART_PLACEMENT_PATTERN = re.compile(
    r"(?:将图表放|图表.{0,24}(?:空白区域|遮挡|位置)|(?:移动|拖动).{0,12}图表)"
)
CONDITIONAL_PATTERN = re.compile(r"(?:如果|若|如不|如未|否则)")
CHART_DATA_RECOVERY_PATTERN = re.compile(
    r"(?:`Data Series`|`Data Ranges`|重新选择.{0,20}(?:范围|数据))"
)
CHART_PLACEMENT_RECOVERY_PATTERN = re.compile(
    r"(?:拖动|移动).{0,30}(?:图表|外框|边框)|(?:图表|外框|边框).{0,30}(?:拖动|移动)"
)


@dataclass(frozen=True)
class ReviewerGuideJob:
    reference_task_id: str
    required_skill_ids: tuple[str, ...]
    task_detail_path: Path
    app: str = "libreoffice_calc"


@dataclass(frozen=True)
class ReviewerGuideResult:
    reference_task_id: str
    task_detail_sha256: str
    guide: dict[str, Any]
    request_id: str
    prompt_sha256: str
    model: str
    input_tokens: int
    output_tokens: int
    estimated_cost_usd: float | None


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def build_reviewer_guide_request(
    job: ReviewerGuideJob,
    task_detail: str,
    *,
    prompt_root: Path = PROMPT_ROOT,
) -> JSONRequest:
    if not task_detail.strip():
        raise ValueError(f"TASK_DETAIL.md is empty for {job.reference_task_id}")
    profile = get_reference_application(job.app)
    stem = profile.reviewer_guide_prompt_stem
    system_prompt = load_prompt(prompt_root / f"{stem}.system.txt")
    user_template = load_prompt(prompt_root / f"{stem}.user.txt")
    user_prompt = render_prompt(
        user_template,
        {
            "REFERENCE_TASK_ID": job.reference_task_id,
            "REQUIRED_SKILL_IDS": json.dumps(
                list(job.required_skill_ids), indent=2, ensure_ascii=False
            ),
            "TASK_DETAIL": task_detail,
        },
    )
    return JSONRequest(
        prompt_name=f"{stem}.v3",
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        response_schema=load_schema(REVIEWER_GUIDE_SCHEMA),
        schema_name="reference_reviewer_guide",
    )


def _guide_explanatory_text(guide: dict[str, Any]) -> str:
    values = [guide["overview"], *guide["starting_state_checks"]]
    for step in guide["steps"]:
        values.extend(
            [
                step["title"],
                *step["instructions"],
                step["efficiency_tip"],
                step["visible_success_signal"],
            ]
        )
    values.extend(guide["final_verification"])
    return "\n".join(values)


def _guide_instructions(guide: dict[str, Any]) -> list[str]:
    return [
        instruction
        for step in guide["steps"]
        for instruction in step["instructions"]
    ]


def _validate_default_dependent_recoveries(guide: dict[str, Any]) -> None:
    explanatory_text = _guide_explanatory_text(guide)
    instructions = _guide_instructions(guide)
    if CHART_DATA_ROLE_PATTERN.search(explanatory_text):
        has_data_recovery = any(
            CONDITIONAL_PATTERN.search(instruction)
            and CHART_DATA_RECOVERY_PATTERN.search(instruction)
            for instruction in instructions
        )
        if not has_data_recovery:
            raise ValueError(
                "Reviewer guide describes inferred chart data roles without a "
                "conditional correction path"
            )
    if CHART_PLACEMENT_PATTERN.search(explanatory_text):
        has_placement_recovery = any(
            CONDITIONAL_PATTERN.search(instruction)
            and CHART_PLACEMENT_RECOVERY_PATTERN.search(instruction)
            for instruction in instructions
        )
        if not has_placement_recovery:
            raise ValueError(
                "Reviewer guide describes chart placement without a conditional "
                "drag-or-move correction path"
            )


def validate_reviewer_guide(
    reference_task_id: str,
    required_skill_ids: Sequence[str],
    guide: dict[str, Any],
) -> None:
    validate_payload(guide, load_schema(REVIEWER_GUIDE_SCHEMA))
    if guide["reference_task_id"] != reference_task_id:
        raise ValueError(
            "Reviewer guide task ID differs from its TASK_DETAIL.md input"
        )
    expected = set(required_skill_ids)
    covered: set[str] = set()
    for expected_number, step in enumerate(guide["steps"], start=1):
        if step["step_number"] != expected_number:
            raise ValueError("Reviewer guide step numbers must be consecutive from 1")
        skill_ids = step["skill_ids"]
        if len(skill_ids) != len(set(skill_ids)):
            raise ValueError("A reviewer guide step cannot repeat a skill ID")
        unexpected = set(skill_ids).difference(expected)
        if unexpected:
            raise ValueError(
                f"Reviewer guide contains unexpected skill IDs: {sorted(unexpected)}"
            )
        covered.update(skill_ids)
    missing = expected.difference(covered)
    if missing:
        raise ValueError(
            f"Reviewer guide does not cover required skills: {sorted(missing)}"
        )
    if not CHINESE_PATTERN.search(_guide_explanatory_text(guide)):
        raise ValueError("Reviewer guide explanatory content must be Chinese")
    for step in guide["steps"]:
        for instruction in step["instructions"]:
            match = CHINESE_QUOTED_UI_ACTION.search(instruction)
            if match:
                raise ValueError(
                    "Reviewer guide uses a Chinese visible UI label in an action: "
                    f"{match.group(1)!r}. Use the exact English UI label in backticks."
                )
    _validate_default_dependent_recoveries(guide)


async def generate_reviewer_guides(
    jobs: Sequence[ReviewerGuideJob],
    client: OpenAICompatibleAsyncClient,
    *,
    semantic_retries: int = 2,
) -> list[ReviewerGuideResult]:
    if semantic_retries < 0:
        raise ValueError("semantic_retries must be non-negative")
    details = [job.task_detail_path.read_text(encoding="utf-8") for job in jobs]
    requests = [
        build_reviewer_guide_request(job, detail)
        for job, detail in zip(jobs, details)
    ]
    responses = await client.generate_many(requests)
    results: list[ReviewerGuideResult] = []
    for job, detail, base_request, initial_response in zip(
        jobs, details, requests, responses
    ):
        request = base_request
        response = initial_response
        last_error: ValueError | None = None
        for retry in range(semantic_retries + 1):
            try:
                validate_reviewer_guide(
                    job.reference_task_id,
                    job.required_skill_ids,
                    response.data,
                )
            except ValueError as exc:
                last_error = exc
                if retry >= semantic_retries:
                    break
                request = JSONRequest(
                    prompt_name=base_request.prompt_name,
                    system_prompt=base_request.system_prompt,
                    user_prompt=(
                        base_request.user_prompt
                        + f"\n\nCorrection attempt {retry + 1}. The previous "
                        "response failed local validation: "
                        + str(exc)
                        + ". Return a complete corrected guide. Keep Chinese "
                        "explanations, but write every visible LibreOffice UI "
                        "label in exact English inside backticks. Cover exactly "
                        "these required skill IDs: "
                        + json.dumps(list(job.required_skill_ids))
                        + "."
                    ),
                    response_schema=base_request.response_schema,
                    schema_name=base_request.schema_name,
                )
                response = await client.generate_json(request)
                continue
            last_error = None
            break
        if last_error is not None:
            raise ValueError(
                f"Reviewer guide for {job.reference_task_id} remained invalid "
                f"after retries: {last_error}"
            )
        results.append(
            ReviewerGuideResult(
                reference_task_id=job.reference_task_id,
                task_detail_sha256=sha256_text(detail),
                guide=response.data,
                request_id=response.request_id,
                prompt_sha256=request.prompt_sha256,
                model=response.model,
                input_tokens=response.usage.input_tokens,
                output_tokens=response.usage.output_tokens,
                estimated_cost_usd=response.estimated_cost_usd,
            )
        )
    return results


def write_reviewer_guides(
    path: Path, results: Sequence[ReviewerGuideResult]
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    known_costs = [
        item.estimated_cost_usd
        for item in results
        if item.estimated_cost_usd is not None
    ]
    document = {
        "schema_version": "1.0",
        "guides": [
            {
                "reference_task_id": item.reference_task_id,
                "task_detail_sha256": item.task_detail_sha256,
                "guide": item.guide,
                "generation": {
                    "request_id": item.request_id,
                    "prompt_sha256": item.prompt_sha256,
                    "model": item.model,
                    "input_tokens": item.input_tokens,
                    "output_tokens": item.output_tokens,
                    "estimated_cost_usd": item.estimated_cost_usd,
                },
            }
            for item in results
        ],
        "totals": {
            "calls": len(results),
            "input_tokens": sum(item.input_tokens for item in results),
            "output_tokens": sum(item.output_tokens for item in results),
            "estimated_cost_usd": round(sum(known_costs), 12),
            "pricing_complete": len(known_costs) == len(results),
        },
    }
    path.write_text(
        json.dumps(document, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def load_reviewer_guides(path: Path) -> dict[str, dict[str, Any]]:
    document = json.loads(path.read_text(encoding="utf-8"))
    entries = document.get("guides")
    if not isinstance(entries, list):
        raise ValueError(f"{path} has no guides list")
    result: dict[str, dict[str, Any]] = {}
    for entry in entries:
        task_id = entry.get("reference_task_id")
        if not isinstance(task_id, str) or not task_id:
            raise ValueError(f"{path} contains a guide without a task ID")
        if task_id in result:
            raise ValueError(f"Duplicate reviewer guide task ID: {task_id}")
        detail_digest = entry.get("task_detail_sha256")
        if not isinstance(detail_digest, str) or not SHA256_PATTERN.fullmatch(
            detail_digest
        ):
            raise ValueError(f"Invalid TASK_DETAIL.md SHA256 for {task_id}")
        guide = entry.get("guide")
        if not isinstance(guide, dict):
            raise ValueError(f"Reviewer guide payload is missing for {task_id}")
        result[task_id] = entry
    return result
