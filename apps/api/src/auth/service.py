# apps/api/src/auth/service.py
"""Authentication domain logic: users, passwords, JWTs, and refresh tokens."""

from __future__ import annotations

import secrets
from datetime import UTC, datetime, timedelta
from typing import Any, cast
from uuid import UUID

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.src.auth import models
from apps.api.src.auth.repository import RefreshTokenRepository, UserRepository
from apps.api.src.auth.schemas import LoginRequest, RegisterRequest, TokenResponse
from apps.api.src.config import Settings
from apps.api.src.exceptions import AuthenticationError, ConflictError

# pbkdf2_sha256 avoids bcrypt's 72-byte password limit; still strong for API use.
_pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def _ensure_utc(dt: datetime) -> datetime:
    """Normalize SQLite-returned naive datetimes to UTC."""

    if dt.tzinfo is None:
        return dt.replace(tzinfo=UTC)
    return dt


class AuthService:
    """Coordinates credential verification and token lifecycle."""

    def __init__(
        self,
        session: AsyncSession,
        settings: Settings,
        users: UserRepository,
        tokens: RefreshTokenRepository,
    ) -> None:
        self._session = session
        self._settings = settings
        self._users = users
        self._tokens = tokens

    async def create_user(self, request: RegisterRequest) -> models.User:
        """Register a user; raises ConflictError if the email exists."""

        existing = await self._users.get_by_email(str(request.email))
        if existing is not None:
            raise ConflictError("Email already registered")

        now = datetime.now(UTC)
        user = models.User(
            email=str(request.email),
            hashed_password=_pwd_context.hash(request.password),
            is_active=True,
            tenant_id=None,
            created_at=now,
            updated_at=now,
        )
        return await self._users.create(user)

    async def authenticate_user(self, request: LoginRequest) -> models.User:
        """Validate credentials and return the active user."""

        user = await self._users.get_by_email(str(request.email))
        generic_error = AuthenticationError("Invalid credentials")
        if user is None or not user.is_active:
            raise generic_error
        if not _pwd_context.verify(request.password, user.hashed_password):
            raise generic_error
        return user

    def create_access_token(self, user: models.User) -> str:
        """Create a signed JWT access token."""

        now = datetime.now(UTC)
        expire = now + timedelta(minutes=self._settings.jwt_access_token_expire_minutes)
        claims: dict[str, Any] = {
            "sub": str(user.id),
            "email": user.email,
            "exp": expire,
            "iat": now,
        }
        if user.tenant_id is not None:
            claims["tenant_id"] = str(user.tenant_id)
        return cast(
            str,
            jwt.encode(
                claims,
                self._settings.jwt_secret_key,
                algorithm=self._settings.jwt_algorithm,
            ),
        )

    async def create_refresh_token(self, user: models.User) -> str:
        """Persist and return an opaque refresh token."""

        token_value = secrets.token_urlsafe(48)
        now = datetime.now(UTC)
        expires_at = now + timedelta(days=self._settings.jwt_refresh_token_expire_days)
        refresh = models.RefreshToken(
            user_id=user.id,
            token=token_value,
            expires_at=expires_at,
            revoked=False,
            created_at=now,
        )
        created = await self._tokens.create(refresh)
        return created.token

    def verify_access_token(self, token: str) -> dict[str, Any]:
        """Validate a JWT access token and return claims."""

        try:
            return cast(
                dict[str, Any],
                jwt.decode(
                    token,
                    self._settings.jwt_secret_key,
                    algorithms=[self._settings.jwt_algorithm],
                ),
            )
        except JWTError as exc:
            raise AuthenticationError("Invalid or expired token") from exc

    async def issue_tokens(self, user: models.User) -> TokenResponse:
        """Create access + refresh tokens for a user."""

        access = self.create_access_token(user)
        refresh = await self.create_refresh_token(user)
        return TokenResponse(
            access_token=access,
            refresh_token=refresh,
            expires_in=self._settings.jwt_access_token_expire_minutes * 60,
        )

    async def refresh_tokens(self, refresh_token: str) -> TokenResponse:
        """Rotate refresh token and issue a new access token."""

        now = datetime.now(UTC)
        token_row = await self._tokens.get_by_token(refresh_token)
        if token_row is None or token_row.revoked:
            raise AuthenticationError("Invalid refresh token")
        expires_at = _ensure_utc(token_row.expires_at)
        if expires_at <= now:
            raise AuthenticationError("Invalid refresh token")

        user = await self._users.get_by_id(token_row.user_id)
        if user is None or not user.is_active:
            raise AuthenticationError("Invalid refresh token")

        await self._tokens.mark_revoked_flush(token_row)
        return await self.issue_tokens(user)

    async def revoke_refresh_token(self, refresh_token: str, user_id: UUID) -> None:
        """Revoke a refresh token for logout."""

        token_row = await self._tokens.get_by_token(refresh_token)
        if token_row is None or token_row.user_id != user_id:
            raise AuthenticationError("Invalid refresh token")
        await self._tokens.revoke(token_row)
