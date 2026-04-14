# skills/init/archetype-mapper.md

<!-- CROSS-REFERENCES -->
<!-- - Machinery: skills/init/archetype-mapper.py -->
<!-- - Spec: §27.3 archetype-to-profile mapping -->

> PURPOSE: [FULL SKILL] Map idea.md archetype and profile selections to a concrete file scaffolding plan. Uses archetype-mapper.py machinery. Per spec §28.7 item 331.

## Purpose

> CONTENT: One paragraph. The archetype mapper translates the abstract idea description into a concrete list of files to create, modules to scaffold, profiles to enable, and queue categories to use. Its output is the initialization plan that subsequent skills execute.

## When to Invoke

> CONTENT: Second skill in initialization sequence (after idea-validator.md passes).

## Prerequisites

> CONTENT: idea-validator.md passed. idea.md completely read. spec §27.3 archetype-profile mapping table known.

## Relevant Files/Areas

> CONTENT: idea.md, skills/init/archetype-mapper.py, spec/spec.md §27.3

## Step-by-Step Method

> CONTENT: Numbered steps:
> 1. Read archetype selection from idea.md §3 (find the [x] checked row)
> 2. Apply default profile set from spec §27.3 archetype-profile mapping table
> 3. Override defaults with explicit selections from idea.md §5 (profile enable/disable)
> 4. Run archetype-mapper.py to generate the initialization plan JSON
> 5. Review the plan: modules, profiles, queue categories, files to create/modify
> 6. Document the plan (store in a draft file or PR description)

## Command Examples

> CONTENT: `python skills/init/archetype-mapper.py idea.md --output init-plan.json`

## Validation Checklist

> CONTENT:
> - [ ] Archetype identified
> - [ ] Default profiles applied per §27.3 table
> - [ ] Explicit profile overrides from §5 applied
> - [ ] Initialization plan generated with: modules, profiles, queue_categories, files
> - [ ] Plan documented

## Common Failure Modes

> CONTENT: Archetype not found (multiple selected or none selected) → validator should have caught this. If it slips through: fix idea.md §3.

## Handoff Expectations

> CONTENT: Initialization plan JSON or document produced, ready for profile-resolver.md and module-template-generator.md.

## Related Procedures

> CONTENT: docs/procedures/initialize-repo.md (Phase 1 — Validate and Plan)

## Related Prompts

> CONTENT: prompts/repo_initializer.md

## Related Rules

> CONTENT: .cursor/rules/initialization.md

## Machinery

> CONTENT: `skills/init/archetype-mapper.py` — reads idea.md, applies archetype-profile mapping per §27.3, generates JSON initialization plan. Invoke: `python skills/init/archetype-mapper.py idea.md`.
