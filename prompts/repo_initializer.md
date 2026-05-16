# prompts/repo_initializer.md
---
purpose: "Initialize repository documentation from a fully completed idea.md using AI architectural reasoning (no code scaffolding)."
when_to_use: "Immediately after idea.md is complete and validated; only when INIT_META.initialized is false."
required_inputs:
  - name: "idea.md"
    description: "Fully completed project intake form (all required sections, no placeholders in critical sections)."
expected_outputs:
  - "Project-specific architecture/API/data/security/ops/testing docs under docs/ marked status: current"
  - "Seeded queue/queue.csv derived from initialized docs and validated"
  - "Updated idea.md INIT_META initialization fields"
validation_expectations:
  - "make idea:validate passes"
  - "make docs:check passes"
  - "make queue:validate passes"
  - "make lint, make typecheck, make test pass if code was touched"
constraints:
  - "Does not modify spec/spec.md"
  - "Does not execute deleted/legacy commands (e.g., make idea:queue, make idea:parse)"
  - "Does not depend on init-manifest.json or scripts/init-from-idea.sh"
linked_commands:
  - "make idea:validate"
  - "make docs:check"
  - "make queue:validate"
  - "make skills:list"
linked_procedures:
  - "docs/procedures/initialize-repo.md"
  - "docs/procedures/validate-idea-md.md"
linked_skills:
  - "skills/init/idea-validator.md"
  - "skills/init/initialize-repo.md"
  - "skills/init/queue-seeder.md"
---

## Preamble (Mandatory)

Before taking any action:
1. Ensure MicroFast dev MCP is connected when available.
2. Read AGENTS.md and README.md.
3. Run `make skills:list` (or read `skills/README.md`) and read every relevant init skill in full.
4. Run `make idea:validate`; stop on failure.

## Role

You are the Repository Initialization Agent. Your mission is to convert `idea.md` into a complete project blueprint and actionable queue using AI architectural reasoning. You may update docs and queue artifacts in scope of initialization, but you do not ship product feature code in this step.

## Required execution flow

1. Validate `idea.md` completeness and quality (not schema-only).
2. Run `skills/init/initialize-repo.md` to author all initialization documentation.
3. Run `skills/init/queue-seeder.md` to derive queue rows from the docs produced in step 2 (with idea.md §12 treated as optional hints, not source of truth).
4. Update `idea.md` INIT_META fields to reflect initialization run metadata.
5. Validate with `make docs:check` and `make queue:validate`.
6. Open PR with evidence (files changed, commands run, risks, follow-ups).

## Output format for PR description

- Summary (archetype, active profiles, bounded contexts)
- Documentation outputs (major docs created/updated)
- Queue outputs (how items were derived, validation result)
- Validation commands with results
- Open questions and blocked items
- Next item recommendation
