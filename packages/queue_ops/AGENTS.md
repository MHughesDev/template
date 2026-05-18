# packages/queue_ops/AGENTS.md

**Purpose:** Scoped agent instructions for queue CSV helpers.

## Scope

`packages.queue_ops` is **stdlib-only**: parsing and validation for `queue/queue.csv` and `queue/queuearchive.csv`. It is imported from `scripts/queue_top_item.py`, `scripts/queue_validate.py`, and unit tests.

## Rules

- Keep this package free of third-party dependencies.
- Align `OPEN_FIELDS`, validation rules, and JSON shape with `queue/QUEUE_INSTRUCTIONS.md` and `make queue:top-item` behavior.
- Prefer extending this module over duplicating CSV logic in scripts.
