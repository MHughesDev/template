# apps/api/src/example/schemas.py
"""Pydantic shapes for the example module."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class ExampleCreate(BaseModel):
    """Create an example row."""

    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None


class ExampleUpdate(BaseModel):
    """Patch fields on an example row."""

    title: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    status: str | None = None


class ExampleResponse(BaseModel):
    """API response for a single example."""

    model_config = {"from_attributes": True}

    id: uuid.UUID
    title: str
    description: str | None
    status: str
    created_at: datetime
    updated_at: datetime
