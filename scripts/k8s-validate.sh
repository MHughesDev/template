#!/usr/bin/env bash
# scripts/k8s-validate.sh
# Validate rendered manifests for each overlay (requires kubectl).

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if ! command -v kubectl >/dev/null 2>&1; then
  echo "error: kubectl required" >&2
  exit 1
fi

for o in dev staging prod; do
  echo "== overlay: $o"
  kubectl kustomize "$ROOT/deploy/k8s/overlays/$o" | kubectl apply --dry-run=client -f - >/dev/null
done
echo "k8s-validate: OK"
