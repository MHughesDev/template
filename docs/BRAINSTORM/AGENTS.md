# BRAINSTORM — Agent contract (`docs/BRAINSTORM/AGENTS.md`)

**Purpose:** Rules for agents operating in `docs/BRAINSTORM/`. This file is scoped to this directory; it does not override root [`AGENTS.md`](../../AGENTS.md) on repository-wide policy.

## Instruction hierarchy (this folder)

1. Root [`AGENTS.md`](../../AGENTS.md)
2. This file (`docs/BRAINSTORM/AGENTS.md`)
3. [`PIPELINE-from-brainstorm-to-queue.md`](PIPELINE-from-brainstorm-to-queue.md) when moving from ideation to execution

## Read-only rule (critical)

- **Do not** edit `apps/`, `packages/`, `deploy/`, `queue/`, root `spec/spec.md`, or other implementation artifacts **solely** because a brainstorm file suggests it.
- **Do** use brainstorms as **input** to planning and to drafting **queue** items when the idea is explicitly marked ready for implementation (see pipeline doc).

Creating or editing files under `docs/BRAINSTORM/` is allowed; that is documentation of ideas, not product code.

## Creating a new brainstorm

1. Copy [`TEMPLATE-brainstorm.md`](TEMPLATE-brainstorm.md) to `docs/BRAINSTORM/ideas/<YYYY-MM-DD>-<short-slug>.md` (see [`ideas/README.md`](ideas/README.md)).
2. Fill every section; use `TBD` only where intentionally open.
3. Keep the file **structured** — add subsections under the template’s major headings rather than unstructured prose.

## Turning a brainstorm into work (summary)

When the brainstorm’s **Status** is set to **ready for implementation**:

1. Follow [`PIPELINE-from-brainstorm-to-queue.md`](PIPELINE-from-brainstorm-to-queue.md) end-to-end.
2. Use the queue as the execution lane: [`queue/QUEUE_INSTRUCTIONS.md`](../../queue/QUEUE_INSTRUCTIONS.md).
3. **Code first, then spec/docs:** implement and merge behavior per queue items, **then** update `spec/spec.md` and other docs to match (per pipeline step 6).

## Handoff

When leaving a brainstorm session, note in the brainstorm file (or queue notes) what changed and what remains open.
