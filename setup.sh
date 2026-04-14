#!/usr/bin/env bash
# setup.sh
# One-shot bootstrap: venv, editable install, .env, migrations.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

need() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "Missing required command: $1" >&2
    exit 1
  }
}

need python3
need make
need docker
need git

if docker compose version >/dev/null 2>&1; then
  COMPOSE="docker compose"
elif command -v docker-compose >/dev/null 2>&1; then
  COMPOSE="docker-compose"
else
  echo "Missing: docker compose (v2 plugin or docker-compose standalone)" >&2
  exit 1
fi

if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi
# shellcheck source=/dev/null
source .venv/bin/activate
python -m pip install --upgrade pip
if [[ -f requirements.lock ]]; then
  pip install -r requirements.lock
  pip install -e . --no-deps
else
  pip install -e ".[dev]"
fi

if [[ ! -f .env ]]; then
  cp .env.example .env
  echo "Created .env from .env.example — set JWT_SECRET_KEY before production."
fi

export PYTHONPATH="$ROOT"

echo "Starting Docker Compose services..."
$COMPOSE up -d

echo "Waiting for Compose to settle..."
sleep 5
if ! $COMPOSE ps --status running 2>/dev/null | grep -q .; then
  echo "Warning: no running Compose services — check docker-compose.yml" >&2
fi

make migrate
make lint
make fmt
make typecheck
make test
echo "Setup complete. Run ./run.sh or make dev to start the API."
