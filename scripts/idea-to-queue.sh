#!/usr/bin/env bash
# scripts/idea-to-queue.sh
# Seed queue from idea.md §12 (skills/init/queue-seeder.py).

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ -f ".venv/bin/activate" ]]; then
  # shellcheck source=/dev/null
  source ".venv/bin/activate"
fi

SEEDER="$ROOT/skills/init/queue-seeder.py"
if [[ -f "$SEEDER" ]]; then
  exec python3 "$SEEDER"
fi

echo "error: queue-seeder.py not implemented" >&2
exit 1
