"""State stores with atomic workspace admission rules."""

from __future__ import annotations

import threading
import time
from dataclasses import replace
from typing import Any, Protocol

from .models import (
    ACTIVE_WORKSPACE_STATUSES,
    PortalSession,
    TaskAssignment,
    TaskReviewRecord,
    WorkspaceSession,
    WorkspaceStatus,
    utc_now_iso,
)


class PortalStoreError(RuntimeError):
    pass


class SessionConflictError(PortalStoreError):
    pass


class ConcurrencyLimitError(PortalStoreError):
    pass


class InvalidTransitionError(PortalStoreError):
    pass


class PortalStore(Protocol):
    def put_assignment(self, assignment: TaskAssignment) -> None: ...

    def assignments_for(self, username: str) -> list[TaskAssignment]: ...

    def put_task_review(self, record: TaskReviewRecord) -> None: ...

    def get_task_review(
        self, catalog_version: str, task_id: str
    ) -> TaskReviewRecord | None: ...

    def put_final_submission(
        self, username: str, task_id: str, session_id: str
    ) -> None: ...

    def final_submission_for(self, username: str, task_id: str) -> str | None: ...

    def clear_final_submission(
        self, username: str, task_id: str, session_id: str
    ) -> None: ...

    def put_portal_session(self, session: PortalSession) -> None: ...

    def get_portal_session(self, token_hash: str) -> PortalSession | None: ...

    def delete_portal_session(self, token_hash: str) -> None: ...

    def create_workspace(
        self, workspace: WorkspaceSession, *, max_active: int
    ) -> WorkspaceSession: ...

    def get_workspace(self, session_id: str) -> WorkspaceSession | None: ...

    def active_workspace_for_user(self, username: str) -> WorkspaceSession | None: ...

    def active_workspaces(self) -> list[WorkspaceSession]: ...

    def workspaces_for_user(self, username: str | None = None) -> list[WorkspaceSession]: ...

    def update_workspace(
        self,
        session_id: str,
        *,
        expected: set[WorkspaceStatus],
        status: WorkspaceStatus,
        **changes: object,
    ) -> WorkspaceSession: ...


