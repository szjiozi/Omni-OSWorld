import json
import re
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from pathlib import Path
from types import SimpleNamespace

import pytest

from benchmark_construction.annotation_portal.auth import (
    CognitoIdentityProvider,
    LoginSuccess,
    PasswordChangeRequired,
    PortalSessionManager,
    PasswordChallengeManager,
    StaticIdentityProvider,
)
from benchmark_construction.annotation_portal.catalog import AnnotationTask, TaskCatalog
from benchmark_construction.annotation_portal.app import PortalWebConfig, create_app
from benchmark_construction.annotation_portal.models import (
    TaskAssignment,
    UserIdentity,
    UserRole,
    WorkspaceSession,
    WorkspaceStatus,
)
from benchmark_construction.annotation_portal.storage import S3BundlePublisher
from benchmark_construction.annotation_portal.service import (
    AnnotationPortalService,
    FakeWorkspaceController,
    InlineExecutor,
    WorkspaceJanitor,
)
from benchmark_construction.annotation_portal.store import (
    ConcurrencyLimitError,
    DynamoPortalStore,
    InvalidTransitionError,
    MemoryPortalStore,
    PortalStoreError,
    SessionConflictError,
)


def _workspace(session_id: str, task_id: str, username: str) -> WorkspaceSession:
    return WorkspaceSession(
        session_id=session_id,
        task_id=task_id,
        username=username,
        region="ap-east-1",
    )


def test_memory_store_enforces_user_task_and_global_workspace_locks():
    store = MemoryPortalStore()
    store.create_workspace(_workspace("s1", "t1", "alice"), max_active=2)

    with pytest.raises(SessionConflictError, match="alice"):
        store.create_workspace(_workspace("s2", "t2", "alice"), max_active=2)
    with pytest.raises(SessionConflictError, match="t1"):
        store.create_workspace(_workspace("s3", "t1", "bob"), max_active=2)

    store.create_workspace(_workspace("s4", "t2", "bob"), max_active=2)
    with pytest.raises(ConcurrencyLimitError, match="2 active"):
        store.create_workspace(_workspace("s5", "t3", "carol"), max_active=2)


def test_terminal_transition_releases_capacity_but_transition_is_conditional():
    store = MemoryPortalStore()
    store.create_workspace(_workspace("s1", "t1", "alice"), max_active=1)
    store.update_workspace(
        "s1",
        expected={WorkspaceStatus.PROVISIONING},
        status=WorkspaceStatus.TERMINATED,
    )
    store.create_workspace(_workspace("s2", "t1", "alice"), max_active=1)

    with pytest.raises(InvalidTransitionError, match="provisioning"):
        store.update_workspace(
            "s2",
            expected={WorkspaceStatus.READY},
            status=WorkspaceStatus.RECORDING,
        )


class _AccessDeniedError(Exception):
    response = {"Error": {"Code": "AccessDeniedException"}}


class _AccessDeniedDynamo:
    exceptions = SimpleNamespace(
        TransactionCanceledException=type("Canceled", (Exception,), {})
    )

    def transact_write_items(self, **_kwargs):
        raise _AccessDeniedError


def test_dynamo_workspace_admission_reports_missing_storage_permission():
    store = DynamoPortalStore(_AccessDeniedDynamo(), table_name="portal-state")

    with pytest.raises(PortalStoreError, match="permission is incomplete"):
        store.create_workspace(_workspace("s1", "t1", "alice"), max_active=4)


def test_assignments_and_opaque_portal_sessions():
    store = MemoryPortalStore()
    store.put_assignment(TaskAssignment(task_id="t2", username="alice"))
    store.put_assignment(TaskAssignment(task_id="t1", username="alice"))
    assert {item.task_id for item in store.assignments_for("alice")} == {"t1", "t2"}

    manager = PortalSessionManager(store, lifetime_seconds=60)
    token = manager.create(UserIdentity("alice", UserRole.ANNOTATOR))
    assert token not in store._portal_sessions
    assert manager.resolve(token) == UserIdentity("alice", UserRole.ANNOTATOR)
    manager.revoke(token)
    assert manager.resolve(token) is None


