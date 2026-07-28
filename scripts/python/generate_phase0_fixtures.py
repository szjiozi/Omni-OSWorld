#!/usr/bin/env python3
"""Generate deterministic Office/video fixtures for Phase 0 tasks."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import zipfile
from pathlib import Path
import cv2
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Pt


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_DIR = (
    REPO_ROOT
    / "evaluation_examples"
    / "video_learning"
    / "fixtures"
    / "generated"
)


def _font() -> ImageFont.ImageFont:
    return ImageFont.load_default()


def _card(
    *,
    title: str,
    lines: list[str],
    background: tuple[int, int, int],
    foreground: tuple[int, int, int],
) -> Image.Image:
    image = Image.new("RGB", (960, 540), background)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle(
        (80, 70, 880, 470),
        radius=24,
        outline=(180, 180, 180),
        width=3,
    )
    draw.text((120, 110), title, fill=foreground, font=_font())
    y = 185
    for line in lines:
        draw.text((120, y), line, fill=foreground, font=_font())
        y += 55
    return image


def _write_demo_video(path: Path, before: Image.Image, after: Image.Image) -> None:
    fps = 10
    writer = cv2.VideoWriter(
        str(path),
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        before.size,
    )
    if not writer.isOpened():
        raise RuntimeError("OpenCV could not initialize the mp4v video writer")

    transition = _card(
        title="Apply the same transformation",
        lines=["BEFORE  ->  AFTER", "Transfer the rule, not the content."],
        background=(245, 245, 245),
        foreground=(20, 20, 20),
    )
    try:
        for image, seconds in ((before, 1.2), (transition, 0.6), (after, 1.2)):
            frame = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
            for _ in range(round(seconds * fps)):
                writer.write(frame)
    finally:
        writer.release()


def _normalize_office_zip(path: Path) -> None:
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    with zipfile.ZipFile(path, "r") as source, zipfile.ZipFile(
        tmp_path,
        "w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as target:
        for name in sorted(source.namelist()):
            source_info = source.getinfo(name)
            target_info = zipfile.ZipInfo(
                filename=name,
                date_time=(1980, 1, 1, 0, 0, 0),
            )
            target_info.compress_type = zipfile.ZIP_DEFLATED
            target_info.external_attr = source_info.external_attr
            target_info.create_system = source_info.create_system
            target.writestr(target_info, source.read(name))
    os.replace(tmp_path, path)


def _presentation(
    path: Path,
    *,
    title: str,
    body: str,
    title_font: str = "Liberation Sans",
    title_size: int = 28,
    title_color: str = "222222",
    body_color: str = "333333",
    background: str = "FFFFFF",
) -> None:
    presentation = Presentation()
    slide = presentation.slides.add_slide(presentation.slide_layouts[1])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = RGBColor.from_string(background)
    slide.shapes.title.text = title
    slide.placeholders[1].text = body

    title_run = slide.shapes.title.text_frame.paragraphs[0].runs[0]
    title_run.font.name = title_font
    title_run.font.size = Pt(title_size)
    title_run.font.color.rgb = RGBColor.from_string(title_color)

    body_run = slide.placeholders[1].text_frame.paragraphs[0].runs[0]
    body_run.font.name = "Liberation Sans"
    body_run.font.size = Pt(18)
    body_run.font.color.rgb = RGBColor.from_string(body_color)
    presentation.save(path)
    _normalize_office_zip(path)


def _workbook_currency(
    path: Path,
    *,
    rows: list[tuple[str, float]],
    apply_style: bool,
) -> None:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Budget"
    sheet.append(["Item", "Amount"])
    for row in rows:
        sheet.append(row)
    if apply_style:
        for cell in sheet["B"][1:]:
            cell.number_format = "$#,##0.00"
    workbook.save(path)
    _normalize_office_zip(path)


def _workbook_header(
    path: Path,
    *,
    headers: list[str],
    rows: list[tuple[object, ...]],
    apply_style: bool,
) -> None:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Overview"
    sheet.append(headers)
    for row in rows:
        sheet.append(row)
    if apply_style:
        for cell in sheet[1]:
            cell.font = Font(
                name="Liberation Sans",
                size=11,
                bold=True,
                color="FFFFFFFF",
            )
            cell.fill = PatternFill(
                fill_type="solid",
                fgColor="FF1F4E78",
            )
    workbook.save(path)
    _normalize_office_zip(path)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def generate(output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)

    _presentation(
        output_dir / "impress_title_initial.pptx",
        title="Quarterly Review",
        body="Revenue, retention, and next steps",
    )
    _presentation(
        output_dir / "impress_title_gold.pptx",
        title="Quarterly Review",
        body="Revenue, retention, and next steps",
        title_font="Liberation Serif",
        title_size=32,
        title_color="1F4E78",
    )
    _presentation(
        output_dir / "impress_title_demo_before.pptx",
        title="Research Update",
        body="Methods, findings, and open questions",
    )
    _presentation(
        output_dir / "impress_title_demo_after.pptx",
        title="Research Update",
        body="Methods, findings, and open questions",
        title_font="Liberation Serif",
        title_size=32,
        title_color="1F4E78",
    )
    _write_demo_video(
        output_dir / "impress_title_demo.mp4",
        _card(
            title="BEFORE: Research Update",
            lines=["Liberation Sans", "28 pt", "dark gray"],
            background=(255, 255, 255),
            foreground=(34, 34, 34),
        ),
        _card(
            title="AFTER: Research Update",
            lines=["Liberation Serif", "32 pt", "blue #1F4E78"],
            background=(255, 255, 255),
            foreground=(31, 78, 120),
        ),
    )

    _presentation(
        output_dir / "impress_background_initial.pptx",
        title="Customer Stories",
        body="Three teams and what they learned",
        background="F2F2F2",
    )
    _presentation(
        output_dir / "impress_background_gold.pptx",
        title="Customer Stories",
        body="Three teams and what they learned",
        title_color="FFFFFF",
        body_color="FFFFFF",
        background="1F4E78",
    )
    _presentation(
        output_dir / "impress_background_demo_before.pptx",
        title="Design Systems",
        body="Foundations and reusable components",
        background="F2F2F2",
    )
    _presentation(
        output_dir / "impress_background_demo_after.pptx",
        title="Design Systems",
        body="Foundations and reusable components",
        title_color="FFFFFF",
        body_color="FFFFFF",
        background="1F4E78",
    )
    _write_demo_video(
        output_dir / "impress_background_demo.mp4",
        _card(
            title="BEFORE: Design Systems",
            lines=["light gray background", "dark title", "dark body"],
            background=(242, 242, 242),
            foreground=(34, 34, 34),
        ),
        _card(
            title="AFTER: Design Systems",
            lines=["blue background #1F4E78", "white title", "white body"],
            background=(31, 78, 120),
            foreground=(255, 255, 255),
        ),
    )

    _workbook_currency(
        output_dir / "calc_currency_initial.xlsx",
        rows=[("Hosting", 1200), ("Research", 875.5), ("Travel", 430.25)],
        apply_style=False,
    )
    _workbook_currency(
        output_dir / "calc_currency_gold.xlsx",
        rows=[("Hosting", 1200), ("Research", 875.5), ("Travel", 430.25)],
        apply_style=True,
    )
    _workbook_currency(
        output_dir / "calc_currency_demo_before.xlsx",
        rows=[("Software", 199), ("Equipment", 1450.75)],
        apply_style=False,
    )
    _workbook_currency(
        output_dir / "calc_currency_demo_after.xlsx",
        rows=[("Software", 199), ("Equipment", 1450.75)],
        apply_style=True,
    )
    _write_demo_video(
        output_dir / "calc_currency_demo.mp4",
        _card(
            title="BEFORE: Budget amounts",
            lines=["199", "1450.75", "General number format"],
            background=(255, 255, 255),
            foreground=(30, 30, 30),
        ),
        _card(
            title="AFTER: Budget amounts",
            lines=["$199.00", "$1,450.75", "Currency: $#,##0.00"],
            background=(255, 255, 255),
            foreground=(30, 30, 30),
        ),
    )

    _workbook_header(
        output_dir / "calc_header_initial.xlsx",
        headers=["Team", "Owner", "Status"],
        rows=[("Alpha", "Ava", "On track"), ("Beta", "Ben", "At risk")],
        apply_style=False,
    )
    _workbook_header(
        output_dir / "calc_header_gold.xlsx",
        headers=["Team", "Owner", "Status"],
        rows=[("Alpha", "Ava", "On track"), ("Beta", "Ben", "At risk")],
        apply_style=True,
    )
    _workbook_header(
        output_dir / "calc_header_demo_before.xlsx",
        headers=["Course", "Teacher", "Room"],
        rows=[("Math", "Mia", 204), ("History", "Noah", 110)],
        apply_style=False,
    )
    _workbook_header(
        output_dir / "calc_header_demo_after.xlsx",
        headers=["Course", "Teacher", "Room"],
        rows=[("Math", "Mia", 204), ("History", "Noah", 110)],
        apply_style=True,
    )
    _write_demo_video(
        output_dir / "calc_header_demo.mp4",
        _card(
            title="BEFORE: Table header",
            lines=["plain text", "no fill", "regular weight"],
            background=(255, 255, 255),
            foreground=(30, 30, 30),
        ),
        _card(
            title="AFTER: Table header",
            lines=["bold white text", "blue fill #1F4E78", "data unchanged"],
            background=(31, 78, 120),
            foreground=(255, 255, 255),
        ),
    )

    files = sorted(path for path in output_dir.iterdir() if path.is_file())
    manifest = {
        "schema_version": "1.0",
        "generator": str(Path(__file__).relative_to(REPO_ROOT)),
        "files": {
            path.name: {
                "sha256": _sha256(path),
                "bytes": path.stat().st_size,
            }
            for path in files
            if path.name != "fixture_manifest.json"
        },
    }
    (output_dir / "fixture_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    manifest = generate(args.output_dir)
    print(f"Generated {len(manifest['files'])} files in {args.output_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
