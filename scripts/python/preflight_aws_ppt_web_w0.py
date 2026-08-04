#!/usr/bin/env python3
"""Offline preflight checks for the AWS Ubuntu PowerPoint Web deployment."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from dataclasses import asdict, dataclass
from typing import Callable, Mapping, Sequence


MINIMUM_PYTHON = (3, 12)
DEFAULT_TTL_MINUTES = 180


@dataclass(frozen=True)
class Check:
    name: str
    status: str
    message: str


def _configured(environ: Mapping[str, str], name: str) -> bool:
    return bool(environ.get(name, "").strip())


def _format_check(name: str, configured: bool, requirement: str) -> Check:
    if configured:
        return Check(name, "pass", "configured")
    return Check(name, "blocked", requirement)


def _validate_identifier(
    environ: Mapping[str, str],
    name: str,
    pattern: str,
    missing_message: str,
    *,
    required: bool = True,
) -> Check:
    check_name = name.lower()
    value = environ.get(name, "").strip()
    if not value:
        return Check(
            check_name,
            "blocked" if required else "warning",
            missing_message,
        )
    if not re.fullmatch(pattern, value):
        return Check(
            check_name,
            "blocked",
            "configured value has an unexpected format",
        )
    return Check(check_name, "pass", "configured")


def evaluate_preflight(
    environ: Mapping[str, str] | None = None,
    *,
    which: Callable[[str], str | None] = shutil.which,
    python_version: Sequence[int] | None = None,
    stage: str = "w1",
) -> list[Check]:
    """Return checks without calling AWS or exposing configuration values."""

    if stage not in {"w0", "w1"}:
        raise ValueError("stage must be 'w0' or 'w1'")

    env = os.environ if environ is None else environ
    version = sys.version_info if python_version is None else python_version
    checks: list[Check] = []

    python_ok = tuple(version[:2]) >= MINIMUM_PYTHON
    checks.append(
        Check(
            "python",
            "pass" if python_ok else "blocked",
            "Python 3.12+ available" if python_ok else "Python 3.12+ is required",
        )
    )

    checks.append(
        Check(
            "aws_cli",
            "pass" if which("aws") else "blocked",
            "available" if which("aws") else "AWS CLI is not installed or not on PATH",
        )
    )

    has_profile = _configured(env, "AWS_PROFILE")
    has_access_key_pair = _configured(env, "AWS_ACCESS_KEY_ID") and _configured(
        env, "AWS_SECRET_ACCESS_KEY"
    )
    has_web_identity = _configured(env, "AWS_WEB_IDENTITY_TOKEN_FILE") and _configured(
        env, "AWS_ROLE_ARN"
    )
    checks.append(
        Check(
            "aws_identity_source",
            "pass" if has_profile or has_access_key_pair or has_web_identity else "blocked",
            (
                "configured"
                if has_profile or has_access_key_pair or has_web_identity
                else "set AWS_PROFILE/SSO or another supported short-lived identity source"
            ),
        )
    )

    region = (
        env.get("AWS_REGION", "").strip()
        or env.get("AWS_DEFAULT_REGION", "").strip()
    )
    has_region = bool(region)
    checks.append(
        _format_check(
            "aws_region",
            has_region,
            "set AWS_REGION or AWS_DEFAULT_REGION",
        )
    )
    checks.append(
        _validate_identifier(
            env,
            "AWS_SUBNET_ID",
            r"subnet-[A-Za-z0-9]+",
            "set AWS_SUBNET_ID in W1 after selecting the deployment subnet",
            required=stage == "w1",
        )
    )
    checks.append(
        _validate_identifier(
            env,
            "AWS_SECURITY_GROUP_ID",
            r"sg-[A-Za-z0-9]+",
            "set AWS_SECURITY_GROUP_ID in W1 after creating the restricted security group",
            required=stage == "w1",
        )
    )
    checks.append(
        Check(
            "osworld_ubuntu_ami",
            "pass" if region == "us-east-1" else "blocked",
            (
                "official OSWorld 1920x1080 AMI mapping selected"
                if region == "us-east-1"
                else "Phase W0 currently requires AWS_REGION=us-east-1"
            ),
        )
    )
    checks.append(
        _format_check(
            "aws_instance_type",
            _configured(env, "AWS_INSTANCE_TYPE"),
            "set AWS_INSTANCE_TYPE after the cost/capacity decision",
        )
    )
    connection_mode = env.get("AWS_CONNECTION_MODE", "private").strip().lower()
    checks.append(
        Check(
            "aws_connection_mode",
            "pass" if connection_mode in {"private", "public"} else "blocked",
            (
                f"{connection_mode} mode selected"
                if connection_mode in {"private", "public"}
                else "AWS_CONNECTION_MODE must be private or public"
            ),
        )
    )

    ttl_enabled = env.get("ENABLE_TTL", "true").strip().lower()
    if ttl_enabled not in {"true", "false"}:
        checks.append(
            Check("ttl_enabled", "blocked", "ENABLE_TTL must be true or false")
        )
    elif ttl_enabled == "false":
        checks.append(
            Check("ttl_enabled", "blocked", "TTL must remain enabled for AWS runs")
        )
    else:
        checks.append(Check("ttl_enabled", "pass", "enabled"))

    ttl_raw = env.get("DEFAULT_TTL_MINUTES", str(DEFAULT_TTL_MINUTES)).strip()
    try:
        ttl_minutes = int(ttl_raw)
    except ValueError:
        ttl_minutes = 0
    checks.append(
        Check(
            "ttl_minutes",
            "pass" if ttl_minutes > 0 else "blocked",
            "positive integer configured" if ttl_minutes > 0 else "must be a positive integer",
        )
    )

    scheduler_configured = _configured(env, "AWS_SCHEDULER_ROLE_ARN") or _configured(
        env, "AWS_SCHEDULER_ROLE_NAME"
    )
    checks.append(
        Check(
            "ttl_scheduler_role",
            (
                "pass"
                if scheduler_configured
                else "blocked" if stage == "w1" else "warning"
            ),
            (
                "configured"
                if scheduler_configured
                else "not explicit; current code may attempt to create a default scheduler role"
            ),
        )
    )
    checks.append(
        _validate_identifier(
            env,
            "AWS_EC2_INSTANCE_PROFILE_NAME",
            r"[A-Za-z0-9+=,.@_-]{1,128}",
            "set AWS_EC2_INSTANCE_PROFILE_NAME after creating the W1 SSM diagnostic profile",
            required=stage == "w1",
        )
    )
    return checks


def summarize(checks: Sequence[Check]) -> dict[str, int]:
    return {
        status: sum(check.status == status for check in checks)
        for status in ("pass", "warning", "blocked")
    }


def format_text(checks: Sequence[Check]) -> str:
    lines = [
        f"[{check.status.upper():7}] {check.name}: {check.message}"
        for check in checks
    ]
    counts = summarize(checks)
    lines.append(
        "Summary: "
        f"{counts['pass']} pass, {counts['warning']} warning, "
        f"{counts['blocked']} blocked"
    )
    lines.append("No AWS API calls were made and no configuration values were printed.")
    return "\n".join(lines)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run offline AWS Ubuntu PowerPoint Web prerequisite checks."
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON without environment-variable values.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero when a blocking check is present.",
    )
    parser.add_argument(
        "--stage",
        choices=("w0", "w1"),
        default="w1",
        help="Treat cloud resource identifiers as W0 warnings or W1 requirements.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    checks = evaluate_preflight(stage=args.stage)
    if args.json:
        print(
            json.dumps(
                {
                    "checks": [asdict(check) for check in checks],
                    "summary": summarize(checks),
                    "stage": args.stage,
                    "aws_api_calls_made": False,
                    "configuration_values_printed": False,
                },
                indent=2,
                sort_keys=True,
            )
        )
    else:
        print(format_text(checks))
    return 1 if args.strict and any(check.status == "blocked" for check in checks) else 0


if __name__ == "__main__":
    raise SystemExit(main())
