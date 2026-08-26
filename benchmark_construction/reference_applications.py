"""Application-specific contracts for expert-skill reference tasks."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceApplication:
    app: str
    artifact_type: str
    artifact_extension: str
    artifact_label: str
    title_field: str
    package_schema: str
    package_prompt_stem: str
    skill_prompt_stem: str
    artifact_schema: str
    artifact_prompt_stem: str
    annotation_schema: str
    annotation_prompt_stem: str
    reviewer_guide_prompt_stem: str

    @property
    def packet_artifact_filename(self) -> str:
        return f"initial_artifact{self.artifact_extension}"

    @property
    def final_artifact_filename(self) -> str:
        return f"final_artifact{self.artifact_extension}"


_APPLICATIONS = {
    "libreoffice_calc": ReferenceApplication(
        app="libreoffice_calc",
        artifact_type="xlsx",
        artifact_extension=".xlsx",
        artifact_label="Workbook",
        title_field="workbook_title",
        package_schema="reference-package-candidate.schema.json",
        package_prompt_stem="generate_reference_package",
        skill_prompt_stem="extract_skills",
        artifact_schema="calc-artifact-blueprint.schema.json",
        artifact_prompt_stem="generate_calc_artifact",
        annotation_schema="reference-annotation-blueprint.schema.json",
        annotation_prompt_stem="generate_reference_annotation_blueprint",
        reviewer_guide_prompt_stem="generate_reviewer_guide",
    ),
    "libreoffice_impress": ReferenceApplication(
        app="libreoffice_impress",
        artifact_type="pptx",
        artifact_extension=".pptx",
        artifact_label="Presentation",
        title_field="presentation_title",
        package_schema="reference-package-impress-candidate.schema.json",
        package_prompt_stem="generate_impress_reference_package",
        skill_prompt_stem="extract_impress_skills",
        artifact_schema="impress-artifact-blueprint.schema.json",
        artifact_prompt_stem="generate_impress_artifact",
        annotation_schema="reference-impress-annotation-blueprint.schema.json",
        annotation_prompt_stem="generate_impress_annotation_blueprint",
        reviewer_guide_prompt_stem="generate_impress_reviewer_guide",
    ),
}


def get_reference_application(app: str) -> ReferenceApplication:
    try:
        return _APPLICATIONS[app]
    except KeyError as exc:
        raise ValueError(f"Unsupported reference-task application: {app!r}") from exc


def get_reference_application_for_artifact_type(
    artifact_type: str,
) -> ReferenceApplication:
    matches = [
        profile
        for profile in _APPLICATIONS.values()
        if profile.artifact_type == artifact_type
    ]
    if len(matches) != 1:
        raise ValueError(f"Unsupported artifact type: {artifact_type!r}")
    return matches[0]

