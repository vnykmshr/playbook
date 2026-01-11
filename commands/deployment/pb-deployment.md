# Advanced Deployment Strategies

Deploy with confidence: minimize risk, maintain uptime, rollback quickly if needed.

---

## Purpose

Deployment is a controlled risk. Goals:
- **Zero downtime**: Users don't notice deployment
- **Fast rollback**: If something breaks, revert in seconds
- **Gradual rollout**: Start small, expand to all users
- **Safety first**: Catch problems before users see them

---

## Deployment Strategies

Choose strategy based on risk and scope.

### Strategy 1: Blue-Green Deployment (Safest)

**How it works:**
1. Keep current version running (Blue)
2. Deploy new version to separate environment (Green)
3. Test Green environment fully
4. Switch traffic to Green instantly
5. Old Blue stays running for quick rollback

**Diagram:**
```
Before:
  Users → [Blue - current version running]

Deploy:
  Users → [Blue - current version]
  [Green - new version deployed, not receiving traffic yet]

After:
  Users → [Green - new version live]
  [Blue - previous version, ready for rollback]
```

**Advantages:**
- Zero downtime (instant switch)
- Fast rollback (switch back to Blue)
- Full testing before traffic switch
- Two environments to compare

**Disadvantages:**
- Expensive (need 2x resources)
- Database migrations must be compatible
- Can't test at full production load

**When to use:**
- Critical systems (payment, auth)
- Zero downtime required
- Budget allows 2x infrastructure

**Implementation:**
```bash
# 1. Deploy new version to green environment
kubectl set image deployment/app-green app=myapp:v2.0

# 2. Wait for green to be ready
kubectl rollout status deployment/app-green

# 3. Test green (health checks pass)
curl http://green.internal/health  # Should return 200

# 4. Switch traffic
kubectl patch service app -p '{"spec":{"selector":{"version":"v2.0"}}}'

# 5. If broken, switch back instantly
kubectl patch service app -p '{"spec":{"selector":{"version":"v1.0"}}}'
```

---

### Strategy 2: Canary Deployment (Balanced)

**How it works:**
1. Deploy new version alongside current
2. Send small % of traffic to new version (5%)
3. Monitor for errors
4. Gradually increase % (5% → 25% → 50% → 100%)
5. If errors spike, rollback the canary

**Diagram:**
```
Phase 1: 5% traffic to v2.0
  90% → [v1.0 - stable]
  10% → [v2.0 - canary, low traffic]

Phase 2: 50% traffic to v2.0
  50% → [v1.0]
  50% → [v2.0]

Phase 3: 100% traffic to v2.0
  [v2.0 - all traffic, fully rolled out]
```

**Advantages:**
- Catch bugs with real traffic (small blast radius)
- Gradual rollout (if errors, affect few users)
- Monitor real user impact
- Easy to rollback (just reduce canary %)

**Disadvantages:**
- Longer deployment time (30min - 2 hours)
- Complex monitoring (compare v1 vs v2 metrics)
- Database must be compatible

**When to use:**
- Medium-risk deployments
- Want real traffic testing
- Can monitor and react quickly

**Implementation:**
```yaml
# Kubernetes Canary with Flagger
---
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: app
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: app
  service:
    port: 80

  # Gradually shift traffic
  skipAnalysis: false
  analysis:
    interval: 1m
    threshold: 5  # Max 5% error rate increase
    maxWeight: 50  # Max 50% traffic in canary phase
    stepWeight: 5  # Increase by 5% each minute

  metrics:
  - name: error-rate
    thresholdRange:
      max: 0.05  # Error rate < 5%
  - name: latency
    thresholdRange:
      max: 500m  # P99 latency < 500ms
```

**Manual canary (without Flagger):**
```bash
# 1. Deploy new version (initially gets 0% traffic)
kubectl set image deployment/app app=myapp:v2.0

# 2. Verify new pods are healthy
kubectl get pods -l app=app

# 3. Use load balancer to send 5% traffic to v2.0
kubectl patch service app -p '{"spec":{"trafficPolicy":{"canary":{"weight":5}}}}'

# 4. Monitor error rate and latency (should match v1.0)
# Watch metrics dashboard for 5 minutes

# 5. If good, increase to 25%
kubectl patch service app -p '{"spec":{"trafficPolicy":{"canary":{"weight":25}}}}'

# 6. If errors spike, rollback to 0%
kubectl patch service app -p '{"spec":{"trafficPolicy":{"canary":{"weight":0}}}}'
kubectl delete deployment app
```

---

### Strategy 3: Rolling Deployment (Fast)

**How it works:**
1. Gradually replace old instances with new
2. Take down one instance, deploy new, bring up
3. Repeat until all replaced
4. If errors detected, stop and rollback

**Diagram:**
```
Phase 1: Replace 1/5 instances
  [v1.0] [v1.0] [v1.0] [v1.0] [v2.0]

Phase 2: Replace 2/5 instances
  [v1.0] [v1.0] [v1.0] [v2.0] [v2.0]

Phase 3: All replaced
  [v2.0] [v2.0] [v2.0] [v2.0] [v2.0]
```

