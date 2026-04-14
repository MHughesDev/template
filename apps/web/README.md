# apps/web/README.md

<!-- BLUEPRINT: Composer 2 implements from this structure -->
<!-- Per spec §26.8 item 232 — optional web profile placeholder -->

> PURPOSE: Web frontend placeholder. Documents when/how to enable this profile. Per spec §26.8 item 232.

## Status: Placeholder

> CONTENT: This directory is a placeholder for the optional web frontend profile. It contains no application code — the web frontend has not been initialized.

## When to Enable

> CONTENT: Enable this profile when the project requires a browser-based user interface. See idea.md §5 and docs/optional-clients/web.md for the full decision guide.

## Setup Instructions

> CONTENT: To enable the web frontend profile:
> 1. Fill out idea.md §5 (web: yes) if not already done
> 2. Run: `make profile:enable PROFILE=web`
> 3. Follow the steps in docs/procedures/add-optional-app-profile.md

## Link to Full Docs

> CONTENT: See docs/optional-clients/web.md for: when to enable, when not to enable, prerequisites, setup steps, environment variables, and operational burden.
