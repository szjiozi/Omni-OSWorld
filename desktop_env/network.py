"""Network helpers for direct host-to-VM controller traffic."""

from __future__ import annotations

import os
from typing import MutableMapping


def add_no_proxy_host(
    host: str,
    environ: MutableMapping[str, str] | None = None,
) -> str:
    """Add one VM host to both no-proxy variables without dropping user entries."""

    env = os.environ if environ is None else environ
    normalized_host = host.strip().strip("[]")
    if not normalized_host:
        raise ValueError("VM host must not be empty")

    entries: list[str] = []
    for name in ("NO_PROXY", "no_proxy"):
        entries.extend(
            entry.strip()
            for entry in env.get(name, "").split(",")
            if entry.strip()
        )
    entries.append(normalized_host)
    merged = ",".join(dict.fromkeys(entries))
    env["NO_PROXY"] = merged
    env["no_proxy"] = merged
    return merged
