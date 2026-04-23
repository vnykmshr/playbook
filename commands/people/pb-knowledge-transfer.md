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
version: "1.2.0"
version_notes: "v2.21.0 (v1.2.0): Added How to Use workflow block, Tiered KT Modes (Standard/Comprehensive), Section 13 Access & Authority Transfer, Shadow Mode session format, Doc Hygiene review cadence. Correctness pass: awk portability caveat, marker graduation clarified, week-1 postmortem fallback, worked-example framing. v1.1.0: Pruned Payment Service stubs (-352 lines). Added Pre-KT risk map, mechanical/tribal split on five Core Sections, WHY/DECISION/TRADEOFF markers, week-1 exit criteria, per-section audience."
breaking_changes: []
---
# Knowledge Transfer (KT) Session Preparation

Structured guide for documenting and transferring project knowledge to new team members and stakeholders.

**Mindset:** Teach the preamble first, then the design rules.

`/pb-preamble` gives new team members the stance: challenge assumptions, prefer correctness, think like peers. `/pb-design-rules` gives them the shape: the design principles (Clarity, Modularity, Robustness, Extensibility) that govern how systems are built in this team.

**Resource Hint:** sonnet - structured documentation and template application, not architectural judgment.

---

## How to Use This Skill

1. **Identify the scenario** - cooperative planned transition, new-hire onboarding, emergency departure, or adversarial/disengaged exit. The last changes the shape of the whole KT; see *Adversarial / disengaged departure* under Tiered KT Modes.
2. **Pick a tier** - Standard (2-3 days) for most cooperative handoffs, Comprehensive (1-2 weeks with shadow) for critical or new-hire. See *Tiered KT Modes* below.
3. **Run *Pre-KT: Map Knowledge Risk*** - target the session before writing a single section.
4. **If you are the departing engineer, work the priority list first** - see *For the Departing Engineer: Do These Before Friday*. Irreversible artifacts (markers, Section 7 tribal, Section 13 vendor relationships) before reconstructable ones.
5. **Fill the Core Sections required for your tier** - Section 1 is shown full as the worked example; 2-13 give you the shape and a compact snippet. Sections 1-2 are receiving-engineer homework from the repo; the departing engineer spends time where only they can.
6. **Produce inline markers in the departing engineer's hot paths** - durable beyond the doc. See *Durable Artifacts: Inline Decision Markers*.
7. **Run the exit-criteria checklist for your tier** - verify the KT actually landed, not just that setup worked.

---

## When to Use

Planned departure, new-hire onboarding, team-to-team service handoff, major feature handoff, on-call training, or the month before extended leave. Picking a *tier* (below) matters more than picking a scenario - time budget is the binding constraint.

A well-run KT keeps new developers productive in days (not weeks), prevents knowledge loss on departure, gives dev/QA/product/management a shared mental model, and turns tribal knowledge into artifacts that outlive the person.

---

## Tiered KT Modes

Two tiers. Pick by time budget, not by ideal outcome - an incomplete KT that ships beats a comprehensive one that stays in someone's head.

### Standard - planned transition (2-3 days)

**When to use:** most handoffs. Planned departure with 2-4 weeks of runway. Team-to-team transfer of an existing service.

**Required full:** Sections 1 (Project Overview), 2 (Architecture), 3 (Data Flows), 4 (Dependencies), 7 (Pain Points), 8 (Monitoring), 13 (Access & Authority).

**Lightly filled or linked to existing docs:** Sections 5 (Dev Setup), 6 (Testing), 9 (Deployment), 10 (Product Context), 11 (Demo), 12 (FAQs). If a section already has a good dedicated doc elsewhere, link to it rather than duplicate.

**Who writes what:** Sections 1 and 2 are receiving-engineer homework - draft them from the repo and the risk map, then have the departing engineer *verify* rather than author from scratch. Sections 3, 4, 7, 8, 13 are where only the departing engineer can write the tribal half; that is where their time goes.

**Process:** Pre-KT risk map (all four primitives) → receiving engineer drafts Sections 1-2 → departing engineer fills Sections 3, 4, 7, 8, 13 → inline marker sweep on hot paths → one 90-min formal session → Week-1 exit criteria.

