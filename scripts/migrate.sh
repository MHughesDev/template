#!/usr/bin/env bash
# scripts/migrate.sh
# Apply Alembic migrations or create a new revision (MESSAGE=... for create).

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ -f ".venv/bin/activate" ]]; then
  # shellcheck source=/dev/null
  source ".venv/bin/activate"
fi

API_DIR="$ROOT/apps/api"
cd "$API_DIR"

if [[ "${1:-}" == "create" ]]; then
  if [[ -z "${MESSAGE:-}" ]]; then
    echo "error: MESSAGE=<description> is required for migrate:create" >&2
    exit 1
  fi
  exec python3 -m alembic revision --autogenerate -m "$MESSAGE"
fi

exec python3 -m alembic upgrade head
