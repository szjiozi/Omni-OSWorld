#!/usr/bin/env python3
"""Create or resolve the narrowly scoped OSWorld TTL scheduler role."""

from __future__ import annotations

import logging
import os

from desktop_env.providers.aws.scheduler_utils import _resolve_scheduler_role_arn


def main() -> int:
    os.environ["AWS_AUTO_CREATE_SCHEDULER_ROLE"] = "true"
    logger = logging.getLogger("osworld.aws.ttl_setup")
    logger.addHandler(logging.NullHandler())
    role_arn = _resolve_scheduler_role_arn(logger)
    if not role_arn:
        raise RuntimeError("TTL scheduler role could not be created or resolved")
    print(role_arn)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
