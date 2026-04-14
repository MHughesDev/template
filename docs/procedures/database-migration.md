# docs/procedures/database-migration.md

<!-- CROSS-REFERENCES -->
<!-- - Per spec §26.5 and §28.3; CI: .github/workflows/ci.yml migrate-dry-run -->

**Purpose:** Author Alembic revisions that work for **both** SQLite (used in CI dry-run and many dev setups) and PostgreSQL (production).

## Trigger / When to Use

- Adding or changing tables, columns, indexes, or constraints.
- Any PR that adds files under `apps/api/alembic/versions/`.

## Prerequisites

- `DATABASE_URL` and `JWT_SECRET_KEY` set for local runs (see `.env.example`).
- Read [ci-failure-triage.md](ci-failure-triage.md) if CI `migrate-dry-run` fails.

## Dialect rules (required)

1. **SQLite cannot apply arbitrary `ALTER` operations.** Adding/dropping foreign keys or some constraints may require **`op.batch_alter_table(...)`** (batch mode) for SQLite while PostgreSQL can use plain `op.add_column` / `op.create_foreign_key`.
2. **Test both paths before pushing:** run `make ci-migrate-dry-run` (matches CI: ephemeral SQLite file + `make migrate`). If you use Postgres locally, also run `make migrate` against a dev Postgres URL.
3. **Autogenerate is a draft.** Review every revision for dialect-specific operations; adjust with `batch_alter_table` or `op.get_bind().dialect.name` branches when needed.
4. **Downgrade:** keep `downgrade()` symmetric with `upgrade()` for SQLite batch sections.

## Exact commands

| Command | Purpose |
|---------|---------|
| `make migrate` | Apply migrations to DB pointed at by `DATABASE_URL` |
| `make migrate:create MESSAGE="..."` | Create new revision (autogenerate) |
| `make ci-migrate-dry-run` | **Same checks as CI** — SQLite SQL preview + apply to fresh file |

## Validation checks

- [ ] `make ci-migrate-dry-run` passes.
- [ ] `make test` passes (ORM and API tests use migrated schema).

## Rollback or failure handling

- If `upgrade` fails in CI on SQLite, classify as **migration/dialect** in [ci-failure-triage.md](ci-failure-triage.md), fix the revision using batch mode or conditional dialect branches, then re-run `make ci-migrate-dry-run`.

## Handoff expectations

- Note in the PR which dialects were verified (SQLite via `ci-migrate-dry-run`, Postgres if applicable).
