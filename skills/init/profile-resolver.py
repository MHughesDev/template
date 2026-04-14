# skills/init/profile-resolver.py
"""Print enabled optional profiles from idea.md keywords."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    path = args.repo_root / "idea.md"
    if not path.is_file():
        print("Missing idea.md", file=sys.stderr)
        return 1
    text = path.read_text(encoding="utf-8").lower()
    profiles: list[str] = []
    if re.search(r"\b(chroma|vector|embedding|rag)\b", text):
        profiles.append("ai")
    if re.search(r"\b(next\.js|react|vite|expo|mobile)\b", text):
        profiles.append("clients")
    print("Suggested profiles:", ", ".join(profiles) or "(none detected)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
