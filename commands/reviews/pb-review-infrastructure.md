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

See `/pb-alex-infra` for the comprehensive infrastructure review framework and checklist.

**For infrastructure-specific review, focus on:**
- **Failure Detection:** Can we detect component failures before users notice? Are health checks in place?
- **Graceful Degradation:** If one service fails, does the system degrade or cascade?
- **Deployment Safety:** Are rollouts gradual? Can we rollback in < 5 minutes?
- **Observability:** Do dashboards and alerts give actionable insights?
- **Capacity Planning:** Are resource limits set? Load-tested to 10x peak?

**Alex's Red Flags for Infrastructure:**
- No health checks or monitoring of critical paths
- Single point of failure (all-in-one deployment)
- Manual recovery processes or rollback plans
- No resource limits (services can starve each other)

---

## Linus's Security Review

See `/pb-linus-agent` for the comprehensive security review framework and checklist.

**For infrastructure-specific review, focus on:**
- **Attack Surface:** What threat vectors exist? Are data in transit and at rest encrypted?
- **Access Control:** Is least privilege enforced? Can we audit who accessed what?
- **Assumptions:** Are we trusting the internal network? Components? User input? Could assumptions be violated?
- **Secrets Management:** Are secrets in a vault (not code)? Rotated? Access logged?
- **Compliance:** Is GDPR/HIPAA/PCI-DSS met? Retention policies enforced?

**Linus's Red Flags for Infrastructure:**
- Hardcoded secrets or credentials in code/config
- No TLS for sensitive connections or internal services
- Over-broad access permissions (all developers as admin)
- No audit logging for administrative actions
- Sensitive data in logs (credit cards, tokens, PII)

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