def test_annotator_can_receive_multiple_tasks():
    first = _catalog().get("task-1")
    second = replace(first, task_id="task-2", instruction="Create another summary.")
    store = MemoryPortalStore()
    store.put_assignment(TaskAssignment("task-1", "alice"))
    store.put_assignment(TaskAssignment("task-2", "alice"))
    service = AnnotationPortalService(
        store=store,
        catalog=TaskCatalog([first, second]),
        controller=FakeWorkspaceController(Path("/tmp/unused-portal-test")),
        task_config_dir=Path("/tmp/unused-portal-test"),
        region="local",
        executor=InlineExecutor(),
    )

    assert [task["task_id"] for task in service.tasks_for(UserIdentity("alice"))] == [
        "task-1",
        "task-2",
    ]


def test_task_review_is_validated_persisted_and_bound_to_catalog_version(tmp_path):
    service, _controller, store = _service(tmp_path)
    identity = UserIdentity("alice")
    store.put_assignment(TaskAssignment("task-1", "alice"))

    saved = service.save_task_review(
        identity,
        "task-1",
        decision="approved",
        reason_codes=[],
        revision_instructions=[],
        notes="The task is natural and all required skills are observable.",
    )

    assert saved["reviewer"] == "alice"
    assert service.task_review_for(identity, "task-1") == saved
    assert service.tasks_for(identity)[0]["portal_review"] == saved
    with pytest.raises(ValueError, match="revision_instructions"):
        service.save_task_review(
            identity,
            "task-1",
            decision="revision_requested",
            reason_codes=["artifact_too_complex"],
            revision_instructions=[],
            notes="Simplify the artifact.",
        )

    task = _catalog().get("task-1")
    service.catalog = TaskCatalog([replace(task, catalog_version="new-version")])
    assert service.task_review_for(identity, "task-1")["decision"] == ""


class _FakeCognitoPasswordError(Exception):
    response = {"Error": {"Code": "InvalidPasswordException"}}


class _FakeCognito:
    def __init__(self, challenge: bool = False, reject_weak_password: bool = False):
        self.challenge = challenge
        self.reject_weak_password = reject_weak_password
        self.calls = []

    def initiate_auth(self, **kwargs):
        self.calls.append(("initiate_auth", kwargs))
        if self.challenge:
            return {"ChallengeName": "NEW_PASSWORD_REQUIRED", "Session": "challenge"}
        return {"AuthenticationResult": {"AccessToken": "access"}}

    def respond_to_auth_challenge(self, **kwargs):
        self.calls.append(("respond_to_auth_challenge", kwargs))
        if (
            self.reject_weak_password
            and kwargs["ChallengeResponses"]["NEW_PASSWORD"] == "weak"
        ):
            raise _FakeCognitoPasswordError()
        return {"AuthenticationResult": {"AccessToken": "access"}}

    def get_user(self, **kwargs):
        self.calls.append(("get_user", kwargs))
        return {"Username": "alice"}


def test_cognito_provider_supports_temporary_password_challenge():
    client = _FakeCognito(challenge=True)
    provider = CognitoIdentityProvider(client, client_id="client")

    result = provider.login("alice", "temporary-password")
    assert result == PasswordChangeRequired("alice", "challenge")
    completed = provider.complete_new_password("alice", "new-password", "challenge")
    assert completed == LoginSuccess(UserIdentity("alice", UserRole.ANNOTATOR))


