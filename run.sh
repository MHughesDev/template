#!/usr/bin/env bash
# run.sh
# BLUEPRINT: Composer 2 implements from this structure
# PURPOSE: Linux/macOS day-to-day dev runner. Starts API with hot reload.
#          Run this every day to start development after initial setup.
#          Per spec §10.3 and §26.12 item 349.
# CORRESPONDS TO: make dev (delegates to this after checks)
# DEPENDS ON: .env file (must exist), Docker Compose (for db service), Make

# STEP 1: set -euo pipefail

# STEP 2: Verify .env exists
#   - if [ ! -f .env ]; then print error "No .env file. Run ./setup.sh first or: cp .env.example .env"; exit 1; fi

# STEP 3: Verify .venv exists
#   - if [ ! -d .venv ]; then print error "No .venv. Run ./setup.sh first"; exit 1; fi

# STEP 4: Source .venv
#   - source .venv/bin/activate

# STEP 5: Start Docker Compose services if not running
#   - Check if db service is running: docker compose ps db | grep "running"
#   - If not running: docker compose up -d db
#   - Wait for db health check (poll with timeout)

# STEP 6: Wait for services to be healthy
#   - Poll docker compose ps until all required services show "healthy"
#   - Timeout after 30 seconds with clear error

# STEP 7: Print local URL and key endpoints
#   - echo "API: http://localhost:8000"
#   - echo "Docs: http://localhost:8000/docs"
#   - echo "Health: http://localhost:8000/health"
#   - echo ""
#   - echo "Key commands: make test, make queue:peek, make audit:self"

# STEP 8: Start API with hot reload
#   - make dev (which runs scripts/dev.sh → uvicorn with --reload)

# ERROR HANDLING:
#   - If .env missing: print setup hint and exit 1
#   - If .venv missing: print setup hint and exit 1
#   - If Docker Compose fails: print troubleshooting hint (docs/troubleshooting/common-issues.md)
#   - If API fails to start: show last 20 lines of logs

# OUTPUT:
#   - Clear status messages for each step
#   - API URL and key endpoint list before starting
#   - Hot reload server logs streamed to terminal
