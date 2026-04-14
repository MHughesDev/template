# apps/web/AGENTS.md

<!-- Per spec §26.8 item 233 — optional web profile -->

> PURPOSE: Scoped agent instructions for web frontend development. Per spec §26.8 item 233.

## Scope

> CONTENT: This AGENTS.md is active only when the web frontend profile is enabled. It supplements root AGENTS.md with web-specific conventions. The root AGENTS.md remains supreme for all repo-wide policy.

## Framework Conventions

> CONTENT: Framework-specific conventions to be filled during profile enablement based on idea.md §3 (archetype) and chosen framework (e.g., Next.js, Vite+React). Fill conventions when enabling the web profile from idea.md.

## API Integration Patterns

> CONTENT: Reference skills/frontend/react-api-integration.md for API integration patterns. Key points: use generated API client from OpenAPI spec, handle auth token storage per skills/frontend/expo-auth-storage.md, propagate correlation IDs.

## Testing

> CONTENT: Frontend testing conventions. Reference skills/testing/pytest-conventions.md for API contract tests. Frontend unit tests: vitest or jest conventions documented here after initialization.

## Build and Deploy

> CONTENT: Build process and deployment notes. Reference docs/operations/docker.md for containerization. Frontend environment variables per skills/frontend/frontend-env-handling.md.
