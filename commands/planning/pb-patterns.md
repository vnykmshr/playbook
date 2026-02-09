---
name: "pb-patterns"
title: "Architecture & Design Patterns"
category: "planning"
difficulty: "advanced"
model_hint: "opus"
execution_pattern: "reference"
related_commands: ['pb-patterns-core', 'pb-patterns-resilience', 'pb-patterns-async', 'pb-patterns-db', 'pb-patterns-distributed']
tags: ['design', 'testing', 'security', 'workflow', 'review']
last_reviewed: "2026-02-09"
last_evolved: ""
---
# Architecture & Design Patterns

Overview and navigation guide for the pattern family.

**Every pattern has trade-offs:** Use `/pb-preamble` thinking (challenge assumptions, transparent reasoning) and `/pb-design-rules` thinking (patterns should serve Clarity, Simplicity, and Modularity).

Question whether this pattern fits your constraints. Challenge the costs. Explore alternatives. Good patterns are tools you understand and choose, not dogma you follow.

**Resource Hint:** sonnet — Pattern navigation and selection; index-level reference material.

## When to Use

- Choosing which pattern family applies to your design problem
- Getting an overview of available architectural patterns before diving deep
- Navigating to the right specialized pattern command

---

## Purpose

Patterns provide:
- **Proven solutions** to recurring architectural problems
- **Shared vocabulary** for design discussions
- **Trade-off documentation** (pros, cons, gotchas)
- **Real code examples** across languages
- **Failure learning** (antipatterns from production)

---

## Pattern Family Overview

The playbook organizes patterns into specialized commands:

### 1. Core Patterns (`/pb-patterns-core`)

Foundational architectural and structural patterns.

**Topics:**
- Architectural: Service-Oriented Architecture (SOA), Event-Driven
- Data Access: Repository, DTO
- Integration: Strangler Fig
- Antipatterns: When patterns fail
- **Pattern Interactions**: How patterns work together in real systems

**When to read:**
- Designing new system architecture
- Understanding SOA/Event-Driven tradeoffs
- Choosing data access patterns (Repository, DTO)
- Real-world composition examples

**Examples:**
- E-commerce order processing (SOA + Event-Driven + Saga)
- Data layer design (Repository + DTO + Strangler Fig)
- Cross-pattern composition (see Pattern Interactions section)

---

### 2. Async Patterns (`/pb-patterns-async`)

Non-blocking execution patterns for concurrent operations.

**Topics:**
- Callbacks (when to use, callback hell)
- Promises (chaining, error handling)
- Async/Await (synchronous-looking code)
- Reactive/RxJS (complex event streams)
- Worker Threads (CPU-bound work)
- Job Queues (background processing)

**When to read:**
- Implementing concurrent/parallel operations
- Handling event streams
- Designing background job systems
- Choosing between async approaches

**Examples:**
- User input debouncing with RxJS
- CPU-intensive calculations with workers
- Email job queue with retries
- Fetching data sequentially vs in parallel

**Languages:** JavaScript, Python, Go

---

### 3. Database Patterns (`/pb-patterns-db`)

Patterns for efficient, scalable database operations.

**Topics:**
- Connection Pooling (reuse connections)
- Query Optimization (N+1, indexes, EXPLAIN)
- Replication (primary + replicas)
- Sharding (split data by key)
- Transactions (ACID across operations)
- Batch Operations (insert/update efficiency)
- Caching Strategies (write-through, write-behind)

**When to read:**
- Database is performance bottleneck
- Scaling beyond single database
- Optimizing slow queries
- Designing high-availability systems

**Examples:**
- Connection pool tuning
- Solving N+1 query problem
- Read/write splitting with replicas
- Sharding by customer_id
- Batch loading for performance

**Languages:** Python, JavaScript, SQL

---

### 4. Distributed Patterns (`/pb-patterns-distributed`)

Patterns for coordinating across services/databases.

**Topics:**
- Saga Pattern (choreography vs orchestration)
- CQRS (separate read/write models)
- Eventual Consistency (acceptance, guarantees)
- Two-Phase Commit (strong consistency)
- Pattern Interactions (combining patterns)

