---
doc_id: "6.13"
title: "rollback runbook"
section: "Operations"
status: "current"
summary: "Application rollback, database migration rollback, and incident response procedures for products initialized from this template."
updated: "2026-05-17"
---

# Rollback Runbook

## Purpose

Revert to a previous known-good state when a deployment fails, causes errors, or introduces critical bugs. Covers application rollback, database migration rollback, and worker draining procedures.

## When to Rollback vs. Fix Forward

| Situation | Recommended Action | Rationale |
|-----------|-------------------|-----------|
| Deployment fails health checks | **Rollback** | No users affected, quick recovery |
| Database migration fails | **Rollback** | Data integrity at risk |
| High error rate (>10%) | **Rollback** | User impact, unknown cause |
| Security vulnerability exposed | **Rollback** | Immediate threat |
| Minor bug, low impact | **Fix forward** | Faster than rollback + redeploy |
| Feature incomplete | **Fix forward** | Rollback discards valid work |

---

## Triggers

Rollback immediately if any of these conditions are met:

- [ ] Health checks failing for >5 minutes after deployment
- [ ] Error rate >10% (measured by Sentry or logs)
- [ ] Critical functionality broken (login, payments, data access)
- [ ] Database migration failure during deploy
- [ ] Security incident related to new code
- [ ] Performance degradation >50% latency increase

---

## Phase 1: Assessment (2 minutes)

Before rolling back, confirm the scope:

```bash
# 1. Check deployment status
kubectl get deployments -n prod
kubectl rollout status deployment/api -n prod

# 2. Check pod status
kubectl get pods -n prod
kubectl describe pods -n prod -l app=api

# 3. Check recent logs
kubectl logs -n prod deployment/api --tail=50

# 4. Check error rate (if Sentry configured)
# Login to Sentry dashboard, check for spike

# 5. Check database status
kubectl logs -n prod deployment/api --tail=20 | grep -i "database\|migration\|error"
```

**Decision point:** If assessment confirms critical issue, proceed to Phase 2.

---

## Phase 2: Application Rollback

### Kubernetes Rollback (Standard)

```bash
# Identify current revision
kubectl rollout history deployment/api -n prod

# Rollback to previous revision
kubectl rollout undo deployment/api -n prod

# Monitor rollback
kubectl rollout status deployment/api -n prod --timeout=5m

# Verify pods are running
kubectl get pods -n prod

# Verify health endpoint
curl https://api.yourdomain.com/api/v1/utils/health-check/
```

**What this does:**
- Reverts to previous ReplicaSet (last known good image tag)
- Maintains database state (does NOT roll back migrations)
- Preserves existing pods until new ones are healthy

---

### Emergency Manual Rollback

If `rollout undo` fails:

```bash
# 1. Identify last known good image
kubectl get pods -n prod -o jsonpath='{..image}' | tr ' ' '\n' | sort | uniq

# 2. Manually set image to previous version
kubectl set image deployment/api \
  api=ghcr.io/your-org/your-repo:sha-LAST_KNOWN_GOOD \
  -n prod

# 3. Monitor
kubectl rollout status deployment/api -n prod

# 4. Verify
kubectl get pods -n prod
curl https://api.yourdomain.com/api/v1/utils/health-check/
```

---

## Phase 3: Database Migration Rollback

⚠️ **CRITICAL:** Database rollbacks are risky. Only perform if:
- Migration is reversible (Alembic `downgrade` exists)
- No data loss will occur (check migration SQL first)
- You have a database backup from before migration

### Safe Migration Rollback Procedure

```bash
# 1. Stop application (prevent new writes)
kubectl scale deployment/api --replicas=0 -n prod

# 2. Check migration history
cd apps/api
alembic history

# 3. See what downgrade will do (dry run)
alembic downgrade -1 --sql

# 4. If safe, execute downgrade
alembic downgrade -1

# 5. Verify database state
alembic current

# 6. Restart application with old image
kubectl scale deployment/api --replicas=3 -n prod
kubectl rollout status deployment/api -n prod
```

### Migration Rollback Decision Matrix

| Migration Type | Can Rollback? | Procedure |
|---------------|---------------|-----------|
| Add column (nullable) | ✅ Yes | `alembic downgrade -1` |
| Add column (non-nullable) | ⚠️ Careful | Check default values, may need data fix |
| Drop column | ❌ No | Restore from backup, data is lost |
| Rename column | ❌ No | Create new migration to rename back |
| Add index | ✅ Yes | `alembic downgrade -1` |
| Data migration | ⚠️ Case-by-case | May need custom downgrade logic |

