# skills/init/queue-seeder.py
"""Append template rows to queue.csv from a simple spec file (id|summary per line)."""

from __future__ import annotations

import argparse
import csv
import io
import sys
from datetime import date
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", type=Path, help="Lines: id|long summary text")
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    qpath = args.repo_root / "queue" / "queue.csv"
    if not qpath.is_file():
        print("Missing queue.csv", file=sys.stderr)
        return 1
    if not args.spec or not args.spec.is_file():
        print("Provide --spec file with rows id|summary")
        return 0
    raw = qpath.read_text(encoding="utf-8")
    lines = raw.splitlines()
    start = 1 if lines and lines[0].startswith("#") else 0
    comment = (lines[0] + "\n") if start else ""
    reader = csv.DictReader(io.StringIO("\n".join(lines[start:])))
    fieldnames = list(reader.fieldnames or [])
    existing = list(reader)
    today = date.today().isoformat()
    for line in args.spec.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("|", 1)
        if len(parts) != 2:
            continue
        qid, summary = parts[0].strip(), parts[1].strip()
        existing.append(
            {
                "id": qid,
                "batch": "1",
                "phase": "1",
                "category": "init",
                "summary": summary,
                "dependencies": "",
                "notes": "",
                "created_date": today,
            },
        )
    buf = io.StringIO()
    if comment:
        buf.write(comment)
    w = csv.DictWriter(buf, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(existing)
    qpath.write_text(buf.getvalue(), encoding="utf-8")
    print(f"Updated {qpath}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
