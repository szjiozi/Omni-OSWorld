"""Semantic PowerPoint animation timeline extraction and comparison."""

from __future__ import annotations

import logging
import re
import zipfile
from copy import deepcopy
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET


logger = logging.getLogger("desktopenv.metric.pptx_animation")

PRESENTATION_NS = (
    "http://schemas.openxmlformats.org/presentationml/2006/main"
)
DRAWING_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
NS = {"p": PRESENTATION_NS, "a": DRAWING_NS}

TRIGGER_TYPES = {
    "clickEffect": "on_click",
    "withEffect": "with_previous",
    "afterEffect": "after_previous",
}


def _slide_number(name: str) -> int:
    match = re.fullmatch(r"ppt/slides/slide(\d+)\.xml", name)
    if not match:
        raise ValueError(f"not a slide XML path: {name}")
    return int(match.group(1))


def _shape_catalog(root: ET.Element) -> dict[str, dict[str, str]]:
    shapes: dict[str, dict[str, str]] = {}
    for shape_tag in ("sp", "pic", "graphicFrame", "grpSp", "cxnSp"):
        for shape in root.findall(f".//p:{shape_tag}", NS):
            properties = shape.find(".//p:cNvPr", NS)
            if properties is None:
                continue
            shape_id = properties.get("id")
            if not shape_id:
                continue
            text = " ".join(
                value.strip()
                for value in (
                    node.text or "" for node in shape.findall(".//a:t", NS)
                )
                if value.strip()
            )
            shapes[shape_id] = {
                "shape_id": shape_id,
                "target_name": properties.get("name", ""),
                "target_text": text,
            }
    return shapes


def _duration_ms(effect: ET.Element) -> int | None:
    behavior_timing = effect.find("./p:cBhvr/p:cTn", NS)
    if behavior_timing is None:
        return None
    raw_duration = behavior_timing.get("dur", "")
    if not raw_duration.isdigit():
        return None
    return int(raw_duration)


def _extract_slide_events(root: ET.Element) -> list[dict[str, Any]]:
    shapes = _shape_catalog(root)
    events: list[dict[str, Any]] = []
    for timing in root.findall(".//p:cTn[@presetClass]", NS):
        target = timing.find(".//p:spTgt", NS)
        if target is None or not target.get("spid"):
            continue
        shape_id = target.get("spid", "")
        animation_effect = timing.find(".//p:animEffect", NS)
        trigger_node = timing.get("nodeType", "")
        trigger = TRIGGER_TYPES.get(trigger_node, trigger_node or "unknown")

        effect = ""
        transition = ""
        duration_ms = None
        if animation_effect is not None:
            effect = animation_effect.get("filter", "")
            transition = animation_effect.get("transition", "")
            duration_ms = _duration_ms(animation_effect)
        if not effect:
            effect = f"preset:{timing.get('presetID', '')}"

        event = {
            "order": len(events),
            "target_shape_id": shape_id,
            "target_name": "",
            "target_text": "",
            "effect": effect.lower(),
            "transition": transition.lower(),
            "trigger": trigger,
            "duration_ms": duration_ms,
            "preset_class": timing.get("presetClass", ""),
            "preset_id": timing.get("presetID", ""),
            "preset_subtype": timing.get("presetSubtype", ""),
        }
        event.update(shapes.get(shape_id, {}))
        event["target_shape_id"] = event.pop("shape_id", shape_id)
        events.append(event)
    return events


def extract_pptx_animation_timeline(pptx_path: str | Path) -> dict[str, Any]:
    """Extract an implementation-independent animation timeline from a PPTX."""

    path = Path(pptx_path)
    if not path.is_file():
        raise FileNotFoundError(path)

    with zipfile.ZipFile(path) as package:
        slide_names = sorted(
            (
                name
                for name in package.namelist()
                if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)
            ),
            key=_slide_number,
        )
        slides = []
        for slide_name in slide_names:
            root = ET.fromstring(package.read(slide_name))
            slides.append(
                {
                    "slide_index": _slide_number(slide_name) - 1,
                    "events": _extract_slide_events(root),
                }
            )
    return {"slides": slides}


