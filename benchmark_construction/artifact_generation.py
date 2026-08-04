"""Generate validated Calc workbook blueprints from reference packages."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

from .llm import JSONRequest, OpenAICompatibleAsyncClient
from .prompts import load_prompt, render_prompt
from .reference_generation import PROMPT_ROOT
from .schema import load_schema, validate_payload


ARTIFACT_BLUEPRINT_SCHEMA = "calc-artifact-blueprint.schema.json"
CELL_REFERENCE = re.compile(r"^[A-Z]{1,3}[1-9][0-9]{0,5}$")


@dataclass(frozen=True)
class ArtifactBlueprintResult:
    reference_task_id: str
    blueprint: dict[str, Any]
    request_id: str
    prompt_sha256: str
    model: str
    input_tokens: int
    output_tokens: int
    estimated_cost_usd: float | None


def load_artifact_blueprints(path: Path) -> list[ArtifactBlueprintResult]:
    document = json.loads(path.read_text(encoding="utf-8"))
    entries = document.get("blueprints")
    if not isinstance(entries, list):
        raise ValueError(f"{path} has no blueprints list")
    results: list[ArtifactBlueprintResult] = []
    seen_ids: set[str] = set()
    for entry in entries:
        task_id = entry.get("reference_task_id")
        if not isinstance(task_id, str) or not task_id:
            raise ValueError(f"{path} contains a blueprint without a task ID")
        if task_id in seen_ids:
            raise ValueError(f"Duplicate artifact blueprint ID: {task_id}")
        seen_ids.add(task_id)
        blueprint = entry.get("blueprint")
        validate_payload(blueprint, load_schema(ARTIFACT_BLUEPRINT_SCHEMA))
        generation = entry.get("generation", {})
        results.append(
            ArtifactBlueprintResult(
                reference_task_id=task_id,
                blueprint=blueprint,
                request_id=str(generation.get("request_id", "")),
                prompt_sha256=str(generation.get("prompt_sha256", "")),
                model=str(generation.get("model", "")),
                input_tokens=int(generation.get("input_tokens", 0)),
                output_tokens=int(generation.get("output_tokens", 0)),
                estimated_cost_usd=generation.get("estimated_cost_usd"),
            )
        )
    return results


def build_artifact_blueprint_request(
    package: dict[str, Any],
    *,
    prompt_root: Path = PROMPT_ROOT,
) -> JSONRequest:
    system_prompt = load_prompt(prompt_root / "generate_calc_artifact.system.txt")
    user_template = load_prompt(prompt_root / "generate_calc_artifact.user.txt")
    relevant_package = {
        "reference_task_id": package["reference_task_id"],
        "task_instruction": package["task_instruction"],
        "required_skill_ids": package["required_skill_ids"],
        "artifact_spec": package["artifact_spec"],
        "operator_guide": package["operator_guide"],
        "expected_incidental_operations": package[
            "expected_incidental_operations"
        ],
    }
    user_prompt = render_prompt(
        user_template,
        {
            "REFERENCE_PACKAGE": json.dumps(
                relevant_package, indent=2, ensure_ascii=False
            )
        },
    )
    return JSONRequest(
        prompt_name="generate_calc_artifact.v1",
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        response_schema=load_schema(ARTIFACT_BLUEPRINT_SCHEMA),
        schema_name="calc_artifact_blueprint",
    )


def validate_artifact_blueprint(
    package: dict[str, Any], blueprint: dict[str, Any]
) -> None:
    validate_payload(blueprint, load_schema(ARTIFACT_BLUEPRINT_SCHEMA))
    spec = package["artifact_spec"]
    spec_sheets = {sheet["name"]: sheet for sheet in spec["sheets"]}
    sheet_names = [sheet["name"] for sheet in blueprint["sheets"]]
    if len(set(sheet_names)) != len(sheet_names):
        raise ValueError("Blueprint sheet names must be unique")
    if set(sheet_names) != set(spec_sheets):
        raise ValueError(
            "Blueprint sheets differ from artifact_spec; "
            f"expected={sorted(spec_sheets)}, returned={sorted(sheet_names)}"
        )

    for sheet in blueprint["sheets"]:
        expected = spec_sheets[sheet["name"]]
        expected_headers = [column["name"] for column in expected["columns"]]
        expected_types = [column["data_type"] for column in expected["columns"]]
        if sheet["headers"] != expected_headers:
            raise ValueError(
                f"Blueprint headers differ for sheet {sheet['name']}"
            )
        if sheet["column_types"] != expected_types:
            raise ValueError(
                f"Blueprint column types differ for sheet {sheet['name']}"
            )
        if len(sheet["column_number_formats"]) != len(sheet["headers"]):
            raise ValueError(
                f"Blueprint number formats differ in width for sheet {sheet['name']}"
            )
        if len(sheet["rows"]) != expected["row_count"]:
            raise ValueError(
                f"Blueprint row count differs for sheet {sheet['name']}"
            )
        width = len(sheet["headers"])
        for index, row in enumerate(sheet["rows"], start=2):
            if len(row["values"]) != width:
                raise ValueError(
                    f"Sheet {sheet['name']} row {index} has the wrong width"
                )
        formula_cells: set[str] = set()
        for formula in sheet["formulas"]:
            cell = formula["cell"].upper()
            if not CELL_REFERENCE.fullmatch(cell):
                raise ValueError(f"Invalid formula cell reference: {cell}")
            if cell in formula_cells:
                raise ValueError(f"Duplicate formula cell: {cell}")
            if not formula["formula"].startswith("="):
                raise ValueError(f"Formula must begin with '=': {cell}")
            formula_cells.add(cell)

        artifact_text = json.dumps(spec, ensure_ascii=False).lower()
        autofilter_range = sheet["autofilter_range"]
        if "autofilter enabled" in artifact_text and autofilter_range is None:
            raise ValueError(
                f"Sheet {sheet['name']} explicitly requires an AutoFilter"
            )
        if "filter-free" in artifact_text and autofilter_range is not None:
            raise ValueError(
                f"Sheet {sheet['name']} explicitly forbids an AutoFilter"
            )
        if autofilter_range is not None:
            last_column_index = width
            last_column = ""
            while last_column_index:
                last_column_index, remainder = divmod(last_column_index - 1, 26)
                last_column = chr(65 + remainder) + last_column
            expected_range = f"A1:{last_column}{len(sheet['rows']) + 1}"
            if autofilter_range.upper() != expected_range:
                raise ValueError(
                    f"Sheet {sheet['name']} AutoFilter must cover {expected_range}"
                )


async def generate_artifact_blueprints(
    packages: Sequence[dict[str, Any]],
    client: OpenAICompatibleAsyncClient,
) -> list[ArtifactBlueprintResult]:
    if not packages:
        return []
    requests = [build_artifact_blueprint_request(package) for package in packages]
    results = await client.generate_many(requests)
    blueprints: list[ArtifactBlueprintResult] = []
    for package, request, result in zip(packages, requests, results):
        validate_artifact_blueprint(package, result.data)
        blueprints.append(
            ArtifactBlueprintResult(
                reference_task_id=package["reference_task_id"],
                blueprint=result.data,
                request_id=result.request_id,
                prompt_sha256=request.prompt_sha256,
                model=result.model,
                input_tokens=result.usage.input_tokens,
                output_tokens=result.usage.output_tokens,
                estimated_cost_usd=result.estimated_cost_usd,
            )
        )
    return blueprints


def write_artifact_blueprints(
    path: Path,
    results: Sequence[ArtifactBlueprintResult],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    total_cost = sum(
        result.estimated_cost_usd
        for result in results
        if result.estimated_cost_usd is not None
    )
    document = {
        "schema_version": "1.0",
        "artifact_type": "xlsx",
        "blueprints": [
            {
                "reference_task_id": result.reference_task_id,
                "blueprint": result.blueprint,
                "generation": {
                    "request_id": result.request_id,
                    "prompt_sha256": result.prompt_sha256,
                    "model": result.model,
                    "input_tokens": result.input_tokens,
                    "output_tokens": result.output_tokens,
                    "estimated_cost_usd": result.estimated_cost_usd,
                },
            }
            for result in results
        ],
        "totals": {
            "calls": len(results),
            "input_tokens": sum(result.input_tokens for result in results),
            "output_tokens": sum(result.output_tokens for result in results),
            "estimated_cost_usd": round(total_cost, 12),
            "pricing_complete": all(
                result.estimated_cost_usd is not None for result in results
            ),
        },
    }
    path.write_text(
        json.dumps(document, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
