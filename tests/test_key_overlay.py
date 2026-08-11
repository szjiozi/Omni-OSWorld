import json
from pathlib import Path
from types import SimpleNamespace

from benchmark_construction.key_overlay import (
    KeyOverlayEvent,
    PointerOverlayEvent,
    burn_key_overlay_in_guest,
    guest_recording_start_monotonic_ns,
    parse_timestamped_pointer_events,
    parse_timestamped_xinput,
    render_key_overlay_ass,
    start_guest_key_capture,
    stop_guest_key_capture,
    write_key_events,
    write_pointer_events,
)


KEYMAP = """\
keycode  36 = Return NoSymbol Return
keycode  37 = Control_L NoSymbol Control_L
keycode  38 = a A a A
keycode  50 = Shift_L NoSymbol Shift_L
keycode  55 = v V v V
keycode  56 = b B b B
"""


def _line(monotonic_ns: int, line: str) -> str:
    return json.dumps({"monotonic_ns": monotonic_ns, "line": line})


def _event(event_type: str, keycode: int, monotonic_ns: int) -> list[str]:
    event_number = 2 if event_type == "KeyPress" else 3
    return [
        _line(monotonic_ns, f"EVENT type {event_number} ({event_type})"),
        _line(monotonic_ns + 1, f"    detail: {keycode}"),
    ]


def _raw_event(event_type: str, keycode: int, monotonic_ns: int) -> list[str]:
    event_number = 13 if event_type == "KeyPress" else 14
    return [
        _line(
            monotonic_ns,
            f"EVENT type {event_number} (Raw{event_type})",
        ),
        _line(monotonic_ns + 1, f"    detail: {keycode}"),
    ]


def _button_event(
    event_type: str,
    button: int,
    monotonic_ns: int,
    x: float,
    y: float,
) -> list[str]:
    event_number = 4 if event_type == "ButtonPress" else 5
    return [
        _line(monotonic_ns, f"EVENT type {event_number} ({event_type})"),
        _line(monotonic_ns + 1, f"    detail: {button}"),
        _line(monotonic_ns + 2, f"    root: {x:.2f}/{y:.2f}"),
    ]


def test_parser_emits_shortcuts_and_special_keys_but_hides_plain_typing():
    start = 1_000_000_000
    lines = []
    lines += _event("KeyPress", 37, start + 100_000_000)
    lines += _event("KeyPress", 38, start + 150_000_000)
    lines += _event("KeyRelease", 38, start + 180_000_000)
    lines += _event("KeyRelease", 37, start + 200_000_000)
    lines += _event("KeyPress", 56, start + 250_000_000)
    lines += _event("KeyRelease", 56, start + 270_000_000)
    lines += _event("KeyPress", 36, start + 300_000_000)
    lines += _event("KeyRelease", 36, start + 320_000_000)
    lines += _event("KeyPress", 50, start + 350_000_000)
    lines += _event("KeyPress", 55, start + 400_000_000)

    events = parse_timestamped_xinput(
        "\n".join(lines),
        KEYMAP,
        video_start_monotonic_ns=start,
    )

    assert [event.label for event in events] == ["Ctrl + A", "Enter"]
    assert [event.timestamp_ms for event in events] == [150, 300]
    assert all("B" not in event.label and "V" not in event.label for event in events)


def test_parser_keeps_shift_inside_real_shortcut_and_suppresses_repeat():
    start = 2_000_000_000
    lines = []
    lines += _event("KeyPress", 37, start + 100_000_000)
    lines += _event("KeyPress", 50, start + 110_000_000)
    lines += _event("KeyPress", 55, start + 120_000_000)
    lines += _event("KeyRelease", 55, start + 130_000_000)
    lines += _event("KeyPress", 55, start + 150_000_000)

    events = parse_timestamped_xinput(
        "\n".join(lines),
        KEYMAP,
        video_start_monotonic_ns=start,
    )

    assert [event.label for event in events] == ["Ctrl + Shift + V"]


def test_parser_accepts_raw_xi2_key_events():
    start = 3_000_000_000
    lines = []
    lines += _raw_event("KeyPress", 37, start + 100_000_000)
    lines += _raw_event("KeyPress", 38, start + 120_000_000)

    events = parse_timestamped_xinput(
        "\n".join(lines),
        KEYMAP,
        video_start_monotonic_ns=start,
    )

    assert [event.label for event in events] == ["Ctrl + A"]


def test_ass_renderer_stacks_two_recent_shortcuts_and_writes_jsonl(tmp_path):
    events = [
        KeyOverlayEvent(100, ("Ctrl", "A"), "Ctrl + A"),
        KeyOverlayEvent(500, ("Enter",), "Enter"),
    ]

    ass = render_key_overlay_ass(events)
    output = tmp_path / "key_events.jsonl"
    write_key_events(output, events)

    assert "PlayResX: 1920" in ass
    assert r"Ctrl + A\NEnter" in ass
    assert "Dialogue:" in ass
    records = [json.loads(line) for line in output.read_text().splitlines()]
    assert records[0]["keys"] == ["Ctrl", "A"]
    assert records[1]["timestamp_ms"] == 500


