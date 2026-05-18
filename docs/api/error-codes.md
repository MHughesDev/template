---
doc_id: "4.2"
title: "error codes"
section: "API"
status: "pending-init"
summary: "Error code taxonomy. Stable codes with descriptions, HTTP status mappings, and client handling guidance. Populated during initialization from IDEA.md workflows."
updated: "2026-05-17"
---

# API Error Codes
<!-- derived from: IDEA.md workflows — populated by repo_initialize -->

## Error format

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": {}
  }
}
```

## Error codes

| Code | HTTP | Description | Resolution |
|------|------|-------------|------------|
| `INVALID_REQUEST` | 400 | Malformed request | Check request body |
| `UNAUTHORIZED` | 401 | Missing/invalid token | Authenticate |
| `FORBIDDEN` | 403 | Insufficient permissions | Check role |
| `NOT_FOUND` | 404 | Resource not found | Verify ID |
| `CONFLICT` | 409 | Resource already exists | Use unique values |

_[This section is populated by `skills/init/repo_initialize.md` during repository initialization.]_
