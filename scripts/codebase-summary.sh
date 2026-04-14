#!/usr/bin/env bash
# scripts/codebase-summary.sh
# Append a dated snapshot section to CODEBASE_SUMMARY.md (counts + module list).

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$ROOT/CODEBASE_SUMMARY.md"

{
  echo ""
  echo "## Automated snapshot"
  echo ""
  echo "_Generated: $(date -u "+%Y-%m-%dT%H:%M:%SZ")_"
  echo ""
} >>"$OUT"

python3 <<'PY' >>"$OUT"
from __future__ import annotations

from pathlib import Path

root = Path(".")
mods = sorted({p.parent.name for p in root.glob("apps/api/src/*/router.py")})
pkgs = sorted({p.parent.name for p in root.glob("packages/*/AGENTS.md")})
skills = len([p for p in root.glob("skills/**/*.md") if p.name != "README.md"])
prompts = len([p for p in root.glob("prompts/*.md") if p.name != "README.md"])
scripts = len(list(root.glob("scripts/*.sh")))
print("- **API modules (router.py):**", len(mods), "—", mods)
print("- **Packages:**", pkgs)
print("- **Skills (.md):**", skills)
print("- **Prompts (.md):**", prompts)
print("- **Shell scripts:**", scripts)
print()
PY

echo "Appended snapshot to CODEBASE_SUMMARY.md"
