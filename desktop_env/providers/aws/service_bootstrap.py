"""Install the OSWorld service startup guard through SSM after EC2 launch."""

from __future__ import annotations

import base64
import logging
import time

import boto3
from botocore.exceptions import ClientError

from desktop_env.providers.aws.launch_config import OSWORLD_SERVICE_DROP_IN


DROP_IN_PATH = "/etc/systemd/system/osworld.service.d/10-wait-for-x.conf"
_TERMINAL_FAILURE_STATUSES = {
    "Cancelled",
    "Cancelling",
    "Failed",
    "TimedOut",
}


def _bootstrap_commands() -> list[str]:
    encoded_drop_in = base64.b64encode(
        OSWORLD_SERVICE_DROP_IN.encode("utf-8")
    ).decode("ascii")
    return [
        "set -eu",
        "install -d -m 0755 /etc/systemd/system/osworld.service.d",
        (
            f"printf '%s' '{encoded_drop_in}' | base64 --decode "
            f"> {DROP_IN_PATH}"
        ),
        "systemctl daemon-reload",
        "systemctl cat osworld.service | grep -F '10-wait-for-x.conf'",
        "systemctl cat osworld.service | grep -F 'StartLimitIntervalSec=0'",
        "systemctl cat osworld.service | grep -F '/tmp/.X11-unix/X0'",
        (
            "for second in $(seq 1 360); do "
            "test -S /tmp/.X11-unix/X0 && break; "
            "if test \"$second\" -eq 360; then "
            "echo 'X11 display socket did not become ready' >&2; "
            "systemctl status display-manager.service --no-pager || true; "
            "exit 1; fi; sleep 1; done"
        ),
        (
            "for attempt in 1 2; do "
            "systemctl reset-failed osworld.service || true; "
            "if systemctl restart osworld.service; then "
            "for second in $(seq 1 120); do "
            "if systemctl is-active --quiet osworld.service && "
            "/usr/bin/python3 -c \"import urllib.request; "
            "response=urllib.request.urlopen('http://127.0.0.1:5000/platform', "
            "timeout=2); raise SystemExit(0 if response.status == 200 else 1)\" "
            "2>/dev/null; then "
            "echo 'OSWorld API is ready'; exit 0; fi; sleep 1; done; fi; "
            "echo \"OSWorld service attempt $attempt failed\" >&2; "
            "systemctl status osworld.service --no-pager || true; "
            "journalctl -u osworld.service -n 120 --no-pager || true; "
            "sleep 5; done; "
            "echo 'OSWorld service failed after two attempts' >&2; exit 1"
        ),
    ]


def ensure_osworld_service_x11_wait(
    region: str,
    instance_id: str,
    logger: logging.Logger | None = None,
    *,
    timeout_seconds: int = 900,
    poll_seconds: int = 5,
) -> None:
    """Idempotently install and verify the X11 startup guard via SSM."""

    log = logger or logging.getLogger(__name__)
    ssm = boto3.client("ssm", region_name=region)
    deadline = time.monotonic() + timeout_seconds

    while True:
        response = ssm.describe_instance_information(
            Filters=[{"Key": "InstanceIds", "Values": [instance_id]}]
        )
        instances = response.get("InstanceInformationList", [])
        if any(
            instance.get("PingStatus") == "Online"
            for instance in instances
        ):
            break
        if time.monotonic() >= deadline:
            raise TimeoutError(
                f"SSM did not become online for instance {instance_id}"
            )
        time.sleep(poll_seconds)

    command = ssm.send_command(
        InstanceIds=[instance_id],
        DocumentName="AWS-RunShellScript",
        Parameters={"commands": _bootstrap_commands()},
        TimeoutSeconds=min(max(timeout_seconds, 30), 3600),
    )
    command_id = command["Command"]["CommandId"]

    while True:
        try:
            invocation = ssm.get_command_invocation(
                CommandId=command_id,
                InstanceId=instance_id,
            )
        except ClientError as error:
            if (
                error.response.get("Error", {}).get("Code")
                != "InvocationDoesNotExist"
            ):
                raise
        else:
            status = invocation.get("Status")
            if status == "Success":
                log.info(
                    "Installed and verified OSWorld X11 wait drop-in on %s",
                    instance_id,
                )
                return
            if status in _TERMINAL_FAILURE_STATUSES:
                error_text = invocation.get("StandardErrorContent", "")
                output_text = invocation.get("StandardOutputContent", "")
                raise RuntimeError(
                    "OSWorld service bootstrap failed for "
                    f"{instance_id}: status={status}, "
                    f"stderr={error_text[-4000:]!r}, "
                    f"stdout={output_text[-4000:]!r}"
                )

        if time.monotonic() >= deadline:
            raise TimeoutError(
                f"SSM bootstrap timed out for instance {instance_id}"
            )
        time.sleep(poll_seconds)
