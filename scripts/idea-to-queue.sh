#!/usr/bin/env bash
# scripts/idea-to-queue.sh
# Seed queue/queue.csv: prefer init-manifest.json (resolved_decisions.queue_seed_rows), else idea.md §12.
# Implementation delegates to skills/init/queue-seeder.py (single code path).

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MANIFEST="$ROOT/init-manifest.json"

if [[ -f "$MANIFEST" ]]; then
  # Prefer manifest when it contains queue_seed_rows (queue-seeder.py checks JSON).
  exec python3 "$ROOT/skills/init/queue-seeder.py" --repo-root "$ROOT"
fi

exec python3 "$ROOT/skills/init/queue-seeder.py" --repo-root "$ROOT" --from-idea
