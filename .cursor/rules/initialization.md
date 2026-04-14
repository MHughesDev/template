---
globs:
  - "idea.md"
  - "prompts/repo_initializer.md"
description: Rules active during repo initialization. Ensures the initializer follows the correct procedure and produces a complete initialization PR.
---

# .cursor/rules/initialization.md

<!-- BLUEPRINT: Composer 2 implements from this structure -->
<!-- CROSS-REFERENCES -->
<!-- - Referenced by: prompts/repo_initializer.md, docs/procedures/initialize-repo.md -->
<!-- - Skills: skills/init/ (all initialization skills) -->

> PURPOSE: Rules that constrain agent behavior specifically during repository initialization (the process of turning this template into a configured project). Ensures the initializer reads idea.md completely before acting, follows the 6-phase procedure, and produces a complete initialization PR. Per spec §28.5 item 295.

## Section: Pre-Initialization Requirements

> CONTENT: Rules that MUST be satisfied before any initialization action. Rules:
> 1. MUST read `idea.md` completely before creating or modifying any file
> 2. MUST run `make idea:validate` (or `scripts/validate-idea.sh`) to verify idea.md completeness
> 3. MUST NOT proceed if idea.md has unfilled placeholder sections (HTML comment placeholders remaining)
> 4. MUST NOT modify `spec/spec.md` during initialization — it is the authoritative spec, not a template
> 5. MUST produce an initialization plan (list of files to create/modify, profiles to enable, queue items to seed) before executing

## Section: Six-Phase Procedure Enforcement

> CONTENT: Rules enforcing adherence to the spec §27.4 six-phase initialization procedure. Rules:
> 1. Phase 1 (Validate and Plan) MUST complete before any file creation
> 2. Phase 2 (Configure Root) runs before Phase 3 (Scaffold Domain)
> 3. Phase 4 (Configure Profiles) runs after all domain modules are scaffolded
> 4. Phase 5 (Seed Queue) is the last configuration step before validation
> 5. Phase 6 (Validate and Handoff) MUST include: `make lint`, `make typecheck`, `make test`, `make audit:self`
> 6. Checkpoint commands at each phase boundary — do not proceed to next phase if checks fail

## Section: Initialization PR Requirements

> CONTENT: Rules for the initialization PR that the agent must produce. Rules:
> 1. PR title: `chore: initialize repository from idea.md — <project-name>`
> 2. PR description MUST include: idea.md archetype selected, profiles enabled, modules scaffolded, queue items created, all validation commands run with output
> 3. PR MUST be opened against `main` branch as a PR (not direct push)
> 4. ALL CI checks must pass on the initialization PR before it can be merged
> 5. The initialization PR is the ONLY acceptable way to deliver initialization — no "drive-by" commits to main

## Section: Immutable Files During Initialization

> CONTENT: Files that MUST NOT be modified during initialization. Rules:
> 1. `spec/spec.md` — authoritative specification; never modified by initialization agent
> 2. `spec/IMPLEMENTATION_PLAN.md` — implementation checklist; not part of initialization output
> 3. `PYTHON_PROCEDURES.md` — Python coding procedures; not project-specific
> 4. `.github/` CI configuration — initialization may ADD env vars but must not change CI logic
> 5. `skills/` and `prompts/` — these are the agent library; not modified during initialization (only consumed)
