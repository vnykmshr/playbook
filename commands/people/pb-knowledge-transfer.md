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
---
# Knowledge Transfer (KT) Session Preparation

Structured guide for documenting and transferring project knowledge to new team members and stakeholders.

**Mindset:** The best knowledge transfer includes both frameworks.

Teach `/pb-preamble` first: new team members need to know how to challenge assumptions, prefer correctness, and think like peers. Then teach `/pb-design-rules`: help them understand the design principles (Clarity, Modularity, Robustness, Extensibility) that govern how systems are built in this team.

**Resource Hint:** sonnet — structured documentation and template application, not architectural judgment.

---

## When to Use This Command

- **Planning a KT session** — Structuring effective knowledge transfer
- **Team member leaving** — Capturing their knowledge before departure
- **New hire starting** — Preparing materials for their ramp-up
- **Service handoff** — Transferring ownership between teams

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
```

---

### 2. Technical Architecture

**Provide:**
- High-level system diagram (ASCII or Mermaid)
- Key components (APIs, databases, workers, caches)
- External dependencies (3rd party services, other internal services)
- Technology stack (languages, frameworks, databases)
- Data model overview (key entities, relationships)

**Template:**
```markdown
## Architecture

```
┌─────────────────────────────────────────────────┐
│           API Gateway (Kong)                    │
└────────────────────┬────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
    ┌───▼──┐    ┌───▼──┐   ┌───▼──┐
    │ Web  │    │Mobile│   │ IOS  │
    └──────┘    └──────┘   └──────┘
        │            │            │
        └────────────┼────────────┘
                     │
        ┌────────────▼────────────┐
        │  Payment Service (Go)   │
        │  ├─ Order API           │
        │  ├─ Payment API         │
        │  └─ Refund API          │
        └────────────┬────────────┘
        │            │            │
    ┌───▼──┐   ┌───▼──┐   ┌──────▼──┐
    │ Postgres       │ Redis        │ RabbitMQ   │
    │ (Orders)       │ (Cache)      │ (Events)   │
    └────────────────────────────────────────────┘
```

**Key Components**:
- **Payment Service**: Go HTTP API handling charge/refund
- **Order Service**: Python service managing order lifecycle
- **Webhook Consumer**: Node.js service processing payment updates from Stripe

**External Dependencies**:
- Stripe (payment processor)
- Auth0 (authentication)
- Datadog (monitoring)
```

---

### 3. Key Data Flows

**Provide:**
- Critical request/response flows with sequence diagrams
- Event flows (async, queues, webhooks)
- Error handling and fallback paths

**Template - Request Flow:**
```markdown
## User Payment Flow

1. User submits payment in web UI
2. Frontend calls `/api/orders/:id/pay`
3. Payment Service:
   - Validates order (amount, user, items)
   - Creates payment record (status: pending)
   - Calls Stripe API to charge card
   - Updates payment record (status: completed/failed)
4. Publishes "payment.completed" event
5. Order Service listens, marks order as "paid"
6. Frontend receives success, redirects to order confirmation

Sequence Diagram:
```
Client → Payment API: POST /pay (card)
Payment API → Stripe: Charge card ($99.99)
Stripe → Payment API: Charge ID + status
Payment API → Database: INSERT payment record
Payment API → Message Queue: Publish payment.completed
Order Service ← Message Queue: Listen for event
Order Service → Database: UPDATE order status
Payment API → Client: 200 OK + order link
```

**Event Flow:**
```
payment.completed event contains:
- payment_id: "pay_123"
- order_id: "ord_456"
- amount: 99.99
- timestamp: 2026-01-11T10:30:00Z

Consumers:
- Order Service: Update order status to "paid"
- Notification Service: Send email receipt
- Analytics Service: Log transaction for metrics
```

**Error Flow:**
```
If card charge fails:
→ Payment record marked as "failed"
→ "payment.failed" event published
→ Order Service rolls back any inventory changes
→ Client sees error: "Payment declined - try different card"
→ Alert to fraud team if 3+ failures in 5 minutes
```
```

---

### 4. Dependencies & Integration Points

**Provide:**
- All upstream services (who calls us?)
- All downstream services (who do we call?)
- Third-party integrations
- Retry logic and timeouts
- Circuit breaker settings

**Template:**
```markdown
## Service Dependencies

**Upstream** (Services calling us):
- Web Frontend → POST /api/orders/:id/pay
- Mobile App → POST /api/orders/:id/pay
- Admin Dashboard → GET /api/payments?customer_id=X

**Downstream** (Services we call):
- Stripe: Charge card (timeout: 5s, retries: 3 with exponential backoff)
- Order Service: Fetch order details (timeout: 1s, cached 5 min)
- User Service: Get customer profile (timeout: 500ms, fallback to cache)

