#!/usr/bin/env bash
# scripts/queue-archive.sh
# Move completed queue row to queuearchive.csv (QUEUE_ID required).

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ -z "${QUEUE_ID:-}" ]]; then
  echo "error: set QUEUE_ID=<id> (e.g. Q-001)" >&2
  exit 1
fi

exec python3 - "$ROOT" "${QUEUE_ID}" <<'PY'
from __future__ import annotations

import csv
import sys
from datetime import UTC, date
from pathlib import Path

repo = Path(sys.argv[1])
qid = sys.argv[2]
queue_path = repo / "queue" / "queue.csv"
archive_path = repo / "queue" / "queuearchive.csv"

today = date.today().isoformat()

def load_csv(path: Path) -> tuple[str, list[dict[str, str]], list[str]]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    preamble = ""
    if lines and lines[0].lstrip().startswith("#") and not lines[0].strip().lower().startswith("# id,"):
        preamble = lines[0] + "\n"
        lines = lines[1:]
    reader = csv.DictReader(lines)
    fieldnames = list(reader.fieldnames or [])
    rows = [row for row in reader if any(v.strip() for v in row.values())]
    return preamble, rows, fieldnames


q_pre, q_rows, q_fields = load_csv(queue_path)
a_pre, a_rows, a_fields = load_csv(archive_path)

if "status" not in a_fields or "completed_date" not in a_fields:
    print("error: queuearchive.csv missing status/completed_date columns", file=sys.stderr)
    sys.exit(1)

found = None
remaining: list[dict[str, str]] = []
for row in q_rows:
    if row.get("id", "").strip() == qid:
        found = row.copy()
    else:
        remaining.append(row)

if found is None:
    print(f"error: id {qid!r} not found in queue.csv", file=sys.stderr)
    sys.exit(1)

found["status"] = "done"
found["completed_date"] = today
a_rows.append(found)

with queue_path.open("w", encoding="utf-8", newline="") as fh:
    fh.write(q_pre)
    w = csv.DictWriter(fh, fieldnames=q_fields, lineterminator="\n")
    w.writeheader()
    w.writerows(remaining)

with archive_path.open("w", encoding="utf-8", newline="") as fh:
    fh.write(a_pre)
    w = csv.DictWriter(fh, fieldnames=a_fields, lineterminator="\n")
    w.writeheader()
    w.writerows(a_rows)

print(f"Archived {qid} (status=done, completed_date={today})")
print("Run: make queue-validate")
PY
