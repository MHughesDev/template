#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "[project:health] queue validation"
make queue:validate

echo "[project:health] docs map invariants"
python3 scripts/check_docs_map.py

echo "[project:health] docs check"
make docs:check

echo "[project:health] adr index tool presence check"
test -f skills/repo-governance/adr-index-generator.py

echo "[project:health] placeholder scan (docs + idea)"
if rg -n "<placeholder>|Stub procedure placeholder|Compatibility stub" docs idea.md >/tmp/project_health_placeholders.txt; then
  echo "Found unresolved placeholders/stubs:"
  cat /tmp/project_health_placeholders.txt
  exit 1
fi

echo "project:health OK"
