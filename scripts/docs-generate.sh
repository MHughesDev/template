#!/usr/bin/env bash
# scripts/docs-generate.sh
# Regenerate docs from source (OpenAPI stub + index).

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GEN="$ROOT/skills/repo-governance/docs-generator.py"

if [[ -f "$GEN" ]]; then
  if [[ -f "$ROOT/.venv/bin/activate" ]]; then
    # shellcheck source=/dev/null
    source "$ROOT/.venv/bin/activate"
  fi
  exec python3 "$GEN"
fi

echo "docs-generate: docs-generator.py not present; nothing to do"
