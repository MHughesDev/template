#!/usr/bin/env bash
# scripts/seed-db.sh
# Placeholder seed — extend when domain fixtures are added.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ -f ".venv/bin/activate" ]]; then
  # shellcheck source=/dev/null
  source ".venv/bin/activate"
fi

echo "seed-db: no default seed data in template (add scripts or Alembic data migration)."
echo "Apply migrations first: make migrate"
