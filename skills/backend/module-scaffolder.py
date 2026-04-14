# skills/backend/module-scaffolder.py
"""Create a minimal bounded-context skeleton under apps/api/src/."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="snake_case module name, e.g. billing")
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    name = args.name.strip().lower()
    if not re.match(r"^[a-z][a-z0-9_]*$", name):
        print("Invalid module name", file=sys.stderr)
        return 1
    title = name.replace("_", " ").title().replace(" ", "")
    base = args.repo_root / "apps" / "api" / "src" / name
    if base.exists():
        print(f"Already exists: {base}", file=sys.stderr)
        return 1
    base.mkdir(parents=True)

    router = f'''# apps/api/src/{name}/router.py
"""HTTP routes for {name}."""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/{name}", tags=["{name}"])


@router.get("/")
async def ping() -> dict[str, str]:
    return {{"status": "ok", "context": "{name}"}}
'''
    service = f'''# apps/api/src/{name}/service.py
"""Domain logic for {name}."""

from __future__ import annotations


class {title}Service:
    """Application service for {name}."""

    pass
'''
    init = f'''# apps/api/src/{name}/__init__.py
"""Bounded context: {name}."""

from apps.api.src.{name}.router import router

__all__ = ["router"]
'''
    (base / "__init__.py").write_text(init, encoding="utf-8")
    (base / "router.py").write_text(router, encoding="utf-8")
    (base / "service.py").write_text(service, encoding="utf-8")
    print(f"Created {base}")
    print("Wire in apps/api/src/main.py: import router and include_router under API_PREFIX.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
