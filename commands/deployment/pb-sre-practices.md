# SRE Practices

Build sustainable, reliable operations through toil reduction, error budgets, and healthy on-call practices. This command focuses on prevention and culture—complementing `/pb-incident` (response) and `/pb-observability` (monitoring).

**Mindset:** SRE practices embody `/pb-preamble` thinking: blameless culture, honest assessment of reliability, and challenging "we've always done it this way." Apply `/pb-design-rules` thinking: Robustness (systems should handle failure gracefully) and Transparency (make operational health visible).

Reliability is a feature. Invest in it deliberately, not reactively.

---

## Quick Reference

| Practice | Purpose | Frequency |
|----------|---------|-----------|
| Toil reduction | Eliminate repetitive manual work | Ongoing |
| Error budgets | Balance reliability vs velocity | Per release |
| Capacity planning | Prevent resource exhaustion | Quarterly |
| Service ownership | Clear accountability | Always |
| On-call health | Sustainable rotations | Weekly review |

---

## Toil Identification & Reduction

### What Is Toil?

Toil is work that is:
- **Manual** — Requires human intervention
- **Repetitive** — Done over and over
- **Automatable** — Could be scripted or eliminated
- **Reactive** — Triggered by events, not planned
- **No enduring value** — Doesn't improve the system

**Examples of toil:**
- Manually restarting crashed services
- Responding to the same alert repeatedly
- Manual deployment steps
- Copying data between systems
- Responding to routine access requests

**Not toil:**
- On-call incident response (unavoidable, requires judgment)
- Postmortems (creates enduring improvement)
- System design (creates lasting value)

### Toil Tracking

Track toil to understand where to invest automation.

**Toil log template:**

| Date | Task | Time Spent | Frequency | Automatable? | Priority |
|------|------|------------|-----------|--------------|----------|
| 2026-01-20 | Restart API pod after OOM | 15min | 2x/week | Yes | High |
| 2026-01-20 | Generate weekly report | 30min | Weekly | Yes | Medium |
| 2026-01-20 | Provision dev environment | 1hr | 3x/month | Yes | High |

**Metrics to track:**
- Total toil hours per week
- Toil as percentage of engineering time (target: < 50%)
- Top 5 toil sources
- Toil reduction over time

### Toil Budget

**Rule:** Keep toil below 50% of on-call/operations time.

```
If toil > 50%:
  → Stop new feature work
  → Focus on automation until toil < 50%
  → This is not optional
```

**Why 50%?** Engineers need time for:
- Improving systems (not just keeping them running)
- Learning and growth
- Sustainable pace

### Prioritizing Automation

| Criteria | Weight |
|----------|--------|
| Frequency (how often) | High |
| Time per occurrence | High |
| Error-prone when manual | High |
| Blocks other work | Medium |
| Causes context switching | Medium |

**Automation ROI formula:**
```
Hours saved = (frequency × time per occurrence × weeks) - automation time
If hours saved > 0 in reasonable timeframe → automate
```

**Quick wins first:** Start with high-frequency, low-complexity tasks.

---

## Error Budget Policies

Error budgets translate SLO targets into actionable decisions. For SLO definition, see `/pb-observability`.

### Understanding Error Budgets

If your SLO is 99.9% availability (43 minutes downtime/month):
- **Error budget** = 43 minutes of allowed downtime
- **Budget consumed** = actual downtime this month
- **Budget remaining** = what you can "spend" on risky changes

```
SLO: 99.9% availability
Monthly error budget: 43 minutes

Week 1: 10 min downtime → 33 min remaining (77% left)
Week 2: 5 min downtime → 28 min remaining (65% left)
Week 3: 20 min downtime → 8 min remaining (19% left)
Week 4: SLOW DOWN - limited budget for risky deploys
```

### Error Budget Policy

**When budget is healthy (> 50% remaining):**
- Deploy new features freely
- Take calculated risks
- Experiment with new technologies

**When budget is concerning (25-50% remaining):**
- Increase review rigor for changes
- Prioritize reliability fixes
- Reduce deployment frequency
- Add more testing before deploy

**When budget is critical (< 25% remaining):**
- Freeze non-critical deployments
- Focus exclusively on reliability
- Postmortem recent incidents
- Delay feature work until budget recovers

**When budget is exhausted (0% remaining):**
- Emergency mode: reliability only
- No new features until SLO is met
- All hands on reliability improvement
- Stakeholder communication required

### Negotiating with Product

