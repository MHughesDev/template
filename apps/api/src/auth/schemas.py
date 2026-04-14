# apps/api/src/auth/schemas.py
"""Pydantic schemas for authentication endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class RegisterRequest(BaseModel):
    """Create a new user account."""

    model_config = ConfigDict(frozen=True)

    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

    @field_validator("password")
    @classmethod
    def _password_strength(cls, value: str) -> str:
        if value.isalpha():
            msg = "password must include at least one non-letter character"
            raise ValueError(msg)
        return value


class LoginRequest(BaseModel):
    """Authenticate with email and password."""

    model_config = ConfigDict(frozen=True)

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Issued OAuth2-style token pair."""

    model_config = ConfigDict(frozen=True)

    access_token: str
    refresh_token: str
    token_type: Literal["bearer"] = "bearer"  # noqa: S105
    expires_in: int


class RefreshRequest(BaseModel):
    """Refresh or revoke a refresh token."""

    model_config = ConfigDict(frozen=True)

    refresh_token: str


class UserResponse(BaseModel):
    """Public user representation."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: str
    is_active: bool
    tenant_id: UUID | None
    created_at: datetime


class LogoutResponse(BaseModel):
    """Logout acknowledgement."""

    model_config = ConfigDict(frozen=True)

    status: Literal["logged_out"] = "logged_out"
