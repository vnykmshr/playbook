---
name: "pb-review-infrastructure"
title: "Infrastructure Review: Alex + Linus"
category: "reviews"
difficulty: "advanced"
model_hint: "opus"
execution_pattern: "parallel"
related_commands: ['pb-alex-infra', 'pb-linus-agent', 'pb-hardening', 'pb-deployment', 'pb-standards']
last_reviewed: "2026-02-12"
last_evolved: ""
version: "1.1.0"
version_notes: "Initial v2.11.0 (Phase 1-4 enhancements)"
breaking_changes: []
---

# Infrastructure Review: Resilience & Security Focus

Multi-perspective infrastructure code review combining **Alex Chen** (Infrastructure & Resilience) and **Linus Torvalds** (Security & Pragmatism) expertise.

**When to use:** Infrastructure changes, Terraform/Kubernetes configs, deployment pipelines, security configurations, system architecture changes.

**Resource Hint:** opus — Systems thinking + security hardening. Parallel execution of both agents recommended.

---

## How This Works

Two expert perspectives review in parallel, then synthesize:

1. **Alex's Review** — Resilience lens
   - What can fail? How do we recover?
   - Is the system designed for failure?
   - Can we deploy safely? Monitor effectively?
   - Is capacity understood and modeled?

2. **Linus's Review** — Security lens
   - What are the threat vectors?
   - Are implicit security assumptions correct?
   - Is there data exposure risk?
   - Are we making assumptions we'll regret?

3. **Synthesize** — Combined perspective
   - Identify security-resilience trade-offs
   - Surface hidden assumptions
   - Ensure robustness without over-engineering

---

## Alex's Resilience Review

**What Alex Examines:**

### 1. Failure Modes & Detection
- [ ] What components can fail?
- [ ] How is each failure detected?
- [ ] Are there cascading failures?
- [ ] Can we detect failures before users notice?

**Bad:** Single database instance. No health checks. Service hangs on database failure.
**Good:** Primary + replicas. Health checks every 10s. Circuit breaker stops requests on failure.

### 2. Graceful Degradation & Fallbacks
- [ ] If critical component fails, does system degrade?
- [ ] Are fallbacks documented and tested?
- [ ] What's the performance in degraded mode?
- [ ] Is degradation visible to users?

**Bad:** Payment service down → entire checkout fails.
**Good:** Payment service slow → queue payments → process asynchronously → retry with backoff.

### 3. Deployment Safety
- [ ] Is deployment automated?
- [ ] Are rollouts gradual (canary, blue-green)?
- [ ] Health checks run before traffic routing?
- [ ] Can we rollback in < 5 minutes?

**Bad:** Manual deployment. All servers updated at once. No rollback plan.
**Good:** Automated. 1 server at a time. Health checks before traffic. Instant rollback via DNS.

### 4. Observability & Monitoring
- [ ] Can you see system state in real-time?
- [ ] Are alerts actionable?
- [ ] Is alert noise manageable?
- [ ] Can you debug production issues without logs?

**Bad:** No dashboards. Alert: "Error rate high" (how high? what errors?).
**Good:** Dashboard shows error rate by type. Alerts include context. Log aggregation enables debugging.

### 5. Capacity Planning & Scaling
- [ ] Are resource limits set?
- [ ] Is peak capacity modeled?
- [ ] Does autoscaling work (tested)?
- [ ] What's the breaking point?

**Bad:** No limits. One service consumes all CPU. Others starve.
**Good:** Resource requests/limits. Horizontal autoscaling. Load tested to 10x peak.

**Alex's Checklist:**
- [ ] Failure modes documented
- [ ] Health checks configured (startup, readiness, liveness)
- [ ] Graceful degradation planned
- [ ] Deployment automated + gradual + safe
- [ ] Observability sufficient (metrics, logs, alerts)
- [ ] Capacity modeled and tested
- [ ] RTO and RPO defined

**Alex's Automatic Rejection Criteria:**
- 🚫 No health checks
- 🚫 No resource limits (can starve other services)
- 🚫 All-in-one deployment (single point of failure)
- 🚫 Manual recovery processes > 1 hour
- 🚫 No monitoring of critical paths
- 🚫 Secrets in code/config files
- 🚫 No documented rollback plan

---

## Linus's Security Review

**What Linus Examines:**

### 1. Threat Modeling & Attack Vectors
- [ ] What are the threat vectors?
- [ ] Are we protecting data in transit and at rest?
- [ ] Could someone escalate privileges?
- [ ] Is there input validation at every boundary?

**Bad:** Database password in config file. Unencrypted database connections. No access controls.
**Good:** Secrets in vault. TLS for all connections. IAM roles restrict access.

### 2. Implicit Assumptions
- [ ] Are we assuming components are trustworthy?
- [ ] Do we assume internal network is safe?
- [ ] Are we trusting user input without validation?
- [ ] Could any assumption be violated?

