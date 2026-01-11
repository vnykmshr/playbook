# Architecture Decision Record (ADR)

Document significant architectural decisions to capture the context, alternatives considered, and rationale for future reference.

---

## When to Write an ADR

Write an ADR when:
- Choosing between multiple valid technical approaches
- Adopting a new technology, library, or pattern
- Making decisions that affect system architecture
- Changing existing architectural patterns
- Decisions that will be hard to reverse

Don't write an ADR for:
- Obvious implementation choices
- Temporary workarounds (document differently)
- Decisions that can easily be changed later

---

## ADR Template

Create ADR files at: `docs/adr/NNNN-title-with-dashes.md`

```markdown
# ADR-NNNN: [Title]

**Date:** YYYY-MM-DD
**Status:** [Proposed | Accepted | Deprecated | Superseded by ADR-XXXX]
**Deciders:** [Names/roles involved]

## Context

[What is the issue we're addressing? What forces are at play?
Include technical constraints, business requirements, and team context.
Be specific about the problem, not the solution.]

## Decision

[What is the change we're proposing and/or doing?
State the decision clearly and directly.]

## Alternatives Considered

### Option A: [Name]
[Brief description]

**Pros:**
- [Pro 1]
- [Pro 2]

**Cons:**
- [Con 1]
- [Con 2]

### Option B: [Name]
[Brief description]

**Pros:**
- [Pro 1]

**Cons:**
- [Con 1]

### Option C: [Name] (Selected)
[Brief description]

**Pros:**
- [Pro 1]
- [Pro 2]

**Cons:**
- [Con 1]

## Rationale

[Why did we choose this option over the others?
What were the deciding factors?
What trade-offs are we accepting?]

## Consequences

**Positive:**
- [Benefit 1]
- [Benefit 2]

**Negative:**
- [Drawback 1]
- [Drawback 2]

**Neutral:**
- [Side effect that's neither good nor bad]

## Implementation Notes

[Any specific implementation guidance.
Things to watch out for.
Migration steps if applicable.]

## References

- [Link to relevant docs, issues, or discussions]
- [Related ADRs]
```

---

## ADR Numbering

Use sequential 4-digit numbers:
- `0001-initial-architecture.md`
- `0002-database-selection.md`
- `0003-authentication-strategy.md`

---

## Example ADR

```markdown
# ADR-0015: Self-Hosted Fonts Instead of Google Fonts

**Date:** 2026-01-04
**Status:** Accepted
**Deciders:** Engineering team

## Context

The application uses multiple custom fonts for different themes. Currently loading
from Google Fonts CDN, which introduces:
- External dependency and privacy concerns
- Render-blocking requests
- FOUT (Flash of Unstyled Text) on slow connections

Performance audits show font loading accounts for 400ms+ of blocking time.

## Decision

Self-host all fonts using @fontsource packages. Implement lazy loading for
theme-specific fonts.

## Alternatives Considered

### Option A: Keep Google Fonts
**Pros:** Zero maintenance, CDN caching
**Cons:** Privacy, render-blocking, external dependency

### Option B: Self-host with preload all
**Pros:** No external dependency, control over loading
**Cons:** Large initial payload, wasted bandwidth for unused themes

### Option C: Self-host with lazy loading (Selected)
**Pros:** Control over loading, minimal initial payload, load only what's needed
**Cons:** Slight complexity in implementation

## Rationale

Option C provides the best balance: eliminates external dependency while
minimizing payload through lazy loading of theme-specific fonts.

## Consequences

**Positive:**
- 87% reduction in render-blocking time
- No external dependencies
- Privacy-friendly (no Google tracking)

**Negative:**
- Slightly larger bundle (fonts in assets)
- Need to update fonts manually

## Implementation Notes

- Critical fonts (Inter, Noto Serif Devanagari) preloaded
- Theme fonts loaded on theme selection
- Font files in `/public/fonts/`
```

---

## Example ADRs (Additional)

### Example 2: Database Selection (PostgreSQL vs MongoDB)

