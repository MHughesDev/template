---
doc_id: "5.16"
title: "initialize repo"
section: "Procedures"
summary: "Initialize a repository from idea.md using the documentation-first AI flow, then seed queue items from generated docs."
updated: "2026-05-16"
---

# 5.16 — initialize repo

**Purpose:** Canonical initialization workflow for converting a completed `idea.md` into project documentation and an executable queue.

## Preconditions

- `idea.md` is complete and passes `make idea:validate`.
- Initialization has not already completed (`INIT_META.initialized: false`).
- Agent has completed mandatory skill search and read `skills/init/initialize-repo.md` and `skills/init/queue-seeder.md`.

## Exact commands

- `make idea:validate`
- `make docs:check`
- `make queue:validate`
- `make lint && make typecheck && make test` (if code changed)

## Ordered steps

1. Read `idea.md` fully, including open questions and constraints.
2. Run `make idea:validate`; stop if it fails.
3. Execute `skills/init/initialize-repo.md` to generate/update initialization docs.
4. Execute `skills/init/queue-seeder.md` to derive queue rows from generated docs.
   - `idea.md` §12 is optional prioritization input only.
5. Update `idea.md` INIT_META (`initialized`, `init_completed_at`, `init_branch`, `init_pr_url`) as applicable.
6. Run `make docs:check` and `make queue:validate`.
7. If any executable code changed, run `make lint`, `make typecheck`, `make test`.
8. Open one PR with evidence: files changed, commands run, outputs, risks, follow-ups.

## Expected outputs

- Initialization docs in `docs/` updated to project-specific, current state.
- Valid queue rows derived from docs.
- Initialization metadata updated in `idea.md`.