**Bad:** "Internal services don't need authentication" (but what if one is compromised?).
**Good:** mTLS for internal services. Defense in depth (don't trust anything).

### 3. Access Control & Permissions
- [ ] Who can access what?
- [ ] Is principle of least privilege enforced?
- [ ] Can we audit who accessed what?
- [ ] Could permissions be over-granted?

**Bad:** All developers have admin access to production.
**Good:** Role-based access control. Audit logs for all admin actions. JIT (just-in-time) access.

### 4. Data Handling & Privacy
- [ ] Is sensitive data encrypted at rest and in transit?
- [ ] Is data retained longer than necessary?
- [ ] Can sensitive data be logged or exposed?
- [ ] Is compliance met (GDPR, HIPAA, PCI-DSS)?

**Bad:** Credit card numbers logged to disk. Data kept indefinitely.
**Good:** PCI-DSS compliance verified. Tokenized payments. Data retention policies enforced.

### 5. Secrets Management & Rotation
- [ ] How are secrets stored?
- [ ] Are secrets rotated regularly?
- [ ] Is access to secrets logged?
- [ ] Can we revoke secrets without downtime?

**Bad:** Hardcoded API keys. Never rotated. No audit trail.
**Good:** Secrets in vault. Rotated monthly. Access logged. Instant revocation.

**Linus's Checklist:**
- [ ] Threat model documented
- [ ] No hardcoded credentials
- [ ] TLS for all network communication
- [ ] Access control follows least privilege principle
- [ ] Audit logging for sensitive operations
- [ ] Secrets properly managed and rotated
- [ ] Compliance requirements identified and met

**Linus's Automatic Rejection Criteria:**
- 🚫 Hardcoded secrets in code/config
- 🚫 No TLS for sensitive connections
- 🚫 Over-broad access permissions
- 🚫 No audit logging for admin actions
- 🚫 Sensitive data in logs
- 🚫 SQL injection or command injection risks
- 🚫 Assumptions about internal network safety

---

## Combined Perspective: Infrastructure Review Synthesis

**When Alex & Linus Agree:**
- ✅ Infrastructure is resilient AND secure
- ✅ Approve for merging

**When They Disagree:**
Common disagreement: "Should we add encryption everywhere?"
- Linus says: "Encrypt all data at rest and in transit"
- Alex says: "Encryption adds latency. Measure first."
- Resolution: Default to secure. Profile to find real bottlenecks. Encrypt what matters.

**Trade-offs to Surface:**
1. **Security vs Performance**
   - Encryption adds CPU load
   - But data breaches cost more
   - Measure latency. Encrypt if acceptable.

2. **Simplicity vs Defense in Depth**
   - One firewall is simple
   - Multiple layers are complex but safer
   - Use both. Understand the trade-off.

3. **Scalability vs Security**
   - Autoscaling simplifies operations
   - But each new instance is a potential attack surface
   - Automate security hardening too.

---

## Review Checklist

### Before Review Starts
- [ ] Infrastructure code change is documented
- [ ] Threat model (if new infrastructure) documented
- [ ] Change tested in staging environment
- [ ] Rollback plan documented

### During Alex's Review
- [ ] Failure modes identified
- [ ] Observability sufficient
- [ ] Deployment plan is safe
- [ ] Capacity is modeled

### During Linus's Review
- [ ] Threat vectors identified
- [ ] Access control follows principle of least privilege
- [ ] Secrets properly managed
- [ ] Compliance met

### After Both Reviews
- [ ] Feedback synthesized
- [ ] Security-resilience trade-offs understood
- [ ] Assumptions surfaced and challenged
- [ ] Approval given (or revisions requested)

---

## Review Decision Tree

```
1. Is infrastructure resilient (Alex)?
   NO → Ask for resilience improvements
   YES → Continue

2. Is infrastructure secure (Linus)?
   NO → Ask for security hardening
   YES → Continue

3. Are there trade-off disagreements?
   YES → Discuss (often about latency vs security)
   NO → Continue

4. Are implicit assumptions challenged?
   YES → Re-examine whether assumptions are safe
   NO → Continue

5. Is infrastructure ready to deploy?
   YES → Approve
   NO → Request specific revisions
```

---

## Example: Database Cluster Review

**Code Being Reviewed:** PostgreSQL cluster in Kubernetes

### Alex's Review:
**Resilience Check:**
- ✅ Primary + 2 replicas (redundancy)
- ✅ Health checks configured
- ❌ Issue: No backup strategy documented
- ✅ Good: Automatic failover configured
- ❌ Issue: No capacity planning for disk growth

**Alex's Recommendation:**
- Document backup strategy (daily + weekly + monthly)
- Model disk usage growth
- Test failover under load

### Linus's Review:
**Security Check:**
- ❌ Problem: Database password in config
- ❌ Problem: No encryption in transit (replication between pods)
- ✅ Good: Access controlled to pod network
- ❌ Problem: No audit logging of queries
- ✅ Good: Backups encrypted

**Linus's Recommendation:**
- Move password to secrets vault
- Enable TLS for replication
- Enable query audit logging
- Define retention policy

### Synthesis:
**Trade-off Identified:**
- Alex: "Audit logging might slow queries"
- Linus: "But data integrity requires it"
- Resolution: Enable audit logging. Profile to measure impact. Add to monitoring.

**Approval:** Conditional on both Alex's and Linus's changes.

---

## Related Commands

- **Alex's Deep Dive:** `/pb-alex-infra` — Systems thinking, failure modes, resilience design
- **Linus's Deep Dive:** `/pb-linus-agent` — Security assumptions, threat modeling, code correctness
- **Hardening:** `/pb-hardening` — Security hardening checklist (reference standard)
- **Deployment:** `/pb-deployment` — Deployment execution and verification
- **Standards:** `/pb-standards` — Coding principles both agents apply

---

## When to Escalate

**Escalate to Maya (Product)** if:
- Infrastructure changes impact user experience
- Capacity planning affects feature roadmap
- Cost/benefit trade-offs matter

**Escalate to Jordan (Testing)** if:
- Failover scenarios need testing
- Load testing needed to validate capacity
- Chaos engineering needed to verify resilience

**Escalate to Sam (Documentation)** if:
- Runbooks need documentation
- Complex infrastructure needs explanation
- Team onboarding needs guides

---

*Infrastructure review: Systems that don't fail + remain secure when attacked*

