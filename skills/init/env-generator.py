# skills/init/env-generator.py
"""Copy .env.example to .env if missing."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    src = args.repo_root / ".env.example"
    dst = args.repo_root / ".env"
    if not src.is_file():
        print("Missing .env.example", file=sys.stderr)
        return 1
    if dst.exists():
        print(".env already exists")
        return 0
    shutil.copy(src, dst)
    print("Created .env from .env.example")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
