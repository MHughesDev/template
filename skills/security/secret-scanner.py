# skills/security/secret-scanner.py
"""Scan git-tracked text files for common secret patterns (informational)."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

PATTERNS = (
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"),
)


def tracked_files(repo: Path) -> list[str]:
    r = subprocess.run(
        ["git", "-C", str(repo), "ls-files"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [line.strip() for line in r.stdout.splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    hits = 0
    for rel in tracked_files(args.repo_root):
        if not rel.endswith((".py", ".md", ".yml", ".yaml", ".sh", ".toml", ".json")):
            continue
        path = args.repo_root / rel
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for pat in PATTERNS:
            if pat.search(text):
                print(f"Match: {rel}")
                hits += 1
                break
    print(f"Done. Files flagged: {hits}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
