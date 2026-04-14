#!/usr/bin/env bash
# scripts/db-reset.sh
# Remove local SQLite DB files and re-apply migrations.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

rm -f apps/api/dev.db apps/api/test.db dev.db test.db 2>/dev/null || true
export PYTHONPATH="$ROOT"
"$ROOT/scripts/migrate.sh"
echo "Database reset complete."
