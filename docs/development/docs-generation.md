---
doc_id: "3.3"
title: "docs generation"
section: "Development"
summary: "How the docs pipeline works and how to extend it."
updated: "2026-04-17"
---

# 3.3 — docs generation

<!-- CROSS-REFERENCES -->
<!-- - Referenced by: docs/development/README.md, README.md -->

**Purpose:** How the docs pipeline works and how to extend it.

## 3.3.1 Overview

How the docs pipeline works and how to extend it. See [AGENTS.md](../../AGENTS.md) for validation commands and [spec/spec.md](../../spec/spec.md) for the full specification.

## 3.3.2 Commands

| Command | Role |
|---------|------|
| `make docs-generate` / `make docs:generate` | Runs `scripts/docs-generate.sh` — regenerates derived docs (e.g. OpenAPI-derived Markdown when wired) |
| `make docs-check` / `make docs:check` | Runs `scripts/docs-check.sh` — link and drift checks for documentation |

## 3.3.3 Workflow

1. Change source artifacts (FastAPI routes, `pyproject.toml`, etc.) as needed.
2. Run `make docs-generate` and commit any updated generated files.
3. Run `make docs-check` before pushing doc-heavy PRs.

## 3.3.4 Related

- [skills/repo-governance/docs-generator.md](../../skills/repo-governance/docs-generator.md)
- [docs/api/endpoints.md](../api/endpoints.md) — endpoint catalog (regenerate when routes change)
