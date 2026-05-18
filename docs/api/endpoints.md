---
doc_id: "4.1"
title: "endpoints"
section: "API"
status: "pending-init"
summary: "API endpoint catalog. Auto-generated or manually maintained list of all routes with request/response schemas. Populated during initialization from IDEA.md §12."
updated: "2026-05-17"
---

# API Endpoints
<!-- derived from: IDEA.md §12 — populated by repo_initialize -->

## Authentication

### POST /api/v1/auth/login

**Request:**
```json
{
  "email": "user@example.com",
  "password": "string"
}
```

**Response:**
```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

## Core Resources

### GET /api/v1/items

**Query params:** `skip`, `limit`

**Response:**
```json
{
  "items": [],
  "total": 0
}
```

### POST /api/v1/items

**Request:**
```json
{
  "name": "string",
  "description": "string"
}
```

_[This section is populated by `skills/init/repo_initialize.md` during repository initialization.]_
