---
doc_id: "5.35"
title: "cloud deployment setup"
section: "Procedures"
status: "current"
summary: "First-time setup procedure for deploying a product initialized from this template to cloud infrastructure."
updated: "2026-05-17"
---

# Cloud Deployment Setup Procedure

## Purpose

This procedure configures a newly initialized product for its first cloud deployment. Run this after `skills/init/repo_initialize.md` completes and before the first deployment to staging.

## When to Run

- Immediately after repository initialization
- When adding a new deployment environment (dev/staging/prod)
- When switching cloud providers or deployment targets

## Prerequisites

- Repository initialized from template (see `skills/init/repo_initialize.md`)
- Cloud provider account created (AWS/GCP/Azure/DigitalOcean)
- Domain name purchased (or decision to use temporary domain)
- Decision on secrets management approach (A, B, or C)

## Time Estimate

- Simple setup (GitHub Secrets + DigitalOcean): 2-3 hours
- Production setup (AWS + External Secrets): 4-6 hours

---

## Phase 1: Cloud Provider Setup (30 minutes)

### Step 1.1: Choose Provider and Region

| Provider | Recommended Region | Kubernetes Service |
|----------|-------------------|-------------------|
| AWS | us-east-1 / us-west-2 | EKS |
| GCP | us-central1 | GKE |
| Azure | East US | AKS |
| DigitalOcean | nyc3 / sfo3 | DOKS |

**Decision criteria:**
- Latency to your users
- Pricing (DOKS cheapest for small workloads)
- Existing team expertise
- Compliance requirements (data residency)

### Step 1.2: Create Kubernetes Cluster

**DigitalOcean (Quickest):**
```bash
# Via UI: Create → Kubernetes → Select version → 2 vCPU / 4GB nodes
# Or via doctl:
doctl kubernetes cluster create prod-cluster \
  --region nyc3 \
  --version 1.29 \
  --node-pool "name=worker;size=s-2vcpu-4gb;count=2;auto-scale=true;min-nodes=2;max-nodes=4"
```

**AWS EKS:**
```bash
# Use eksctl (simpler) or Terraform
eksctl create cluster \
  --name prod-cluster \
  --region us-east-1 \
  --node-type t3.medium \
  --nodes 2 \
  --nodes-min 2 \
  --nodes-max 4
```

**GCP GKE:**
```bash
gcloud container clusters create prod-cluster \
  --zone us-central1-a \
  --num-nodes 2 \
  --machine-type e2-medium \
  --enable-autoscaling \
  --min-nodes 2 \
  --max-nodes 4
```

### Step 1.3: Configure kubectl

```bash
# DigitalOcean
doctl kubernetes cluster kubeconfig save <cluster-id>

# AWS
aws eks update-kubeconfig --region us-east-1 --name prod-cluster

# GCP
gcloud container clusters get-credentials prod-cluster --zone us-central1-a

# Verify
kubectl get nodes
kubectl get namespaces
```

### Step 1.4: Create Namespaces

```bash
kubectl create namespace staging
kubectl create namespace prod

# Verify
kubectl get namespaces
```

---

## Phase 2: Domain and DNS (20 minutes)

### Step 2.1: Configure Domain

1. Purchase domain (Namecheap, Cloudflare, Google Domains)
2. Point nameservers to your DNS provider (Cloudflare recommended)
3. Create A records:

| Host | Type | Value |
|------|------|-------|
| api | A | <Load Balancer IP> |
| app | A | <Load Balancer IP> |
| traefik | A | <Load Balancer IP> (optional) |

**Get Load Balancer IP:**
```bash
# After installing ingress controller (e.g., Traefik, NGINX)
kubectl get svc -n ingress-nginx  # or -n traefik

# Output will show EXTERNAL-IP
```

### Step 2.2: Verify DNS

```bash
# Check propagation (may take 5-30 minutes)
dig api.yourdomain.com
nslookup app.yourdomain.com

# Should return your load balancer IP
```

---

## Phase 3: Container Registry (15 minutes)

### Step 3.1: Verify GHCR Access

The template uses GitHub Container Registry by default.

**Repository Settings:**
- Settings → Actions → General → Workflow permissions: Read and write
- Verify `GITHUB_TOKEN` has `packages: write` permission (already in cd.yml)

**Alternative registries:**
- AWS ECR: `aws ecr create-repository --repository-name myapp-api`
- GCP GCR: `gcloud artifacts repositories create myapp --repository-format=docker`
- DigitalOcean Registry: Create in UI

