#!/usr/bin/env bash
# scripts/scaffold-module.sh
# Scaffold bounded context module (MODULE=name required).

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ -z "${MODULE:-}" ]]; then
  echo "error: MODULE=<context_name> required" >&2
  exit 1
fi

SCAF="$ROOT/skills/backend/module-scaffolder.py"
if [[ -f "$SCAF" ]]; then
  if [[ -f ".venv/bin/activate" ]]; then
    # shellcheck source=/dev/null
    source ".venv/bin/activate"
  fi
  exec python3 "$SCAF" --name "$MODULE"
fi

echo "error: module-scaffolder.py not available" >&2
exit 1
