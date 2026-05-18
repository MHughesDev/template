---
doc_id: "12.3"
title: "queue system overview"
section: "Queue"
summary: "Queue system conceptual overview: purpose, lifecycle, single-lane semantics, tooling."
updated: "2026-05-17"
---

# 12.3 — queue system overview

<!-- CROSS-REFERENCES -->
<!-- - Referenced by: queue/QUEUE_INSTRUCTIONS.md, docs/README.md -->
<!-- - Per spec §26.5 item 187 and §17 -->

**Purpose:** Queue system conceptual overview: purpose, lifecycle, single-lane semantics, tooling. Per spec §17 and §26.5 item 187.

## 12.3.1 Purpose

One paragraph. The queue is the agent work orchestration lane — NOT a product backlog or PM system. It coordinates agent execution in a controlled, auditable way with strict lifecycle rules that prevent work from being dropped or duplicated.

## 12.3.2 File Roles

Table explaining each queue file:
- queue/queue.csv — Open items; top row = active work item for single-lane processing. Each row includes **`context_files`** (read-only paths for context), **`touch_files`** (only paths an executor may modify), and other contract fields per **[QUEUE_INSTRUCTIONS.md](../../queue/QUEUE_INSTRUCTIONS.md)**.
- queue/queuearchive.csv — Historical record; append-only; completed/cancelled/superseded
- queue/QUEUE_INSTRUCTIONS.md — Human + agent SOP for all queue operations
- queue/QUEUE_AGENT_PROMPT.md — Executable behavior contract for agents processing queue items
- queue/queue.lock — Optional mutex preventing concurrent processing
- queue/audit.log — Append-only JSON lines emitted on archive; see §12.3.9 for format

## 12.3.3 Single-Lane Semantics

Explanation of the single-lane model: at most one processor claims the top row at a time. Top row = active item. Processors read the entire row and treat summary as the contract. Why: coordination between agents without complex locking.

When maintainers add new rows, ordering is dependency-first: insert a new row only after any open prerequisite rows listed in its `dependencies`. Batch/phase/FIFO conventions apply only after dependency ordering is satisfied.

## 12.3.4 Lifecycle States

Table per spec §17.3:
| State | Location | Transition Rules |
|-------|----------|-----------------|
| Open | queue.csv | Top row = next item |
| In Progress | queue.csv (notes column with branch info) | Document branch in notes |
| Blocked | queue.csv | Notes must explain blocker, owner, next step |
| Done | queuearchive.csv | Moved with status=done, completed_date, PR URL |
| Cancelled | queuearchive.csv | status=cancelled, reason in notes |
| Superseded | queuearchive.csv | status=superseded, successor ID in notes |

## 12.3.5 Branch Naming

Pattern: `queue/<id>-short-slug`. The queue ID is mandatory. PR must reference queue ID in title or body.

## 12.3.6 Queue Intelligence

Brief overview of the intelligence layer (§17.11): dependency DAG, complexity estimates, batch suggestions, conflict detection. Links to docs/queue/queue-intelligence.md for full conceptual docs.

## 12.3.7 Tooling

Table of queue-related make targets and their purpose:
- make queue:top-item — First open row as **one JSON line** (all columns; agents use this first)
- make queue:peek — Raw CSV: header + first row (read-only)
- make queue:validate — Schema + invariants
- make queue:archive — Move a row by id from open to archive
- make queue:archive-top — Move the **top** open row to archive (no id; token-friendly for single-lane)
- make queue:graph — Visualize dependency DAG
- make queue:analyze — Full queue intelligence analysis
- make queue:metrics — Summarize audit.log metrics (median time-to-merge, PR count, complexity distribution)

Equivalents without Make (e.g. Windows): **`python scripts/queue_top_item.py`** and **`python scripts/queue_validate.py`** from the repo root (they extend `sys.path` so **`packages.queue_ops`** imports resolve).

## 12.3.9 Audit Log Format (queue/audit.log)

On every archive operation, `scripts/queue_archive.py` appends a JSON line to `queue/audit.log`:

```json
{
  "queue_id": "Q-042",
  "batch": "migrations",
  "complexity": "M",
  "status": "done",
  "branch_created_at": "2026-05-10",
  "archived_at": "2026-05-15T09:30:00+00:00",
  "pr_url": "https://github.com/org/repo/pull/123",
  "review_rounds": 2
}
```

**Fields:**
- `queue_id` — Archived queue item ID
- `batch` — Batch assignment
- `complexity` — S/M/L/XL complexity estimate
- `status` — done/cancelled/superseded
- `branch_created_at` — Date from queue row (best-effort branch creation date)
- `archived_at` — ISO timestamp when archived
- `pr_url` — Extracted from queue notes if present
- `review_rounds` — Best-effort count from `gh pr view` (null if unavailable)

**Analysis:**
Run `make queue:metrics` to summarize:
- Median time-to-merge (days from creation to archive)
- Total PR count
- Complexity distribution
- Median review rounds

## 12.3.10 Python implementation (`packages/queue_ops`)

Validation and JSON shaping for **`make queue:top-item`** are implemented in **`packages/queue_ops`** (stdlib only). Scripts under **`scripts/`** import this package; unit tests live in **`packages/queue_ops/test_queue_ops.py`**. This replaces any historical pattern of a separate stdio “dev MCP” process for the same behavior — see **[local-setup.md](../development/local-setup.md)** §3.7.5.
