# skills/repo-governance/adr-index-generator.py
"""Print a Markdown table of docs/adr/*.md (excluding README and template)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    adr = args.repo_root / "docs" / "adr"
    if not adr.is_dir():
        print("No docs/adr", file=sys.stderr)
        return 1
    files = sorted(
        p for p in adr.glob("*.md") if p.name not in {"README.md", "template.md"}
    )
    print("# ADR index\n")
    print("| ADR | Title |")
    print("|-----|-------|")
    for p in files:
        first = p.read_text(encoding="utf-8").splitlines()[:1]
        title = first[0].lstrip("# ").strip() if first else p.stem
        rel = p.relative_to(args.repo_root)
        print(f"| [{p.stem}]({rel.as_posix()}) | {title} |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