Error budgets create healthy tension between reliability and velocity.

**Conversation framework:**
```
Product: "We need to ship feature X this week"

SRE: "Our error budget is at 15%. If we deploy and cause an outage,
      we'll miss our SLO commitment.

      Options:
      1. Wait until budget recovers (2 weeks)
      2. Deploy with extra safeguards (canary, feature flag)
      3. Accept SLO miss and communicate to customers

      Which tradeoff works for the business?"
```

**Document the decision.** If product chooses to spend budget, that's a valid business decision—but make it explicit.

---

## Capacity Planning

Prevent resource exhaustion before it becomes an incident.

### Capacity Metrics

Track these for critical services:

| Metric | Warning | Critical | Action |
|--------|---------|----------|--------|
| CPU utilization | > 60% sustained | > 80% | Scale up |
| Memory utilization | > 70% sustained | > 85% | Scale up or optimize |
| Disk usage | > 70% | > 85% | Expand or clean |
| Database connections | > 70% of pool | > 85% | Increase pool or optimize |
| Request latency | P99 > 2x baseline | P99 > 5x | Investigate |

### Forecasting Load

**Simple linear projection:**
```
Current: 1000 requests/sec
Growth rate: 10% month-over-month
Capacity limit: 2000 requests/sec

Months until capacity:
  1000 × 1.1^n = 2000
  n ≈ 7 months

Action: Plan capacity increase by month 5
```

**Consider:**
- Organic growth (user base)
- Seasonal patterns (holidays, events)
- Marketing campaigns
- New feature launches

### Capacity Planning Cadence

**Quarterly:**
- Review current utilization
- Update growth projections
- Plan infrastructure changes for next quarter

**Before major launches:**
- Load testing at 2x expected traffic
- Pre-scale infrastructure
- Define rollback triggers

**Template: Quarterly Capacity Review**
```markdown
## Q1 2026 Capacity Review

### Current State
- API servers: 8 instances, 45% avg CPU
- Database: 16GB RAM, 60% utilized
- Storage: 500GB, 55% used

### Growth Since Last Quarter
- Traffic: +15%
- Storage: +20%
- Users: +12%

### Projections for Q2
- Expected traffic: +15% (based on trend)
- Storage needs: +100GB (based on data growth)
- No CPU concerns (headroom sufficient)

### Actions
- [ ] Increase storage allocation by 200GB (buffer)
- [ ] Monitor database memory (approaching threshold)
- [ ] No immediate scaling needed for compute
```

---

## Service Ownership Model

Clear ownership prevents "that's not my job" failures.

### What Owners Are Responsible For

**Service owners must:**
- Maintain SLO compliance
- Respond to pages for their service
- Document runbooks and architecture
- Plan capacity for their service
- Perform regular dependency audits
- Conduct postmortems for incidents

### Ownership Documentation

Every service needs:

```markdown
## Service: Payment Processing

### Owner
- Team: Payments
- Primary contact: @payments-oncall
- Escalation: @payments-lead

### SLOs
- Availability: 99.95%
- Latency P99: < 500ms
- Error rate: < 0.1%

### Dependencies
- Database: PostgreSQL (owned by Data Platform)
- Queue: Redis (owned by Platform)
- External: Stripe API

### Runbooks
- [Payment processing failures](link)
- [High latency investigation](link)
- [Database connection issues](link)

### On-Call
- Rotation: Weekly, Monday handoff
- Contact: PagerDuty "payments" service
```

### Handoff Protocol

When ownership changes (reorg, team changes):

1. **Documentation audit** — Is everything documented?
2. **Runbook review** — Walk through with new owner
3. **Shadow on-call** — New owner shadows for 2 weeks
4. **Gradual handoff** — New owner primary, old owner backup
5. **Clean handoff** — New owner fully responsible

**Never abandon a service without explicit handoff.**

---

## Blameless Culture & Psychological Safety

Blame prevents learning. Psychological safety enables improvement.

### Why Blameless Matters

**With blame:**
- Engineers hide mistakes
- Root causes stay hidden
- Same incidents repeat
- Team trust erodes

**Without blame:**
- Engineers report problems early
- Root causes are discovered
- Systems improve
- Team trust grows

### Blameless Postmortem Language

**Avoid:**
- "John caused the outage by..."
- "The mistake was..."
- "They should have known..."
- "Why didn't anyone..."

**Instead:**
- "The system allowed..."
- "The process didn't catch..."
- "The automation was missing..."
- "How might we prevent..."

