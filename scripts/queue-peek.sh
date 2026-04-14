#!/usr/bin/env bash
# scripts/queue-peek.sh
# Print queue header and first open data row (read-only).

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
QUEUE="$ROOT/queue/queue.csv"

if [[ ! -f "$QUEUE" ]]; then
  echo "error: $QUEUE not found" >&2
  exit 1
fi

awk '
  /^#/ { next }
  NR==1 { print "HEADER:", $0; next }
  NF {
    print "ACTIVE ROW:", $0
    exit
  }
  END {
    if (NR < 2) print "No open rows in queue.csv"
  }
' "$QUEUE"
