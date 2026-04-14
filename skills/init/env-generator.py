# skills/init/env-generator.py
"""Manage .env from .env.example; optionally print example content."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap .env from .env.example")
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument(
        "--show",
        action="store_true",
        help="Print .env.example contents to stdout (no file writes)",
    )
    args = parser.parse_args()
    src = args.repo_root / ".env.example"
    dst = args.repo_root / ".env"
    if not src.is_file():
        print("Missing .env.example", file=sys.stderr)
        return 1
    if args.show:
        sys.stdout.write(src.read_text(encoding="utf-8"))
        return 0
    if dst.exists():
        print(".env already exists")
        return 0
    shutil.copy(src, dst)
    print("Created .env from .env.example")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
