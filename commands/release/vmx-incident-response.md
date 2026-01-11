# Incident Response

Emergency workflow for P0/P1 production incidents requiring immediate action.

---

## Severity Levels

| Level | Definition | Response Time |
|-------|------------|---------------|
| **P0** | Service down, data loss, security breach | Immediate |
| **P1** | Major feature broken, significant user impact | < 1 hour |
| **P2** | Feature degraded, workaround exists | < 4 hours |
| **P3** | Minor issue, low user impact | Next business day |

---

## Phase 1: Assess (First 5 minutes)

### Gather Information

```bash
# Check service health
curl -s https://[domain]/api/v1/admin/status | jq

# Check container status
docker ps -a

# Check recent logs
make logs | tail -100

# Check recent deployments
git log --oneline -5
gh release list --limit 3
```

### Quick Assessment Checklist

- [ ] What is broken? (specific symptoms)
- [ ] When did it start? (check logs, deploys)
- [ ] Who is affected? (all users, subset, specific feature)
- [ ] What changed recently? (deploy, config, external service)

---

## Phase 2: Mitigate (Next 10-15 minutes)

### Option A: Rollback

If recent deploy caused the issue:

```bash
# Rollback to previous version
make rollback

# Verify health after rollback
curl -s https://[domain]/api/v1/admin/status | jq
```

### Option B: Hotfix

If rollback isn't viable, apply minimal fix:

```bash
# Create hotfix branch
git checkout -b hotfix/incident-description main

# Make MINIMAL change to fix issue
# ... edit files ...

# Quick verification
make lint && make test

# Deploy hotfix
git push origin hotfix/incident-description
# Fast-track review and merge
```

### Option C: Disable Feature

If feature can be toggled:

```bash
# Update feature flag or config
# Redeploy with feature disabled
```

---

## Phase 3: Communicate

### Internal Communication

```
INCIDENT: [Brief description]
STATUS: [Investigating | Mitigating | Resolved]
IMPACT: [Who/what is affected]
ETA: [Expected resolution time or "Unknown"]
ACTIONS: [What we're doing]
```

### User Communication (if needed)

```
We're currently experiencing issues with [feature].
Our team is actively working on a fix.
We'll update you when service is restored.
```

---

## Phase 4: Resolve

### After Immediate Fix

- [ ] Verify service is healthy
- [ ] Confirm user-facing functionality works
- [ ] Monitor for 15-30 minutes for recurrence
- [ ] Update status communication

### Document the Incident

```markdown
## Incident Report: [Date] - [Brief Title]

**Duration:** [Start time] - [End time]
**Severity:** P[0/1/2]
**Impact:** [Users/features affected]

### Timeline
- HH:MM - Issue detected
- HH:MM - Investigation started
- HH:MM - Root cause identified
- HH:MM - Fix deployed
- HH:MM - Service restored

### Root Cause
[What actually caused the issue]

### Resolution
[What we did to fix it]

### Follow-up Actions
- [ ] [Action item 1]
- [ ] [Action item 2]

### Lessons Learned
- [What we'll do differently]
```

---

## Phase 5: Follow-up (Within 24 hours)

### Backfill Proper Fix

If hotfix was minimal/hacky:

1. Create proper fix branch
2. Full SDLC process (`/vmx-dev-cycle`)
3. Thorough testing
4. Replace hotfix with proper solution

### Post-Incident Review

- [ ] Document full incident timeline
- [ ] Identify root cause
- [ ] Create tickets for follow-up work
- [ ] Schedule post-mortem if P0/P1
- [ ] Update runbooks if needed

---

## Emergency Contacts

```
# Add your contacts here
# On-call: [contact]
# Escalation: [contact]
# Infrastructure: [contact]
```

---

## Quick Reference

| Action | Command |
|--------|---------|
| Check health | `curl .../api/v1/admin/status` |
| View logs | `make logs` |
| Rollback | `make rollback` |
| Deploy | `make deploy` |
| Container status | `docker ps -a` |

---

## Hotfix SDLC (Abbreviated)

For P0/P1 only - normal process for P2/P3:

1. **Fix** - Minimal change to resolve issue
2. **Expedited review** - Sync review, not async
3. **Deploy** - With rollback ready
4. **Backfill** - Proper fix within 24 hours
5. **Document** - Incident report

**Never skip:** Testing that fix works. Always verify before deploying.

---

*Stay calm. Assess first. Communicate clearly.*