### Step 3.2: Update Image References

Edit these files with your registry:

**`deploy/k8s/overlays/staging/kustomization.yaml`:**
```yaml
images:
  - name: template-api
    newName: ghcr.io/your-org/your-repo/api  # Update this
    newTag: latest
```

**`.github/workflows/cd.yml`:**
```yaml
- uses: docker/login-action@v4
  with:
    registry: ghcr.io  # Change if using ECR/GCR/etc.
```

---

## Phase 4: Secrets Management Setup (30-45 minutes)

Choose ONE approach:

---

### Option A: GitHub Environment Secrets (Recommended for MVP)

**Step 4A.1: Generate Secrets**

```bash
# Run locally to generate secure values
export SECRET_KEY=$(openssl rand -hex 32)
export POSTGRES_PASSWORD=$(openssl rand -hex 16)
export FIRST_SUPERUSER_PASSWORD=$(openssl rand -hex 16)

# Print for copying to GitHub (don't save to file!)
echo "SECRET_KEY: $SECRET_KEY"
echo "POSTGRES_PASSWORD: $POSTGRES_PASSWORD"
```

**Step 4A.2: Add to GitHub**

Navigate to:
```
Repository → Settings → Environments → New environment
```

Create two environments:
- `staging`
- `production`

Add these secrets to EACH environment (values should be different per environment):

| Secret Name | Value | How to Generate |
|-------------|-------|-----------------|
| `SECRET_KEY` | 64-char hex | `openssl rand -hex 32` |
| `POSTGRES_PASSWORD` | 32-char hex | `openssl rand -hex 16` |
| `FIRST_SUPERUSER_PASSWORD` | 32-char hex | `openssl rand -hex 16` |
| `SMTP_PASSWORD` | API key | From SendGrid/AWS SES/etc. |
| `SENTRY_DSN` | DSN URL | From sentry.io project settings |
| `KUBECONFIG` | base64 kubeconfig | `cat ~/.kube/config \| base64` |

**Step 4A.3: Verify CI/CD Integration**

The template's `.github/workflows/cd.yml` already references these secrets. Verify this section exists:

```yaml
deploy-staging:
  environment: staging  # Pulls secrets from GitHub
  steps:
    - name: Deploy Secrets
      run: |
        kubectl create secret generic api-secrets \
          --from-literal=SECRET_KEY="${{ secrets.SECRET_KEY }}" \
          # ... other secrets
```

**Step 4A.4: Deploy Secrets Manually (if not using CI/CD)**

```bash
# For staging
kubectl create namespace staging --dry-run=client -o yaml | kubectl apply -f -

kubectl create secret generic api-secrets \
  --from-literal=SECRET_KEY="$SECRET_KEY" \
  --from-literal=POSTGRES_PASSWORD="$POSTGRES_PASSWORD" \
  --from-literal=FIRST_SUPERUSER_PASSWORD="$FIRST_SUPERUSER_PASSWORD" \
  --from-literal=SMTP_PASSWORD="$SMTP_PASSWORD" \
  --from-literal=SENTRY_DSN="$SENTRY_DSN" \
  --namespace=staging \
  --dry-run=client -o yaml | kubectl apply -f -

# Verify
kubectl get secrets -n staging api-secrets -o yaml
```

---

### Option B: External Secrets Operator

**When to use:** Compliance requirements, multiple services, production at scale

**Quick Start:**

1. **Install External Secrets Operator:**
   ```bash
   helm repo add external-secrets https://charts.external-secrets.io
   helm install external-secrets external-secrets/external-secrets \
     --namespace external-secrets \
     --create-namespace
   ```

2. **Configure Cloud Provider Access** (AWS example):
   ```bash
   # Create IAM role with SecretsManagerReadWrite policy
   # Configure IRSA (IAM Roles for Service Accounts)
   # See full guide in external documentation
   ```

3. **Store Secrets in AWS Secrets Manager:**
   ```bash
   aws secretsmanager create-secret \
     --name staging/api/SECRET_KEY \
     --secret-string "$SECRET_KEY"
   ```

4. **Create ExternalSecret Resource:**
   ```yaml
   apiVersion: external-secrets.io/v1beta1
   kind: ExternalSecret
   metadata:
     name: api-secrets
     namespace: staging
   spec:
     refreshInterval: 1h
     secretStoreRef:
       kind: ClusterSecretStore
       name: aws-secrets-manager
     target:
       name: api-secrets
     data:
       - secretKey: SECRET_KEY
         remoteRef:
           key: staging/api/SECRET_KEY
   ```

