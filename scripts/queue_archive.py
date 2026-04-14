# scripts/queue_archive.py
"""Move a queue row from queue.csv to queuearchive.csv."""

from __future__ import annotations

import argparse
import csv
import io
import sys
from datetime import date
from pathlib import Path

OPEN_FIELDS = [
    "id",
    "batch",
    "phase",
    "category",
    "summary",
    "dependencies",
    "notes",
    "created_date",
]
ARCHIVE_FIELDS = OPEN_FIELDS + ["status", "completed_date"]


def _load_queue(path: Path) -> tuple[str, list[dict[str, str]]]:
    raw = path.read_text(encoding="utf-8")
    lines = raw.splitlines()
    comment = ""
    start = 0
    if lines and lines[0].startswith("#"):
        comment = lines[0] + "\n"
        start = 1
    body = "\n".join(lines[start:])
    reader = csv.DictReader(io.StringIO(body))
    if list(reader.fieldnames or []) != OPEN_FIELDS:
        msg = f"{path}: expected columns {OPEN_FIELDS}, got {reader.fieldnames}"
        raise ValueError(msg)
    return comment, list(reader)


def _write_queue(path: Path, comment: str, rows: list[dict[str, str]]) -> None:
    buf = io.StringIO()
    if comment:
        buf.write(comment)
    writer = csv.DictWriter(buf, fieldnames=OPEN_FIELDS)
    writer.writeheader()
    writer.writerows(rows)
    path.write_text(buf.getvalue(), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Archive a queue row by id")
    parser.add_argument("queue_id")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    root = args.root
    q_path = root / "queue" / "queue.csv"
    a_path = root / "queue" / "queuearchive.csv"

    try:
        comment, rows = _load_queue(q_path)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1

    found: dict[str, str] | None = None
    kept: list[dict[str, str]] = []
    for row in rows:
        if row.get("id") == args.queue_id:
            found = row
        else:
            kept.append(row)

    if found is None:
        print(f"id {args.queue_id!r} not found in queue.csv", file=sys.stderr)
        return 1

    _write_queue(q_path, comment, kept)

    arch_row = {k: found.get(k, "") for k in OPEN_FIELDS}
    arch_row["status"] = "done"
    arch_row["completed_date"] = date.today().isoformat()

    a_path.parent.mkdir(parents=True, exist_ok=True)
    file_exists = a_path.exists() and a_path.stat().st_size > 0
    with a_path.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=ARCHIVE_FIELDS)
        if not file_exists:
            handle.write("# queue/queuearchive.csv\n")
            writer.writeheader()
        writer.writerow(arch_row)

    print(f"Archived {args.queue_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
