#!/usr/bin/env python3
"""Create the fixed Cognito annotator accounts and save temp passwords locally."""

from __future__ import annotations

import argparse
import json
import os
import secrets
import string
from pathlib import Path


DEFAULT_USERNAMES = (
    "annotator-hk-1",
    "annotator-hk-2",
    "annotator-hk-3",
    "annotator-us-1",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--user-pool-id", required=True)
    parser.add_argument("--region", default="ap-east-1")
    parser.add_argument("--profile")
    parser.add_argument("--username", action="append", dest="usernames")
    parser.add_argument(
        "--credentials-output",
        type=Path,
        required=True,
        help="Sensitive local JSON output; do not place it in the repository.",
    )
    return parser.parse_args()


def _temporary_password() -> str:
    alphabet = string.ascii_letters + string.digits + "!@#%^*-_"
    while True:
        password = "".join(secrets.choice(alphabet) for _ in range(22))
        if (
            any(char.islower() for char in password)
            and any(char.isupper() for char in password)
            and any(char.isdigit() for char in password)
            and any(char in "!@#%^*-_" for char in password)
        ):
            return password


def main() -> int:
    args = parse_args()
    output = args.credentials_output.expanduser().resolve()
    if output.exists():
        raise SystemExit(
            f"Refusing to overwrite existing credentials file: {output}"
        )
    import boto3
    from botocore.exceptions import ClientError

    session = boto3.Session(profile_name=args.profile, region_name=args.region)
    client = session.client("cognito-idp")
    created = []
    for username in args.usernames or DEFAULT_USERNAMES:
        password = _temporary_password()
        try:
            client.admin_create_user(
                UserPoolId=args.user_pool_id,
                Username=username,
                TemporaryPassword=password,
                MessageAction="SUPPRESS",
            )
        except ClientError as exc:
            if exc.response.get("Error", {}).get("Code") == "UsernameExistsException":
                raise SystemExit(
                    f"Cognito user {username!r} already exists; no password was changed"
                ) from exc
            raise
        created.append({"username": username, "temporary_password": password})

    output.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
        json.dump(
            {"user_pool_id": args.user_pool_id, "users": created},
            stream,
            indent=2,
        )
        stream.write("\n")
    print(f"Created {len(created)} users. Temporary credentials saved to {output}")
    print("Distribute each credential privately; users must change it at first login.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
