---
name: "pb-documentation"
title: "Writing Great Engineering Documentation"
category: "core"
difficulty: "beginner"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-adr', 'pb-review-docs', 'pb-repo-readme', 'pb-repo-blog', 'pb-onboarding']
last_reviewed: "2026-02-09"
last_evolved: ""
version: "1.0.0"
version_notes: "v2.10.0 baseline"
breaking_changes: []
---
# Writing Great Engineering Documentation

Clear documentation enables people to work independently, makes knowledge transferable, and saves time.

**Mindset:** Documentation should invite scrutiny. Be clear enough that errors are obvious.

This embodies `/pb-preamble` thinking (clear writing enables critical thinking, ambiguous docs hide flawed thinking) and applies `/pb-design-rules` thinking, particularly:

**Key Design Rules for Documentation:**
- **Clarity**: Documentation must be crystal clear so readers immediately understand the system
- **Representation**: Information architecture matters—organize docs so knowledge is findable, not buried
- **Least Surprise**: Documentation should behave like readers expect; no hidden gotchas or contradictions

**Resource Hint:** sonnet — Documentation writing is implementation-level work; routine quality standards.

---

## When to Use This Command

- **Writing new docs** — Creating READMEs, guides, API docs
- **Improving existing docs** — Docs review found issues to fix
- **Onboarding prep** — Ensuring docs support new team members
- **Knowledge transfer** — Capturing tribal knowledge before someone leaves
- **Architecture documentation** — Documenting system design decisions

---

## Purpose

Good documentation:
- **Enables onboarding**: New people learn faster
- **Preserves knowledge**: Doesn't disappear when people leave
- **Reduces questions**: People can find answers themselves
- **Saves debugging time**: Common issues documented with solutions
- **Improves quality**: Explains design, catches inconsistencies
- **Enables async work**: Remote teams need written context

Bad documentation:
- Outdated (last updated 2 years ago)
- Incomplete ("see code for details")
- Wrong (misleading, inaccurate)
- Scattered (spread across 10 places)
- Unreadable (walls of text, no examples)

---

## Documentation Levels

### Level 1: Code Comments

**Purpose**: Explain why code exists, not what it does.

Good code is self-documenting:
```python
# Bad
x = y + 2  # Add 2
delay = 1000 * 60  # Delay

# Good
buffer_size = max_size + overhead  # Account for header
wait_time_ms = seconds_to_wait * 1000  # Convert to milliseconds
```

**What to comment:**
- Why a non-obvious approach was chosen
- Warning about common mistakes
- Reference to related code
- Complex logic (but usually means refactor instead)

```python
# Bad comment (obvious)
def add(a, b):
    # Add a and b
    return a + b

# Good comment (explains non-obvious)
def calculate_deadline(start_time):
    # Add 5 days but skip weekends (business days only)
    # See accounting_spec.md for requirements
    days = 5
    current = start_time
    while days > 0:
        current += timedelta(days=1)
        if current.weekday() < 5:  # 0-4 = Mon-Fri
            days -= 1
    return current
```

### Level 2: Function/Module Documentation

**Purpose**: Tell someone reading code what it does and how to use it.

```python
def create_order(customer_id, items, payment_method):
    """
    Create a new order for a customer.

    Args:
        customer_id: ID of customer placing order
        items: List of {product_id, quantity}
        payment_method: "credit_card" or "bank_transfer"

    Returns:
        Order object with fields: id, status, total, created_at

    Raises:
        ValueError: If items is empty
        PaymentError: If payment fails

    Note:
        - Inventory is decremented immediately
        - Email confirmation sent asynchronously
        - See order_processing.md for state diagram
    """
```

**TypeScript/JavaScript:**
```typescript
/**
 * Fetch user profile with optional caching
 *
 * @param userId - User ID to fetch
 * @param options.useCache - Cache result for 5 minutes (default: true)
 * @returns Promise resolving to User object
 * @throws NotFoundError if user doesn't exist
 *
 * @example
 * const user = await fetchUser('user_123');
 * const freshUser = await fetchUser('user_123', { useCache: false });
 */
async function fetchUser(userId: string, options?: { useCache?: boolean }): Promise<User> {
```

### Level 3: API/Integration Documentation

