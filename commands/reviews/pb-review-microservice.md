---
name: "pb-review-microservice"
title: "Microservice Architecture Review"
category: "reviews"
difficulty: "advanced"
model_hint: "opus"
execution_pattern: "sequential"
related_commands: ['pb-patterns-core', 'pb-patterns-resilience', 'pb-patterns-distributed', 'pb-observability', 'pb-incident']
last_reviewed: "2026-11-05"
version: "1.2.0"
version_notes: "v1.2.0: Example code cut; each section keeps its question and checklist, and the common issues and review template stay."
breaking_changes: []
---
# Microservice Architecture Review

Framework for reviewing microservice design, implementation, and operations.

**Mindset:** Microservice reviews embody `/pb-preamble` thinking (question service boundaries) and `/pb-design-rules` thinking (especially Modularity and Separation: are services correctly decoupled?).

Question whether the service boundary is correct. Challenge the coupling assumptions. Surface design flaws before they become operational problems.

**Resource Hint:** opus - microservice review requires deep analysis of boundaries, coupling, data ownership, and operational concerns

---

## When to Use

- Evaluating a new service before it goes to production
- Periodic architecture review of existing microservices
- After splitting a monolith or extracting a new service
- When inter-service communication issues arise

---

## Purpose

Microservice reviews ensure:
- **Clear boundaries** - Service owns specific business domain
- **Loose coupling** - Services don't depend on each other's internals
- **Scalability** - Service can scale independently
- **Resilience** - Service failures don't cascade
- **Observability** - Can debug issues across services
- **Deployability** - Can deploy independently

---

## Review Checklist

### 1. Service Boundaries

**Question: Is this the right scope for a service?**

**Bad Service Boundaries:**
- Service per function (getUser, createUser, deleteUser = 3 services)
- Service per tier (frontend, backend, database services)
- Service per database table
- Shared database between services

**Good Service Boundaries:**
- Service per business domain (User Service, Order Service, Payment Service)
- Service owns its data (no shared database)
- Service encapsulates related functionality
- Service is independently deployable

**Checklist:**
```
☐ Service boundary aligns with business domain
☐ Service has clear responsibility
☐ Service owns its data (no shared database)
☐ Service can be deployed independently
☐ Service makes sense to teams (not fragmented across 10 teams)
☐ Not too big (>3 teams can't understand it)
☐ Not too small (<1 person can't maintain it)
```

---

### 2. API Contract & Versioning

**Question: Is the service API stable and well-defined?**

**API Checklist:**
```
☐ API endpoints documented with examples
☐ Request/response formats defined (JSON schema)
☐ Authentication mechanism documented
☐ Error responses documented (what can fail?)
☐ Rate limiting defined (requests/sec)
☐ Timeout values defined
☐ Retry policy defined
☐ API versioning strategy (v1, v2, etc.)
☐ Deprecation timeline documented
```

**API Versioning Strategy:**

```
Option 1: URL Versioning (Simple)
GET /v1/users/123
GET /v2/users/123

Option 2: Header Versioning (Clean)
GET /users/123
Header: API-Version: 2

Option 3: Content Negotiation
GET /users/123
Header: Accept: application/vnd.myapp.v2+json

Recommend: URL versioning (simple, clear)
Deprecation: Support v1 for 6 months, then remove
```

---

### 3. Data Management

**Question: How does service manage data?**

**Checklist:**
```
☐ Service owns its data (no shared database)
☐ Data migrations documented
☐ Backup strategy defined
☐ Data retention policy defined
☐ Database indexes optimized (EXPLAIN ANALYZE run)
☐ Connection pooling configured
☐ Read replicas set up (if needed)
```

---

### 4. Service Communication

**Question: How do services talk to each other?**

**Checklist:**
```
☐ Communication pattern documented (sync vs async)
☐ Service discovery mechanism (DNS, Consul, etc.)
☐ Resilience patterns (Circuit Breaker, Retry)
☐ Timeout values set
☐ Error handling defined
☐ Cascading failure prevention (bulkheads)
```

---

### 5. Health & Observability

**Question: Can we monitor and debug the service?**

**Health Checks:**

```
Checklist:
☐ Health check endpoint (GET /health)
☐ Readiness probe (can handle requests?)
☐ Liveness probe (is service alive?)
☐ Dependency health (can reach database? Other services?)
```

**Observability Checklist:**

