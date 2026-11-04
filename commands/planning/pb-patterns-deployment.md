---
name: "pb-patterns-deployment"
title: "Deployment Patterns & Strategies"
category: "planning"
difficulty: "advanced"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-deployment', 'pb-preflight', 'pb-release', 'pb-database-ops', 'pb-dr']
last_reviewed: "2026-11-04"
last_evolved: ""
version: "2.0.0"
version_notes: "v2.0.0: Cut from 1076 to 163 lines: example code, walkthroughs and language sections removed; decisions, gotchas and when-to-use kept. /pb-preflight and /pb-deployment own the checklists; /pb-database-ops owns expand/contract; a feature flag is removed with its dead branch once the rollout is stable."
breaking_changes: ['Example code, walkthroughs and language sections removed; decisions and gotchas kept, constraints from removed code restated; deploy checklists live in /pb-preflight and /pb-deployment.']
---
# Deployment Patterns & Strategies

Reference guide for deployment strategies, patterns, and best practices. Use this to learn about and plan deployment approaches.

**For executing deployments**, use `/pb-deployment` (actionable deployment workflow). `/pb-preflight` is the pre-deploy gate; it and `/pb-deployment` own the checklists.

**Principle:** Every deployment strategy involves trade-offs.

Use `/pb-preamble` thinking: question your actual risk tolerance before choosing. Use `/pb-design-rules` thinking: balance Simplicity (don't use complex strategies you don't need) with Robustness (design for failure and rollback). Challenge whether you need the complexity of advanced strategies or if simpler approaches work.

**Resource Hint:** sonnet - Deployment pattern reference; implementation-level release strategy decisions.

## When to Use

- Choosing a deployment strategy for a new service or major release
- Evaluating risk tolerance and rollback requirements
- Planning blue-green, canary, or rolling deployments

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

**Disadvantages:**
- Expensive (need 2x resources)
- Database migrations must be compatible
- Can't test at full production load

**When to use:**
- Critical systems (payment, auth)
- Zero downtime required
- Budget allows 2x infrastructure

---

### Strategy 2: Canary Deployment (Balanced)

**How it works:**
1. Deploy new version alongside current
2. Send small % of traffic to new version (5%)
3. Monitor for errors
4. Gradually increase % (5% → 25% → 50% → 100%)
5. If errors spike, rollback the canary

**Disadvantages:**
- Longer deployment time (30min - 2 hours)
- Complex monitoring (compare v1 vs v2 metrics)
- Database must be compatible

**When to use:**
- Medium-risk deployments
- Want real traffic testing
- Can monitor and react quickly

---

### Strategy 3: Rolling Deployment (Fast)

**How it works:**
1. Gradually replace old instances with new
2. Take down one instance, deploy new, bring up
3. Repeat until all replaced
4. If errors detected, stop and rollback

**Disadvantages:**
- Temporary reduced capacity during rollout
- Must support both versions simultaneously (database!)
- Can't fully test before rolling out
- Harder rollback (must roll back the rollout)

**When to use:**
- Budget-constrained
- Fast deployments
- Confident in changes

---

## Feature Flags: Deploy Without Releasing

Deploy code dark behind a flag, then toggle it on or off without redeploying. Remove the flag and its dead branch once the rollout is stable.

---

## Database Migrations: Avoid Data Loss

**Problem:** Schema changes can break running code.

**Solution:** Expand, migrate, contract: old and new code both run against every intermediate schema. See `/pb-database-ops` Expand/Contract Pattern.

---

## Smoke Testing: Quick Validation After Deployment

### Data Persistence Validation

**Critical:** HTTP 200 response doesn't guarantee data was saved.

**Solution: Verify data persisted, not just HTTP 200**

**What to verify per application type:**

| Application | What to verify | Why |
|-------------|----------------|-----|
| E-commerce | Order saved, inventory decremented | Financial accuracy |
| SaaS | Workspace created, settings saved | Data loss is deal-breaker |
| API Service | Record persisted with correct values | Silent data loss |
| Messaging | Message in queue/database | Lost messages = lost data |
| Billing | Payment recorded, invoice generated | Revenue impact |

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

## Related Commands

- `/pb-deployment` - Execute deployment workflows
- `/pb-preflight` - Pre-deploy readiness gate
- `/pb-release` - Release orchestration and version management
- `/pb-database-ops` - Expand/contract migrations
- `/pb-dr` - Disaster recovery planning for deployment failures

---

*Category: Patterns | Reference Document | See `/pb-deployment` for actionable workflow*