```markdown
# ADR-0001: PostgreSQL for Primary Database

**Date:** 2026-01-05
**Status:** Accepted
**Deciders:** Engineering team, Tech lead

## Context

Building a new SaaS application. Need to select primary data store for user accounts, billing,
and product data. Team has experience with both SQL and NoSQL. Requirements:
- Strong consistency (financial transactions)
- Complex queries across related data
- ACID transactions required
- Expected growth: 100M+ records over 5 years

## Decision

Use PostgreSQL as primary database. Use Redis for caching and sessions.

## Alternatives Considered

### Option A: PostgreSQL (Selected)
**Pros:**
- ACID guarantees for transactions
- Complex queries with JOINs
- Strong consistency
- Mature tooling and libraries
- Battle-tested at scale

**Cons:**
- Requires schema design upfront
- Vertical scaling limitations (horizontal scaling complex)
- Not ideal for unstructured data

### Option B: MongoDB
**Pros:**
- Flexible schema (iterate quickly)
- Built-in horizontal scaling
- Good for unstructured data
- Document-oriented (natural data model for some use cases)

**Cons:**
- Eventual consistency (problematic for financial data)
- Complex transactions until v4.0+
- Higher memory footprint
- Harder to query across documents

### Option C: Multi-database (PostgreSQL + MongoDB)
**Pros:**
- Best of both worlds
- Flexibility by data type

**Cons:**
- Operational complexity
- Data sync challenges
- Increased maintenance burden

## Rationale

Financial data (billing, subscriptions, payments) demands ACID guarantees. Complex reporting
queries (user analytics, revenue reports) benefit from SQL. PostgreSQL's maturity and
proven scaling strategies at companies like Stripe, Pinterest, Instagram make it the best fit.

## Consequences

**Positive:**
- Data integrity guaranteed
- Complex queries fast and efficient
- Excellent ecosystem (ORMs, migration tools, monitoring)
- Smaller operational footprint than MongoDB

**Negative:**
- Schema migrations required when data model changes
- Developers must think about schema design upfront
- Scaling read load requires replication setup

**Neutral:**
- Network latency same as MongoDB for single-node setup

## Implementation Notes

- Use connection pooling (PgBouncer) from day 1
- Set up read replicas before launch for analytics queries
- Configure backup strategy (WAL archiving, pg_basebackup)
- Monitor table bloat and run VACUUM regularly
- Use indexes strategically (query plans matter)
```

---

### Example 3: Authentication Strategy (JWT vs OAuth2 vs Session-based)

```markdown
# ADR-0002: JWT with Refresh Tokens for Authentication

**Date:** 2026-01-07
**Status:** Accepted
**Deciders:** Engineering team, Security lead

## Context

Building SPA (React) + mobile app (iOS/Android) + backend. Need stateless authentication
that works across multiple clients. Requirements:
- Support web, iOS, Android clients
- Stateless backend (can scale horizontally)
- Secure token revocation (logout)
- Standard industry practice

## Decision

Use JWT (JSON Web Tokens) with refresh token rotation. Short-lived access tokens (15 min),
longer-lived refresh tokens (7 days) with rotation on each refresh.

## Alternatives Considered

### Option A: Session-based (traditional)
**Pros:**
- Simple to understand
- Easy token revocation
- Built-in CSRF protection (when using cookies)
- Server controls session lifetime

**Cons:**
- Requires server-side session storage
- Doesn't scale well horizontally (session affinity needed or shared store)
- Poor mobile experience (cookies not ideal)
- Logout requires server cleanup

### Option B: JWT without refresh tokens
**Pros:**
- Stateless, scales horizontally
- Works great for mobile/SPA

**Cons:**
- Long token lifetime = security risk if token stolen
- Can't revoke tokens (except via blacklist, defeating statelessness)
- Logout doesn't actually log you out (token still valid)

### Option C: JWT with refresh tokens (Selected)
**Pros:**
- Stateless backend (scales horizontally)
- Secure: access token short-lived, refresh token rotated
- Logout works (invalidate refresh token)
- Works for web, mobile, SPA
- Standard industry practice

**Cons:**
- More complex than simple sessions
- Requires client-side refresh token storage (secure HttpOnly cookie recommended)
- Extra network call when token expires

## Rationale

Refresh token rotation provides security benefits of short-lived tokens without
logout UX issues. Industry standard used by Auth0, Firebase, AWS Cognito.

## Consequences

**Positive:**
- Horizontal scaling without session store
- Logout is instant (revoke refresh token)
- Security: token theft has limited window
- Mobile-friendly

**Negative:**
- Slightly more implementation complexity
- Requires secure refresh token storage
- Extra API call on token refresh

**Neutral:**
- Network latency barely noticeable (typical 20-50ms refresh call)

## Implementation Notes

- Access token lifetime: 15 minutes (tradeoff between security and UX)
- Refresh token lifetime: 7 days
- Rotate refresh token on each use (new refresh token returned)
- Store refresh token in httpOnly, secure cookie (not localStorage)
- Include token fingerprint to prevent token reuse attacks
- Implement refresh token revocation list for logout
```

