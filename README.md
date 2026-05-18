<!-- README.md -->

# Template: The AI Software Factory

Build new products faster without re-litigating the same setup decisions every time.

This repository is a production-ready full-stack baseline (`FastAPI` + `React`) plus an agent operating system (`AGENTS.md`, skills, prompts, and queue workflows) designed to turn an idea into execution-ready work.

If you want fewer repeated setup prompts, fewer "what file should I touch?" loops, and cleaner agent handoffs, this is the point.

---

## What You Actually Get

- A working backend in `apps/api/` with auth, models, migrations, tests, and API routes.
- A working frontend in `apps/web/` with typed client generation and test scaffolding.
- A queue-driven execution model in `queue/` so work is decomposed, auditable, and parallel-ready.
- A skill and prompt library in `skills/` and `prompts/` so agents follow reusable workflows instead of making them up.
- Repo governance built in: validations, docs mapping, self-audit checks, and CI workflows.

---

## Two Modes of Use

### 1) Build a Product from This Template

1. Fill out `idea.md` completely.
2. Ask an agent to run `skills/init/repo_initialize.md`.
3. Review generated docs/spec/queue output.
4. Execute queue items from top to bottom.

Important: initialization is docs-first and queue-first. It does not directly write product feature code.

### 2) Improve the Template Itself

Use the queue in `queue/queue.csv` to ship reusable upgrades that save time/tokens for future projects (scripts, defaults, docs, automation, guardrails).

---

## Required Flow for Coding Agents

Before implementation work in this repo:

1. Ensure `microfast-dev` MCP is connected (when available).
2. Read `README.md` (this file).
3. Read `AGENTS.md` fully (authoritative policy).
4. Perform mandatory skill search via `skills/README.md` or `make skills:list`.
5. Use queue procedures from `queue/QUEUE_INSTRUCTIONS.md`.

If policy is unclear, re-read `AGENTS.md` before proceeding.

---

## Quickstart

### Prerequisites

- Python 3.12+
- Docker + Docker Compose
- Bun
- Git
- Make (or command alternatives in `scripts/`)

### Local Bootstrap

```bash
git clone <your-repo-url>
cd <your-repo-folder>
make init
```

### Run Stack

```bash
make docker-up
make health-check
```

### Run Components Separately

```bash
make dev-api
make dev-web
```

### Quality Commands

```bash
make lint
make fmt
make typecheck
make test
make docs:check
make queue:validate
make audit:self
```

---

## Core Queue Commands

```bash
make queue:top-item
make queue:peek
make queue:validate
make queue:graph
make queue:analyze
```

- `queue:top-item` returns the active non-human-ops row as JSON.
- `queue:validate` is required after queue edits.
- Executor agents should not mutate queue ledgers directly unless explicitly acting as operator.

---

## Initialization Flow (Token-Saving Version)

```text
idea.md -> skills/init/repo_initialize.md -> spec/docs refresh -> queue seed -> execution
```

Why this matters:

- You capture intent once in `idea.md`.
- Agents generate structured artifacts once.
- Implementation then follows queue rows with explicit constraints and acceptance criteria.

That means less repeated "re-explain the project" overhead in every chat.

---

## Project Structure

```text
apps/
  api/                 FastAPI backend
  web/                 React frontend
dev_mcp/               MicroFast MCP server + queue ops helpers
docs/                  Architecture, procedures, runbooks, security, etc.
prompts/               Reusable agent prompt templates
queue/                 Open + archived queue ledgers and SOPs
scripts/               Validation, automation, queue and repo tooling
skills/                Task-specific reusable operational skills
spec/                  Canonical system specification
AGENTS.md              Agent contract and instruction hierarchy
idea.md                Product intake contract
Makefile               Canonical command interface
```

---

## Most Important Files

- `AGENTS.md` - authoritative workflow and policy contract.
- `queue/QUEUE_INSTRUCTIONS.md` - queue schema and lifecycle SOP.
- `skills/README.md` - skill index for mandatory skill search.
- `docs/DOCS_MAP.md` - canonical doc index with stable doc IDs.
- `spec/spec.md` - system specification baseline.

---

## Common Pitfalls to Avoid

- Treating `idea.md` as optional: it is the product contract.
- Writing feature code during initialization flow.
- Skipping mandatory skill search.
- Editing queue rows without validating with `make queue:validate`.
- Using ad hoc shell commands when a `make` target exists.

---

## Contributing

Use small, reviewable changes. Prefer one logical change per PR.

When behavior changes, update docs and validation expectations in the same PR.

For queue-driven work, include queue IDs in PR titles and follow archive/merge procedure after completion.

---

## License

MIT. See `LICENSE`.
