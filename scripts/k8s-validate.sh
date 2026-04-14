#!/usr/bin/env bash
# scripts/k8s-validate.sh
# Validate rendered manifests with kubeconform if available.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OVERLAY="${OVERLAY:-dev}"

if command -v kubeconform >/dev/null 2>&1; then
  kubectl kustomize "$ROOT/deploy/k8s/overlays/$OVERLAY" | kubeconform -strict -summary
else
  kubectl kustomize "$ROOT/deploy/k8s/overlays/$OVERLAY" >/dev/null
  echo "k8s:validate OK (kubeconform not installed — syntax only)"
fi