**3rd Party Integrations**:
- Stripe API: Charges, refunds, webhooks
- SendGrid: Email receipts (async, best-effort)
- Slack: Alert failed transactions (async, non-blocking)

**Resilience Settings**:
- Circuit breaker (Open after 5 failures in 30s)
- Timeout: 5s for external calls
- Retry: Exponential backoff, max 3 attempts
- Cache: Order data cached 5 min, user data cached 15 min
- Fallback: Use stale cache if service down
```

---

### 5. Development Setup

**Provide:**
- Step-by-step local environment setup
- Required dependencies (Go 1.19+, PostgreSQL 14+, Redis 7+)
- Environment variables (with example .env.example)
- How to run locally
- How to run tests

**Template:**
```markdown
## Getting Started Locally

### Prerequisites
- Go 1.19+ (install from golang.org)
- PostgreSQL 14+ (brew install postgresql)
- Redis 7+ (brew install redis)
- Docker (optional, for containerized setup)

### Setup Steps

1. Clone the repository
```bash
git clone github.com/company/payment-service
cd payment-service
```

2. Create .env file from template
```bash
cp .env.example .env
# Edit .env with local values
```

3. Create .env.example (checked into git, template only)
```
DATABASE_URL=postgres://user:password@localhost:5432/payment_dev
REDIS_URL=redis://localhost:6379
STRIPE_API_KEY=sk_test_...  # TEST key only, get from 1password
PORT=8080
LOG_LEVEL=debug
```

4. Initialize database
```bash
make db-setup  # Creates tables, loads seed data
```

5. Run locally
```bash
make run  # Starts server on :8080
# Test: curl http://localhost:8080/health
```

6. Run tests
```bash
make test        # All tests
make test-unit   # Unit tests only
make test-int    # Integration tests (needs DB)
```

### Common Tasks
```bash
make fmt         # Format code
make lint        # Run linter
make db-reset    # Clear database (dev only!)
make seed        # Load test data
```

### Debugging
- Server logs: See stdout (colored, JSON structured)
- Database queries: Set LOG_LEVEL=debug to see queries
- Stripe calls: Check https://dashboard.stripe.com/test/logs
```

---

### 6. Testing Strategy

**Provide:**
- What unit tests exist & why
- What integration tests exist & why
- How to run full test suite
- Test data setup (fixtures, seeds)
- CI/CD pipeline flow

**Template:**
```markdown
## Testing

### Unit Tests
```
tests/
  ├── payment_test.go      # Payment domain logic
  ├── stripe_client_test.go # Stripe API mocking
  └── order_validator_test.go
```

**Purpose**: Test business logic in isolation
**Coverage Target**: 80% (critical paths 100%)
**Run**: `make test-unit` (30 seconds)

### Integration Tests
```
tests/integration/
  ├── payment_end_to_end_test.go  # Full request flow
  └── stripe_webhook_test.go       # Webhook handling
```

**Purpose**: Test component interactions (API, DB, external services)
**Setup**: Uses real PostgreSQL + Redis (containerized)
**Run**: `make test-int` (2 minutes, requires DB)

### Test Data
- Fixtures in `tests/fixtures/` (JSON files for database state)
- Seeds in `db/seeds.sql` (load test data during setup)
- Stripe test keys in `tests/stripe_mock.go` (mocked responses)

### CI/CD Pipeline
```
GitHub Push
  ├─ Lint & Format Check (2 min)
  ├─ Unit Tests (1 min)
  ├─ Build Docker Image (3 min)
  ├─ Integration Tests (3 min) ← Requires DB
  ├─ Security Scan (1 min)
  └─ Deploy to Staging (if main branch)

Total: ~10 minutes
```
```

---

### 7. Pain Points & Gotchas

**Provide:**
- Known bugs or limitations
- Non-obvious behaviors (tribal knowledge)
- Performance bottlenecks
- Areas with technical debt
- Common mistakes to avoid

**Template:**
```markdown
## Known Issues & Gotchas

### Performance
- **N+1 Query Problem**: Fetching orders without batching. Always use JOIN or batch queries.
  - Bad: `for order_id in order_ids: order = db.fetch(order_id)`
  - Good: `orders = db.fetch_batch(order_id_list)`

- **Redis Cache Invalidation**: Stale cache after refund can cause double-charging if not careful.
  - Solution: Always clear cache when refund is processed

### Bugs & Limitations
- Refunds can only be done within 90 days of charge (Stripe limitation)
- Large payouts (>$100k) are delayed 7 days in test mode
- ⚠️ Webhook retries sometimes arrive out-of-order

