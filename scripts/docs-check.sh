#!/usr/bin/env bash
# scripts/docs-check.sh
# Verify relative markdown links under docs/ resolve to existing paths.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec python3 - "$ROOT" <<'PY'
from __future__ import annotations

import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
docs = root / "docs"
link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
failed = False

for md in docs.rglob("*.md"):
    text = md.read_text(encoding="utf-8", errors="replace")
    for m in link_re.finditer(text):
        raw = m.group(1).strip()
        if raw.startswith(("#", "http://", "https://", "mailto:")):
            continue
        path_part = raw.split("#", 1)[0]
        if not path_part:
            continue
        target = (md.parent / path_part).resolve()
        try:
            target.relative_to(root)
        except ValueError:
            print(f"link escapes repo: {md}: {raw}", file=sys.stderr)
            failed = True
            continue
        if not target.is_file():
            print(f"broken link: {md} -> {raw}", file=sys.stderr)
            failed = True

sys.exit(1 if failed else 0)
PY