def test_pointer_parser_distinguishes_clicks_scroll_and_omits_drag():
    start = 4_000_000_000
    lines = []
    lines += _button_event("ButtonPress", 1, start + 100_000_000, 100, 200)
    lines += _button_event("ButtonRelease", 1, start + 140_000_000, 101, 201)
    lines += _button_event("ButtonPress", 1, start + 300_000_000, 103, 202)
    lines += _button_event("ButtonRelease", 1, start + 340_000_000, 103, 202)
    lines += _button_event("ButtonPress", 3, start + 900_000_000, 400, 300)
    lines += _button_event("ButtonRelease", 3, start + 940_000_000, 400, 300)
    lines += _button_event("ButtonPress", 4, start + 1_000_000_000, 500, 350)
    lines += _button_event("ButtonRelease", 4, start + 1_010_000_000, 500, 350)
    lines += _button_event("ButtonPress", 4, start + 1_100_000_000, 500, 350)
    lines += _button_event("ButtonRelease", 4, start + 1_110_000_000, 500, 350)
    lines += _button_event("ButtonPress", 5, start + 1_300_000_000, 500, 350)
    lines += _button_event("ButtonRelease", 5, start + 1_310_000_000, 500, 350)
    lines += _button_event("ButtonPress", 1, start + 1_500_000_000, 10, 10)
    lines += _button_event("ButtonRelease", 1, start + 1_600_000_000, 100, 100)

    events = parse_timestamped_pointer_events(
        "\n".join(lines),
        video_start_monotonic_ns=start,
    )

    assert [event.action for event in events] == [
        "double_click",
        "right_click",
        "scroll_up",
        "scroll_down",
    ]
    assert events[0].label == "Double Click"
    assert (events[0].x, events[0].y) == (103, 202)


def test_pointer_parser_accepts_split_coordinates_and_event_boundaries():
    start = 5_000_000_000
    lines = [
        _line(start + 100_000_000, "EVENT type 4 (ButtonPress)"),
        _line(start + 100_000_001, "    detail: 1"),
        _line(start + 100_000_002, "    root_x: 250.5"),
        _line(start + 100_000_003, "    root_y: 350.5"),
        _line(start + 110_000_000, "EVENT type 6 (Motion)"),
        _line(start + 110_000_001, "    root: 999.00/999.00"),
        _line(start + 120_000_000, "EVENT type 5 (ButtonRelease)"),
        _line(start + 120_000_001, "    detail: 1"),
        _line(start + 120_000_002, "    root_x: 251.0"),
        _line(start + 120_000_003, "    root_y: 351.0"),
    ]

    events = parse_timestamped_pointer_events(
        "\n".join(lines),
        video_start_monotonic_ns=start,
    )

    assert [(event.action, event.x, event.y) for event in events] == [
        ("left_click", 250, 350)
    ]


def test_ass_renderer_includes_pointer_labels_and_writes_jsonl(tmp_path):
    pointer_events = [
        PointerOverlayEvent(100, "left_click", 100, 200, "Left Click"),
        PointerOverlayEvent(500, "right_click", 300, 400, "Right Click"),
        PointerOverlayEvent(900, "scroll_down", 500, 600, "Scroll ↓"),
    ]

    ass = render_key_overlay_ass([], pointer_events=pointer_events)
    output = tmp_path / "pointer_events.jsonl"
    write_pointer_events(output, pointer_events)

    assert "Left Click" in ass
    assert "Right Click" in ass
    assert "Scroll ↓" in ass
    assert r"\pos(100,200)" in ass
    records = [json.loads(line) for line in output.read_text().splitlines()]
    assert records[0]["action"] == "left_click"
    assert records[2]["y"] == 600


class _FakeController:
    def __init__(self):
        self.commands = []
        self.files = {
            "/tmp/osworld-human-input.log": b"raw",
            "/tmp/osworld-human-input.timestamped.jsonl": b"timestamped",
            "/tmp/osworld-human-keymap.xmodmap": b"keymap",
            "/tmp/osworld-recording-with-keys.mp4": b"....ftyp....",
        }

    def execute_python_command(self, command):
        self.commands.append(command)
        if "osworld-key-capture.py" in command:
            return {"output": "1234"}
        if "key-capture-readiness" in command:
            return {"output": "ready"}
        if "key-capture-stop" in command:
            return {"output": "stopped"}
        if "recording-start-time" in command:
            return {"output": "987654321"}
        if "subprocess.Popen" in command and "ffmpeg" in command:
            return {"output": "5678"}
        if "/proc/5678" in command:
            return {"output": "done"}
        return {"output": "ok"}

    def get_file(self, path):
        return self.files.get(path)


def test_guest_capture_and_burn_helpers_preserve_expected_artifacts(tmp_path):
    controller = _FakeController()
    env = SimpleNamespace(controller=controller)

    assert start_guest_key_capture(env)
    assert guest_recording_start_monotonic_ns(env) == 987654321
    assert stop_guest_key_capture(env, tmp_path)
    ass_path = tmp_path / "key_overlay.ass"
    ass_path.write_text(render_key_overlay_ass([]), encoding="utf-8")
    video_path = tmp_path / "recording.mp4"
    burn_key_overlay_in_guest(env, ass_path, video_path)

    assert (tmp_path / "input_events.xinput.log").read_bytes() == b"raw"
    assert (tmp_path / "input_events.timestamped.jsonl").is_file()
    assert video_path.read_bytes() == b"....ftyp...."
    assert any(
        "ass=/tmp/osworld-key-overlay.ass" in item for item in controller.commands
    )
