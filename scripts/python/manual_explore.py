#!/usr/bin/env python3
"""Start an OSWorld environment and keep it alive for manual exploration."""

from __future__ import annotations

import argparse
import signal
import sys
import time
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Start OSWorld without executing an agent action, print desktop access "
            "instructions, and keep the environment alive until you stop it."
        )
    )
    parser.add_argument(
        "--provider-name",
        "--provider_name",
        dest="provider_name",
        default="docker",
        help="OSWorld provider to use (default: docker).",
    )
    parser.add_argument(
        "--path-to-vm",
        "--path_to_vm",
        dest="path_to_vm",
        default=None,
        help="Optional existing VM image or provider-specific VM path.",
    )
    parser.add_argument(
        "--os-type",
        "--os_type",
        dest="os_type",
        default="Ubuntu",
        choices=("Ubuntu", "Windows"),
        help="Guest operating system (default: Ubuntu).",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Start a local hypervisor without its native GUI.",
    )
    parser.add_argument(
        "--ssh-host",
        default=None,
        help=(
            "SSH config alias for the machine running this script. When supplied, "
            "print a copy-pasteable noVNC tunnel command."
        ),
    )
    parser.add_argument(
        "--local-vnc-port",
        type=int,
        default=8006,
        help="Local Mac port to use in the suggested SSH tunnel (default: 8006).",
    )
    return parser.parse_args()


def _format_url_host(host: str) -> str:
    host = host.strip("[]")
    return f"[{host}]" if ":" in host else host


def print_access_instructions(env: Any, args: argparse.Namespace) -> None:
    provider = args.provider_name.lower()
    vm_host = str(env.vm_ip)

    print("\nOSWorld is ready.")
    print(f"Provider: {provider}")
    print(f"VM/controller host: {vm_host}")
    print(f"OSWorld server port: {env.server_port}")
    print(f"VNC port reported by provider: {env.vnc_port}")

    if provider in {"vmware", "virtualbox"} and not args.headless:
        print("\nUse the VMware/VirtualBox window for direct manual interaction.")
        print("The environment remains running until this script exits.")
        return

    if vm_host in {"localhost", "127.0.0.1", "::1"}:
        if args.ssh_host:
            print("\nOn your Mac, open a second terminal and run:")
            print(
                f"  ssh -N -L {args.local_vnc_port}:127.0.0.1:{env.vnc_port} "
                f"{args.ssh_host}"
            )
            print("\nThen open this URL on your Mac:")
            print(f"  http://127.0.0.1:{args.local_vnc_port}")
        else:
            print("\nOpen this URL on the machine running the script:")
            print(f"  http://127.0.0.1:{env.vnc_port}")
        return

    if provider in {"aws", "aliyun", "volcengine", "fastvm"}:
        print("\nOpen the provider's noVNC URL:")
        print(f"  http://{_format_url_host(vm_host)}:5910/vnc.html")
        return

    print("\nTry the provider-reported VNC endpoint:")
    print(f"  http://{_format_url_host(vm_host)}:{env.vnc_port}")


def wait_until_stopped() -> None:
    if sys.stdin.isatty():
        input("\nPress Enter to stop the environment and clean up...\n")
        return

    print("\nNo interactive terminal detected. Press Ctrl-C or send SIGTERM to stop.")
    while True:
        time.sleep(3600)


def main() -> int:
    args = parse_args()

    if not 1 <= args.local_vnc_port <= 65535:
        raise SystemExit("--local-vnc-port must be between 1 and 65535")

    # Import after argument parsing so `--help` works before heavy dependencies
    # are installed and the repository can be inspected from any directory.
    from desktop_env.desktop_env import DesktopEnv

    env = None
    try:
        print("Starting OSWorld environment...")
        env = DesktopEnv(
            provider_name=args.provider_name,
            path_to_vm=args.path_to_vm,
            os_type=args.os_type,
            action_space="pyautogui",
            headless=args.headless,
            require_a11y_tree=False,
        )

        print("Checking that the desktop is responsive...")
        env.reset(task_config=None)
        print_access_instructions(env, args)
        wait_until_stopped()
        return 0
    except KeyboardInterrupt:
        print("\nStop requested.")
        return 130
    finally:
        if env is not None:
            print("Stopping OSWorld environment...")
            env.close()
            print("Environment stopped.")


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, lambda _signum, _frame: sys.exit(0))
    raise SystemExit(main())
