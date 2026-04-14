# apps/api/src/health/router.py
"""Health, readiness, and liveness endpoints."""

from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.src.dependencies import get_db

router = APIRouter(tags=["Health"])


class HealthResponse(BaseModel):
    """Basic liveness payload."""

    status: Literal["ok"] = "ok"


class ReadinessResponse(BaseModel):
    """Readiness payload with dependency checks."""

    status: Literal["ready", "not_ready"]
    checks: dict[str, str] = Field(default_factory=dict)


class LivenessResponse(BaseModel):
    """Process liveness payload."""

    status: Literal["alive"] = "alive"


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Fast liveness probe — no external dependencies."""

    return HealthResponse()


@router.get("/ready", response_model=ReadinessResponse)
async def ready(session: AsyncSession = Depends(get_db)) -> ReadinessResponse:
    """Readiness probe — verifies database connectivity."""

    try:
        await session.execute(text("SELECT 1"))
    except Exception as exc:  # noqa: BLE001 - surface dependency failures
        return ReadinessResponse(
            status="not_ready", checks={"database": f"error: {exc!s}"}
        )
    return ReadinessResponse(status="ready", checks={"database": "ok"})


@router.get("/live", response_model=LivenessResponse)
async def live() -> LivenessResponse:
    """Kubernetes-style liveness endpoint."""

    return LivenessResponse()
