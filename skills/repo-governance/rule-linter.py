# skills/repo-governance/rule-linter.py
"""Verify .cursor/rules/*.md start with YAML front matter."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    rules = args.repo_root / ".cursor" / "rules"
    err = 0
    for f in sorted(rules.glob("*.md")):
        first = f.read_text(encoding="utf-8").splitlines()[:1]
        if not first or first[0].strip() != "---":
            print(f"Missing front matter: {f}", file=sys.stderr)
            err += 1
    return err


if __name__ == "__main__":
    raise SystemExit(main())
