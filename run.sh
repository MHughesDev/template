#!/usr/bin/env bash
# run.sh
# Start the API (delegates to scripts/dev.sh).

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

if [[ ! -f .env ]]; then
  echo "No .env — run ./setup.sh or: cp .env.example .env" >&2
  exit 1
fi

if [[ -f .venv/bin/activate ]]; then
  # shellcheck source=/dev/null
  source .venv/bin/activate
fi

if command -v docker >/dev/null 2>&1 && [[ -f docker-compose.yml ]]; then
  if ! docker compose ps --status running --format '{{.Name}}' 2>/dev/null | grep -q .; then
    echo "Starting Docker Compose services..."
    docker compose up -d
    sleep 3
  fi
fi

echo "API: http://localhost:8000"
echo "Docs: http://localhost:8000/docs"
echo "Health: http://localhost:8000/health"

exec "$ROOT/scripts/dev.sh"
