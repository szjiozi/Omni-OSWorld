#!/usr/bin/env python3
"""Induce reusable Calc skills from the four reference recordings."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from benchmark_construction.video_skill_induction import (
    VideoInductionConfig,
    discover_reference_videos,
    induce_video_skills,
    write_induction_outputs,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
PROMPT_ROOT = REPO_ROOT / "evaluation_examples/expert_skill_learning/prompts"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--videos-root",
        type=Path,
        default=REPO_ROOT / "results/reference_annotations",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=REPO_ROOT
        / "results/expert_skill_learning/qwen37_engineering_pilot/stage1",
    )
    parser.add_argument("--model", default="qwen3.7-plus-2026-05-26")
    parser.add_argument("--fps", type=float, default=1.0)
    parser.add_argument("--max-pixels", type=int, default=1_048_576)
    parser.add_argument("--max-tokens", type=int, default=8192)
    parser.add_argument("--seed", type=int, default=20260812)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    videos = discover_reference_videos(args.videos_root)
    system_prompt = (PROMPT_ROOT / "induce_video_skills.system.txt").read_text(
        encoding="utf-8"
    )
    user_prompt = (PROMPT_ROOT / "induce_video_skills.user.txt").read_text(
        encoding="utf-8"
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)

    def save_raw_response(raw_text: str) -> None:
        raw_path = args.output_dir / "raw_response.txt"
        temporary = raw_path.with_name(f".{raw_path.name}.tmp")
        temporary.write_text(raw_text + "\n", encoding="utf-8")
        os.replace(temporary, raw_path)

    learned_skills, run, raw_text = induce_video_skills(
        videos,
        system_prompt=system_prompt,
        user_prompt_template=user_prompt,
        config=VideoInductionConfig(
            model=args.model,
            fps=args.fps,
            max_pixels=args.max_pixels,
            max_tokens=args.max_tokens,
            seed=args.seed,
        ),
        raw_response_sink=save_raw_response,
    )
    write_induction_outputs(args.output_dir, learned_skills, run, raw_text)
    print(args.output_dir / "learned_skills.json")


if __name__ == "__main__":
    main()
