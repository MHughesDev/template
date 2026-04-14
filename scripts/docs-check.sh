#!/usr/bin/env bash
# scripts/docs-check.sh
# Verify internal markdown links under docs/ only.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

python3 <<'PY'
from __future__ import annotations

import re
import sys
from pathlib import Path

root = Path("docs")
link_re = re.compile(r"\]\(([^)]+)\)")
errors = 0
for md in root.rglob("*.md"):
    text = md.read_text(encoding="utf-8", errors="ignore")
    for m in link_re.finditer(text):
        target = m.group(1).split("#", 1)[0].strip()
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        if target.startswith("/"):
            continue
        resolved = (md.parent / target).resolve()
        try:
            resolved.relative_to(Path(".").resolve())
        except ValueError:
            continue
        if not resolved.exists():
            print(f"Broken link in {md}: {target}", file=sys.stderr)
            errors += 1
sys.exit(1 if errors else 0)
PY
echo "Checking generated docs for drift..."
python3 "$ROOT/skills/repo-governance/docs-generator.py" --mode check --repo-root "$ROOT"
echo "docs:check OK"
