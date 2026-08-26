"""Capture X11 input events and render privacy-safe video overlays."""

from __future__ import annotations

import base64
import json
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence


GUEST_RAW_LOG = "/tmp/osworld-human-input.log"
GUEST_TIMESTAMPED_LOG = "/tmp/osworld-human-input.timestamped.jsonl"
GUEST_KEYMAP = "/tmp/osworld-human-keymap.xmodmap"
GUEST_CAPTURE_PID = "/tmp/osworld-human-input.pid"
GUEST_CAPTURE_SCRIPT = "/tmp/osworld-key-capture.py"
GUEST_CAPTURE_STDERR = "/tmp/osworld-key-capture.stderr.log"
GUEST_CAPTURE_DONE = "/tmp/osworld-human-input.done"
GUEST_RECORDING = "/tmp/recording.mp4"
GUEST_OVERLAY_ASS = "/tmp/osworld-key-overlay.ass"
GUEST_OVERLAY_VIDEO = "/tmp/osworld-recording-with-keys.mp4"
GUEST_OVERLAY_STDERR = "/tmp/osworld-key-overlay.ffmpeg.log"

EVENT_HEADER = re.compile(r"EVENT type \d+ \((?:Raw)?(KeyPress|KeyRelease)\)")
EVENT_DETAIL = re.compile(r"^\s*detail:\s*(\d+)")
ANY_EVENT_HEADER = re.compile(r"EVENT type \d+ \(")
BUTTON_EVENT_HEADER = re.compile(r"EVENT type \d+ \((ButtonPress|ButtonRelease)\)")
POINTER_COORDINATE = re.compile(
    r"^\s*(root_x|root_y|event_x|event_y):\s*(-?\d+(?:\.\d+)?)"
)
POINTER_COORDINATE_PAIR = re.compile(
    r"^\s*(root|event):\s*(-?\d+(?:\.\d+)?)/(-?\d+(?:\.\d+)?)"
)
KEYMAP_LINE = re.compile(r"^keycode\s+(\d+)\s+=\s*(.*)$")

MODIFIER_NAMES = {
    "Control_L": "Ctrl",
    "Control_R": "Ctrl",
    "Shift_L": "Shift",
    "Shift_R": "Shift",
    "Alt_L": "Alt",
    "Alt_R": "Alt",
    "Meta_L": "Alt",
    "Meta_R": "Alt",
    "Super_L": "Super",
    "Super_R": "Super",
    "ISO_Level3_Shift": "AltGr",
}
MODIFIER_ORDER = ("Ctrl", "Shift", "Alt", "Super", "AltGr")
SHORTCUT_MODIFIERS = {"Ctrl", "Alt", "Super"}
SPECIAL_KEYS = {
    "Return": "Enter",
    "KP_Enter": "Enter",
    "Escape": "Esc",
    "Tab": "Tab",
    "ISO_Left_Tab": "Tab",
    "BackSpace": "Backspace",
    "Delete": "Delete",
    "Left": "Left",
    "Right": "Right",
    "Up": "Up",
    "Down": "Down",
    "Home": "Home",
    "End": "End",
    "Page_Up": "Page Up",
    "Page_Down": "Page Down",
    "Insert": "Insert",
    "Print": "Print Screen",
}
PRINTABLE_KEY_NAMES = {
    "space": "Space",
    "plus": "+",
    "minus": "-",
    "equal": "=",
    "comma": ",",
    "period": ".",
    "slash": "/",
    "semicolon": ";",
    "apostrophe": "'",
    "bracketleft": "[",
    "bracketright": "]",
    "grave": "`",
    "KP_Add": "+",
    "KP_Subtract": "-",
    "KP_Multiply": "*",
    "KP_Divide": "/",
}


@dataclass(frozen=True)
class KeyOverlayEvent:
    timestamp_ms: int
    keys: tuple[str, ...]
    label: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": "1.0",
            "timestamp_ms": self.timestamp_ms,
            "event": "shortcut" if len(self.keys) > 1 else "special_key",
            "keys": list(self.keys),
            "label": self.label,
        }