def test_fastapi_password_policy_failure_keeps_challenge_retriable(tmp_path):
    fastapi_testclient = pytest.importorskip("fastapi.testclient")
    service, _controller, store = _service(tmp_path)
    provider = CognitoIdentityProvider(
        _FakeCognito(challenge=True, reject_weak_password=True),
        client_id="client",
    )
    app = create_app(
        config=PortalWebConfig(
            static_dir=Path(__file__).parents[1]
            / "benchmark_construction/annotation_portal/static",
            cookie_secure=False,
        ),
        identity_provider=provider,
        session_manager=PortalSessionManager(store),
        challenge_manager=PasswordChallengeManager(),
        service=service,
    )

    with fastapi_testclient.TestClient(app) as client:
        login = client.post(
            "/api/auth/login",
            json={"username": "alice", "password": "temporary-password"},
        ).json()
        payload = {
            "username": "alice",
            "challenge_id": login["challenge_id"],
            "new_password": "weak",
        }
        rejected = client.post("/api/auth/new-password", json=payload)

        assert rejected.status_code == 400
        assert "at least 12 characters" in rejected.json()["detail"]

        payload["new_password"] = "StrongPassword1!"
        accepted = client.post("/api/auth/new-password", json=payload)
        assert accepted.status_code == 200
        assert accepted.json()["status"] == "authenticated"
        assert accepted.cookies.get("osworld_annotation_session")


class _FakeS3:
    def __init__(self, corrupt_metadata: bool = False):
        self.objects = {}
        self.corrupt_metadata = corrupt_metadata
        self.tags = {}
        self.deleted = []

    def upload_file(self, filename, bucket, key, ExtraArgs):
        self.objects[(bucket, key)] = {
            "Body": open(filename, "rb").read(),
            **ExtraArgs,
        }

    def head_object(self, *, Bucket, Key):
        metadata = self.objects[(Bucket, Key)]["Metadata"]
        return {"Metadata": {"sha256": "bad"} if self.corrupt_metadata else metadata}

    def put_object(self, **kwargs):
        self.objects[(kwargs["Bucket"], kwargs["Key"])] = kwargs

    def generate_presigned_url(self, operation, Params, ExpiresIn):
        assert operation == "get_object"
        return f"https://private.example/{Params['Key']}?expires={ExpiresIn}"

    def get_object(self, **kwargs):
        raw = self.objects[(kwargs["Bucket"], kwargs["Key"])]["Body"]
        start = 0
        end = len(raw) - 1
        content_range = None
        if kwargs.get("Range"):
            match = re.fullmatch(r"bytes=(\d*)-(\d*)", kwargs["Range"])
            assert match
            if match.group(1):
                start = int(match.group(1))
            if match.group(2):
                end = int(match.group(2))
            content_range = f"bytes {start}-{end}/{len(raw)}"
        return {
            "Body": _FakeStreamingBody(raw[start : end + 1]),
            "ContentLength": end - start + 1,
            "ContentType": "binary/octet-stream",
            "ContentRange": content_range,
            "ETag": '"video-etag"',
        }

    def list_objects_v2(self, **kwargs):
        rows = [
            {"Key": key}
            for (bucket, key) in self.objects
            if bucket == kwargs["Bucket"] and key.startswith(kwargs["Prefix"])
        ]
        return {"Contents": rows, "IsTruncated": False}

    def put_object_tagging(self, **kwargs):
        self.tags[(kwargs["Bucket"], kwargs["Key"])] = kwargs["Tagging"]["TagSet"]

    def list_object_versions(self, **kwargs):
        return {
            "Versions": [
                {"Key": key, "VersionId": "v1"}
                for (bucket, key) in self.objects
                if bucket == kwargs["Bucket"] and key.startswith(kwargs["Prefix"])
            ],
            "IsTruncated": False,
        }

    def delete_objects(self, **kwargs):
        self.deleted.extend(kwargs["Delete"]["Objects"])


class _FakeStreamingBody:
    def __init__(self, value):
        self.value = value
        self.closed = False

    def iter_chunks(self, chunk_size):
        for start in range(0, len(self.value), chunk_size):
            yield self.value[start : start + chunk_size]

    def close(self):
        self.closed = True