**Budget reality:** 2-3 days of the departing engineer's focused time, plus 1-2 days of the receiving engineer's draft work in parallel. Teams that try to compress this into "1-2 days of one person" abandon it on day 2 and fall back to a Google Doc - do not design for failure.

**Exit:** new dev can find their way, knows the dragons (ungoverned hotspots), can respond to standard alerts, has the access they need.

**Emergency carve-out:** no 2-3 days available? Cut Standard to Sections 1/7/8/13 only and name the cut in the KT doc header so the receiving engineer sees what is and is not covered. This is a survival handoff, not a full transfer - label it honestly.

### Comprehensive - critical handoff or new-hire onboarding (1-2 weeks, with shadow)

**When to use:** critical-service handoff (high business impact, low bus factor). New hire onboarding to a complex area. Departures where the engineer carries vendor relationships, incident history, or tacit decision-making beyond what lives in the code.

**Required full:** all 13 Core Sections.

**Process:** Standard's process + 2-week Shadow Mode (see *KT Session Format*) + Week-1 AND Week-2 exit criteria + month-1 follow-up.

**Exit:** new dev is on-call primary, has resolved at least one incident end-to-end, can answer questions from other teammates without escalating.

### Adversarial / disengaged departure

Comprehensive and Standard both assume the departing engineer cooperates. Sometimes they do not - notice given, checked out, minimum effort, or actively unhelpful. This is a real failure mode; pretending otherwise ships a doc that breaks on first contact with a bad exit.

**What changes:**

- **Treat the departing engineer as a read-only source.** Do not depend on them authoring anything. Instead, extract from what already exists: git history, Slack archives, PR comments, past incident postmortems, ticket systems. The risk map runs the same; the session format changes.
- **Prioritize Section 13 (Access & Authority) revocation over transfer.** In a cooperative departure, you want Alice's vendor contacts handed over cleanly. In an adversarial one, you want Alice's prod access revoked on their last day - and you accept that the vendor-side relationships may genuinely be lost. Name the loss; do not pretend you transferred what you did not.
- **Ungoverned hotspots become unresolvable dragons.** In a cooperative KT the departing engineer writes inline markers on their hot paths. In an adversarial one, the markers will not happen. Label every ungoverned hotspot in the risk map as "unresolved at departure - next owner to investigate and mark during the first three months of ownership."
- **Week-1 exit criteria are unreachable.** "New dev explains a `WHY:` marker" cannot be tested when no new markers were written. Replace with: new dev has read at least one postmortem in a hot path, has reviewed the commit history of each ungoverned hotspot, and has listed three concrete questions they would want to ask the departing engineer if they still could.

**Label it in the KT doc header:** "Departure was non-cooperative; this doc is extracted, not authored. Sections marked ⚠ are reconstructions from artifacts, not transferred knowledge." The receiving engineer needs to know which sections they can trust and which they cannot.

---

## For the Departing Engineer: Do These Before Friday

**Audience:** the person leaving (if you are cooperating with the KT)

If your time is scarce - last week, last day, last three hours - work this list top to bottom. Ordered by irreversibility: what disappears with you vs what the next person can reconstruct.

**1. Inline markers in your hot paths (irreversible).** Run the ungoverned-hotspots grep on your files. For each one, drop at least one `WHY:`/`DECISION:`/`TRADEOFF:` marker capturing the non-obvious bit. The doc goes stale; the markers survive every refactor until the file is deleted. If you do nothing else from this list, do this.

```bash
grep -RL "WHY:\|DECISION:\|TRADEOFF:" path/to/your-hot-paths/
```

**2. Section 7 tribal knowledge (irreversible).** Pain Points and Gotchas. The "works by accident" list. The "nobody dares touch it" list. The performance cliffs that only appear under specific traffic patterns. None of this is reconstructable from code - it is pure memory, and it leaves with you. Write it down in any form; prose beats nothing.

**3. Section 13 vendor relationships (partially reversible).** List every third-party vendor contact you have a relationship with. Names, email addresses, when you last spoke, what they helped with. Schedule one-on-one intros where you can - transferring the *relationship* matters more than transferring the email. Do not paste credentials; just paths and handoffs.