@dataclass(frozen=True)
class PointerOverlayEvent:
    timestamp_ms: int
    action: str
    x: int
    y: int
    label: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": "1.0",
            "timestamp_ms": self.timestamp_ms,
            "event": "pointer",
            "action": self.action,
            "x": self.x,
            "y": self.y,
            "label": self.label,
        }


_GUEST_CAPTURE_SOURCE = r"""
import json
import os
import signal
import subprocess
import time

RAW_LOG = "/tmp/osworld-human-input.log"
TIMESTAMPED_LOG = "/tmp/osworld-human-input.timestamped.jsonl"
KEYMAP = "/tmp/osworld-human-keymap.xmodmap"
DONE = "/tmp/osworld-human-input.done"

env = dict(os.environ, DISPLAY=":0")
keymap = subprocess.run(
    ["xmodmap", "-pke"], env=env, capture_output=True, text=True, check=True
).stdout
with open(KEYMAP, "w", encoding="utf-8") as stream:
    stream.write(keymap)

proc = subprocess.Popen(
    ["stdbuf", "-oL", "xinput", "test-xi2", "--root"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1,
    env=env,
)

def stop(_signum, _frame):
    if proc.poll() is None:
        proc.terminate()

signal.signal(signal.SIGTERM, stop)
signal.signal(signal.SIGINT, stop)

with open(RAW_LOG, "w", encoding="utf-8", buffering=1) as raw_stream, open(
    TIMESTAMPED_LOG, "w", encoding="utf-8", buffering=1
) as timestamped_stream:
    for line in proc.stdout:
        monotonic_ns = time.monotonic_ns()
        raw_stream.write(line)
        timestamped_stream.write(
            json.dumps(
                {"monotonic_ns": monotonic_ns, "line": line.rstrip("\n")},
                ensure_ascii=False,
            )
            + "\n"
        )

if proc.poll() is None:
    proc.terminate()
proc.wait(timeout=5)
with open(DONE, "w", encoding="utf-8") as stream:
    stream.write(str(time.monotonic_ns()))
""".strip()

_GUEST_RECORDING_START_SOURCE = r"""
import json
from pathlib import Path

data = json.loads(
    Path("/tmp/osworld-reference-recording-start.json").read_text(encoding="utf-8")
)
print(int(data["first_frame_monotonic_ns"]))
""".strip()


def start_guest_key_capture(env: Any) -> bool:
    """Start a timestamped XInput capture process inside the guest."""

    encoded = base64.b64encode(_GUEST_CAPTURE_SOURCE.encode("utf-8")).decode("ascii")
    command = (
        "import base64,os,pathlib,subprocess,sys; "
        f"stale={[GUEST_RAW_LOG, GUEST_TIMESTAMPED_LOG, GUEST_KEYMAP, GUEST_CAPTURE_PID, GUEST_CAPTURE_DONE]!r}; "
        "[(pathlib.Path(item).unlink()) for item in stale "
        "if pathlib.Path(item).exists()]; "
        f"script=pathlib.Path({GUEST_CAPTURE_SCRIPT!r}); "
        f"script.write_bytes(base64.b64decode({encoded!r})); "
        f"stderr=open({GUEST_CAPTURE_STDERR!r},'w'); "
        "proc=subprocess.Popen([sys.executable,str(script)],"
        "stdout=stderr,stderr=stderr,start_new_session=True,"
        "env=dict(os.environ,DISPLAY=':0')); "
        f"pathlib.Path({GUEST_CAPTURE_PID!r}).write_text(str(proc.pid)); "
        "print(proc.pid)"
    )
    result = env.controller.execute_python_command(command)
    output = result.get("output", "").strip() if result else ""
    if not output.isdigit():
        return False
    pid = int(output)
    readiness_source = f"""
import pathlib
import time

pid = {pid}
for _ in range(50):
    if (
        pathlib.Path({GUEST_KEYMAP!r}).is_file()
        and pathlib.Path({GUEST_TIMESTAMPED_LOG!r}).is_file()
    ):
        print("ready")
        break
    if not pathlib.Path(f"/proc/{{pid}}").exists():
        print("failed")
        break
    time.sleep(0.1)
else:
    print("timeout")
""".strip()
    readiness_encoded = base64.b64encode(readiness_source.encode("utf-8")).decode(
        "ascii"
    )
    readiness = env.controller.execute_python_command(
        "import base64; "
        f"exec(compile(base64.b64decode({readiness_encoded!r}),"
        "'<key-capture-readiness>','exec'))"
    )
    return bool(readiness and readiness.get("output", "").strip() == "ready")


