---
name: "pb-knowledge-transfer"
title: "Knowledge Transfer (KT) Session Preparation"
category: "people"
difficulty: "advanced"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-onboarding', 'pb-guide', 'pb-security', 'pb-adr', 'pb-incident']
last_reviewed: "2026-02-09"
last_evolved: ""
version: "1.0.0"
version_notes: "v2.10.0 baseline"
breaking_changes: []
---
# Knowledge Transfer (KT) Session Preparation

Structured guide for documenting and transferring project knowledge to new team members and stakeholders.

**Mindset:** The best knowledge transfer includes both frameworks.

Teach `/pb-preamble` first: new team members need to know how to challenge assumptions, prefer correctness, and think like peers. Then teach `/pb-design-rules`: help them understand the design principles (Clarity, Modularity, Robustness, Extensibility) that govern how systems are built in this team.

**Resource Hint:** sonnet - structured documentation and template application, not architectural judgment.

---

## When to Use This Command

- **Planning a KT session** - Structuring effective knowledge transfer
- **Team member leaving** - Capturing their knowledge before departure
- **New hire starting** - Preparing materials for their ramp-up
- **Service handoff** - Transferring ownership between teams

---

## Purpose

Knowledge transfer (KT) ensures:
- New developers can contribute effectively within days, not weeks
- Team handoffs are smooth and complete
- Institutional knowledge doesn't disappear when people leave
- All stakeholders (dev, QA, product, management) have shared understanding
- Critical "tribal knowledge" is documented

---

## When to Conduct KT Sessions

- **New developer joining team** - Full comprehensive KT
- **Major feature handoff** - Focused KT on that feature
- **Team transition** - New team taking over service ownership
- **On-call rotation training** - Ops perspective KT
- **Before extended leave** - Critical knowledge before person is unavailable

---

## Core Sections: KT Package Contents

Sections 1-12 below. Section 1 (Project Overview) is shown full as the worked example; sections 2-12 give you the shape and a compact snippet. Mirror Section 1's fidelity when you fill them in.

### 1. Project Overview

