import hashlib
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
import requests

from benchmark_construction.aws_annotation import (
    active_project_instance_ids,
    arm_guest_termination_backstop,
    refresh_annotation_ingress,
    resolve_annotation_aws_resources,
    start_ssm_port_forward,
    start_ssm_ssh_forward,
    wait_for_novnc_ready,
    wait_for_osworld_api,
    wait_for_ssm_online,
)
from benchmark_construction.reference_annotation import (
    assemble_osworld_annotation_config,
    build_annotation_blueprint_request,
    load_review_decisions,
    require_launchable_review,
    validate_annotation_blueprint,
)
from benchmark_construction.schema import load_schema
from scripts.python.record_reference_task import (
    _configure_aws,
    _load_task_config,
    _novnc_preview_url,
    _retarget_env_to_local_api,
    _save_guest_workbook,
    _validate_recording_options,
    parse_args,
)


def test_novnc_preview_url_uses_low_bandwidth_settings():
    assert _novnc_preview_url("127.0.0.1", 15910) == (
        "http://127.0.0.1:15910/vnc.html?"
        "autoconnect=true&resize=scale&quality=0&compression=9"
    )


def test_reference_annotation_disables_periodic_screenshots_by_default(
    monkeypatch,
):
    monkeypatch.setattr(
        sys,
        "argv",
        ["record_reference_task.py", "--reference-task-id", "reference-task"],
    )

    assert parse_args().sample_interval == 0.0


def _package() -> dict:
    return {
        "reference_task_id": "reference-task-r01-001",
        "app": "libreoffice_calc",
        "task_instruction": "Create a concise summary in the workbook.",
        "required_skill_ids": ["source.skill-01"],
        "artifact_spec": {"initial_state": ["The raw table is visible."]},
        "operator_guide": {
            "recommended_demonstration": [],
            "allowed_variation": "Equivalent Calc operations are allowed.",
            "recording_start_state": "The raw table is open.",
            "recording_end_state": "The summary is visible.",
        },
        "expected_incidental_operations": [],
    }


def _blueprint() -> dict:
    return {
        "snapshot": "libreoffice_calc",
        "artifact_slot": "initial_artifact",
        "guest_filename": "workshop-enrollment.xlsx",
        "open_after_upload": True,
        "ready_state_checks": ["The raw table is visible in Calc."],
        "setup_notes": [],
    }


def _manifest_entry(repo_root: Path, content: bytes = b"xlsx") -> dict:
    artifact = repo_root / "artifacts" / "initial_artifact.xlsx"
    artifact.parent.mkdir(parents=True)
    artifact.write_bytes(content)
    return {
        "reference_task_id": "reference-task-r01-001",
        "artifact_path": "artifacts/initial_artifact.xlsx",
        "artifact_sha256": hashlib.sha256(content).hexdigest(),
        "manual_setup_required": False,
        "manual_setup_steps": [],
    }


def test_annotation_blueprint_schema_is_valid_and_rejects_paths():
    assert load_schema("reference-annotation-blueprint.schema.json")[
        "$schema"
    ].endswith("2020-12/schema")
    validate_annotation_blueprint(_blueprint())

    unsafe = {**_blueprint(), "guest_filename": "../escape.xlsx"}
    with pytest.raises(Exception):
        validate_annotation_blueprint(unsafe)


def test_annotation_blueprint_prompt_excludes_trusted_paths_and_hashes(tmp_path):
    package = _package()
    entry = {
        **_manifest_entry(tmp_path),
        "artifact_path": "/secret/host/path.xlsx",
        "artifact_sha256": "secret-hash",
    }

    request = build_annotation_blueprint_request(package, entry)

    assert "upload_file" in request.system_prompt
    assert "trusted local assembler" in request.system_prompt
    assert "/secret/host/path.xlsx" not in request.user_prompt
    assert "secret-hash" not in request.user_prompt


