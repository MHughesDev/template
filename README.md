# Template — Agent-operated software factory

A batteries-included **template repository** for Cursor-first, agent-operated development: a Python 3.12+ **FastAPI** modular monolith, optional **React/Expo** client profiles, **CSV queue**-driven agent work, and a full **docs / skills / prompts / CI** machine. See **[AGENTS.md](AGENTS.md)** for the agent contract and **[spec/spec.md](spec/spec.md)** for the full specification.

## Prerequisites

| Tool | Check |
|------|--------|
| Python 3.12+ | `python --version` |
| Docker + Compose v2+ | `docker --version`, `docker compose version` |
| GNU Make | `make --version` |
| Git | `git --version` |
| Optional: Node 20+ (web profile) | `node --version` |
| Optional: Expo tooling (mobile profile) | project-specific |

Details and troubleshooting: **[docs/getting-started/prerequisites.md](docs/getting-started/prerequisites.md)**.

## Quickstart

1. **Clone:** `git clone <repo-url> && cd <repo-name>`
2. **Bootstrap (recommended):** `./setup.sh` (Linux/macOS) or `setup.bat` (Windows) — installs dependencies, prepares `.env`, runs migrations and tests where configured.
3. **Manual path:** copy `cp .env.example .env`, edit values, then `make dev` and `make test`.

Use **`./setup.sh`** on a fresh clone unless you have a reason to wire the environment by hand.

## Key commands

| Target | Purpose |
|--------|---------|
| `make dev` | Local API / dev stack (see Makefile) |
| `make test` | Test suite with coverage |
| `make lint` | Ruff lint |
| `make fmt` | Format check (CI mode) |
| `make typecheck` | mypy strict |
| `make migrate` | Database migrations |
| `make queue:peek` | Read current queue top row |
| `make audit:self` | Repo self-audit / combined checks |

Run **`make help`** or open the **Makefile** for the full catalog.

## Key resources

| Resource | Path | Purpose |
|----------|------|---------|
| Agent control plane | [AGENTS.md](AGENTS.md) | Read first for policy and workflow |
| Full specification | [spec/spec.md](spec/spec.md) | Authoritative design and requirements |
| Getting started | [docs/getting-started/](docs/getting-started/) | Prerequisites and quickstart detail |
| Architecture | [docs/architecture/](docs/architecture/) | System design and contexts |
| Procedures | [docs/procedures/](docs/procedures/) | Canonical SOPs |
| Queue | [queue/QUEUE_INSTRUCTIONS.md](queue/QUEUE_INSTRUCTIONS.md) | CSV queue lifecycle |
| Skills | [skills/README.md](skills/README.md) | Playbooks by category |
| Prompts | [prompts/README.md](prompts/README.md) | Role templates |
| Local setup / Make | [docs/development/local-setup.md](docs/development/local-setup.md) | Targets and environment |
| API | [docs/api/](docs/api/) | Endpoints and error catalog |

## License

This template is distributed under the **MIT License** — see **[LICENSE](LICENSE)**.
