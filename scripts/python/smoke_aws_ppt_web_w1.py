#!/usr/bin/env python3
"""Launch one OSWorld AWS VM, probe browser services, and clean up safely."""

from __future__ import annotations

import argparse
import json
import os
import time
import urllib.parse
from datetime import datetime, timedelta, timezone

import boto3
import requests

from desktop_env.providers.aws.manager import _allocate_vm
from desktop_env.providers.aws.scheduler_utils import (
    delete_instance_termination_schedules,
)


PROJECT_TAG = "OSWorld-PPT-Web"
PROBE_TIMEOUT_SECONDS = 900
DIRECT_HTTP_SESSION = requests.Session()
DIRECT_HTTP_SESSION.trust_env = False


def _request(
    url: str,
    *,
    method: str = "GET",
    timeout: int = 10,
    body: bytes | None = None,
    headers: dict[str, str] | None = None,
    read_limit: int | None = None,
) -> bytes:
    response = DIRECT_HTTP_SESSION.request(
        method,
        url,
        data=body,
        headers=headers or {},
        timeout=timeout,
    )
    if response.status_code != 200:
        raise RuntimeError(f"Unexpected HTTP status {response.status_code}")
    if method == "HEAD":
        return b""
    if read_limit is not None:
        return response.content[:read_limit]
    return response.content


def _wait_for_url(
    name: str,
    url: str,
    deadline: float,
    *,
    method: str = "GET",
    read_limit: int | None = None,
) -> bytes:
    last_error: Exception | None = None
    next_progress = 0.0
    while time.monotonic() < deadline:
        try:
            payload = _request(url, method=method, read_limit=read_limit)
            print(f"PASS {name}")
            return payload
        except (OSError, RuntimeError, requests.RequestException) as exc:
            last_error = exc
            now = time.monotonic()
            if now >= next_progress:
                print(f"WAIT {name}")
                next_progress = now + 30
            time.sleep(10)
    raise TimeoutError(f"{name} was not ready: {last_error}")


def _launch_command(public_ip: str, command: list[str]) -> None:
    body = json.dumps({"command": command, "shell": False}).encode("utf-8")
    response = _request(
        f"http://{public_ip}:5000/setup/launch",
        method="POST",
        body=body,
        headers={"Content-Type": "application/json"},
    )
    if b"launched successfully" not in response:
        raise RuntimeError(f"OSWorld setup launch failed: {response!r}")


def _launch_chrome(public_ip: str) -> None:
    _launch_command(
        public_ip,
        [
            "google-chrome",
            "--remote-debugging-port=1337",
        ],
    )
    _launch_command(
        public_ip,
        [
            "socat",
            "tcp-listen:9222,fork,reuseaddr",
            "tcp:localhost:1337",
        ],
    )
    print("PASS Chrome and CDP forwarding launched")


def _desktop_is_ready(public_ip: str) -> bool:
    body = json.dumps(
        {
            "command": [
                "bash",
                "-lc",
                "pgrep -x gnome-shell >/dev/null && DISPLAY=:0 xdpyinfo >/dev/null",
            ],
            "shell": False,
        }
    ).encode("utf-8")
    payload = _request(
        f"http://{public_ip}:5000/execute",
        method="POST",
        body=body,
        headers={"Content-Type": "application/json"},
    )
    result = json.loads(payload.decode("utf-8"))
    return result.get("status") == "success" and result.get("returncode") == 0


def _wait_for_desktop(public_ip: str, deadline: float) -> None:
    next_progress = 0.0
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        try:
            if _desktop_is_ready(public_ip):
                print("PASS GNOME/X11 desktop")
                return
            last_error = RuntimeError("GNOME/X11 readiness command returned non-zero")
        except (OSError, RuntimeError, ValueError, requests.RequestException) as exc:
            last_error = exc
        now = time.monotonic()
        if now >= next_progress:
            print("WAIT GNOME/X11 desktop")
            next_progress = now + 30
        time.sleep(10)
    raise TimeoutError(f"GNOME/X11 desktop was not ready: {last_error}")


def _verify_screenshot(public_ip: str) -> None:
    payload = _request(
        f"http://{public_ip}:5000/screenshot",
        timeout=60,
    )
    if not payload.startswith(b"\x89PNG\r\n\x1a\n"):
        raise RuntimeError("OSWorld screenshot response is not a PNG")
    print("PASS OSWorld screenshot")


