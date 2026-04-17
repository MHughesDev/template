# .cursor/commands/queue-next.md

Claim and start the **current** queue item (top row) in single-lane mode.

| Field | Value |
|-------|--------|
| **Name** | Queue next |
| **Description** | Read **`queue/queue.csv`**, verify dependencies, branch, plan, then implement per SOP. |
| **When to use** | Starting new queue work after the previous item is archived or not in progress. |
| **Procedure** | [`docs/procedures/start-queue-item.md`](../docs/procedures/start-queue-item.md) |
| **Skill** | [`skills/agent-ops/queue-triage.md`](../skills/agent-ops/queue-triage.md) |
| **Read-only helper** | **`make queue:top-item`** (one JSON line — full row); optional `make queue:peek` (raw CSV) |

## Steps

1. Run **`make queue:top-item`** — parse the **JSON** line; every column is present; **`summary`** is the contract.
2. Parse **`dependencies`** — every listed ID must be **done** in **`queuearchive.csv`** (or empty).
3. If blocked: update **`notes`** with reason and next step; **stop**.
4. Run **`make queue:validate`** before modifying queue files.
5. Create branch **`git checkout -b queue/<id>-short-slug`** including the queue **`id`**.
6. Mandatory skill search: **`make skills:list`**, read relevant skills fully.
7. Write a plan: files, acceptance criteria, risks, **out-of-scope** — paste into PR draft or queue **`notes`**.
8. Implement per [`docs/procedures/implement-change.md`](../docs/procedures/implement-change.md).

## Expected output

- Branch **`queue/<id>-...`**
- Written plan aligned with the **`summary`** column
- No work started on blocked dependencies
