---
doc_id: "2.13"
title: "auth"
section: "Architecture"
status: "pending-init"
summary: "Auth strategy: scheme, token lifecycle, permission model, endpoint access matrix, multi-tenancy intersection. Populated during initialization from IDEA.md §10."
updated: "2026-05-17"
---

# Authentication & Authorization
<!-- derived from: IDEA.md §10 — populated by repo_initialize -->

## Authentication scheme

_[e.g., JWT bearer tokens with refresh rotation]_

## Token lifecycle

- **Access token expiry:** _[e.g., 15 minutes]_
- **Refresh token expiry:** _[e.g., 7 days]_
- **Rotation:** _[e.g., Refresh tokens are single-use and rotated on each access token renewal]_

## Permission model

| Role | Permissions | Notes |
|------|-------------|-------|
| _[Role 1]_ | _[CRUD on X, read Y]_ | _[Notes]_ |
| _[Role 2]_ | _[Read X, admin Z]_ | _[Notes]_ |

## Endpoint access matrix

| Endpoint | Auth | Roles | Notes |
|----------|------|-------|-------|
| `GET /api/v1/items` | Bearer | Any | Public read |
| `POST /api/v1/items` | Bearer | Admin | Admin only |

_[This section is populated by `skills/init/repo_initialize.md` during repository initialization.]_
