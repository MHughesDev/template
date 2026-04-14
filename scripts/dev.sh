#!/usr/bin/env bash
# scripts/dev.sh
# Start the FastAPI app locally with hot reload (uvicorn).

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ ! -f "pyproject.toml" ]]; then
  echo "error: run from repository root (pyproject.toml not found)" >&2
  exit 1
fi

if [[ -f ".venv/bin/activate" ]]; then
  # shellcheck source=/dev/null
  source ".venv/bin/activate"
fi

HOST="${API_HOST:-0.0.0.0}"
PORT="${API_PORT:-8000}"

echo "Starting API at http://${HOST}:${PORT} (reload on) ..."
exec python3 -m uvicorn apps.api.src.main:app --reload --host "$HOST" --port "$PORT"
