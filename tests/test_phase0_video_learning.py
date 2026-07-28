from zipfile import ZipFile

from scripts.python.generate_phase0_fixtures import generate
from scripts.python.validate_phase0_tasks import validate


def test_phase0_fixture_generation_is_deterministic(tmp_path):
    first = generate(tmp_path / "first")
    second = generate(tmp_path / "second")

    assert len(first["files"]) == 20
    assert first["files"] == second["files"]
    for package_path in (tmp_path / "first").iterdir():
        if package_path.suffix not in {".pptx", ".xlsx"}:
            continue
        with ZipFile(package_path) as package:
            core_properties = package.read("docProps/core.xml")
        assert b"2000-01-01T00:00:00Z" in core_properties


def test_phase0_tasks_validate_locally():
    report = validate(generate=False, daytona=False)

    assert report["status"] == "passed"
    assert len(report["tasks"]) == 4
    assert all(task["initial_score"] == 0.0 for task in report["tasks"])
    assert all(task["gold_score"] == 1.0 for task in report["tasks"])