def test_assembler_injects_only_standard_actions_and_verified_artifact(tmp_path):
    entry = _manifest_entry(tmp_path)

    config = assemble_osworld_annotation_config(
        _package(), entry, _blueprint(), repo_root=tmp_path
    )

    assert [step["type"] for step in config["config"]] == [
        "upload_file",
        "open",
    ]
    uploaded = config["config"][0]["parameters"]["files"][0]
    assert uploaded["local_path"] == "artifacts/initial_artifact.xlsx"
    assert uploaded["path"] == "/home/user/Desktop/workshop-enrollment.xlsx"
    assert config["config"][1]["parameters"]["path"] == uploaded["path"]
    assert "evaluator" not in config
    assert config["reference_annotation"]["artifact_sha256"] == entry["artifact_sha256"]


def test_assembler_rejects_changed_artifact(tmp_path):
    entry = _manifest_entry(tmp_path)
    (tmp_path / entry["artifact_path"]).write_bytes(b"changed")

    with pytest.raises(ValueError, match="SHA256 mismatch"):
        assemble_osworld_annotation_config(
            _package(), entry, _blueprint(), repo_root=tmp_path
        )


def test_review_gate_allows_approved_and_explicit_pending_only(tmp_path):
    review_path = tmp_path / "reviews.json"
    review_path.write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "reviews": [
                    {
                        "reference_task_id": "approved-task",
                        "decision": "approved",
                        "reason_codes": [],
                        "revision_instructions": [],
                        "reviewer": "reviewer@example.test",
                        "notes": "",
                    },
                    {
                        "reference_task_id": "pending-task",
                        "decision": "",
                        "reason_codes": [],
                        "revision_instructions": [],
                        "reviewer": "",
                        "notes": "",
                    },
                    {
                        "reference_task_id": "rejected-task",
                        "decision": "rejected",
                        "reason_codes": ["unnatural"],
                        "revision_instructions": [],
                        "reviewer": "reviewer@example.test",
                        "notes": "",
                    },
                ],
            }
        ),
        encoding="utf-8",
    )
    decisions = load_review_decisions(review_path)

    assert require_launchable_review("approved-task", decisions) == "approved"
    with pytest.raises(ValueError, match="pending review"):
        require_launchable_review("pending-task", decisions)
    assert (
        require_launchable_review("pending-task", decisions, allow_pending=True)
        == "pending"
    )
    with pytest.raises(ValueError, match="not launchable"):
        require_launchable_review("rejected-task", decisions, allow_pending=True)


class _FakeEc2:
    def __init__(self):
        self.revoked = []
        self.authorized = []

    def describe_security_groups(self, **_kwargs):
        return {
            "SecurityGroups": [
                {
                    "IpPermissions": [
                        {
                            "IpProtocol": "tcp",
                            "FromPort": 5000,
                            "ToPort": 5000,
                            "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
                            "Ipv6Ranges": [],
                        },
                        {
                            "IpProtocol": "tcp",
                            "FromPort": 5910,
                            "ToPort": 5910,
                            "IpRanges": [{"CidrIp": "203.0.113.7/32"}],
                            "Ipv6Ranges": [],
                        },
                    ]
                }
            ]
        }

    def describe_instances(self, **_kwargs):
        return {
            "Reservations": [
                {
                    "Instances": [
                        {"InstanceId": "i-0123456789abcdef0"},
                        {"InstanceId": "i-11111111111111111"},
                    ]
                }
            ]
        }

    def revoke_security_group_ingress(self, **kwargs):
        self.revoked.append(kwargs)

    def authorize_security_group_ingress(self, **kwargs):
        self.authorized.append(kwargs)


def test_security_group_refresh_replaces_stale_public_ranges():
    ec2 = _FakeEc2()

    result = refresh_annotation_ingress(ec2, "sg-0123456789abcdef0", "203.0.113.7")

    assert result["cidr"] == "203.0.113.7/32"
    assert result["revoked_ranges"] == 1
    assert result["added_rules"] == 1
    assert ec2.revoked[0]["IpPermissions"][0]["IpRanges"] == [{"CidrIp": "0.0.0.0/0"}]
    assert ec2.authorized[0]["IpPermissions"][0]["FromPort"] == 5000


def test_active_project_instance_ids_are_flattened():
    assert active_project_instance_ids(_FakeEc2(), "OSWorld-Test") == [
        "i-0123456789abcdef0",
        "i-11111111111111111",
    ]


