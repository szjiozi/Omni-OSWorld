#!/usr/bin/env python3
"""Collect non-sensitive SSM diagnostics for W1 OSWorld service startup."""

from __future__ import annotations

import argparse
import json
import os
import re
import time
from pathlib import Path
from typing import Any

import boto3

from desktop_env.providers.aws.manager import _allocate_vm
from scripts.python.smoke_aws_ppt_web_w1 import _cleanup_instance
from scripts.python.soak_aws_ppt_web_w1 import _wait_for_clean


DIAGNOSTIC_COMMANDS = [
    "systemctl status osworld --no-pager --full || true",
    (
        "systemctl show osworld "
        "-p ActiveState -p SubState -p Result -p NRestarts "
        "-p ExecMainCode -p ExecMainStatus || true"
    ),
    "systemctl cat osworld || true",
    "journalctl -u osworld -b --no-pager -n 400 || true",
    "ss -ltnp || true",
    "pgrep -a -f 'main.py|server.py|flask|gunicorn|Xorg|gnome-shell' || true",
    "ls -la /tmp/.X11-unix || true",
]


def _redact_diagnostics(text: str) -> str:
    return re.sub(
        r"(?im)(Debugger PIN:\s*)[0-9-]+",
        r"\1<redacted>",
        text,
    )


def _wait_for_ssm(ssm: Any, instance_id: str, timeout_seconds: int) -> None:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        response = ssm.describe_instance_information(
            Filters=[
                {
                    "Key": "InstanceIds",
                    "Values": [instance_id],
                }
            ]
        )
        instances = response.get("InstanceInformationList", [])
        if instances and instances[0].get("PingStatus") == "Online":
            return
        time.sleep(10)
    raise TimeoutError(f"Instance {instance_id} did not register online in SSM")


def _run_diagnostics(
    ssm: Any,
    instance_id: str,
    timeout_seconds: int,
) -> dict[str, Any]:
    response = ssm.send_command(
        InstanceIds=[instance_id],
        DocumentName="AWS-RunShellScript",
        Parameters={"commands": DIAGNOSTIC_COMMANDS},
        TimeoutSeconds=timeout_seconds,
        Comment="OSWorld W1 service startup diagnostics",
    )
    command_id = response["Command"]["CommandId"]
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        invocation = ssm.get_command_invocation(
            CommandId=command_id,
            InstanceId=instance_id,
        )
        if invocation["Status"] in {
            "Success",
            "Cancelled",
            "TimedOut",
            "Failed",
        }:
            return {
                "status": invocation["Status"],
                "stdout": _redact_diagnostics(
                    invocation.get("StandardOutputContent", "")
                ),
                "stderr": _redact_diagnostics(
                    invocation.get("StandardErrorContent", "")
                ),
            }
        time.sleep(2)
    raise TimeoutError(f"SSM command {command_id} did not finish")


def diagnose(region: str) -> dict[str, Any]:
    _wait_for_clean(region, timeout_seconds=1)
    ec2 = boto3.client("ec2", region_name=region)
    ssm = boto3.client("ssm", region_name=region)
    instance_id: str | None = None
    try:
        instance_id = _allocate_vm(region, screen_size=(1920, 1080))
        ec2.get_waiter("instance_status_ok").wait(
            InstanceIds=[instance_id],
            WaiterConfig={"Delay": 15, "MaxAttempts": 40},
        )
        _wait_for_ssm(ssm, instance_id, timeout_seconds=600)
        result = _run_diagnostics(ssm, instance_id, timeout_seconds=300)
        result["instance_id"] = instance_id
        return result
    finally:
        if instance_id is not None:
            _cleanup_instance(instance_id, region)
        _wait_for_clean(region)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--region", default=os.getenv("AWS_REGION", "us-east-1"))
    parser.add_argument("--profile", default=os.getenv("AWS_PROFILE", "osworld-dev"))
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    os.environ["AWS_PROFILE"] = args.profile
    report = diagnose(args.region)
    payload = json.dumps(report, indent=2, sort_keys=True)
    print(payload)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(payload + "\n", encoding="utf-8")
    return 0 if report["status"] == "Success" else 1


if __name__ == "__main__":
    raise SystemExit(main())
