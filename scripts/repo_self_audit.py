# scripts/repo_self_audit.py
"""Lightweight repository self-audit: queue schema + critical paths + optional checks."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REQUIRED_PATHS = (
    "AGENTS.md",
    "spec/spec.md",
    "Makefile",
    "pyproject.toml",
    "queue/queue.csv",
    "queue/QUEUE_INSTRUCTIONS.md",
)


def run_queue_validate(root: Path) -> tuple[bool, str]:
    """Return (ok, message)."""

    script = root / "scripts" / "queue_validate.py"
    proc = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(root),
        capture_output=True,
        text=True,
        check=False,
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode == 0, out.strip() or ("OK" if proc.returncode == 0 else "failed")


def check_required_files(root: Path) -> list[str]:
    missing: list[str] = []
    for rel in REQUIRED_PATHS:
        if not (root / rel).is_file():
            missing.append(rel)
    return missing


def main() -> int:
    parser = argparse.ArgumentParser(description="Repository self-audit")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
    )
    args = parser.parse_args()
    root: Path = args.repo_root
    blocking: list[str] = []

    missing = check_required_files(root)
    if missing:
        blocking.append(f"Missing required files: {', '.join(missing)}")

    ok, msg = run_queue_validate(root)
    if not ok:
        blocking.append(f"Queue validation failed: {msg}")

    if blocking:
        print("# Audit: BLOCKING issues\n")
        for b in blocking:
            print(f"- {b}")
        return 1

    print("# Audit: OK\n")
    print("- Required files present")
    print(f"- Queue: {msg}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
