"""Helpers for dependency-isolated evaluator namespaces."""

from __future__ import annotations

import ast
import importlib
from pathlib import Path
from typing import Iterable


def build_function_index(
    package_dir: Path,
    package_name: str,
    module_order: Iterable[str],
) -> dict[str, str]:
    """Index top-level functions without importing evaluator dependencies."""

    exports: dict[str, str] = {}
    for module_name in module_order:
        source_path = package_dir / f"{module_name}.py"
        tree = ast.parse(source_path.read_text(encoding="utf-8"), source_path.name)
        qualified_name = f"{package_name}.{module_name}"
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                exports[node.name] = qualified_name
    return exports


def resolve_export(name: str, exports: dict[str, str]):
    module_name = exports.get(name)
    if module_name is None:
        raise AttributeError(name)
    module = importlib.import_module(module_name)
    try:
        return getattr(module, name)
    except AttributeError as exc:
        raise AttributeError(name) from exc
