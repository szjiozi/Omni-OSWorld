#!/usr/bin/env python3
"""Derive the W1 animation-free initial deck from the verified web gold."""

from __future__ import annotations

import argparse
import re
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURE_ROOT = (
    REPO_ROOT / "evaluation_examples" / "powerpoint_web" / "fixtures"
)
DEFAULT_GOLD = FIXTURE_ROOT / "osworld_w1_fade_gold.pptx"
DEFAULT_INITIAL = FIXTURE_ROOT / "osworld_w1_fade_initial.pptx"
TIMING_PATTERN = re.compile(rb"<p:timing>.*?</p:timing>", re.DOTALL)


def derive_initial(gold_path: Path, initial_path: Path) -> Path:
    removed = 0
    initial_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(gold_path) as source, zipfile.ZipFile(
        initial_path,
        "w",
    ) as target:
        for info in source.infolist():
            payload = source.read(info.filename)
            if re.fullmatch(r"ppt/slides/slide\d+\.xml", info.filename):
                payload, count = TIMING_PATTERN.subn(b"", payload)
                removed += count
            target.writestr(info, payload)
    if removed != 1:
        initial_path.unlink(missing_ok=True)
        raise ValueError(f"expected exactly one timing tree, removed {removed}")
    return initial_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gold", type=Path, default=DEFAULT_GOLD)
    parser.add_argument("--initial", type=Path, default=DEFAULT_INITIAL)
    args = parser.parse_args()
    output = derive_initial(args.gold, args.initial)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
