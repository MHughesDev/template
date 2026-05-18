---
doc_id: "6.14"
title: "database recovery runbook"
section: "Operations"
status: "current"
summary: "Database recovery procedures for corruption, accidental deletion, failed migrations, and connection failures."
updated: "2026-05-17"
---

# Database Recovery Runbook

## Purpose

Recover from database corruption, accidental data deletion, failed migrations, connectivity loss, and other database failure scenarios.

## Prerequisites

- Database backups are configured and verified
- Access to backup storage (S3, cloud provider, etc.)
- kubectl access to cluster
- Database credentials available
- Understanding of last known good state

---

## Scenario 1: Failed Migration

**Symptoms:**
- Deployment fails with migration error
- Alembic reports `CommandError` or `OperationalError`
- Application crashes on startup with schema mismatch

**Impact:** Application cannot start or connect to database.

### Diagnosis

```bash
# Check migration status
cd apps/api
alembic current
# Shows current revision

# View migration history
alembic history --verbose

# Check for multiple heads (indicates branching issue)
alembic heads
# Should show single head; multiple = problem
```

### Resolution

#### Option A: Fix Forward (Recommended for Production)

If migration is complex or data would be lost on downgrade:

```bash
# 1. Create new migration that fixes the issue
alembic revision -m "fix_previous_migration" --autogenerate

# 2. Review generated migration
# Edit: apps/api/app/alembic/versions/<new_revision>.py

# 3. Apply fix
alembic upgrade head
```

#### Option B: Rollback Migration (If Safe)

Only if migration is reversible and no data loss:

```bash
# 1. Check what downgrade will do (CRITICAL: Review SQL!)
alembic downgrade -1 --sql

# 2. If safe, execute downgrade
alembic downgrade -1

# 3. Verify current revision
alembic current

# 4. Fix migration file or create new corrected one
# Edit the migration that failed, or create replacement

# 5. Re-apply corrected migration
alembic upgrade head
```

#### Option C: Stamp and Recreate (Nuclear Option)

**⚠️ DANGER:** Use only if database is disposable (e.g., dev environment):

```bash
# 1. Stop all applications
kubectl scale deployment/api --replicas=0 -n prod

# 2. Drop and recreate database (DESTRUCTIVE!)
# For managed database: use cloud console or CLI
# For self-hosted: 
dropdb your_database_name
createdb your_database_name

# 3. Stamp as current (mark as at base)
alembic stamp base

# 4. Apply all migrations fresh
alembic upgrade head

# 5. Restore data from backup, or re-seed
python scripts/seed_database.py  # if you have seed data

# 6. Restart applications
kubectl scale deployment/api --replicas=3 -n prod
```

---

## Scenario 2: Data Corruption

**Symptoms:**
- Users report missing or incorrect data
- Database integrity errors in logs
- Checksum mismatches on tables
- Constraint violations on supposedly valid data

**Impact:** Data quality issues, potential data loss.

### Diagnosis

```bash
# 1. Identify affected tables
# Check application logs for errors
kubectl logs -n prod deployment/api | grep -i "integrity\|constraint\|foreign key"

# 2. Check database consistency
psql $DATABASE_URL -c "
  SELECT schemaname, tablename, n_tup_ins, n_tup_upd, n_tup_del
  FROM pg_stat_user_tables
  ORDER BY n_tup_upd DESC;
"

# 3. Look for unusual patterns
psql $DATABASE_URL -c "
  SELECT table_name, 
         pg_size_pretty(pg_total_relation_size(quote_ident(table_name)))
  FROM information_schema.tables
  WHERE table_schema = 'public'
  ORDER BY pg_total_relation_size(quote_ident(table_name)) DESC;
"
```

### Resolution

#### Option A: Restore from Backup (Recommended)