### Non-Obvious Behaviors
- **Idempotency**: All POST requests should be idempotent (check Idempotency-Key header)
- **Stripe Webhooks**: Can arrive multiple times, always check if payment already processed
- **Time Zones**: Store all times in UTC, only convert for display

### Technical Debt
- Legacy card tokenization code (replace with Stripe elements in next release)
- TODO: Migrate from synchronous to event-based order fulfillment
- TODO: Add monitoring for refund failures

### Mistakes I Made (so you don't)
- "I didn't validate amount on both sides, led to overcharging" → Always validate server-side
- "I cached payment status without TTL, old data caused confusion" → Always set cache TTL
- "I didn't handle network timeouts, orders got stuck in 'pending'" → Always set timeouts
```

---

### 8. Monitoring & Observability

**Provide:**
- Key dashboards (links + what to look for)
- Alert rules (what triggers alerts, what on-call does)
- Log locations and important messages
- How to debug in production (safely)
- Incident response runbooks

**Template:**
```markdown
## Monitoring

### Dashboards
- **Payment Success Rate**: https://datadog.company.com/payment-success-rate
  - What to look for: > 99% success. Below 95% = page on-call
  - How to investigate: Check payment-service error logs, Stripe status

- **Payment Latency (p99)**: https://datadog.company.com/payment-latency
  - What to look for: < 500ms. Above 1s = page on-call
  - How to investigate: Database slow queries? Stripe slow? Network latency?

- **Refund Processing**: https://datadog.company.com/refund-processing
  - What to look for: All refunds processed within 1 hour
  - How to investigate: Check async job queue, message broker

### Alert Rules
```
| Alert | Trigger | Action |
|-------|---------|--------|
| Payment failures spike | >1% error rate for 5 min | Page on-call |
| Database connection pool exhausted | All connections in use | Page on-call (critical) |
| Stripe API timeout | Response time > 10s | Warn in Slack (not critical) |
| Refund job failures | > 10 failed refunds in 1 hour | Page on-call |
```

### Log Locations
- Application logs: `kubectl logs -f deployment/payment-service-prod`
- Database logs: AWS RDS CloudWatch
- Stripe logs: https://dashboard.stripe.com/test/logs

### Important Log Messages
```
[ERROR] "Stripe charge failed" payment_id=X error_code=card_declined
  → Customer's card was declined, not our problem

[ERROR] "Stripe charge failed" payment_id=X error_code=rate_limit_exceeded
  → We're hitting Stripe rate limits, implement backoff

[ERROR] "Database connection timeout" pool_exhausted=true active_connections=100
  → Connection leak, restart service and investigate
```

### Production Debugging (Safe)
```bash
# 1. Never modify production data manually
# 2. Safe queries: read-only
# 3. Check logs first: `kubectl logs -f deployment/...`
# 4. Check metrics: Dashboard for latency, error rate
# 5. If truly stuck, follow incident runbook

# Safe debugging commands:
$ kubectl exec -it pod-name -- bash
$ psql $DATABASE_URL -c "SELECT * FROM payments WHERE id = 'pay_123';"
$ redis-cli -h redis-host GET payment:pay_123
```

### Incident Response
- If payment success rate drops: See `/runbook-payment-failures.md`
- If service is down: See `/runbook-service-down.md`
- If database is slow: See `/runbook-database-slow.md`
```

---

### 9. Deployment & Operations

**Provide:**
- How code gets deployed
- Rollback procedures
- Database migrations
- Configuration management
- Post-deployment verification

**Template:**
```markdown
## Deployment

### How to Deploy
```bash
# 1. Create PR with your changes
# 2. Get approval from tech lead
# 3. Merge to main (triggers CI/CD)
# 4. CI runs tests (10 min)
# 5. Staging deployment (automatic)
# 6. Manual promotion to production via:

make deploy-prod  # Runs on your machine
# OR via UI: go to https://deploy.company.com/payment-service

# Deployment: rolling update (no downtime)
# - 1 pod at a time
# - Health checks verify each pod
# - Can abort if checks fail
```

### Rollback
```bash
# If something breaks:
make rollback-prod   # Rolls back to previous version
# Takes ~2 minutes, no downtime
```

### Database Migrations
```bash
# Before deploying code that changes schema:
1. Create migration: `make migration create_payment_index`
2. Write SQL in migrations/001_create_payment_index.sql
3. Test migration: `make migration test`
4. Deploy migration first: `make deploy-db-migrations`
5. Then deploy code that uses new schema
```

### Configuration
- Environment variables in Kubernetes secrets
- Feature flags in Unleash (release features gradually)
- For hotfixes: Can update environment variables without redeploying

