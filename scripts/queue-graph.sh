#!/usr/bin/env bash
# scripts/queue-graph.sh
# Emit Mermaid graph for queue dependencies.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
QUEUE="$ROOT/queue/queue.csv"

python3 - "$QUEUE" <<'PY'
from __future__ import annotations

import csv
import sys
from pathlib import Path

path = Path(sys.argv[1])
rows = []
with path.open(encoding="utf-8") as fh:
    for line in fh:
        if line.lstrip().startswith("#"):
            continue
        rows.append(line)
reader = csv.DictReader(rows)
print("graph TD")
for row in reader:
    rid = row.get("id", "").strip()
    if not rid:
        continue
    deps = row.get("dependencies", "").strip()
    for d in [x.strip() for x in deps.split(",") if x.strip()]:
        print(f"  {d} --> {rid}")
PY