def _static_xml_members(package: zipfile.ZipFile) -> dict[str, bytes]:
    members: dict[str, bytes] = {}
    patterns = (
        r"ppt/presentation\.xml",
        r"ppt/slides/slide\d+\.xml",
        r"ppt/slideLayouts/slideLayout\d+\.xml",
        r"ppt/slideMasters/slideMaster\d+\.xml",
        r"ppt/theme/theme\d+\.xml",
    )
    for name in package.namelist():
        if not any(re.fullmatch(pattern, name) for pattern in patterns):
            continue
        root = ET.fromstring(package.read(name))
        if re.fullmatch(r"ppt/slides/slide\d+\.xml", name):
            root = deepcopy(root)
            timing = root.find("p:timing", NS)
            if timing is not None:
                root.remove(timing)
        members[name] = ET.tostring(root, encoding="utf-8")
    return members


def compare_pptx_static_content(
    result_pptx: str | None,
    expected_pptx: str | None,
    **_options: Any,
) -> float:
    """Require slide content, layout, colors, masters, and theme to stay fixed."""

    if not result_pptx or not expected_pptx:
        return 0.0
    try:
        with zipfile.ZipFile(result_pptx) as result_package:
            result_members = _static_xml_members(result_package)
        with zipfile.ZipFile(expected_pptx) as expected_package:
            expected_members = _static_xml_members(expected_package)
    except (FileNotFoundError, KeyError, OSError, ET.ParseError, zipfile.BadZipFile):
        logger.exception("Unable to read PPTX static content")
        return 0.0
    return float(result_members == expected_members)


def _same_target(result: dict[str, Any], expected: dict[str, Any]) -> bool:
    result_text = result.get("target_text", "")
    expected_text = expected.get("target_text", "")
    if result_text and expected_text:
        return result_text == expected_text
    result_name = result.get("target_name", "")
    expected_name = expected.get("target_name", "")
    if result_name and expected_name:
        return result_name == expected_name
    return result.get("target_shape_id") == expected.get("target_shape_id")


def _event_matches(
    result: dict[str, Any],
    expected: dict[str, Any],
    duration_tolerance_ms: int,
) -> bool:
    if not _same_target(result, expected):
        return False
    for field in (
        "effect",
        "transition",
        "trigger",
        "preset_class",
        "preset_id",
        "preset_subtype",
    ):
        if result.get(field) != expected.get(field):
            return False

    result_duration = result.get("duration_ms")
    expected_duration = expected.get("duration_ms")
    if result_duration is None or expected_duration is None:
        return result_duration == expected_duration
    return abs(result_duration - expected_duration) <= duration_tolerance_ms


def compare_pptx_animation_timelines(
    result_pptx: str | None,
    expected_pptx: str | None,
    **options: Any,
) -> float:
    """Score semantic animation events without comparing OOXML node IDs."""

    if not result_pptx or not expected_pptx:
        return 0.0
    duration_tolerance_ms = int(options.get("duration_tolerance_ms", 50))
    if duration_tolerance_ms < 0:
        raise ValueError("duration_tolerance_ms must be non-negative")

    try:
        result = extract_pptx_animation_timeline(result_pptx)
        expected = extract_pptx_animation_timeline(expected_pptx)
    except (FileNotFoundError, KeyError, OSError, ET.ParseError, zipfile.BadZipFile):
        logger.exception("Unable to read PPTX animation timeline")
        return 0.0

    result_slides = result["slides"]
    expected_slides = expected["slides"]
    if len(result_slides) != len(expected_slides):
        return 0.0

    total_expected = sum(len(slide["events"]) for slide in expected_slides)
    total_result = sum(len(slide["events"]) for slide in result_slides)
    if total_expected == 0:
        return float(total_result == 0)

    matched = 0
    for result_slide, expected_slide in zip(result_slides, expected_slides):
        result_events = result_slide["events"]
        expected_events = expected_slide["events"]
        for result_event, expected_event in zip(result_events, expected_events):
            if _event_matches(
                result_event,
                expected_event,
                duration_tolerance_ms,
            ):
                matched += 1
    return matched / max(total_expected, total_result)
