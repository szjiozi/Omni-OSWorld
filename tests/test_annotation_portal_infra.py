from pathlib import Path
import importlib.util
import tarfile

import yaml


class _CloudFormationLoader(yaml.SafeLoader):
    pass


def _construct_tag(loader, tag_suffix, node):
    if isinstance(node, yaml.ScalarNode):
        value = loader.construct_scalar(node)
    elif isinstance(node, yaml.SequenceNode):
        value = loader.construct_sequence(node)
    else:
        value = loader.construct_mapping(node)
    return {tag_suffix: value}


_CloudFormationLoader.add_multi_constructor("!", _construct_tag)


def _template():
    path = Path(__file__).parents[1] / "infra/annotation_portal/template.yaml"
    return yaml.load(path.read_text(encoding="utf-8"), Loader=_CloudFormationLoader)


def test_portal_template_uses_private_cloudfront_origin_and_no_open_worker_ports():
    template = _template()
    resources = template["Resources"]

    origin = resources["PortalVpcOrigin"]
    assert origin["Type"] == "AWS::CloudFront::VpcOrigin"
    distribution = resources["PortalDistribution"]["Properties"]["DistributionConfig"]
    assert distribution["ViewerCertificate"]["CloudFrontDefaultCertificate"] is True
    assert "VpcOriginConfig" in distribution["Origins"][0]
    assert distribution["DefaultCacheBehavior"]["ViewerProtocolPolicy"] == "redirect-to-https"

    worker_ingress = resources["WorkerSecurityGroup"]["Properties"][
        "SecurityGroupIngress"
    ]
    assert {rule["FromPort"] for rule in worker_ingress} == {5000, 5910}
    assert all("SourceSecurityGroupId" in rule for rule in worker_ingress)
    assert all("CidrIp" not in rule for rule in worker_ingress)


def test_portal_template_disables_signup_and_keeps_results_private():
    resources = _template()["Resources"]
    user_pool = resources["PortalUserPool"]["Properties"]
    assert user_pool["AdminCreateUserConfig"]["AllowAdminCreateUserOnly"] is True

    bucket = resources["AnnotationBucket"]["Properties"]
    public = bucket["PublicAccessBlockConfiguration"]
    assert all(public.values())
    assert bucket["VersioningConfiguration"]["Status"] == "Enabled"

    gateway_data = resources["GatewayInstance"]["Properties"]["UserData"]
    rendered = str(gateway_data)
    assert "ENABLE_TTL=true" in rendered
    assert "AWS_SCHEDULER_ROLE_ARN" in rendered
    assert "--pilot-root" in rendered
    assert "live-pilot" in rendered

    assert resources["GatewayRole"]["Properties"]["RoleName"] == (
        "osworld-annotation-portal-gateway"
    )
    assert resources["SchedulerExecutionRole"]["Properties"]["RoleName"] == (
        "osworld-annotation-portal-scheduler"
    )
    assert resources["GatewayInstanceProfile"]["Properties"][
        "InstanceProfileName"
    ] == "osworld-annotation-portal-gateway"
    assert resources["WorkerRole"]["Properties"]["RoleName"] == (
        "osworld-annotation-portal-worker-v2"
    )
    assert resources["WorkerInstanceProfile"]["Properties"][
        "InstanceProfileName"
    ] == "osworld-annotation-portal-worker-v2"
    worker_actions = {
        action
        for policy in resources["WorkerRole"]["Properties"]["Policies"]
        for statement in policy["PolicyDocument"]["Statement"]
        for action in statement["Action"]
    }
    assert "ssm:UpdateInstanceInformation" in worker_actions
    assert "ssmmessages:OpenControlChannel" in worker_actions