**Advantages:**
- No extra infrastructure needed
- Fast (completes in minutes)
- Automatic rollback on error
- Uses existing instance capacity

**Disadvantages:**
- Temporary reduced capacity during rollout
- Must support both versions simultaneously (database!)
- Can't fully test before rolling out
- Harder rollback (must roll back the rollout)

**When to use:**
- Budget-constrained
- Fast deployments
- Confident in changes

**Implementation:**
```yaml
# Kubernetes Rolling Update (default)
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  replicas: 5
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1  # Max 1 extra instance during rollout
      maxUnavailable: 0  # Min 0 unavailable (no service interruption)

  template:
    spec:
      containers:
      - name: app
        image: myapp:v2.0  # New version

        # Health check (stop rollout if failing)
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
```

---

## Feature Flags: Deploy Without Releasing

**Problem:** New code deployed but not visible to users (until enabled).

**Solution:** Feature flags to toggle features on/off without redeploying.

```python
# Feature flag pattern
def checkout():
    # Old code still runs (feature flag OFF)
    if feature_flag_enabled('new_checkout'):
        return new_checkout()  # New code (feature flag ON)
    else:
        return old_checkout()  # Old code
```

**Benefits:**
- Decouple deployment from release
- Deploy at any time (flag off)
- Release when ready (flag on)
- Instant rollback (flag off)
- A/B testing (flag on for 10% of users)

**Implementation:**
```python
# Using LaunchDarkly or similar
import ld_client

def checkout():
    user = get_current_user()

    # Check if flag enabled for this user
    if ld_client.variation('new-checkout', user, False):
        return new_checkout()
    else:
        return old_checkout()
```

**Deployment with flags:**
```bash
# Step 1: Deploy with feature flag OFF
kubectl set image deployment/app app=myapp:v2.0
# Feature is deployed but disabled

# Step 2: Monitor for errors (shouldn't be any, code not running)
# Wait 1 hour, no errors

# Step 3: Enable for internal team (1% of traffic)
flag.set_percentage('new_checkout', percentage=1)
# Monitor for 30 minutes

# Step 4: Enable for 10% of users
flag.set_percentage('new_checkout', percentage=10)
# Monitor for 1 hour

# Step 5: Enable for all users
flag.set_percentage('new_checkout', percentage=100)
```

**Cleanup:**
```python
# After feature stable for 2 weeks
def checkout():
    # Remove feature flag completely
    return new_checkout()  # Just use new code
```

---

## Database Migrations: Avoid Data Loss

**Problem:** Schema changes can break running code.

**Solution:** Gradual migrations, test thoroughly, rollback plan.

### Zero-Downtime Migration Pattern

**Step 1: Add new column (backwards compatible)**
```sql
ALTER TABLE users ADD COLUMN phone_number VARCHAR(20) DEFAULT NULL;
-- Old code: uses email
-- New code: will use phone_number, falls back to email if NULL
-- Both work simultaneously
```

**Step 2: Deploy code that reads new column**
```python
# New code reads new column, with fallback
def get_contact_method(user):
    if user.phone_number:
        return user.phone_number
    else:
        return user.email  # Fallback
```

**Step 3: Deploy code that writes new column**
```python
# New code writes to both old and new
def update_user(user):
    user.email = new_email  # Old column
    user.phone_number = new_phone  # New column
    user.save()
```

**Step 4: Backfill existing data**
```sql
-- Backfill old records (can be slow, non-blocking)
UPDATE users SET phone_number = email WHERE phone_number IS NULL;
-- Done slowly in background
```

**Step 5: Remove fallback, use only new column**
```python
# Remove fallback after backfill complete
def get_contact_method(user):
    return user.phone_number  # Just use new column
```

**Step 6: Remove old column (if really needed)**
```sql
ALTER TABLE users DROP COLUMN email;
-- Keep old column for 3+ months for emergency rollback
-- Then remove
```

**Why this pattern is safe:**
- Each step is backwards compatible
- Can rollback at any step
- No data loss
- No blocking locks on table
- Users not affected

---

## Rollback Strategies

### Quick Rollback (Use Feature Flags)

**Fastest:** Feature flag off (instant)
```bash
# Users still get old behavior, no code redeployment
flag.set_percentage('new_checkout', percentage=0)
# Done. Takes 1 second.
```

### Fast Rollback (Use Blue-Green)

**Fast:** Switch traffic to previous version (seconds)
```bash
# Instant traffic switch to previous version
kubectl patch service app -p '{"spec":{"selector":{"version":"v1.0"}}}'
# Takes 1-2 seconds, users see no interruption
```

### Rollback Last Deployment (Kubernetes)

**Medium:** Rollback last deployment (30 seconds)
```bash
kubectl rollout undo deployment/app
# Rolls back to previous version automatically
# Waits for new pods to be ready
# Takes ~30 seconds
```

### Manual Rollback (With Backups)

**For data corruption:** Restore from backup
```bash
# 1. Take database offline
kubectl scale deployment app --replicas=0

# 2. Restore from backup
pg_restore mydb backup_2024_01_11_1400.dump

# 3. Bring old version back online
kubectl set image deployment/app app=myapp:v1.0
kubectl scale deployment app --replicas=5

# Takes 5-10 minutes, data restored, old version running
```