```bash
# 1. Stop application to prevent further corruption
kubectl scale deployment/api --replicas=0 -n prod

# 2. Identify last known good backup
# Check your backup storage:
# - AWS: aws s3 ls s3://your-backup-bucket/
# - GCP: gsutil ls gs://your-backup-bucket/
# - Self-hosted: ls /backup/directory/

# 3. Restore from backup
# For AWS RDS:
aws rds restore-db-instance-to-point-in-time \
  --source-db-instance-identifier prod-db \
  --target-db-instance-identifier prod-db-recovery \
  --restore-time "2026-05-17T10:00:00Z"  # Before corruption

# For DigitalOcean:
doctl databases replica create prod-db \
  --name prod-db-recovery \
  --restore-from-time "2026-05-17T10:00:00Z"

# For pg_dump backup:
gunzip < backup_2026-05-17_10-00-00.sql.gz | psql $DATABASE_URL

# 4. Verify data integrity
psql $DATABASE_URL -c "SELECT COUNT(*) FROM users;"
psql $DATABASE_URL -c "SELECT COUNT(*) FROM items;"
# Compare to expected counts

# 5. Restart application
kubectl scale deployment/api --replicas=3 -n prod

# 6. Verify functionality
make smoke-test ENV=production
```

#### Option B: Manual Data Repair (If Scope is Small)

For small, isolated data issues:

```bash
# 1. Connect to database
psql $DATABASE_URL

# 2. Query corrupted data
SELECT * FROM items WHERE created_at IS NULL;

# 3. Fix specific records (if known good state)
UPDATE items SET created_at = NOW() WHERE created_at IS NULL;

# 4. Verify fix
SELECT * FROM items WHERE id = <specific_id>;
```

**⚠️ Warning:** Manual repairs risk making corruption worse. Document all changes.

---

## Scenario 3: Accidental Table/Row Deletion

**Symptoms:**
- Table or rows missing after mistaken DROP/DELETE
- Application errors: "relation does not exist"
- Foreign key violations due to missing parent records

**Impact:** Data loss, application failures.

### Immediate Response

```bash
# 1. STOP all writes immediately
kubectl scale deployment/api --replicas=0 -n prod

# 2. Document what was deleted (timestamp, table, estimated rows)
# Check logs if available:
kubectl logs -n prod deployment/api --previous | grep -i "delete\|drop"
```

### Recovery

#### Option A: Point-in-Time Recovery (Managed Databases)

**AWS RDS:**
```bash
# Restore to specific point in time (before deletion)
aws rds restore-db-instance-to-point-in-time \
  --source-db-instance-identifier prod-db \
  --target-db-instance-identifier prod-db-recovery \
  --restore-time "2026-05-17T14:30:00Z"  # 5 minutes before deletion

# Once verified, rename instances
aws rds modify-db-instance \
  --db-instance-identifier prod-db \
  --new-db-instance-identifier prod-db-old \
  --apply-immediately

aws rds modify-db-instance \
  --db-instance-identifier prod-db-recovery \
  --new-db-instance-identifier prod-db \
  --apply-immediately
```

**GCP Cloud SQL:**
```bash
# Restore from backup
gcloud sql backups restore \
  --restore-time "2026-05-17T14:30:00Z" \
  --instance=prod-db
```

**DigitalOcean:**
```bash
# Create fork from point in time
doctl databases replica create prod-db \
  --name prod-db-recovery \
  --restore-from-time "2026-05-17T14:30:00Z"

# Verify, then switch connection string
# Update secret and restart pods
```

#### Option B: Restore Specific Table from Backup

If only one table was deleted:

```bash
# 1. Extract table from backup
# If using pg_dump custom format:
pg_restore --table=deleted_table_name backup.dump > deleted_table.sql

# 2. Recreate table structure (if needed)
psql $DATABASE_URL < deleted_table_schema.sql

# 3. Load data
psql $DATABASE_URL < deleted_table.sql

# 4. Verify and fix sequences
psql $DATABASE_URL -c "
  SELECT setval('deleted_table_id_seq', 
                 (SELECT MAX(id) FROM deleted_table));
"

# 5. Restart application
kubectl scale deployment/api --replicas=3 -n prod
```

