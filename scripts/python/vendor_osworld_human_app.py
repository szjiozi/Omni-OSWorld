#!/usr/bin/env python3
"""Vendor one OSWorld-Human app directory without changing source bytes."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from benchmark_construction.osworld_human import vendor_osworld_human_app


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--app", default="libreoffice_calc")
    parser.add_argument(
        "--source-repository",
        default="https://github.com/WukLab/osworld-human",
    )
    parser.add_argument("--source-commit", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = vendor_osworld_human_app(
        args.source_root,
        args.output_root,
        app=args.app,
        source_repository=args.source_repository,
        source_commit=args.source_commit,
    )
    print(
        f"Vendored {len(manifest['tasks'])} {args.app} tasks to "
        f"{args.output_root}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