def test_s3_publisher_writes_complete_marker_last(tmp_path):
    (tmp_path / "recording.mp4").write_bytes(b"video")
    (tmp_path / "manifest.json").write_text("{}", encoding="utf-8")
    s3 = _FakeS3()

    published = S3BundlePublisher(
        s3, bucket="private-bucket", root_prefix="annotations"
    ).publish(tmp_path, username="alice", task_id="task-1", run_id="run-1")

    assert published.complete_key.endswith("/COMPLETE.json")
    complete = json.loads(s3.objects[("private-bucket", published.complete_key)]["Body"])
    assert {item["path"] for item in complete["files"]} == {
        "manifest.json",
        "recording.mp4",
    }
    assert list(s3.objects)[-1][1].endswith("COMPLETE.json")
    assert s3.objects[("private-bucket", f"{published.prefix}/recording.mp4")][
        "ContentType"
    ] == "video/mp4"


def test_s3_publisher_does_not_mark_corrupt_upload_complete(tmp_path):
    (tmp_path / "recording.mp4").write_bytes(b"video")
    s3 = _FakeS3(corrupt_metadata=True)

    with pytest.raises(RuntimeError, match="verification failed"):
        S3BundlePublisher(s3, bucket="bucket", root_prefix="annotations").publish(
            tmp_path, username="alice", task_id="task-1", run_id="run-1"
        )

    assert all(not key.endswith("COMPLETE.json") for _, key in s3.objects)


def _catalog() -> TaskCatalog:
    return TaskCatalog(
        [
            AnnotationTask(
                task_id="task-1",
                app="libreoffice_calc",
                instruction="Create a summary.",
                operator_guide={"recording_start_state": "Workbook is open."},
                skills=(
                    {
                        "skill_id": "skill-1",
                        "name": "Fill a formula",
                        "procedure": ["Enter the formula.", "Autofill the range."],
                        "efficiency_tip": "Use the fill handle.",
                    },
                ),
                review_decision="approved",
            )
        ]
    )


def _service(tmp_path, store=None, publisher=None):
    store = store or MemoryPortalStore()
    config_dir = tmp_path / "configs"
    config_dir.mkdir()
    (config_dir / "task-1.json").write_text("{}", encoding="utf-8")
    controller = FakeWorkspaceController(tmp_path / "outputs")
    service = AnnotationPortalService(
        store=store,
        catalog=_catalog(),
        controller=controller,
        task_config_dir=config_dir,
        region="ap-east-1",
        executor=InlineExecutor(),
        publisher=publisher,
    )
    return service, controller, store


def test_service_runs_prepare_record_finalize_state_machine(tmp_path):
    service, controller, store = _service(tmp_path)
    identity = UserIdentity("alice")
    store.put_assignment(TaskAssignment("task-1", "alice"))

    workspace = service.launch(identity, "task-1")
    assert workspace.status == WorkspaceStatus.READY
    workspace = service.start_recording(identity, workspace.session_id)
    assert workspace.status == WorkspaceStatus.RECORDING
    workspace = service.stop_recording(identity, workspace.session_id)
    assert workspace.status == WorkspaceStatus.SUBMITTED
    assert [name for name, _ in controller.calls] == [
        "prepare",
        "start",
        "stop",
        "terminate",
    ]


def test_service_can_close_ready_workspace_without_submission_and_relaunch(tmp_path):
    service, controller, store = _service(tmp_path)
    identity = UserIdentity("alice")
    store.put_assignment(TaskAssignment("task-1", "alice"))

    first = service.launch(identity, "task-1")
    closed = service.terminate_ready_workspace(identity, first.session_id)

    assert closed.status == WorkspaceStatus.TERMINATED
    assert closed.progress_stage == "terminated"
    assert service.current_workspace(identity) is None
    assert controller.calls[-1] == ("terminate", first.session_id)

    second = service.launch(identity, "task-1")
    assert second.status == WorkspaceStatus.READY
    assert second.session_id != first.session_id