def test_osworld_api_waits_through_transient_connect_failure():
    class FakeSession:
        trust_env = True

        def __init__(self):
            self.calls = 0

        def get(self, url, timeout):
            assert url == "http://203.0.113.8:5000/platform"
            assert timeout == (3, 5)
            self.calls += 1
            if self.calls == 1:
                raise requests.ConnectTimeout("guest is still starting")
            return SimpleNamespace(status_code=200)

    session = FakeSession()
    elapsed = wait_for_osworld_api(
        "203.0.113.8",
        timeout_seconds=1,
        poll_seconds=0,
        session=session,
    )

    assert elapsed >= 0
    assert session.calls == 2
    assert session.trust_env is False


def test_novnc_readiness_requires_html_websocket_and_rfb():
    class FakeResponse:
        status_code = 200
        content = b"<title>noVNC</title>"

        def raise_for_status(self):
            return None

    class FakeSession:
        trust_env = True

        def get(self, url, timeout):
            assert url == "http://127.0.0.1:15910/vnc.html"
            assert timeout == (5, 20)
            return FakeResponse()

    class FakeSocket:
        def __init__(self):
            self.sent = b""
            self.chunks = [
                b"HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\n\r\n"
                b"\x82\x0cRFB 003.008\n"
            ]

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def settimeout(self, _timeout):
            return None

        def sendall(self, content):
            self.sent = content

        def recv(self, _size):
            return self.chunks.pop(0)

    stream = FakeSocket()
    session = FakeSession()
    elapsed = wait_for_novnc_ready(
        "127.0.0.1",
        15910,
        session=session,
        connection_factory=lambda address, timeout: stream,
    )

    assert elapsed >= 0
    assert session.trust_env is False
    assert b"GET /websockify HTTP/1.1" in stream.sent


def test_ssm_waits_until_instance_is_online():
    class FakeSsm:
        def __init__(self):
            self.calls = 0

        def describe_instance_information(self, **kwargs):
            assert kwargs["Filters"][0]["Values"] == ["i-0123456789abcdef0"]
            self.calls += 1
            status = "ConnectionLost" if self.calls == 1 else "Online"
            return {"InstanceInformationList": [{"PingStatus": status}]}

    client = FakeSsm()
    assert wait_for_ssm_online(
        client, "i-0123456789abcdef0", timeout_seconds=1, poll_seconds=0
    ) >= 0
    assert client.calls == 2


def test_guest_termination_backstop_waits_for_systemd_timer():
    class FakeSsm:
        def __init__(self):
            self.sent = None

        def send_command(self, **kwargs):
            self.sent = kwargs
            return {"Command": {"CommandId": "command-ttl"}}

        def get_command_invocation(self, **kwargs):
            assert kwargs == {
                "CommandId": "command-ttl",
                "InstanceId": "i-0123456789abcdef0",
            }
            return {"Status": "Success"}

    client = FakeSsm()
    command_id = arm_guest_termination_backstop(
        client,
        "i-0123456789abcdef0",
        ttl_minutes=180,
    )

    assert command_id == "command-ttl"
    command = client.sent["Parameters"]["commands"][0]
    assert "--on-active=180min" in command
    assert "/usr/bin/systemctl poweroff" in command


def test_guest_termination_backstop_rejects_short_ttl():
    with pytest.raises(ValueError, match="at least 30 minutes"):
        arm_guest_termination_backstop(
            SimpleNamespace(),
            "i-0123456789abcdef0",
            ttl_minutes=10,
        )


