# skills/init/archetype-mapper.md

**Status:** Deprecated as a deterministic workflow.

## Purpose

Historical reference for archetype/profile heuristics only. In the current initialization model, AI architectural reasoning in `skills/init/initialize-repo.md` is authoritative.

## When to Invoke

- Optional lookup only, when you need quick archetype/profile hints.
- Do **not** treat this skill as a required execution step.

## Prohibited usage

- Do not run deterministic init orchestration from this skill.
- Do not block initialization on this skill's scripts/tables.

## Source of truth

- `skills/init/initialize-repo.md`
- `prompts/repo_initializer.md`
- `docs/procedures/initialize-repo.md`
