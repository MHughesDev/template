#!/usr/bin/env bash
# scripts/queue-archive.sh
# Move QUEUE_ID row from queue.csv to queuearchive.csv.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ -z "${QUEUE_ID:-}" ]]; then
  echo "Usage: QUEUE_ID=<id> make queue:archive" >&2
  exit 1
fi

exec python3 "$ROOT/scripts/queue_archive.py" "$QUEUE_ID" --root "$ROOT"