---

### Option C: Sealed Secrets (GitOps)

**When to use:** GitOps workflows (Flux/ArgoCD), multi-cloud, air-gapped

**Quick Start:**

1. **Install Sealed Secrets Controller:**
   ```bash
   helm repo add sealed-secrets https://bitnami-labs.github.io/sealed-secrets
   helm install sealed-secrets sealed-secrets/sealed-secrets \
     --namespace kube-system
   ```

2. **Install kubeseal CLI:**
   ```bash
   # macOS
   brew install kubeseal
   
   # Linux
   wget https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.24.0/kubeseal-linux-amd64 -O kubeseal
   chmod +x kubeseal
   sudo mv kubeseal /usr/local/bin/
   ```

3. **Create and Encrypt Secret:**
   ```bash
   # Create regular secret
   kubectl create secret generic api-secrets \
     --from-literal=SECRET_KEY="$SECRET_KEY" \
     --dry-run=client -o yaml > /tmp/secret.yaml
   
   # Encrypt with cluster's public key
   kubeseal --format yaml < /tmp/secret.yaml > deploy/k8s/overlays/staging/sealed-secret.yaml
   
   # Remove unencrypted file
   rm /tmp/secret.yaml
   
   # Commit the sealed secret (safe to commit!)
   git add deploy/k8s/overlays/staging/sealed-secret.yaml
   ```

---

## Phase 5: Database Setup (30 minutes)

### Step 5.1: Provision Managed Database

If not already done, provision a managed PostgreSQL instance:

**DigitalOcean:**
- UI: Create → Databases → PostgreSQL
- Select version 16, smallest instance for staging
- Note the connection string

**AWS RDS:**
```bash
aws rds create-db-instance \
  --db-instance-identifier staging-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --allocated-storage 20 \
  --master-username postgres \
  --master-user-password "$POSTGRES_PASSWORD"
```

**GCP Cloud SQL:**
```bash
gcloud sql instances create staging-db \
  --database-version=POSTGRES_16 \
  --tier=db-f1-micro \
  --storage-size=20GB
```

### Step 5.2: Configure Connection

Get connection details from your provider:
- Host (e.g., `staging-db.ondigitalocean.com`)
- Port (usually 5432, or 25060 for DigitalOcean)
- Database name (e.g., `defaultdb`)
- Username (e.g., `doadmin`)

Update the secret with these values. The secret should include:
- `POSTGRES_SERVER`
- `POSTGRES_PORT`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`

### Step 5.3: Configure Network Access

**Critical:** Database must be reachable from Kubernetes cluster nodes.

**DigitalOcean:**
- Database → Settings → Trusted Sources
- Add your Kubernetes cluster's node IPs

**AWS:**
- RDS → Security Groups
- Add inbound rule allowing cluster security group

**GCP:**
- Cloud SQL → Connections → Authorized networks
- Add cluster node IP ranges

### Step 5.4: Test Connectivity

```bash
# From local machine
psql "postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_SERVER:$POSTGRES_PORT/$POSTGRES_DB?sslmode=require"

# From Kubernetes cluster
kubectl run -it --rm db-test --image=postgres:16 --restart=Never -- \
  psql "postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_SERVER:$POSTGRES_PORT/$POSTGRES_DB?sslmode=require"
```

Both should connect successfully. If not, check:
- Firewall/security group rules
- Correct password in secret
- SSL mode (managed DBs usually require SSL)

---

## Phase 6: Email Provider Setup (15 minutes, optional)

Skip if not using email features (password reset, notifications).

**SendGrid (Recommended):**
1. Create account at sendgrid.com
2. Verify sender domain (add DNS records)
3. Create API key with "Mail Send" permissions
4. Add to secrets:
   ```bash
   SMTP_HOST=smtp.sendgrid.net
   SMTP_USER=apikey
   SMTP_PASSWORD=SG.xxxxxxxxx  # API key
   EMAILS_FROM_EMAIL=noreply@yourdomain.com
   ```

**Alternative: Disable email**
Edit `apps/api/app/core/config.py` or set:
```bash
EMAILS_ENABLED=false  # Skip SMTP configuration
```

---

## Phase 7: Error Tracking Setup (10 minutes, optional)

**Sentry:**
1. Create account at sentry.io
2. Create project → Select Python/FastAPI
3. Copy DSN:
   ```bash
   SENTRY_DSN=https://xxxxx@xxxxx.ingest.sentry.io/xxxxx
   ```
4. Add to environment secrets

**Alternative: Skip for now**
Leave `SENTRY_DSN` empty in secrets.

---

## Phase 8: Environment File Creation (15 minutes)

### Step 8.1: Create `.env.staging`

```bash
cp .env.example .env.staging
```

Edit values:
```bash
DOMAIN=staging.yourdomain.com
FRONTEND_HOST=https://staging.yourdomain.com
ENVIRONMENT=staging

