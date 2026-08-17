"""Lazy getter exports for application-specific evaluator dependencies."""

from pathlib import Path

from desktop_env.evaluators.lazy_exports import (
    build_function_index,
    resolve_export,
)


_MODULE_ORDER = (
    "chrome",
    "file",
    "general",
    "gimp",
    "impress",
    "info",
    "misc",
    "replay",
    "vlc",
    "vscode",
    "calc",
)
_EXPORTS = build_function_index(Path(__file__).parent, __name__, _MODULE_ORDER)
_EXPORTS["get_url_path_parse"] = f"{__name__}.chrome"


def __getattr__(name: str):
    value = resolve_export(name, _EXPORTS)
    globals()[name] = value
    return value


def __dir__():
    return sorted(set(globals()) | set(_EXPORTS))
