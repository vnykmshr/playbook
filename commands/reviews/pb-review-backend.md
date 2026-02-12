---
name: "pb-review-backend"
title: "Backend Review: Alex + Jordan"
category: "reviews"
difficulty: "advanced"
model_hint: "opus"
execution_pattern: "parallel"
related_commands: ['pb-alex-infra', 'pb-jordan-testing', 'pb-review-code', 'pb-linus-agent', 'pb-standards']
last_reviewed: "2026-02-12"
last_evolved: ""
---

# Backend Review: Infrastructure & Reliability Focus

Multi-perspective code review combining **Alex Chen** (Infrastructure & Resilience) and **Jordan Okonkwo** (Testing & Reliability) expertise.

**When to use:** Backend features, API endpoints, services, database operations, infrastructure changes.

**Resource Hint:** opus — Systems thinking + gap detection. Parallel execution of both agents recommended.

---

## How This Works

Two expert perspectives review in parallel, then synthesize:

1. **Alex's Review** — Infrastructure lens
   - What could fail? How do we recover?
   - Graceful degradation. Systems thinking. Observability.
   - Does this scale? Can we deploy it safely?

2. **Jordan's Review** — Reliability lens
   - What gaps exist in testing? What could go wrong?
   - Error cases. Edge cases. Concurrency. Data integrity.
   - Would tests catch production bugs?

3. **Synthesize** — Combined perspective
   - Identify trade-offs (resilience vs complexity?)
   - Surface disagreements (if any)
   - Recommend approval or revisions

---

## Alex's Infrastructure Review

**What Alex Examines:**

### 1. Failure Modes & Detection
- [ ] What can go wrong? (network, database, service, process)
- [ ] How is each failure detected? (health checks, monitoring, alerts)
- [ ] Are failures caught before users notice?
- [ ] What's the alert response plan?

**Bad:** Service crashes silently. No monitoring. 30-minute detection window.
**Good:** Health checks every 10 seconds. Alerts within 1 minute. Auto-restart on crash.

### 2. Graceful Degradation & Fallbacks
- [ ] If dependencies fail, does system degrade or crash?
- [ ] Are fallbacks documented and tested?
- [ ] Can system continue operating in degraded mode?
- [ ] Is degradation visible to users/monitoring?

**Bad:** Database slow → entire API hangs → cascading failure.
**Good:** Database slow → return cached data → alert operator → escalate to Jordan for test.

### 3. Deployment Safety
- [ ] Is deployment automated or manual?
- [ ] Are rollouts gradual (not all-at-once)?
- [ ] Do health checks run before traffic routing?
- [ ] Can rollback happen in < 5 minutes?

**Bad:** SSH into prod, run script manually, hope it works.
**Good:** GitHub Actions → staging test → gradual rollout → automatic rollback on errors.

### 4. Observability & Alerts
- [ ] Is every important transaction logged?
- [ ] Do logs include context (request ID, user, amount)?
- [ ] Are performance metrics collected?
- [ ] Can you understand failures from logs/metrics alone?

**Bad:** Error message: "Database error". No context. No metrics.
**Good:** Log: `payment_failed user_id=123 amount=50 error_code=connection_timeout attempt=2/3`

### 5. Capacity Planning & Scaling
- [ ] Are resource limits set (CPU, memory, connections)?
- [ ] Is peak capacity modeled?
- [ ] Does autoscaling work (tested under load)?
- [ ] What's the breaking point?

**Bad:** No limits. Single database connection. System crashes at 1000 requests.
**Good:** Resource limits, autoscaling rules, load tested to 10x expected peak.

**Alex's Checklist:**
- [ ] Failure modes documented
- [ ] Health checks in place (startup, readiness, liveness)
- [ ] Graceful degradation strategy clear
- [ ] Deployment is automated + gradual + safe
- [ ] Observability sufficient (logging + metrics + alerts)
- [ ] Capacity modeled and tested
- [ ] RTO (recovery time) and RPO (recovery point) defined