def _cleanup_instance(instance_id: str, region: str) -> None:
    ec2 = boto3.client("ec2", region_name=region)
    ec2.terminate_instances(InstanceIds=[instance_id])
    ec2.get_waiter("instance_terminated").wait(
        InstanceIds=[instance_id],
        WaiterConfig={"Delay": 10, "MaxAttempts": 60},
    )
    delete_instance_termination_schedules(region, instance_id)
    print("CLEANUP instance terminated and TTL schedules removed")


def _assert_no_active_project_instance(region: str) -> None:
    ec2 = boto3.client("ec2", region_name=region)
    response = ec2.describe_instances(
        Filters=[
            {"Name": "tag:Project", "Values": [PROJECT_TAG]},
            {
                "Name": "instance-state-name",
                "Values": ["pending", "running", "stopping", "stopped"],
            },
        ]
    )
    active = [
        instance
        for reservation in response.get("Reservations", [])
        for instance in reservation.get("Instances", [])
    ]
    if active:
        raise RuntimeError("An active OSWorld-PPT-Web instance already exists")


def _verify_ttl_schedule(instance_id: str, region: str) -> None:
    scheduler = boto3.client("scheduler", region_name=region)
    prefix = f"osworld-ttl-{instance_id}-"
    for _ in range(12):
        schedules = scheduler.list_schedules(NamePrefix=prefix).get("Schedules", [])
        if schedules:
            print("PASS TTL schedule")
            return
        time.sleep(5)
    raise RuntimeError("TTL schedule was not created")


def _open_powerpoint_web(public_ip: str, deadline: float) -> None:
    target = urllib.parse.quote(
        "https://www.microsoft365.com/launch/powerpoint",
        safe="",
    )
    _wait_for_url(
        "Chrome DevTools",
        f"http://{public_ip}:9222/json/version",
        deadline,
    )
    _request(f"http://{public_ip}:9222/json/new?{target}", method="PUT")
    for _ in range(30):
        tabs = json.loads(
            _request(f"http://{public_ip}:9222/json/list").decode("utf-8")
        )
        if any(
            "microsoft" in tab.get("url", "").lower()
            or "office" in tab.get("url", "").lower()
            for tab in tabs
        ):
            print("PASS PowerPoint Web tab opened")
            return
        time.sleep(2)
    raise RuntimeError("PowerPoint Web tab did not appear in Chrome")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--region", default=os.getenv("AWS_REGION", "us-east-1"))
    parser.add_argument(
        "--keep-running",
        action="store_true",
        help="Keep a successful instance for manual Microsoft login; TTL remains active.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    _assert_no_active_project_instance(args.region)
    instance_id: str | None = None
    success = False
    started = time.monotonic()

    try:
        instance_id = _allocate_vm(args.region, screen_size=(1920, 1080))
        ec2 = boto3.client("ec2", region_name=args.region)
        ec2.get_waiter("instance_status_ok").wait(
            InstanceIds=[instance_id],
            WaiterConfig={"Delay": 15, "MaxAttempts": 40},
        )
        instance = ec2.describe_instances(InstanceIds=[instance_id])[
            "Reservations"
        ][0]["Instances"][0]
        public_ip = instance.get("PublicIpAddress")
        if not public_ip:
            raise RuntimeError("Instance has no public IP")

        _verify_ttl_schedule(instance_id, args.region)
        deadline = time.monotonic() + PROBE_TIMEOUT_SECONDS
        _wait_for_url(
            "OSWorld API",
            f"http://{public_ip}:5000/platform",
            deadline,
        )
        _wait_for_desktop(public_ip, deadline)
        _wait_for_url(
            "noVNC",
            f"http://{public_ip}:5910/vnc.html",
            deadline,
            method="HEAD",
        )
        _launch_chrome(public_ip)
        _open_powerpoint_web(public_ip, deadline)
        _verify_screenshot(public_ip)

        expires_at = datetime.now(timezone.utc) + timedelta(minutes=180)
        ec2.create_tags(
            Resources=[instance_id],
            Tags=[
                {"Key": "Purpose", "Value": "W1-PowerPoint-Web-Login"},
                {"Key": "ExpiresAt", "Value": expires_at.isoformat()},
            ],
        )
        success = True
        print(f"SMOKE PASS elapsed_seconds={time.monotonic() - started:.1f}")
        print(f"VNC http://{public_ip}:5910/vnc.html")
        if args.keep_running:
            print("KEEPING instance running for manual login; TTL schedule is active")
        return 0
    finally:
        if instance_id and (not success or not args.keep_running):
            _cleanup_instance(instance_id, args.region)


if __name__ == "__main__":
    raise SystemExit(main())