def stop_guest_key_capture(env: Any, output_dir: Path) -> bool:
    """Stop guest capture and retrieve raw, timestamped, and keymap artifacts."""

    stop_source = f"""
import os
import pathlib
import signal
import time

pid = int(pathlib.Path({GUEST_CAPTURE_PID!r}).read_text())
try:
    os.kill(pid, signal.SIGTERM)
except ProcessLookupError:
    pass
for _ in range(50):
    if pathlib.Path({GUEST_CAPTURE_DONE!r}).is_file():
        print("stopped")
        break
    time.sleep(0.1)
else:
    print("timeout")
""".strip()
    encoded = base64.b64encode(stop_source.encode("utf-8")).decode("ascii")
    result = env.controller.execute_python_command(
        "import base64; "
        f"exec(compile(base64.b64decode({encoded!r}),"
        "'<key-capture-stop>','exec'))"
    )
    completed = bool(result and result.get("output", "").strip() == "stopped")
    files = {
        GUEST_RAW_LOG: output_dir / "input_events.xinput.log",
        GUEST_TIMESTAMPED_LOG: output_dir / "input_events.timestamped.jsonl",
        GUEST_KEYMAP: output_dir / "input_keymap.xmodmap",
    }
    retrieved = True
    for guest_path, local_path in files.items():
        content = env.controller.get_file(guest_path)
        if content is None:
            retrieved = False
            continue
        local_path.write_bytes(content)
    return completed and retrieved


def guest_recording_start_monotonic_ns(env: Any) -> int:
    """Read the first encoded frame time in the guest monotonic clock domain."""

    encoded = base64.b64encode(_GUEST_RECORDING_START_SOURCE.encode("utf-8")).decode(
        "ascii"
    )
    command = (
        "import base64; "
        f"exec(compile(base64.b64decode({encoded!r}),"
        "'<recording-start-time>','exec'))"
    )
    result = env.controller.execute_python_command(command)
    output = result.get("output", "").strip() if result else ""
    if not output.isdigit():
        raise RuntimeError("Could not determine guest ffmpeg start time")
    return int(output)


def parse_xmodmap(text: str) -> dict[int, tuple[str, ...]]:
    mapping: dict[int, tuple[str, ...]] = {}
    for line in text.splitlines():
        match = KEYMAP_LINE.match(line.strip())
        if not match:
            continue
        symbols = tuple(
            symbol for symbol in match.group(2).split() if symbol != "NoSymbol"
        )
        if symbols:
            mapping[int(match.group(1))] = symbols
    return mapping


def _symbol_for_keycode(
    keycode: int, mapping: dict[int, tuple[str, ...]], modifiers: set[str]
) -> str | None:
    symbols = mapping.get(keycode)
    if not symbols:
        return None
    if "Shift" in modifiers and len(symbols) > 1:
        return symbols[1]
    return symbols[0]


def _display_key(symbol: str) -> str | None:
    if symbol in SPECIAL_KEYS:
        return SPECIAL_KEYS[symbol]
    if symbol in PRINTABLE_KEY_NAMES:
        return PRINTABLE_KEY_NAMES[symbol]
    if re.fullmatch(r"F(?:[1-9]|1[0-2])", symbol):
        return symbol
    if len(symbol) == 1 and symbol.isprintable():
        return symbol.upper() if symbol.isalpha() else symbol
    return None


