"""Allowlisted UI-state setup profiles for Impress reference annotation."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any


SETUP_SCRIPTS = {
    "hide_slides_pane": (
        "import pyautogui,time; "
        "time.sleep(2); "
        "w,h=pyautogui.size(); pyautogui.click(w//2,h//2); "
        "pyautogui.press('esc'); time.sleep(0.3); "
        "pyautogui.press('f10'); time.sleep(0.3); "
        "pyautogui.press('right', presses=2, interval=0.1); time.sleep(0.3); "
        "pyautogui.press('down', presses=11, interval=0.1); "
        "pyautogui.press('enter'); time.sleep(1); print('setup-complete')"
    )
}


def apply_impress_setup_profiles(env: Any, profiles: Iterable[str]) -> list[str]:
    applied: list[str] = []
    for profile in profiles:
        script = SETUP_SCRIPTS.get(profile)
        if script is None:
            raise ValueError(f"Unknown Impress setup profile: {profile}")
        result = env.controller.execute_python_command(script)
        if not result:
            raise RuntimeError(f"Impress setup profile failed: {profile}")
        applied.append(profile)
    return applied
