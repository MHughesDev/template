# skills/init/profile-resolver.md

<!-- CROSS-REFERENCES -->
<!-- - Machinery: skills/init/profile-resolver.py -->
<!-- - Related: skills/init/archetype-mapper.py -->

> PURPOSE: Resolve profile enablement from idea.md §5 and archetype defaults. Handles conflicts and dependencies between profiles. Per spec §28.7 item 336.

## Purpose

> CONTENT: One paragraph. Profile resolution combines the archetype default profiles with explicit selections in idea.md §5, then validates that profile dependencies are met (e.g., billing requires auth and multi-tenancy for SaaS) and flags conflicts. The resolved profile set is the authoritative input for configuration steps.

## When to Invoke

> CONTENT: During initialization Phase 4 (Configure Profiles), after archetype-mapper.md produces the initialization plan.

## Prerequisites

> CONTENT: archetype-mapper.py plan available. idea.md §5 read. Profile dependency rules understood.

## Relevant Files/Areas

> CONTENT: idea.md §5, skills/init/profile-resolver.py, docker-compose.yml (profiles to enable)

## Step-by-Step Method

> CONTENT: Numbered steps:
> 1. Run `python skills/init/profile-resolver.py idea.md`
> 2. Review resolved profile set: which profiles are enabled after dependencies and overrides
> 3. Review any warnings (conflicts, implicit enablement of dependency profiles)
> 4. For each enabled profile: run `make profile:enable <profile>`
> 5. Verify docker-compose.yml updated, .env.example updated, package stubs created

## Command Examples

> CONTENT: `python skills/init/profile-resolver.py idea.md`, `make profile:enable web`

## Validation Checklist

> CONTENT:
> - [ ] All enabled profiles satisfy their dependencies
> - [ ] No conflicts between profiles
> - [ ] Resolved profile set matches human's intent
> - [ ] Each enabled profile configured (docker-compose, .env.example)

## Common Failure Modes

> CONTENT: Billing profile enabled without multi-tenancy → resolver should warn. Fix: enable multi-tenancy or reconsider billing profile.

## Handoff Expectations

> CONTENT: Resolved profile set documented, each profile configured.

## Related Procedures

> CONTENT: docs/procedures/enable-profile.md

## Related Prompts

> CONTENT: prompts/profile_configurator.md

## Related Rules

> CONTENT: .cursor/rules/initialization.md

## Machinery

> CONTENT: `skills/init/profile-resolver.py` — resolves profile enablement with dependency checking and conflict detection. Invoke: `python skills/init/profile-resolver.py idea.md`.
