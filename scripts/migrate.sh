#!/usr/bin/env bash
# scripts/migrate.sh
# Run Alembic from apps/api (requires PYTHONPATH=repo root for imports).

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PYTHONPATH="$ROOT"
cd "$ROOT/apps/api"

if [[ "${1:-}" == "create" ]]; then
  if [[ -z "${MESSAGE:-}" ]]; then
    echo "Usage: MESSAGE='description' make migrate:create" >&2
    exit 1
  fi
  exec python3 -m alembic revision --autogenerate -m "${MESSAGE}"
fi

exec python3 -m alembic upgrade head
