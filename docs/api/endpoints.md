---
doc_id: "4.1"
title: "endpoints"
section: "API"
summary: "API endpoint catalog. Auto-generated or manually maintained list of all routes with request/response schemas."
updated: "2026-04-17"
---

# 4.1 — endpoints

<!-- CROSS-REFERENCES -->
<!-- - Source: generated from FastAPI OpenAPI (make docs:generate) -->

**Purpose:** API endpoint catalog. Auto-generated or manually maintained list of all routes with request/response schemas.

## 4.1.1 Overview

API endpoint catalog. Auto-generated or manually maintained list of all routes with request/response schemas. See [AGENTS.md](../../AGENTS.md) for validation commands and [spec/spec.md](../../spec/spec.md) for the full specification.

## 4.1.2 MCP (Model Context Protocol)

When the MCP integration is enabled in `apps/api/src/main.py`, the HTTP MCP
server is mounted at **`/mcp`** (see `apps/api/src/mcp/__init__.py`). Tools are
derived from the OpenAPI schema; see [add-mcp-tool.md](../procedures/add-mcp-tool.md).

## 4.1.3 Examples (teaching module)

Base path: `/api/v1/examples` (requires `Authorization: Bearer <access_token>`). List and CRUD apply to **examples owned by the authenticated user** (`owner_user_id`).

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Paginated list (`page`, `page_size`, optional `cursor` / `offset`) |
| POST | `/` | Create (`title`, optional `description`) — 201 |
| GET | `/{id}` | Get by UUID |
| PATCH | `/{id}` | Partial update |
| DELETE | `/{id}` | Delete — 204 |
