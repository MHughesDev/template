#!/usr/bin/env bash
# scripts/profile-enable.sh
# Placeholder for enabling optional app profiles.

set -euo pipefail

if [[ -z "${PROFILE:-}" ]]; then
  echo "Usage: PROFILE=web make profile:enable" >&2
  exit 1
fi
echo "Profile enablement for '$PROFILE' is manual in this template (update docs + deps)."
exit 0
