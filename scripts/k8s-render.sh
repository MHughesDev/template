#!/usr/bin/env bash
# scripts/k8s-render.sh
# Render Kustomize overlay to stdout.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OVERLAY="${OVERLAY:-dev}"
exec kubectl kustomize "$ROOT/deploy/k8s/overlays/$OVERLAY"
