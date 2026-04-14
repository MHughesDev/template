#!/usr/bin/env bash
# scripts/k8s-render.sh
# Render Kustomize overlay to stdout (OVERLAY=dev|staging|prod).

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OVERLAY="${OVERLAY:-dev}"

if ! command -v kubectl >/dev/null 2>&1; then
  echo "error: kubectl required for kustomize build" >&2
  exit 1
fi

kubectl kustomize "$ROOT/deploy/k8s/overlays/$OVERLAY"
