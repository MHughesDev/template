---
globs:
  - "skills/**"
description: Rules for skill files. Ensures skills follow the §6.2 structure, include machinery code where applicable, and cross-reference procedures/prompts/rules.
---

# .cursor/rules/skills.md

<!-- BLUEPRINT: Composer 2 implements from this structure -->
<!-- CROSS-REFERENCES -->
<!-- - Referenced by: docs/procedures/update-or-create-skill.md -->
<!-- - Validation: skills/repo-governance/rule-linter.py -->

> PURPOSE: Rules governing skill file content and structure. Ensures every skill in skills/ follows the spec §6.2 required structure, machinery code is referenced and tested, and skills cross-reference related procedures/prompts/rules. Per spec §28.5 item 296.

## Section: Required Sections Rule

> CONTENT: Rules about mandatory section headings in skill files. Rules:
> 1. Every skill `.md` file MUST contain these sections (in order): Purpose, When to invoke, Prerequisites, Relevant files/areas, Step-by-step method, Command examples, Validation checklist, Common failure modes, Handoff expectations, Related procedures, Related prompts, Related rules
> 2. Stub skills may have `TODO` as section body but MUST have all headings present
> 3. Full skills (≥10 required per spec §6.1) have all sections with production-usable content
> 4. Steps must be numbered, actionable, and use exact `make` target names where applicable
> 5. Validation checklist uses `- [ ]` checkbox format

## Section: Machinery Code Reference Rule

> CONTENT: Rules about skill machinery files. Rules:
> 1. Skills with supporting code (`.py` files) MUST have a `## Machinery` section in the `.md` file
> 2. The `## Machinery` section must: name the file, explain what it does, show how to invoke it
> 3. Machinery code MUST begin with the file title comment per §1.7
> 4. Machinery code MUST follow PYTHON_PROCEDURES.md (typed, boundary-validated, testable)
> 5. Machinery invoked by Make targets must be documented in both the skill and scripts/README.md

## Section: Cross-Reference Requirements

> CONTENT: Rules for cross-referencing between skills and other artifacts. Rules:
> 1. Every skill MUST list at least one related procedure in `docs/procedures/`
> 2. Every skill MUST list at least one related prompt in `prompts/` OR state "No specific prompt — use generic implementation_agent"
> 3. Every skill MUST list applicable cursor rules in `.cursor/rules/`
> 4. Skills index (`skills/README.md`) MUST be updated when a new skill is added
> 5. When a skill is updated, verify that all cross-references are still accurate
