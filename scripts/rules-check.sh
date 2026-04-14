#!/usr/bin/env bash
# scripts/rules-check.sh
# Basic validation: .mdc/.md rules under .cursor/rules/ are non-empty.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RULES="$ROOT/.cursor/rules"

if [[ ! -d "$RULES" ]]; then
  echo "error: $RULES missing" >&2
  exit 1
fi

FAILED=0
while IFS= read -r -d '' f; do
  if [[ ! -s "$f" ]]; then
    echo "error: empty rule file $f" >&2
    FAILED=1
  fi
done < <(find "$RULES" -type f \( -name '*.md' -o -name '*.mdc' \) -print0)

if [[ "$FAILED" -ne 0 ]]; then
  exit 1
fi
echo "rules-check: OK"
