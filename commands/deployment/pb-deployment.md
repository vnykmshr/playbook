---
name: "pb-deployment"
title: "Deploy to Environment"
category: "deployment"
difficulty: "advanced"
model_hint: "opus"
execution_pattern: "sequential"
related_commands: ['pb-release', 'pb-patterns-deployment', 'pb-incident', 'pb-observability']
tags: ['design', 'testing', 'security', 'workflow', 'review']
last_reviewed: "2026-02-09"
last_evolved: ""
---
# Deploy to Environment

Execute deployment to target environment with surgical precision. This command guides you through discovery, pre-flight checks, execution, and verification.

**For deployment strategy reference** (blue-green, canary, rolling, feature flags), see `/pb-patterns-deployment`.

**Mindset:** Deployments are controlled risk. Use `/pb-preamble` thinking: challenge readiness assumptions, surface risks before deploying. Use `/pb-design-rules` thinking: prefer Simplicity (don't over-engineer deployment), ensure Robustness (have rollback ready), maintain Clarity (know exactly what's deploying).

**Resource Hint:** sonnet — deployment execution and verification

---

## When to Use This Command

- Deploying code changes to any environment (staging, production)
- After `/pb-release` triggers deployment
- Manual deployment outside release flow
- Rollback execution

---

## Phase 1: Discovery

Identify your project's deployment infrastructure.

### Step 1.1: Detect Deployment Method

```bash
# Check for common deployment patterns
ls -la Makefile 2>/dev/null && grep -E "deploy|release" Makefile
ls -la package.json 2>/dev/null && grep -E "deploy" package.json
ls -la .github/workflows/*.yml 2>/dev/null
ls -la docker-compose*.yml 2>/dev/null
ls -la Dockerfile 2>/dev/null
ls -la k8s/ kubernetes/ deploy/ 2>/dev/null
```

### Step 1.2: Identify Deployment Target

| Infrastructure | Indicators | Typical Command |
|----------------|------------|-----------------|
| **Makefile** | `make deploy` target | `make deploy` |
| **Docker Compose** | `docker-compose.yml` | `docker-compose up -d` |
| **Kubernetes** | `k8s/`, `kubectl` | `kubectl apply -f` |
| **Serverless** | `serverless.yml` | `serverless deploy` |
| **Platform** | Vercel, Netlify, Fly.io | `vercel --prod`, `flyctl deploy` |
| **SSH/rsync** | Deploy scripts | `./scripts/deploy.sh` |
| **CI/CD only** | GitHub Actions, GitLab CI | Push to trigger |

### Step 1.3: Document Deployment Flow

```markdown
## Deployment Configuration

**Target:** [staging/production]
**Method:** [Makefile/Docker/K8s/Platform/CI]
**Command:** [exact deployment command]
**Rollback:** [rollback command or procedure]
**Health Check:** [health check URL or command]
**Estimated Duration:** [time estimate]
```

---

## Phase 2: Pre-flight Checks

Verify everything is ready before deploying.

### Step 2.1: Branch & Code State

```bash
# Verify on correct branch
git branch --show-current

# Verify branch is clean
git status

# Verify up to date with remote
git fetch origin
git log --oneline HEAD..origin/main  # Should be empty or intentional

# Verify what's being deployed
git log --oneline origin/main..HEAD  # Your changes
```

**Checklist:**
- [ ] On correct branch (main for prod, feature for staging)
- [ ] Working tree clean (no uncommitted changes)
- [ ] Branch up to date with remote
- [ ] Know exactly what commits are deploying

### Step 2.2: CI/CD Status

```bash
# Check CI status
gh run list --limit 3
gh run view [RUN_ID]

# If PR exists, check PR status
gh pr checks [PR_NUMBER]
```

**Checklist:**
- [ ] CI pipeline passing
- [ ] All required checks green
- [ ] No failing tests

### Step 2.3: Environment Readiness

```bash
# Check target environment is reachable
curl -s [TARGET_URL]/health | jq

# Check dependencies are up
# (database, cache, external services)

# Verify secrets/config are in place
# (environment-specific checks)
```

**Checklist:**
- [ ] Target environment reachable
- [ ] Dependencies healthy
- [ ] Configuration/secrets ready
- [ ] Rollback plan confirmed

### Step 2.4: Pre-flight Summary

```markdown
## Pre-flight Status

**Deploying:** [commit hash] - [commit message]
**To:** [environment]
**CI:** PASS
**Environment:** READY
**Rollback:** [command/procedure documented]

**GO / NO-GO:** ___
```

---

## Phase 3: Execute Deployment

### Step 3.1: Notify (If Team Process)

```bash
# Slack/Discord notification (if applicable)
echo "🚀 Deploying [version] to [environment] - [your name]"
```

### Step 3.2: Run Deployment

Execute the deployment command identified in Discovery:

```bash
# Example patterns (use your project's actual command)

# Makefile
make deploy ENV=production

# Docker Compose
docker-compose -f docker-compose.prod.yml up -d --build

# Kubernetes
kubectl apply -f k8s/
kubectl rollout status deployment/[app-name]

# Platform (Fly.io example)
flyctl deploy --app [app-name]

# SSH/Script
./scripts/deploy.sh production
```