### Post-Deployment Verification
```bash
# After deployment:
1. Check dashboard (success rate, latency)
2. Check alerts (no new errors)
3. Run smoke tests: make smoke-test-prod
4. Monitor for 1 hour before declaring success
```

---

### 10. Product Context

**Provide:**
- What user-facing features use this service
- Product roadmap (what's planned)
- Pending decisions or open questions
- Product metrics (what the business cares about)
- How this service fits into larger product

**Template:**
```markdown
## Product Context

### User Features
- Users make purchases and pay with credit card (uses Payment Service)
- Admins can refund orders (uses Payment Service)
- Users see order confirmation with receipt (uses Payment Service data)

### Roadmap
- Q2: Add Apple Pay / Google Pay support
- Q3: Split payments (pay part now, part later)
- Q4: Buy now, pay later (BNPL) integration

### Open Questions
- Should we support cryptocurrency payments? (Customer request, not decided yet)
- How long to keep payment records? (Currently 7 years, compliance TBD)

### Product Metrics
- Conversion rate (users who pay / users who start checkout)
- Average order value (AOV)
- Payment success rate (our KPI: > 99%)
- Refund rate (% of orders refunded)

### System Fit
```
Payment Service is the core of our monetization:
User Flow: Browse Catalog → Add to Cart → Checkout → Payment Service → Order Complete
Revenue Flow: Customer Pays → Payment Service → Company Account (minus Stripe fees)
```
```

---

### 11. Demo & Hands-On

**Provide:**
- Key API calls to demo (with curl examples)
- Example requests/responses
- Workflow walkthroughs
- UI flows (if applicable)
- "Try it yourself" exercises

**Template:**
```markdown
## Demo & Hands-On

### Key API Calls

**1. Charge a customer**
```bash
curl -X POST http://localhost:8080/api/payments/charge \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": "ord_123",
    "amount": 99.99,
    "currency": "USD",
    "card_token": "tok_visa_4242"
  }'

Response: {"payment_id": "pay_456", "status": "completed"}
```

**2. Refund a payment**
```bash
curl -X POST http://localhost:8080/api/payments/pay_456/refund \
  -H "Content-Type: application/json" \
  -d '{"reason": "customer_request"}'

Response: {"refund_id": "ref_789", "status": "pending"}
```

**3. Check payment status**
```bash
curl http://localhost:8080/api/payments/pay_456

Response: {
  "payment_id": "pay_456",
  "order_id": "ord_123",
  "amount": 99.99,
  "status": "completed",
  "created_at": "2026-01-11T10:00:00Z"
}
```

### Workflow Demo
1. Start server: `make run`
2. Create order: `curl -X POST http://localhost:8080/api/orders`
3. List orders: `curl http://localhost:8080/api/orders`
4. Charge payment: Use curl command above with test card
5. Check dashboard: https://dashboard.stripe.com/test/payments

### Exercises for New Dev
- [ ] Run local tests (should pass)
- [ ] Create test payment (use test card: 4242 4242 4242 4242)
- [ ] Refund a test payment
- [ ] Modify code, run tests, commit
- [ ] Deploy to staging, verify works
```

---

### 12. FAQs

**Provide:**
- Common questions new developers ask
- Quick answers with links to details
- Troubleshooting tips

**Template:**
```markdown
## FAQs

**Q: How do I test a payment locally?**
A: Use Stripe test keys and test card 4242 4242 4242 4242. See [Local Setup](#local-setup)

**Q: Why is my test payment declining?**
A: Check Stripe dashboard for errors. Common: wrong amount format, expired test key.

**Q: How do I debug a stuck payment?**
A: Check logs: `kubectl logs -f deployment/payment-service-prod | grep payment_id`

**Q: Can I deploy on a Friday?**
A: Yes, but stay online for 1 hour post-deploy to monitor. Incident runbook ready at `/runbook-payment-failures.md`

**Q: Who do I page if something breaks?**
A: Check who's on-call: `make check-oncall`. Page them via PagerDuty.

**Q: Where do I find the database password?**
A: Never hardcoded. Kubernetes secret: `kubectl get secret payment-db-creds`

**Q: How do I add a new payment method (Apple Pay)?**
A: See [feature development guide](#feature-development). Stripe has good docs for new methods.
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

- `/pb-onboarding` — Full team onboarding (includes KT)
- `/pb-guide` — SDLC guide (referenced in KT)
- `/pb-security` — Security considerations during KT
- `/pb-adr` — Architecture decisions (why choices were made)
- `/pb-incident` — Incident runbooks (part of KT package)

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
