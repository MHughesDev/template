# docs/development/dependency-management.md

<!-- CROSS-REFERENCES -->
<!-- - Referenced by: docs/development/README.md, README.md -->

**Purpose:** How Python dependencies are declared, upgraded, and reviewed in this repo.

## Overview

How Python dependencies are declared, upgraded, and reviewed in this repo. See [AGENTS.md](../../AGENTS.md) for validation commands and [spec/spec.md](../../spec/spec.md) for the full specification.

## Where dependencies live

- **Runtime and dev:** `pyproject.toml` (`[project.dependencies]` and `[project.optional-dependencies] dev`).
- **Locking:** Use committed constraints in `pyproject.toml`; pin major upgrades deliberately.

## Upgrade workflow

1. Edit version constraints in `pyproject.toml`.
2. Reinstall: `pip install -e ".[dev]"`.
3. Run `make lint`, `make typecheck`, `make test`.
4. Run `make security-scan` / `make security:scan` for dependency-related security review.
5. Document notable upgrades in `CHANGELOG.md` when behavior or operators are affected.

## Related

- [docs/procedures/dependency-upgrade.md](../procedures/dependency-upgrade.md)
- [skills/security/dependency-review.md](../../skills/security/dependency-review.md)
