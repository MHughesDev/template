# skills/testing/test-scaffolder.py
"""Emit pytest stub tests for each @router.get/post/... in a router module (regex-based)."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def find_routes(source: str) -> list[tuple[str, str]]:
    """Return (method, path) from FastAPI route decorators."""
    out: list[tuple[str, str]] = []
    for m in re.finditer(
        r"@router\.(get|post|put|patch|delete)\(\s*[\"']([^\"']+)[\"']",
        source,
    ):
        out.append((m.group(1).upper(), m.group(2)))
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("router_file", type=Path, help="Path to router.py")
    args = parser.parse_args()
    if not args.router_file.is_file():
        print("File not found", file=sys.stderr)
        return 1
    text = args.router_file.read_text(encoding="utf-8")
    routes = find_routes(text)
    mod = args.router_file.parent.name
    print(f'"""Generated stubs for {mod}."""')
    print()
    print("import pytest")
    print()
    for method, path in routes:
        safe = path.replace("/", "_").replace("{", "").replace("}", "").strip("_") or "root"
        fname = f"test_{mod}_{method.lower()}_{safe}"
        print()
        print(f"async def {fname}() -> None:")
        print(f'    raise NotImplementedError("{method} {path}")')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
