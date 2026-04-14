#!/usr/bin/env bash
# scripts/validate-idea.sh
# Check idea.md exists; warn on HTML comment placeholders (does not fail CI for template).

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FILE="$ROOT/idea.md"
if [[ ! -f "$FILE" ]]; then
  echo "Missing idea.md" >&2
  exit 1
fi
if grep -q '<!--' "$FILE"; then
  echo "idea:validate — note: idea.md still contains <!-- ... --> placeholders; replace before production init." >&2
fi
echo "idea:validate OK"
