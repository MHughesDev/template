# deploy/k8s/README.md

<!-- BLUEPRINT: Composer 2 implements from this structure -->
<!-- Per spec §26.10 item 247 -->

> PURPOSE: Kubernetes deployment documentation. Manifest structure, rendering, validation, deployment. Per spec §26.10 item 247.

## Directory Structure

> CONTENT: Kustomize-based structure:
> - deploy/k8s/base/ — Base manifests shared across all environments
> - deploy/k8s/overlays/dev/ — Dev patches (single replica, debug settings)
> - deploy/k8s/overlays/staging/ — Staging patches (lower scale)
> - deploy/k8s/overlays/prod/ — Production patches (full scale, PDB)

## Rendering

> CONTENT: Generate manifests from Kustomize: `make k8s:render` → `kustomize build deploy/k8s/overlays/dev`. Output to stdout for review.

## Validation

> CONTENT: Validate rendered manifests: `make k8s:validate` → `kubeconform` or `kubeval` against Kubernetes API schemas. Also validates: resource limits, probes, security context (via skills/devops/k8s-manifest-validator.py).

## Deployment Procedure

> CONTENT: Deploy to an environment: `kubectl apply -k deploy/k8s/overlays/<env>`. Wait for rollout: `kubectl rollout status deployment/api -n <namespace>`. Verify health: `make health:check` against the deployed endpoint.

## Environment Overlays

> CONTENT: Each overlay patches specific values from base: image tag, replica count, resource limits, environment-specific ConfigMap values. Never hardcode secrets in manifests — use Kubernetes Secrets or external secret management.
