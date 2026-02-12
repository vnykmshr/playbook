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
version: "1.1.0"
version_notes: "Initial v2.11.0 (Phase 1-4 enhancements)"
breaking_changes: []
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

See `/pb-alex-infra` for the comprehensive infrastructure review framework and checklist.

**For backend-specific review, focus on:**
- **Failure Modes:** What database/service failures could cascade? How quickly detected?
- **Graceful Degradation:** If DB is slow, does API hang or return cached data?
- **Deployment Safety:** Is rollout gradual? Can rollback happen in < 5 minutes?
- **Observability:** Do logs include request context? Are metrics collected?
- **Capacity Planning:** Are database connection limits set? Load tested?

**Alex's Red Flags for Backend:**
- No health checks on database connections
- Single point of failure in service architecture
- Manual recovery process (can't auto-rollback)
- No monitoring of critical database queries

---

## Jordan's Testing Review

See `/pb-jordan-testing` for the comprehensive testing review framework and checklist.

**For backend-specific review, focus on:**
- **Error Path Testing:** Are timeouts, connection failures, and database errors tested?
- **Concurrency & Race Conditions:** Are async handlers tested under load? Shared state mutations safe?
- **Data Invariants:** Are database constraints enforced? Could data corruption happen?
- **Integration Testing:** Are real database queries tested (not just mocks)? Connection pooling validated?
- **Gap Detection:** What edge cases could cause production bugs? What's untested?

**Jordan's Red Flags for Backend:**
- Only happy path tested; error cases ignored
- All database calls mocked; real queries never executed
- No concurrency testing for async handlers
- Data invariants undocumented or untested

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