**Purpose**: Help someone use the API/service without reading code.

```markdown
# Payment API

## Overview
The Payment API handles charging customers, refunds, and payment status.

## Base URL
`https://api.example.com/v1`

## Authentication
All requests must include header: `Authorization: Bearer {token}`

## Endpoints

### Create Order
```
POST /orders
Content-Type: application/json

Request:
{
  "customer_id": "cust_123",
  "items": [
    {"product_id": "prod_1", "quantity": 2}
  ],
  "payment_method": "credit_card"
}

Response (201):
{
  "id": "order_456",
  "status": "pending_payment",
  "total": 99.99,
  "created_at": "2026-01-11T14:30:00Z"
}

Error (400):
{
  "error": "missing_required_field",
  "message": "items cannot be empty"
}
```

## Rate Limiting
100 requests per minute per API key

## Webhooks
- `order.created` — Order created
- `payment.succeeded` — Payment processed
- `payment.failed` — Payment failed

See webhook specification in #webhooks section
```

### Level 4: System Documentation

**Purpose**: Help someone understand how systems fit together.

**What to include:**
```markdown
# Payment System Architecture

## Purpose
Process payments, handle refunds, track payment status.

## Components
- Payment API (Node.js)
- Payment Database (PostgreSQL)
- Stripe integration (external)
- Webhook handler (async processor)
- Audit log (for compliance)

## Diagram
```
User → Payment API → Stripe
                   ↓
              Payment DB
              Audit Log
```

## Data Flow
1. User submits payment
2. API sends to Stripe
3. Stripe responds with status
4. API stores in DB
5. Webhook fires (order.paid)
6. Email sent asynchronously

## Key Decisions
- Why Stripe? See ADR-2024-001
- Why PostgreSQL? See ADR-2024-002

## Scaling Concerns
- Stripe timeout handling (retry with exponential backoff)
- Audit log growth (partition by date)

## Related Systems
- Order system (creates orders)
- Email system (sends confirmations)
- Billing system (monthly invoices)

## Runbooks
- Payment processing stuck: See runbook-payment-stuck.md
- Database grew too large: See runbook-db-size.md
```

### Level 5: Process Documentation

**Purpose**: Help someone follow a process or handle an event.

```markdown
# Release Process

## Overview
Releasing code to production involves building, testing, and deploying.

## Steps
1. Create release branch (release/v1.2.3)
2. Update CHANGELOG
3. Tag commit (v1.2.3)
4. Build Docker image
5. Deploy to staging
6. Run smoke tests
7. Deploy to production
8. Monitor for errors

## Detailed Steps

### 1. Create Release Branch
```bash
git checkout -b release/v1.2.3 main
```
Why: Isolates release prep from ongoing development

### 2. Update Changelog
Edit CHANGELOG.md:
- Add new version (v1.2.3)
- List features added, bugs fixed, breaking changes
- Include author names

Example:
```
## [1.2.3] - 2026-01-11
### Added
- Support for bulk user import (#234)
- New analytics dashboard (#245)
### Fixed
- Bug: Orders not showing in some cases (#240)
### Breaking
- Removed deprecated /v1/orders endpoint
```

### 3. Tag Commit
```bash
git tag -a v1.2.3 -m "Release version 1.2.3"
git push origin v1.2.3
```

### 4. Build Docker Image
CI/CD automatically builds when tag pushed.
Check: CI pipeline passes all checks.

### 5. Deploy to Staging
```bash
./deploy staging v1.2.3
./run-smoke-tests staging
```

Check:
- Smoke tests pass
- No errors in logs
- Performance acceptable
- Database migrations successful

### 6. Deploy to Production
```bash
./deploy production v1.2.3
```

Monitor:
- Error rate (should be same as before)
- Latency (should be same as before)
- Resource usage (should be reasonable)
- User complaints (check Slack)

### 7. Post-Release
- Send release notes to stakeholders
- Update documentation
- Monitor for issues
- Be available for next 2 hours

## Rollback
If something breaks:
```bash
./deploy production v1.2.2
```
Fast: < 2 minutes
Safe: Previous version still tested
```

---

## Writing Guidelines

### 1. Know Your Audience

Different people need different docs:

```
Junior Developer:
  - Detailed step-by-step
  - Explain assumptions
  - Show examples
  - Link to further reading