**When to read:**
- System spans multiple services
- Need to coordinate across boundaries
- Dealing with distributed transactions
- Balancing consistency and scalability

**Examples:**
- Payment saga (order → payment → inventory)
- Follower count with eventual consistency
- CQRS for user profiles
- When to use 2PC vs Saga

---

### 5. Resilience Patterns (`/pb-patterns-resilience`)

Patterns for making systems reliable under failure conditions.

**Topics:**
- Retry with Exponential Backoff (transient failure recovery)
- Circuit Breaker (prevent cascading failures)
- Rate Limiting (protect against abuse)
- Cache-Aside (performance + resilience)
- Bulkhead (resource isolation)

**When to read:**
- Service calls fail intermittently
- Need to protect against cascading failures
- API needs rate limiting
- Adding caching layer for reliability

**Examples:**
- Payment service retry with backoff
- Circuit breaker protecting external API calls
- Token bucket rate limiting implementation
- Cache stampede prevention with locks

---

## How to Use This Guide

### Quick Pattern Selection

**Question: I need to design something. Which pattern?**

1. **Service boundaries?** → `/pb-patterns-core` → SOA
2. **Service communication?** → `/pb-patterns-core` → Event-Driven
3. **Service failing?** → `/pb-patterns-resilience` → Circuit Breaker, Retry
4. **Rate limit API?** → `/pb-patterns-resilience` → Rate Limiting
5. **Database operations?** → `/pb-patterns-db` → Pooling, Optimization, Replication
6. **Background processing?** → `/pb-patterns-async` → Job Queues
7. **Multi-step across services?** → `/pb-patterns-distributed` → Saga
8. **Slow database?** → `/pb-patterns-db` → Connection Pooling, Indexes, Caching
9. **Complex UI events?** → `/pb-patterns-async` → Reactive/RxJS

### Common Scenarios

**Building a new microservice:**
1. Read `/pb-patterns-core` (SOA section)
2. Read `/pb-patterns-distributed` (Saga)
3. Design service boundary
4. Read `/pb-patterns-api` (API design)
5. Read `/pb-review-microservice` for review checklist

**System is slow:**
1. Measure bottleneck first (database query logs, network traces, CPU profiling)
2. Identify bottleneck (database, network, CPU?)
3. If database: Read `/pb-patterns-db`
4. If network/service communication: Read `/pb-patterns-resilience` (Circuit Breaker, Cache-Aside)
5. If CPU-intensive: Read `/pb-patterns-async` (Worker Threads)

**Payment/Order processing:**
1. Read `/pb-patterns-core` (Event-Driven)
2. Read `/pb-patterns-resilience` (Retry, Circuit Breaker)
3. Read `/pb-patterns-distributed` (Saga)
4. Read `/pb-incident` (handling Saga failures)

**Scaling to 1M users:**
1. Read `/pb-patterns-db` (Replication, Sharding)
2. Read `/pb-patterns-resilience` (Cache-Aside)
3. Read `/pb-patterns-async` (Job Queues)
4. Read `/pb-deployment` (deployment strategies)

---

## Pattern Decision Tree

```
Problem: Need to...

├─ Decouple services?
│  └─ /pb-patterns-core: Event-Driven
│
├─ Handle external service failure?
│  └─ /pb-patterns-resilience: Circuit Breaker + Retry
│
├─ Rate limit API?
│  └─ /pb-patterns-resilience: Rate Limiting
│
├─ Add caching layer?
│  └─ /pb-patterns-resilience: Cache-Aside
│
├─ Scale database reads?
│  └─ /pb-patterns-db: Replication, Connection Pooling
│
├─ Scale database writes?
│  └─ /pb-patterns-db: Sharding
│
├─ Speed up slow database?
│  └─ /pb-patterns-db: Indexes, Caching, Batch Ops
│
├─ Process many events asynchronously?
│  └─ /pb-patterns-async: Job Queues, Event Streams
│
├─ Coordinate multi-step across services?
│  └─ /pb-patterns-distributed: Saga
│
├─ Separate read/write models?
│  └─ /pb-patterns-distributed: CQRS
│
├─ Run CPU-intensive work?
│  └─ /pb-patterns-async: Worker Threads
│
└─ Accept eventual consistency?
   └─ /pb-patterns-distributed: Eventual Consistency
```