---

### Example 4: Caching Strategy (Redis vs In-memory vs CDN)

```markdown
# ADR-0003: Tiered Caching Strategy (CDN + Redis + In-memory)

**Date:** 2026-01-08
**Status:** Accepted
**Deciders:** Engineering team, Infrastructure team

## Context

Application serves millions of requests daily with 30% cache-able content (product data,
user profiles, configurations). Current approach (no caching) causes N+1 queries and
slow response times. Need to balance cost, complexity, and performance.

Requirements:
- <100ms p99 latency
- 50M+ requests/day
- Global users (US + EU)
- Cache invalidation must be reliable

## Decision

Implement three-tier caching:
1. CDN (CloudFront) for static assets and API responses
2. Redis for session data and frequently accessed objects
3. In-memory application cache for hot data

## Alternatives Considered

### Option A: Redis only
**Pros:**
- Simple to understand
- Works globally (with replication)

**Cons:**
- Extra network hop (vs in-memory)
- Database load on cache misses
- Single point of failure (high availability needed)
- Expensive at scale

### Option B: In-memory only
**Pros:**
- Fastest possible (no network)
- No operational overhead

**Cons:**
- Data lost on restart
- Doesn't work for distributed systems
- Cache invalidation complexity across instances
- Can't share session data across servers

### Option C: Tiered caching (Selected)
**Pros:**
- Best performance (hit CDN first, Redis second, in-memory third)
- Cost-effective (CDN is cheap for static content)
- Resilient (fallback if one layer fails)
- Scales to billions of requests

**Cons:**
- More complex (three systems to manage)
- Cache invalidation across layers
- Potential stale data issues

## Rationale

Real-world performance requires multiple cache layers. Netflix, Uber, Airbnb use similar
patterns. Each layer serves different purposes: CDN for geographic distribution, Redis
for shared state, in-memory for hot data.

## Consequences

**Positive:**
- P99 latency drops from 500ms to 50ms
- Reduced database load (70% hit rate)
- Global performance (CDN)
- Cost-effective at scale

**Negative:**
- Operational complexity (managing 3 systems)
- Cache invalidation harder to reason about
- Potential stale data (eventual consistency)

**Neutral:**
- Need to monitor cache hit rates separately

## Implementation Notes

- CDN cache TTL: 1 hour for product data, 5 min for user data
- Redis TTL: 15 minutes
- In-memory TTL: 5 minutes
- Cache invalidation: Event-driven (webhook on data change)
- Monitor: Cache hit rates, eviction rates, memory usage
```

---

## ADR Lifecycle

```
Proposed → Accepted → [Active]
                   ↓
              Deprecated (no longer applies)
                   or
              Superseded (replaced by new ADR)
```

When superseding:
1. Create new ADR with updated decision
2. Update old ADR status to "Superseded by ADR-XXXX"
3. Reference old ADR in new ADR's context

---

## Directory Structure

```
docs/
└── adr/
    ├── 0001-initial-architecture.md
    ├── 0002-database-selection.md
    ├── 0003-authentication-strategy.md
    ├── ...
    └── README.md  # Index of all ADRs
```

### ADR Index Template

```markdown
# Architecture Decision Records

| ADR | Title | Status | Date |
|-----|-------|--------|------|
| [0001](0001-initial-architecture.md) | Initial Architecture | Accepted | 2025-01-01 |
| [0002](0002-database-selection.md) | PostgreSQL for Primary Database | Accepted | 2025-01-05 |
```

---

## Tips for Good ADRs

1. **Write in present tense** - "We decide" not "We decided"
2. **Be specific** - Vague context leads to vague decisions
3. **Include alternatives** - Shows you considered options
4. **State trade-offs** - No decision is perfect, acknowledge downsides
5. **Keep it concise** - 1-2 pages max
6. **Link to context** - Reference issues, PRs, discussions

---

*Decisions as code. Future you will thank present you.*
