---
doc_id: "2.12"
title: "async workers"
section: "Architecture"
status: "pending-init"
summary: "Every async task: trigger, payload shape, retry policy, failure handling, and idempotency approach. Populated during initialization from IDEA.md §12 when background work is enabled."
updated: "2026-05-17"
---

# Async Workers
<!-- derived from: IDEA.md §12 — populated by repo_initialize -->

## Worker infrastructure

_[e.g., Celery with Redis broker]_

## Task inventory

| Task | Trigger | Retry | Idempotency |
|------|---------|-------|-------------|
| _[Task 1]_ | _[Event/schedule]_ | _[3x exponential]_ | _[Key: user_id + timestamp]_ |
| _[Task 2]_ | _[Event]_ | _[5x linear]_ | _[Key: job_id]_ |

## Failure handling

_[What happens when tasks fail permanently? e.g., Dead letter queue, alerting, manual retry]_

_[This section is populated by `skills/init/repo_initialize.md` during repository initialization when background workers are enabled.]_
