import tempfile
import unittest
import zipfile
from pathlib import Path

from desktop_env.evaluators.pptx_animation import (
    compare_pptx_animation_timelines,
    extract_pptx_animation_timeline,
)
from scripts.python.validate_aws_ppt_web_w1_task import (
    TASK_ROOT,
    validate,
)


FIXTURE_ROOT = TASK_ROOT / "fixtures"
INITIAL = FIXTURE_ROOT / "osworld_w1_fade_initial.pptx"
GOLD = FIXTURE_ROOT / "osworld_w1_fade_gold.pptx"


def _replace_slide_xml(source: Path, destination: Path, old: bytes, new: bytes):
    with zipfile.ZipFile(source) as package, zipfile.ZipFile(
        destination,
        "w",
    ) as output:
        for info in package.infolist():
            payload = package.read(info.filename)
            if info.filename == "ppt/slides/slide1.xml":
                if old not in payload:
                    raise AssertionError(f"{old!r} not present in fixture")
                payload = payload.replace(old, new, 1)
            output.writestr(info, payload)


class PptxAnimationEvaluatorTests(unittest.TestCase):
    def test_extracts_semantic_fade_event(self):
        timeline = extract_pptx_animation_timeline(GOLD)
        event = timeline["slides"][0]["events"][0]

        self.assertEqual(event["target_text"], "Quarterly Review")
        self.assertEqual(event["effect"], "fade")
        self.assertEqual(event["transition"], "in")
        self.assertEqual(event["trigger"], "on_click")
        self.assertEqual(event["duration_ms"], 500)

    def test_initial_fails_and_gold_passes(self):
        self.assertEqual(
            compare_pptx_animation_timelines(INITIAL, GOLD),
            0.0,
        )
        self.assertEqual(
            compare_pptx_animation_timelines(GOLD, GOLD),
            1.0,
        )

    def test_duration_mutation_is_detected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            mutated = Path(temp_dir) / "duration.pptx"
            _replace_slide_xml(GOLD, mutated, b'dur="500"', b'dur="900"')

            self.assertEqual(
                compare_pptx_animation_timelines(
                    mutated,
                    GOLD,
                    duration_tolerance_ms=50,
                ),
                0.0,
            )

    def test_formal_w1_task_is_discriminative(self):
        report = validate()

        self.assertEqual(report["status"], "passed")
        self.assertEqual(report["initial_animation_score"], 0.0)
        self.assertEqual(report["gold_animation_score"], 1.0)
        self.assertEqual(report["gold_design_score"], 1.0)


if __name__ == "__main__":
    unittest.main()
