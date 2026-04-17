#!/usr/bin/env bash
# scripts/queue-pr-merge.sh
# Merge an open PR with a merge commit and delete the head branch (GitHub).
# Requires: gh CLI, authenticated (gh auth login).
#
# Usage:
#   From the PR branch (recommended before archiving the queue row):
#     make queue:pr-merge
#   When you are on another branch but know the PR number:
#     PR_NUMBER=123 make queue:pr-merge
#   Extra gh flags after -- are passed through (e.g. --admin if your policy allows).
#
# Typical queue completion order: merge PR (this target), then move the row to
# queuearchive.csv (make queue:archive-top or queue:archive), then make queue:validate.

set -euo pipefail

if ! command -v gh >/dev/null 2>&1; then
  echo "queue-pr-merge: gh (GitHub CLI) is not installed or not on PATH." >&2
  echo "Install: https://cli.github.com/ — then run: gh auth login" >&2
  exit 1
fi

if [[ -n "${PR_NUMBER:-}" ]]; then
  exec gh pr merge "$PR_NUMBER" --merge --delete-branch "$@"
fi

exec gh pr merge --merge --delete-branch "$@"
