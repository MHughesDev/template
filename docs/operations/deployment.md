---
doc_id: "6.10"
title: "deployment"
section: "Operations"
status: "current"
summary: "Cloud deployment procedures for products initialized from this template. Covers Kubernetes, Docker Compose, and validation workflows."
updated: "2026-05-17"
---

# Deployment Guide

## Purpose

This document provides cloud-agnostic deployment procedures for products initialized from this template. It covers the three supported deployment targets and the validation workflows that ensure safe deployments.

## Supported Deployment Targets

| Target | Use Case | Complexity | Cost |
|--------|----------|------------|------|
| **Kubernetes (K8s)** | Production workloads, scaling, high availability | Medium | $40-200/mo |
| **Docker Compose** | Single-node production, simpler architectures | Low | $20-50/mo |
| **Serverless** | Variable workloads, minimal ops (requires ADR) | Low | Usage-based |

## Prerequisites Before First Deployment

All products initialized from this template must complete these prerequisites:

- [ ] Domain purchased and DNS A records configured
- [ ] Container registry accessible (GHCR, ECR, GCR, etc.)
- [ ] Secrets stored in environment (GitHub/GitLab/GitOps)
- [ ] Database provisioned and network-accessible from cluster
- [ ] TLS certificate strategy confirmed (Let's Encrypt or custom)
- [ ] Email provider configured (SendGrid, SES, etc.) or disabled
- [ ] Sentry DSN created (or error tracking disabled)

See `docs/procedures/pre-deploy-checklist.md` for the complete checklist.

---

## Per-Environment Deployment

### Staging Environment

**Purpose:** Pre-production validation. mirrors production configuration with reduced scale.

**Procedure:**
```bash
# 1. Verify staging overlay is customized
cat deploy/k8s/overlays/staging/kustomization.yaml

# 2. Ensure secrets are in GitHub Environment 'staging'
# Repository Settings → Environments → staging → Secrets

# 3. Deploy via CI/CD (recommended)
git push origin main  # Triggers CD workflow for staging

# 4. Or deploy manually
kubectl apply -k deploy/k8s/overlays/staging
kubectl rollout status deployment/api -n staging

# 5. Verify deployment
make health-check ENV=staging
make smoke-test ENV=staging
```

**Staging-specific configurations:**
- 1-2 replicas (vs. 3+ in production)
- Smaller resource limits
- Debug logging enabled
- Same database version, smaller instance

---

### Production Environment

**⚠️ WARNING:** Never deploy to production without successful staging deployment.

**Procedure:**
```bash
# 1. Run pre-deploy checklist
make pre-deploy-check ENV=production

# 2. Apply database migrations (before app deployment)
make migrate ENV=production

# 3. Deploy via CI/CD (tag-based)
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0  # Triggers production deployment

# 4. Monitor rollout
kubectl rollout status deployment/api -n prod --timeout=5m

# 5. Verify health
make health-check ENV=production

# 6. Run smoke tests
make smoke-test ENV=production
```

**Production-specific configurations:**
- 3+ replicas for high availability
- Pod Disruption Budgets (PDB) configured
- Resource limits enforced
- Debug logging disabled
- Horizontal Pod Autoscaler (HPA) enabled

---

## Deployment Workflows

### GitHub Actions CI/CD (Default)

The template provides `.github/workflows/cd.yml` with this flow:

```
Push to main ──► Build image ──► Deploy to staging ──► Run tests
                                        │
Tag v* ─────────────────────────────────┘
     │
     ▼
Deploy to production ──► Smoke tests ──► Notify
```

**Required GitHub Environments:**
- `staging` — auto-deploy on main branch push
- `production` — manual/tag-based deployment with approval

**Required Secrets:**
- `KUBECONFIG` — Cluster access (base64-encoded)
- `SECRET_KEY` — Per-environment JWT signing key
- `POSTGRES_PASSWORD` — Database password
- `FIRST_SUPERUSER_PASSWORD` — Admin password
- `SMTP_PASSWORD` — Email service password
- `SENTRY_DSN` — Error tracking (optional)

---

### Manual Deployment (Emergency Only)

Use only when CI/CD is unavailable:

```bash
# 1. Build and push image
docker build -t ghcr.io/org/repo:manual-$(date +%s) -f apps/api/Dockerfile .
docker push ghcr.io/org/repo:manual-$(date +%s)

# 2. Update image in overlay
kubectl set image deployment/api \
  api=ghcr.io/org/repo:manual-$(date +%s) \
  -n prod

# 3. Monitor and verify
kubectl rollout status deployment/api -n prod
```

**Document all manual deployments in incident log.**

---

## Validation Workflows

### Pre-Deployment Validation

Run before any deployment:

```bash
make pre-deploy-check ENV=staging
```

Checks:
- No secrets in Git
- Required files present
- Kubernetes connection working
- Domain DNS resolution
- Database connectivity

### Health Checks

After deployment, verify:

```bash
# Application health
curl https://api.yourdomain.com/api/v1/utils/health-check/

# Kubernetes pod status
kubectl get pods -n prod

# Logs check
kubectl logs -n prod deployment/api --tail=100
```

### Smoke Tests

End-to-end validation:

```bash
make smoke-test ENV=staging
```

Tests:
- User registration
- Login flow
- Password reset email
- CRUD operations on primary entities
- File uploads (if applicable)

---

## Rollback Procedures

### Automatic Rollback (Kubernetes)

If deployment fails health checks:
```bash
kubectl rollout undo deployment/api -n prod
```

### Manual Rollback

See `docs/operations/runbooks/rollback.md` for:
- Identifying last known good image
- Database migration rollbacks
- Communication procedures

---

## Environment Configuration

### Environment Variables by Target

**Kubernetes:**
- Stored in GitHub Environment Secrets
- Injected as `envFrom: secretRef` in deployment
- ConfigMaps for non-sensitive configuration

**Docker Compose:**
- `.env.staging` and `.env.production` files
- Loaded via `env_file` in compose.yml
- Never commit to Git (add to `.gitignore`)

---

## Secrets Management

Three approaches supported:

| Approach | Setup Complexity | Security | Best For |
|----------|------------------|----------|----------|
| **GitHub Secrets** (default) | Low | Medium | MVP, small teams |
| **External Secrets Operator** | High | High | Compliance, scale |
| **Sealed Secrets** | Medium | High | GitOps workflows |

See `docs/security/secrets-management.md` for detailed setup.

---

## Troubleshooting

### Common Deployment Failures

**ImagePullBackOff:**
- Verify image tag exists: `docker pull <image>`
- Check registry credentials: `kubectl get secrets -n prod`
- Verify network access from cluster to registry

**CrashLoopBackOff:**
- Check logs: `kubectl logs -n prod deployment/api`
- Verify environment variables: `kubectl exec -n prod deployment/api -- env`
- Check database connectivity

**Pending Pods:**
- Check resource quotas: `kubectl describe resourcequota -n prod`
- Verify node capacity: `kubectl top nodes`
- Check for taints: `kubectl get nodes -o yaml | grep taints`

---

## Security Considerations

### Deployment Security Checklist

- [ ] Non-root container user (already in template)
- [ ] Read-only root filesystem (add if needed)
- [ ] Resource limits enforced
- [ ] Network policies restrict pod-to-pod traffic
- [ ] Secrets never logged or exposed in errors
- [ ] TLS 1.2+ only (enforced by Traefik)
- [ ] Container images scanned in CI: `make image-scan`

### Production Hardening

Beyond the baseline:
- Enable Pod Security Standards (restricted)
- Use private container registries
- Implement admission controllers (OPA/Kyverno)
- Enable audit logging
- Regular security scans: `make security:scan`

---

## Cost Optimization

### Right-Sizing Recommendations

| Environment | CPU Request | Memory | Replicas | Est. Monthly |
|-------------|-------------|--------|----------|--------------|
| Staging | 100m | 256Mi | 1-2 | $20-40 |
| Production (small) | 250m | 512Mi | 3 | $60-100 |
| Production (medium) | 500m | 1Gi | 3-5 | $150-250 |

### Cost Controls

- Set resource quotas per namespace
- Use HPA for automatic scaling (scale to zero if supported)
- Review unused Load Balancers
- Use spot/preemptible instances for non-critical workloads

---

## Related Documents

| Document | Purpose |
|----------|---------|
| `docs/procedures/cloud-deployment-setup.md` | First-time setup procedure |
| `docs/procedures/pre-deploy-checklist.md` | Pre-flight validation |
| `docs/security/secrets-management.md` | Secrets configuration |
| `docs/operations/runbooks/rollback.md` | Rollback procedures |
| `docs/operations/runbooks/database-recovery.md` | Database recovery |
| `skills/devops/deploy-to-kubernetes.md` | Agent skill for deployment |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-05-17 | Initial cloud-agnostic deployment guide | Template |
