# docs/getting-started/quickstart.md

> PURPOSE: Step-by-step from clone to running dev server with passing tests. Per spec §26.5 item 114.

## Quickstart Steps
> CONTENT: Numbered steps with exact commands and expected output for each:
> 1. Clone: `git clone <repo-url> && cd <repo-name>`
> 2. Bootstrap: `./setup.sh` (Linux/macOS) or `setup.bat` (Windows)
>    - Expected: "Setup complete!" message, all tests passing
> 3. OR manual setup:
>    a. `cp .env.example .env && nano .env` (fill in real values)
>    b. `python -m venv .venv && source .venv/bin/activate`
>    c. `pip install -e ".[dev,test,lint]"`
>    d. `make docker:up && make migrate`
>    e. `make dev` — API starts at http://localhost:8000
> 4. Verify: `make health:check` — health, ready, live all return 200
> 5. Test: `make test` — all tests pass

## What's Running?
> CONTENT: Brief description of what setup.sh starts: FastAPI API on port 8000, (optional) PostgreSQL on port 5432.

## Next Steps
> CONTENT: Links to: docs/development/local-setup.md (all make targets), queue/QUEUE_INSTRUCTIONS.md (start working), AGENTS.md (agent policy).