def test_service_refuses_close_without_submission_after_recording_starts(tmp_path):
    service, controller, store = _service(tmp_path)
    identity = UserIdentity("alice")
    store.put_assignment(TaskAssignment("task-1", "alice"))
    workspace = service.launch(identity, "task-1")
    workspace = service.start_recording(identity, workspace.session_id)

    with pytest.raises(RuntimeError, match="Only a ready workspace"):
        service.terminate_ready_workspace(identity, workspace.session_id)

    assert store.get_workspace(workspace.session_id).status == WorkspaceStatus.RECORDING
    assert controller.calls[-1] == ("start", workspace.session_id)


def test_fastapi_login_assignment_and_annotation_flow(tmp_path):
    fastapi_testclient = pytest.importorskip("fastapi.testclient")
    service, _controller, store = _service(tmp_path)
    store.put_assignment(TaskAssignment("task-1", "alice"))
    sessions = PortalSessionManager(store)
    app = create_app(
        config=PortalWebConfig(
            static_dir=Path(__file__).parents[1]
            / "benchmark_construction/annotation_portal/static",
            cookie_secure=False,
        ),
        identity_provider=StaticIdentityProvider(
            {"alice": "test-password"}, admin_usernames=frozenset()
        ),
        session_manager=sessions,
        challenge_manager=PasswordChallengeManager(),
        service=service,
    )

    with fastapi_testclient.TestClient(app) as client:
        assert client.get("/api/tasks").status_code == 401
        response = client.post(
            "/api/auth/login",
            json={"username": "alice", "password": "test-password"},
        )
        assert response.status_code == 200
        assert response.cookies.get("osworld_annotation_session")
        tasks = client.get("/api/tasks").json()
        assert [task["task_id"] for task in tasks] == ["task-1"]

        workspace = client.post("/api/tasks/task-1/launch").json()
        assert workspace["status"] == "ready"
        started = client.post(
            f"/api/workspaces/{workspace['session_id']}/recording/start"
        ).json()
        assert started["status"] == "recording"
        submitted = client.post(
            f"/api/workspaces/{workspace['session_id']}/recording/stop"
        ).json()
        assert submitted["status"] == "submitted"
        selected = client.put(
            f"/api/submissions/{workspace['session_id']}/final"
        )
        assert selected.status_code == 200
        assert selected.json()["status"] == "selected"
        assert client.get("/api/submissions").json()[0]["is_final"] is True


def test_fastapi_ready_workspace_can_be_closed_without_submission(tmp_path):
    fastapi_testclient = pytest.importorskip("fastapi.testclient")
    service, _controller, store = _service(tmp_path)
    store.put_assignment(TaskAssignment("task-1", "alice"))
    app = create_app(
        config=PortalWebConfig(
            static_dir=Path(__file__).parents[1]
            / "benchmark_construction/annotation_portal/static",
            cookie_secure=False,
        ),
        identity_provider=StaticIdentityProvider(
            {"alice": "test-password"}, admin_usernames=frozenset()
        ),
        session_manager=PortalSessionManager(store),
        challenge_manager=PasswordChallengeManager(),
        service=service,
    )

    with fastapi_testclient.TestClient(app) as client:
        client.post(
            "/api/auth/login",
            json={"username": "alice", "password": "test-password"},
        )
        workspace = client.post("/api/tasks/task-1/launch").json()
        closed = client.post(
            f"/api/workspaces/{workspace['session_id']}/terminate"
        )

        assert closed.status_code == 200
        assert closed.json()["status"] == "terminated"
        assert client.get("/api/workspaces/current").json() is None


