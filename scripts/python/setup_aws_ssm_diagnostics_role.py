#!/usr/bin/env python3
"""Create the narrowly scoped EC2 instance profile used for W1 diagnostics."""

from __future__ import annotations

import json

import boto3
from botocore.exceptions import ClientError


ROLE_NAME = "osworld-ec2-ssm-diagnostics"
PROFILE_NAME = ROLE_NAME
POLICY_NAME = "osworld-ssm-managed-instance-core"
PROJECT_TAG = {"Key": "Project", "Value": "OSWorld-PPT-Web"}

TRUST_POLICY = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"Service": "ec2.amazonaws.com"},
            "Action": "sts:AssumeRole",
        }
    ],
}

SSM_CORE_POLICY = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ssm:DescribeAssociation",
                "ssm:GetDeployablePatchSnapshotForInstance",
                "ssm:GetDocument",
                "ssm:DescribeDocument",
                "ssm:GetManifest",
                "ssm:GetParameter",
                "ssm:GetParameters",
                "ssm:ListAssociations",
                "ssm:ListInstanceAssociations",
                "ssm:PutInventory",
                "ssm:PutComplianceItems",
                "ssm:PutConfigurePackageResult",
                "ssm:UpdateAssociationStatus",
                "ssm:UpdateInstanceAssociationStatus",
                "ssm:UpdateInstanceInformation",
            ],
            "Resource": "*",
        },
        {
            "Effect": "Allow",
            "Action": [
                "ssmmessages:CreateControlChannel",
                "ssmmessages:CreateDataChannel",
                "ssmmessages:OpenControlChannel",
                "ssmmessages:OpenDataChannel",
            ],
            "Resource": "*",
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2messages:AcknowledgeMessage",
                "ec2messages:DeleteMessage",
                "ec2messages:FailMessage",
                "ec2messages:GetEndpoint",
                "ec2messages:GetMessages",
                "ec2messages:SendReply",
            ],
            "Resource": "*",
        },
    ],
}


def _not_found(exc: ClientError) -> bool:
    return exc.response.get("Error", {}).get("Code") == "NoSuchEntity"


def main() -> int:
    iam = boto3.client("iam")

    try:
        iam.get_role(RoleName=ROLE_NAME)
    except ClientError as exc:
        if not _not_found(exc):
            raise
        iam.create_role(
            RoleName=ROLE_NAME,
            AssumeRolePolicyDocument=json.dumps(TRUST_POLICY),
            Description="OSWorld W1 EC2 role for private SSM diagnostics",
            Tags=[PROJECT_TAG],
        )
    else:
        iam.update_assume_role_policy(
            RoleName=ROLE_NAME,
            PolicyDocument=json.dumps(TRUST_POLICY),
        )

    iam.put_role_policy(
        RoleName=ROLE_NAME,
        PolicyName=POLICY_NAME,
        PolicyDocument=json.dumps(SSM_CORE_POLICY),
    )

    try:
        profile = iam.get_instance_profile(
            InstanceProfileName=PROFILE_NAME,
        )["InstanceProfile"]
    except ClientError as exc:
        if not _not_found(exc):
            raise
        profile = iam.create_instance_profile(
            InstanceProfileName=PROFILE_NAME,
            Tags=[PROJECT_TAG],
        )["InstanceProfile"]

    attached_roles = {role["RoleName"] for role in profile.get("Roles", [])}
    if ROLE_NAME not in attached_roles:
        iam.add_role_to_instance_profile(
            InstanceProfileName=PROFILE_NAME,
            RoleName=ROLE_NAME,
        )

    print(PROFILE_NAME)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
