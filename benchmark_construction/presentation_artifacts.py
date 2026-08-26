"""Render and inspect synthetic PPTX reference-task artifacts."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree


PLACEHOLDER_PATTERN = re.compile(
    r"(?:xxxx|lorem|ipsum|click to add|this .{0,20}(?:page|slide).{0,20}layout)",
    re.IGNORECASE,
)
DRAWING_TEXT = "{http://schemas.openxmlformats.org/drawingml/2006/main}t"


def _slide_xml_paths(archive: zipfile.ZipFile) -> list[str]:
    paths = [
        name
        for name in archive.namelist()
        if re.fullmatch(r"ppt/slides/slide[1-9][0-9]*\.xml", name)
    ]
    return sorted(paths, key=lambda value: int(re.search(r"(\d+)", value).group(1)))


def inspect_pptx(path: Path) -> dict:
    if not zipfile.is_zipfile(path):
        raise ValueError(f"PPTX is not a ZIP package: {path}")
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
        required = {"[Content_Types].xml", "ppt/presentation.xml"}
        missing = sorted(required.difference(names))
        if missing:
            raise ValueError(f"PPTX lacks required parts: {missing}")
        slides = []
        all_text = []
        for index, name in enumerate(_slide_xml_paths(archive), start=1):
            root = ElementTree.fromstring(archive.read(name))
            texts = [node.text or "" for node in root.iter(DRAWING_TEXT)]
            all_text.extend(texts)
            slides.append(
                {
                    "slide_number": index,
                    "text": texts,
                    "shape_count": sum(1 for node in root.iter() if node.tag.endswith("}sp")),
                    "picture_count": sum(1 for node in root.iter() if node.tag.endswith("}pic")),
                    "graphic_frame_count": sum(
                        1 for node in root.iter() if node.tag.endswith("}graphicFrame")
                    ),
                }
            )
        joined = "\n".join(all_text)
        return {
            "slide_count": len(slides),
            "slides": slides,
            "text": all_text,
            "placeholder_matches": sorted(set(PLACEHOLDER_PATTERN.findall(joined))),
            "media_parts": sorted(name for name in names if name.startswith("ppt/media/")),
            "notes_parts": sorted(name for name in names if name.startswith("ppt/notesSlides/")),
        }


def _contact_sheet(images: list[Path], output: Path) -> None:
    from PIL import Image, ImageDraw

    loaded = [Image.open(path).convert("RGB") for path in images]
    if not loaded:
        raise ValueError("Cannot create a contact sheet without slide previews")
    thumb_width = 640
    thumb_height = round(loaded[0].height * thumb_width / loaded[0].width)
    columns = 2 if len(loaded) > 1 else 1
    rows = (len(loaded) + columns - 1) // columns
    label_height = 34
    canvas = Image.new(
        "RGB",
        (columns * thumb_width, rows * (thumb_height + label_height)),
        "white",
    )
    draw = ImageDraw.Draw(canvas)
    for index, image in enumerate(loaded):
        image.thumbnail((thumb_width, thumb_height))
        column = index % columns
        row = index // columns
        x = column * thumb_width
        y = row * (thumb_height + label_height)
        canvas.paste(image, (x, y))
        draw.text((x + 10, y + thumb_height + 8), f"Slide {index + 1}", fill="black")
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output)


def render_and_qa_presentation(
    pptx_path: Path,
    preview_dir: Path,
    qa_seed_path: Path,
    qa_path: Path,
    *,
    expected_slide_count: int,
    soffice: str = "soffice",
    pdftoppm: str = "pdftoppm",
) -> dict:
    preview_dir.mkdir(parents=True, exist_ok=True)
    inspection = inspect_pptx(pptx_path)
    if inspection["slide_count"] != expected_slide_count:
        raise ValueError(
            f"PPTX has {inspection['slide_count']} slides; expected {expected_slide_count}"
        )
    if inspection["placeholder_matches"]:
        raise ValueError(
            "PPTX contains leftover placeholder text: "
            + ", ".join(inspection["placeholder_matches"])
        )

    with tempfile.TemporaryDirectory(prefix="reference-pptx-render-") as tmp:
        render_dir = Path(tmp)
        profile_dir = render_dir / "libreoffice-profile"
        profile_dir.mkdir()
        subprocess.run(
            [
                soffice,
                "--headless",
                f"-env:UserInstallation={profile_dir.as_uri()}",
                "--convert-to",
                "pdf",
                "--outdir",
                str(render_dir),
                str(pptx_path),
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        pdf_path = render_dir / f"{pptx_path.stem}.pdf"
        if not pdf_path.is_file():
            raise RuntimeError("LibreOffice did not create a PDF preview")
        prefix = render_dir / "slide"
        subprocess.run(
            [pdftoppm, "-png", "-r", "120", str(pdf_path), str(prefix)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        rendered = sorted(render_dir.glob("slide-*.png"))
        if len(rendered) != expected_slide_count:
            raise RuntimeError(
                f"Rendered {len(rendered)} slides; expected {expected_slide_count}"
            )
        copied = []
        for index, source in enumerate(rendered, start=1):
            target = preview_dir / f"slide-{index:02d}.png"
            shutil.copy2(source, target)
            copied.append(target)
        _contact_sheet(copied, preview_dir / "contact-sheet.png")

    seed = json.loads(qa_seed_path.read_text(encoding="utf-8"))
    qa = {
        "schema_version": "1.0",
        "artifact_type": "pptx",
        "opens_as_zip_package": True,
        "libreoffice_render_succeeded": True,
        "slide_count": inspection["slide_count"],
        "semantic_object_count": seed["semantic_object_count"],
        "geometric_overlap_warnings": seed["geometric_overlap_warnings"],
        "placeholder_matches": inspection["placeholder_matches"],
        "media_part_count": len(inspection["media_parts"]),
        "notes_part_count": len(inspection["notes_parts"]),
        "slides": inspection["slides"],
        "preview_files": [
            f"slide-{index:02d}.png" for index in range(1, expected_slide_count + 1)
        ],
        "contact_sheet": "contact-sheet.png",
        "visual_review_required": True,
    }
    qa_path.write_text(json.dumps(qa, ensure_ascii=False, indent=2) + "\n")
    return qa