def test_fastapi_review_json_round_trip_and_download(tmp_path):
    fastapi_testclient = pytest.importorskip("fastapi.testclient")
    service, _controller, store = _service(tmp_path)
    store.put_assignment(TaskAssignment("task-1", "alice"))
    app = create_app(
        config=PortalWebConfig(
            static_dir=Path(__file__).parents[1]
            / "benchmark_construction/annotation_portal/static",
            cookie_secure=False,
        ),
        identity_provider=StaticIdentityProvider(
            {"alice": "test-password"}, admin_usernames=frozenset()
        ),
        session_manager=PortalSessionManager(store),
        challenge_manager=PasswordChallengeManager(),
        service=service,
    )

    with fastapi_testclient.TestClient(app) as client:
        client.post(
            "/api/auth/login",
            json={"username": "alice", "password": "test-password"},
        )
        response = client.put(
            "/api/tasks/task-1/review.json",
            json={
                "decision": "rejected",
                "reason_codes": ["unnatural_combination"],
                "revision_instructions": [],
                "notes": "The required skills do not form one natural task.",
            },
        )
        assert response.status_code == 200
        assert response.json()["reviewer"] == "alice"

        download = client.get("/api/tasks/task-1/review.json?download=true")
        assert download.json() == response.json()
        assert download.headers["content-disposition"] == 'attachment; filename="review.json"'


def test_fastapi_streams_private_recording_through_same_origin_with_range(tmp_path):
    fastapi_testclient = pytest.importorskip("fastapi.testclient")
    s3 = _FakeS3()
    publisher = S3BundlePublisher(s3, bucket="private-bucket", root_prefix="annotations")
    service, _controller, store = _service(tmp_path, publisher=publisher)
    store.put_assignment(TaskAssignment("task-1", "alice"))
    app = create_app(
        config=PortalWebConfig(
            static_dir=Path(__file__).parents[1]
            / "benchmark_construction/annotation_portal/static",
            cookie_secure=False,
        ),
        identity_provider=StaticIdentityProvider(
            {"alice": "test-password"}, admin_usernames=frozenset()
        ),
        session_manager=PortalSessionManager(store),
        challenge_manager=PasswordChallengeManager(),
        service=service,
    )

    with fastapi_testclient.TestClient(app) as client:
        client.post(
            "/api/auth/login",
            json={"username": "alice", "password": "test-password"},
        )
        workspace = client.post("/api/tasks/task-1/launch").json()
        client.post(f"/api/workspaces/{workspace['session_id']}/recording/start")
        client.post(f"/api/workspaces/{workspace['session_id']}/recording/stop")
        response = client.get(
            f"/api/submissions/{workspace['session_id']}/video",
            headers={"Range": "bytes=0-4"},
        )

        assert response.status_code == 206
        assert response.content == b"local"
        assert response.headers["accept-ranges"] == "bytes"
        assert response.headers["content-range"] == "bytes 0-4/17"
        assert response.headers["content-type"].startswith("video/mp4")


def test_real_catalog_hides_pending_without_explicit_smoke_flag():
    pilot = Path(__file__).parents[1] / "evaluation_examples/expert_skill_learning/pilot"
    production = TaskCatalog.load(
        packages_path=pilot / "reference_packages.json",
        skills_path=pilot / "skill_pool.json",
        reviews_path=pilot / "reference_package_reviews.json",
    )
    smoke = TaskCatalog.load(
        packages_path=pilot / "reference_packages.json",
        skills_path=pilot / "skill_pool.json",
        reviews_path=pilot / "reference_package_reviews.json",
        allow_pending=True,
    )

    assert production.all() == []
    assert len(smoke.all()) == 4


def test_real_catalog_renders_task_markdown_and_scopes_relative_assets():
    pilot = Path(__file__).parents[1] / "evaluation_examples/expert_skill_learning/pilot"
    task = TaskCatalog.load(
        packages_path=pilot / "reference_packages.json",
        skills_path=pilot / "skill_pool.json",
        reviews_path=pilot / "reference_package_reviews.json",
        allow_pending=True,
    ).get("reference-task-r01-001")

    assert "<h1>Workshop Enrollment Queue</h1>" in task.task_markdown_html
    assert (
        '/api/tasks/reference-task-r01-001/files/artifact/previews/Enrollment_Log.png'
        in task.task_markdown_html
    )
    assert 'href="#"' in task.task_markdown_html
    assert "../../../reviewer.md" not in task.task_markdown_html
    assert "<table>" in task.task_markdown_html
    assert (
        "/api/tasks/reference-task-r01-001/review.json?download=true"
        in task.task_markdown_html
    )


