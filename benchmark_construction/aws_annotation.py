"""AWS preflight helpers for interactive reference annotation."""

from __future__ import annotations

import ipaddress
import json
import re
import shlex
import shutil
import socket
import subprocess
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

import requests


ANNOTATION_PORTS = (5000, 5910)
INGRESS_DESCRIPTION = "OSWorld reference annotation current IPv4"
SUPPORTED_ANNOTATION_REGIONS = {
    "us-east-1": {
        "source_ami_id": "ami-0d23263edb96951d8",
        "requires_private_ami": False,
    },
    "ap-east-1": {
        "source_ami_id": "ami-0d23263edb96951d8",
        "requires_private_ami": True,
    },
}
_RESOURCE_ID = re.compile(r"^(?:subnet|sg|ami)-[0-9a-f]{8,17}$")


@dataclass(frozen=True)
class AnnotationAwsResources:
    region: str
    subnet_id: str
    security_group_id: str
    ami_id: str | None
    source_ami_id: str

    @property
    def ami_distribution(self) -> str:
        return "private_encrypted_copy" if self.ami_id else "official_public"


@dataclass
class SsmPortForward:
    """One local TCP listener backed by an AWS Session Manager session."""

    process: subprocess.Popen[str]
    local_port: int
    remote_port: int

    def close(self) -> None:
        _stop_process(self.process)


@dataclass
class SsmSshForward:
    """Multiplex API and noVNC through SSH carried by one SSM session."""

    process: subprocess.Popen[str]
    ssm_forward: SsmPortForward
    api_port: int
    novnc_port: int
    key_directory: Any

    def close(self) -> None:
        _stop_process(self.process)
        self.ssm_forward.close()
        self.key_directory.cleanup()


def _stop_process(process: subprocess.Popen[str]) -> None:
    if process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)


def _region_env_prefix(region: str) -> str:
    return region.upper().replace("-", "_")


def _validate_resource_id(name: str, value: str, prefix: str) -> None:
    if not _RESOURCE_ID.fullmatch(value) or not value.startswith(f"{prefix}-"):
        raise ValueError(f"{name} has an unexpected AWS resource ID")


def resolve_annotation_aws_resources(
    environ: Mapping[str, str], region: str
) -> AnnotationAwsResources:
    """Resolve region-scoped resources without leaking another region's defaults."""

    if region not in SUPPORTED_ANNOTATION_REGIONS:
        supported = ", ".join(sorted(SUPPORTED_ANNOTATION_REGIONS))
        raise ValueError(
            f"Unsupported reference annotation AWS region {region!r}; "
            f"supported regions: {supported}"
        )
    config = SUPPORTED_ANNOTATION_REGIONS[region]
    prefix = _region_env_prefix(region)
    subnet_name = f"AWS_{prefix}_SUBNET_ID"
    security_group_name = f"AWS_{prefix}_SECURITY_GROUP_ID"
    subnet_id = environ.get(subnet_name, "").strip()
    security_group_id = environ.get(security_group_name, "").strip()

    # Preserve the original deployment without ever reusing its IDs in Hong Kong.
    if region == "us-east-1":
        subnet_id = subnet_id or environ.get("AWS_SUBNET_ID", "").strip()
        security_group_id = (
            security_group_id or environ.get("AWS_SECURITY_GROUP_ID", "").strip()
        )
    missing = [
        name
        for name, value in (
            (subnet_name, subnet_id),
            (security_group_name, security_group_id),
        )
        if not value
    ]
    if missing:
        raise ValueError(
            "Missing region-specific AWS annotation resources: " + ", ".join(missing)
        )
    _validate_resource_id(subnet_name, subnet_id, "subnet")
    _validate_resource_id(security_group_name, security_group_id, "sg")

    ami_id = None
    if config["requires_private_ami"]:
        ami_name = f"AWS_{prefix}_AMI_ID"
        ami_id = environ.get(ami_name, "").strip()
        if not ami_id:
            raise ValueError(
                f"{ami_name} is required because the public OSWorld AMI for "
                f"{region} is unavailable"
            )
        _validate_resource_id(ami_name, ami_id, "ami")
    return AnnotationAwsResources(
        region=region,
        subnet_id=subnet_id,
        security_group_id=security_group_id,
        ami_id=ami_id,
        source_ami_id=str(config["source_ami_id"]),
    )


