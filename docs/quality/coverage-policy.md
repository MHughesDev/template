# docs/quality/coverage-policy.md

<!-- Per spec §26.5 items 183-186 -->

**Purpose:** Coverage floor definition and ratcheting mechanism.

## Overview

Coverage floor definition and ratcheting mechanism. See [AGENTS.md](../../AGENTS.md) for validation commands and [spec/spec.md](../../spec/spec.md) for the full specification.

<!-- coverage-floor: 55 -->
The default floor matches `fail_under` in `pyproject.toml` (pytest coverage). The `coverage-ratchet` skill may update this comment when coverage improves.
