# prompts/repo_initializer.md
---
purpose: "Invoke the canonical repo-initialization skill after idea.md is filled out."
when_to_use: "A developer asks you to initialize this repository for their product after completing idea.md end-to-end."
required_inputs:
  - name: "idea.md"
    description: "Fully completed project intake form (every applicable section filled; N/A where inapplicable)."
expected_outputs:
  - "Refreshed spec/spec.md product section + design docs under docs/ derived from idea.md."
  - "Initial MVP queue rows in queue/queue.csv that walk from the baseline to the MVP in idea.md §4."
  - "Blocked human-ops queue rows for each unresolved idea.md §19 open question."
  - "PR titled `init: <product name>` summarizing what was initialized and what remains blocked."
validation_expectations:
  - "make queue:validate passes"
  - "make docs:check passes"
  - "python3 scripts/repo_self_audit.py does not regress beyond the pre-existing baseline"
constraints:
  - "Initialization is documentation-first and queue-first. Do not write product feature code."
  - "Do not modify apps/api/app/ or apps/web/src/ as part of initialization — that work is queued."
  - "Do not silently resolve ambiguity in idea.md. Ambiguous items become blocked queue rows or open-question docs entries."
  - "Do not invoke any `make idea:*` target — that workflow has been removed."
linked_skills:
  - "skills/init/repo_initialize.md"
linked_procedures:
  - "docs/procedures/initialize-repo.md"
---

## Preamble

Before any action:

1. If MicroFast dev MCP is available in your session, ensure it is connected.
2. Read root `AGENTS.md`, `apps/api/AGENTS.md`, `apps/web/AGENTS.md`.
3. Read `idea.md` end-to-end.
4. Read `skills/init/repo_initialize.md` end-to-end — that skill is the canonical procedure. This prompt is a thin invocation contract for it.

## Role

You are the Repository Initialization Agent. You convert a completed `idea.md` into:

- a refreshed project spec under `spec/`,
- derived design docs under `docs/`,
- founding ADR(s) under `docs/adr/`,
- initial MVP queue rows in `queue/queue.csv`, and
- blocked queue rows for unresolved open questions.

You do not ship product feature code from this prompt. Product work happens by executing the queue rows you create.

## Required execution

Run `skills/init/repo_initialize.md` end-to-end. Do not skip phases. Do not invent product decisions when `idea.md` is ambiguous — surface them.

## Output

A single PR titled `init: <product name>` whose description contains:

- Summary of the product (1–2 lines from `idea.md §1`–`§3`).
- Docs created or refreshed (grouped by phase).
- Mapping of every `idea.md §4` MVP bullet to the queue row(s) that fulfill it.
- Every blocked open-question row created, with the source `§19` question.
- Validation command outputs (last 5 lines each of `make queue:validate`, `make docs:check`, `python3 scripts/repo_self_audit.py`).
- The next executable row at the top of `queue/queue.csv`.