### Step 3.3: Monitor Deployment Progress

```bash
# Watch deployment status (K8s example)
kubectl rollout status deployment/[app-name] --timeout=5m

# Watch logs during deployment
kubectl logs -f deployment/[app-name] --tail=50

# Or platform-specific
flyctl logs --app [app-name]
```

**During deployment, watch for:**
- [ ] Deployment command completes without error
- [ ] New instances starting
- [ ] Health checks passing
- [ ] No crash loops

---

## Phase 4: Verify Deployment

### Step 4.1: Health Check

```bash
# Hit health endpoint
curl -s [PROD_URL]/health | jq

# Expected: {"status": "ok"} or similar
```

### Step 4.2: Smoke Test Critical Paths

```bash
# Test authentication (if applicable)
curl -s -X POST [PROD_URL]/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"..."}' | jq

# Test core API endpoint
curl -s [PROD_URL]/api/[core-endpoint] | jq

# Test frontend loads (if applicable)
curl -s -o /dev/null -w "%{http_code}" [PROD_URL]
```

**Smoke test checklist:**
- [ ] Health endpoint returns OK
- [ ] Authentication works
- [ ] Core API endpoints respond
- [ ] Frontend loads (if applicable)
- [ ] No errors in logs

### Step 4.3: Monitor Metrics

```bash
# Check error rates (tool-specific)
# Datadog, Grafana, CloudWatch, etc.

# Check recent logs for errors
kubectl logs deployment/[app-name] --tail=100 | grep -i error

# Check resource usage
kubectl top pods
```

**Metrics checklist:**
- [ ] Error rate normal (not spiking)
- [ ] Latency normal (not degraded)
- [ ] Resource usage normal
- [ ] No new errors in logs

---

## Phase 5: Finalize or Rollback

### If Verification Passes: Finalize

```bash
# Update deployment log (if maintained)
echo "[$(date)] Deployed [version] to [env] - SUCCESS" >> deployments.log

# Notify team
echo "✅ Deployment complete: [version] to [environment]"

# Tag deployment (optional)
git tag -a deploy-[env]-$(date +%Y%m%d-%H%M) -m "Deployed to [env]"
```

### If Verification Fails: Rollback

**Immediate rollback triggers:**
- Health check failing
- Error rate spike (>5% increase)
- Critical user flows broken
- Crash loops detected

```bash
# Rollback commands by platform

# Kubernetes
kubectl rollout undo deployment/[app-name]
kubectl rollout status deployment/[app-name]

# Docker Compose (restore previous image)
docker-compose -f docker-compose.prod.yml up -d [previous-image]

# Platform (Fly.io)
flyctl releases list --app [app-name]
flyctl deploy --image [previous-image]

# Makefile (if rollback target exists)
make rollback

# Manual: redeploy previous version
git checkout [previous-commit]
make deploy
```

**After rollback:**
1. Verify rollback successful (health check)
2. Notify team of rollback
3. Investigate root cause
4. Document in incident log
5. Run `/pb-incident` if production impact

---

## Deployment Checklist Summary

```
PHASE 1: DISCOVERY
[ ] Deployment method identified
[ ] Deployment command documented
[ ] Rollback procedure documented

PHASE 2: PRE-FLIGHT
[ ] Correct branch, clean state
[ ] CI passing
[ ] Environment ready
[ ] GO decision made

PHASE 3: EXECUTE
[ ] Team notified (if applicable)
[ ] Deployment command run
[ ] Deployment completed without error

PHASE 4: VERIFY
[ ] Health check passing
[ ] Smoke tests passing
[ ] Metrics normal
[ ] No new errors

PHASE 5: FINALIZE
[ ] Deployment logged
[ ] Team notified of success
[ ] OR rollback executed if issues
```

---

## Quick Reference

| Action | Command Pattern |
|--------|-----------------|
| Check CI | `gh run list --limit 3` |
| Health check | `curl -s [URL]/health \| jq` |
| Watch logs | `kubectl logs -f deployment/[app]` |
| Rollback (K8s) | `kubectl rollout undo deployment/[app]` |
| Check metrics | Platform-specific dashboard |

---

## Integration with Playbook

**Part of release workflow:**
- `/pb-release` — Orchestrates release (triggers this command)
- `/pb-patterns-deployment` — Strategy reference (blue-green, canary, etc.)
- `/pb-incident` — If deployment causes issues

**Related commands:**
- `/pb-observability` — Monitoring setup
- `/pb-hardening` — Infrastructure security
- `/pb-secrets` — Secrets management
- `/pb-database-ops` — Database migrations
- `/pb-dr` — Disaster recovery

---

## Related Commands

- `/pb-release` — Orchestrate versioned releases to production
- `/pb-patterns-deployment` — Deployment strategy reference (blue-green, canary, rolling)
- `/pb-incident` — Respond to production incidents caused by deployments
- `/pb-observability` — Set up monitoring and alerting for deployment verification

---

*Deploy with confidence. Verify before celebrating. Rollback without hesitation.*
