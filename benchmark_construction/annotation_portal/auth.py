"""Cognito authentication and opaque portal-cookie helpers."""

from __future__ import annotations

import hashlib
import secrets
import threading
import time
from dataclasses import dataclass
from typing import Any, Protocol

from .models import PortalSession, UserIdentity, UserRole
from .store import PortalStore


@dataclass(frozen=True)
class LoginSuccess:
    identity: UserIdentity


@dataclass(frozen=True)
class PasswordChangeRequired:
    username: str
    cognito_session: str


LoginResult = LoginSuccess | PasswordChangeRequired


class IdentityProvider(Protocol):
    def login(self, username: str, password: str) -> LoginResult: ...

    def complete_new_password(
        self, username: str, new_password: str, cognito_session: str
    ) -> LoginSuccess: ...


class StaticIdentityProvider:
    """Explicit local-development provider; never enabled implicitly."""

    def __init__(
        self, credentials: dict[str, str], *, admin_usernames: frozenset[str]
    ) -> None:
        self.credentials = dict(credentials)
        self.admin_usernames = admin_usernames

    def login(self, username: str, password: str) -> LoginResult:
        expected = self.credentials.get(username)
        if expected is None or not secrets.compare_digest(expected, password):
            raise PermissionError("Invalid username or password")
        role = UserRole.ADMIN if username in self.admin_usernames else UserRole.ANNOTATOR
        return LoginSuccess(UserIdentity(username, role))

    def complete_new_password(
        self, username: str, new_password: str, cognito_session: str
    ) -> LoginSuccess:
        raise PermissionError("Local development users do not have password challenges")


class PasswordChallengeManager:
    """Keep Cognito challenge sessions server-side behind short-lived opaque IDs."""

    def __init__(self, *, lifetime_seconds: int = 10 * 60) -> None:
        self.lifetime_seconds = lifetime_seconds
        self._lock = threading.Lock()
        self._challenges: dict[str, tuple[str, str, int]] = {}

    def create(self, challenge: PasswordChangeRequired) -> str:
        challenge_id = secrets.token_urlsafe(24)
        with self._lock:
            self._challenges[challenge_id] = (
                challenge.username,
                challenge.cognito_session,
                int(time.time()) + self.lifetime_seconds,
            )
        return challenge_id

    def consume(self, challenge_id: str, username: str) -> str:
        with self._lock:
            challenge = self._challenges.pop(challenge_id, None)
        if challenge is None:
            raise PermissionError("Password challenge is missing or already used")
        expected_username, cognito_session, expires_at = challenge
        if expires_at <= int(time.time()) or expected_username != username:
            raise PermissionError("Password challenge is invalid or expired")
        return cognito_session


class CognitoIdentityProvider:
    """Authenticate pre-created users without exposing Cognito tokens to browsers."""

    def __init__(
        self,
        client: Any,
        *,
        client_id: str,
        admin_usernames: frozenset[str] = frozenset(),
    ) -> None:
        self.client = client
        self.client_id = client_id
        self.admin_usernames = admin_usernames

    def login(self, username: str, password: str) -> LoginResult:
        response = self.client.initiate_auth(
            AuthFlow="USER_PASSWORD_AUTH",
            ClientId=self.client_id,
            AuthParameters={"USERNAME": username, "PASSWORD": password},
        )
        if response.get("ChallengeName") == "NEW_PASSWORD_REQUIRED":
            return PasswordChangeRequired(
                username=username,
                cognito_session=response["Session"],
            )
        return LoginSuccess(self._identity(response, fallback_username=username))

    def complete_new_password(
        self, username: str, new_password: str, cognito_session: str
    ) -> LoginSuccess:
        response = self.client.respond_to_auth_challenge(
            ClientId=self.client_id,
            ChallengeName="NEW_PASSWORD_REQUIRED",
            Session=cognito_session,
            ChallengeResponses={"USERNAME": username, "NEW_PASSWORD": new_password},
        )
        return LoginSuccess(self._identity(response, fallback_username=username))

    def _identity(
        self, response: dict[str, Any], *, fallback_username: str
    ) -> UserIdentity:
        access_token = response.get("AuthenticationResult", {}).get("AccessToken")
        if not access_token:
            raise RuntimeError("Cognito response did not contain an access token")
        user = self.client.get_user(AccessToken=access_token)
        username = user.get("Username") or fallback_username
        role = (
            UserRole.ADMIN
            if username in self.admin_usernames
            else UserRole.ANNOTATOR
        )
        return UserIdentity(username=username, role=role)


class PortalSessionManager:
    def __init__(self, store: PortalStore, *, lifetime_seconds: int = 12 * 3600):
        self.store = store
        self.lifetime_seconds = lifetime_seconds

    @staticmethod
    def token_hash(token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    def create(self, identity: UserIdentity) -> str:
        token = secrets.token_urlsafe(32)
        self.store.put_portal_session(
            PortalSession(
                token_hash=self.token_hash(token),
                username=identity.username,
                role=identity.role,
                expires_at_epoch=int(time.time()) + self.lifetime_seconds,
            )
        )
        return token

    def resolve(self, token: str | None) -> UserIdentity | None:
        if not token:
            return None
        session = self.store.get_portal_session(self.token_hash(token))
        if session is None:
            return None
        if session.expires_at_epoch <= int(time.time()):
            self.store.delete_portal_session(session.token_hash)
            return None
        return UserIdentity(username=session.username, role=session.role)

    def revoke(self, token: str | None) -> None:
        if token:
            self.store.delete_portal_session(self.token_hash(token))
