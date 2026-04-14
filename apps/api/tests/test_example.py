# apps/api/tests/test_example.py
"""Tests for the example teaching module (CRUD + pagination)."""

from __future__ import annotations

import uuid

import pytest
from httpx import AsyncClient


async def _register_and_token(client: AsyncClient, email: str) -> str:
    await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "strong-pass1"},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "strong-pass1"},
    )
    assert login.status_code == 200
    return login.json()["access_token"]


def _auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_create_example_success(client: AsyncClient) -> None:
    token = await _register_and_token(client, "ex-create@example.com")
    response = await client.post(
        "/api/v1/examples/",
        json={"title": "Hello", "description": "d1"},
        headers=_auth_headers(token),
    )
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Hello"
    assert body["description"] == "d1"
    assert body["status"] == "draft"
    assert "id" in body


@pytest.mark.asyncio
async def test_create_example_missing_title(client: AsyncClient) -> None:
    token = await _register_and_token(client, "ex-bad@example.com")
    response = await client.post(
        "/api/v1/examples/",
        json={"title": ""},
        headers=_auth_headers(token),
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_example_success(client: AsyncClient) -> None:
    token = await _register_and_token(client, "ex-get@example.com")
    created = await client.post(
        "/api/v1/examples/",
        json={"title": "T1", "description": None},
        headers=_auth_headers(token),
    )
    assert created.status_code == 201
    ex_id = created.json()["id"]
    got = await client.get(
        f"/api/v1/examples/{ex_id}",
        headers=_auth_headers(token),
    )
    assert got.status_code == 200
    assert got.json()["title"] == "T1"


@pytest.mark.asyncio
async def test_get_example_not_found(client: AsyncClient) -> None:
    token = await _register_and_token(client, "ex-404@example.com")
    rid = str(uuid.uuid4())
    response = await client.get(
        f"/api/v1/examples/{rid}",
        headers=_auth_headers(token),
    )
    assert response.status_code == 404
    detail = response.json()["detail"]
    assert isinstance(detail, dict)
    assert detail.get("code") == "NOT_FOUND"


@pytest.mark.asyncio
async def test_list_examples_empty(client: AsyncClient) -> None:
    token = await _register_and_token(client, "ex-empty@example.com")
    response = await client.get(
        "/api/v1/examples/",
        headers=_auth_headers(token),
    )
    assert response.status_code == 200
    body = response.json()
    assert body["items"] == []
    assert "page_info" in body


@pytest.mark.asyncio
async def test_list_examples_paginated(client: AsyncClient) -> None:
    token = await _register_and_token(client, "ex-page@example.com")
    for i in range(3):
        r = await client.post(
            "/api/v1/examples/",
            json={"title": f"Item {i}"},
            headers=_auth_headers(token),
        )
        assert r.status_code == 201
    response = await client.get(
        "/api/v1/examples/?page_size=2&page=1",
        headers=_auth_headers(token),
    )
    assert response.status_code == 200
    body = response.json()
    assert len(body["items"]) == 2
    assert body["page_info"]["has_next"] is True


@pytest.mark.asyncio
async def test_update_example_success(client: AsyncClient) -> None:
    token = await _register_and_token(client, "ex-upd@example.com")
    created = await client.post(
        "/api/v1/examples/",
        json={"title": "Old"},
        headers=_auth_headers(token),
    )
    ex_id = created.json()["id"]
    patch = await client.patch(
        f"/api/v1/examples/{ex_id}",
        json={"title": "New"},
        headers=_auth_headers(token),
    )
    assert patch.status_code == 200
    assert patch.json()["title"] == "New"


@pytest.mark.asyncio
async def test_update_example_not_found(client: AsyncClient) -> None:
    token = await _register_and_token(client, "ex-upd404@example.com")
    rid = str(uuid.uuid4())
    response = await client.patch(
        f"/api/v1/examples/{rid}",
        json={"title": "X"},
        headers=_auth_headers(token),
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_example_success(client: AsyncClient) -> None:
    token = await _register_and_token(client, "ex-del@example.com")
    created = await client.post(
        "/api/v1/examples/",
        json={"title": "To delete"},
        headers=_auth_headers(token),
    )
    ex_id = created.json()["id"]
    deleted = await client.delete(
        f"/api/v1/examples/{ex_id}",
        headers=_auth_headers(token),
    )
    assert deleted.status_code == 204
    again = await client.get(
        f"/api/v1/examples/{ex_id}",
        headers=_auth_headers(token),
    )
    assert again.status_code == 404


@pytest.mark.asyncio
async def test_delete_example_not_found(client: AsyncClient) -> None:
    token = await _register_and_token(client, "ex-del404@example.com")
    rid = str(uuid.uuid4())
    response = await client.delete(
        f"/api/v1/examples/{rid}",
        headers=_auth_headers(token),
    )
    assert response.status_code == 404