def parse_timestamped_xinput(
    timestamped_text: str,
    keymap_text: str,
    *,
    video_start_monotonic_ns: int,
    repeat_suppression_ms: int = 80,
) -> list[KeyOverlayEvent]:
    """Normalize timestamped XInput lines into shortcut/special-key events."""

    mapping = parse_xmodmap(keymap_text)
    pending: tuple[str, int] | None = None
    pressed_keycodes: set[int] = set()
    modifiers: set[str] = set()
    modifier_by_keycode: dict[int, str] = {}
    events: list[KeyOverlayEvent] = []

    for raw_entry in timestamped_text.splitlines():
        if not raw_entry.strip():
            continue
        entry = json.loads(raw_entry)
        line = entry["line"]
        header = EVENT_HEADER.search(line)
        if header:
            pending = (header.group(1), int(entry["monotonic_ns"]))
            continue
        detail = EVENT_DETAIL.match(line)
        if pending is None or not detail:
            continue
        event_type, event_ns = pending
        pending = None
        keycode = int(detail.group(1))
        base_symbol = _symbol_for_keycode(keycode, mapping, set())
        modifier = MODIFIER_NAMES.get(base_symbol or "")

        if event_type == "KeyRelease":
            pressed_keycodes.discard(keycode)
            released_modifier = modifier_by_keycode.pop(keycode, modifier)
            if released_modifier:
                modifiers.discard(released_modifier)
            continue

        if keycode in pressed_keycodes:
            continue
        pressed_keycodes.add(keycode)
        if modifier:
            modifier_by_keycode[keycode] = modifier
            modifiers.add(modifier)
            continue

        symbol = _symbol_for_keycode(keycode, mapping, modifiers)
        if symbol is None:
            continue
        display_key = _display_key(symbol)
        if display_key is None:
            continue
        is_special = symbol in SPECIAL_KEYS or re.fullmatch(
            r"F(?:[1-9]|1[0-2])", symbol
        )
        ordered_modifiers = tuple(item for item in MODIFIER_ORDER if item in modifiers)
        if not is_special and not SHORTCUT_MODIFIERS.intersection(modifiers):
            continue
        if event_ns < video_start_monotonic_ns:
            continue
        keys = (*ordered_modifiers, display_key)
        timestamp_ms = round((event_ns - video_start_monotonic_ns) / 1_000_000)
        label = " + ".join(keys)
        if (
            events
            and events[-1].label == label
            and timestamp_ms - events[-1].timestamp_ms < repeat_suppression_ms
        ):
            continue
        events.append(
            KeyOverlayEvent(timestamp_ms=timestamp_ms, keys=keys, label=label)
        )
    return events


def _timestamped_xinput_blocks(
    timestamped_text: str,
) -> list[tuple[str, int, dict[str, float | int]]]:
    blocks: list[tuple[str, int, dict[str, float | int]]] = []
    pending: tuple[str, int, dict[str, float | int]] | None = None
    for raw_entry in timestamped_text.splitlines():
        if not raw_entry.strip():
            continue
        entry = json.loads(raw_entry)
        line = entry["line"]
        header = BUTTON_EVENT_HEADER.search(line)
        if ANY_EVENT_HEADER.search(line):
            if pending is not None:
                blocks.append(pending)
            pending = (
                (header.group(1), int(entry["monotonic_ns"]), {})
                if header
                else None
            )
            continue
        if pending is None:
            continue
        detail = EVENT_DETAIL.match(line)
        coordinate = POINTER_COORDINATE.match(line)
        coordinate_pair = POINTER_COORDINATE_PAIR.match(line)
        if detail:
            pending[2]["detail"] = int(detail.group(1))
        elif coordinate:
            pending[2][coordinate.group(1)] = float(coordinate.group(2))
        elif coordinate_pair:
            prefix = coordinate_pair.group(1)
            pending[2][f"{prefix}_x"] = float(coordinate_pair.group(2))
            pending[2][f"{prefix}_y"] = float(coordinate_pair.group(3))
    if pending is not None:
        blocks.append(pending)
    return blocks