#### Option C: Logical Replication (If Configured)

If you have streaming replication to standby:

```bash
# 1. Promote standby to primary
# Procedure depends on your replication setup

# 2. Switch application to promoted standby
# Update DATABASE_URL in secrets

# 3. Verify data integrity on standby
```

---

## Scenario 4: Complete Database Loss

**Symptoms:**
- Database instance deleted or inaccessible
- Complete data loss event
- Provider incident (rare with managed databases)

**Impact:** Total service outage, all data potentially lost.

### Recovery Procedure

```bash
# Phase 1: Create New Database Instance

# AWS RDS
aws rds create-db-instance \
  --db-instance-identifier prod-db-new \
  --db-instance-class db.t3.medium \
  --engine postgres \
  --master-username postgres \
  --master-user-password "$NEW_PASSWORD"

# GCP Cloud SQL
gcloud sql instances create prod-db-new \
  --database-version=POSTGRES_16 \
  --tier=db-custom-2-4096 \
  --region=us-central1

# DigitalOcean
doctl databases create prod-db-new \
  --engine pg \
  --version 16 \
  --size db-s-2vcpu-4gb \
  --region nyc3

# Phase 2: Restore from Latest Backup

# Find latest backup
aws s3 ls s3://your-backup-bucket/ | sort | tail -1

# Download and restore
aws s3 cp s3://your-backup-bucket/latest_backup.sql.gz .
gunzip < latest_backup.sql.gz | psql $NEW_DATABASE_URL

# Phase 3: Update Application Connection

# Update secret with new connection string
kubectl create secret generic api-secrets \
  --from-literal=POSTGRES_SERVER="new-db-host" \
  --from-literal=POSTGRES_PASSWORD="$NEW_PASSWORD" \
  --namespace=prod \
  --dry-run=client -o yaml | kubectl apply -f -

# Restart application
kubectl rollout restart deployment/api -n prod

# Phase 4: Verification

# Check application logs
kubectl logs -n prod deployment/api

# Run health checks
make health-check ENV=production

# Run smoke tests
make smoke-test ENV=production
```

---

## Scenario 5: Connection Failures / Database Unreachable

**Symptoms:**
- Application logs: "could not connect to server"
- Intermittent timeouts
- Connection pool exhaustion errors

**Impact:** Service degradation or outage.

### Diagnosis

```bash
# 1. Check if database is running
# AWS:
aws rds describe-db-instances --db-instance-identifier prod-db

# GCP:
gcloud sql instances describe prod-db

# DigitalOcean:
doctl databases get <db-id>

# 2. Test connectivity from cluster
kubectl run -it --rm db-test --image=postgres:16 --restart=Never -- \
  timeout 5 psql "$DATABASE_URL" -c "SELECT 1"

# 3. Check connection pool status
# If you can connect:
psql $DATABASE_URL -c "
  SELECT count(*) as current_connections,
         (SELECT setting::int FROM pg_settings WHERE name = 'max_connections') as max_connections
  FROM pg_stat_activity;
"

# 4. Check firewall/network
# Verify security groups allow cluster IPs
# Verify VPC peering (if applicable)
```

### Resolution

#### Connection Pool Exhaustion

```bash
# 1. Identify long-running queries
psql $DATABASE_URL -c "
  SELECT pid, state, query_start, query
  FROM pg_stat_activity
  WHERE state = 'active' AND query_start < NOW() - interval '5 minutes';
"

# 2. Terminate runaway queries (carefully!)
SELECT pg_terminate_backend(<pid>);

# 3. Restart application to reset connection pools
kubectl rollout restart deployment/api -n prod

# 4. Increase pool size or add connection pooling (PgBouncer)
```

#### Network/Firewall Issues

```bash
# AWS: Update security group
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxx \
  --protocol tcp \
  --port 5432 \
  --source-group sg-cluster-nodes

# GCP: Update authorized networks
gcloud sql instances patch prod-db \
  --authorized-networks="10.0.0.0/8"

# DigitalOcean: Add trusted sources
doctl databases firewalls append <db-id> --rule k8s:<cluster-id>
```