def test_task_packet_file_access_prevents_directory_traversal(tmp_path):
    packet = tmp_path / "packet"
    packet.mkdir()
    (packet / "preview.png").write_bytes(b"png")
    outside = tmp_path / "outside.txt"
    outside.write_text("private", encoding="utf-8")
    task = replace(_catalog().get("task-1"), packet_dir=packet)
    service, _controller, store = _service(tmp_path, publisher=None)
    service.catalog = TaskCatalog([task])
    store.put_assignment(TaskAssignment("task-1", "alice"))

    assert service.task_file(UserIdentity("alice"), "task-1", "preview.png").is_file()
    with pytest.raises(FileNotFoundError):
        service.task_file(UserIdentity("alice"), "task-1", "../outside.txt")
    with pytest.raises(PermissionError):
        service.task_file(UserIdentity("bob"), "task-1", "preview.png")


def test_submission_preview_discard_restore_and_retention_purge(tmp_path):
    s3 = _FakeS3()
    publisher = S3BundlePublisher(s3, bucket="private-bucket", root_prefix="annotations")
    service, _controller, store = _service(tmp_path, publisher=publisher)
    identity = UserIdentity("alice")
    store.put_assignment(TaskAssignment("task-1", "alice"))
    workspace = service.launch(identity, "task-1")
    workspace = service.start_recording(identity, workspace.session_id)
    workspace = service.stop_recording(identity, workspace.session_id)

    assert workspace.status == WorkspaceStatus.SUBMITTED
    stream = service.recording_stream(
        identity,
        workspace.session_id,
        byte_range="bytes=0-4",
    )
    assert stream.status_code == 206
    assert stream.content_range == "bytes 0-4/17"
    assert b"".join(stream.body.iter_chunks(1024)) == b"local"
    assert [item["session_id"] for item in service.submissions_for(identity)] == [
        workspace.session_id
    ]
    with pytest.raises(PermissionError):
        service.recording_stream(UserIdentity("bob"), workspace.session_id)
    with pytest.raises(ValueError, match="Invalid video byte range"):
        service.recording_stream(
            identity,
            workspace.session_id,
            byte_range="bytes=not-a-range",
        )

    discarded = service.discard_submission(identity, workspace.session_id)
    assert discarded.status == WorkspaceStatus.DISCARDED
    assert all(
        tags == [{"Key": "AnnotationStatus", "Value": "discarded"}]
        for tags in s3.tags.values()
    )
    restored = service.restore_submission(identity, workspace.session_id)
    assert restored.status == WorkspaceStatus.SUBMITTED

    discarded = service.discard_submission(identity, workspace.session_id)
    old = (datetime.now(UTC) - timedelta(days=8)).isoformat()
    store._workspaces[workspace.session_id] = replace(discarded, discarded_at=old)
    assert service.purge_discarded() == [workspace.session_id]
    assert store.get_workspace(workspace.session_id).status == WorkspaceStatus.DELETED
    assert s3.deleted