def active_project_instance_ids(ec2_client: Any, project: str) -> list[str]:
    if not project.strip():
        raise ValueError("AWS project tag must not be empty")
    response = ec2_client.describe_instances(
        Filters=[
            {"Name": "tag:Project", "Values": [project]},
            {
                "Name": "instance-state-name",
                "Values": ["pending", "running", "stopping", "stopped"],
            },
        ]
    )
    return [
        instance["InstanceId"]
        for reservation in response.get("Reservations", [])
        for instance in reservation.get("Instances", [])
    ]


def discover_public_ipv4() -> str:
    session = requests.Session()
    session.trust_env = False
    response = session.get("https://checkip.amazonaws.com", timeout=10)
    response.raise_for_status()
    address = response.text.strip()
    parsed = ipaddress.ip_address(address)
    if parsed.version != 4:
        raise ValueError("checkip.amazonaws.com did not return an IPv4 address")
    return str(parsed)


def wait_for_osworld_api(
    host: str,
    *,
    port: int = 5000,
    timeout_seconds: float = 300,
    poll_seconds: float = 2,
    session: requests.Session | None = None,
) -> float:
    """Wait until the guest HTTP API is reachable without using host proxies."""

    if timeout_seconds <= 0 or poll_seconds < 0:
        raise ValueError("OSWorld API wait durations are invalid")
    client = session or requests.Session()
    client.trust_env = False
    started = time.monotonic()
    deadline = started + timeout_seconds
    last_error = "no response"
    if not 1 <= port <= 65535:
        raise ValueError("OSWorld API port must be between 1 and 65535")
    url = f"http://{host}:{port}/platform"
    while True:
        try:
            response = client.get(url, timeout=(3, 5))
            if response.status_code == 200:
                return time.monotonic() - started
            last_error = f"HTTP {response.status_code}"
        except requests.RequestException as exc:
            last_error = f"{type(exc).__name__}: {exc}"
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError(
                f"OSWorld API did not become ready at {url}: {last_error}"
            )
        time.sleep(min(poll_seconds, remaining))


def wait_for_novnc_ready(
    host: str,
    port: int,
    *,
    timeout_seconds: float = 60,
    session: requests.Session | None = None,
    connection_factory: Any = socket.create_connection,
) -> float:
    """Require noVNC HTML, WebSocket upgrade, and the guest RFB banner."""

    if not 1 <= port <= 65535:
        raise ValueError("noVNC port must be between 1 and 65535")
    if timeout_seconds <= 0:
        raise ValueError("noVNC timeout must be positive")
    started = time.monotonic()
    client = session or requests.Session()
    client.trust_env = False
    url = f"http://{host}:{port}/vnc.html"
    response = client.get(url, timeout=(5, min(20, timeout_seconds)))
    response.raise_for_status()
    if b"noVNC" not in response.content:
        raise RuntimeError("noVNC HTML did not contain the expected application marker")

    remaining = timeout_seconds - (time.monotonic() - started)
    if remaining <= 0:
        raise TimeoutError("noVNC HTML consumed the entire readiness timeout")
    request = (
        f"GET /websockify HTTP/1.1\r\n"
        f"Host: {host}:{port}\r\n"
        "Connection: Upgrade\r\n"
        "Upgrade: websocket\r\n"
        "Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\n"
        "Sec-WebSocket-Version: 13\r\n\r\n"
    ).encode("ascii")
    with connection_factory((host, port), timeout=min(5, remaining)) as stream:
        stream.settimeout(min(20, remaining))
        stream.sendall(request)
        received = b""
        while b"\r\n\r\n" not in received:
            chunk = stream.recv(4096)
            if not chunk:
                raise RuntimeError("noVNC WebSocket closed before returning headers")
            received += chunk
        headers, payload = received.split(b"\r\n\r\n", 1)
        if not headers.startswith(b"HTTP/1.1 101"):
            status = headers.split(b"\r\n", 1)[0].decode("ascii", "replace")
            raise RuntimeError(f"noVNC WebSocket upgrade failed: {status}")
        while b"RFB " not in payload:
            if time.monotonic() - started >= timeout_seconds:
                raise TimeoutError("noVNC WebSocket did not deliver the RFB banner")
            chunk = stream.recv(4096)
            if not chunk:
                raise RuntimeError("noVNC WebSocket closed before the RFB banner")
            payload += chunk
    return time.monotonic() - started


