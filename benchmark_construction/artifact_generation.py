"""Generate validated application artifacts from reference packages."""

from __future__ import annotations

import asyncio
from datetime import date
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

from .llm import JSONRequest, OpenAICompatibleAsyncClient
from .prompts import load_prompt, render_prompt
from .reference_applications import (
    get_reference_application,
    get_reference_application_for_artifact_type,
)
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
    app: str = "libreoffice_calc"


def load_artifact_blueprints(path: Path) -> list[ArtifactBlueprintResult]:
    document = json.loads(path.read_text(encoding="utf-8"))
    profile = get_reference_application_for_artifact_type(
        document.get("artifact_type", "xlsx")
    )
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
        validate_payload(blueprint, load_schema(profile.artifact_schema))
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
                app=profile.app,
            )
        )
    return results


def build_artifact_blueprint_request(
    package: dict[str, Any],
    *,
    prompt_root: Path = PROMPT_ROOT,
) -> JSONRequest:
    profile = get_reference_application(package.get("app", "libreoffice_calc"))
    stem = profile.artifact_prompt_stem
    system_prompt = load_prompt(prompt_root / f"{stem}.system.txt")
    user_template = load_prompt(prompt_root / f"{stem}.user.txt")
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
        prompt_name=f"{stem}.v1",
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        response_schema=load_schema(profile.artifact_schema),
        schema_name=f"{profile.artifact_type}_artifact_blueprint",
    )


def validate_artifact_blueprint(
    package: dict[str, Any], blueprint: dict[str, Any]
) -> None:
    profile = get_reference_application(package.get("app", "libreoffice_calc"))
    validate_payload(blueprint, load_schema(profile.artifact_schema))
    if profile.artifact_type == "pptx":
        _validate_impress_artifact_blueprint(package, blueprint)
        return
    _validate_calc_artifact_blueprint(package, blueprint)


def _validate_calc_artifact_blueprint(
    package: dict[str, Any], blueprint: dict[str, Any]
) -> None:
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
        width = len(sheet["headers"])
        if len(sheet["column_types"]) != width:
            raise ValueError(
                f"Blueprint column types differ in width for sheet {sheet['name']}"
            )
        if len(sheet["column_number_formats"]) != width:
            raise ValueError(
                f"Blueprint number formats differ in width for sheet {sheet['name']}"
            )
        if len(sheet["rows"]) != expected["row_count"]:
            raise ValueError(
                f"Blueprint row count differs for sheet {sheet['name']}"
            )
        for index, row in enumerate(sheet["rows"], start=2):
            if len(row["values"]) != width:
                raise ValueError(
                    f"Sheet {sheet['name']} row {index} has the wrong width"
                )
            for column_index, (value, data_type) in enumerate(
                zip(row["values"], sheet["column_types"]), start=1
            ):
                if value == "" or data_type == "text":
                    continue
                try:
                    if data_type == "integer":
                        if not re.fullmatch(r"[+-]?\d+", value.strip()):
                            raise ValueError
                        int(value)
                    elif data_type in {"decimal", "currency"}:
                        float(value)
                    elif data_type == "date":
                        date.fromisoformat(value)
                except (TypeError, ValueError) as exc:
                    raise ValueError(
                        f"Sheet {sheet['name']} row {index} column "
                        f"{column_index} has invalid {data_type} value: {value!r}"
                    ) from exc
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


