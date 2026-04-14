# skills/init/env-generator.md

<!-- CROSS-REFERENCES -->
<!-- - Machinery: skills/init/env-generator.py -->

**Purpose:** Generate .env.example tailored to enabled profiles. Each profile adds its required env vars with documentation comments. Per spec §28.7 item 338.

## Purpose

One paragraph. Each enabled profile requires specific environment variables. This skill generates a .env.example that includes exactly the variables needed for the enabled profiles, properly organized into sections with documentation comments.

## When to Invoke

During initialization Phase 4 (Configure Profiles), after profile-resolver.md determines the resolved profile set.

## Prerequisites

Profile resolution complete. skills/backend/env-var-sync.py available for post-generation verification.

## Relevant Files/Areas

.env.example, apps/api/src/config.py, skills/init/env-generator.py

## Step-by-Step Method

Numbered steps:
1. Run `python skills/init/env-generator.py --profiles web,ai_rag,workers > .env.example`
2. Review generated .env.example: verify all profile vars present with correct comments
3. Run `python skills/backend/env-var-sync.py` to verify sync with config.py
4. Update apps/api/src/config.py if new vars need Settings fields

## Command Examples

`python skills/init/env-generator.py --profiles <comma-list>`, `python skills/backend/env-var-sync.py`

## Validation Checklist

- [ ] All enabled profile vars present in .env.example
- [ ] All vars have documentation comments
- [ ] env-var-sync.py passes (code and .env.example in sync)

## Common Failure Modes

Missing profile var → agents can't know what to set → deployment fails. Fix: always run env-var-sync.py after generating.

## Handoff Expectations

.env.example updated, sync verified.

## Related Procedures

docs/procedures/initialize-repo.md (Phase 4)

## Related Prompts

prompts/profile_configurator.md

## Related Rules

.cursor/rules/documentation.md (env var update triggers)

## Machinery

`skills/init/env-generator.py` — generates .env.example content from enabled profiles. Invoke: `python skills/init/env-generator.py --profiles <list>`.