**4. Section 4 dependency gotchas (semi-reversible).** For each upstream and downstream dependency, write one line on why the timeout/retry settings are what they are. Most are "past incident, we tuned down after X happened." The incident is in the commit log; the reasoning usually is not.

**5. Section 8 alert signal/noise (semi-reversible).** For each alert, name which ones fire frequently enough that you have learned to ignore them, and which always matter. The next on-call will learn this by getting paged - but they will learn it faster if you write it down.

**6. Everything else (reversible).** Architecture diagrams, data-flow documentation, deployment mechanics - the receiving engineer can reconstruct these from the repo if they have the time and the risk map. If you run out of days, these are the drop candidates.

Priority is not "what is easy" or "what is comprehensive" - it is "what cannot be recovered without you." Every hour you spend on items 1-3 is worth a day spent on item 6.

---

## Pre-KT: Map Knowledge Risk

**Audience:** KT organizer (targets the session before content is written)

Before planning a session, identify what knowledge is actually at risk. Target the session - depth where it matters, skim where it does not. Four primitives, all compute with plain `git` on any repo. A ~20-line script or an off-the-shelf co-change tool can automate them, but is not required to start.

### Bus factor - what only one person knows

Files where one engineer owns a dominant share of the lines are the highest-risk KT targets when that engineer leaves. Default threshold: top contributor >80%. Tune for your team - a two-person codebase rides higher concentrations without real risk; a ten-person team treats 60% as a red flag.

```bash
# Contributors by line count for a single file
git shortlog -sne -- path/to/file.go

# Per-author line count across a module (blame-based, faster batching)
git ls-files -z path/to/module \
  | xargs -0 -n 50 git blame --line-porcelain -- \
  | grep "^author " | sort | uniq -c | sort -rn
```

The batched `-0 -n 50` form avoids re-forking `git blame` per file; on a 200-file module it runs in seconds rather than minutes. Any file where the top contributor exceeds your threshold is a session priority.

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

```python
#!/usr/bin/env python3
# co_change.py - top file pairs that change together (6-month window)
import subprocess, itertools, collections

log = subprocess.check_output(
    ["git", "log", "--since=6 months ago", "--name-only",
     "--pretty=format:---"], text=True
)
pairs = collections.Counter()
for commit in log.split("---"):
    files = [f for f in commit.strip().splitlines() if f]
    if 2 <= len(files) <= 20:  # skip huge refactors
        for a, b in itertools.combinations(sorted(files), 2):
            pairs[(a, b)] += 1

for (a, b), n in pairs.most_common(20):
    print(f"{n:4}  {a}  {b}")
```

Run `python3 co_change.py` in the repo root - works on macOS, Linux, and anywhere Python 3 is available. Any co-change tool that reads git history works as well; the primitive is the commit-level file set, not the language.

When a section says "these two files always move together," that is co-change intelligence. Record it explicitly - the new owner will not notice it otherwise.

### Ungoverned hotspots - unwritten intent

Hotspot files with no ADR, no README section, and no inline `WHY:`/`DECISION:`/`TRADEOFF:` markers. These are the "here be dragons" targets.

```bash
# Hotspots missing any inline decision markers
grep -RL "WHY:\|DECISION:\|TRADEOFF:" path/to/module
```

### Worked example

Risk map for a departing engineer owning `payment-service/` (numbers illustrative; real output will be messier):

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

Sections 1-13 below. Section 1 (Project Overview) is shown full as the worked example; sections 2-13 give you the shape and a compact snippet. Mirror Section 1's fidelity when you fill them in.

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

**What the tools show**: call graphs, HTTP/RPC entry points, event subscribers, which queues and topics exist.
**What they miss**: which error paths have actually fired in production (vs defensive code that never runs), the intended rollback behavior when two services disagree, the flows customers exercise vs the flows that exist on paper.

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

**What the tools show**: CI pipeline definitions, deploy scripts, migration tooling, feature-flag config.
**What they miss**: which rollbacks have actually been used in anger, migrations that looked safe in staging and bit in prod, the unwritten rule about never deploying after 4pm Friday, which config changes need a warm-up window, which flags are load-bearing vs stale.

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

### 13. Access & Authority Transfer

**Audience:** KT organizer, departing engineer

