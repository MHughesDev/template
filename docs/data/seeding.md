---
doc_id: "21.3"
title: "seeding"
section: "Data"
status: "pending-init"
summary: "What make db:seed creates, in which environments, and how to reset/re-seed. Populated during initialization."
updated: "2026-05-17"
---

# Database Seeding
<!-- populated by repo_initialize -->

## Seed data

_[What data is created by `make db:seed`]_

## Environments

| Environment | Seeding behavior |
|-------------|------------------|
| Development | _[Full seed with test data]_ |
| Staging | _[Minimal seed]_ |
| Production | _[No seeding]_ |

## Reset/re-seed

```bash
make db:reset  # Drop, create, migrate, seed
```

_[This section is populated by `skills/init/repo_initialize.md` during repository initialization.]_