def test_gateway_role_can_register_with_ssm_for_private_diagnostics():
    policies = _template()["Resources"]["GatewayRole"]["Properties"]["Policies"]
    actions = {
        action
        for policy in policies
        for statement in policy["PolicyDocument"]["Statement"]
        for action in (
            statement["Action"]
            if isinstance(statement["Action"], list)
            else [statement["Action"]]
        )
    }

    assert "ssm:UpdateInstanceInformation" in actions
    assert "ssm:DescribeInstanceInformation" in actions
    assert "ssm:SendCommand" in actions
    assert "ssm:GetCommandInvocation" in actions
    assert "ssmmessages:OpenControlChannel" in actions
    assert "ec2messages:GetMessages" in actions
    assert "s3:PutObjectTagging" in actions
    assert "s3:DeleteObjectVersion" in actions
    assert "s3:ListBucketVersions" in actions
    assert "dynamodb:ConditionCheckItem" in actions


def test_recording_state_update_preserves_authenticated_novnc_iframe():
    source = (
        Path(__file__).parents[1]
        / "benchmark_construction/annotation_portal/static/assets/app.js"
    ).read_text(encoding="utf-8")

    assert 'const existingDesktop = node.querySelector(".desktop-frame")' in source
    assert "desktopReady && existingDesktop" in source
    assert "node.dataset.sessionId === workspace.session_id" in source
    assert 'node.querySelector("#start-recording").disabled = !canStart' in source


def test_gateway_bundle_includes_online_review_validation_schema():
    deployer = (
        Path(__file__).parents[1] / "scripts/python/deploy_annotation_portal.py"
    ).read_text(encoding="utf-8")

    assert '"evaluation_examples/expert_skill_learning/schemas"' in deployer
    assert "reference-package-review.schema.json" in (
        Path(__file__).parents[1]
        / "evaluation_examples/expert_skill_learning/schemas/reference-package-review.schema.json"
    ).read_text(encoding="utf-8")


def test_gateway_is_a_two_phase_private_self_bootstrap_behind_nat():
    template = _template()
    resources = template["Resources"]
    gateway = resources["GatewayInstance"]

    assert gateway["Condition"] == "GatewayEnabled"
    assert gateway["Properties"]["SubnetId"] == {
        "Ref": "GatewayPrivateSubnet"
    }
    assert "NetworkInterfaces" not in gateway["Properties"]
    nat = resources["NatInstance"]
    assert nat["Condition"] == "GatewayEnabled"
    assert nat["Properties"]["SourceDestCheck"] is False
    assert nat["Properties"]["NetworkInterfaces"][0][
        "AssociatePublicIpAddress"
    ] is True
    assert resources["GatewayPrivateDefaultRoute"]["Properties"][
        "InstanceId"
    ] == {"Ref": "NatInstance"}
    assert resources["PortalVpcOrigin"]["Condition"] == "GatewayEnabled"
    assert resources["PortalDistribution"]["Condition"] == "GatewayEnabled"
    distribution = resources["PortalDistribution"]["Properties"][
        "DistributionConfig"
    ]
    assert distribution["DefaultCacheBehavior"]["CachePolicyId"] == {
        "Ref": "CloudFrontCachePolicyId"
    }

    rendered = str(gateway["Properties"]["UserData"])
    assert "GatewaySourceKey" in rendered
    assert "GatewaySourceSha256" in rendered
    assert "sha256sum --check --strict" in rendered
    assert "gateway-requirements.txt" in rendered
    assert "AWS_EBS_IOPS=3000" in rendered
    assert "AWS_EBS_THROUGHPUT_MIBPS=125" in rendered
    assert "AWS_EC2_INSTANCE_PROFILE_NAME" in rendered