def _validate_impress_artifact_blueprint(
    package: dict[str, Any], blueprint: dict[str, Any]
) -> None:
    spec = package["artifact_spec"]
    if blueprint["presentation_title"] != spec["presentation_title"]:
        raise ValueError("Blueprint presentation title differs from artifact_spec")
    if blueprint["slide_size"] != spec["slide_size"]:
        raise ValueError("Blueprint slide size differs from artifact_spec")
    if blueprint["theme"] != spec["theme"]:
        raise ValueError("Blueprint theme differs from artifact_spec")

    spec_slides = {slide["slide_number"]: slide for slide in spec["slides"]}
    slide_numbers = [slide["slide_number"] for slide in blueprint["slides"]]
    if slide_numbers != list(range(1, len(slide_numbers) + 1)):
        raise ValueError("Blueprint slide numbers must be consecutive from 1")
    if set(slide_numbers) != set(spec_slides):
        raise ValueError("Blueprint slides differ from artifact_spec")

    semantic_ids: set[str] = set()
    slide_width = 13.333 if blueprint["slide_size"] == "wide" else 10.0
    slide_height = 7.5
    for slide in blueprint["slides"]:
        expected = spec_slides[slide["slide_number"]]
        expected_objects = {
            item["semantic_id"]: item for item in expected["object_plan"]
        }
        actual_objects = {item["semantic_id"]: item for item in slide["objects"]}
        if set(actual_objects) != set(expected_objects):
            raise ValueError(
                f"Blueprint objects differ on slide {slide['slide_number']}"
            )
        for semantic_id, item in actual_objects.items():
            if semantic_id in semantic_ids:
                raise ValueError(f"Duplicate semantic object ID: {semantic_id}")
            semantic_ids.add(semantic_id)
            if item["type"] != expected_objects[semantic_id]["type"]:
                raise ValueError(
                    f"Blueprint object type differs for {semantic_id}"
                )
            if item["x"] + item["w"] > slide_width + 1e-6:
                raise ValueError(f"Object {semantic_id} exceeds slide width")
            if item["y"] + item["h"] > slide_height + 1e-6:
                raise ValueError(f"Object {semantic_id} exceeds slide height")
            content = item["content"]
            if item["type"] == "text" and not content["text"]:
                raise ValueError(f"Text object {semantic_id} has no text")
            if item["type"] == "shape" and not content["shape_kind"]:
                raise ValueError(f"Shape object {semantic_id} has no shape_kind")
            if item["type"] == "image" and not content["image_kind"]:
                raise ValueError(f"Image object {semantic_id} has no image_kind")
            if item["type"] == "table":
                rows = content["rows"]
                if not rows or len({len(row) for row in rows}) != 1:
                    raise ValueError(f"Table object {semantic_id} is not rectangular")
            if item["type"] == "chart":
                categories = content["categories"]
                series = content["series"]
                if not categories or not series:
                    raise ValueError(f"Chart object {semantic_id} lacks data")
                if any(len(entry["values"]) != len(categories) for entry in series):
                    raise ValueError(
                        f"Chart object {semantic_id} series length differs from categories"
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
                app=package.get("app", "libreoffice_calc"),
            )
        )
    return blueprints


def _artifact_result(
    package: dict[str, Any],
    request: JSONRequest,
    result: Any,
) -> ArtifactBlueprintResult:
    validate_artifact_blueprint(package, result.data)
    return ArtifactBlueprintResult(
        reference_task_id=package["reference_task_id"],
        blueprint=result.data,
        request_id=result.request_id,
        prompt_sha256=request.prompt_sha256,
        model=result.model,
        input_tokens=result.usage.input_tokens,
        output_tokens=result.usage.output_tokens,
        estimated_cost_usd=result.estimated_cost_usd,
        app=package.get("app", "libreoffice_calc"),
    )