**Provide:**
- 1-2 paragraph summary of what the service does
- Business value (why does this exist?)
- Key users/customers who depend on it
- Ownership (who's responsible for what)
- Links to repo, docs, Slack channel, runbooks

**Template:**
```markdown
## Service: Payment Processing API

**Purpose**: Handles all payment transactions for our platform.
Customers depend on this to process credit card charges with 99.99% uptime.

**Ownership**:
- Dev lead: @alice (architecture decisions)
- On-call: @bob (incidents)
- Product owner: @charlie (feature requests)

**Links**:
- Repo: github.com/company/payment-service
- Docs: https://wiki.company.com/payment-service
- Runbooks: https://runbooks.company.com/payment
- Slack: #payment-team
```

---

### 2. Technical Architecture

**Provide:**
- High-level system diagram (ASCII or Mermaid)
- Key components (APIs, databases, workers, caches)
- External dependencies (3rd party services, other internal services)
- Technology stack (languages, frameworks, databases)
- Data model overview (key entities, relationships)

**Snippet:**
```markdown
## Architecture

Clients (Web / Mobile / iOS) → API Gateway → Payment Service (Go)
Payment Service → Postgres (Orders) · Redis (Cache) · RabbitMQ (Events)

**Components**: Payment Service (Go HTTP API), Order Service (Python), Webhook Consumer (Node.js).
**External**: Stripe (payments), Auth0 (authn), Datadog (monitoring).
```

---

### 3. Key Data Flows

**Provide:**
- Critical request/response flows with sequence diagrams
- Event flows (async, queues, webhooks)
- Error handling and fallback paths

**Snippet:**
```markdown
## User Payment Flow

1. User submits payment → Frontend POST /api/orders/:id/pay
2. Payment Service: validate → create record (pending) → Stripe charge → update record
3. Publish `payment.completed` → Order Service marks order as paid
4. On failure: record marked failed, `payment.failed` event, Order Service rolls back
```

---

### 4. Dependencies & Integration Points

**Provide:**
- All upstream services (who calls us?)
- All downstream services (who do we call?)
- Third-party integrations
- Retry logic and timeouts
- Circuit breaker settings

**Snippet:**
```markdown
## Service Dependencies

**Upstream**: Web, Mobile, Admin Dashboard → POST /api/orders/:id/pay
**Downstream**: Stripe (5s timeout, 3 retries), Order Service (1s, cached 5m), User Service (500ms, stale-cache fallback)
**Resilience**: Circuit breaker opens after 5 failures in 30s. Exponential backoff on retries. Stale cache allowed if downstream down.
```

---

### 5. Development Setup

**Provide:**
- Step-by-step local environment setup
- Required dependencies (languages, databases, services)
- Environment variables (with `.env.example`)
- How to run locally
- How to run tests

**Snippet:**
```markdown
## Getting Started Locally

**Prereqs**: Go 1.19+, PostgreSQL 14+, Redis 7+, Docker (optional)
**Setup**: `git clone` → `cp .env.example .env` → edit → `make db-setup` → `make run`
**Tests**: `make test` (all) · `make test-unit` · `make test-int` (needs DB)
**Debug**: stdout JSON logs · `LOG_LEVEL=debug` for DB queries · Stripe dashboard for external calls
```

---

### 6. Testing Strategy

**Provide:**
- What unit tests exist & why
- What integration tests exist & why
- How to run full test suite
- Test data setup (fixtures, seeds)
- CI/CD pipeline flow

**Snippet:**
```markdown
## Testing

- **Unit** (`tests/`): business logic in isolation, target 80% coverage (100% critical paths). `make test-unit` (~30s).
- **Integration** (`tests/integration/`): real Postgres + Redis (containerized). `make test-int` (~2m).
- **Fixtures** in `tests/fixtures/`, seeds in `db/seeds.sql`, Stripe test keys in `tests/stripe_mock.go`.
- **CI**: lint → unit → build → integration → security scan → stage (main) → total ~10m.
```

---

### 7. Pain Points & Gotchas

**Provide:**
- Known bugs or limitations
- Non-obvious behaviors (tribal knowledge)
- Performance bottlenecks
- Areas with technical debt
- Common mistakes to avoid

**Snippet:**
```markdown
## Known Issues & Gotchas

**Performance**
- N+1 query risk on order fetches. Always batch: `db.fetch_batch(ids)`, never loop.
- Redis cache must be cleared on refund or you will double-charge.

**Limitations**
- Stripe refunds only within 90 days of charge.
- Webhook retries sometimes arrive out of order - guard with idempotency keys.

**Non-obvious**
- All POSTs must be idempotent (Idempotency-Key header).
- Stripe webhooks can deliver twice; check payment state before acting.
- Store UTC only; convert for display.

**Mistakes made (so you do not)**
- Client-only amount validation → overcharging. Validate server-side.
- Cached payment status without TTL → stale reads. Always TTL.
- No network timeouts → stuck pending payments. Always timeout.
```

---

### 8. Monitoring & Observability

**Provide:**
- Key dashboards (links + what to look for)
- Alert rules (what triggers alerts, what on-call does)
- Log locations and important messages
- How to debug in production (safely)
- Incident response runbooks

**Snippet:**
```markdown
## Monitoring

**Dashboards**
- Success rate (>99% healthy, <95% pages). Latency p99 (<500ms healthy, >1s pages). Refund processing (all <1h).

**Alerts**
- Payment error rate >1% for 5m → page. DB pool exhausted → page (critical). Stripe >10s → Slack warn. Refund failures >10/h → page.

**Logs**
- `kubectl logs deploy/payment-service-prod`. Stripe at dashboard.stripe.com/test/logs.
- Watch: `card_declined` (customer), `rate_limit_exceeded` (us, back off), `pool_exhausted` (connection leak).

**Production debugging**: read-only queries, check logs + metrics first, follow `/runbook-*.md` for incidents. Never modify prod data manually.
```

---

### 9. Deployment & Operations

**Provide:**
- How code gets deployed
- Rollback procedures
- Database migrations
- Configuration management
- Post-deployment verification

**Snippet:**
```markdown
## Deployment

**Deploy**: PR → approval → merge main → CI (10m) → auto-stage → manual prod via `make deploy-prod` (rolling, health-checked, zero-downtime).
**Rollback**: `make rollback-prod` (~2m, no downtime).
**Migrations**: write SQL in `migrations/`, `make migration test`, deploy migration before code.
**Config**: Kubernetes secrets for env vars, Unleash for feature flags.
**Verify**: dashboard (success rate, latency) → alerts clean → `make smoke-test-prod` → watch 1h.
```

---

### 10. Product Context

**Provide:**
- What user-facing features use this service
- Product roadmap (what's planned)
- Pending decisions or open questions
- Product metrics (what the business cares about)
- How this service fits into larger product

**Snippet:**
```markdown
## Product Context

**Features using this service**: checkout (purchase), admin refunds, order confirmation receipt.
**Roadmap**: Q2 Apple/Google Pay · Q3 split payments · Q4 BNPL.
**Open**: crypto support (not decided) · record retention (currently 7y, compliance TBD).
**Metrics the business watches**: conversion rate, AOV, payment success rate (KPI >99%), refund rate.
```

---

### 11. Demo & Hands-On

**Provide:**
- Key API calls to demo (with curl examples)
- Example requests/responses
- Workflow walkthroughs
- UI flows (if applicable)
- "Try it yourself" exercises

**Snippet:**
```markdown
## Demo

```bash
# Charge
curl -X POST localhost:8080/api/payments/charge \
  -d '{"order_id":"ord_123","amount":99.99,"card_token":"tok_visa_4242"}'
# → {"payment_id":"pay_456","status":"completed"}

# Refund
curl -X POST localhost:8080/api/payments/pay_456/refund -d '{"reason":"customer_request"}'

# Status
curl localhost:8080/api/payments/pay_456
```

**Exercises for new dev**: run tests pass · create test payment (card 4242 4242 4242 4242) · refund it · commit a small change · deploy to staging.
```

---

### 12. FAQs

**Provide:**
- Common questions new developers ask
- Quick answers with links to details
- Troubleshooting tips

**Snippet:**
```markdown
## FAQs

- **Test a payment locally?** Stripe test keys, card `4242 4242 4242 4242`.
- **Test payment declines?** Check Stripe dashboard for error code; usually wrong amount format or expired key.
- **Debug a stuck payment?** `kubectl logs ... | grep payment_id=...`.
- **Deploy Friday?** Yes, stay online 1h post-deploy. Runbook: `/runbook-payment-failures.md`.
- **Who to page?** `make check-oncall` → PagerDuty.
- **Database password?** Never hardcoded. `kubectl get secret payment-db-creds`.
```

---

## KT Session Format

### For In-Person Sessions (90 min)
```
1. Kickoff & goals (5 min)
   "By the end, you'll understand: architecture, deployment, how to debug"

2. Live demo (20 min)
   - Walk through code, show it running locally
   - Make a test payment, show logs
   - Show how to deploy

3. Interactive Q&A (15 min)
   - What questions do you have?
   - What concerns you?

4. Hands-on (40 min)
   - New dev runs local setup themselves
   - Makes a test payment
   - Deploys to staging
   - You watch and help

5. Wrap-up (10 min)
   - Key takeaways
   - Next steps: First PR, oncall training
   - Resources & who to ask
```

### For Remote/Async Sessions
```
1. Prepare documentation (this guide)
2. Record video walkthrough (30 min)
3. Schedule Q&A call (1 hour)
4. New dev does hands-on locally, asks questions in Slack
5. Follow-up: First day pair programming on simple bug fix
```

---

## Related Commands

- `/pb-onboarding` - Full team onboarding (includes KT)
- `/pb-guide` - SDLC guide (referenced in KT)
- `/pb-security` - Security considerations during KT
- `/pb-adr` - Architecture decisions (why choices were made)
- `/pb-incident` - Incident runbooks (part of KT package)

---

## KT Checklist

Before the KT session, ensure:
- [ ] Documentation is up-to-date (check dates)
- [ ] Local setup works (try it yourself)
- [ ] All links work (docs, dashboards, repos)
- [ ] Test data is loaded in dev environment
- [ ] Recording equipment works (if recording)
- [ ] Quiet, distraction-free environment
- [ ] 1:1 session (not group, for personalized learning)

After the KT session:
- [ ] New dev successfully runs locally
- [ ] New dev made test payment
- [ ] New dev deployed to staging
- [ ] Assigned first task (small bug fix, not big feature)
- [ ] Scheduled follow-up (1 week) to check progress

---

*Created: 2026-01-11 | Category: Onboarding | Tier: M*
