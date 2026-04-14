# .cursor/commands/validate.md

<!-- BLUEPRINT: Composer 2 implements from this structure -->
<!-- CROSS-REFERENCES -->
<!-- - Links to: docs/procedures/validate-change.md -->
<!-- - Make targets: lint, fmt, typecheck, test, queue:validate -->

> PURPOSE: Optional reusable Cursor command to run the full validation suite before any PR. Ensures agents run all required checks in the correct order. Per spec §26.2 item 17.

## Command Metadata

> CONTENT: Command metadata block. Fields:
> - name: "Validate"
> - description: "Run full validation suite: lint, format check, typecheck, tests, queue validate. Use before any PR."
> - trigger: "After implementing changes, before opening a PR. Also use after significant refactoring."
> - linked_procedure: docs/procedures/validate-change.md

## Steps

> CONTENT: Ordered validation steps (exact Make targets):
> 1. `make fmt` — apply ruff formatting (or check-only with `make fmt:check`)
> 2. `make lint` — run ruff linting
> 3. `make typecheck` — run mypy --strict
> 4. `make test` — run full test suite with coverage
> 5. `make queue:validate` — validate queue schema and invariants (if queue was touched)
> 6. `make docs:check` — verify documentation links and generated docs (if docs were updated)
> 7. `make security:scan` — run bandit and dependency audit (for security-adjacent changes)
> 8. Capture all output — include in PR description as evidence

## Expected Output

> CONTENT: Expected output from a fully passing validation run:
> - ruff: no lint errors, no format changes needed
> - mypy: no type errors
> - pytest: all tests pass, coverage above floor
> - queue:validate: "Queue valid" message
> - docs:check: "Docs OK" or "Generated docs match source"
> - security:scan: no HIGH/CRITICAL findings (or all findings in accepted-risks.md)
