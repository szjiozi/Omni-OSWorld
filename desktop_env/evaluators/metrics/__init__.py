"""Lazy metric exports.

OSWorld supports many application-specific evaluators with large, independent
dependency trees. Resolve a metric only when a task requests it so a Calc task
does not require the OCR, audio, video, PDF, and browser stacks.
"""

from pathlib import Path

from desktop_env.evaluators.lazy_exports import (
    build_function_index,
    resolve_export,
)


_MODULE_ORDER = (
    "basic_os",
    "chrome",
    "docs",
    "general",
    "gimp",
    "libreoffice",
    "others",
    "pdf",
    "slides",
    "table",
    "thunderbird",
    "vlc",
    "vscode",
)
_EXPORTS = build_function_index(Path(__file__).parent, __name__, _MODULE_ORDER)
_EXPORTS.update(
    {
        "compare_pptx_animation_timelines": (
            "desktop_env.evaluators.pptx_animation"
        ),
        "compare_pptx_static_content": "desktop_env.evaluators.pptx_animation",
    }
)


def infeasible():
    pass


def __getattr__(name: str):
    value = resolve_export(name, _EXPORTS)
    globals()[name] = value
    return value


def __dir__():
    return sorted(set(globals()) | set(_EXPORTS))
