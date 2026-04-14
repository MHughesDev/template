# skills/backend/env-var-sync.py
"""Compare Settings in apps/api/src/config.py with keys in .env.example."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def env_var_names_from_example(text: str) -> set[str]:
    names: set[str] = set()
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"^([A-Z][A-Z0-9_]*)\s*=", line)
        if m:
            names.add(m.group(1))
    return names


def field_names_from_config(text: str) -> set[str]:
    # Heuristic: Field(..., alias="X") or field_name: type
    names: set[str] = set()
    for m in re.finditer(r"^\s+([a-z_][a-z0-9_]*)\s*:", text, re.MULTILINE):
        names.add(m.group(1))
    return names


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    root = args.repo_root
    ex = root / ".env.example"
    cfg = root / "apps" / "api" / "src" / "config.py"
    if not ex.is_file() or not cfg.is_file():
        print("Missing .env.example or config.py", file=sys.stderr)
        return 1
    env_keys = env_var_names_from_example(ex.read_text(encoding="utf-8"))
    # Map Settings fields to env: pydantic-settings uses upper field names by default
    settings_fields = field_names_from_config(cfg.read_text(encoding="utf-8"))
    expected_upper = {f.upper() for f in settings_fields if f != "model_config"}
    missing = sorted(expected_upper - env_keys)
    extra = sorted(env_keys - expected_upper)
    if missing:
        print("In Settings but not in .env.example:", ", ".join(missing))
    if extra:
        print("In .env.example but not detected from config.py:", ", ".join(extra))
    if not missing and not extra:
        print("env sync OK (heuristic match).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