def test_final_submission_selection_replaces_per_task_and_clears_on_discard(tmp_path):
    s3 = _FakeS3()
    publisher = S3BundlePublisher(s3, bucket="private-bucket", root_prefix="annotations")
    service, _controller, store = _service(tmp_path, publisher=publisher)
    identity = UserIdentity("alice")
    store.put_assignment(TaskAssignment("task-1", "alice"))

    runs = []
    for _ in range(2):
        workspace = service.launch(identity, "task-1")
        service.start_recording(identity, workspace.session_id)
        runs.append(service.stop_recording(identity, workspace.session_id))

    service.select_final_submission(identity, runs[0].session_id)
    first_state = {item["session_id"]: item["is_final"] for item in service.submissions_for(identity)}
    assert first_state == {runs[0].session_id: True, runs[1].session_id: False}

    service.select_final_submission(identity, runs[1].session_id)
    second_state = {item["session_id"]: item["is_final"] for item in service.submissions_for(identity)}
    assert second_state == {runs[0].session_id: False, runs[1].session_id: True}
    with pytest.raises(PermissionError):
        service.select_final_submission(UserIdentity("bob"), runs[1].session_id)

    service.discard_submission(identity, runs[1].session_id)
    assert not any(item["is_final"] for item in service.submissions_for(identity))
    with pytest.raises(RuntimeError, match="active submitted video"):
        service.select_final_submission(identity, runs[1].session_id)


def test_portal_uses_absolute_novnc_websocket_path():
    script = (
        Path(__file__).parents[1]
        / "benchmark_construction/annotation_portal/static/assets/app.js"
    ).read_text(encoding="utf-8")

    assert (
        "const vncPath = `/api/workspaces/${workspace.session_id}/vnc/websockify`;"
        in script
    )
    assert "const vncPath = `api/workspaces/" not in script


def test_portal_refreshes_dashboard_after_successful_submission():
    script = (
        Path(__file__).parents[1]
        / "benchmark_construction/annotation_portal/static/assets/app.js"
    ).read_text(encoding="utf-8")

    assert 'if (workspace.status === "submitted")' in script
    assert "Submission complete." in script
    assert "await refresh();" in script
    assert "Task instructions (TASK.md)" in script
    assert "Quick operator guide and required skills" not in script
    assert "task.instruction" not in script
    assert "Preparing your submission" in script
    assert "Discard this run" in script


def test_portal_exposes_fullscreen_close_and_failed_workspace_retry_controls():
    script = (
        Path(__file__).parents[1]
        / "benchmark_construction/annotation_portal/static/assets/app.js"
    ).read_text(encoding="utf-8")
    styles = (
        Path(__file__).parents[1]
        / "benchmark_construction/annotation_portal/static/assets/app.css"
    ).read_text(encoding="utf-8")

    assert "shell.requestFullscreen()" in script
    assert "document.exitFullscreen()" in script
    assert "Exit fullscreen" in script
    assert "allowfullscreen" in script
    assert "Close without submitting" in script
    assert "Retry workspace" in script
    assert "/terminate`" in script
    assert ".desktop-shell:fullscreen" in styles
    assert ".desktop-shell:fullscreen .exit-fullscreen" in styles


def test_portal_renders_one_task_page_with_review_form_and_left_right_navigation():
    script = (
        Path(__file__).parents[1]
        / "benchmark_construction/annotation_portal/static/assets/app.js"
    ).read_text(encoding="utf-8")

    assert "state.selectedTaskId" in script
    assert "← Previous task" in script
    assert "Next task →" in script
    assert "Task ${index + 1} of ${tasks.length}" in script
    assert "Save review.json" in script
    assert "/review.json?download=true" in script
    assert 'method: "PUT"' in script
    assert "renderSubmissions(submissions, task.task_id)" in script
    assert "No submissions for this task yet." in script
    assert "Select as final" in script
    assert "/final`" in script


def test_janitor_expires_ready_idle_workspace(tmp_path):
    service, controller, store = _service(tmp_path)
    identity = UserIdentity("alice")
    store.put_assignment(TaskAssignment("task-1", "alice"))
    workspace = service.launch(identity, "task-1")
    old = (datetime.now(UTC) - timedelta(minutes=46)).isoformat()
    store._workspaces[workspace.session_id] = replace(
        workspace, ready_at=old, updated_at=old
    )

    expired = WorkspaceJanitor(service).run_once()

    assert expired == [workspace.session_id]
    assert store.get_workspace(workspace.session_id).status == WorkspaceStatus.EXPIRED
    assert controller.calls[-1] == ("terminate", workspace.session_id)