def _timestamped_modifier_states(
    timestamped_text: str,
    keymap_text: str,
) -> list[tuple[int, tuple[str, ...]]]:
    mapping = parse_xmodmap(keymap_text)
    pending: tuple[str, int] | None = None
    modifier_by_keycode: dict[int, str] = {}
    states: list[tuple[int, tuple[str, ...]]] = []
    for raw_entry in timestamped_text.splitlines():
        if not raw_entry.strip():
            continue
        entry = json.loads(raw_entry)
        line = entry["line"]
        header = EVENT_HEADER.search(line)
        if header:
            pending = (header.group(1), int(entry["monotonic_ns"]))
            continue
        if ANY_EVENT_HEADER.search(line):
            pending = None
            continue
        detail = EVENT_DETAIL.match(line)
        if pending is None or not detail:
            continue
        event_type, event_ns = pending
        pending = None
        keycode = int(detail.group(1))
        base_symbol = _symbol_for_keycode(keycode, mapping, set())
        modifier = MODIFIER_NAMES.get(base_symbol or "")
        if event_type == "KeyPress" and modifier:
            modifier_by_keycode[keycode] = modifier
        elif event_type == "KeyRelease":
            modifier_by_keycode.pop(keycode, None)
        else:
            continue
        active = set(modifier_by_keycode.values())
        ordered = tuple(item for item in MODIFIER_ORDER if item in active)
        if not states or states[-1][1] != ordered:
            states.append((event_ns, ordered))
    return states


def parse_timestamped_pointer_events(
    timestamped_text: str,
    *,
    video_start_monotonic_ns: int,
    keymap_text: str | None = None,
    drag_threshold_px: int = 10,
    double_click_ms: int = 500,
    double_click_distance_px: int = 12,
    scroll_suppression_ms: int = 180,
) -> list[PointerOverlayEvent]:
    """Normalize XI2 pointer events while deliberately omitting drags."""

    if drag_threshold_px < 0 or double_click_ms <= 0:
        raise ValueError("Pointer event thresholds are invalid")
    pressed: dict[int, tuple[int, int, int, tuple[str, ...]]] = {}
    events: list[PointerOverlayEvent] = []
    last_left: tuple[int, int, int, int] | None = None
    modifier_states = (
        _timestamped_modifier_states(timestamped_text, keymap_text)
        if keymap_text
        else []
    )
    modifier_index = 0
    active_modifiers: tuple[str, ...] = ()

    def modifiers_at(event_ns: int) -> tuple[str, ...]:
        nonlocal modifier_index, active_modifiers
        while (
            modifier_index < len(modifier_states)
            and modifier_states[modifier_index][0] <= event_ns
        ):
            active_modifiers = modifier_states[modifier_index][1]
            modifier_index += 1
        return active_modifiers

    def pointer_label(action: str, modifiers: tuple[str, ...]) -> str:
        return " + ".join((*modifiers, action))

    for event_type, event_ns, fields in _timestamped_xinput_blocks(
        timestamped_text
    ):
        button = fields.get("detail")
        x_value = fields.get("root_x", fields.get("event_x"))
        y_value = fields.get("root_y", fields.get("event_y"))
        if not isinstance(button, int) or x_value is None or y_value is None:
            continue
        x = round(float(x_value))
        y = round(float(y_value))
        if event_ns < video_start_monotonic_ns:
            continue
        timestamp_ms = round((event_ns - video_start_monotonic_ns) / 1_000_000)
        event_modifiers = modifiers_at(event_ns)

        if button in {4, 5} and event_type == "ButtonPress":
            action = "scroll_up" if button == 4 else "scroll_down"
            base_label = "Scroll ↑" if button == 4 else "Scroll ↓"
            label = pointer_label(base_label, event_modifiers)
            if (
                events
                and events[-1].action == action
                and timestamp_ms - events[-1].timestamp_ms < scroll_suppression_ms
            ):
                continue
            events.append(PointerOverlayEvent(timestamp_ms, action, x, y, label))
            continue

        if button not in {1, 3}:
            continue
        if event_type == "ButtonPress":
            pressed[button] = (event_ns, x, y, event_modifiers)
            continue
        press = pressed.pop(button, None)
        if press is None:
            continue
        press_ns, press_x, press_y, press_modifiers = press
        if (x - press_x) ** 2 + (y - press_y) ** 2 > drag_threshold_px**2:
            continue
        press_timestamp_ms = round(
            (press_ns - video_start_monotonic_ns) / 1_000_000
        )
        if button == 3:
            events.append(
                PointerOverlayEvent(
                    press_timestamp_ms,
                    "right_click",
                    press_x,
                    press_y,
                    pointer_label("Right Click", press_modifiers),
                )
            )
            continue

        if last_left is not None:
            previous_ms, previous_x, previous_y, previous_index = last_left
            close_in_time = press_timestamp_ms - previous_ms <= double_click_ms
            close_in_space = (
                (press_x - previous_x) ** 2 + (press_y - previous_y) ** 2
                <= double_click_distance_px**2
            )
            if close_in_time and close_in_space:
                events[previous_index] = PointerOverlayEvent(
                    press_timestamp_ms,
                    "double_click",
                    press_x,
                    press_y,
                    pointer_label("Double Click", press_modifiers),
                )
                last_left = None
                continue
        events.append(
            PointerOverlayEvent(
                press_timestamp_ms,
                "left_click",
                press_x,
                press_y,
                pointer_label("Left Click", press_modifiers),
            )
        )
        last_left = (press_timestamp_ms, press_x, press_y, len(events) - 1)
    return sorted(events, key=lambda event: event.timestamp_ms)


