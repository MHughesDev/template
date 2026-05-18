---
doc_id: "1.2"
title: "quickstart"
section: "Getting Started"
summary: "Step-by-step from clone to running dev server with passing tests."
updated: "2026-05-17"
---

# 1.2 — quickstart

**Purpose:** Step-by-step from clone to running dev server with passing tests. Per spec §26.5 item 114.

## 1.2.1 Quickstart Steps
Numbered steps with exact commands and expected output for each:
1. Clone: `git clone <repo-url> && cd <repo-name>`
2. Bootstrap: `./setup.sh` (Linux/macOS/WSL/Git Bash on Windows)
   - Expected: "Setup complete!" message, all tests passing
   - **Windows users:** Use WSL or Git Bash. The template standardizes on Unix-like shells for cross-platform consistency.
3. OR manual setup:
   a. `cp .env.example .env && nano .env` (fill in real values)
   b. `python -m venv .venv && source .venv/bin/activate`
   c. `pip install -e ".[dev,test,lint]"`
   d. `make docker:up && make migrate`
   e. `make dev` — API starts at http://localhost:8000
4. Verify: `make health:check` — health, ready, live all return 200
5. Test: `make test` — all tests pass

## 1.2.2 What's Running?
Brief description of what setup.sh starts: FastAPI API on port 8000, (optional) PostgreSQL on port 5432.

## 1.2.3 Next Steps
Links to: docs/development/local-setup.md (all make targets plus **agent/queue tooling**), queue/QUEUE_INSTRUCTIONS.md (start working), AGENTS.md (agent policy).

**Coding agents:** Follow **AGENTS.md** section 3 — no project-specific MCP connection is required; queue introspection uses **Make** or **`python scripts/queue_top_item.py`** (see **docs/development/local-setup.md**).
