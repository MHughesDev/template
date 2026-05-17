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
# Backend deps come from apps/api/pyproject.toml (uv-managed in production).
# For a quick local install without uv, install backend deps in editable mode:
if [[ -f apps/api/pyproject.toml ]]; then
  pip install -e apps/api
fi
# Repo-wide dev tools:
pip install -e ".[dev]" || true

if [[ ! -f .env ]]; then
  cp .env.example .env
  echo "Created .env from .env.example — set SECRET_KEY, POSTGRES_PASSWORD, FIRST_SUPERUSER_PASSWORD before production."
fi

export PYTHONPATH="$ROOT/apps/api"

echo "Starting Docker Compose services..."
$COMPOSE up -d

echo "Waiting for Compose to settle..."
sleep 5
if ! $COMPOSE ps --status running 2>/dev/null | grep -q .; then
  echo "Warning: no running Compose services — check compose.yml" >&2
fi

# Frontend deps via bun if available.
if command -v bun >/dev/null 2>&1; then
  echo "Installing frontend deps via bun..."
  (cd apps/web && bun install)
fi

make lint || true
make fmt || true
echo "Setup complete. Run ./run.sh or \`make dev-api\` for the backend; \`make dev-web\` for the frontend."
