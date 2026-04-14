# skills/frontend/frontend-env-handling.md

<!-- CROSS-REFERENCES -->
<!-- - Profile: optional web/mobile profile -->
<!-- - Related docs: docs/optional-clients/ -->

> PURPOSE: [OPTIONAL] Frontend/mobile skill. Enable the web or mobile profile before relying on this.

## Purpose
> CONTENT: What this frontend skill enables.

## When to Invoke
> CONTENT: When web or mobile profile is active.

## Prerequisites
> CONTENT: Profile enabled, Node.js/Expo installed.

## Relevant Files/Areas
> CONTENT: apps/web/ or apps/mobile/, docs/optional-clients/

## Step-by-Step Method
> CONTENT: Use `.env` / `app.config` for public API URL only; never embed secrets in client bundles.

## Command Examples
> CONTENT: `EXPO_PUBLIC_API_URL=http://localhost:8000`

## Validation Checklist
> CONTENT:
> - [ ] Frontend/mobile connects to API
> - [ ] Auth flow works end-to-end

## Common Failure Modes
> CONTENT: CORS configuration, auth token storage.

## Handoff Expectations
> CONTENT: Frontend connected, tested.

## Related Procedures
> CONTENT: docs/procedures/add-optional-app-profile.md

## Related Prompts
> CONTENT: prompts/profile_configurator.md

## Related Rules
> CONTENT: .cursor/rules/security.md
