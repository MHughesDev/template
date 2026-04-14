# skills/init/archetype-mapper.py
"""Map keywords in idea.md to a coarse archetype label."""

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
    t = path.read_text(encoding="utf-8").lower()
    if re.search(r"\b(saas|multi-tenant|tenant)\b", t):
        archetype = "multi-tenant-saas"
    elif re.search(r"\b(api|rest|fastapi)\b", t):
        archetype = "api-backend"
    else:
        archetype = "general"
    print("Archetype:", archetype)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
