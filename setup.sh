#!/usr/bin/env bash
# setup.sh
# One-shot bootstrap: venv, editable install, .env, migrations.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

need() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "Missing required command: $1" >&2
    exit 1
  }
}

need python3
need make

if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi
# shellcheck source=/dev/null
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev]"

if [[ ! -f .env ]]; then
  cp .env.example .env
  echo "Created .env from .env.example — set JWT_SECRET_KEY before production."
fi

export PYTHONPATH="$ROOT"
make migrate
make lint
make fmt
make typecheck
make test
echo "Setup complete. Run ./run.sh or make dev to start the API."
