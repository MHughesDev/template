# scripts/queue_top_item.py
"""Print the first open queue row as one line (JSON) for agents."""

from __future__ import annotations

import csv
import io
import json
import sys
from pathlib import Path

OPEN_FIELDS = [
    "id",
    "batch",
    "phase",
    "category",
    "summary",
    "dependencies",
    "related_files",
    "notes",
    "created_date",
]


def _load_open_rows(path: Path) -> list[dict[str, str]]:
    raw = path.read_text(encoding="utf-8")
    lines = raw.splitlines()
    start = 0
    if lines and lines[0].startswith("#"):
        start = 1
    body = "\n".join(lines[start:])
    reader = csv.DictReader(io.StringIO(body))
    if list(reader.fieldnames or []) != OPEN_FIELDS:
        msg = f"{path}: expected columns {OPEN_FIELDS}, got {reader.fieldnames}"
        raise ValueError(msg)
    return list(reader)


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    path = root / "queue" / "queue.csv"
    if not path.is_file():
        err = {"error": "missing_file", "path": "queue/queue.csv"}
        print(json.dumps(err, ensure_ascii=False), file=sys.stderr)
        return 1
    try:
        rows = _load_open_rows(path)
    except ValueError as e:
        err = {"error": "invalid_csv", "detail": str(e)}
        print(json.dumps(err, ensure_ascii=False), file=sys.stderr)
        return 1
    if not rows:
        empty = {"error": "no_open_items", "message": "queue.csv has no data rows"}
        print(json.dumps(empty, ensure_ascii=False))
        return 0
    row = rows[0]
    item = {k: (row.get(k) or "").strip() for k in OPEN_FIELDS}
    print(json.dumps(item, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
