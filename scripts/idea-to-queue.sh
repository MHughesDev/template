#!/usr/bin/env bash
# scripts/idea-to-queue.sh
# Seed queue/queue.csv from idea.md §12 via queue-seeder.py.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec python3 "$ROOT/skills/init/queue-seeder.py" --repo-root "$ROOT" --from-idea "$@"