---

## Anti-Pattern: Too Many Patterns

**[NO] Bad:**
```
Using Circuit Breaker + Retry + Timeout + Bulkhead + Saga + CQRS
for a simple service (overkill, hard to maintain)
```

**[YES] Good:**
```
Start simple, add patterns only when needed
Service slow? Add cache (Cache-Aside)
Service fails? Add Circuit Breaker
Multiple services? Add Saga
```

---

## Pattern Quality Standards

All patterns in this family follow these standards:

[YES] **Real Code Examples** (not pseudocode)
- Python and JavaScript examples throughout
- Copy-paste ready
- Production tested

[YES] **Trade-offs Documented**
- Pros and cons explicit
- When to use, when not to
- Comparison with alternatives

[YES] **Gotchas Included**
- Real production failures
- Why the gotcha happens
- How to prevent it

[YES] **Antipatterns Shown**
- Bad patterns from real systems
- Lessons learned
- How to do it right

---

## Integration with Playbook

**Architectural decisions:**
- `/pb-adr` — Document why specific patterns chosen
- `/pb-guide` — System design using patterns
- `/pb-deployment` — How patterns affect deployment

**Implementation:**
- `/pb-commit` — Atomic commits for pattern implementations
- `/pb-testing` — Testing pattern implementations
- `/pb-performance` — Performance optimization using patterns

**Operations:**
- `/pb-observability` — Monitoring patterns in production
- `/pb-incident` — Handling pattern failures
- `/pb-security` — Secure pattern implementations

**Reviews:**
- `/pb-review-microservice` — Microservice design review (uses pattern knowledge)

---

## Quick Reference

| Pattern | Command | Use When | Avoid When |
|---------|---------|----------|-----------|
| **SOA** | `/pb-patterns-core` | Services need independence | Single team project |
| **Event-Driven** | `/pb-patterns-core` | Loose coupling needed | Strict ordering required |
| **Repository** | `/pb-patterns-core` | Complex data access | Simple CRUD |
| **Retry** | `/pb-patterns-resilience` | Transient failures possible | Permanent failure (auth) |
| **Circuit Breaker** | `/pb-patterns-resilience` | Service might be down | One-time operations |
| **Rate Limiting** | `/pb-patterns-resilience` | API abuse protection | Internal-only services |
| **Cache-Aside** | `/pb-patterns-resilience` | High read load | Strict consistency |
| **Bulkhead** | `/pb-patterns-resilience` | Different load per service | Single service |
| **Saga** | `/pb-patterns-distributed` | Multi-step across services | Single service transaction |
| **CQRS** | `/pb-patterns-distributed` | Different read/write patterns | Simple CRUD |
| **Eventual Consistency** | `/pb-patterns-distributed` | Consistency delay acceptable | Strong consistency required |

---

## Related Commands

- `/pb-patterns-core` — Core architectural and structural patterns (SOA, Event-Driven, Repository, DTO)
- `/pb-patterns-resilience` — Resilience patterns (Retry, Circuit Breaker, Rate Limiting, Cache-Aside, Bulkhead)
- `/pb-patterns-async` — Asynchronous patterns
- `/pb-patterns-db` — Database patterns
- `/pb-patterns-distributed` — Distributed systems patterns
- `/pb-patterns-frontend` — Frontend architecture patterns (components, state, theming)
- `/pb-patterns-api` — API design patterns (REST, GraphQL, gRPC)
- `/pb-patterns-deployment` — Deployment strategies and patterns
- `/pb-patterns-cloud` — Cloud deployment patterns (AWS, GCP, Azure)

---

*Created: 2026-01-11 | Category: Architecture | Tier: L*

