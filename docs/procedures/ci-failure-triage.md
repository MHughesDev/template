# docs/procedures/ci-failure-triage.md

<!-- CROSS-REFERENCES -->
<!-- - Related: validate-change.md, database-migration.md -->

**Purpose:** Classify GitHub Actions failures and reproduce them locally before guessing fixes.

## When to use

Any time a workflow job fails on `main` or a PR branch.

## Classification (pick one before editing code)

| Bucket | Typical signals | First local check |
|--------|-----------------|-------------------|
| **Authoring** | Test assertion, mypy, ruff | `make test`, `make typecheck`, `make lint` |
| **Migration / dialect** | Alembic error mentioning SQLite, `ALTER`, constraint | `make ci-migrate-dry-run` |
| **Container / scan policy** | Trivy exits 1 after image exists | `make image-build` then `make image-scan`; read table vs exit message |
| **Tooling / workflow** | Action not found, login 403, missing permission | Compare workflow `uses:` pins to upstream tags; verify GHCR login and `permissions` |
| **Platform feature** | dependency-review “Dependency graph disabled” | Enable graph in repo settings, or accept `continue-on-error` with documented risk |

## Local parity targets (map to workflows)

- **CI `migrate-dry-run` job:** `make ci-migrate-dry-run` (SQLite SQL preview + `make migrate` on a fresh DB file — same pattern as `.github/workflows/ci.yml`).
- **Security `image-scan`:** `make image-build` then `make image-scan` (requires `trivy` in PATH).
- **Full gate before PR:** `make validate-change` or the matrix in [validate-change.md](validate-change.md).

## Ordered steps

1. Open the failed workflow run and note the **exact job name** and **failing step** (not only Copilot summary).
2. Assign the failure to one bucket in the table above.
3. Run the matching **local parity** command from the repo root.
4. Fix at the correct layer (migration vs app vs workflow vs policy doc), then re-run the same local command.
5. If the fix is procedural, add a sentence to the relevant procedure or PR template so the same class fails earlier next time.

## Validation

- [ ] Local parity command passes for the same failure class.
- [ ] `make docs:check` if documentation changed.

## Related

- [database-migration.md](database-migration.md) — SQLite vs PostgreSQL migration rules.
- [validate-change.md](validate-change.md) — Pre-PR validation matrix.
