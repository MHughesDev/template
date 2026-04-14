# apps/api/src/example/router.py
"""HTTP routes for the example teaching module."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, Response, status
from packages.contracts.pagination import PaginatedResponse, PaginationParams

from apps.api.src.auth.dependencies import app_error_to_http, get_current_user
from apps.api.src.auth.models import User
from apps.api.src.example.dependencies import get_example_service, get_pagination_params
from apps.api.src.example.schemas import ExampleCreate, ExampleResponse, ExampleUpdate
from apps.api.src.example.service import ExampleService
from apps.api.src.exceptions import AppError

router = APIRouter(prefix="/examples", tags=["Examples"])


def _handle(exc: AppError) -> HTTPException:
    return app_error_to_http(exc)


@router.get("/", response_model=PaginatedResponse[ExampleResponse])
async def list_examples(
    params: PaginationParams = Depends(get_pagination_params),
    service: ExampleService = Depends(get_example_service),
    _user: User = Depends(get_current_user),
) -> PaginatedResponse[ExampleResponse]:
    try:
        return await service.list(params)
    except AppError as exc:
        raise _handle(exc) from exc


@router.post(
    "/",
    response_model=ExampleResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_example(
    body: ExampleCreate,
    service: ExampleService = Depends(get_example_service),
    _user: User = Depends(get_current_user),
) -> ExampleResponse:
    try:
        row = await service.create(body)
        return ExampleResponse.model_validate(row)
    except AppError as exc:
        raise _handle(exc) from exc


@router.get("/{example_id}", response_model=ExampleResponse)
async def get_example(
    example_id: uuid.UUID,
    service: ExampleService = Depends(get_example_service),
    _user: User = Depends(get_current_user),
) -> ExampleResponse:
    try:
        row = await service.get(example_id)
        return ExampleResponse.model_validate(row)
    except AppError as exc:
        raise _handle(exc) from exc


@router.patch("/{example_id}", response_model=ExampleResponse)
async def update_example(
    example_id: uuid.UUID,
    body: ExampleUpdate,
    service: ExampleService = Depends(get_example_service),
    _user: User = Depends(get_current_user),
) -> ExampleResponse:
    try:
        row = await service.update(example_id, body)
        return ExampleResponse.model_validate(row)
    except AppError as exc:
        raise _handle(exc) from exc


@router.delete("/{example_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_example(
    example_id: uuid.UUID,
    service: ExampleService = Depends(get_example_service),
    _user: User = Depends(get_current_user),
) -> Response:
    try:
        await service.delete(example_id)
    except AppError as exc:
        raise _handle(exc) from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)
