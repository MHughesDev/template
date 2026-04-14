# skills/repo-governance/docs-generator.md

<!-- CROSS-REFERENCES -->
<!-- - Machinery: skills/repo-governance/docs-generator.py -->
<!-- - Conceptual docs: docs/development/docs-generation.md -->
<!-- - Make targets: make docs:generate, make docs:check -->

**Purpose:** [FULL SKILL] How to run, extend, and maintain the documentation generation pipeline. Covers adding new source→target mappings, running locally, and CI integration. Per spec §9.4 and §26.12 item 356-357.

## Purpose

One paragraph. The documentation generation pipeline automatically produces Markdown documentation from authoritative sources (FastAPI OpenAPI, Pydantic Settings, pyproject.toml, Compose, K8s YAML, Makefile). This prevents documentation drift — the most common failure mode in agentic repos. When sources change, docs update automatically via `make docs:generate` and CI catches drift with `make docs:check`.

## When to Invoke

- After any change to a source file that has a corresponding generated doc target
- To add a new source→target mapping to the pipeline
- When `make docs:check` fails in CI (regenerate and commit)
- On release preparation (ensure all docs are fresh)

## Prerequisites

FastAPI app can be imported (make migrate applied, .env set). Python 3.12+ with venv activated.

## Relevant Files/Areas

- `skills/repo-governance/docs-generator.py` — the engine (read this before extending)
- `scripts/docs-generate.sh` → `make docs:generate`
- `scripts/docs-check.sh` → `make docs:check`
- `docs/development/docs-generation.md` — human-readable docs about the pipeline

## Step-by-Step Method — Running

Numbered steps for running the pipeline:
1. `make docs:generate` — regenerate all docs from source
2. Review changed files: `git diff docs/`
3. If expected changes: commit with `docs: regenerate from source`
4. `make docs:check` — verify no drift (should pass after generate + commit)

## Step-by-Step Method — Extending

Numbered steps for adding a new source→target mapping:
1. Read the TARGETS list in docs-generator.py completely
2. Write a new generator function: `generate_<name>() -> str`
   - Parse the source file(s)
   - Format as token-efficient Markdown (tables preferred over prose)
   - Add source annotation comment
3. Register a new DocTarget in TARGETS with source_paths and target_path
4. Run `make docs:generate` to test the new generator
5. Run `make docs:check` to verify it produces stable output
6. Update `docs/development/docs-generation.md` with the new mapping

## Command Examples

- `make docs:generate` — generate all docs
- `make docs:check` — check for drift (CI mode)
- `python skills/repo-governance/docs-generator.py --generate` — generate only
- `python skills/repo-governance/docs-generator.py --check` — check only
- `python skills/repo-governance/docs-generator.py --generate --target env-vars` — specific target

## Validation Checklist

- [ ] make docs:generate runs without error
- [ ] make docs:check passes (no drift)
- [ ] New generator produces valid Markdown
- [ ] Source annotations present in generated sections
- [ ] docs/development/docs-generation.md updated if new mapping added

## Common Failure Modes

- **App import error**: generator can't import FastAPI app → endpoint docs fail. Fix: ensure PYTHONPATH includes apps/api/src.
- **Drift in CI**: generated docs on disk are stale → run make docs:generate locally and commit.
- **Generator produces unstable output**: timestamps or sort order varies → use deterministic formatting.

## Handoff Expectations

All generated docs committed, make docs:check passes, new mapping documented.

## Related Procedures

docs/procedures/update-documentation.md, docs/development/docs-generation.md

## Related Prompts

prompts/documentation_updater.md

## Related Rules

.cursor/rules/documentation.md (doc update triggers)

## Machinery

`skills/repo-governance/docs-generator.py` — the complete generation engine. Supports --generate and --check modes. See file docstring for full API. Invoked by `scripts/docs-generate.sh` and `scripts/docs-check.sh`.