Experienced Developer:
  - Quick reference
  - Why, not what
  - Key decisions/gotchas
  - Links to detailed docs

DevOps Engineer:
  - Architecture overview
  - Infrastructure requirements
  - Scaling considerations
  - Monitoring/alerting
```

### 2. Use Clear Structure

Bad:
```
The system works by first doing thing A which connects to thing B
and then thing C happens which processes the data from B, so then
you get the result in D. Sometimes if D fails you should check B.
```

Good:
```
## How the system works

1. **Data Collection (Component A)**
   Gathers input from users

2. **Processing (Component B)**
   Transforms data according to rules

3. **Storage (Component C)**
   Saves result to database

## If processing fails
Check Component B logs for errors
```

### 3. Show Examples

Always show examples, even for simple things.

Bad:
```
Use the create_order function to create orders.
```

Good:
```
Use the create_order function to create orders:

```python
order = create_order(
    customer_id="cust_123",
    items=[
        {"product_id": "prod_1", "quantity": 2},
        {"product_id": "prod_2", "quantity": 1}
    ]
)
print(f"Order created: {order.id}")
```

## Common mistakes
- Empty items list (will raise ValueError)
- Forgetting payment method (will fail at checkout)
```

### 4. Keep It Updated

**Stale docs are worse than no docs.**

Outdated docs:
```
# Installing

1. Clone the repo
2. Install Node 14  ← Node 14 is deprecated!
3. Run npm install
4. npm start
```

Fix:
```
# Installing

1. Clone the repo
2. Install Node 18+ (required)
   - macOS: `brew install node@18`
   - Ubuntu: `sudo apt-get install nodejs=18.*`
3. Run `npm install`
4. Run `npm start`

Last updated: 2026-01-11
```

**How to keep docs updated:**

```
- Link docs in code review (remind people they exist)
- Update docs in same PR as code change
- Schedule quarterly review (is this still accurate?)
- Delete docs that no longer apply
- Note last-updated date prominently
```

### 5. Use Visuals

Pictures convey information faster.

Text:
```
The system has a frontend that talks to an API which talks to a database
and also talks to an external payment service.
```

Diagram:
```
┌─────────┐      ┌─────┐       ┌──────────┐
│Frontend │─────→│ API │──────→│ Database │
└─────────┘      └─────┘       └──────────┘
                    │
                    ↓
              ┌──────────────┐
              │Payment Service│
              └──────────────┘
```

Tools:
- **Mermaid**: Embed diagrams in markdown
- **Excalidraw**: Draw diagrams quickly
- **Lucidchart**: More complex diagrams
- **ASCII art**: Simple diagrams in text

### 6. Link, Don't Repeat

Bad:
```
# API Documentation

The API requires authentication...
(then 500 words about auth)

# Database Documentation

The database requires authentication...
(same 500 words repeated)
```

Good:
```
# API Documentation
See Authentication section below.

# Database Documentation
See Authentication section below.

# Authentication (Single Source of Truth)
[Detailed auth explanation once]
```

### 7. Make It Scannable

People don't read documentation linearly. They scan.

Bad:
```
To set up, first you need to have docker installed, you can get it from
docker.com, then you run docker-compose up which will start the database,
after that you can run npm install and then npm start to start the server
```

Good:
```
## Setup

### Prerequisites
- Docker installed from docker.com
- Node 18+
- npm 9+

### Steps
1. Start database: `docker-compose up -d`
2. Install dependencies: `npm install`
3. Start server: `npm start`
4. Visit http://localhost:3000
```

---

## Documentation Templates

### README.md Template

```markdown
# Project Name

Short description of what this does.

## Features
- Feature 1
- Feature 2

## Quick Start

### Prerequisites
- Node 18+
- PostgreSQL 14+

### Installation
```bash
git clone ...
cd ...
npm install
npm run setup-db
npm start
```

Visit http://localhost:3000

## Documentation
- [Architecture](docs/architecture.md)
- [API Reference](docs/api.md)
- [Contributing](docs/contributing.md)
- [Troubleshooting](docs/troubleshooting.md)

## Getting Help
- Slack: #engineering
- Issues: GitHub issues
- Email: team@example.com
```

### API Documentation Template

```markdown
# API Name