def test_ssm_port_forward_starts_listener_and_closes(monkeypatch):
    class FakeConnection:
        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

    class FakeProcess:
        def __init__(self):
            self.returncode = None
            self.stdout = None
            self.terminated = False

        def poll(self):
            return None

        def terminate(self):
            self.terminated = True

        def wait(self, timeout):
            assert timeout == 10
            return 0

    process = FakeProcess()
    commands = []
    monkeypatch.setattr(
        "benchmark_construction.aws_annotation.shutil.which",
        lambda name: f"/env/bin/{name}",
    )
    monkeypatch.setattr(
        "benchmark_construction.aws_annotation._free_local_port", lambda: 15432
    )
    monkeypatch.setattr(
        "benchmark_construction.aws_annotation.subprocess.Popen",
        lambda command, **_kwargs: commands.append(command) or process,
    )
    monkeypatch.setattr(
        "benchmark_construction.aws_annotation.socket.create_connection",
        lambda address, timeout: FakeConnection(),
    )

    tunnel = start_ssm_port_forward(
        "i-0123456789abcdef0",
        5910,
        profile="osworld-dev",
        region="ap-east-1",
    )

    assert tunnel.local_port == 15432
    parameters = commands[0][commands[0].index("--parameters") + 1]
    assert '"portNumber":["5910"]' in parameters
    assert '"localPortNumber":["15432"]' in parameters
    tunnel.close()
    assert process.terminated is True


def test_ssm_ssh_forward_builds_multiplexed_api_and_novnc_tunnel(
    monkeypatch, tmp_path
):
    class FakeDirectory:
        name = str(tmp_path)
        cleaned = False

        def cleanup(self):
            self.cleaned = True

    class FakeProcess:
        returncode = None
        stdout = None

        def __init__(self):
            self.terminated = False

        def poll(self):
            return None

        def terminate(self):
            self.terminated = True

        def wait(self, timeout):
            assert timeout == 10
            return 0

    class FakeSsmForward:
        local_port = 52222

        def __init__(self):
            self.closed = False

        def close(self):
            self.closed = True

    class FakeSsm:
        def __init__(self):
            self.parameters = None

        def send_command(self, **kwargs):
            self.parameters = kwargs
            return {"Command": {"CommandId": "command-1"}}

    directory = FakeDirectory()
    process = FakeProcess()
    ssm_forward = FakeSsmForward()
    ssm_client = FakeSsm()
    popen_commands = []
    ports = iter((15000, 15910))

    def fake_keygen(command, **_kwargs):
        key_path = Path(command[command.index("-f") + 1])
        key_path.write_text("private", encoding="utf-8")
        key_path.with_suffix(".pub").write_text(
            "ssh-ed25519 AAAATEST osworld-ephemeral-tunnel\n", encoding="utf-8"
        )

    monkeypatch.setattr(
        "benchmark_construction.aws_annotation.shutil.which",
        lambda name: f"/usr/bin/{name}",
    )
    monkeypatch.setattr(
        "benchmark_construction.aws_annotation.tempfile.TemporaryDirectory",
        lambda **_kwargs: directory,
    )
    monkeypatch.setattr(
        "benchmark_construction.aws_annotation.subprocess.run", fake_keygen
    )
    monkeypatch.setattr(
        "benchmark_construction.aws_annotation._wait_for_ssm_command",
        lambda *_args, **_kwargs: None,
    )
    monkeypatch.setattr(
        "benchmark_construction.aws_annotation.start_ssm_port_forward",
        lambda *_args, **_kwargs: ssm_forward,
    )
    monkeypatch.setattr(
        "benchmark_construction.aws_annotation._free_local_port",
        lambda: next(ports),
    )
    monkeypatch.setattr(
        "benchmark_construction.aws_annotation.subprocess.Popen",
        lambda command, **_kwargs: popen_commands.append(command) or process,
    )
    monkeypatch.setattr(
        "benchmark_construction.aws_annotation._wait_for_local_ports",
        lambda *_args, **_kwargs: None,
    )

    tunnel = start_ssm_ssh_forward(
        ssm_client,
        "i-0123456789abcdef0",
        profile="osworld-dev",
        region="ap-east-1",
    )

    assert tunnel.api_port == 15000
    assert tunnel.novnc_port == 15910
    assert "15000:127.0.0.1:5000" in popen_commands[0]
    assert "15910:127.0.0.1:5910" in popen_commands[0]
    assert "authorized_keys" in ssm_client.parameters["Parameters"]["commands"][0]
    tunnel.close()
    assert process.terminated is True
    assert ssm_forward.closed is True
    assert directory.cleaned is True


