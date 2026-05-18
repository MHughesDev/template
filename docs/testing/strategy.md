---
doc_id: "11.3"
title: "testing strategy"
section: "Quality"
status: "pending-init"
summary: "Testing strategy — pyramid, what to test at each level, when to add tests, and coverage policy. Populated during initialization from IDEA.md §15."
updated: "2026-05-17"
---

# Testing Strategy
<!-- derived from: IDEA.md §15 — populated by repo_initialize -->

## Test pyramid

| Level | Tools | Coverage target |
|-------|-------|-----------------|
| Unit | pytest | _[70%]_ |
| Integration | pytest + TestClient | _[Key flows]_ |
| E2E | Playwright | _[Critical paths]_ |

## What to test

### Unit tests
- _[Business logic]_
- _[Utility functions]_

### Integration tests
- _[API endpoints]_
- _[Database operations]_

### E2E tests
- _[User workflows]_

## Coverage policy

_[Coverage ratcheting rules]_

_[This section is populated by `skills/init/repo_initialize.md` during repository initialization.]_