### What NOT to Do

**❌ DON'T rollback by keeping both versions:**
```bash
# Bad: Users see inconsistency, data corruption
kubectl patch service app -p '{"spec":{"selector":{"version":"mixed"}}}'
# Some requests go to v1.0, some to v2.0, data gets out of sync
```

**❌ DON'T deploy fix immediately after rollback:**
```bash
# Bad: Rolled back to v1.0 due to bug
# Then immediately redeployed v2.0 with "fix"
# But the "fix" is untested

# Good: Rollback, investigate, fix, test, deploy
```

---

## Pre-Deployment Checklist

### Code Quality

- [ ] All tests passing (unit, integration, E2E)
- [ ] Code reviewed and approved
- [ ] Linter passing
- [ ] Type checking passing (if applicable)
- [ ] Security scan passed
- [ ] No console.log/print statements left

### Database

- [ ] Migration tested locally
- [ ] Rollback plan documented
- [ ] Backward compatible (old code + new schema works)
- [ ] Backup taken (or auto backup confirmed)
- [ ] Estimated migration time calculated

### Configuration

- [ ] All environment variables configured
- [ ] Secrets not in code (using secret manager)
- [ ] Feature flags ready (old feature on if needed)
- [ ] Monitoring/alerts configured

### Monitoring & Alerts

- [ ] Dashboard created (or updated)
- [ ] Key metrics monitored (latency, errors, resource usage)
- [ ] Alerts configured (error spike, latency spike, resource full)
- [ ] On-call engineer assigned
- [ ] Runbook prepared (what to do if something breaks)

### Communication

- [ ] Stakeholders informed (when deployment will happen)
- [ ] Maintenance window scheduled (if downtime needed)
- [ ] Support team briefed (possible issues)
- [ ] Rollback plan communicated (if needed)

---

## Deployment Checklist

### Before Deployment (1 hour)

- [ ] Check code one more time
- [ ] Check if anything changed since last review (git log)
- [ ] Verify tests still passing
- [ ] Check team is available (for 1-2 hours)
- [ ] Check production status (no current incidents)

### During Deployment

- [ ] Deploy code
- [ ] Wait for new instances to be healthy (health checks pass)
- [ ] Watch error metrics (should be same as before)
- [ ] Watch latency metrics (should be same as before)
- [ ] Wait 5-10 minutes to ensure stable

### After Deployment (30 min - 1 hour)

- [ ] Monitor error rate (no spike)
- [ ] Monitor latency (no spike)
- [ ] Monitor resource usage (no spike)
- [ ] Check logs for warnings/errors
- [ ] Smoke test key user flows
- [ ] Wait 1-2 hours before signing off (catch delayed issues)

### Post-Deployment

- [ ] Create post-deployment issue if any minor issues found
- [ ] Update deployment log
- [ ] Notify team (Slack message confirming successful deployment)

---

## Deployment by Strategy Comparison

| Strategy | Time | Risk | Rollback | Cost | Complexity |
|----------|------|------|----------|------|------------|
| Blue-Green | 5-10m | Low | Instant | High | Medium |
| Canary | 30m-2h | Low | Fast | Medium | High |
| Rolling | 5-15m | Medium | Slow | Low | Medium |
| Feature Flag | N/A | Very Low | Instant | Low | Low |

**Choose:**
- **Critical system:** Blue-Green
- **Confident in changes:** Canary
- **Budget constraints:** Rolling
- **Testing new feature:** Feature Flag

---

## Integration with Playbook

**Part of release and reliability:**
- `/pb-guide` — Section 8 covers deployment readiness
- `/pb-observability` — Monitoring during deployment
- `/pb-incident` — Rollback is incident recovery
- `/pb-release` — Release checklist includes deployment strategy

**Related Commands:**
- `/pb-observability` — Set up monitoring/alerts
- `/pb-guide` — CD requirements
- `/pb-incident` — Recovery if deployment breaks
- `/pb-security` — Deploy-time security checks

---

## Deployment Readiness Checklist

### Deployment Strategy

- [ ] Strategy chosen (Blue-Green, Canary, Rolling, Feature Flag)
- [ ] Deployment plan documented
- [ ] Rollback plan documented
- [ ] Estimated deployment time defined
- [ ] Risk level assessed (Low/Medium/High)

### Code & Database

- [ ] All tests passing
- [ ] Code review complete
- [ ] Database migration tested
- [ ] Backward compatibility verified
- [ ] Backup plan in place

### Monitoring

- [ ] Dashboard created
- [ ] Error rate alert configured
- [ ] Latency alert configured
- [ ] Resource alert configured
- [ ] On-call engineer assigned

### Communication

- [ ] Team informed (timing, strategy, risks)
- [ ] Support team briefed
- [ ] Stakeholders aware
- [ ] Rollback contact list ready
- [ ] Post-incident review time blocked

---

*Created: 2026-01-11 | Category: Deployment | Tier: M/L*

