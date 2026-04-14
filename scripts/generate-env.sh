#!/usr/bin/env bash
# scripts/generate-env.sh
# Copy .env.example to .env if .env does not exist.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

EX="$ROOT/.env.example"
OUT="$ROOT/.env"

if [[ ! -f "$EX" ]]; then
  echo "error: .env.example missing" >&2
  exit 1
fi

if [[ -f "$OUT" ]]; then
  echo ".env already exists — not overwriting"
  exit 0
fi

cp "$EX" "$OUT"
echo "Created .env from .env.example — edit secrets before production."
