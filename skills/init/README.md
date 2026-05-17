# skills/init/README.md

**Purpose:** Index for initialization skills. Repository initialization is driven by a **single canonical skill** that an AI agent runs after a developer has filled out `idea.md` end-to-end.

## When to invoke

- A developer has filled out `idea.md` end-to-end (every applicable section, with `N/A` where appropriate).
- The repo's baseline full-stack app (`apps/api/` + `apps/web/`) is in place and is the substrate for the product.

## Prerequisites

- Read root `AGENTS.md`, `apps/api/AGENTS.md`, `apps/web/AGENTS.md`.
- Read `idea.md` end-to-end before opening the skill.
- Read `queue/QUEUE_INSTRUCTIONS.md` — every row this initialization creates must conform to its schema.

## Skills in this category

| Skill | Purpose |
|-------|---------|
| [`repo_initialize.md`](repo_initialize.md) | Documentation-first, queue-first initialization: read `idea.md`, refresh spec + design docs, seed MVP queue rows, surface open questions as blocked rows. |

## Invocation flow

1. Developer fills out `idea.md` end-to-end.
2. AI agent runs `skills/init/repo_initialize.md`.
3. Output: refreshed spec/docs + initial MVP queue rows + open-question rows for anything ambiguous. **No product code is written by initialization.**

There is no `make idea:*` command. There is no multi-skill phased pipeline. There is one input (`idea.md`), one procedural skill (`repo_initialize.md`), and one output set (docs + queue rows).

## Related resources

- Input contract: [`/idea.md`](../../idea.md)
- Invocation prompt: [`prompts/repo_initializer.md`](../../prompts/repo_initializer.md)
- Queue lifecycle: [`queue/QUEUE_INSTRUCTIONS.md`](../../queue/QUEUE_INSTRUCTIONS.md)
- Founding ADR: [`docs/adr/0001-initial-template-architecture.md`](../../docs/adr/0001-initial-template-architecture.md)
