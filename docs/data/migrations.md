---
doc_id: "21.2"
title: "migrations"
section: "Data"
status: "pending-init"
summary: "Project-specific Alembic SOP: create, review checklist, apply, rollback, CI behavior. Populated during initialization."
updated: "2026-05-17"
---

# Database Migrations
<!-- populated by repo_initialize -->

## Creating migrations

```bash
make migrate message="add_user_table"
```

## Review checklist

- [ ] Migration has both `upgrade()` and `downgrade()`
- [ ] Operations are idempotent where possible
- [ ] Index additions are concurrent (PostgreSQL)
- [ ] No data loss in `downgrade()` path

## Applying migrations

```bash
make migrate-up
```

## Rollback

```bash
make migrate-down
```

_[This section is populated by `skills/init/repo_initialize.md` during repository initialization.]_
