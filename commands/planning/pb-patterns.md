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

Foundational architectural and design patterns.

**Topics:**
- Architectural: Service-Oriented Architecture (SOA), Event-Driven
- Design: Retry, Circuit Breaker, Cache-Aside, Bulkhead
- Data Access: Repository, DTO
- API: Pagination, Versioning
- Integration: Strangler Fig
- Antipatterns: When patterns fail
- **Pattern Interactions**: How patterns work together in real systems

**When to read:**
- Designing new system architecture
- Understanding SOA/Event-Driven tradeoffs
- Learning when Circuit Breaker meets Retry
- Real-world composition examples

**Examples:**
- E-commerce order processing (SOA + Event-Driven)
- Service communication (Circuit Breaker + Retry)
- Cache handling (Cache-Aside + Bulkhead)

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

## How to Use This Guide

### Quick Pattern Selection

**Question: I need to design something. Which pattern?**

1. **Service boundaries?** → `/pb-patterns-core` → SOA
2. **Service communication?** → `/pb-patterns-core` → Event-Driven, Retry, Circuit Breaker
3. **Database operations?** → `/pb-patterns-db` → Pooling, Optimization, Replication
4. **Background processing?** → `/pb-patterns-async` → Job Queues
5. **Multi-step across services?** → `/pb-patterns-distributed` → Saga
6. **Slow database?** → `/pb-patterns-db` → Connection Pooling, Indexes, Caching
7. **Complex UI events?** → `/pb-patterns-async` → Reactive/RxJS

### Common Scenarios

**Building a new microservice:**
1. Read `/pb-patterns-core` (SOA section)
2. Read `/pb-patterns-distributed` (Saga)
3. Design service boundary
4. Read `/pb-patterns-core` (API section)
5. Read `/pb-review-microservice` for review checklist

**System is slow:**
1. Measure bottleneck first (database query logs, network traces, CPU profiling)
2. Identify bottleneck (database, network, CPU?)
3. If database: Read `/pb-patterns-db`
4. If network/service communication: Read `/pb-patterns-core` (Circuit Breaker, Cache-Aside)
5. If CPU-intensive: Read `/pb-patterns-async` (Worker Threads)

**Payment/Order processing:**
1. Read `/pb-patterns-core` (Event-Driven)
2. Read `/pb-patterns-distributed` (Saga)
3. Read `/pb-incident` (handling Saga failures)

**Scaling to 1M users:**
1. Read `/pb-patterns-db` (Replication, Sharding)
2. Read `/pb-patterns-core` (Caching)
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
│  └─ /pb-patterns-core: Circuit Breaker + Retry
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

| Pattern | Category | Use When | Avoid When |
|---------|----------|----------|-----------|
| **SOA** | Architecture | Services need independence | Single team project |
| **Event-Driven** | Architecture | Loose coupling needed | Strict ordering required |
| **Retry** | Resilience | Transient failures possible | Permanent failure (auth) |
| **Circuit Breaker** | Resilience | Service might be down | One-time operations |
| **Cache-Aside** | Performance | High read load | Strict consistency |
| **Bulkhead** | Resilience | Different load per service | Single service |
| **Saga** | Distributed | Multi-step across services | Single service transaction |
| **CQRS** | Data | Different read/write patterns | Simple CRUD |
| **Eventual Consistency** | Consistency | Consistency delay acceptable | Strong consistency required |
| **2PC** | Consistency | Must have all-or-nothing | Poor availability acceptable |

---

## Related Commands

- `/pb-patterns-core` — Core architectural and design patterns
- `/pb-patterns-async` — Asynchronous patterns
- `/pb-patterns-db` — Database patterns
- `/pb-patterns-distributed` — Distributed systems patterns
- `/pb-patterns-frontend` — Frontend architecture patterns (components, state, theming)
- `/pb-patterns-api` — API design patterns (REST, GraphQL, gRPC)
- `/pb-patterns-deployment` — Deployment strategies and patterns
- `/pb-patterns-cloud` — Cloud deployment patterns (AWS, GCP, Azure)

---

*Created: 2026-01-11 | Category: Architecture | Tier: L*

