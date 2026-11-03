---
name: "pb-patterns-core"
title: "Core Architecture & Design Patterns"
category: "planning"
difficulty: "advanced"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-patterns-resilience', 'pb-patterns-async', 'pb-patterns-db', 'pb-patterns-distributed', 'pb-adr']
last_reviewed: "2026-11-04"
last_evolved: ""
version: "2.0.0"
version_notes: "v2.0.0: Cut from 658 to 189 lines: example code, walkthroughs and language sections removed; decisions, gotchas and when-to-use kept. Repository says when not to use it."
breaking_changes: ['Example code, walkthroughs and language sections removed; decisions and gotchas kept, constraints from removed code restated; deploy checklists live in /pb-preflight and /pb-deployment.']
---
# Core Architecture & Design Patterns

Proven solutions to recurring problems. Patterns speed up design and prevent mistakes.

---

**Mindset:** Every pattern has trade-offs. Use `/pb-preamble` thinking (challenge assumptions, surface costs) and `/pb-design-rules` thinking (does this pattern serve Clarity, Simplicity, Modularity?).

Challenge whether this pattern is the right fit for your constraints. Surface the actual costs. Understand the alternatives. A pattern is a starting point, not a law.

**Resource Hint:** sonnet - Pattern reference and application; implementation-level design decisions.

---

## When to Use Patterns

**Use patterns when:**
- Problem is common (many projects have this issue)
- Solution is proven (multiple implementations work well)
- Trade-offs are understood (know pros/cons)
- Context fits (pattern matches your system)

**Don't use patterns when:**
- Problem is unique (no precedent)
- Pattern seems forced (doesn't fit naturally)
- Simple solution exists (YAGNI - You Aren't Gonna Need It)
- System is too small (overkill)

---

## Architectural Patterns

### Pattern: Service-Oriented Architecture (SOA)

**Problem:** Monolithic system is too big, scales badly, hard to test.

**Solution:** Break into independent services, each handling one thing.

**Pros:**
- Independent scaling (payment service under load? Scale just that)
- Independent deployment (order service update doesn't affect payments)
- Technology flexibility (use Node for one, Python for another)
- Clear boundaries (easy to understand what each does)

**Cons:**
- Operational complexity (many services to manage)
- Network latency (services talking over network)
- Data consistency harder (each has own database)
- Debugging harder (request spans multiple services)

**When to use:**
- Team size > 10 people (each team owns a service)
- Different parts scale differently (payments need more resources)
- Different parts use different tech stacks
- System is too large for one team

**Gotchas:**
```
1. "Too fine-grained services" - 20 services, each service per endpoint
   Bad: Too much operational overhead
   Good: 3-5 services, each service per business domain

2. "Synchronous everywhere" - Service A calls B calls C
   Bad: Slow, cascading failures
   Good: Async messaging (service A publishes event, B listens)

3. "Sharing databases" - All services use same DB
   Bad: Defeats purpose (tightly coupled)
   Good: Each service owns its data
```

---

### Pattern: Event-Driven Architecture

**Problem:** Systems are tightly coupled (Order service must know about Payment service).

**Solution:** Services publish events, others listen. No direct coupling.

**Technology:**
- Event bus: RabbitMQ, Kafka, AWS SNS/SQS, Google Pub/Sub
- Event format: JSON events with type and data

**Note:** Include `version` field for event versioning (critical for schema evolution)

**Pros:**
- Loose coupling (services don't know about each other)
- Scalable (can add listeners without changing publisher)
- Resilient (if one service is slow, doesn't block others)
- Debuggable (event history is audit trail)

**Cons:**
- Harder to debug (request spans multiple services asynchronously)
- Eventual consistency (order created, payment might fail later)
- Operational complexity (need event broker)
- Ordering challenges (events might arrive out of order)

**Gotchas:**
```
1. "Event published but nobody listening"
   Bad: Event disappears, nobody processes it
   Good: Monitor for unprocessed events, alert if missing listeners

2. "Event processed twice"
   Bad: Payment processed twice, customer charged twice
   Good: Idempotent processing (processing same event twice = safe)

3. "No ordering guarantees"
   Bad: "order.created" arrives before "order.confirmed"
   Good: Listeners handle events arriving in any order
```

---

## Resilience Patterns

See `/pb-patterns-resilience` for Retry, Circuit Breaker, Rate Limiting, Cache-Aside, and Bulkhead patterns: defensive patterns for making systems reliable under failure.

---

## Data Access Patterns

### Pattern: Repository Pattern

**Problem:** Data access code scattered everywhere. Hard to test. Hard to change database.

**Solution:** Central place for data access. All queries go through repository.

**When not to use:** Simple queries can go direct; a repository per entity is boilerplate.

---

### Pattern: DTO (Data Transfer Object)

**Problem:** Return database object directly. If database schema changes, API breaks.

**Solution:** Create separate object for API responses. API only returns DTOs.

---

## API Design Patterns

See `/pb-patterns-api` for API design patterns including Pagination, Versioning, REST, GraphQL, and gRPC.

---

## Integration Patterns

### Pattern: Strangler Fig Pattern

**Problem:** Have old system, want to replace with new one. Can't rewrite everything at once.

**Solution:** New system gradually takes over. Old and new run together.

---

## When to Apply Patterns

**Pattern checklist:**
```
☐ Problem is common (not unique to this system)
☐ Pattern is proven (multiple successful implementations)
☐ Context fits (system matches pattern requirements)
☐ Trade-offs understood (know pros and cons)
☐ Simpler solution tried (patterns are last resort)
☐ Team understands (can maintain, debug, extend)
```

---

## Related Commands

- `/pb-patterns-resilience` - Resilience patterns (Retry, Circuit Breaker, Rate Limiting, Cache-Aside, Bulkhead)
- `/pb-patterns-async` - Async patterns for non-blocking operations
- `/pb-patterns-db` - Database patterns for data access
- `/pb-patterns-distributed` - Distributed patterns for multi-service coordination
- `/pb-adr` - Document pattern selection decisions
