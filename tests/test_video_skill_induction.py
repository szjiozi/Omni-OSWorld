import json
from pathlib import Path

import pytest

from benchmark_construction.video_skill_induction import (
    ReferenceVideo,
    VideoInductionConfig,
    induce_video_skills,
)


def _videos(tmp_path: Path):
    videos = []
    for index in range(1, 5):
        path = tmp_path / f"video-{index}.mp4"
        path.write_bytes(f"video-{index}".encode())
        videos.append(ReferenceVideo(f"reference-task-{index}", path))
    return videos


def _response(video_id="reference-task-1"):
    payload = {
        "skills": [
            {
                "name": "Fill a formula down a column",
                "procedure": [
                    "Enter the formula in the first destination cell.",
                    "Drag the fill handle through the remaining rows.",
                ],
                "when_to_use": "When one relative formula applies to many rows.",
                "efficiency_tip": "Verify the first formula before filling once.",
                "verification": "Inspect the first and last filled formulas.",
                "evidence": [
                    {
                        "video_id": video_id,
                        "start_seconds": 10,
                        "end_seconds": 18,
                        "observation": "The expert drags the fill handle once.",
                    }
                ],
            }
        ]
    }
    return {
        "status_code": 200,
        "request_id": "request-1",
        "output": {
            "choices": [
                {"message": {"content": [{"text": json.dumps(payload)}]}}
            ]
        },
        "usage": {
            "input_tokens": 1000,
            "output_tokens": 100,
            "input_tokens_details": {"image_tokens": 900, "text_tokens": 100},
        },
    }


def test_induce_video_skills_validates_and_injects_stable_ids(tmp_path):
    captured = {}

    def fake_call(**kwargs):
        captured.update(kwargs)
        return _response()

    skills, run, raw = induce_video_skills(
        _videos(tmp_path),
        system_prompt="system",
        user_prompt_template="IDs: {video_ids_json}",
        config=VideoInductionConfig(),
        call=fake_call,
    )

    assert skills["skills"][0]["skill_id"] == "induced-skill-01"
    assert run["request_id"] == "request-1"
    assert run["usage"]["image_tokens"] == 900
    assert run["estimated_cost_cny"] == pytest.approx(0.0028)
    assert captured["enable_thinking"] is False
    assert captured["messages"][1]["content"][0]["fps"] == 1.0
    staged_names = [
        Path(item["video"]).name
        for item in captured["messages"][1]["content"]
        if "video" in item
    ]
    assert staged_names == [
        "reference-video-01.mp4",
        "reference-video-02.mp4",
        "reference-video-03.mp4",
        "reference-video-04.mp4",
    ]
    assert json.loads(raw)["skills"]


def test_induce_video_skills_rejects_unknown_evidence_video(tmp_path):
    captured_raw = []
    with pytest.raises(ValueError, match="Unknown evidence video ID"):
        induce_video_skills(
            _videos(tmp_path),
            system_prompt="system",
            user_prompt_template="IDs: {video_ids_json}",
            config=VideoInductionConfig(),
            call=lambda **_: _response("not-a-video"),
            raw_response_sink=captured_raw.append,
        )
    assert captured_raw and json.loads(captured_raw[0])["skills"]