class MemoryPortalStore:
    """Thread-safe store used by local development and unit tests."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._assignments: dict[tuple[str, str], TaskAssignment] = {}
        self._task_reviews: dict[tuple[str, str], TaskReviewRecord] = {}
        self._final_submissions: dict[tuple[str, str], str] = {}
        self._portal_sessions: dict[str, PortalSession] = {}
        self._workspaces: dict[str, WorkspaceSession] = {}

    def put_assignment(self, assignment: TaskAssignment) -> None:
        with self._lock:
            self._assignments[(assignment.username, assignment.task_id)] = assignment

    def assignments_for(self, username: str) -> list[TaskAssignment]:
        with self._lock:
            return sorted(
                (
                    item
                    for (owner, _), item in self._assignments.items()
                    if owner == username
                ),
                key=lambda item: (item.assigned_at, item.task_id),
            )

    def put_task_review(self, record: TaskReviewRecord) -> None:
        with self._lock:
            self._task_reviews[(record.catalog_version, record.task_id)] = record

    def get_task_review(
        self, catalog_version: str, task_id: str
    ) -> TaskReviewRecord | None:
        with self._lock:
            return self._task_reviews.get((catalog_version, task_id))

    def put_final_submission(
        self, username: str, task_id: str, session_id: str
    ) -> None:
        with self._lock:
            self._final_submissions[(username, task_id)] = session_id

    def final_submission_for(self, username: str, task_id: str) -> str | None:
        with self._lock:
            return self._final_submissions.get((username, task_id))

    def clear_final_submission(
        self, username: str, task_id: str, session_id: str
    ) -> None:
        with self._lock:
            key = (username, task_id)
            if self._final_submissions.get(key) == session_id:
                self._final_submissions.pop(key)

    def put_portal_session(self, session: PortalSession) -> None:
        with self._lock:
            self._portal_sessions[session.token_hash] = session

    def get_portal_session(self, token_hash: str) -> PortalSession | None:
        with self._lock:
            return self._portal_sessions.get(token_hash)

    def delete_portal_session(self, token_hash: str) -> None:
        with self._lock:
            self._portal_sessions.pop(token_hash, None)

    def create_workspace(
        self, workspace: WorkspaceSession, *, max_active: int
    ) -> WorkspaceSession:
        if workspace.status not in ACTIVE_WORKSPACE_STATUSES:
            raise ValueError("A new workspace must start in an active status")
        with self._lock:
            active = [
                item
                for item in self._workspaces.values()
                if item.status in ACTIVE_WORKSPACE_STATUSES
            ]
            if any(item.username == workspace.username for item in active):
                raise SessionConflictError(
                    f"{workspace.username} already has an active workspace"
                )
            if any(item.task_id == workspace.task_id for item in active):
                raise SessionConflictError(
                    f"{workspace.task_id} already has an active workspace"
                )
            if len(active) >= max_active:
                raise ConcurrencyLimitError(
                    f"The portal already has {max_active} active workspaces"
                )
            if workspace.session_id in self._workspaces:
                raise SessionConflictError(
                    f"Workspace {workspace.session_id} already exists"
                )
            self._workspaces[workspace.session_id] = workspace
            return workspace

    def get_workspace(self, session_id: str) -> WorkspaceSession | None:
        with self._lock:
            return self._workspaces.get(session_id)

    def active_workspace_for_user(self, username: str) -> WorkspaceSession | None:
        with self._lock:
            matches = [
                item
                for item in self._workspaces.values()
                if item.username == username
                and item.status in ACTIVE_WORKSPACE_STATUSES
            ]
            return max(matches, key=lambda item: item.created_at) if matches else None

    def active_workspaces(self) -> list[WorkspaceSession]:
        with self._lock:
            return sorted(
                (
                    item
                    for item in self._workspaces.values()
                    if item.status in ACTIVE_WORKSPACE_STATUSES
                ),
                key=lambda item: item.created_at,
            )

    def workspaces_for_user(self, username: str | None = None) -> list[WorkspaceSession]:
        with self._lock:
            return sorted(
                (
                    item
                    for item in self._workspaces.values()
                    if username is None or item.username == username
                ),
                key=lambda item: (item.created_at, item.session_id),
                reverse=True,
            )

    def update_workspace(
        self,
        session_id: str,
        *,
        expected: set[WorkspaceStatus],
        status: WorkspaceStatus,
        **changes: object,
    ) -> WorkspaceSession:
        with self._lock:
            current = self._workspaces.get(session_id)
            if current is None:
                raise KeyError(session_id)
            if current.status not in expected:
                raise InvalidTransitionError(
                    f"Workspace {session_id} is {current.status.value}, expected one of "
                    f"{sorted(item.value for item in expected)}"
                )
            forbidden = {"session_id", "task_id", "username", "created_at", "status"}
            overlap = forbidden.intersection(changes)
            if overlap:
                raise ValueError(f"Immutable workspace fields: {sorted(overlap)}")
            updated = replace(
                current,
                status=status,
                updated_at=utc_now_iso(),
                **changes,
            )
            self._workspaces[session_id] = updated
            return updated


class DynamoPortalStore:
    """Single-table DynamoDB store with transactional admission locks."""

    def __init__(self, client: Any, *, table_name: str) -> None:
        from boto3.dynamodb.types import TypeDeserializer, TypeSerializer

        self.client = client
        self.table_name = table_name
        self._serializer = TypeSerializer()
        self._deserializer = TypeDeserializer()

    def _item(self, value: dict[str, Any]) -> dict[str, dict[str, Any]]:
        return {key: self._serializer.serialize(item) for key, item in value.items()}

    def _values(self, value: dict[str, Any]) -> dict[str, dict[str, Any]]:
        return self._item(value)

    def _decode(self, value: dict[str, dict[str, Any]]) -> dict[str, Any]:
        return {key: self._deserializer.deserialize(item) for key, item in value.items()}

    def put_assignment(self, assignment: TaskAssignment) -> None:
        self.client.put_item(
            TableName=self.table_name,
            Item=self._item(
                {
                    "pk": f"USER#{assignment.username}",
                    "sk": f"ASSIGNMENT#{assignment.task_id}",
                    "entity": "assignment",
                    "username": assignment.username,
                    "task_id": assignment.task_id,
                    "assigned_at": assignment.assigned_at,
                }
            ),
        )

    def assignments_for(self, username: str) -> list[TaskAssignment]:
        response = self.client.query(
            TableName=self.table_name,
            KeyConditionExpression="pk = :pk AND begins_with(sk, :prefix)",
            ExpressionAttributeValues=self._values(
                {":pk": f"USER#{username}", ":prefix": "ASSIGNMENT#"}
            ),
        )
        return sorted(
            (
                TaskAssignment(
                    task_id=item["task_id"],
                    username=item["username"],
                    assigned_at=item["assigned_at"],
                )
                for item in (self._decode(raw) for raw in response.get("Items", []))
            ),
            key=lambda item: (item.assigned_at, item.task_id),
        )

    def put_task_review(self, record: TaskReviewRecord) -> None:
        self.client.put_item(
            TableName=self.table_name,
            Item=self._item(
                {
                    "pk": f"REVIEW#{record.catalog_version}",
                    "sk": f"TASK#{record.task_id}",
                    "entity": "task_review",
                    "catalog_version": record.catalog_version,
                    "task_id": record.task_id,
                    "username": record.username,
                    "review": record.review,
                    "updated_at": record.updated_at,
                }
            ),
        )

    def get_task_review(
        self, catalog_version: str, task_id: str
    ) -> TaskReviewRecord | None:
        response = self.client.get_item(
            TableName=self.table_name,
            Key=self._item(
                {
                    "pk": f"REVIEW#{catalog_version}",
                    "sk": f"TASK#{task_id}",
                }
            ),
            ConsistentRead=True,
        )
        raw = response.get("Item")
        if raw is None:
            return None
        item = self._decode(raw)
        return TaskReviewRecord(
            catalog_version=item["catalog_version"],
            task_id=item["task_id"],
            username=item["username"],
            review=dict(item["review"]),
            updated_at=item["updated_at"],
        )

    def put_final_submission(
        self, username: str, task_id: str, session_id: str
    ) -> None:
        self.client.put_item(
            TableName=self.table_name,
            Item=self._item(
                {
                    "pk": f"USER#{username}",
                    "sk": f"FINAL_SUBMISSION#{task_id}",
                    "entity": "final_submission",
                    "username": username,
                    "task_id": task_id,
                    "session_id": session_id,
                    "updated_at": utc_now_iso(),
                }
            ),
        )

    def final_submission_for(self, username: str, task_id: str) -> str | None:
        response = self.client.get_item(
            TableName=self.table_name,
            Key=self._item(
                {"pk": f"USER#{username}", "sk": f"FINAL_SUBMISSION#{task_id}"}
            ),
            ConsistentRead=True,
        )
        raw = response.get("Item")
        return self._decode(raw)["session_id"] if raw else None

    def clear_final_submission(
        self, username: str, task_id: str, session_id: str
    ) -> None:
        try:
            self.client.delete_item(
                TableName=self.table_name,
                Key=self._item(
                    {
                        "pk": f"USER#{username}",
                        "sk": f"FINAL_SUBMISSION#{task_id}",
                    }
                ),
                ConditionExpression="session_id = :session_id",
                ExpressionAttributeValues=self._values({":session_id": session_id}),
            )
        except Exception as exc:
            if getattr(exc, "response", {}).get("Error", {}).get("Code") == (
                "ConditionalCheckFailedException"
            ):
                return
            raise

    def put_portal_session(self, session: PortalSession) -> None:
        self.client.put_item(
            TableName=self.table_name,
            Item=self._item(
                {
                    "pk": f"LOGIN#{session.token_hash}",
                    "sk": "META",
                    "entity": "login",
                    "token_hash": session.token_hash,
                    "username": session.username,
                    "role": session.role.value,
                    "expires_at_epoch": session.expires_at_epoch,
                    "created_at": session.created_at,
                    "ttl": session.expires_at_epoch,
                }
            ),
        )

    def get_portal_session(self, token_hash: str) -> PortalSession | None:
        response = self.client.get_item(
            TableName=self.table_name,
            Key=self._item({"pk": f"LOGIN#{token_hash}", "sk": "META"}),
            ConsistentRead=True,
        )
        raw = response.get("Item")
        if raw is None:
            return None
        item = self._decode(raw)
        from .models import UserRole

        return PortalSession(
            token_hash=item["token_hash"],
            username=item["username"],
            role=UserRole(item["role"]),
            expires_at_epoch=int(item["expires_at_epoch"]),
            created_at=item["created_at"],
        )

    def delete_portal_session(self, token_hash: str) -> None:
        self.client.delete_item(
            TableName=self.table_name,
            Key=self._item({"pk": f"LOGIN#{token_hash}", "sk": "META"}),
        )

    def create_workspace(
        self, workspace: WorkspaceSession, *, max_active: int
    ) -> WorkspaceSession:
        if workspace.status not in ACTIVE_WORKSPACE_STATUSES:
            raise ValueError("A new workspace must start in an active status")
        item = {
            "pk": f"WORKSPACE#{workspace.session_id}",
            "sk": "META",
            "entity": "workspace",
            **workspace.to_dict(),
        }
        try:
            self.client.transact_write_items(
                TransactItems=[
                    {
                        "Put": {
                            "TableName": self.table_name,
                            "Item": self._item(item),
                            "ConditionExpression": "attribute_not_exists(pk)",
                        }
                    },
                    self._lock_put(
                        f"LOCK#USER#{workspace.username}", workspace.session_id
                    ),
                    self._lock_put(
                        f"LOCK#TASK#{workspace.task_id}", workspace.session_id
                    ),
                    {
                        "Update": {
                            "TableName": self.table_name,
                            "Key": self._item({"pk": "PORTAL", "sk": "ACTIVE_COUNT"}),
                            "UpdateExpression": "ADD active_count :one",
                            "ConditionExpression": (
                                "attribute_not_exists(active_count) OR active_count < :limit"
                            ),
                            "ExpressionAttributeValues": self._values(
                                {":one": 1, ":limit": max_active}
                            ),
                        }
                    },
                    {
                        "ConditionCheck": {
                            "TableName": self.table_name,
                            "Key": self._item(
                                {"pk": "PORTAL", "sk": "MAINTENANCE"}
                            ),
                            "ConditionExpression": (
                                "attribute_not_exists(blocked) OR #ttl < :now"
                            ),
                            "ExpressionAttributeNames": {"#ttl": "ttl"},
                            "ExpressionAttributeValues": self._values(
                                {":now": int(time.time())}
                            ),
                        }
                    },
                ]
            )
        except self.client.exceptions.TransactionCanceledException as exc:
            raise SessionConflictError(
                "Workspace admission failed: user/task is active or capacity is full"
            ) from exc
        except Exception as exc:
            error = getattr(exc, "response", {}).get("Error", {})
            if error.get("Code") == "AccessDeniedException":
                raise PortalStoreError(
                    "Workspace admission storage permission is incomplete; "
                    "contact the portal administrator"
                ) from exc
            raise
        return workspace

    def _lock_put(self, pk: str, session_id: str) -> dict[str, Any]:
        return {
            "Put": {
                "TableName": self.table_name,
                "Item": self._item(
                    {
                        "pk": pk,
                        "sk": "ACTIVE",
                        "entity": "workspace_lock",
                        "session_id": session_id,
                    }
                ),
                "ConditionExpression": "attribute_not_exists(pk)",
            }
        }

    def get_workspace(self, session_id: str) -> WorkspaceSession | None:
        response = self.client.get_item(
            TableName=self.table_name,
            Key=self._item({"pk": f"WORKSPACE#{session_id}", "sk": "META"}),
            ConsistentRead=True,
        )
        raw = response.get("Item")
        if raw is None:
            return None
        item = self._decode(raw)
        return WorkspaceSession.from_dict(
            {key: value for key, value in item.items() if key not in {"pk", "sk", "entity"}}
        )

    def active_workspace_for_user(self, username: str) -> WorkspaceSession | None:
        response = self.client.get_item(
            TableName=self.table_name,
            Key=self._item({"pk": f"LOCK#USER#{username}", "sk": "ACTIVE"}),
            ConsistentRead=True,
        )
        raw = response.get("Item")
        if raw is None:
            return None
        return self.get_workspace(self._decode(raw)["session_id"])

    def active_workspaces(self) -> list[WorkspaceSession]:
        items: list[WorkspaceSession] = []
        scan_kwargs: dict[str, Any] = {
            "TableName": self.table_name,
            "FilterExpression": "entity = :entity",
            "ExpressionAttributeValues": self._values({":entity": "workspace"}),
        }
        while True:
            response = self.client.scan(**scan_kwargs)
            for raw in response.get("Items", []):
                item = self._decode(raw)
                workspace = WorkspaceSession.from_dict(
                    {
                        key: value
                        for key, value in item.items()
                        if key not in {"pk", "sk", "entity"}
                    }
                )
                if workspace.status in ACTIVE_WORKSPACE_STATUSES:
                    items.append(workspace)
            last_key = response.get("LastEvaluatedKey")
            if not last_key:
                break
            scan_kwargs["ExclusiveStartKey"] = last_key
        return sorted(items, key=lambda item: item.created_at)

    def workspaces_for_user(self, username: str | None = None) -> list[WorkspaceSession]:
        items: list[WorkspaceSession] = []
        values = {":entity": "workspace"}
        filter_expression = "entity = :entity"
        if username is not None:
            values[":username"] = username
            filter_expression += " AND username = :username"
        scan_kwargs: dict[str, Any] = {
            "TableName": self.table_name,
            "FilterExpression": filter_expression,
            "ExpressionAttributeValues": self._values(values),
        }
        while True:
            response = self.client.scan(**scan_kwargs)
            for raw in response.get("Items", []):
                item = self._decode(raw)
                items.append(
                    WorkspaceSession.from_dict(
                        {
                            key: value
                            for key, value in item.items()
                            if key not in {"pk", "sk", "entity"}
                        }
                    )
                )
            last_key = response.get("LastEvaluatedKey")
            if not last_key:
                break
            scan_kwargs["ExclusiveStartKey"] = last_key
        return sorted(
            items,
            key=lambda item: (item.created_at, item.session_id),
            reverse=True,
        )

    def update_workspace(
        self,
        session_id: str,
        *,
        expected: set[WorkspaceStatus],
        status: WorkspaceStatus,
        **changes: object,
    ) -> WorkspaceSession:
        current = self.get_workspace(session_id)
        if current is None:
            raise KeyError(session_id)
        if current.status not in expected:
            raise InvalidTransitionError(
                f"Workspace {session_id} is {current.status.value}, expected one of "
                f"{sorted(item.value for item in expected)}"
            )
        forbidden = {"session_id", "task_id", "username", "created_at", "status"}
        overlap = forbidden.intersection(changes)
        if overlap:
            raise ValueError(f"Immutable workspace fields: {sorted(overlap)}")
        updated = replace(
            current, status=status, updated_at=utc_now_iso(), **changes
        )
        if current.status in ACTIVE_WORKSPACE_STATUSES and status not in ACTIVE_WORKSPACE_STATUSES:
            self._finish_workspace(current, updated)
        else:
            self._conditional_put_workspace(updated, expected)
        return updated

    def _conditional_put_workspace(
        self, workspace: WorkspaceSession, expected: set[WorkspaceStatus]
    ) -> None:
        self.client.put_item(
            TableName=self.table_name,
            Item=self._item(
                {
                    "pk": f"WORKSPACE#{workspace.session_id}",
                    "sk": "META",
                    "entity": "workspace",
                    **workspace.to_dict(),
                }
            ),
            ConditionExpression="#status IN (" + ",".join(f":s{i}" for i, _ in enumerate(expected)) + ")",
            ExpressionAttributeNames={"#status": "status"},
            ExpressionAttributeValues=self._values(
                {f":s{i}": item.value for i, item in enumerate(expected)}
            ),
        )

    def _finish_workspace(
        self, current: WorkspaceSession, updated: WorkspaceSession
    ) -> None:
        expected_values = self._values({":expected": current.status.value})
        lock_values = self._values({":session_id": current.session_id})
        self.client.transact_write_items(
            TransactItems=[
                {
                    "Put": {
                        "TableName": self.table_name,
                        "Item": self._item(
                            {
                                "pk": f"WORKSPACE#{updated.session_id}",
                                "sk": "META",
                                "entity": "workspace",
                                **updated.to_dict(),
                            }
                        ),
                        "ConditionExpression": "#status = :expected",
                        "ExpressionAttributeNames": {"#status": "status"},
                        "ExpressionAttributeValues": expected_values,
                    }
                },
                self._lock_delete(f"LOCK#USER#{current.username}", lock_values),
                self._lock_delete(f"LOCK#TASK#{current.task_id}", lock_values),
                {
                    "Update": {
                        "TableName": self.table_name,
                        "Key": self._item({"pk": "PORTAL", "sk": "ACTIVE_COUNT"}),
                        "UpdateExpression": "ADD active_count :minus_one",
                        "ConditionExpression": "active_count > :zero",
                        "ExpressionAttributeValues": self._values(
                            {":minus_one": -1, ":zero": 0}
                        ),
                    }
                },
            ]
        )

    def _lock_delete(
        self, pk: str, values: dict[str, dict[str, Any]]
    ) -> dict[str, Any]:
        return {
            "Delete": {
                "TableName": self.table_name,
                "Key": self._item({"pk": pk, "sk": "ACTIVE"}),
                "ConditionExpression": "session_id = :session_id",
                "ExpressionAttributeValues": values,
            }
        }
