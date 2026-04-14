#!/usr/bin/env bash
# scripts/docs-index.sh
# Update docs/README.md with an auto-generated directory listing (between markers).

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Updating docs/README.md auto-index section..."
export REPO_ROOT="$ROOT"
python3 <<'PY'
from __future__ import annotations

import os
from pathlib import Path

root = Path(os.environ["REPO_ROOT"]) / "docs"
readme = root / "README.md"
lines = [
    "<!-- AUTO_INDEX_START -->",
    "",
    "## Auto-generated index",
    "",
    "_Machine listing of top-level docs paths — see sections above for curated descriptions._",
    "",
]
for d in sorted(root.iterdir()):
    if d.name.startswith(".") or d.name == "README.md":
        continue
    if d.is_dir():
        sub = d / "README.md"
        if sub.exists():
            lines.append(f"- [{d.name}/]({d.name}/README.md)")
        else:
            lines.append(f"- `{d.name}/`")
    elif d.is_file() and d.suffix == ".md":
        lines.append(f"- [{d.stem}]({d.name})")
lines.append("")
lines.append("<!-- AUTO_INDEX_END -->")
block = "\n".join(lines) + "\n"

if not readme.is_file():
    readme.write_text("# docs/README.md\n\n" + block, encoding="utf-8")
    print(f"Created {readme}")
else:
    text = readme.read_text(encoding="utf-8")
    start, end = "<!-- AUTO_INDEX_START -->", "<!-- AUTO_INDEX_END -->"
    if start in text and end in text:
        before, rest = text.split(start, 1)
        _, after = rest.split(end, 1)
        new_text = before.rstrip() + "\n\n" + block + "\n" + after.lstrip()
    else:
        new_text = text.rstrip() + "\n\n" + block + "\n"
    readme.write_text(new_text, encoding="utf-8")
    print(f"Updated {readme}")
PY
echo "Done."
