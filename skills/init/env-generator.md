# skills/init/env-generator.md

<!-- BLUEPRINT: Composer 2 implements from this structure -->
<!-- CROSS-REFERENCES -->
<!-- - Machinery: skills/init/env-generator.py -->

> PURPOSE: Generate .env.example tailored to enabled profiles. Each profile adds its required env vars with documentation comments. Per spec §28.7 item 338.

## Purpose

> CONTENT: One paragraph. Each enabled profile requires specific environment variables. This skill generates a .env.example that includes exactly the variables needed for the enabled profiles, properly organized into sections with documentation comments.

## When to Invoke

> CONTENT: During initialization Phase 4 (Configure Profiles), after profile-resolver.md determines the resolved profile set.

## Prerequisites

> CONTENT: Profile resolution complete. skills/backend/env-var-sync.py available for post-generation verification.

## Relevant Files/Areas

> CONTENT: .env.example, apps/api/src/config.py, skills/init/env-generator.py

## Step-by-Step Method

> CONTENT: Numbered steps:
> 1. Run `python skills/init/env-generator.py --profiles web,ai_rag,workers > .env.example`
> 2. Review generated .env.example: verify all profile vars present with correct comments
> 3. Run `python skills/backend/env-var-sync.py` to verify sync with config.py
> 4. Update apps/api/src/config.py if new vars need Settings fields

## Command Examples

> CONTENT: `python skills/init/env-generator.py --profiles <comma-list>`, `python skills/backend/env-var-sync.py`

## Validation Checklist

> CONTENT:
> - [ ] All enabled profile vars present in .env.example
> - [ ] All vars have documentation comments
> - [ ] env-var-sync.py passes (code and .env.example in sync)

## Common Failure Modes

> CONTENT: Missing profile var → agents can't know what to set → deployment fails. Fix: always run env-var-sync.py after generating.

## Handoff Expectations

> CONTENT: .env.example updated, sync verified.

## Related Procedures

> CONTENT: docs/procedures/initialize-repo.md (Phase 4)

## Related Prompts

> CONTENT: prompts/profile_configurator.md

## Related Rules

> CONTENT: .cursor/rules/documentation.md (env var update triggers)

## Machinery

> CONTENT: `skills/init/env-generator.py` — generates .env.example content from enabled profiles. Invoke: `python skills/init/env-generator.py --profiles <list>`.
