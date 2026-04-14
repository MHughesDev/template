# skills/init/idea-validator.py
"""Validate idea.md: required heading sections present."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED = (
    "## 1. Project identity",
    "## 2. Problem and solution",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    path = args.repo_root / "idea.md"
    if not path.is_file():
        print("Missing idea.md", file=sys.stderr)
        return 1
    text = path.read_text(encoding="utf-8")
    missing = [h for h in REQUIRED if h not in text]
    if missing:
        print("Missing sections:", missing, file=sys.stderr)
        return 1
    if "<!--" in text:
        print("Note: idea.md still has HTML comments — fill before init.")
    print("idea.md structure OK.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
