# BRAINSTORM — Read-only ideation space

**Purpose:** A dedicated area for **thinking** about improvements and new features **without** treating this folder as a source of truth for implementation. Nothing in `docs/BRAINSTORM/` authorizes or requires code changes by itself.

## What this folder is

- **Read-only relative to the codebase:** Agents and humans should **not** implement features or edit production code **because** a file exists here. Implementation always flows through normal controls: queue, PRs, specs, and procedures.
- **Structured ideation:** Each idea is a separate Markdown file, filled from [`TEMPLATE-brainstorm.md`](TEMPLATE-brainstorm.md).
- **Durable and growable:** Brainstorm files are meant to be revised over time as understanding improves.

## What this folder is not

- Not a substitute for `spec/spec.md`, ADRs, or the CSV queue.
- Not an automatic trigger for CI or deploys.
- Not a place to paste secrets or credentials.

## Layout

| Path | Role |
|------|------|
| [`AGENTS.md`](AGENTS.md) | Agent contract: how to use this folder and the handoff pipeline |
| [`TEMPLATE-brainstorm.md`](TEMPLATE-brainstorm.md) | Copy this structure for each new brainstorm file |
| [`PIPELINE-from-brainstorm-to-queue.md`](PIPELINE-from-brainstorm-to-queue.md) | Generic steps from “ready to build” → queue rows → code → spec/docs updates |
| [`ideas/README.md`](ideas/README.md) | Where individual brainstorm files live and how to name them |

## Related links

- Queue: [`queue/QUEUE_INSTRUCTIONS.md`](../../queue/QUEUE_INSTRUCTIONS.md)
- Procedures index: [`docs/procedures/README.md`](../procedures/README.md)