POSTGRES_SERVER=<staging-db-host>
POSTGRES_PORT=25060
POSTGRES_DB=defaultdb
POSTGRES_USER=doadmin
# Password goes in GitHub Secret, not this file

SECRET_KEY=see-github-secret
FIRST_SUPERUSER=admin@yourdomain.com
FIRST_SUPERUSER_PASSWORD=see-github-secret

SMTP_HOST=smtp.sendgrid.net
SMTP_USER=apikey
SMTP_PASSWORD=see-github-secret
EMAILS_FROM_EMAIL=noreply@yourdomain.com

SENTRY_DSN=see-github-secret
```

### Step 8.2: Create `.env.production`

Same as staging but with production values:
```bash
DOMAIN=yourdomain.com
FRONTEND_HOST=https://yourdomain.com
ENVIRONMENT=production
# ... use production database host
```

**Important:** These `.env.*` files are for local reference only. Do not commit them.

Add to `.gitignore`:
```bash
.env.staging
.env.production
.env.*.local
```

---

## Phase 9: Kubernetes Overlay Customization (20 minutes)

### Step 9.1: Staging Overlay

Edit `deploy/k8s/overlays/staging/kustomization.yaml`:

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - ../../base

namespace: staging  # Changed from default

# CRITICAL: Update image references
images:
  - name: template-api
    newName: ghcr.io/YOUR_ORG/YOUR_REPO/api  # UPDATE
    newTag: latest
  - name: template-frontend
    newName: ghcr.io/YOUR_ORG/YOUR_REPO/frontend  # UPDATE
    newTag: latest

# Optional: Adjust replica count for staging
replicas:
  - name: api
    count: 1  # Staging: single replica is fine

configMapGenerator:
  - name: api-config
    behavior: merge
    literals:
      - ENVIRONMENT=staging
      - DOMAIN=staging.YOURDOMAIN.com  # UPDATE THIS
      - FRONTEND_HOST=https://staging.YOURDOMAIN.com  # UPDATE THIS
```

### Step 9.2: Production Overlay

Edit `deploy/k8s/overlays/prod/kustomization.yaml`:

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - ../../base

namespace: prod

images:
  - name: template-api
    newName: ghcr.io/YOUR_ORG/YOUR_REPO/api
    newTag: latest
  - name: template-frontend
    newName: ghcr.io/YOUR_ORG/YOUR_REPO/frontend
    newTag: latest

replicas:
  - name: api
    count: 3  # Production: 3 replicas for HA

configMapGenerator:
  - name: api-config
    behavior: merge
    literals:
      - ENVIRONMENT=production
      - DOMAIN=YOURDOMAIN.com
      - FRONTEND_HOST=https://YOURDOMAIN.com
```

### Step 9.3: Verify Overlays

```bash
# Test kustomize build
kustomize build deploy/k8s/overlays/staging > /tmp/staging.yaml
# Inspect /tmp/staging.yaml for correctness

# Test production overlay  
kustomize build deploy/k8s/overlays/prod > /tmp/prod.yaml
```

Both should produce valid Kubernetes YAML without errors.

---

## Phase 10: Pre-Deploy Validation (10 minutes)

### Step 10.1: Run Validation Script

```bash
make pre-deploy-check ENV=staging
```

Checks:
- Required files exist
- No secrets in Git
- Kubernetes connection working
- Domain DNS resolving
- Database connectivity

### Step 10.2: Fix Any Issues

Address any failures from the check script before proceeding.

---

## Phase 11: First Deployment (15 minutes)

### Step 11.1: Deploy to Staging

**Via CI/CD (Recommended):**
```bash
git add .
git commit -m "Configure staging deployment"
git push origin main
# Watch GitHub Actions: Actions tab → CD workflow
```

**Manual (if CI/CD not ready):**
```bash
# Build and push images
docker build -t ghcr.io/your-org/your-repo/api:$(git rev-parse --short HEAD) -f apps/api/Dockerfile .
docker push ghcr.io/your-org/your-repo/api:$(git rev-parse --short HEAD)

