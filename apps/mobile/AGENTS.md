# apps/mobile/AGENTS.md

<!-- Per spec §26.8 item 235 — optional mobile profile -->

> PURPOSE: Scoped agent instructions for mobile development (Expo/React Native). Per spec §26.8 item 235.

## Scope

> CONTENT: Active only when mobile profile is enabled. Root AGENTS.md remains supreme.

## Framework Conventions

> CONTENT: Expo/React Native conventions. Reference skills/frontend/expo-auth-storage.md for auth token handling. Filled during profile enablement.

## Auth Storage Patterns

> CONTENT: Use Expo SecureStore for tokens. Never AsyncStorage for secrets. Reference skills/frontend/expo-auth-storage.md.

## Testing

> CONTENT: Jest + Expo testing patterns. API contract tests via skills/testing/api-contract-testing.md.

## Build and Deploy

> CONTENT: EAS Build configuration. iOS/Android target platforms per idea.md §5.
