---
name: "pb-knowledge-transfer"
title: "Knowledge Transfer (KT) Session Preparation"
category: "people"
difficulty: "advanced"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-onboarding', 'pb-guide', 'pb-security', 'pb-adr', 'pb-incident']
last_reviewed: "2026-04-23"
last_evolved: "2026-04-23"
version: "1.1.0"
version_notes: "v2.21.0: Pruned verbose Payment Service stubs (net -352 lines). Added Pre-KT risk map (bus factor, hotspots, co-changes, ungoverned hotspots), mechanical/tribal split on four Core Sections, WHY/DECISION/TRADEOFF inline markers, week-1 exit criteria, per-section audience naming."
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

## Pre-KT: Map Knowledge Risk

**Audience:** KT organizer (targets the session before content is written)

Before planning a session, identify what knowledge is actually at risk. Target the session - depth where it matters, skim where it does not. Four primitives, all compute with plain `git` on any repo. Tools like [repowise](https://github.com/repowise-dev/repowise) automate them but are not required to start.

### Bus factor - what only one person knows

Files where one engineer owns >80% of the lines are the highest-risk KT targets when that engineer leaves.

```bash
# Contributors by line count for a single file
git shortlog -sne -- path/to/file.go

# Per-author line count across a module (blame-based)
git ls-files path/to/module | xargs -I {} git blame --line-porcelain {} \
  | grep "^author " | sort | uniq -c | sort -rn
```

Any file where the top contributor exceeds 80% is a session priority.

### Hotspots - where change concentrates

Files in the top 25% of both churn (commit count) and complexity (line count) are where bugs live and where surprises hide.

```bash
# Commit count per file, last 6 months
git log --since="6 months ago" --name-only --pretty=format: \
  | sort | uniq -c | sort -rn | head -20
```

High-churn + high-size = hotspot. The departing engineer has implicit models of how these files behave that pure code-reading will not recover.

### Co-change pairs - hidden coupling

Files that change together in the same commit without an import link between them. This is coupling that AST analysis cannot see and engineers rarely document.

```bash
# For each recent commit, list files changed together
git log --since="6 months ago" --name-only --pretty=format:"COMMIT" \
  | awk '/^COMMIT/{if(length(f))print f; f=""; next} NF{f=f" "$0} END{print f}' \
  | awk '{for(i=1;i<NF;i++)for(j=i+1;j<=NF;j++)print $i"\t"$j}' \
  | sort | uniq -c | sort -rn | head -20
```

When a section says "these two files always move together," that is co-change intelligence. Record it explicitly - the new owner will not notice it otherwise.

### Ungoverned hotspots - unwritten intent

Hotspot files with no ADR, no README section, and no inline `WHY:`/`DECISION:`/`TRADEOFF:` markers. These are the "here be dragons" targets.

```bash
# Hotspots missing any inline decision markers
grep -RL "WHY:\|DECISION:\|TRADEOFF:" path/to/module
```

### Worked example

Risk map for a departing engineer owning `payment-service/`:

```
$ git shortlog -sne -- payment-service/payments/
  487  alice <alice@company.com>
   42  bob <bob@company.com>
    8  ci-bot <ci@company.com>
  → bus factor: alice owns ~91% of payments/. PRIORITY.

$ git log --since="6 months ago" --name-only --pretty=format: \
    payment-service/ | sort | uniq -c | sort -rn | head -5
  48 payments/processor.ts
  31 webhooks/stripe.ts
  29 refunds/handler.ts
   8 types/payment.ts
  → hotspots: processor.ts, stripe.ts, handler.ts.

$ grep -RL "WHY:\|DECISION:\|TRADEOFF:" payment-service/payments/
  payments/processor.ts
  webhooks/stripe.ts
  → two ungoverned hotspots, both >90% owned by Alice.

Session depth: these two files get 60+ min. Everything else: skim.
```

Run this before writing a single Core Section. The map tells you where to spend the engineer's time.

---

## Core Sections: KT Package Contents

Sections 1-12 below. Section 1 (Project Overview) is shown full as the worked example; sections 2-12 give you the shape and a compact snippet. Mirror Section 1's fidelity when you fill them in.

### 1. Project Overview

**Audience:** new engineer (first-week context)

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

**Audience:** new engineer (mental model)

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

**What the tools show** (verify, do not rewrite from scratch): import graph, file dependency structure, entry points by centrality, module clusters from co-change.
**What they miss** (you write these): why this topology exists (history, constraints, previous attempts), which components are load-bearing vs incidental, which external deps are critical vs legacy.

---

### 3. Key Data Flows

**Audience:** new engineer, on-call responder

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

**Audience:** new engineer, on-call responder

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

**What the tools show**: upstream callers from import graph, downstream HTTP/gRPC calls from client code, package manifests for third-party deps.
**What they miss**: which deps are genuinely critical vs historical leftover, why timeouts and retries are set to *these* values (usually a past incident), services called so rarely everyone forgets until they break.

---

### 5. Development Setup

**Audience:** new engineer (day 1)

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

**Audience:** new engineer (shipping their first PR)

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

**Audience:** new engineer (avoid rookie mistakes), on-call responder (debugging)

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

**What the tools show**: hotspot files (churn × complexity), bug-fix density per file (`fix:` commits), cyclomatic complexity above threshold.
**What they miss**: the "works by accident" list (behaviors no one wrote on purpose but something depends on), the "nobody dares touch it" list, performance cliffs that only appear under specific traffic patterns.

---

### 8. Monitoring & Observability

**Audience:** on-call responder

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

**What the tools show**: existing metric definitions in code, alert rules in alertmanager/datadog config, log-level distribution from recent samples.
**What they miss**: which dashboards actually get opened during an incident (vs built and forgotten), alerts that fire too often to be trusted (real noise-to-signal), the implicit severity mapping - "this alert pages, that one goes to Slack, this one we ignore."

---

### 9. Deployment & Operations

**Audience:** engineer shipping changes

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

**Audience:** engineer making feature trade-offs

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

**Audience:** new engineer (hands-on learning)

**Provide:**
- Key API calls to demo (with curl examples)
- Example requests/responses
- Workflow walkthroughs
- UI flows (if applicable)
- "Try it yourself" exercises

**Snippet:**
````markdown
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
````

---

### 12. FAQs

**Audience:** new engineer (self-service)

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

## Durable Artifacts: Inline Decision Markers

**Audience:** departing engineer (writes markers), all future engineers (read them)

A KT session produces a doc. Docs go stale. Markers in the source survive.

When the "why" is non-obvious, drop one of three lightweight conventions into the code. They render as normal comments, cost nothing to write, and turn tribal reasoning into durable, greppable artifacts:

```go
// WHY: JWT over session cookies - k8s horizontal scaling requires stateless auth.
// DECISION: All external calls wrapped in CircuitBreaker after 2024-Q3 Stripe outage.
// TRADEOFF: Accepted eventual consistency in preferences store for write throughput.
```

**When to use which:**

- `WHY:` - this code looks weird, here is the reason.
- `DECISION:` - this is the chosen approach among alternatives, so the next person does not re-litigate.
- `TRADEOFF:` - we knowingly accepted this cost for that benefit.

**Relation to `/pb-adr`:**

Markers are lightweight siblings of ADRs, not replacements.

|  | Inline marker | `/pb-adr` |
|---|---|---|
| Scope | One file or function | Cross-cutting, multi-file |
| Lifetime | As long as the code | Independent of file moves |
| Cost | A comment | A structured document |
| Discoverability | `grep` | ADR index |

Graduate a marker to an ADR when it governs more than one file, survives a major refactor, or keeps coming up in incident reviews.

**KT integration:**

At session end, sweep the departing engineer's hot paths for ungoverned code:

```bash
grep -RL "WHY:\|DECISION:\|TRADEOFF:" path/to/their-hot-paths/
```

Each ungoverned hotspot gets at least one marker capturing the non-obvious bit. The marker stays after they are gone.

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

Week 1 after the KT session (did it actually land?):
- [ ] New dev opened at least one PR (any scope, even docs)
- [ ] New dev read at least one real incident alert (not necessarily resolved)
- [ ] New dev can explain each ungoverned hotspot from the risk map in their own words
- [ ] New dev has opened the main monitoring dashboards during a normal day
- [ ] New dev can tell which Slack channels carry real signal vs noise
- [ ] Week-2 follow-up 1:1 scheduled to catch drift

"Setup works" is necessary but not sufficient. Shipping work, reading real alerts, and distinguishing signal from noise is the difference between "we did KT" and "knowledge transferred."

---

*Created: 2026-01-11 | Category: Onboarding | Tier: M*