# Update image in overlay
kubectl set image deployment/api \
  api=ghcr.io/your-org/your-repo/api:$(git rev-parse --short HEAD) \
  -n staging

# Or apply full overlay
kubectl apply -k deploy/k8s/overlays/staging
```

### Step 11.2: Verify Staging

```bash
# Check pod status
kubectl get pods -n staging

# Check logs
kubectl logs -n staging deployment/api

# Health check
curl https://staging.yourdomain.com/api/v1/utils/health-check/

# Should return: {"status":"ok"}
```

### Step 11.3: Smoke Test

```bash
make smoke-test ENV=staging
```

Manual verification:
- Register new user
- Login
- Create/read/update/delete resources
- Test password reset email (if email configured)

---

## Phase 12: Production Deployment (15 minutes)

**⚠️ Only after staging is fully verified.**

### Step 12.1: Production-Specific Checks

- [ ] Secrets configured in GitHub Environment `production`
- [ ] Database provisioned and accessible
- [ ] Domain DNS points to production load balancer
- [ ] SSL certificate will auto-provision (Let's Encrypt)

### Step 12.2: Deploy to Production

**Via CI/CD (Recommended):**
```bash
git tag -a v0.1.0 -m "Initial production release"
git push origin v0.1.0
```

GitHub Actions will:
1. Build and push images
2. Deploy to staging (auto)
3. Run smoke tests
4. Deploy to production (manual approval or auto)
5. Verify production health

**Manual (if needed):**
```bash
# Run migrations first
export POSTGRES_SERVER=<prod-db-host>
# ... set other env vars
cd apps/api && python -m alembic upgrade head

# Deploy
kubectl apply -k deploy/k8s/overlays/prod
kubectl rollout status deployment/api -n prod --timeout=10m
```

### Step 12.3: Post-Deploy Verification

```bash
# Health check
curl https://yourdomain.com/api/v1/utils/health-check/

# Check pods
kubectl get pods -n prod

# Check logs for errors
kubectl logs -n prod deployment/api --tail=100

# Run smoke tests
make smoke-test ENV=production
```

---

## Verification Checklist

Before marking deployment complete:

- [ ] Kubernetes namespace created (staging/prod)
- [ ] Secrets stored in chosen provider (GitHub/External/Sealed)
- [ ] Kubernetes Secrets created in namespace
- [ ] Database accessible from cluster pods
- [ ] Migrations applied successfully
- [ ] Application pods running and ready
- [ ] Health endpoint returns 200 with `{"status":"ok"}`
- [ ] User registration works
- [ ] Login returns valid JWT
- [ ] Authenticated requests succeed
- [ ] Frontend loads (if applicable)
- [ ] TLS certificate valid (not self-signed)
- [ ] Logs aggregating without errors

---

## Next Steps

After setup completion:

1. **Document decisions** in `docs/adr/` (why you chose your provider, region, etc.)
2. **Train team** on deployment procedures
3. **Set up monitoring** (Sentry, logging aggregation)
4. **Configure backups** (database backup verification)
5. **Write runbooks** for common incidents

---

## Troubleshooting Common Setup Issues

### Issue: kubectl cannot connect
```bash
# Verify kubeconfig
kubectl config current-context
kubectl config view

# Fix: Re-run provider-specific kubeconfig command
```

### Issue: ImagePullBackOff
```bash
# Check image exists
docker pull ghcr.io/your-org/your-repo/api:latest

# Check imagePullSecrets (if private registry)
kubectl get secrets -n staging

# Check pod events
kubectl describe pod <pod-name> -n staging
```

### Issue: Database connection refused
```bash
# Verify network access
kubectl run -it --rm debug --image=postgres:16 --restart=Never -- \
  psql "postgresql://..."

# Check firewall/security group rules
# Verify credentials in secret
kubectl get secret api-secrets -n staging -o yaml
```

---

## Related Documents

| Document | Purpose |
|----------|---------|
| `docs/operations/deployment.md` | Ongoing deployment procedures |
| `docs/procedures/pre-deploy-checklist.md` | Pre-flight validation |
| `docs/security/secrets-management.md` | Secrets approach details |
| `skills/devops/deploy-to-kubernetes.md` | Agent skill for deployments |
| `docs/operations/runbooks/rollback.md` | Emergency procedures |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-05-17 | Initial cloud deployment setup procedure | Template |
