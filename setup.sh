#!/usr/bin/env bash
# setup.sh
# BLUEPRINT: Composer 2 implements from this structure
# PURPOSE: Linux/macOS one-shot bootstrap after clone. Run once to go from fresh clone to
#          green dev environment. Per spec §10.3 and §26.12 item 347.
# CORRESPONDS TO: No Make target (run directly; called by CI occasionally)
# DEPENDS ON: Python 3.12+, Docker, Docker Compose v2, Make, Git (verified in script)

# STEP 1: set -euo pipefail — fail fast on any error
# STEP 2: Print welcome banner and instructions
# STEP 3: Verify prerequisites
#   - Python 3.12+ (python --version; fail with clear install hint if wrong version)
#   - Docker (docker --version; fail with install link if missing)
#   - Docker Compose v2 (docker compose version; fail if v1 Compose is used)
#   - Make (make --version; fail with brew/apt install hint)
#   - Git (git --version; always present but check anyway)
# STEP 4: Create Python virtual environment (.venv) if not exists
#   - python -m venv .venv
# STEP 5: Activate .venv and install dependencies
#   - source .venv/bin/activate
#   - pip install --upgrade pip
#   - pip install -e ".[dev,test,lint]"  (from pyproject.toml)
# STEP 6: Copy .env.example to .env if .env does not exist
#   - cp .env.example .env
#   - Print message telling user to edit .env with real values
# STEP 7: Start Docker Compose services (base profile: api + db if available)
#   - docker compose up -d db (if db profile available in project)
#   - Wait for services to be healthy (poll docker compose ps --format json)
# STEP 8: Run database migrations
#   - make migrate
# STEP 9: Run linting and type checking to verify setup
#   - make lint
#   - make typecheck
# STEP 10: Run test suite to verify everything works
#   - make test
# STEP 11: Print success message with next steps
#   - "Setup complete! Run ./run.sh to start the development server."
#   - List key make targets: make dev, make test, make queue:peek

# ERROR HANDLING:
#   - Each major step is wrapped in a check function
#   - On failure: print clear error message with remediation hint
#   - Exit with code 1 so CI catches failures

# OUTPUT:
#   - Progress messages to stdout with clear [STEP N/N] prefixes
#   - Error messages to stderr
#   - Final success message with next-steps guide
