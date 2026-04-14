# scripts/inventory_check.py
"""Verify that file checklist rows marked complete in IMPLEMENTATION_PLAN exist on disk."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def parse_completed_paths(plan: Path) -> list[str]:
    text = plan.read_text(encoding="utf-8")
    paths: list[str] = []
    for line in text.splitlines():
        m = re.match(r"^\|\s*\[x\]\s*\|\s*`([^`]+)`\s*\|", line)
        if m:
            paths.append(m.group(1))
    return paths


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    root: Path = args.root
    plan = root / "spec" / "IMPLEMENTATION_PLAN.md"
    if not plan.is_file():
        print(f"Missing {plan}", file=sys.stderr)
        return 1

    missing: list[str] = []
    for rel in parse_completed_paths(plan):
        if rel.endswith("/"):
            p = root / rel.rstrip("/")
            if not p.is_dir():
                missing.append(rel)
            continue
        p = root / rel
        if not p.exists():
            missing.append(rel)

    if missing:
        print("Completed checklist items missing on disk:", file=sys.stderr)
        for m in sorted(missing):
            print(f"  - {m}", file=sys.stderr)
        return 1
    print(f"inventory:check OK ({len(parse_completed_paths(plan))} completed paths verified)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