def wait_for_ssm_online(
    ssm_client: Any,
    instance_id: str,
    *,
    timeout_seconds: float = 180,
    poll_seconds: float = 2,
) -> float:
    """Wait until an EC2 instance is registered and online in Systems Manager."""

    if timeout_seconds <= 0 or poll_seconds < 0:
        raise ValueError("SSM wait durations are invalid")
    started = time.monotonic()
    deadline = started + timeout_seconds
    while True:
        response = ssm_client.describe_instance_information(
            Filters=[{"Key": "InstanceIds", "Values": [instance_id]}]
        )
        instances = response.get("InstanceInformationList", [])
        if any(item.get("PingStatus") == "Online" for item in instances):
            return time.monotonic() - started
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError(f"SSM did not report {instance_id} online")
        time.sleep(min(poll_seconds, remaining))


def _free_local_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        listener.bind(("127.0.0.1", 0))
        return int(listener.getsockname()[1])


def _preferred_local_port(port: int) -> int:
    """Use a stable browser origin when free, otherwise fall back to an ephemeral port."""

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
            listener.bind(("127.0.0.1", port))
        return port
    except OSError:
        return _free_local_port()


def start_ssm_port_forward(
    instance_id: str,
    remote_port: int,
    *,
    profile: str,
    region: str,
    local_port: int | None = None,
    timeout_seconds: float = 30,
    poll_seconds: float = 0.2,
) -> SsmPortForward:
    """Start one AWS-StartPortForwardingSession and wait for its listener."""

    if not 1 <= remote_port <= 65535:
        raise ValueError("Remote tunnel port must be between 1 and 65535")
    if local_port is None:
        local_port = _free_local_port()
    if not 1 <= local_port <= 65535:
        raise ValueError("Local tunnel port must be between 1 and 65535")
    if timeout_seconds <= 0 or poll_seconds < 0:
        raise ValueError("Tunnel wait durations are invalid")
    aws_cli = shutil.which("aws")
    plugin = shutil.which("session-manager-plugin")
    if not aws_cli or not plugin:
        raise RuntimeError(
            "AWS CLI and session-manager-plugin must both be available on PATH"
        )
    parameters = json.dumps(
        {
            "portNumber": [str(remote_port)],
            "localPortNumber": [str(local_port)],
        },
        separators=(",", ":"),
    )
    process = subprocess.Popen(
        [
            aws_cli,
            "ssm",
            "start-session",
            "--profile",
            profile,
            "--region",
            region,
            "--target",
            instance_id,
            "--document-name",
            "AWS-StartPortForwardingSession",
            "--parameters",
            parameters,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    tunnel = SsmPortForward(process, local_port, remote_port)
    deadline = time.monotonic() + timeout_seconds
    try:
        while True:
            if process.poll() is not None:
                output = process.stdout.read().strip() if process.stdout else ""
                detail = output or f"exit status {process.returncode}"
                raise RuntimeError(f"SSM port forward failed: {detail}")
            try:
                with socket.create_connection(
                    ("127.0.0.1", local_port), timeout=0.5
                ):
                    return tunnel
            except OSError:
                pass
            if time.monotonic() >= deadline:
                raise TimeoutError(
                    f"SSM tunnel did not listen on 127.0.0.1:{local_port}"
                )
            time.sleep(poll_seconds)
    except Exception:
        tunnel.close()
        raise


def _wait_for_ssm_command(
    ssm_client: Any,
    command_id: str,
    instance_id: str,
    *,
    timeout_seconds: float = 30,
    poll_seconds: float = 0.5,
) -> None:
    deadline = time.monotonic() + timeout_seconds
    while True:
        result = ssm_client.get_command_invocation(
            CommandId=command_id, InstanceId=instance_id
        )
        status = result.get("Status", "")
        if status == "Success":
            return
        if status in {"Cancelled", "Cancelling", "Failed", "TimedOut"}:
            detail = result.get("StandardErrorContent", "").strip() or status
            raise RuntimeError(f"SSM command failed: {detail}")
        if time.monotonic() >= deadline:
            raise TimeoutError(f"SSM command {command_id} did not complete")
        time.sleep(poll_seconds)


def arm_guest_termination_backstop(
    ssm_client: Any,
    instance_id: str,
    *,
    ttl_minutes: int,
) -> str:
    """Schedule a guest poweroff; EC2 launch config turns poweroff into terminate."""

    if ttl_minutes < 30:
        raise ValueError("Guest termination backstop must be at least 30 minutes")
    command = (
        "systemd-run --unit=osworld-guest-ttl "
        f"--on-active={ttl_minutes}min /usr/bin/systemctl poweroff"
    )
    response = ssm_client.send_command(
        InstanceIds=[instance_id],
        DocumentName="AWS-RunShellScript",
        Parameters={"commands": [command]},
    )
    command_id = response["Command"]["CommandId"]
    _wait_for_ssm_command(ssm_client, command_id, instance_id)
    return command_id


def _wait_for_local_ports(
    process: subprocess.Popen[str],
    ports: Iterable[int],
    *,
    timeout_seconds: float = 30,
    poll_seconds: float = 0.2,
) -> None:
    pending = set(ports)
    deadline = time.monotonic() + timeout_seconds
    while pending:
        if process.poll() is not None:
            output = process.stdout.read().strip() if process.stdout else ""
            detail = output or f"exit status {process.returncode}"
            raise RuntimeError(f"SSH tunnel failed: {detail}")
        for port in tuple(pending):
            try:
                with socket.create_connection(("127.0.0.1", port), timeout=0.5):
                    pending.remove(port)
            except OSError:
                pass
        if not pending:
            return
        if time.monotonic() >= deadline:
            listed = ", ".join(str(port) for port in sorted(pending))
            raise TimeoutError(f"SSH tunnel did not listen on local ports: {listed}")
        time.sleep(poll_seconds)


def start_ssm_ssh_forward(
    ssm_client: Any,
    instance_id: str,
    *,
    profile: str,
    region: str,
    ssh_user: str = "user",
) -> SsmSshForward:
    """Carry multiplexed API/noVNC forwards over one ephemeral SSH connection."""

    if not re.fullmatch(r"[a-z_][a-z0-9_-]*", ssh_user):
        raise ValueError("SSH user has an unexpected format")
    ssh = shutil.which("ssh")
    ssh_keygen = shutil.which("ssh-keygen")
    if not ssh or not ssh_keygen:
        raise RuntimeError("ssh and ssh-keygen must both be available on PATH")
    key_directory = tempfile.TemporaryDirectory(prefix="osworld-ssm-ssh-")
    key_path = Path(key_directory.name) / "id_ed25519"
    ssm_forward = None
    ssh_process = None
    try:
        subprocess.run(
            [
                ssh_keygen,
                "-q",
                "-t",
                "ed25519",
                "-N",
                "",
                "-C",
                "osworld-ephemeral-tunnel",
                "-f",
                str(key_path),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
        )
        public_key = key_path.with_suffix(".pub").read_text(encoding="utf-8").strip()
        quoted_key = shlex.quote(public_key)
        home = f"/home/{ssh_user}"
        command = (
            f"install -d -m 700 -o {ssh_user} -g {ssh_user} {home}/.ssh && "
            f"touch {home}/.ssh/authorized_keys && "
            f"(grep -qxF {quoted_key} {home}/.ssh/authorized_keys || "
            f"printf '%s\\n' {quoted_key} >> {home}/.ssh/authorized_keys) && "
            f"chown {ssh_user}:{ssh_user} {home}/.ssh/authorized_keys && "
            f"chmod 600 {home}/.ssh/authorized_keys"
        )
        response = ssm_client.send_command(
            InstanceIds=[instance_id],
            DocumentName="AWS-RunShellScript",
            Parameters={"commands": [command]},
        )
        command_id = response["Command"]["CommandId"]
        _wait_for_ssm_command(ssm_client, command_id, instance_id)

        ssm_forward = start_ssm_port_forward(
            instance_id,
            22,
            profile=profile,
            region=region,
        )
        api_port = _preferred_local_port(15000)
        novnc_port = _preferred_local_port(15910)
        while novnc_port == api_port:
            novnc_port = _free_local_port()
        ssh_process = subprocess.Popen(
            [
                ssh,
                "-N",
                "-p",
                str(ssm_forward.local_port),
                "-i",
                str(key_path),
                "-L",
                f"{api_port}:127.0.0.1:5000",
                "-L",
                f"{novnc_port}:127.0.0.1:5910",
                "-o",
                "BatchMode=yes",
                "-o",
                "ExitOnForwardFailure=yes",
                "-o",
                "IdentitiesOnly=yes",
                "-o",
                "StrictHostKeyChecking=no",
                "-o",
                "UserKnownHostsFile=/dev/null",
                "-o",
                "ServerAliveInterval=30",
                "-o",
                "ServerAliveCountMax=3",
                f"{ssh_user}@127.0.0.1",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        _wait_for_local_ports(ssh_process, (api_port, novnc_port))
        return SsmSshForward(
            ssh_process,
            ssm_forward,
            api_port,
            novnc_port,
            key_directory,
        )
    except Exception:
        if ssh_process is not None:
            _stop_process(ssh_process)
        if ssm_forward is not None:
            ssm_forward.close()
        key_directory.cleanup()
        raise


def _permission_covers_port(permission: dict[str, Any], port: int) -> bool:
    protocol = str(permission.get("IpProtocol", ""))
    if protocol == "-1":
        return True
    if protocol != "tcp":
        return False
    start = permission.get("FromPort")
    end = permission.get("ToPort")
    return isinstance(start, int) and isinstance(end, int) and start <= port <= end


def refresh_annotation_ingress(
    ec2_client: Any,
    security_group_id: str,
    public_ipv4: str,
    *,
    ports: Iterable[int] = ANNOTATION_PORTS,
) -> dict[str, Any]:
    """Replace public IPv4/IPv6 ingress on annotation ports with one /32."""

    parsed = ipaddress.ip_address(public_ipv4)
    if parsed.version != 4:
        raise ValueError("Annotation ingress requires an IPv4 address")
    cidr = f"{parsed}/32"
    target_ports = tuple(sorted(set(int(port) for port in ports)))
    if not target_ports or any(not 1 <= port <= 65535 for port in target_ports):
        raise ValueError("Annotation ports must be between 1 and 65535")

    response = ec2_client.describe_security_groups(GroupIds=[security_group_id])
    groups = response.get("SecurityGroups", [])
    if len(groups) != 1:
        raise ValueError(f"Security group was not found: {security_group_id}")

    revoked = 0
    current_coverage: set[int] = set()
    for permission in groups[0].get("IpPermissions", []):
        covered = [
            port for port in target_ports if _permission_covers_port(permission, port)
        ]
        if not covered:
            continue
        stale_ipv4 = [
            item
            for item in permission.get("IpRanges", [])
            if item.get("CidrIp") != cidr
        ]
        ipv6 = list(permission.get("Ipv6Ranges", []))
        if stale_ipv4 or ipv6:
            fragment = {
                "IpProtocol": permission["IpProtocol"],
                "IpRanges": stale_ipv4,
                "Ipv6Ranges": ipv6,
            }
            if "FromPort" in permission:
                fragment["FromPort"] = permission["FromPort"]
            if "ToPort" in permission:
                fragment["ToPort"] = permission["ToPort"]
            ec2_client.revoke_security_group_ingress(
                GroupId=security_group_id,
                IpPermissions=[fragment],
            )
            revoked += len(stale_ipv4) + len(ipv6)
        if any(item.get("CidrIp") == cidr for item in permission.get("IpRanges", [])):
            current_coverage.update(covered)

    added = 0
    for port in target_ports:
        if port in current_coverage:
            continue
        ec2_client.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {
                    "IpProtocol": "tcp",
                    "FromPort": port,
                    "ToPort": port,
                    "IpRanges": [{"CidrIp": cidr, "Description": INGRESS_DESCRIPTION}],
                }
            ],
        )
        added += 1
    return {
        "security_group_id": security_group_id,
        "cidr": cidr,
        "ports": list(target_ports),
        "revoked_ranges": revoked,
        "added_rules": added,
    }