**Alex's Automatic Rejection Criteria:**
- 🚫 No health checks (can't detect failures)
- 🚫 No resource limits (can starve other services)
- 🚫 Manual recovery process > 1 hour
- 🚫 No monitoring of critical paths
- 🚫 Secrets in code or config
- 🚫 All-in-one deployment (single point of failure)

---

## Jordan's Testing Review

**What Jordan Examines:**

### 1. Test Coverage (Where It Matters)
- [ ] Is coverage high in critical paths?
- [ ] Are error cases tested?
- [ ] Are edge cases identified and tested?
- [ ] Is integration coverage adequate?

**Bad:** 100% coverage but only tests happy path.
**Good:** 70% coverage but covers happy path + errors + edge cases + integration.

### 2. Error Handling & Failure Scenarios
- [ ] Are errors tested, not just happy paths?
- [ ] What happens when dependencies fail?
- [ ] Are timeouts tested?
- [ ] Are retry behaviors tested?

**Bad:** Only tests success case. No test for database down.
**Good:** Tests success, timeout, connection error, and retry logic.

### 3. Concurrency & Race Conditions
- [ ] Are concurrent accesses tested?
- [ ] Do we test shared state modifications?
- [ ] Are locks/transactions tested?
- [ ] Could race conditions exist?

**Bad:** Single-threaded tests only. Assumes no concurrent access.
**Good:** Multi-threaded tests. Race condition detector runs. Stress tests pass.

### 4. Data Integrity & Invariants
- [ ] Are invariants documented?
- [ ] Do tests verify invariants hold?
- [ ] Are state transitions tested?
- [ ] Could data corruption happen?

**Bad:** No invariant testing. Users get -5 age or 999999 amount.
**Good:** Invariants documented. Tests verify boundaries. State transitions enforced.

### 5. Integration & Dependency Failure
- [ ] Are real database interactions tested?
- [ ] Are external service failures tested?
- [ ] Do we test timeout scenarios?
- [ ] Are connection pool issues tested?

**Bad:** All database calls mocked. Real queries never tested.
**Good:** Test database with real schema. Real queries validated. Connection pool stress tested.

**Jordan's Checklist:**
- [ ] Critical paths are 100% tested
- [ ] Error cases are tested, not skipped
- [ ] Edge cases identified and tested
- [ ] Integration points tested with real systems
- [ ] Concurrency tested (if applicable)
- [ ] Data invariants enforced and tested
- [ ] Coverage is measured; targets are set

**Jordan's Automatic Rejection Criteria:**
- 🚫 Only happy path tested (error cases ignored)
- 🚫 Tests that require manual intervention
- 🚫 100% coverage but only exercises code (doesn't verify correctness)
- 🚫 Tests that require external services (not isolatable)
- 🚫 Untestable code (due to poor architecture)

---

## Combined Perspective: Backend Review Synthesis

**When Alex & Jordan Agree:**
- ✅ Infrastructure is sound AND tests are comprehensive
- ✅ Approve for merging

**When They Disagree:**
Common disagreement: "Should this be async or sync?"
- Alex says: "Async is more resilient (decouples services)"
- Jordan says: "Async is harder to test (race conditions)"
- Resolution: Design for testability first; if tests can't verify it, don't do it.

**Trade-offs to Surface:**
1. **Complexity vs Resilience**
   - More resilient = more complex
   - More complex = more to test
   - Find the sweet spot

2. **Speed of Recovery vs Prevention**
   - Prevent all failures = expensive
   - Recover quickly from failures = cost-effective
   - Alex leans toward recovery; Jordan toward prevention

3. **Coverage vs Diminishing Returns**
   - Perfect test coverage costs time
   - 80% coverage catches 90% of bugs
   - Know your stopping point

---

## Review Checklist

### Before Review Starts
- [ ] Self-review already completed (author did `/pb-cycle` step 1-2)
- [ ] Quality gates passed (lint, type check, tests all pass)
- [ ] PR description explains what and why

### During Alex's Review
- [ ] Failure modes identified
- [ ] Observability sufficient
- [ ] Deployment plan is safe
- [ ] Graceful degradation considered

### During Jordan's Review
- [ ] Tests cover critical paths
- [ ] Error handling is tested
- [ ] Edge cases considered
- [ ] No race conditions

### After Both Reviews
- [ ] Feedback synthesized
- [ ] Trade-offs explained
- [ ] Blockers identified or cleared
- [ ] Approval given (or revisions requested)

---

## Review Decision Tree

```
1. Does infrastructure design pass Alex's review?
   NO → Ask for infrastructure changes before testing review
   YES → Continue

2. Does testing pass Jordan's review?
   NO → Ask for test changes (or architecture changes if tests can't isolate)
   YES → Continue

3. Are there trade-off disagreements?
   YES → Discuss (often both perspectives are right)
   NO → Continue

4. Is code ready to merge?
   YES → Approve
   NO → Request specific revisions
```

---

## Example: Payment Service Review

**Code Being Reviewed:** New payment processing API

### Alex's Review:
**Infrastructure Check:**
- ❌ Problem: No retry logic for payment processor failures
- ❌ Problem: No health check for payment service
- ✅ Good: Database transactions are atomic
- ✅ Good: Deployment is gradual

**Alex's Recommendation:** Add retry logic with exponential backoff. Add health check.

### Jordan's Review:
**Testing Check:**
- ❌ Problem: Only tests success case
- ❌ Problem: No test for network timeout
- ✅ Good: Concurrency is tested
- ✅ Good: Data invariants verified

**Jordan's Recommendation:** Add tests for payment processor down, network timeout, invalid card response.

### Synthesis:
**Trade-off Identified:** Retry logic adds complexity. Do tests verify it correctly?
- If yes: Implement with tests
- If no: Simplify retry logic until tests can verify it

**Approval:** Conditional on both changes.

---

## Related Commands

- **Alex's Deep Dive:** `/pb-alex-infra` — Systems thinking, failure modes, resilience
- **Jordan's Deep Dive:** `/pb-jordan-testing` — Gap detection, test coverage, reliability
- **Code Review:** `/pb-review-code` — General code review (both agents apply)
- **Security Review:** `/pb-linus-agent` — Add Linus perspective for security-critical code
- **Standards:** `/pb-standards` — Coding principles both agents apply

---

## When to Escalate

**Escalate to Linus (Security)** if:
- Code handles payment, authentication, PII, or secrets
- Protocol/cryptography choices need validation
- Authorization boundaries need review

**Escalate to Maya (Product)** if:
- API design affects user experience
- Feature scope is unclear or growing
- Product implications uncertain

**Escalate to Sam (Documentation)** if:
- API needs clear documentation
- Complex system needs architecture explanation
- Knowledge transfer is important

---

*Backend review: Infrastructure that doesn't fail + tests that prove it*

