#!/usr/bin/env python3
"""Run sequential AWS lifecycle soak iterations and audit resource cleanup."""

from __future__ import annotations

import argparse
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import boto3

from desktop_env.providers.aws.manager import _allocate_vm, resolve_ami_id
from desktop_env.providers.aws.provider import AWSProvider
from scripts.python.smoke_aws_ppt_web_w1 import (
    PROBE_TIMEOUT_SECONDS,
    _request,
    _verify_screenshot,
    _verify_ttl_schedule,
    _wait_for_desktop,
    _wait_for_url,
)


PROJECT_TAG = "OSWorld-PPT-Web"


def _project_instances(ec2: Any) -> list[dict[str, Any]]:
    response = ec2.describe_instances(
        Filters=[
            {"Name": "tag:Project", "Values": [PROJECT_TAG]},
            {
                "Name": "instance-state-name",
                "Values": [
                    "pending",
                    "running",
                    "stopping",
                    "stopped",
                    "shutting-down",
                ],
            },
        ]
    )
    return [
        instance
        for reservation in response.get("Reservations", [])
        for instance in reservation.get("Instances", [])
    ]


def _project_volumes(ec2: Any) -> list[dict[str, Any]]:
    return ec2.describe_volumes(
        Filters=[
            {"Name": "tag:Project", "Values": [PROJECT_TAG]},
            {"Name": "status", "Values": ["creating", "available", "in-use"]},
        ]
    ).get("Volumes", [])


def _project_enis(ec2: Any) -> list[dict[str, Any]]:
    security_group_id = os.environ["AWS_SECURITY_GROUP_ID"]
    return ec2.describe_network_interfaces(
        Filters=[
            {"Name": "group-id", "Values": [security_group_id]},
            {"Name": "status", "Values": ["available", "in-use"]},
        ]
    ).get("NetworkInterfaces", [])


def _ttl_schedules(scheduler: Any) -> list[dict[str, Any]]:
    schedules = []
    next_token = None
    while True:
        parameters = {"NamePrefix": "osworld-ttl-"}
        if next_token:
            parameters["NextToken"] = next_token
        response = scheduler.list_schedules(**parameters)
        schedules.extend(response.get("Schedules", []))
        next_token = response.get("NextToken")
        if not next_token:
            return schedules


def _wait_for_clean(region: str, timeout_seconds: int = 600) -> dict[str, int]:
    ec2 = boto3.client("ec2", region_name=region)
    scheduler = boto3.client("scheduler", region_name=region)
    deadline = time.monotonic() + timeout_seconds
    last_counts: dict[str, int] = {}
    while time.monotonic() < deadline:
        last_counts = {
            "instances": len(_project_instances(ec2)),
            "volumes": len(_project_volumes(ec2)),
            "enis": len(_project_enis(ec2)),
            "ttl_schedules": len(_ttl_schedules(scheduler)),
        }
        if not any(last_counts.values()):
            return last_counts
        time.sleep(10)
    raise TimeoutError(f"AWS project resources did not clean up: {last_counts}")


def _probe_instance(
    ec2: Any,
    instance_id: str,
    region: str,
) -> str:
    ec2.get_waiter("instance_status_ok").wait(
        InstanceIds=[instance_id],
        WaiterConfig={"Delay": 15, "MaxAttempts": 40},
    )
    instance = ec2.describe_instances(InstanceIds=[instance_id])[
        "Reservations"
    ][0]["Instances"][0]
    public_ip = instance.get("PublicIpAddress")
    if not public_ip:
        raise RuntimeError(f"Instance {instance_id} has no public IP")

    _verify_ttl_schedule(instance_id, region)
    deadline = time.monotonic() + PROBE_TIMEOUT_SECONDS
    _wait_for_url(
        "OSWorld API",
        f"http://{public_ip}:5000/platform",
        deadline,
    )
    _wait_for_desktop(public_ip, deadline)
    body = json.dumps(
        {
            "command": [
                "bash",
                "-lc",
                "systemctl cat osworld.service",
            ],
            "shell": False,
        }
    ).encode("utf-8")
    payload = json.loads(
        _request(
            f"http://{public_ip}:5000/execute",
            method="POST",
            body=body,
            headers={"Content-Type": "application/json"},
        ).decode("utf-8")
    )
    service_unit = payload.get("output", "")
    required_unit_settings = (
        "10-wait-for-x.conf",
        "ExecStartPre=",
        "xdpyinfo",
        "StartLimitIntervalSec=0",
    )
    if payload.get("status") != "success" or not all(
        setting in service_unit for setting in required_unit_settings
    ):
        raise RuntimeError("OSWorld X11 wait systemd drop-in is not active")
    print("PASS OSWorld X11 wait drop-in")
    _verify_screenshot(public_ip)
    return public_ip


def run_soak(iterations: int, region: str) -> dict[str, Any]:
    if iterations < 1:
        raise ValueError("iterations must be positive")
    if os.getenv("AWS_RESOURCE_PROJECT") != PROJECT_TAG:
        raise ValueError(f"AWS_RESOURCE_PROJECT must be {PROJECT_TAG}")

    _wait_for_clean(region, timeout_seconds=1)
    ami_id = resolve_ami_id(region, (1920, 1080))
    report: dict[str, Any] = {
        "started_at": datetime.now(timezone.utc).isoformat(),
        "region": region,
        "iterations": [],
    }
    ec2 = boto3.client("ec2", region_name=region)
    provider = AWSProvider(region)
    instance_id: str | None = None
    try:
        instance_id = _allocate_vm(region, screen_size=(1920, 1080))
        for iteration in range(1, iterations + 1):
            started = time.monotonic()
            _probe_instance(ec2, instance_id, region)
            report["iterations"].append(
                {
                    "iteration": iteration,
                    "instance_id": instance_id,
                    "elapsed_seconds": round(time.monotonic() - started, 3),
                }
            )
            print(
                f"PASS iteration={iteration} "
                f"instance_id={instance_id}"
            )
            if iteration < iterations:
                previous_instance_id = instance_id
                instance_id = provider.revert_to_snapshot(
                    previous_instance_id,
                    ami_id,
                )
                ec2.get_waiter("instance_terminated").wait(
                    InstanceIds=[previous_instance_id],
                    WaiterConfig={"Delay": 10, "MaxAttempts": 60},
                )
            else:
                provider.stop_emulator(instance_id)
                instance_id = None
    finally:
        if instance_id is not None:
            provider.stop_emulator(instance_id)

    report["cleanup"] = _wait_for_clean(region)
    report["finished_at"] = datetime.now(timezone.utc).isoformat()
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=10)
    parser.add_argument("--region", default=os.getenv("AWS_REGION", "us-east-1"))
    parser.add_argument("--profile", default=os.getenv("AWS_PROFILE", "osworld-dev"))
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    os.environ["AWS_PROFILE"] = args.profile
    report = run_soak(args.iterations, args.region)
    payload = json.dumps(report, indent=2, sort_keys=True)
    print(payload)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(payload + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