#### Database Instance Failure

If managed database is down:

```bash
# 1. Check provider status page
# AWS: https://status.aws.amazon.com/
# GCP: https://status.cloud.google.com/
# DO: https://status.digitalocean.com/

# 2. If confirmed outage, promote read replica (if exists)
# Or restore from backup to new instance

# 3. Update connection string in application
# See Scenario 4 for restore procedure
```

---

## Scenario 6: Replication Lag (Read Replicas)

**Symptoms:**
- Stale data on read replicas
- Lag metrics > acceptable threshold
- Read-after-write inconsistencies

### Diagnosis

```bash
# Check replication lag
psql $PRIMARY_DATABASE_URL -c "
  SELECT client_addr, state, 
         pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn)) as lag
  FROM pg_stat_replication;
"

# Or for logical replication:
psql $REPLICA_DATABASE_URL -c "
  SELECT slot_name, 
         pg_size_pretty(pg_wal_lsn_diff(confirmed_flush_lsn, pg_current_wal_lsn())) as lag
  FROM pg_replication_slots;
"
```

### Resolution

```bash
# 1. Identify cause
# Large transaction? Long-running query? Network issues?

# 2. If necessary, redirect reads to primary temporarily
# Update application config to use primary for reads

# 3. Monitor lag decrease
watch -n 5 'psql $DATABASE_URL -c "SELECT NOW(), replication_lag;"'

# 4. If replica is stuck, recreate it
# AWS:
aws rds delete-db-instance \
  --db-instance-identifier prod-db-replica \
  --skip-final-snapshot

aws rds create-db-instance-read-replica \
  --db-instance-identifier prod-db-replica \
  --source-db-instance-identifier prod-db
```

---

## Backup and Restore Best Practices

### Backup Verification (Do This Regularly!)

```bash
# Monthly restore test

# 1. Create test restore instance
doctl databases create test-restore \
  --engine pg --version 16 --size db-s-1vcpu-1gb --region nyc3

# 2. Restore latest backup
gunzip < $(ls -t /backups/*.sql.gz | head -1) | psql $TEST_DATABASE_URL

# 3. Verify key tables and row counts
psql $TEST_DATABASE_URL -c "
  SELECT 'users' as table, count(*) as rows FROM users
  UNION ALL
  SELECT 'items', count(*) FROM items;
"

# 4. Compare to production counts
# Should match (within recent changes)

# 5. Clean up test instance
doctl databases delete test-restore --force
```

### Backup Retention Policy

| Environment | Full Backup Frequency | Retention | Point-in-Time |
|------------|----------------------|-----------|---------------|
| Production | Daily | 30 days | 7 days |
| Staging | Weekly | 14 days | 1 day |
| Development | Manual only | N/A | N/A |

---

## Emergency Contacts

Add your team's database contacts:

| Role | Name | Contact | Escalation Time |
|------|------|---------|-----------------|
| DBA / On-call | | PagerDuty/Slack | Immediate |
| Engineering Lead | | Slack/Phone | 15 min |
| Cloud Provider Support | | | |

---

## Post-Recovery Checklist

After any database recovery:

- [ ] Application fully operational
- [ ] All data verified (row counts, spot checks)
- [ ] No constraint violations
- [ ] Performance acceptable
- [ ] Backups running again
- [ ] Incident documented
- [ ] Root cause identified
- [ ] Prevention measures planned
- [ ] Team debrief completed

---

## Related Documents

| Document | Purpose |
|----------|---------|
| `docs/operations/runbooks/rollback.md` | Application rollback procedures |
| `docs/procedures/database-migration.md` | Migration SOP |
| `docs/operations/backups.md` | Backup configuration |
| `skills/backend/safe-migration-rollout.md` | Migration safety |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-05-17 | Initial database recovery runbook | Template |