def write_key_events(path: Path, events: Sequence[KeyOverlayEvent]) -> None:
    content = "".join(
        json.dumps(event.to_dict(), ensure_ascii=False) + "\n" for event in events
    )
    path.write_text(content, encoding="utf-8")


def write_pointer_events(path: Path, events: Sequence[PointerOverlayEvent]) -> None:
    content = "".join(
        json.dumps(event.to_dict(), ensure_ascii=False) + "\n" for event in events
    )
    path.write_text(content, encoding="utf-8")


def _ass_time(milliseconds: int) -> str:
    centiseconds = max(0, milliseconds) // 10
    hours, remainder = divmod(centiseconds, 360_000)
    minutes, remainder = divmod(remainder, 6_000)
    seconds, remainder = divmod(remainder, 100)
    return f"{hours}:{minutes:02d}:{seconds:02d}.{remainder:02d}"


def _ass_escape(value: str) -> str:
    return value.replace("\\", r"\\").replace("{", r"\{").replace("}", r"\}")


def render_key_overlay_ass(
    events: Sequence[KeyOverlayEvent],
    *,
    pointer_events: Sequence[PointerOverlayEvent] = (),
    width: int = 1920,
    height: int = 1080,
    display_duration_ms: int = 1200,
    max_visible: int = 2,
) -> str:
    """Render bottom-centered, semi-transparent shortcut subtitles."""

    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {width}
