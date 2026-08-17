#!/usr/bin/env python3
"""Package and deploy the four-user annotation portal to AWS."""

from __future__ import annotations

import argparse
import atexit
import gzip
import hashlib
import ipaddress
import json
import shlex
import subprocess
import sys
import tarfile
import tempfile
import time
import uuid
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_PATH = REPO_ROOT / "infra/annotation_portal/template.yaml"
DEFAULT_ASSIGNMENTS = (
    "evaluation_examples/expert_skill_learning/annotation_portal/"
    "assignments.example.json"
)
DEFAULT_CREDENTIALS = REPO_ROOT / (
    "evaluation_examples/expert_skill_learning/annotation_portal/"
    "credentials.generated.json"
)
SOURCE_PATHS = (
    "benchmark_construction",
    "desktop_env/__init__.py",
    "desktop_env/actions.py",
    "desktop_env/desktop_env.py",
    "desktop_env/network.py",
    "desktop_env/controllers/__init__.py",
    "desktop_env/controllers/python.py",
    "desktop_env/controllers/setup_only.py",
    "desktop_env/providers/__init__.py",
    "desktop_env/providers/base.py",
    "desktop_env/providers/aws",
    "desktop_env/trajectory",
    "evaluation_examples/expert_skill_learning/annotation_portal/assignments.example.json",
    "evaluation_examples/expert_skill_learning/pilot",
    "infra/annotation_portal/gateway-requirements.txt",
    "scripts/python/run_annotation_portal.py",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", default="osworld-dev")
    parser.add_argument("--region", default="ap-east-1")
    parser.add_argument("--stack-name", default="osworld-annotation-portal")
    parser.add_argument("--vpc-id")
    parser.add_argument("--gateway-subnet-id")
    parser.add_argument("--gateway-private-subnet-cidr")
    parser.add_argument("--worker-subnet-id")
    parser.add_argument("--gateway-ami-id")
    parser.add_argument("--nat-ami-id")
    parser.add_argument("--worker-ami-id")
    parser.add_argument("--gateway-instance-type", default="t3.micro")
    parser.add_argument("--nat-instance-type", default="t4g.nano")
    parser.add_argument("--worker-instance-type", default="t3.xlarge")
    parser.add_argument("--allow-pending", action="store_true")
    parser.add_argument(
        "--credentials-output",
        type=Path,
        default=DEFAULT_CREDENTIALS,
        help="Git-ignored local destination for initial Cognito passwords.",
    )
    parser.add_argument(
        "--skip-user-creation",
        action="store_true",
        help="Do not create the four fixed Cognito users for a new stack.",
    )
    return parser.parse_args()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _archive_filter(info: tarfile.TarInfo) -> tarfile.TarInfo | None:
    parts = Path(info.name).parts
    if any(part in {"__pycache__", ".DS_Store"} for part in parts):
        return None
    if info.issym() or info.islnk():
        raise ValueError(f"Source bundle must not contain links: {info.name}")
    info.uid = 0
    info.gid = 0
    info.uname = "root"
    info.gname = "root"
    info.mtime = 0
    return info


def build_source_bundle(output_path: Path) -> str:
    with output_path.open("wb") as raw_stream:
        with gzip.GzipFile(
            filename="", mode="wb", fileobj=raw_stream, mtime=0
        ) as gzip_stream:
            with tarfile.open(
                fileobj=gzip_stream, mode="w", format=tarfile.PAX_FORMAT
            ) as archive:
                for relative in SOURCE_PATHS:
                    source = REPO_ROOT / relative
                    if not source.exists():
                        raise FileNotFoundError(
                            f"Required gateway source is missing: {source}"
                        )
                    archive.add(
                        source,
                        arcname=relative,
                        recursive=True,
                        filter=_archive_filter,
                    )
    return _sha256(output_path)


def _stack_exists(client: Any, stack_name: str) -> bool:
    from botocore.exceptions import ClientError

    try:
        client.describe_stacks(StackName=stack_name)
    except ClientError as exc:
        if "does not exist" in exc.response.get("Error", {}).get("Message", ""):
            return False
        raise
    return True


def _outputs(client: Any, stack_name: str) -> dict[str, str]:
    stack = client.describe_stacks(StackName=stack_name)["Stacks"][0]
    return {
        item["OutputKey"]: item["OutputValue"]
        for item in stack.get("Outputs", [])
    }


def _stack_parameters(client: Any, stack_name: str) -> dict[str, str]:
    stack = client.describe_stacks(StackName=stack_name)["Stacks"][0]
    return {
        item["ParameterKey"]: item["ParameterValue"]
        for item in stack.get("Parameters", [])
    }


def _active_workspace_count(dynamodb: Any, table_name: str) -> int:
    response = dynamodb.get_item(
        TableName=table_name,
        Key={"pk": {"S": "PORTAL"}, "sk": {"S": "ACTIVE_COUNT"}},
        ConsistentRead=True,
    )
    return int(response.get("Item", {}).get("active_count", {}).get("N", "0"))


def _acquire_deployment_lock(dynamodb: Any, table_name: str) -> str:
    deployment_id = uuid.uuid4().hex
    now = int(time.time())
    try:
        dynamodb.transact_write_items(
            TransactItems=[
                {
                    "ConditionCheck": {
                        "TableName": table_name,
                        "Key": {"pk": {"S": "PORTAL"}, "sk": {"S": "ACTIVE_COUNT"}},
                        "ConditionExpression": (
                            "attribute_not_exists(active_count) OR active_count = :zero"
                        ),
                        "ExpressionAttributeValues": {":zero": {"N": "0"}},
                    }
                },
                {
                    "Put": {
                        "TableName": table_name,
                        "Item": {
                            "pk": {"S": "PORTAL"},
                            "sk": {"S": "MAINTENANCE"},
                            "entity": {"S": "maintenance_lock"},
                            "blocked": {"BOOL": True},
                            "deployment_id": {"S": deployment_id},
                            "ttl": {"N": str(now + 1800)},
                        },
                        "ConditionExpression": (
                            "attribute_not_exists(blocked) OR #ttl < :now"
                        ),
                        "ExpressionAttributeNames": {"#ttl": "ttl"},
                        "ExpressionAttributeValues": {":now": {"N": str(now)}},
                    }
                },
            ]
        )
    except Exception as exc:
        error_code = getattr(exc, "response", {}).get("Error", {}).get("Code")
        if error_code == "ValidationException":
            raise RuntimeError(
                "DynamoDB rejected the deployment maintenance-lock expression"
            ) from exc
        raise RuntimeError(
            "Refusing to deploy: an annotation workspace is active or another "
            "deployment holds the maintenance lock."
        ) from exc
    return deployment_id


def _release_deployment_lock(
    dynamodb: Any, table_name: str, deployment_id: str
) -> None:
    try:
        dynamodb.delete_item(
            TableName=table_name,
            Key={"pk": {"S": "PORTAL"}, "sk": {"S": "MAINTENANCE"}},
            ConditionExpression="deployment_id = :deployment_id",
            ExpressionAttributeValues={":deployment_id": {"S": deployment_id}},
        )
    except Exception:
        pass


def _unused_private_cidr(vpc_cidr: str, subnet_cidrs: list[str]) -> str:
    network = ipaddress.ip_network(vpc_cidr)
    if network.version != 4 or network.prefixlen > 24:
        raise RuntimeError("The selected VPC must contain an unused IPv4 /24")
    occupied = [ipaddress.ip_network(value) for value in subnet_cidrs]
    for candidate in network.subnets(new_prefix=24):
        if all(not candidate.overlaps(existing) for existing in occupied):
            return str(candidate)
    raise RuntimeError("The selected VPC has no unused IPv4 /24 for the gateway")


def _default_network(
    ec2: Any, requested_vpc: str | None
) -> tuple[str, str, str, str]:
    if requested_vpc:
        vpc_id = requested_vpc
        vpcs = ec2.describe_vpcs(VpcIds=[vpc_id])["Vpcs"]
    else:
        vpcs = ec2.describe_vpcs(Filters=[{"Name": "is-default", "Values": ["true"]}])[
            "Vpcs"
        ]
        if len(vpcs) != 1:
            raise RuntimeError("Could not resolve exactly one default VPC")
        vpc_id = vpcs[0]["VpcId"]
    all_subnets = ec2.describe_subnets(
        Filters=[{"Name": "vpc-id", "Values": [vpc_id]}]
    )["Subnets"]
    public_subnets = [row for row in all_subnets if row["MapPublicIpOnLaunch"]]
    if not public_subnets:
        raise RuntimeError("The selected VPC has no public-IPv4 subnet")
    subnet = sorted(
        public_subnets,
        key=lambda row: (row["AvailabilityZone"], row["SubnetId"]),
    )[0]
    private_cidr = _unused_private_cidr(
        vpcs[0]["CidrBlock"], [row["CidrBlock"] for row in all_subnets]
    )
    return vpc_id, subnet["SubnetId"], subnet["AvailabilityZone"], private_cidr


def _canonical_ubuntu_ami(ssm: Any, architecture: str = "amd64") -> str:
    name = (
        "/aws/service/canonical/ubuntu/server/24.04/stable/current/"
        f"{architecture}/hvm/ebs-gp3/ami-id"
    )
    return ssm.get_parameter(Name=name)["Parameter"]["Value"]


def _worker_ami(ec2: Any) -> str:
    images = ec2.describe_images(
        Owners=["self"],
        Filters=[
            {"Name": "state", "Values": ["available"]},
            {"Name": "name", "Values": ["osworld-client-30g-*"]},
        ],
    )["Images"]
    if not images:
        raise RuntimeError("No private osworld-client-30g worker AMI is available")
    return max(images, key=lambda row: row["CreationDate"])["ImageId"]


def _cloudfront_prefix_list(ec2: Any) -> str:
    response = ec2.describe_managed_prefix_lists(
        Filters=[
            {
                "Name": "prefix-list-name",
                "Values": ["com.amazonaws.global.cloudfront.origin-facing"],
            }
        ]
    )
    rows = response["PrefixLists"]
    if len(rows) != 1:
        raise RuntimeError("Could not resolve the CloudFront origin-facing prefix list")
    return rows[0]["PrefixListId"]


def _cloudfront_cache_policy(cloudfront: Any) -> str:
    response = cloudfront.list_cache_policies(Type="managed")
    rows = [
        item["CachePolicy"]
        for item in response.get("CachePolicyList", {}).get("Items", [])
        if item["CachePolicy"]["CachePolicyConfig"]["Name"]
        == "Managed-CachingDisabled"
    ]
    if len(rows) != 1:
        raise RuntimeError("Could not resolve Managed-CachingDisabled cache policy")
    return rows[0]["Id"]


def _parameters(
    args: argparse.Namespace,
    *,
    deploy_gateway: bool,
    vpc_id: str,
    gateway_subnet_id: str,
    gateway_availability_zone: str,
    gateway_private_subnet_cidr: str,
    worker_subnet_id: str,
    gateway_ami_id: str,
    nat_ami_id: str,
    worker_ami_id: str,
    prefix_list_id: str,
    cache_policy_id: str,
    source_key: str,
    source_sha256: str,
) -> list[dict[str, str]]:
    values = {
        "DeployGateway": str(deploy_gateway).lower(),
        "VpcId": vpc_id,
        "GatewaySubnetId": gateway_subnet_id,
        "GatewayAvailabilityZone": gateway_availability_zone,
        "GatewayPrivateSubnetCidr": gateway_private_subnet_cidr,
        "WorkerSubnetId": worker_subnet_id,
        "GatewayAmiId": gateway_ami_id,
        "NatAmiId": nat_ami_id,
        "WorkerAmiId": worker_ami_id,
        "CloudFrontOriginPrefixListId": prefix_list_id,
        "CloudFrontCachePolicyId": cache_policy_id,
        "GatewaySourceKey": source_key,
        "GatewaySourceSha256": source_sha256,
        "AssignmentPath": DEFAULT_ASSIGNMENTS,
        "AllowPending": str(args.allow_pending).lower(),
        "GatewayInstanceType": args.gateway_instance_type,
        "NatInstanceType": args.nat_instance_type,
        "WorkerInstanceType": args.worker_instance_type,
    }
    return [
        {"ParameterKey": key, "ParameterValue": value}
        for key, value in values.items()
    ]


def _wait(client: Any, waiter_name: str, stack_name: str) -> None:
    print(f"Waiting for CloudFormation {waiter_name.replace('_', ' ')} ...", flush=True)
    client.get_waiter(waiter_name).wait(
        StackName=stack_name,
        WaiterConfig={"Delay": 15, "MaxAttempts": 160},
    )


def _create_users(args: argparse.Namespace, user_pool_id: str) -> None:
    command = [
        sys.executable,
        str(REPO_ROOT / "scripts/python/create_annotation_portal_users.py"),
        "--profile",
        args.profile,
        "--region",
        args.region,
        "--user-pool-id",
        user_pool_id,
        "--credentials-output",
        str(args.credentials_output),
    ]
    subprocess.run(command, cwd=REPO_ROOT, check=True)


def _ensure_vpc_origin_ingress(
    ec2: Any, *, vpc_id: str, gateway_security_group_id: str
) -> str:
    from botocore.exceptions import ClientError

    groups = ec2.describe_security_groups(
        Filters=[
            {"Name": "vpc-id", "Values": [vpc_id]},
            {"Name": "group-name", "Values": ["CloudFront-VPCOrigins-Service-SG"]},
        ]
    )["SecurityGroups"]
    if len(groups) != 1:
        raise RuntimeError(
            "Could not resolve exactly one CloudFront VPC Origins service security group"
        )
    source_group_id = groups[0]["GroupId"]
    permission = {
        "IpProtocol": "tcp",
        "FromPort": 8080,
        "ToPort": 8080,
        "UserIdGroupPairs": [
            {
                "GroupId": source_group_id,
                "Description": "CloudFront VPC Origin runtime access",
            }
        ],
    }
    try:
        ec2.authorize_security_group_ingress(
            GroupId=gateway_security_group_id,
            IpPermissions=[permission],
        )
    except ClientError as exc:
        if exc.response.get("Error", {}).get("Code") != "InvalidPermission.Duplicate":
            raise
    return source_group_id


def _wait_for_ssm_online(ssm: Any, instance_id: str) -> None:
    for _ in range(60):
        rows = ssm.describe_instance_information(
            Filters=[{"Key": "InstanceIds", "Values": [instance_id]}]
        ).get("InstanceInformationList", [])
        if rows and rows[0].get("PingStatus") == "Online":
            return
        time.sleep(5)
    raise RuntimeError(f"Gateway {instance_id} did not become online in SSM")


def _refresh_gateway_source(
    ssm: Any,
    *,
    instance_id: str,
    bucket: str,
    source_key: str,
    source_sha256: str,
) -> None:
    _wait_for_ssm_online(ssm, instance_id)
    download_code = (
        "import boto3; "
        f"boto3.client('s3').download_file({bucket!r}, {source_key!r}, "
        "'/tmp/osworld-annotation-refresh.tar.gz')"
    )
    commands = [
        "set -eu",
        f"/usr/bin/python3 -c {shlex.quote(download_code)}",
        (
            f"printf '%s  %s\\n' {shlex.quote(source_sha256)} "
            "/tmp/osworld-annotation-refresh.tar.gz | sha256sum --check --strict"
        ),
        "systemctl stop osworld-annotation-portal.service",
        (
            "tar --extract --gzip --file /tmp/osworld-annotation-refresh.tar.gz "
            "--directory /opt/osworld"
        ),
        (
            "if [ ! -e /opt/osworld/live-pilot ]; then "
            "ln -sfnT /opt/osworld/evaluation_examples/expert_skill_learning/pilot "
            "/opt/osworld/live-pilot; fi"
        ),
        (
            "/opt/osworld/.venv/bin/pip install --disable-pip-version-check "
            "--no-cache-dir --requirement "
            "/opt/osworld/infra/annotation_portal/gateway-requirements.txt"
        ),
        "chown -R osworld:osworld /opt/osworld",
        "systemctl start osworld-annotation-portal.service",
        (
            "for attempt in $(seq 1 30); do "
            "curl --fail --silent http://127.0.0.1:8080/healthz && exit 0; "
            "sleep 2; done; journalctl -u osworld-annotation-portal.service "
            "-n 100 --no-pager; exit 1"
        ),
    ]
    response = ssm.send_command(
        InstanceIds=[instance_id],
        DocumentName="AWS-RunShellScript",
        Comment="Refresh OSWorld annotation portal source",
        Parameters={"commands": commands},
    )
    command_id = response["Command"]["CommandId"]
    waiter_error: Exception | None = None
    try:
        ssm.get_waiter("command_executed").wait(
            CommandId=command_id,
            InstanceId=instance_id,
            WaiterConfig={"Delay": 5, "MaxAttempts": 120},
        )
    except Exception as exc:
        waiter_error = exc
    result = ssm.get_command_invocation(
        CommandId=command_id, InstanceId=instance_id
    )
    if result.get("Status") != "Success":
        details = result.get("StandardErrorContent") or result.get(
            "StandardOutputContent", ""
        )
        raise RuntimeError(f"Gateway source refresh failed: {details[-4000:]}") from waiter_error


def main() -> int:
    args = parse_args()
    import boto3
    from botocore.exceptions import ClientError

    session = boto3.Session(profile_name=args.profile, region_name=args.region)
    cloudformation = session.client("cloudformation")
    ec2 = session.client("ec2")
    s3 = session.client("s3")
    is_new = not _stack_exists(cloudformation, args.stack_name)
    deployment_lock: tuple[Any, str, str] | None = None
    if not is_new:
        existing_outputs = _outputs(cloudformation, args.stack_name)
        dynamodb = session.client("dynamodb")
        deployment_id = _acquire_deployment_lock(
            dynamodb, existing_outputs["StateTableName"]
        )
        deployment_lock = (
            dynamodb,
            existing_outputs["StateTableName"],
            deployment_id,
        )
        atexit.register(_release_deployment_lock, *deployment_lock)
    current = {} if is_new else _stack_parameters(cloudformation, args.stack_name)
    vpc_id, default_subnet, availability_zone, default_private_cidr = (
        _default_network(ec2, args.vpc_id or current.get("VpcId"))
    )
    gateway_subnet = (
        args.gateway_subnet_id or current.get("GatewaySubnetId") or default_subnet
    )
    if args.gateway_subnet_id:
        gateway_subnet_row = ec2.describe_subnets(
            SubnetIds=[args.gateway_subnet_id]
        )["Subnets"][0]
        if gateway_subnet_row["VpcId"] != vpc_id:
            raise RuntimeError("Gateway public subnet is not in the selected VPC")
        if not gateway_subnet_row["MapPublicIpOnLaunch"]:
            raise RuntimeError("Gateway NAT subnet must assign public IPv4 addresses")
        availability_zone = gateway_subnet_row["AvailabilityZone"]
    else:
        availability_zone = current.get(
            "GatewayAvailabilityZone", availability_zone
        )
    worker_subnet = (
        args.worker_subnet_id or current.get("WorkerSubnetId") or default_subnet
    )
    gateway_ami = (
        args.gateway_ami_id
        or current.get("GatewayAmiId")
        or _canonical_ubuntu_ami(session.client("ssm"))
    )
    nat_ami = (
        args.nat_ami_id
        or current.get("NatAmiId")
        or _canonical_ubuntu_ami(session.client("ssm"), architecture="arm64")
    )
    worker_ami = args.worker_ami_id or current.get("WorkerAmiId") or _worker_ami(ec2)
    prefix_list = _cloudfront_prefix_list(ec2)
    cache_policy = _cloudfront_cache_policy(session.client("cloudfront"))

    with tempfile.TemporaryDirectory(prefix="osworld-portal-") as temp_dir:
        bundle = Path(temp_dir) / "gateway-source.tar.gz"
        source_sha256 = build_source_bundle(bundle)
        source_key = f"bootstrap/gateway-source-{source_sha256}.tar.gz"
        common = dict(
            vpc_id=vpc_id,
            gateway_subnet_id=gateway_subnet,
            gateway_availability_zone=availability_zone,
            gateway_private_subnet_cidr=(
                args.gateway_private_subnet_cidr
                or current.get("GatewayPrivateSubnetCidr")
                or default_private_cidr
            ),
            worker_subnet_id=worker_subnet,
            gateway_ami_id=gateway_ami,
            nat_ami_id=nat_ami,
            worker_ami_id=worker_ami,
            prefix_list_id=prefix_list,
            cache_policy_id=cache_policy,
            source_key=source_key,
            source_sha256=source_sha256,
        )

        if is_new:
            print("Creating the non-compute control plane ...", flush=True)
            cloudformation.create_stack(
                StackName=args.stack_name,
                TemplateBody=TEMPLATE_PATH.read_text(encoding="utf-8"),
                Parameters=_parameters(args, deploy_gateway=False, **common),
                Capabilities=["CAPABILITY_NAMED_IAM"],
                OnFailure="ROLLBACK",
                Tags=[
                    {"Key": "Project", "Value": "OSWorld-Expert-Skill-Learning"},
                    {"Key": "Component", "Value": "AnnotationPortal"},
                ],
            )
            _wait(cloudformation, "stack_create_complete", args.stack_name)

        control_outputs = _outputs(cloudformation, args.stack_name)
        bucket = control_outputs["AnnotationBucketName"]
        print(f"Uploading verified gateway source bundle ({source_sha256[:12]}) ...")
        s3.upload_file(
            str(bundle),
            bucket,
            source_key,
            ExtraArgs={"Metadata": {"sha256": source_sha256}},
        )
        metadata = s3.head_object(Bucket=bucket, Key=source_key).get("Metadata", {})
        if metadata.get("sha256") != source_sha256:
            raise RuntimeError("Uploaded gateway source metadata verification failed")

        if is_new and not args.skip_user_creation:
            _create_users(args, control_outputs["UserPoolId"])

        print("Deploying the gateway and CloudFront HTTPS endpoint ...", flush=True)
        try:
            cloudformation.update_stack(
                StackName=args.stack_name,
                TemplateBody=TEMPLATE_PATH.read_text(encoding="utf-8"),
                Parameters=_parameters(args, deploy_gateway=True, **common),
                Capabilities=["CAPABILITY_NAMED_IAM"],
            )
        except ClientError as exc:
            if "No updates are to be performed" not in str(exc):
                raise
        else:
            _wait(cloudformation, "stack_update_complete", args.stack_name)

    outputs = _outputs(cloudformation, args.stack_name)
    service_group_id = _ensure_vpc_origin_ingress(
        ec2,
        vpc_id=vpc_id,
        gateway_security_group_id=outputs["GatewaySecurityGroupId"],
    )
    print("Refreshing the running gateway source through SSM ...", flush=True)
    _refresh_gateway_source(
        session.client("ssm"),
        instance_id=outputs["GatewayInstanceId"],
        bucket=outputs["AnnotationBucketName"],
        source_key=source_key,
        source_sha256=source_sha256,
    )
    print(json.dumps(outputs, indent=2, sort_keys=True))
    print(f"CloudFront VPC Origin ingress is restricted to {service_group_id}.")
    print("Portal deployment is complete. Verify PortalUrl/healthz before sharing it.")
    if deployment_lock:
        _release_deployment_lock(*deployment_lock)
        atexit.unregister(_release_deployment_lock)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