def _write_blueprint_checkpoint(
    path: Path,
    result: ArtifactBlueprintResult,
    *,
    base_prompt_sha256: str,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "reference_task_id": result.reference_task_id,
                "base_prompt_sha256": base_prompt_sha256,
                "blueprint": result.blueprint,
                "generation": {
                    "request_id": result.request_id,
                    "prompt_sha256": result.prompt_sha256,
                    "model": result.model,
                    "input_tokens": result.input_tokens,
                    "output_tokens": result.output_tokens,
                    "estimated_cost_usd": result.estimated_cost_usd,
                },
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


async def generate_artifact_blueprints_checkpointed(
    packages: Sequence[dict[str, Any]],
    client: OpenAICompatibleAsyncClient,
    *,
    checkpoint_dir: Path,
    resume: bool,
    semantic_retries: int = 2,
) -> list[ArtifactBlueprintResult]:
    """Retain validated results and retry only locally invalid blueprints."""

    if semantic_retries < 0:
        raise ValueError("semantic_retries must be non-negative")

    async def process(package: dict[str, Any]) -> ArtifactBlueprintResult:
        base_request = build_artifact_blueprint_request(package)
        checkpoint = checkpoint_dir / f"{package['reference_task_id']}.json"
        if resume and checkpoint.is_file():
            document = json.loads(checkpoint.read_text(encoding="utf-8"))
            if document.get("reference_task_id") != package["reference_task_id"]:
                raise ValueError(f"Checkpoint task ID mismatch: {checkpoint}")
            if document.get("base_prompt_sha256") != base_request.prompt_sha256:
                raise ValueError(f"Checkpoint prompt differs: {checkpoint}")
            blueprint = document.get("blueprint")
            try:
                validate_artifact_blueprint(package, blueprint)
            except ValueError:
                pass
            else:
                generation = document.get("generation", {})
                return ArtifactBlueprintResult(
                    reference_task_id=package["reference_task_id"],
                    blueprint=blueprint,
                    request_id=str(generation.get("request_id", "")),
                    prompt_sha256=str(generation.get("prompt_sha256", "")),
                    model=str(generation.get("model", "")),
                    input_tokens=int(generation.get("input_tokens", 0)),
                    output_tokens=int(generation.get("output_tokens", 0)),
                    estimated_cost_usd=generation.get("estimated_cost_usd"),
                    app=package.get("app", "libreoffice_calc"),
                )

        request = base_request
        last_error: ValueError | None = None
        for attempt in range(semantic_retries + 1):
            result = await client.generate_json(request)
            try:
                validated = _artifact_result(package, request, result)
            except ValueError as exc:
                last_error = exc
                if attempt >= semantic_retries:
                    break
                profile = get_reference_application(
                    package.get("app", "libreoffice_calc")
                )
                if profile.artifact_type == "xlsx":
                    required_contract = [
                        {
                            "name": sheet["name"],
                            "headers": [
                                column["name"] for column in sheet["columns"]
                            ],
                            "column_types": [
                                column["data_type"] for column in sheet["columns"]
                            ],
                            "row_count": sheet["row_count"],
                        }
                        for sheet in package["artifact_spec"]["sheets"]
                    ]
                else:
                    required_contract = [
                        {
                            "slide_number": slide["slide_number"],
                            "semantic_objects": [
                                {
                                    "semantic_id": item["semantic_id"],
                                    "type": item["type"],
                                }
                                for item in slide["object_plan"]
                            ],
                        }
                        for slide in package["artifact_spec"]["slides"]
                    ]
                request = JSONRequest(
                    prompt_name=base_request.prompt_name,
                    system_prompt=base_request.system_prompt,
                    user_prompt=(
                        base_request.user_prompt
                        + f"\n\nCorrection attempt {attempt + 1}. Your previous "
                        "response failed local validation: "
                        + str(exc)
                        + ". Return a corrected complete blueprint. Every sheet "
                        "must exactly match this local contract, including exact "
                        "header spelling/order and exact row count:\n"
                        + json.dumps(
                            required_contract, indent=2, ensure_ascii=False
                        )
                    ),
                    response_schema=base_request.response_schema,
                    schema_name=base_request.schema_name,
                )
                continue
            _write_blueprint_checkpoint(
                checkpoint,
                validated,
                base_prompt_sha256=base_request.prompt_sha256,
            )
            return validated
        raise ValueError(
            f"Artifact blueprint remained invalid for "
            f"{package['reference_task_id']}: {last_error}"
        )

    outcomes = await asyncio.gather(
        *(process(package) for package in packages), return_exceptions=True
    )
    failures = [item for item in outcomes if isinstance(item, BaseException)]
    if failures:
        details = "; ".join(f"{type(item).__name__}: {item}" for item in failures)
        raise RuntimeError(
            f"{len(failures)} artifact blueprint task(s) failed; validated "
            f"checkpoints were retained: {details}"
        )
    return list(outcomes)


def write_artifact_blueprints(
    path: Path,
    results: Sequence[ArtifactBlueprintResult],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    apps = {result.app for result in results}
    if len(apps) > 1:
        raise ValueError("Artifact blueprint files cannot mix applications")
    profile = get_reference_application(
        next(iter(apps), "libreoffice_calc")
    )
    total_cost = sum(
        result.estimated_cost_usd
        for result in results
        if result.estimated_cost_usd is not None
    )
    document = {
        "schema_version": "1.0",
        "artifact_type": profile.artifact_type,
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
