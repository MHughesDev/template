#!/usr/bin/env bash
# scripts/profile-enable.sh
# Enable optional profile — delegates to skills/init/profile-resolver.py when present.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ -z "${PROFILE:-}" ]]; then
  echo "error: PROFILE=<web|mobile|ai|worker|...> required" >&2
  exit 1
fi

if [[ -f ".venv/bin/activate" ]]; then
  # shellcheck source=/dev/null
  source ".venv/bin/activate"
fi

RESOLVER="$ROOT/skills/init/profile-resolver.py"
if [[ -f "$RESOLVER" ]]; then
  exec python3 "$RESOLVER" --profile "$PROFILE"
fi

echo "Profile resolver not implemented yet; manual steps for profile: $PROFILE"
echo "- Update docker-compose.yml profiles"
echo "- Update .env.example flags"
echo "- See docs/procedures/enable-profile.md"
