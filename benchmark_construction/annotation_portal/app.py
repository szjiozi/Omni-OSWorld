"""FastAPI application for the multi-annotator portal."""

from dataclasses import dataclass
from pathlib import Path
from typing import Annotated, Any
from urllib.parse import urlencode

import httpx
import websockets
from fastapi import (
    Cookie,
    Depends,
    FastAPI,
    HTTPException,
    Request,
    Response,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .auth import (
    IdentityProvider,
    LoginSuccess,
    PasswordChangeRequired,
    PasswordChallengeManager,
    PortalSessionManager,
)
from .models import TaskAssignment, UserIdentity, UserRole
from .service import AnnotationPortalService


SESSION_COOKIE = "osworld_annotation_session"


@dataclass(frozen=True)
class PortalWebConfig:
    static_dir: Path
    cookie_secure: bool = True
    cookie_max_age: int = 12 * 3600


class LoginBody(BaseModel):
    username: str
    password: str


class NewPasswordBody(BaseModel):
    username: str
    new_password: str
    challenge_id: str


class AssignmentBody(BaseModel):
    username: str
    task_id: str


def create_app(
    *,
    config: PortalWebConfig,
    identity_provider: IdentityProvider,
    session_manager: PortalSessionManager,
    challenge_manager: PasswordChallengeManager,
    service: AnnotationPortalService,
    lifespan: Any = None,
) -> FastAPI:
    app = FastAPI(
        title="OSWorld Reference Annotation Hub", docs_url=None, lifespan=lifespan
    )

    def current_identity(
        token: str | None = Cookie(default=None, alias=SESSION_COOKIE),
    ) -> UserIdentity:
        identity = session_manager.resolve(token)
        if identity is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return identity

    def admin_identity(
        identity: Annotated[UserIdentity, Depends(current_identity)],
    ) -> UserIdentity:
        if identity.role != UserRole.ADMIN:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        return identity

    def set_session_cookie(response: Response, identity: UserIdentity) -> None:
        response.set_cookie(
            SESSION_COOKIE,
            session_manager.create(identity),
            max_age=config.cookie_max_age,
            httponly=True,
            secure=config.cookie_secure,
            samesite="lax",
            path="/",
        )

    @app.get("/healthz")
    def healthz() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/api/auth/login")
    def login(body: LoginBody, response: Response) -> dict[str, object]:
        try:
            result = identity_provider.login(body.username.strip(), body.password)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            ) from exc
        if isinstance(result, PasswordChangeRequired):
            return {
                "status": "new_password_required",
                "username": result.username,
                "challenge_id": challenge_manager.create(result),
            }
        if not isinstance(result, LoginSuccess):
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        set_session_cookie(response, result.identity)
        return {"status": "authenticated", "user": _identity_dict(result.identity)}

    @app.post("/api/auth/new-password")
    def new_password(body: NewPasswordBody, response: Response) -> dict[str, object]:
        try:
            cognito_session = challenge_manager.consume(
                body.challenge_id, body.username.strip()
            )
            result = identity_provider.complete_new_password(
                body.username.strip(), body.new_password, cognito_session
            )
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password change failed; restart sign-in",
            ) from exc
        set_session_cookie(response, result.identity)
        return {"status": "authenticated", "user": _identity_dict(result.identity)}

    @app.post("/api/auth/logout")
    def logout(
        response: Response,
        token: str | None = Cookie(default=None, alias=SESSION_COOKIE),
    ) -> dict[str, str]:
        session_manager.revoke(token)
        response.delete_cookie(SESSION_COOKIE, path="/")
        return {"status": "logged_out"}

    @app.get("/api/me")
    def me(
        identity: Annotated[UserIdentity, Depends(current_identity)],
    ) -> dict[str, str]:
        return _identity_dict(identity)

    @app.get("/api/tasks")
    def tasks(
        identity: Annotated[UserIdentity, Depends(current_identity)],
    ) -> list[dict[str, object]]:
        return service.tasks_for(identity)

    @app.get("/api/tasks/{task_id}/files/{relative_path:path}")
    def task_file(
        task_id: str,
        relative_path: str,
        identity: Annotated[UserIdentity, Depends(current_identity)],
    ) -> FileResponse:
        try:
            return FileResponse(service.task_file(identity, task_id, relative_path))
        except PermissionError as exc:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN) from exc
        except (KeyError, FileNotFoundError) as exc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from exc

    @app.post("/api/tasks/{task_id}/launch")
    def launch(
        task_id: str,
        identity: Annotated[UserIdentity, Depends(current_identity)],
    ) -> dict[str, object]:
        try:
            return service.launch(identity, task_id).to_dict()
        except PermissionError as exc:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc))
        except (KeyError, ValueError) as exc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
        except RuntimeError as exc:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))

    @app.get("/api/workspaces/current")
    def current_workspace(
        identity: Annotated[UserIdentity, Depends(current_identity)],
    ) -> dict[str, object] | None:
        workspace = service.current_workspace(identity)
        return workspace.to_dict() if workspace else None

    @app.get("/api/workspaces/{session_id}")
    def workspace(
        session_id: str,
        identity: Annotated[UserIdentity, Depends(current_identity)],
    ) -> dict[str, object]:
        try:
            return service.workspace(identity, session_id).to_dict()
        except KeyError as exc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from exc
        except PermissionError as exc:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN) from exc

    @app.post("/api/workspaces/{session_id}/terminate")
    def terminate_workspace(
        session_id: str,
        identity: Annotated[UserIdentity, Depends(current_identity)],
    ) -> dict[str, object]:
        try:
            return service.terminate_ready_workspace(identity, session_id).to_dict()
        except KeyError as exc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from exc
        except PermissionError as exc:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN) from exc
        except RuntimeError as exc:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))

    @app.get("/api/submissions")
    def submissions(
        identity: Annotated[UserIdentity, Depends(current_identity)],
    ) -> list[dict[str, object]]:
        return service.submissions_for(identity)

    @app.get("/api/submissions/{session_id}/video")
    def submission_video(
        session_id: str,
        request: Request,
        identity: Annotated[UserIdentity, Depends(current_identity)],
    ) -> StreamingResponse:
        try:
            stream = service.recording_stream(
                identity,
                session_id,
                byte_range=request.headers.get("range"),
            )
        except KeyError as exc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from exc
        except PermissionError as exc:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN) from exc
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
                detail=str(exc),
            ) from exc

        def chunks():
            try:
                yield from stream.body.iter_chunks(chunk_size=1024 * 1024)
            finally:
                stream.body.close()

        headers = {
            "Accept-Ranges": "bytes",
            "Content-Length": str(stream.content_length),
            "Cache-Control": "private, no-store",
            "Content-Disposition": 'inline; filename="recording.mp4"',
        }
        if stream.content_range:
            headers["Content-Range"] = stream.content_range
        if stream.etag:
            headers["ETag"] = stream.etag
        return StreamingResponse(
            chunks(),
            status_code=stream.status_code,
            media_type=stream.content_type,
            headers=headers,
        )

    @app.post("/api/submissions/{session_id}/discard")
    def discard_submission(
        session_id: str,
        identity: Annotated[UserIdentity, Depends(current_identity)],
    ) -> dict[str, object]:
        try:
            return service.discard_submission(identity, session_id).to_dict()
        except KeyError as exc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from exc
        except PermissionError as exc:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN) from exc
        except RuntimeError as exc:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))

    @app.post("/api/submissions/{session_id}/restore")
    def restore_submission(
        session_id: str,
        identity: Annotated[UserIdentity, Depends(current_identity)],
    ) -> dict[str, object]:
        try:
            return service.restore_submission(identity, session_id).to_dict()
        except KeyError as exc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from exc
        except PermissionError as exc:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN) from exc
        except RuntimeError as exc:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))

    @app.post("/api/workspaces/{session_id}/recording/start")
    def start_recording(
        session_id: str,
        identity: Annotated[UserIdentity, Depends(current_identity)],
    ) -> dict[str, object]:
        try:
            return service.start_recording(identity, session_id).to_dict()
        except KeyError as exc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from exc
        except PermissionError as exc:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN) from exc
        except RuntimeError as exc:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))

    @app.post("/api/workspaces/{session_id}/recording/stop")
    def stop_recording(
        session_id: str,
        identity: Annotated[UserIdentity, Depends(current_identity)],
    ) -> dict[str, object]:
        try:
            return service.stop_recording(identity, session_id).to_dict()
        except KeyError as exc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from exc
        except PermissionError as exc:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN) from exc
        except RuntimeError as exc:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))

    @app.api_route(
        "/api/workspaces/{session_id}/vnc/{upstream_path:path}",
        methods=["GET", "POST"],
    )
    async def vnc_http_proxy(
        session_id: str,
        upstream_path: str,
        request: Request,
        identity: Annotated[UserIdentity, Depends(current_identity)],
    ) -> Response:
        try:
            workspace = service.workspace(identity, session_id)
        except KeyError as exc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from exc
        except PermissionError as exc:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN) from exc
        if not workspace.private_ip:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Workspace desktop is not ready",
            )
        query = f"?{request.url.query}" if request.url.query else ""
        upstream_url = (
            f"http://{workspace.private_ip}:5910/{upstream_path}{query}"
        )
        try:
            async with httpx.AsyncClient(trust_env=False, timeout=30) as client:
                upstream = await client.request(
                    request.method,
                    upstream_url,
                    content=await request.body(),
                    headers={
                        key: value
                        for key, value in request.headers.items()
                        if key.lower() in {"accept", "accept-language", "user-agent"}
                    },
                )
        except httpx.HTTPError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Workspace desktop is temporarily unavailable",
            ) from exc
        response_headers = {
            key: value
            for key, value in upstream.headers.items()
            if key.lower() in {"content-type", "cache-control", "etag", "last-modified"}
        }
        return Response(
            content=upstream.content,
            status_code=upstream.status_code,
            headers=response_headers,
        )

    @app.websocket("/api/workspaces/{session_id}/vnc/websockify")
    async def vnc_websocket_proxy(websocket: WebSocket, session_id: str) -> None:
        token = websocket.cookies.get(SESSION_COOKIE)
        identity = session_manager.resolve(token)
        if identity is None:
            await websocket.close(code=4401)
            return
        try:
            workspace = service.workspace(identity, session_id)
        except KeyError:
            await websocket.close(code=4404)
            return
        except PermissionError:
            await websocket.close(code=4403)
            return
        if not workspace.private_ip:
            await websocket.close(code=4409)
            return
        query = urlencode(list(websocket.query_params.multi_items()))
        upstream_url = f"ws://{workspace.private_ip}:5910/websockify"
        if query:
            upstream_url = f"{upstream_url}?{query}"
        try:
            async with websockets.connect(
                upstream_url,
                open_timeout=15,
                close_timeout=5,
                max_size=None,
                proxy=None,
            ) as upstream:
                await websocket.accept()

                async def browser_to_worker() -> None:
                    while True:
                        message = await websocket.receive()
                        if message["type"] == "websocket.disconnect":
                            return
                        if message.get("bytes") is not None:
                            await upstream.send(message["bytes"])
                        elif message.get("text") is not None:
                            await upstream.send(message["text"])

                async def worker_to_browser() -> None:
                    async for message in upstream:
                        if isinstance(message, bytes):
                            await websocket.send_bytes(message)
                        else:
                            await websocket.send_text(message)

                import asyncio

                browser_task = asyncio.create_task(browser_to_worker())
                worker_task = asyncio.create_task(worker_to_browser())
                done, pending = await asyncio.wait(
                    {browser_task, worker_task},
                    return_when=asyncio.FIRST_COMPLETED,
                )
                for task in pending:
                    task.cancel()
                for task in done:
                    task.result()
        except (OSError, TimeoutError, websockets.WebSocketException):
            if websocket.client_state.name != "DISCONNECTED":
                await websocket.close(code=1011)
        except WebSocketDisconnect:
            return

    @app.post("/api/admin/assignments")
    def assign(
        body: AssignmentBody,
        _admin: Annotated[UserIdentity, Depends(admin_identity)],
    ) -> dict[str, str]:
        try:
            service.catalog.get(body.task_id)
        except KeyError as exc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from exc
        assignment = TaskAssignment(
            task_id=body.task_id, username=body.username.strip()
        )
        service.store.put_assignment(assignment)
        return {"status": "assigned", "task_id": body.task_id, "username": body.username}

    @app.post("/api/admin/prepare")
    def prepare(
        body: AssignmentBody,
        _admin: Annotated[UserIdentity, Depends(admin_identity)],
    ) -> dict[str, object]:
        identity = UserIdentity(body.username.strip(), UserRole.ANNOTATOR)
        try:
            return service.launch(identity, body.task_id).to_dict()
        except PermissionError as exc:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc))
        except RuntimeError as exc:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))

    @app.get("/api/admin/status")
    def admin_status(
        _admin: Annotated[UserIdentity, Depends(admin_identity)],
    ) -> dict[str, object]:
        active = service.store.active_workspaces()
        return {
            "active_count": len(active),
            "max_active": service.max_active,
            "workspaces": [item.to_dict() for item in active],
        }

    assets_dir = config.static_dir / "assets"
    app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/{path:path}", include_in_schema=False)
    def frontend(path: str):
        return FileResponse(config.static_dir / "index.html")

    return app


def _identity_dict(identity: UserIdentity) -> dict[str, str]:
    return {"username": identity.username, "role": identity.role.value}
