# docs/development/coding-standards.md

<!-- CROSS-REFERENCES -->
<!-- - Referenced by: docs/development/README.md, README.md -->

**Purpose:** Python and API coding standards for this repository (typing, style, security).

## Overview

Python and API coding standards for this repository (typing, style, security). See [AGENTS.md](../../AGENTS.md) for validation commands and [spec/spec.md](../../spec/spec.md) for the full specification.

## Style and lint

- **Formatter / linter:** Ruff (`make fmt`, `make lint`). Line length 88; target Python 3.12.
- **Types:** mypy strict (`make typecheck`). Avoid `Any` unless justified.

## API code

- Routers delegate to services; no direct DB access in handlers.
- Use `Depends(get_settings)` and `Depends(get_db)` from shared dependencies.
- Stable error responses via shared exception handlers (`packages/contracts/errors.py` patterns).

## Security

- No secrets in source; configuration only via `Settings` in `apps/api/src/config.py`.
- Follow [docs/security/secrets-management.md](../security/secrets-management.md).

## Related

- [PYTHON_PROCEDURES.md](../../PYTHON_PROCEDURES.md) (if present at repo root)
- `.cursor/rules/` — automated enforcement
