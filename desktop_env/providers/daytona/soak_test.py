"""Run repeated Daytona replacement resets against one immutable snapshot."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from desktop_env.providers.daytona.config import OSWORLD_SNAPSHOT
from desktop_env.providers.daytona.manager import DaytonaVMManager
from desktop_env.providers.daytona.provider import DaytonaProvider
from desktop_env.providers.daytona.smoke_test import (
    _assert_office,
    _assert_platform,
    _assert_screenshot,
    _parse_ip_ports,
    _wait_for_old_sandbox_gone,
)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify repeated clean Daytona snapshot replacement resets."
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=10,
        help="Number of replacement resets after the initial launch (default: 10).",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("results/daytona_phase0_soak.json"),
        help="JSON report path.",
    )
    return parser.parse_args()


def _probe(provider: DaytonaProvider, vm_id: str, stage: str) -> dict[str, Any]:
    started = time.monotonic()
    provider.start_emulator(vm_id, headless=True)
    ports = _parse_ip_ports(provider.get_ip_address(vm_id))
    _assert_platform(ports, f"{stage}_platform")
    _assert_screenshot(ports)
    _assert_office(ports, f"{stage}_office")
    return {
        "sandbox_id": vm_id,
        "elapsed_seconds": time.monotonic() - started,
        "ports": {
            "server": ports.server,
            "chromium": ports.chromium,
            "vnc": ports.vnc,
            "vlc": ports.vlc,
        },
    }


def _write_report(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(tmp_path, path)


def main() -> int:
    args = _parse_args()
    if args.iterations < 1:
        raise SystemExit("--iterations must be at least 1")
    if not os.environ.get("DAYTONA_API_KEY"):
        print("[FAIL] preflight: DAYTONA_API_KEY not set", file=sys.stderr)
        return 2
    if not OSWORLD_SNAPSHOT:
        print(
            "[FAIL] preflight: DAYTONA_OSWORLD_SNAPSHOT not set",
            file=sys.stderr,
        )
        return 2

    manager = DaytonaVMManager()
    provider = DaytonaProvider(region=None)
    vm_id: str | None = None
    report: dict[str, Any] = {
        "schema_version": "1.0",
        "snapshot": OSWORLD_SNAPSHOT,
        "requested_resets": args.iterations,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "status": "running",
        "launches": [],
        "resets": [],
    }
    exit_code = 0

    try:
        vm_id = manager.get_vm_path(os_type="Ubuntu")
        report["launches"].append(_probe(provider, vm_id, "initial"))

        for reset_index in range(1, args.iterations + 1):
            old_vm_id = vm_id
            reset_started = time.monotonic()
            vm_id = provider.revert_to_snapshot(old_vm_id, OSWORLD_SNAPSHOT)
            old_status = _wait_for_old_sandbox_gone(old_vm_id)
            probe = _probe(provider, vm_id, f"reset_{reset_index}")
            report["resets"].append(
                {
                    "index": reset_index,
                    "old_sandbox_id": old_vm_id,
                    "new_sandbox_id": vm_id,
                    "old_sandbox_status": old_status,
                    "elapsed_seconds": time.monotonic() - reset_started,
                    "probe": probe,
                }
            )
            print(
                f"[PASS] reset {reset_index}/{args.iterations}: "
                f"{old_vm_id} -> {vm_id}"
            )

        report["status"] = "passed"
    except Exception as exc:  # noqa: BLE001 - persist the soak failure.
        report["status"] = "failed"
        report["error"] = f"{type(exc).__name__}: {exc}"
        print(f"[FAIL] soak: {exc}", file=sys.stderr)
        exit_code = 1
    finally:
        if vm_id is not None:
            try:
                provider.stop_emulator(vm_id)
            except Exception as exc:  # noqa: BLE001 - keep the original failure.
                report["teardown_error"] = f"{type(exc).__name__}: {exc}"
                if exit_code == 0:
                    exit_code = 1
                    report["status"] = "failed"
        report["finished_at"] = datetime.now(timezone.utc).isoformat()
        _write_report(args.report, report)
        print(f"Report: {args.report}")

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
