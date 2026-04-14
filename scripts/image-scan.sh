#!/usr/bin/env bash
# scripts/image-scan.sh
# Scan API image with Trivy (requires trivy CLI).

set -euo pipefail

TAG="${IMAGE_TAG:-template-api:local}"

if ! command -v trivy >/dev/null 2>&1; then
  echo "error: install trivy (https://aquasecurity.github.io/trivy/) for image scanning" >&2
  exit 1
fi

trivy image --severity HIGH,CRITICAL --exit-code 1 "$TAG"
