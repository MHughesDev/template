# apps/api/tests/factories.py
"""Test data helpers for ORM models."""

from __future__ import annotations

import secrets
import uuid
from datetime import UTC, datetime, timedelta
from uuid import UUID

from passlib.context import CryptContext

from apps.api.src.auth.models import RefreshToken, User
from apps.api.src.tenancy.models import Tenant

_pwd = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password with reduced rounds for faster tests."""

    return _pwd.hash(password, rounds=4)


def create_test_tenant(
    *,
    name: str = "Test Org",
    slug: str | None = None,
) -> Tenant:
    """Build a ``Tenant`` row (caller persists)."""

    now = datetime.now(UTC)
    return Tenant(
        name=name,
        slug=slug or f"t-{uuid.uuid4().hex[:8]}",
        is_active=True,
        created_at=now,
        updated_at=now,
    )


def create_test_user(
    *,
    email: str | None = None,
    password: str = "testpassword1!",
    tenant_id: UUID | None = None,
) -> User:
    """Build a ``User`` row (caller persists)."""

    now = datetime.now(UTC)
    return User(
        email=email or f"user-{uuid.uuid4().hex[:8]}@example.com",
        hashed_password=hash_password(password),
        is_active=True,
        tenant_id=tenant_id,
        created_at=now,
        updated_at=now,
    )


def create_test_refresh_token(*, user: User, token: str | None = None) -> RefreshToken:
    """Build a refresh token row (caller persists)."""

    now = datetime.now(UTC)
    return RefreshToken(
        user_id=user.id,
        token=token or secrets.token_urlsafe(32),
        expires_at=now + timedelta(days=30),
        revoked=False,
        created_at=now,
    )
