# apps/api/src/auth/repository.py
"""Persistence layer for auth domain (users and refresh tokens)."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.src.auth import models


class UserRepository:
    """User row access."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_email(self, email: str) -> models.User | None:
        result = await self._session.execute(
            select(models.User).where(models.User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: UUID) -> models.User | None:
        return await self._session.get(models.User, user_id)

    async def create(self, user: models.User) -> models.User:
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user


class RefreshTokenRepository:
    """Refresh token row access."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_token(self, token: str) -> models.RefreshToken | None:
        result = await self._session.execute(
            select(models.RefreshToken).where(models.RefreshToken.token == token)
        )
        return result.scalar_one_or_none()

    async def create(self, refresh_token: models.RefreshToken) -> models.RefreshToken:
        self._session.add(refresh_token)
        await self._session.commit()
        await self._session.refresh(refresh_token)
        return refresh_token

    async def mark_revoked_flush(self, refresh_token: models.RefreshToken) -> None:
        """Mark revoked and flush (no commit) for token rotation."""

        refresh_token.revoked = True
        await self._session.flush()

    async def revoke(self, refresh_token: models.RefreshToken) -> None:
        refresh_token.revoked = True
        await self._session.commit()
