#!/usr/bin/env bash
# scripts/db-reset.sh
# Remove local SQLite dev DB and re-run migrations.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ -f ".venv/bin/activate" ]]; then
  # shellcheck source=/dev/null
  source ".venv/bin/activate"
fi

rm -f apps/api/dev.db apps/api/./dev.db 2>/dev/null || true
scripts/migrate.sh
echo "db-reset: OK"
