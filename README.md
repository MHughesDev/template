# README.md

<!-- BLUEPRINT: Composer 2 implements from this structure -->
<!-- CROSS-REFERENCES -->
<!-- - Referenced by: AGENTS.md §Navigation, docs/getting-started/quickstart.md -->
<!-- - Links to: AGENTS.md, spec/spec.md, docs/, Makefile -->

> PURPOSE: Quickstart entry point for humans and agents. The first file read when approaching this repository. Links to all key resources: AGENTS.md, spec, docs, command catalog. Per spec §26.1 item 3.

## Project Title

> CONTENT: The project display name as a top-level H1 heading. One-paragraph description of what this repository is: a batteries-included template repository designed as a Cursor-first, agent-operated software factory. State that it is a Python 3.12+ / FastAPI modular monolith template with optional React/Expo frontends, queue-driven agent work orchestration, and a full documentation and governance machine.

## Prerequisites

> CONTENT: Minimal list of required tools with version commands to verify each. Items:
> - Python 3.12+ (`python --version`)
> - Docker + Docker Compose v2+ (`docker --version`, `docker compose version`)
> - Make (`make --version`)
> - Git (`git --version`)
> - Optional: Node.js 20+ (web profile), Expo CLI (mobile profile)
>
> Link to `docs/getting-started/prerequisites.md` for detailed setup and troubleshooting.

## Quickstart

> CONTENT: Numbered steps from clone to green dev server. Exact commands (not pseudocode):
> 1. Clone: `git clone <repo-url> && cd <repo-name>`
> 2. Bootstrap: `./setup.sh` (Linux/macOS) or `setup.bat` (Windows) — installs deps, creates .env, starts services, runs migrations and tests
> 3. OR manual: copy `.env.example` → `.env`, `make dev`, `make test`
>
> Expected output for key steps. State that `setup.sh` is the recommended path for a fresh clone.

## Key Commands

> CONTENT: Quick-reference table of the most important `make` targets. Columns: Target, Purpose. Rows for: `make dev`, `make test`, `make lint`, `make fmt`, `make typecheck`, `make migrate`, `make queue:peek`, `make audit:self`, `make skills:list`. State: "See Makefile or run `make help` for all targets."

## Key Resources

> CONTENT: Link table to all major resources. Columns: Resource, Link, Purpose. Rows:
> - Agent control plane: AGENTS.md — read this first if you are an agent
> - Full specification: spec/spec.md — authoritative design and policy document
> - Getting started: docs/getting-started/ — prerequisites and quickstart in detail
> - Architecture: docs/architecture/ — system design and bounded contexts
> - Procedures: docs/procedures/ — canonical SOPs for recurring workflows
> - Queue system: queue/QUEUE_INSTRUCTIONS.md — how the agent work queue works
> - Skills library: skills/README.md — executable playbooks by category
> - Prompt templates: prompts/README.md — reusable agent role templates
> - Development: docs/development/local-setup.md — all Make targets documented
> - API docs: docs/api/ — endpoint catalog and error codes

## License

> CONTENT: License badge and one-line statement (MIT or Apache-2.0 — filled at initialization time). Link to LICENSE file.
