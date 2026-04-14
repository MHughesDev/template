# apps/api/src/auth/router.py
"""Authentication routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from apps.api.src.auth import schemas
from apps.api.src.auth.dependencies import (
    app_error_to_http,
    get_auth_service,
    get_current_user,
)
from apps.api.src.auth.models import User
from apps.api.src.auth.service import AuthService
from apps.api.src.exceptions import AppError

router = APIRouter(prefix="/auth", tags=["Auth"])


def _handle(exc: AppError) -> HTTPException:
    return app_error_to_http(exc)


@router.post(
    "/register",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    payload: schemas.RegisterRequest,
    service: AuthService = Depends(get_auth_service),
) -> schemas.UserResponse:
    """Register a new user account."""

    try:
        user = await service.create_user(payload)
    except AppError as exc:
        raise _handle(exc) from exc
    return schemas.UserResponse.model_validate(user)


@router.post("/login", response_model=schemas.TokenResponse)
async def login(
    payload: schemas.LoginRequest,
    service: AuthService = Depends(get_auth_service),
) -> schemas.TokenResponse:
    """Authenticate and issue tokens."""

    try:
        user = await service.authenticate_user(payload)
        return await service.issue_tokens(user)
    except AppError as exc:
        raise _handle(exc) from exc


@router.post("/refresh", response_model=schemas.TokenResponse)
async def refresh(
    payload: schemas.RefreshRequest,
    service: AuthService = Depends(get_auth_service),
) -> schemas.TokenResponse:
    """Exchange a refresh token for a new token pair."""

    try:
        return await service.refresh_tokens(payload.refresh_token)
    except AppError as exc:
        raise _handle(exc) from exc


@router.post("/logout", response_model=schemas.LogoutResponse)
async def logout(
    payload: schemas.RefreshRequest,
    current_user: User = Depends(get_current_user),
    service: AuthService = Depends(get_auth_service),
) -> schemas.LogoutResponse:
    """Revoke the provided refresh token for the authenticated user."""

    try:
        await service.revoke_refresh_token(payload.refresh_token, current_user.id)
    except AppError as exc:
        raise _handle(exc) from exc
    return schemas.LogoutResponse()
