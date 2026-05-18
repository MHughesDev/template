---
doc_id: "3.11"
title: "commands"
section: "Development"
status: "pending-init"
summary: "Make target catalog scoped to this product (dev / test / db / queue / CI / profiles). Populated during initialization."
updated: "2026-05-17"
---

# Development Commands
<!-- populated by repo_initialize -->

## Development

| Command | Purpose |
|---------|---------|
| `make dev` | Start development servers |
| `make docker-up` | Start with Docker Compose |
| `make docker-down` | Stop Docker Compose |

## Testing

| Command | Purpose |
|---------|---------|
| `make test` | Run full test suite |
| `make test:affected` | Run tests for changed files |

## Database

| Command | Purpose |
|---------|---------|
| `make migrate` | Create migration |
| `make migrate-up` | Apply migrations |
| `make migrate-down` | Rollback migration |
| `make db:seed` | Seed database |

## Queue

| Command | Purpose |
|---------|---------|
| `make queue:top-item` | Show next queue item |
| `make queue:validate` | Validate queue CSV |

_[This section is populated by `skills/init/repo_initialize.md` during repository initialization.]_
