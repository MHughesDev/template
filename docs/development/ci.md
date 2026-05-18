---
doc_id: "3.9"
title: "ci"
section: "Development"
status: "pending-init"
summary: "CI pipeline stages, matrix, how to reproduce locally, common CI failures and fixes. Populated during initialization."
updated: "2026-05-17"
---

# Continuous Integration
<!-- populated by repo_initialize -->

## Pipeline stages

1. **Lint & Format** — Ruff checks
2. **Type Check** — mypy
3. **Test** — pytest with coverage
4. **Build** — Docker image build
5. **Security Scan** — dependency audit

## Matrix

| Python | Database | Profile |
|--------|----------|---------|
| 3.12 | PostgreSQL | default |
| 3.12 | SQLite | minimal |

## Reproducing locally

```bash
# Run the full CI pipeline locally
make preflight
make lint
make typecheck
make test
make security:scan
```

## Common failures

| Failure | Cause | Fix |
|---------|-------|-----|
| _[e.g., Lockfile out of date]_ | _[Dependencies changed]_ | _[Run `make lock`]_ |

_[This section is populated by `skills/init/repo_initialize.md` during repository initialization.]_
