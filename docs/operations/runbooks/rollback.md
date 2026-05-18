---
doc_id: "6.13"
title: "runbook — rollback"
section: "Operations"
status: "pending-init"
summary: "Application rollback, database migration rollback, and incident response procedures. Populated during initialization."
updated: "2026-05-17"
---

# Runbook: Rollback
<!-- populated by repo_initialize -->

## Application rollback

### Kubernetes

```bash
kubectl rollout undo deployment/api
```

### Docker Compose

```bash
docker compose pull api:latest-stable
docker compose up -d api
```

## Database migration rollback

```bash
make migrate-down  # One step
alembic downgrade -2  # Multiple steps
```

## When to rollback vs. fix-forward

| Situation | Recommended action |
|-----------|-------------------|
| _[Data corruption]_ | Rollback |
| _[Minor UI bug]_ | Fix-forward |

_[This section is populated by `skills/init/repo_initialize.md` during repository initialization.]_
