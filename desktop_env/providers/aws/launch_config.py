"""Validated EC2 launch settings shared by AWS allocation and reset paths."""

from __future__ import annotations

import base64
import os
import re
from dataclasses import dataclass
from typing import Mapping


DEFAULT_INSTANCE_TYPE = "t3.xlarge"
DEFAULT_VOLUME_SIZE_GIB = 30
DEFAULT_VOLUME_IOPS = 4000
DEFAULT_VOLUME_THROUGHPUT_MIBPS = 1000
DEFAULT_VOLUME_ENCRYPTED = True
DEFAULT_RESOURCE_PROJECT = "OSWorld"

_INSTANCE_TYPE_PATTERN = re.compile(r"[a-z0-9-]+\.[a-z0-9]+")

OSWORLD_SERVICE_DROP_IN = """[Unit]
After=display-manager.service
Wants=display-manager.service
StartLimitIntervalSec=0

[Service]
ExecStartPre=/bin/bash -c 'for i in $(seq 1 300); do DISPLAY=:0 /usr/bin/xdpyinfo >/dev/null 2>&1 && exit 0; sleep 1; done; exit 1'
Restart=on-failure
RestartSec=5s
"""
_OSWORLD_SERVICE_DROP_IN_BASE64 = base64.b64encode(
    OSWORLD_SERVICE_DROP_IN.encode("utf-8")
).decode("ascii")
OSWORLD_SERVICE_USER_DATA = f"""#!/bin/bash
set -euo pipefail
install -d -m 0755 /etc/systemd/system/osworld.service.d
printf '%s' '{_OSWORLD_SERVICE_DROP_IN_BASE64}' \
  | base64 --decode \
  > /etc/systemd/system/osworld.service.d/10-wait-for-x.conf
systemctl daemon-reload
systemctl reset-failed osworld.service || true
systemctl restart osworld.service
"""


@dataclass(frozen=True)
class AwsLaunchConfig:
    instance_type: str
    volume_size_gib: int
    volume_iops: int
    volume_throughput_mibps: int
    volume_encrypted: bool
    resource_project: str
    instance_profile_name: str | None
    resource_role: str | None = None

    def block_device_mapping(self, device_name: str = "/dev/sda1") -> dict:
        return {
            "DeviceName": device_name,
            "Ebs": {
                "VolumeSize": self.volume_size_gib,
                "VolumeType": "gp3",
                "Throughput": self.volume_throughput_mibps,
                "Iops": self.volume_iops,
                "Encrypted": self.volume_encrypted,
                "DeleteOnTermination": True,
            },
        }

    def tag_specifications(self) -> list[dict]:
        tags = [
            {"Key": "Project", "Value": self.resource_project},
            {"Key": "ManagedBy", "Value": "OSWorld"},
        ]
        if self.resource_role:
            tags.append({"Key": "Role", "Value": self.resource_role})
        return [
            {"ResourceType": "instance", "Tags": tags},
            {"ResourceType": "volume", "Tags": tags},
        ]

    def instance_profile_parameter(self) -> dict:
        if not self.instance_profile_name:
            return {}
        return {"IamInstanceProfile": {"Name": self.instance_profile_name}}

    def user_data_parameter(self) -> dict:
        return {"UserData": OSWORLD_SERVICE_USER_DATA}


def _read_int(
    environ: Mapping[str, str],
    name: str,
    default: int,
    minimum: int,
    maximum: int,
) -> int:
    raw_value = environ.get(name, str(default)).strip()
    try:
        value = int(raw_value)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer") from exc
    if not minimum <= value <= maximum:
        raise ValueError(f"{name} must be between {minimum} and {maximum}")
    return value


def _read_bool(
    environ: Mapping[str, str],
    name: str,
    default: bool,
) -> bool:
    raw_value = environ.get(name, str(default)).strip().lower()
    if raw_value in {"1", "true", "yes", "on"}:
        return True
    if raw_value in {"0", "false", "no", "off"}:
        return False
    raise ValueError(
        f"{name} must be one of true/false, yes/no, on/off, or 1/0"
    )


def load_launch_config(
    environ: Mapping[str, str] | None = None,
    *,
    default_instance_type: str = DEFAULT_INSTANCE_TYPE,
) -> AwsLaunchConfig:
    """Load non-secret launch settings without making AWS API calls."""

    env = os.environ if environ is None else environ
    instance_type = env.get("AWS_INSTANCE_TYPE", default_instance_type).strip()
    if not _INSTANCE_TYPE_PATTERN.fullmatch(instance_type):
        raise ValueError("AWS_INSTANCE_TYPE has an unexpected format")
    resource_project = env.get(
        "AWS_RESOURCE_PROJECT",
        DEFAULT_RESOURCE_PROJECT,
    ).strip()
    if not resource_project:
        raise ValueError("AWS_RESOURCE_PROJECT must not be empty")
    instance_profile_name = env.get(
        "AWS_EC2_INSTANCE_PROFILE_NAME",
        "",
    ).strip()
    if instance_profile_name and not re.fullmatch(
        r"[A-Za-z0-9+=,.@_-]{1,128}",
        instance_profile_name,
    ):
        raise ValueError("AWS_EC2_INSTANCE_PROFILE_NAME has an unexpected format")
    resource_role = env.get("AWS_RESOURCE_ROLE", "").strip()
    if resource_role and not re.fullmatch(r"[A-Za-z0-9 _.:/=+@-]{1,256}", resource_role):
        raise ValueError("AWS_RESOURCE_ROLE has an unexpected format")

    return AwsLaunchConfig(
        instance_type=instance_type,
        volume_size_gib=_read_int(
            env,
            "AWS_EBS_VOLUME_SIZE_GIB",
            DEFAULT_VOLUME_SIZE_GIB,
            1,
            65536,
        ),
        volume_iops=_read_int(
            env,
            "AWS_EBS_IOPS",
            DEFAULT_VOLUME_IOPS,
            3000,
            80000,
        ),
        volume_throughput_mibps=_read_int(
            env,
            "AWS_EBS_THROUGHPUT_MIBPS",
            DEFAULT_VOLUME_THROUGHPUT_MIBPS,
            125,
            2000,
        ),
        volume_encrypted=_read_bool(
            env,
            "AWS_EBS_ENCRYPTED",
            DEFAULT_VOLUME_ENCRYPTED,
        ),
        resource_project=resource_project,
        instance_profile_name=instance_profile_name or None,
        resource_role=resource_role or None,
    )
