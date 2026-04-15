# skills/agent-ops/idea-init-engine.md

<!-- CROSS-REFERENCES -->
<!-- - Procedure: docs/procedures/initialize-from-idea.md -->

## Purpose

Use the initialization engine to move from a completed `idea.md` to a deterministic
`init-manifest.json`, review resolved decisions, and execute scaffolding, profile stubs,
env updates, and queue seeding in one auditable pass.

## When to invoke

- At repository initialization time (first clone of the template for a real project)
- When troubleshooting a partial initialization (re-run after fixing scripts or `idea.md`)
- When adding a new profile to an already-initialized project (update `idea.md`, clear
  manifest per docs, re-run)

## Prerequisites

- `make idea:validate` passes with zero errors
- `idea.md` includes the INIT_META block with `initialized: false`
- Python 3.12+ and Docker/Compose available for profile scripts that patch Compose

## Relevant files/areas

- `idea.md` — intake form (structured tables and profile checkboxes)
- `scripts/idea-parser.py` — produces `init-manifest.json`
- `scripts/init-from-idea.py` — orchestrator
- `scripts/profiles/*.sh` — enable/discard profile hooks
- `queue/queue.csv` — seeded rows must match schema in `queue/QUEUE_INSTRUCTIONS.md`
- `docs/procedures/initialize-from-idea.md` — canonical SOP

## Step-by-step method

1. Fill required sections of `idea.md` (no `<!--` placeholders in sections 1, 3, 4, 6, 7, 9).
2. Answer every profile row with `[x] yes` or `[x] no` (or leave `[ ]` to accept archetype defaults in the parser).
3. Run `make idea:validate` and fix all errors.
4. Run `make idea:parse` and commit `init-manifest.json` as the audit trail.
5. Run `make idea:plan` to review stdout summary and optional JSON (dry-run prints manifest).
6. Run `make idea:execute` (or `make init:from-idea` for validate+parse+execute).
7. Review the generated PR; resolve open questions from `idea.md` §16 before building product features.

## Command examples

- `make idea:validate`
- `make idea:parse`
- `make idea:plan`
- `make idea:execute`
- `make init:from-idea`

## Validation checklist

- [ ] `make queue:validate`
- [ ] `make audit:self`
- [ ] `make test`
- [ ] `make lint`
- [ ] `init-manifest.json` committed with a clear hash in `meta`

## Common failure modes

- **Archetype not selected** — fix `idea.md` §3 so exactly one `[x]` appears in the Select column.
- **Profile checkbox invalid** — each row must be `[x] yes`, `[x] no`, or `[ ]` for archetype fill-in.
- **Module already exists** — orchestrator skips scaffolding; expected on re-run.
- **Queue validation fails** — check duplicate IDs or summaries under 100 characters in `queue/queue.csv`.
- **Pyproject.toml parse error after dependency append** — fix TOML manually; re-run orchestrator.

## Handoff expectations

- PR link (or manual instructions if `gh` is unavailable)
- `init_manifest_hash` from `init-manifest.json`
- List of open questions copied into the PR body

## Related procedures

- `docs/procedures/initialize-from-idea.md`

## Related prompts

- `prompts/repo_initializer.md`

## Related rules

- `.cursor/rules/global.md`