---

## Phase 4: Verification

After rollback, verify:

```bash
# 1. Application health
curl -f https://api.yourdomain.com/api/v1/utils/health-check/

# 2. Key functionality
# Test login, critical API endpoints, database reads/writes

# 3. Error rates
# Check Sentry dashboard — should return to baseline

# 4. Performance
# Check response times — should return to baseline

# 5. Database connectivity
kubectl exec -n prod deployment/api -- \
  python -c "from app.core.db import engine; print('DB OK')"
```

---

## Phase 5: Communication

### Immediate (within 15 minutes)

Post in team channel (#incidents or similar):

```
🚨 INCIDENT: Rollback executed for production
- Issue: [brief description]
- Time: [timestamp]
- Action: Rolled back to [revision/image tag]
- Status: Monitoring
- ETA: 30 minutes for full verification
```

### Update (within 1 hour)

```
📊 UPDATE: Rollback verification complete
- Services restored: ✅
- Error rate: [current] (baseline: [normal])
- Next steps: [fix forward plan or deeper investigation]
- Lead: [@engineer]
```

### Post-Incident (within 24 hours)

Schedule postmortem to document:
- Root cause
- Why rollback was necessary
- Detection time
- Recovery time
- Prevention measures

---

## Special Cases

### Rollback with Database Schema Changes

If deployment included irreversible schema changes:

1. **Do NOT rollback application** — old code won't work with new schema
2. **Fix forward** with new deployment that:
   - Handles both old and new schema (expand/contract pattern)
   - Or reverts schema in new migration

### Rollback with Background Jobs

If workers are processing jobs:

```bash
# 1. Pause workers (stop picking up new jobs)
kubectl scale deployment/worker --replicas=0 -n prod

# 2. Wait for in-flight jobs to complete
# Monitor queue depth, wait for zero

# 3. Rollback application
kubectl rollout undo deployment/api -n prod

# 4. Restart workers
kubectl scale deployment/worker --replicas=3 -n prod
```

### Rollback with Feature Flags

If using feature flags (see `skills/backend/feature-flags.md`):

1. **First:** Disable feature flag (instant, no deploy needed)
2. **Then:** Plan rollback or fix forward

```bash
# Example: Disable feature via environment
kubectl set env deployment/api FEATURE_NEW_CHECKOUT=false -n prod
```

---

## Prevention: Rollback Readiness

### Before Every Deployment

- [ ] Database migration has `downgrade` function
- [ ] Migration tested on staging with rollback
- [ ] Feature flags available for high-risk changes
- [ ] Health checks will catch failures quickly
- [ ] Sentry alerts configured for error rate spikes

### Maintaining Rollback Capability

```bash
# Test rollback on staging monthly
kubectl rollout undo deployment/api -n staging
kubectl rollout status deployment/api -n staging

# Verify Alembic downgrades work
cd apps/api
alembic downgrade -1  # On staging DB
alembic upgrade head  # Restore
```

---

## Rollback Checklist

Use this during incidents:

**Assessment:**
- [ ] Issue confirmed (not transient)
- [ ] Scope understood (which services affected)
- [ ] Decision made: rollback vs. fix forward

**Execution:**
- [ ] Team notified in incident channel
- [ ] Application rollback executed
- [ ] Database status checked (migrations, connectivity)
- [ ] Application scaled back up
- [ ] Health checks passing

**Verification:**
- [ ] Error rate returned to normal
- [ ] Critical functionality tested
- [ ] No new issues introduced
- [ ] Team updated with status

**Follow-up:**
- [ ] Postmortem scheduled within 24h
- [ ] Root cause identified
- [ ] Prevention measures planned
- [ ] Documentation updated if needed

---

## Related Documents

| Document | Purpose |
|----------|---------|
| `docs/operations/deployment.md` | Standard deployment procedures |
| `docs/operations/runbooks/database-recovery.md` | Database failure scenarios |
| `docs/procedures/incident-rollback.md` | Incident response procedure |
| `skills/devops/rollout-rollback.md` | Rollout and rollback skill |

---

## Emergency Contacts

Add your team's emergency contacts:

| Role | Name | Contact | Escalation |
|------|------|---------|------------|
| On-call Engineer | | PagerDuty/Slack | 15 min |
| Engineering Lead | | Slack/Phone | 30 min |
| Database Admin | | Slack/Phone | Immediate |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-05-17 | Initial rollback runbook for template | Template |