### Creating Psychological Safety

**Leaders must:**
- Thank people for reporting problems
- Share their own mistakes openly
- Never punish for honest errors
- Focus questions on systems, not people
- Celebrate learning from failures

**Indicators of safety:**
- People raise concerns early
- Bad news travels fast
- Postmortems are collaborative, not defensive
- Teams voluntarily share failures

### The "5 Whys" Without Blame

```
Incident: Customer data exposed in logs

Why? Logs included full request bodies
  Why? Logging configuration didn't exclude sensitive fields
    Why? No standard logging template for sensitive services
      Why? Each team built their own logging
        Why? No central platform team until recently

Action: Create standard logging library with PII redaction
```

Notice: No individual blamed. Focus on system improvement.

---

## On-Call Health

Sustainable on-call prevents burnout and maintains quality.

### Healthy Rotation Patterns

**Good:**
- 1 week on, 3+ weeks off
- Defined business hours (primary) vs after-hours (backup)
- Clear escalation paths
- Compensatory time off after heavy rotations

**Bad:**
- Always-on expectations
- 1 week on, 1 week off (too frequent)
- No backup coverage
- Pages for non-actionable alerts

### On-Call Load Metrics

Track per rotation:

| Metric | Healthy | Concerning | Action Needed |
|--------|---------|------------|---------------|
| Pages per week | < 5 | 5-15 | > 15 |
| Night pages | < 1 | 1-3 | > 3 |
| Time to acknowledge | < 5 min | 5-15 min | > 15 min |
| False positive rate | < 10% | 10-30% | > 30% |

**If metrics are concerning:**
- Reduce alert noise (tune thresholds)
- Automate responses where possible
- Add more people to rotation
- Split into sub-rotations by service

### Preventing Burnout

**Signs of on-call burnout:**
- Dreading rotation weeks
- Ignoring or silencing pages
- Decreased quality of incident response
- Increased sick days during rotation
- Team members leaving

**Prevention:**
- Regular rotation reviews
- Rotate out of on-call for a quarter (recovery)
- Celebrate reliability improvements
- Make on-call load visible to leadership
- Budget time for on-call automation

### On-Call Handoff Template

```markdown
## On-Call Handoff: Jan 20 → Jan 27

### Outgoing (Alice)
- No ongoing incidents
- Known issues:
  - API latency spike at 3pm daily (monitoring, not actionable)
  - Staging environment flaky (don't page for staging)

### Incoming (Bob)
- Confirmed: I have access to all systems
- Confirmed: PagerDuty is configured correctly
- Questions: None

### Deployment Schedule
- Tuesday: Feature X (low risk)
- Thursday: Database migration (high risk, after-hours)

### Contacts
- Database: @db-oncall
- Infrastructure: @infra-oncall
- Escalation: @engineering-lead
```

---

## Operational Review Cadence

Regular reviews prevent drift and maintain operational health.

### Weekly: Operational Standup (15 min)

- Recent incidents and postmortem status
- Current error budget consumption
- On-call load from last week
- Any blockers or concerns

### Monthly: Reliability Review (1 hour)

- SLO compliance for the month
- Error budget trends
- Toil tracking update
- Capacity utilization review
- Action items from postmortems

### Quarterly: Operational Planning (2 hours)

- Quarterly capacity planning
- Toil reduction priorities
- On-call rotation health
- SLO adjustments (if needed)
- Training and documentation gaps

### Annually: Disaster Recovery Testing

- Full DR test (see `/pb-dr`)
- On-call process review
- Major incident simulation
- Documentation audit

---

## Integration with Playbook

**Complements existing commands:**
- `/pb-incident` — Incident response and postmortems
- `/pb-observability` — SLO definitions, metrics, alerting
- `/pb-deployment` — Deployment strategies
- `/pb-dr` — Disaster recovery planning

**Workflow:**
```
Design (/pb-observability - define SLOs)
    ↓
Operate (this command - sustainable practices)
    ↓
Respond (/pb-incident - when things break)
    ↓
Recover (/pb-dr - disaster scenarios)
    ↓
Improve (back to operate)
```

---

## Quick Commands

| Topic | Action |
|-------|--------|
| Track toil | Log time spent on repetitive tasks |
| Check error budget | Compare incidents to SLO allowance |
| Review capacity | Quarterly utilization review |
| Assess on-call health | Track pages per week, night pages |
| Conduct postmortem | Blameless, focus on systems |

---

*Reliability is a feature. Invest in it deliberately.*
