"""Build safe OSWorld configs for human reference-video annotation."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Sequence

from .llm import JSONRequest, OpenAICompatibleAsyncClient
from .prompts import load_prompt, render_prompt
from .reference_applications import get_reference_application
from .reference_generation import PROMPT_ROOT
from .reference_review import load_reference_reviews
from .schema import load_schema, validate_payload


ANNOTATION_BLUEPRINT_SCHEMA = "reference-annotation-blueprint.schema.json"
SAFE_TASK_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
GUEST_DESKTOP = PurePosixPath("/home/user/Desktop")
GUEST_DOWNLOADS = PurePosixPath("/home/user/Downloads")
SAFE_OUTPUT_ROLE = re.compile(r"^[a-z][a-z0-9_]{0,63}$")
SAFE_OUTPUT_FILENAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._ -]{0,159}$")


@dataclass(frozen=True)
class AnnotationBlueprintResult:
    reference_task_id: str
    blueprint: dict[str, Any]
    request_id: str
    prompt_sha256: str
    model: str
    input_tokens: int
    output_tokens: int
    estimated_cost_usd: float | None


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_artifact_manifest(path: Path) -> dict[str, dict[str, Any]]:
    document = json.loads(path.read_text(encoding="utf-8"))
    entries = document.get("artifacts")
    if not isinstance(entries, list):
        raise ValueError(f"{path} has no artifacts list")
    result: dict[str, dict[str, Any]] = {}
    for entry in entries:
        task_id = entry.get("reference_task_id")
        if not isinstance(task_id, str) or not task_id:
            raise ValueError(f"{path} contains an artifact without a task ID")
        if task_id in result:
            raise ValueError(f"Duplicate artifact manifest ID: {task_id}")
        result[task_id] = entry
    return result


def load_review_decisions(path: Path) -> dict[str, str]:
    # Reuse the full human-review semantic checks before retaining pending rows.
    load_reference_reviews(path)
    document = json.loads(path.read_text(encoding="utf-8"))
    reviews = document.get("reviews")
    if not isinstance(reviews, list):
        raise ValueError(f"{path} has no reviews list")
    schema = load_schema("reference-package-review.schema.json")
    decisions: dict[str, str] = {}
    for review in reviews:
        validate_payload(review, schema)
        task_id = review["reference_task_id"]
        if task_id in decisions:
            raise ValueError(f"Multiple reviews for the same package: {task_id}")
        decisions[task_id] = review["decision"]
    return decisions


def require_launchable_review(
    task_id: str,
    decisions: dict[str, str],
    *,
    allow_pending: bool = False,
) -> str:
    if task_id not in decisions:
        raise ValueError(f"No review form exists for reference task {task_id}")
    decision = decisions[task_id]
    if decision == "approved":
        return decision
    if decision == "" and allow_pending:
        return "pending"
    if decision == "":
        raise ValueError(
            f"Reference task {task_id} is pending review; use --allow-pending "
            "only for an engineering smoke test"
        )
    raise ValueError(
        f"Reference task {task_id} is not launchable: review decision is "
        f"{decision!r}"
    )


def build_annotation_blueprint_request(
    package: dict[str, Any],
    artifact_entry: dict[str, Any],
    *,
    prompt_root: Path = PROMPT_ROOT,
) -> JSONRequest:
    profile = get_reference_application(package.get("app", "libreoffice_calc"))
    stem = profile.annotation_prompt_stem
    system_prompt = load_prompt(prompt_root / f"{stem}.system.txt")
    user_template = load_prompt(prompt_root / f"{stem}.user.txt")
    package_input = {
        "reference_task_id": package["reference_task_id"],
        "app": package["app"],
        "task_instruction": package["task_instruction"],
        "artifact_spec": package["artifact_spec"],
        "operator_guide": package["operator_guide"],
    }
    artifact_input = {
        "reference_task_id": artifact_entry["reference_task_id"],
        "manual_setup_required": artifact_entry["manual_setup_required"],
        "manual_setup_steps": artifact_entry["manual_setup_steps"],
    }
    user_prompt = render_prompt(
        user_template,
        {
            "REFERENCE_PACKAGE": json.dumps(
                package_input, indent=2, ensure_ascii=False
            ),
            "ARTIFACT_MANIFEST_ENTRY": json.dumps(
                artifact_input, indent=2, ensure_ascii=False
            ),
        },
    )
    return JSONRequest(
        prompt_name=f"{stem}.v1",
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        response_schema=load_schema(profile.annotation_schema),
        schema_name="reference_annotation_blueprint",
    )


def validate_annotation_blueprint(
    blueprint: dict[str, Any], *, expected_app: str | None = None
) -> None:
    app = expected_app or blueprint.get("snapshot")
    profile = get_reference_application(app)
    validate_payload(blueprint, load_schema(profile.annotation_schema))
    filename = blueprint["guest_filename"]
    safe_filename = re.compile(
        rf"^[A-Za-z0-9][A-Za-z0-9._-]{{0,119}}{re.escape(profile.artifact_extension)}$"
    )
    if not safe_filename.fullmatch(filename):
        raise ValueError(f"Unsafe guest filename: {filename!r}")
    if PurePosixPath(filename).name != filename:
        raise ValueError("guest_filename must be a basename")


async def generate_annotation_blueprints(
    packages: Sequence[dict[str, Any]],
    artifact_by_id: dict[str, dict[str, Any]],
    client: OpenAICompatibleAsyncClient,
) -> list[AnnotationBlueprintResult]:
    requests: list[JSONRequest] = []
    for package in packages:
        task_id = package["reference_task_id"]
        if task_id not in artifact_by_id:
            raise ValueError(f"No artifact manifest entry for {task_id}")
        requests.append(
            build_annotation_blueprint_request(package, artifact_by_id[task_id])
        )
    results = await client.generate_many(requests)
    blueprints: list[AnnotationBlueprintResult] = []
    for package, request, result in zip(packages, requests, results):
        validate_annotation_blueprint(result.data, expected_app=package.get("app"))
        blueprints.append(
            AnnotationBlueprintResult(
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


def write_annotation_blueprints(
    path: Path, results: Sequence[AnnotationBlueprintResult]
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    known_costs = [
        item.estimated_cost_usd
        for item in results
        if item.estimated_cost_usd is not None
    ]
    document = {
        "schema_version": "1.0",
        "blueprints": [
            {
                "reference_task_id": item.reference_task_id,
                "blueprint": item.blueprint,
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


def load_annotation_blueprints(path: Path) -> list[AnnotationBlueprintResult]:
    document = json.loads(path.read_text(encoding="utf-8"))
    entries = document.get("blueprints")
    if not isinstance(entries, list):
        raise ValueError(f"{path} has no blueprints list")
    results: list[AnnotationBlueprintResult] = []
    seen: set[str] = set()
    for entry in entries:
        task_id = entry.get("reference_task_id")
        if not isinstance(task_id, str) or not task_id or task_id in seen:
            raise ValueError(f"Invalid or duplicate blueprint ID: {task_id!r}")
        seen.add(task_id)
        blueprint = entry.get("blueprint")
        validate_annotation_blueprint(blueprint)
        generation = entry.get("generation", {})
        results.append(
            AnnotationBlueprintResult(
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


def _resolve_artifact_path(repo_root: Path, raw_path: str) -> Path:
    candidate = Path(raw_path)
    resolved = (
        candidate.resolve()
        if candidate.is_absolute()
        else (repo_root / candidate).resolve()
    )
    try:
        resolved.relative_to(repo_root.resolve())
    except ValueError as exc:
        raise ValueError(f"Artifact path escapes the repository: {raw_path}") from exc
    if not resolved.is_file():
        raise FileNotFoundError(f"Artifact file does not exist: {resolved}")
    return resolved


def _portable_artifact_path(repo_root: Path, raw_path: str) -> tuple[Path, str]:
    resolved = _resolve_artifact_path(repo_root, raw_path)
    return resolved, str(resolved.relative_to(repo_root.resolve()))


def _validate_guest_file_path(raw_path: str) -> str:
    guest_path = PurePosixPath(raw_path)
    if guest_path.parent not in {GUEST_DESKTOP, GUEST_DOWNLOADS}:
        raise ValueError(
            "Guest artifact paths must be direct children of Desktop or Downloads: "
            f"{raw_path}"
        )
    if not SAFE_OUTPUT_FILENAME.fullmatch(guest_path.name):
        raise ValueError(f"Unsafe guest artifact filename: {guest_path.name!r}")
    return str(guest_path)


def _resolve_supporting_files(
    artifact_entry: dict[str, Any], *, repo_root: Path, main_guest_path: str
) -> list[dict[str, str]]:
    resolved: list[dict[str, str]] = []
    seen_guest_paths = {main_guest_path}
    for item in artifact_entry.get("supporting_files", []):
        if not isinstance(item, dict):
            raise ValueError("supporting_files entries must be objects")
        role = item.get("role", "supporting_input")
        if not isinstance(role, str) or not SAFE_OUTPUT_ROLE.fullmatch(role):
            raise ValueError(f"Unsafe supporting-file role: {role!r}")
        guest_path = _validate_guest_file_path(item.get("guest_path", ""))
        if guest_path in seen_guest_paths:
            raise ValueError(f"Duplicate guest artifact path: {guest_path}")
        seen_guest_paths.add(guest_path)
        path, portable_path = _portable_artifact_path(
            repo_root, item.get("local_path", "")
        )
        expected_hash = str(item.get("sha256", "")).casefold()
        actual_hash = _sha256(path)
        if actual_hash != expected_hash:
            raise ValueError(
                f"Supporting artifact SHA256 mismatch for {path.name}: "
                f"expected {expected_hash}, got {actual_hash}"
            )
        resolved.append(
            {
                "role": role,
                "local_path": portable_path,
                "guest_path": guest_path,
                "sha256": actual_hash,
            }
        )
    return resolved


def _validate_expected_outputs(raw_outputs: Any) -> list[dict[str, Any]]:
    if raw_outputs is None:
        return []
    if not isinstance(raw_outputs, list):
        raise ValueError("expected_outputs must be a list")
    outputs: list[dict[str, Any]] = []
    seen_roles: set[str] = set()
    seen_guest_paths: set[str] = set()
    seen_local_names: set[str] = set()
    for item in raw_outputs:
        if not isinstance(item, dict):
            raise ValueError("expected_outputs entries must be objects")
        role = item.get("role")
        local_filename = item.get("local_filename")
        if not isinstance(role, str) or not SAFE_OUTPUT_ROLE.fullmatch(role):
            raise ValueError(f"Unsafe expected-output role: {role!r}")
        if role in seen_roles:
            raise ValueError(f"Duplicate expected-output role: {role}")
        if (
            not isinstance(local_filename, str)
            or not SAFE_OUTPUT_FILENAME.fullmatch(local_filename)
            or PurePosixPath(local_filename).name != local_filename
        ):
            raise ValueError(f"Unsafe expected-output filename: {local_filename!r}")
        guest_path = _validate_guest_file_path(item.get("guest_path", ""))
        if (
            guest_path in seen_guest_paths
            or local_filename.casefold() in seen_local_names
        ):
            raise ValueError("Duplicate expected-output path or local filename")
        seen_roles.add(role)
        seen_guest_paths.add(guest_path)
        seen_local_names.add(local_filename.casefold())
        outputs.append(
            {
                "role": role,
                "guest_path": guest_path,
                "local_filename": local_filename,
                "required": bool(item.get("required", True)),
            }
        )
    return outputs


def assemble_osworld_annotation_config(
    package: dict[str, Any],
    artifact_entry: dict[str, Any],
    blueprint: dict[str, Any],
    *,
    repo_root: Path,
) -> dict[str, Any]:
    profile = get_reference_application(package.get("app", "libreoffice_calc"))
    validate_annotation_blueprint(blueprint, expected_app=profile.app)
    task_id = package["reference_task_id"]
    if not SAFE_TASK_ID.fullmatch(task_id):
        raise ValueError(f"Unsafe reference task ID: {task_id!r}")
    if artifact_entry.get("reference_task_id") != task_id:
        raise ValueError("Package and artifact manifest task IDs differ")
    artifact_path, portable_path = _portable_artifact_path(
        repo_root, artifact_entry["artifact_path"]
    )
    expected_hash = artifact_entry.get("artifact_sha256", "").lower()
    actual_hash = _sha256(artifact_path)
    if actual_hash != expected_hash:
        raise ValueError(
            f"Artifact SHA256 mismatch for {task_id}: expected "
            f"{expected_hash}, got {actual_hash}"
        )
    guest_path = str(GUEST_DESKTOP / blueprint["guest_filename"])
    supporting_files = _resolve_supporting_files(
        artifact_entry, repo_root=repo_root, main_guest_path=guest_path
    )
    expected_outputs = _validate_expected_outputs(
        artifact_entry.get("expected_outputs")
    )
    setup_profiles = artifact_entry.get("setup_profiles", [])
    if not isinstance(setup_profiles, list) or not all(
        isinstance(item, str) and SAFE_OUTPUT_ROLE.fullmatch(item)
        for item in setup_profiles
    ):
        raise ValueError("setup_profiles must contain safe profile identifiers")
    upload_files = [
        {"local_path": portable_path, "path": guest_path},
        *[
            {"local_path": item["local_path"], "path": item["guest_path"]}
            for item in supporting_files
        ],
    ]
    reference_annotation = {
        "schema_version": "1.0",
        "reference_task_id": task_id,
        "artifact_path": portable_path,
        "artifact_sha256": actual_hash,
        "guest_artifact_path": guest_path,
        "required_skill_ids": package["required_skill_ids"],
        "operator_guide": package["operator_guide"],
        "expected_incidental_operations": package["expected_incidental_operations"],
        "ready_state_checks": blueprint["ready_state_checks"],
        "setup_notes": blueprint["setup_notes"],
        "recording_mode": "human_reference",
    }
    if supporting_files:
        reference_annotation["supporting_files"] = supporting_files
    if expected_outputs:
        reference_annotation["expected_outputs"] = expected_outputs
    if setup_profiles:
        reference_annotation["setup_profiles"] = setup_profiles
    return {
        "id": task_id,
        "snapshot": profile.app,
        "instruction": package["task_instruction"],
        "source": "OSWorld Expert Skill Reference Pilot",
        "config": [
            {
                "type": "upload_file",
                "parameters": {"files": upload_files},
            },
            {"type": "open", "parameters": {"path": guest_path}},
        ],
        "related_apps": [profile.app],
        "reference_annotation": reference_annotation,
        "proxy": False,
        "fixed_ip": False,
        "possibility_of_env_change": "low",
    }


def write_annotation_configs(
    output_dir: Path,
    manifest_path: Path,
    packages: Sequence[dict[str, Any]],
    artifact_by_id: dict[str, dict[str, Any]],
    blueprints: Sequence[AnnotationBlueprintResult],
    *,
    repo_root: Path,
) -> list[dict[str, Any]]:
    package_by_id = {item["reference_task_id"]: item for item in packages}
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_entries: list[dict[str, Any]] = []
    for result in blueprints:
        task_id = result.reference_task_id
        if task_id not in package_by_id:
            raise ValueError(f"Blueprint references unknown package {task_id}")
        if task_id not in artifact_by_id:
            raise ValueError(f"Blueprint references unknown artifact {task_id}")
        config = assemble_osworld_annotation_config(
            package_by_id[task_id],
            artifact_by_id[task_id],
            result.blueprint,
            repo_root=repo_root,
        )
        config_path = output_dir / f"{task_id}.json"
        config_path.write_text(
            json.dumps(config, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        try:
            portable_config_path = str(
                config_path.resolve().relative_to(repo_root.resolve())
            )
        except ValueError:
            portable_config_path = str(config_path)
        manifest_entries.append(
            {
                "reference_task_id": task_id,
                "task_config_path": portable_config_path,
                "artifact_sha256": config["reference_annotation"]["artifact_sha256"],
                "blueprint_request_id": result.request_id,
            }
        )
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(
            {"schema_version": "1.0", "task_configs": manifest_entries},
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    return manifest_entries