```
☐ Structured logging (JSON with correlation ID)
☐ Metrics exported (Prometheus, StatsD)
☐ Distributed tracing configured (Jaeger, Zipkin)
☐ Alerts defined (high error rate, latency, etc.)
☐ SLI/SLO defined (what's success?)
```

---

### 6. Deployment & Operations

**Question: Can we deploy and operate this service independently?**

**Checklist:**
```
☐ Service can be deployed without deploying others
☐ Backward compatibility maintained (old and new versions work)
☐ Database migrations handled gracefully
☐ Canary deployment tested
☐ Rollback procedure documented
☐ Monitoring/alerting in place before deployment
```

---

### 7. Testing

**Question: Is the service tested thoroughly?**

**Checklist:**
```
☐ Unit tests cover critical paths
☐ Integration tests with real database
☐ Contract tests with other services
☐ Load tests show performance baseline
☐ Chaos testing (what if service X is slow?)
☐ Error scenarios tested
```

---

## Common Microservice Issues

### Issue 1: Shared Database

**Problem:**
```
User Service → Shared Database ← Order Service
              (tight coupling)
```

**Why Bad:**
- User Service can't change schema without coordinating
- Order Service depends on User database being up
- Scaling difficult (can't scale User db independently)

**Fix:**
```
User Service → User Database
Order Service → Order Database

Services communicate via API (loose coupling)
```

### Issue 2: Cascading Failures

**Problem:**
```
Request → Service A → Service B (down) → Timeout → Request hangs
(Service B down affects Service A)
```

**Why Bad:**
- One service down cascades to all upstream services
- Whole system becomes slow/unavailable

**Fix:**
```
Request → Service A
          (with Circuit Breaker, Retry, Timeout)
          → Service B

If Service B down:
- Circuit breaker opens
- Service A fails fast (doesn't hang)
- System stays responsive
```

### Issue 3: Data Consistency

**Problem:**
```
Order created in Order Service
Payment processed in Payment Service
(Events arrive out of order, data inconsistent)
```

**Why Bad:**
- Payment might be processed before order exists
- Orphaned payments, invalid orders

**Fix:**
```
Use Saga pattern:
1. Order Service receives order
2. Publishes "order.created" event
3. Payment Service listens, validates order exists
4. Publishes "payment.processed" or "payment.failed"
5. If failed, Order Service compensates (cancels order)
```

---

## Review Template

**Use this template to review a microservice:**

```markdown
# Review: [Service Name]

## Service Boundaries
- [ ] Domain clearly defined
- [ ] Owns its data
- [ ] Independently deployable

## API Contract
- [ ] Endpoints documented
- [ ] Response formats defined
- [ ] Error handling defined
- [ ] Versioning strategy defined

## Data Management
- [ ] Own database (no shared)
- [ ] Migrations handled
- [ ] Indexes optimized
- [ ] Connection pooling configured

## Communication
- [ ] Pattern documented (sync/async)
- [ ] Resilience patterns implemented
- [ ] Timeouts configured
- [ ] Error handling defined

## Health & Observability
- [ ] Health checks implemented
- [ ] Logging configured (JSON, correlation IDs)
- [ ] Metrics exported
- [ ] Tracing configured
- [ ] Alerts defined

## Deployment
- [ ] Independent deployment tested
- [ ] Backward compatibility maintained
- [ ] Canary deployment documented
- [ ] Rollback procedure documented

## Testing
- [ ] Unit tests adequate
- [ ] Integration tests in place
- [ ] Contract tests with dependencies
- [ ] Load tests performed
- [ ] Error scenarios tested

## Issues Found
1. [Issue]: [Description] [Severity: P1/P2/P3]
2. ...

## Recommendations
1. [Recommendation]
2. ...

## Sign-off
Reviewed by: [Name]
Date: [Date]
Status: APPROVED / APPROVED WITH CONDITIONS / REJECTED
```

---

## Comment Register

Findings posted as PR/issue comments follow `~/.claude/CLAUDE.md` § GitHub Artifact Register: one load-bearing observation per comment, one sentence per finding, no narration or severity adjectives.

---

## Related Commands

- `/pb-patterns-core` - SOA and Event-Driven architecture
- `/pb-patterns-resilience` - Resilience patterns (Circuit Breaker, Retry, Rate Limiting)
- `/pb-patterns-distributed` - Saga, CQRS patterns
- `/pb-observability` - Health checks, monitoring
- `/pb-incident` - Handling microservice failures