def test_annotation_resources_resolve_hong_kong_without_us_fallback():
    resources = resolve_annotation_aws_resources(
        {
            "AWS_SUBNET_ID": "subnet-aaaaaaaaaaaaaaaaa",
            "AWS_SECURITY_GROUP_ID": "sg-bbbbbbbbbbbbbbbbb",
            "AWS_AP_EAST_1_SUBNET_ID": "subnet-11111111111111111",
            "AWS_AP_EAST_1_SECURITY_GROUP_ID": "sg-22222222222222222",
            "AWS_AP_EAST_1_AMI_ID": "ami-33333333333333333",
        },
        "ap-east-1",
    )

    assert resources.subnet_id == "subnet-11111111111111111"
    assert resources.security_group_id == "sg-22222222222222222"
    assert resources.ami_id == "ami-33333333333333333"
    assert resources.ami_distribution == "private_encrypted_copy"
    assert resources.source_ami_id == "ami-0d23263edb96951d8"


def test_annotation_resources_preserve_us_legacy_fallback():
    resources = resolve_annotation_aws_resources(
        {
            "AWS_SUBNET_ID": "subnet-aaaaaaaaaaaaaaaaa",
            "AWS_SECURITY_GROUP_ID": "sg-bbbbbbbbbbbbbbbbb",
        },
        "us-east-1",
    )

    assert resources.subnet_id == "subnet-aaaaaaaaaaaaaaaaa"
    assert resources.security_group_id == "sg-bbbbbbbbbbbbbbbbb"
    assert resources.ami_id is None
    assert resources.ami_distribution == "official_public"


def test_annotation_resources_reject_cross_region_fallback_and_unknown_region():
    legacy_only = {
        "AWS_SUBNET_ID": "subnet-aaaaaaaaaaaaaaaaa",
        "AWS_SECURITY_GROUP_ID": "sg-bbbbbbbbbbbbbbbbb",
    }
    with pytest.raises(ValueError, match="AWS_AP_EAST_1_SUBNET_ID"):
        resolve_annotation_aws_resources(legacy_only, "ap-east-1")
    with pytest.raises(ValueError, match="Unsupported"):
        resolve_annotation_aws_resources({}, "eu-west-1")


def test_configure_aws_injects_hong_kong_resources(monkeypatch):
    class FakeEc2:
        def describe_images(self, **_kwargs):
            return {"Images": [{"State": "available"}]}

    class FakeSession:
        def client(self, name):
            if name == "sts":
                return SimpleNamespace(get_caller_identity=lambda: {"Account": "test"})
            assert name == "ec2"
            return FakeEc2()

    fake_boto3 = SimpleNamespace(Session=lambda **_kwargs: FakeSession())
    monkeypatch.setitem(sys.modules, "boto3", fake_boto3)
    monkeypatch.setenv("AWS_AP_EAST_1_SUBNET_ID", "subnet-11111111111111111")
    monkeypatch.setenv("AWS_AP_EAST_1_SECURITY_GROUP_ID", "sg-22222222222222222")
    monkeypatch.setenv("AWS_AP_EAST_1_AMI_ID", "ami-33333333333333333")
    monkeypatch.setattr(
        "scripts.python.record_reference_task.active_project_instance_ids",
        lambda _client, _project: [],
    )
    monkeypatch.setattr(
        "scripts.python.record_reference_task.discover_public_ipv4",
        lambda: "203.0.113.7",
    )
    monkeypatch.setattr(
        "scripts.python.record_reference_task.refresh_annotation_ingress",
        lambda _client, group_id, public_ip: {
            "security_group_id": group_id,
            "cidr": f"{public_ip}/32",
            "ports": [5000, 5910],
        },
    )

    result = _configure_aws(
        SimpleNamespace(
            aws_profile="osworld-dev",
            aws_region="ap-east-1",
            aws_connection_mode="public",
            no_refresh_security_group=False,
        )
    )

    assert result["ami_id"] == "ami-33333333333333333"
    assert result["ami_distribution"] == "private_encrypted_copy"
    assert result["network"]["cidr"] == "203.0.113.7/32"
    assert result["security_group_id"] == "sg-22222222222222222"