## Overview
What does this API do?

## Base URL
`https://api.example.com/v1`

## Authentication
How to authenticate?

## Endpoints

### Create Resource
```
POST /resources
Content-Type: application/json

Request: {...}
Response (201): {...}
Error (400): {...}
```

## Rate Limiting
Limits and behavior

## Webhooks
What events are available?

## SDK
Available libraries for common languages
```

### Architecture Documentation Template

```markdown
# System Architecture

## Purpose
Why does this system exist?

## Components
- Component A: What it does
- Component B: What it does

## Diagram
[Visual diagram]

## Data Flow
How data moves through system

## Key Decisions
Why were choices made?

## Scaling
How does it scale?

## Monitoring
What to watch for?

## Runbooks
- [Common issue 1](runbook-1.md)
- [Common issue 2](runbook-2.md)
```

---

## Documentation Tools & Organization

### Tools

| Tool | Use For | Example |
|------|---------|---------|
| README.md | Quick start, overview | How to get running |
| Markdown files | Detailed docs | Architecture, guides |
| ADR folder | Design decisions | Why we chose X |
| Runbooks | How to fix things | Recovery procedures |
| API docs | API reference | Endpoint definitions |
| Video | Complex processes | Architecture walkthrough |
| Diagrams | Visual understanding | System flows |
| Code comments | Why code exists | Explain non-obvious |

### Organization

Good structure:
```
Project/
  README.md (Start here)
  docs/
    architecture.md (System design)
    api.md (API reference)
    getting-started.md (Setup guide)
    troubleshooting.md (Common issues)
    adr/ (Design decisions)
      adr-001-database-choice.md
      adr-002-api-versioning.md
    runbooks/ (How to fix things)
      runbook-payment-stuck.md
      runbook-database-full.md
    images/ (Diagrams, screenshots)
  src/ (Code with clear structure)
```

Bad structure:
```
Project/
  README.md (Outdated, hard to follow)
  doc-old.md (Obsolete)
  NOTES.txt (Unclear)
  docs/
    stuff.md (What is this?)
    more-stuff.md (Unclear title)
  Lots of scattered documentation
```

---

## Documentation Maintenance

### Quarterly Review

Each quarter:
```
1. Read each doc
2. Is it still accurate? (Mark last-updated date)
3. Is it clear? (Ask someone else to read it)
4. Is it complete? (What's missing?)
5. Delete obsolete docs
```

### Keep Docs in Sync with Code

Bad:
```
Engineer changes code but doesn't update docs
Docs become wrong
New person reads old docs, confused
```

Good:
```
Engineer changes code AND updates docs
PR review checks that docs match code
Docs stay accurate
```

In code review:
```
Reviewer: "You added a new API. Did you update docs/api.md?"
Engineer: "Yes, added new endpoint and examples"
```

---

## Integration with Playbook

**Part of SDLC:**
- `/pb-guide` — Document requirements by project size
- `/pb-onboarding` — Good docs enable self-guided learning
- `/pb-adr` — Documenting decisions
- `/pb-security` — Documenting security practices

---

## Related Commands

- `/pb-adr` — How to document decisions
- `/pb-review-docs` — Documentation quality review
- `/pb-sam-documentation` — Clarity-first documentation review (see "When to Use" for integration)
- `/pb-repo-readme` — Generate project README
- `/pb-repo-blog` — Write technical blog post
- `/pb-onboarding` — Using docs for training

---

## Documentation Checklist

- [ ] README exists and is current
- [ ] Getting started guide works (tested)
- [ ] Architecture documented with diagrams
- [ ] API endpoints documented with examples
- [ ] Key decisions documented (ADRs)
- [ ] Common issues documented (troubleshooting)
- [ ] Setup/deploy procedures documented (runbooks)
- [ ] Code is self-documenting (good names, structure)
- [ ] Comments explain why, not what
- [ ] Last-updated date shown
- [ ] Docs are linked in code (easy to find)
- [ ] Broken links checked
- [ ] Examples actually work
- [ ] Docs reviewed quarterly
- [ ] Obsolete docs deleted

---

*Created: 2026-01-11 | Category: Documentation | Tier: M/L*