def test_gateway_source_bundle_is_deterministic_and_excludes_local_noise(tmp_path):
    script = (
        Path(__file__).parents[1] / "scripts/python/deploy_annotation_portal.py"
    )
    spec = importlib.util.spec_from_file_location("deploy_annotation_portal", script)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)

    first = tmp_path / "first.tar.gz"
    second = tmp_path / "second.tar.gz"
    first_hash = module.build_source_bundle(first)
    second_hash = module.build_source_bundle(second)
    assert first_hash == second_hash

    with tarfile.open(first, "r:gz") as archive:
        names = archive.getnames()
    assert "scripts/python/run_annotation_portal.py" in names
    assert "benchmark_construction/models.py" in names
    assert "infra/annotation_portal/gateway-requirements.txt" in names
    assert all("secret_keys" not in name for name in names)
    assert all(".DS_Store" not in name for name in names)
    assert all("__pycache__" not in name for name in names)


def test_private_gateway_cidr_selection_avoids_existing_subnets():
    script = (
        Path(__file__).parents[1] / "scripts/python/deploy_annotation_portal.py"
    )
    spec = importlib.util.spec_from_file_location("deploy_annotation_portal_cidr", script)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)

    selected = module._unused_private_cidr(
        "172.31.0.0/16",
        ["172.31.0.0/20", "172.31.16.0/20", "172.31.32.0/20"],
    )
    assert selected == "172.31.48.0/24"


def test_deployer_acknowledges_named_iam_resources():
    script = (
        Path(__file__).parents[1] / "scripts/python/deploy_annotation_portal.py"
    ).read_text(encoding="utf-8")
    assert script.count('Capabilities=["CAPABILITY_NAMED_IAM"]') == 2
    assert 'Capabilities=["CAPABILITY_IAM"]' not in script
    assert "worker_instance_profile_name" in script
    assert "AWS_EC2_INSTANCE_PROFILE_NAME=" in script


class _FakeEc2SecurityGroups:
    def __init__(self):
        self.authorized = []

    def describe_security_groups(self, **kwargs):
        return {"SecurityGroups": [{"GroupId": "sg-cloudfront"}]}

    def authorize_security_group_ingress(self, **kwargs):
        self.authorized.append(kwargs)


def test_deployer_allows_only_cloudfront_vpc_origin_sg_to_gateway():
    script = (
        Path(__file__).parents[1] / "scripts/python/deploy_annotation_portal.py"
    )
    spec = importlib.util.spec_from_file_location("deploy_annotation_portal_sg", script)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    ec2 = _FakeEc2SecurityGroups()

    source = module._ensure_vpc_origin_ingress(
        ec2, vpc_id="vpc-test", gateway_security_group_id="sg-gateway"
    )

    assert source == "sg-cloudfront"
    call = ec2.authorized[0]
    assert call["GroupId"] == "sg-gateway"
    permission = call["IpPermissions"][0]
    assert permission["FromPort"] == permission["ToPort"] == 8080
    assert permission["UserIdGroupPairs"][0]["GroupId"] == "sg-cloudfront"


class _FakeCloudFormationStack:
    def describe_stacks(self, **kwargs):
        return {
            "Stacks": [
                {
                    "Parameters": [
                        {
                            "ParameterKey": "GatewayPrivateSubnetCidr",
                            "ParameterValue": "172.31.48.0/24",
                        },
                        {"ParameterKey": "VpcId", "ParameterValue": "vpc-test"},
                    ]
                }
            ]
        }


def test_deployer_can_reuse_existing_stack_network_parameters():
    script = (
        Path(__file__).parents[1] / "scripts/python/deploy_annotation_portal.py"
    )
    spec = importlib.util.spec_from_file_location(
        "deploy_annotation_portal_parameters", script
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)

    parameters = module._stack_parameters(
        _FakeCloudFormationStack(), "osworld-annotation-portal"
    )

    assert parameters == {
        "GatewayPrivateSubnetCidr": "172.31.48.0/24",
        "VpcId": "vpc-test",
    }


class _FakeWaiter:
    def __init__(self):
        self.calls = []

    def wait(self, **kwargs):
        self.calls.append(kwargs)


