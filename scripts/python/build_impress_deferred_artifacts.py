#!/usr/bin/env python3
"""Build reviewable Impress artifacts from materialized deferred-skill strategies."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from benchmark_construction.presentation_artifacts import (
    inspect_pptx,
    render_and_qa_presentation,
)
from benchmark_construction.reference_review import load_reference_packages


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packages", type=Path, action="append", required=True)
    parser.add_argument("--materialized-strategies", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--soffice", default="soffice")
    parser.add_argument("--pdftoppm", default="pdftoppm")
    return parser.parse_args()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _portable(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(REPO_ROOT))
    except ValueError:
        return str(resolved)


def build_deferred_artifacts(
    packages: list[dict],
    materialized: dict,
    output_dir: Path,
    *,
    soffice: str,
    pdftoppm: str,
) -> dict:
    strategy_by_id = {item["strategy_id"]: item for item in materialized["strategies"]}
    manifest_entries = []
    output_dir.mkdir(parents=True, exist_ok=True)
    for package in packages:
        strategy_ids = package.get("artifact_strategy_ids", [])
        if not strategy_ids:
            raise ValueError(
                f"Deferred package lacks artifact_strategy_ids: {package['reference_task_id']}"
            )
        try:
            strategies = [strategy_by_id[item] for item in strategy_ids]
        except KeyError as exc:
            raise ValueError(f"Unknown materialized strategy: {exc.args[0]}") from exc
        task_dir = output_dir / package["reference_task_id"]
        task_dir.mkdir(parents=True, exist_ok=True)
        primary_assets = [
            asset for asset in strategies[0]["assets"] if asset["role"] == "primary"
        ]
        if len(primary_assets) != 1:
            raise ValueError(f"Primary strategy has no unique PPTX: {strategy_ids[0]}")
        artifact_path = task_dir / "initial_artifact.pptx"
        shutil.copy2(primary_assets[0]["local_path"], artifact_path)

        supporting_files = []
        seen_guest_paths: set[str] = set()
        for strategy in strategies:
            for asset in strategy["assets"]:
                if asset["role"] != "supporting":
                    continue
                guest_path = asset["guest_path"]
                if guest_path in seen_guest_paths:
                    continue
                seen_guest_paths.add(guest_path)
                source = Path(asset["local_path"])
                target = task_dir / "supporting" / source.name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
                supporting_files.append(
                    {
                        "role": "supporting_input",
                        "local_path": _portable(target),
                        "guest_path": guest_path,
                        "sha256": _sha256(target),
                    }
                )

        expected_outputs = []
        expected_output_roles: set[str] = set()
        setup_profiles = []
        for strategy in strategies:
            for item in strategy["expected_outputs"]:
                if item["role"] not in expected_output_roles:
                    expected_outputs.append(item)
                    expected_output_roles.add(item["role"])
            for profile in strategy["setup_profiles"]:
                if profile not in setup_profiles:
                    setup_profiles.append(profile)

        inspection = inspect_pptx(artifact_path)
        blueprint_path = task_dir / "artifact_blueprint.json"
        blueprint_path.write_text(
            json.dumps(
                {
                    "schema_version": "1.0",
                    "builder": "impress_deferred_artifact_adapter",
                    "artifact_strategy_ids": strategy_ids,
                    "package_artifact_spec": package["artifact_spec"],
                    "source_provenance": [
                        {
                            "strategy_id": strategy["strategy_id"],
                            "source_task_id": strategy["source_task_id"],
                            "source_license": strategy["source_license"],
                        }
                        for strategy in strategies
                    ],
                },
                indent=2,
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
        qa_seed_path = task_dir / ".artifact_qa_seed.json"
        qa_seed_path.write_text(
            json.dumps(
                {
                    "semantic_object_count": sum(
                        slide["shape_count"]
                        + slide["picture_count"]
                        + slide["graphic_frame_count"]
                        for slide in inspection["slides"]
                    ),
                    "geometric_overlap_warnings": [],
                }
            ),
            encoding="utf-8",
        )
        qa_path = task_dir / "artifact_qa.json"
        render_and_qa_presentation(
            artifact_path,
            task_dir / "previews",
            qa_seed_path,
            qa_path,
            expected_slide_count=inspection["slide_count"],
            soffice=soffice,
            pdftoppm=pdftoppm,
        )
        qa_seed_path.unlink(missing_ok=True)
        manifest_entries.append(
            {
                "reference_task_id": package["reference_task_id"],
                "app": "libreoffice_impress",
                "artifact_type": "pptx",
                "artifact_path": _portable(artifact_path),
                "artifact_sha256": _sha256(artifact_path),
                "blueprint_path": _portable(blueprint_path),
                "qa_path": _portable(qa_path),
                "supporting_files": supporting_files,
                "expected_outputs": expected_outputs,
                "setup_profiles": setup_profiles,
                "artifact_strategy_ids": strategy_ids,
                "manual_setup_required": False,
                "manual_setup_steps": [],
            }
        )
    manifest = {"schema_version": "1.0", "artifacts": manifest_entries}
    (output_dir / "artifact_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> int:
    args = parse_args()
    packages = load_reference_packages(args.packages)
    materialized = json.loads(args.materialized_strategies.read_text(encoding="utf-8"))
    manifest = build_deferred_artifacts(
        packages,
        materialized,
        args.output_dir,
        soffice=args.soffice,
        pdftoppm=args.pdftoppm,
    )
    print(f"Built {len(manifest['artifacts'])} deferred Impress artifacts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
