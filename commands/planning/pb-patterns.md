---
name: "pb-patterns"
title: "Architecture & Design Patterns"
category: "planning"
difficulty: "advanced"
model_hint: "sonnet"
execution_pattern: "reference"
related_commands: ['pb-patterns-core', 'pb-patterns-resilience', 'pb-patterns-async', 'pb-patterns-db', 'pb-patterns-distributed']
last_reviewed: "2026-11-04"
last_evolved: "2026-02-18"
version: "2.0.0"
version_notes: "v2.0.0: Cut from 388 to 99 lines: example code, walkthroughs and language sections removed; decisions, gotchas and when-to-use kept. The selection tree and Related list name every pattern family, pinned by a test; scaling points at /pb-patterns-deployment."
breaking_changes: ['Example code, walkthroughs and language sections removed; decisions and gotchas kept, constraints from removed code restated; deploy checklists live in /pb-preflight and /pb-deployment.']
---
# Architecture & Design Patterns

Overview and navigation guide for the pattern family.

**Every pattern has trade-offs:** Use `/pb-preamble` thinking (challenge assumptions, transparent reasoning) and `/pb-design-rules` thinking (patterns should serve Clarity, Simplicity, and Modularity).

Question whether this pattern fits your constraints. Challenge the costs. Explore alternatives. Good patterns are tools you understand and choose, not dogma you follow.

**Resource Hint:** sonnet - Pattern navigation and selection; index-level reference material.

## When to Use

- Choosing which pattern family applies to your design problem
- Getting an overview of available architectural patterns before diving deep
- Navigating to the right specialized pattern command

---

## Pattern Selection Workflow

```
DESIGN PROBLEM
│
├─ Service boundaries?     → /pb-patterns-core (SOA)
├─ Service communication?  → /pb-patterns-core (Event-Driven)
├─ API design?             → /pb-patterns-api (REST, GraphQL, gRPC)
├─ Service failing?        → /pb-patterns-resilience (Circuit Breaker)
├─ Rate limit API?         → /pb-patterns-resilience (Rate Limiting)
├─ Database operations?    → /pb-patterns-db (Pooling, Optimization)
├─ Background processing?  → /pb-patterns-async (Job Queues)
├─ Multi-step across services? → /pb-patterns-distributed (Saga)
├─ Slow database?          → /pb-patterns-db (Caching)
├─ Complex UI events?      → /pb-patterns-async (Reactive/RxJS)
├─ Deployment strategy?    → /pb-patterns-deployment
├─ Frontend architecture?  → /pb-patterns-frontend
├─ Cloud infrastructure?   → /pb-patterns-cloud
└─ Security concerns?      → /pb-patterns-security

THEN: Read pattern family, understand trade-offs, implement with knowledge
```

---

## How to Use This Guide

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
4. Read `/pb-patterns-deployment` (deployment strategies)

---

## Related Commands

- `/pb-patterns-core` - Core architectural and structural patterns (SOA, Event-Driven, Repository, DTO)
- `/pb-patterns-resilience` - Resilience patterns (Retry, Circuit Breaker, Rate Limiting, Cache-Aside, Bulkhead)
- `/pb-patterns-async` - Asynchronous patterns
- `/pb-patterns-db` - Database patterns
- `/pb-patterns-distributed` - Distributed systems patterns
- `/pb-patterns-frontend` - Frontend architecture patterns (components, state, theming)
- `/pb-patterns-api` - API design patterns (REST, GraphQL, gRPC)
- `/pb-patterns-deployment` - Deployment strategies and patterns
- `/pb-patterns-cloud` - Cloud deployment patterns (AWS, GCP, Azure)
- `/pb-patterns-security` - Security patterns (authn, authz, secrets, data protection)