class _FakeSsm:
    def __init__(self):
        self.sent = []
        self.waiter = _FakeWaiter()

    def describe_instance_information(self, **kwargs):
        return {"InstanceInformationList": [{"PingStatus": "Online"}]}

    def send_command(self, **kwargs):
        self.sent.append(kwargs)
        return {"Command": {"CommandId": "command-test"}}

    def get_waiter(self, name):
        assert name == "command_executed"
        return self.waiter

    def get_command_invocation(self, **kwargs):
        return {"Status": "Success"}


def test_deployer_refreshes_content_addressed_gateway_bundle_through_ssm():
    script = (
        Path(__file__).parents[1] / "scripts/python/deploy_annotation_portal.py"
    )
    spec = importlib.util.spec_from_file_location("deploy_annotation_portal_ssm", script)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    ssm = _FakeSsm()

    module._refresh_gateway_source(
        ssm,
        instance_id="i-gateway",
        bucket="annotation-bucket",
        source_key="bootstrap/source-hash.tar.gz",
        source_sha256="a" * 64,
        worker_instance_profile_name="osworld-annotation-portal-worker-v2",
    )

    command = ssm.sent[0]
    assert command["InstanceIds"] == ["i-gateway"]
    rendered = "\n".join(command["Parameters"]["commands"])
    assert "set -eu" in rendered
    assert "pipefail" not in rendered
    assert "bootstrap/source-hash.tar.gz" in rendered
    assert "sha256sum --check --strict" in rendered
    assert "systemctl start osworld-annotation-portal.service" in rendered
    assert "--pilot-root /opt/osworld/live-pilot --assignments" in rendered
    assert "systemctl daemon-reload" in rendered
    assert "AWS_EC2_INSTANCE_PROFILE_NAME=" in rendered
    assert "osworld-annotation-portal-worker-v2" in rendered
    assert "127.0.0.1:8080/healthz" in rendered
    assert "live-pilot" in rendered


class _FakeDynamoActiveCount:
    def __init__(self, count):
        self.count = count

    def get_item(self, **kwargs):
        return {"Item": {"active_count": {"N": str(self.count)}}}


def test_deployer_reads_active_workspace_count_before_gateway_restart():
    script = Path(__file__).parents[1] / "scripts/python/deploy_annotation_portal.py"
    spec = importlib.util.spec_from_file_location("deploy_annotation_portal_active", script)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)

    assert module._active_workspace_count(_FakeDynamoActiveCount(3), "table") == 3


class _FakeDynamoMaintenance:
    def __init__(self):
        self.transactions = []
        self.deletes = []

    def transact_write_items(self, **kwargs):
        self.transactions.append(kwargs)

    def delete_item(self, **kwargs):
        self.deletes.append(kwargs)


def test_deployer_uses_expiring_atomic_maintenance_lock():
    script = Path(__file__).parents[1] / "scripts/python/deploy_annotation_portal.py"
    spec = importlib.util.spec_from_file_location("deploy_annotation_portal_lock", script)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    dynamodb = _FakeDynamoMaintenance()

    deployment_id = module._acquire_deployment_lock(dynamodb, "table")
    module._release_deployment_lock(dynamodb, "table", deployment_id)

    transaction = dynamodb.transactions[0]["TransactItems"]
    assert "active_count = :zero" in transaction[0]["ConditionCheck"]["ConditionExpression"]
    lock = transaction[1]["Put"]["Item"]
    assert lock["sk"] == {"S": "MAINTENANCE"}
    assert lock["ttl"]["N"].isdigit()
    assert transaction[1]["Put"]["ExpressionAttributeNames"] == {"#ttl": "ttl"}
    assert dynamodb.deletes[0]["ConditionExpression"] == (
        "deployment_id = :deployment_id"
    )


def test_workspace_admission_checks_deployment_maintenance_lock():
    source = (
        Path(__file__).parents[1]
        / "benchmark_construction/annotation_portal/store.py"
    ).read_text(encoding="utf-8")
    assert '"sk": "MAINTENANCE"' in source
    assert "attribute_not_exists(blocked) OR #ttl < :now" in source