def test_configure_aws_defaults_hong_kong_to_ssm_without_ingress(monkeypatch):
    class FakeEc2:
        def describe_images(self, **_kwargs):
            return {"Images": [{"State": "available"}]}

    class FakeSession:
        def client(self, name):
            if name == "sts":
                return SimpleNamespace(get_caller_identity=lambda: {"Account": "test"})
            return FakeEc2()

    monkeypatch.setitem(
        sys.modules,
        "boto3",
        SimpleNamespace(Session=lambda **_kwargs: FakeSession()),
    )
    monkeypatch.setenv("AWS_AP_EAST_1_SUBNET_ID", "subnet-11111111111111111")
    monkeypatch.setenv(
        "AWS_AP_EAST_1_SECURITY_GROUP_ID", "sg-22222222222222222"
    )
    monkeypatch.setenv("AWS_AP_EAST_1_AMI_ID", "ami-33333333333333333")
    monkeypatch.setattr(
        "scripts.python.record_reference_task.active_project_instance_ids",
        lambda _client, _project: [],
    )
    monkeypatch.setattr(
        "scripts.python.record_reference_task.discover_public_ipv4",
        lambda: pytest.fail("SSM mode must not query the public IP"),
    )

    result = _configure_aws(
        SimpleNamespace(
            aws_profile="osworld-dev",
            aws_region="ap-east-1",
            aws_connection_mode="auto",
            no_refresh_security_group=False,
        )
    )

    assert result["connection_mode"] == "ssm"
    assert result["network"]["reason"] == "ssm_tunnel_does_not_require_public_ingress"


def test_retarget_env_replaces_controllers_with_local_api():
    env = SimpleNamespace(
        vm_ip="203.0.113.9",
        server_port=5000,
        cache_dir_base="cache",
    )

    _retarget_env_to_local_api(env, 15432)

    assert env.vm_ip == "127.0.0.1"
    assert env.server_port == 15432
    assert env.controller.http_server == "http://127.0.0.1:15432"
    assert env.setup_controller.http_server == "http://127.0.0.1:15432"


def test_runtime_loader_rejects_evaluator_and_resolves_artifact(tmp_path):
    artifact = tmp_path / "initial.xlsx"
    artifact.write_bytes(b"xlsx")
    config = {
        "id": "reference-task-r01-001",
        "snapshot": "libreoffice_calc",
        "config": [
            {
                "type": "upload_file",
                "parameters": {
                    "files": [
                        {
                            "local_path": str(artifact),
                            "path": "/home/user/Desktop/initial.xlsx",
                        }
                    ]
                },
            },
            {
                "type": "open",
                "parameters": {"path": "/home/user/Desktop/initial.xlsx"},
            },
        ],
    }
    path = tmp_path / "task.json"
    path.write_text(json.dumps(config), encoding="utf-8")

    loaded = _load_task_config(path)
    assert loaded["config"][0]["parameters"]["files"][0]["local_path"] == str(artifact)

    config["evaluator"] = {}
    path.write_text(json.dumps(config), encoding="utf-8")
    with pytest.raises(ValueError, match="must not contain an evaluator"):
        _load_task_config(path)


def test_final_workbook_is_saved_then_downloaded(tmp_path):
    controller = SimpleNamespace()
    controller.execute_python_command = lambda _command: {"output": "ok"}
    controller.get_file = (
        lambda path: b"PK-final-xlsx" if path.endswith(".xlsx") else None
    )
    env = SimpleNamespace(controller=controller)
    output = tmp_path / "final_artifact.xlsx"

    _save_guest_workbook(env, "/home/user/Desktop/task.xlsx", output)

    assert output.read_bytes() == b"PK-final-xlsx"


def test_key_overlay_requires_input_events():
    valid = SimpleNamespace(
        sample_interval=1.0,
        no_input_events=False,
        no_key_overlay=False,
    )
    _validate_recording_options(valid)

    invalid = SimpleNamespace(
        sample_interval=1.0,
        no_input_events=True,
        no_key_overlay=False,
    )
    with pytest.raises(SystemExit, match="requires --no-key-overlay"):
        _validate_recording_options(invalid)

    debug = SimpleNamespace(
        sample_interval=1.0,
        no_input_events=True,
        no_key_overlay=True,
    )
    _validate_recording_options(debug)
