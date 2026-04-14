#!/usr/bin/env bash
# scripts/validate-idea.sh
# Validate idea.md completeness (skills/init/idea-validator.py).

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ -f ".venv/bin/activate" ]]; then
  # shellcheck source=/dev/null
  source ".venv/bin/activate"
fi

IDEA="${1:-idea.md}"
exec python3 "$ROOT/skills/init/idea-validator.py" "$IDEA"
