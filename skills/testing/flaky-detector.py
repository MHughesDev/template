# skills/testing/flaky-detector.py
"""Run pytest multiple times; report tests with mixed outcomes (best-effort)."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--path", default="apps/api/tests")
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    outcomes: dict[str, list[bool]] = {}
    for _ in range(args.runs):
        r = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                args.path,
                "-q",
                "--tb=no",
            ],
            cwd=str(args.repo_root),
            capture_output=True,
            text=True,
        )
        ok = r.returncode == 0
        # parse last line counts if available
        for line in (r.stdout or "").splitlines():
            if " passed" in line and "failed" in line:
                pass
        # Without junit, we only know global pass/fail per run
        outcomes.setdefault("suite", []).append(ok)
    mixed = [k for k, v in outcomes.items() if len(set(v)) > 1]
    if mixed:
        print("Inconsistent outcomes across runs (suite level):", outcomes)
    else:
        print("Suite outcome stable across runs:", outcomes.get("suite"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