PlayResY: {height}
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: KeyOverlay,DejaVu Sans,42,&H00FFFFFF,&H00FFFFFF,&H70000000,&H70000000,-1,0,0,0,100,100,1,0,3,14,0,2,80,80,65,1
Style: PointerOverlay,DejaVu Sans,28,&H00FFFFFF,&H00FFFFFF,&H70000000,&H70000000,-1,0,0,0,100,100,0,0,3,8,0,7,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    if not events and not pointer_events:
        return header
    boundaries = sorted(
        {
            boundary
            for event in events
            for boundary in (
                event.timestamp_ms,
                event.timestamp_ms + display_duration_ms,
            )
        }
    )
    dialogues: list[str] = []
    for start, end in zip(boundaries, boundaries[1:]):
        active = [
            event
            for event in events
            if event.timestamp_ms <= start
            and start < event.timestamp_ms + display_duration_ms
        ][-max_visible:]
        if not active or end <= start:
            continue
        label = r"\N".join(_ass_escape(event.label) for event in active)
        dialogues.append(
            f"Dialogue: 0,{_ass_time(start)},{_ass_time(end)},"
            f"KeyOverlay,,0,0,0,,{label}"
        )
    pointer_colors = {
        "left_click": "&H00ED802F",
        "double_click": "&H00ED802F",
        "right_click": "&H004A99F2",
        "scroll_up": "&H004BC27A",
        "scroll_down": "&H004BC27A",
    }
    pointer_glyphs = {
        "left_click": "○",
        "double_click": "◎",
        "right_click": "○",
        "scroll_up": "↑",
        "scroll_down": "↓",
    }
    for event in pointer_events:
        x = min(max(0, event.x), width)
        y = min(max(0, event.y), height)
        end_ms = event.timestamp_ms + (
            950 if event.action in {"double_click", "right_click"} else 700
        )
        color = pointer_colors[event.action]
        glyph = pointer_glyphs[event.action]
        glyph_text = (
            rf"{{\an5\pos({x},{y})\fs54\1c{color}\bord3\shad0}}{glyph}"
        )
        label_x = min(width - 20, x + 28)
        label_y = max(20, y - 34)
        label_text = (
            rf"{{\an7\pos({label_x},{label_y})\1c{color}}}"
            + _ass_escape(event.label)
        )
        for text in (glyph_text, label_text):
            dialogues.append(
                f"Dialogue: 1,{_ass_time(event.timestamp_ms)},{_ass_time(end_ms)},"
                f"PointerOverlay,,0,0,0,,{text}"
            )
    return header + "\n".join(dialogues) + "\n"


def burn_key_overlay_in_guest(env: Any, ass_path: Path, output_path: Path) -> None:
    """Burn an ASS overlay with guest ffmpeg and download the resulting MP4."""

    encoded = base64.b64encode(ass_path.read_bytes()).decode("ascii")
    command = (
        "import base64,pathlib,subprocess; "
        f"pathlib.Path({GUEST_OVERLAY_ASS!r}).write_bytes("
        f"base64.b64decode({encoded!r})); "
        f"pathlib.Path({GUEST_OVERLAY_VIDEO!r}).unlink(missing_ok=True); "
        f"stderr=open({GUEST_OVERLAY_STDERR!r},'wb'); "
        "proc=subprocess.Popen(["
        "'ffmpeg','-y','-i',"
        f"{GUEST_RECORDING!r},'-vf','ass={GUEST_OVERLAY_ASS}',"
        "'-c:v','libx264','-preset','veryfast','-crf','18',"
        "'-an','-movflags','+faststart',"
        f"{GUEST_OVERLAY_VIDEO!r}],stdout=subprocess.DEVNULL,stderr=stderr,"
        "start_new_session=True); print(proc.pid)"
    )
    result = env.controller.execute_python_command(command)
    output = result.get("output", "").strip() if result else ""
    if not output.isdigit():
        raise RuntimeError("Guest ffmpeg returned no overlay process ID")
    pid = int(output)
    for _ in range(300):
        poll = env.controller.execute_python_command(
            "import pathlib; "
            f"print('running' if pathlib.Path('/proc/{pid}').exists() else 'done')"
        )
        state = poll.get("output", "").strip() if poll else ""
        if state == "done":
            break
        if state != "running":
            raise RuntimeError("Could not poll the guest overlay process")
        time.sleep(2)
    else:
        env.controller.execute_python_command(
            f"import os,signal; os.kill({pid},signal.SIGKILL)"
        )
        raise RuntimeError("Guest key-overlay encoding exceeded 600 seconds")
    content = env.controller.get_file(GUEST_OVERLAY_VIDEO)
    if not content or b"ftyp" not in content[:32]:
        stderr = env.controller.get_file(GUEST_OVERLAY_STDERR) or b""
        message = stderr.decode("utf-8", errors="replace")[-4000:]
        raise RuntimeError(
            "Guest key-overlay video is missing or invalid. ffmpeg stderr: " + message
        )
    output_path.write_bytes(content)