**Provide:**
- Secrets and credentials: what exists, where stored, who has rotation authority
- Production access paths: DB creds, API keys, deploy keys
- Service accounts: third-party vendor logins, cloud provider service accounts
- Platform roles: Slack moderation, GitHub org/team access, PagerDuty schedules
- Escalation paths: new primary on-call, new secondary, manager escalation

**Snippet:**
```markdown
## Access & Authority

**Secrets (what, where, who rotates)**
- Stripe prod key - 1Password/engineering, rotated yearly, @alice → @bob
- Postgres prod password - K8s secret, rotated quarterly, @alice → @bob
- Deploy keys - GitHub repo settings, SRE team-owned (no change)

**Service accounts**
- Stripe dashboard admin - alice@ → transfer to bob@
- AWS IAM payments-service role - service-owned, no change
- Datadog org admin - alice → bob

**Platform roles**
- Slack #payment-team - alice (channel admin) → bob
- GitHub payment-service - alice (Admin) → bob (Maintain)
- PagerDuty primary - alice → bob (effective 2026-05-15)

**Escalation**: new primary @bob · secondary @charlie (unchanged) · manager @dana
```

**What the tools show**: GitHub/GitLab team membership, K8s RBAC, IAM roles, PagerDuty schedules.
**What they miss**: "Alice is the only one who ever called the vendor's support line" - vendor-side relationships, informal authority that does not live in any RBAC, tribal knowledge of which secret-rotation runbooks are actually current.

**Do not** paste real secrets or key values into this section. Paths and ownership transitions only.

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

Graduate a marker to an ADR when the underlying reason keeps being re-encountered across refactors, governs more than one file, or keeps coming up in incident reviews. (The comment itself may be deleted along with its file - it is the reason that graduates, not the text.)

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

### Shadow Mode (informal pairing, 1-2 weeks)

Used in the Comprehensive tier. Not a replacement for a formal session - a complement that captures what the formal session cannot.

**What shadowing transfers:**
- How the engineer actually triages alerts (vs what the runbooks say)
- Which tools they reach for first when something looks wrong
- Which teammates they Slack for which kinds of problems
- What "normal" looks like in logs, dashboards, and error rates

**Format:**
- 30-60 minutes per day for 1-2 weeks
- Shadower watches while the engineer works; does not interrupt unless asked
- End-of-day 10-minute debrief: "why did you do X?" turns observation into understanding
- Shadower keeps running notes (treat like distill notes, not meeting minutes)

**When shadow beats formal session:** when the engineer cannot articulate what they know. Some decisions are tacit - muscle memory, pattern recognition from past incidents, "I don't know why, but this usually works." Shadowing surfaces it; a formal session misses it.

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
- [ ] New dev read at least one real incident alert (or, if the week stayed quiet, walked a past postmortem with the departing engineer)
- [ ] New dev can explain each ungoverned hotspot from the risk map in their own words
- [ ] New dev can explain at least one `WHY:`/`DECISION:`/`TRADEOFF:` marker in the hot paths, unprompted, without the departing engineer in the room
- [ ] New dev has opened the main monitoring dashboards during a normal day
- [ ] New dev can tell which Slack channels carry real signal vs noise
- [ ] Week-2 follow-up 1:1 scheduled to catch drift

"Setup works" is necessary but not sufficient. Shipping work, reading real alerts, and distinguishing signal from noise is the difference between "we did KT" and "knowledge transferred."

**Doc hygiene after handoff:**

A KT doc has no cadence of its own. Absent a named owner and scheduled reviews, assume it goes stale within a quarter of the engineer's departure - adjust to your team's pace, but do not assume longer without evidence.

- [ ] KT doc has a named owner (usually the receiving engineer)
- [ ] Review dates set as calendar invites during the KT session itself, not as checklist aspirations - the 3-month invite is what survives; the checkbox is not
- [ ] Default cadence 3 / 6 / 12 months; tighten for safety-critical services, loosen for stable ones
- [ ] 3-month review: check links still work, verify local setup instructions still work, flag stale sections
- [ ] 6-month review: verify ungoverned hotspots now have inline markers, review Access & Authority list for drift
- [ ] 12-month review: decide keep / rewrite / archive

---

