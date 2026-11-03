---
name: "pb-patterns-resilience"
title: "Resilience & Protection Patterns"
category: "planning"
difficulty: "advanced"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-patterns-core', 'pb-patterns-distributed', 'pb-patterns-async', 'pb-hardening', 'pb-incident']
last_reviewed: "2026-11-04"
last_evolved: ""
version: "2.0.0"
version_notes: "v2.0.0: Cut from 572 to 188 lines: example code, walkthroughs and language sections removed; decisions, gotchas and when-to-use kept."
breaking_changes: ['Example code, walkthroughs and language sections removed; decisions and gotchas kept, constraints from removed code restated; deploy checklists live in /pb-preflight and /pb-deployment.']
---
# Resilience & Protection Patterns

Patterns for making systems reliable under failure. These are defensive patterns added during or after implementation to protect against transient failures, cascading outages, resource exhaustion, and abuse.

---

**Mindset:** Use `/pb-preamble` thinking (challenge assumptions - do you actually need this pattern, or is the root cause fixable?) and `/pb-design-rules` thinking (Fail noisily and early; patterns should add clarity, not hide problems).

**Resource Hint:** sonnet - Pattern reference and application; implementation-level design decisions.

---

## When to Use

- Service calls fail intermittently and you need retry/backoff logic
- External dependencies go down and you need to prevent cascading failures
- API needs protection against abuse or resource exhaustion
- Adding a caching layer for performance and reliability

---

### Pattern: Retry with Exponential Backoff

**Problem:** External service timeout. Should we fail immediately or retry?

**Solution:** Retry a few times, wait longer between each attempt.

**When to use:**
- Calling external APIs (network timeouts happen)
- Database operations (short temporary outages)
- NOT for validation errors (retrying won't help)
- NOT for authorization failures (retrying won't help)

**Gotchas:**
```
1. "Retry forever"
   Bad: Server stuck in retry loop
   Good: Max retries (usually 3-5)

2. "Retry synchronously"
   Bad: User waits 15 seconds (1+2+4+8) for result
   Good: Fail fast, queue for async retry

3. "No jitter"
   Bad: All clients retry at exact same time, thundering herd
   Good: Add random jitter (retry at 1-2 seconds, not exactly 1)
```

---

### Pattern: Circuit Breaker

**Problem:** External service is down. Calling it repeatedly wastes time, resources.

**Solution:** After N failures, stop calling for a while. Check periodically.

**When to use:**
- Calling external APIs (prevent cascading failures)
- Database connection pooling
- Any resource that might be temporarily down
- NOT for immediate failures you want to handle differently

---

### Pattern: Rate Limiting

**Problem:** API being abused. Too many requests from one client. Resources exhausted (CPU, memory, database).

**Solution:** Limit requests per time window. Too many requests? Reject or delay.

**Where to implement:**

1. **API Gateway (Best):** Rate limit before hitting services
   - All services protected
   - Single configuration point
   - Can reject early

2. **Individual Service:** Rate limit per service
   - Finer control (payment service stricter than logging)
   - Redundant (if gateway exists)

3. **Redis (Distributed):** Share limits across servers
   - Multiple API instances
   - Fair across load balancer

**When to use:**
- Public APIs (prevent abuse)
- Resource-intensive endpoints (batch processing, exports)
- Protecting against DDoS
- Fair-sharing (one user can't monopolize)
- Cost control (if calls cost money)

**Gotchas:**
```
1. "Too strict, blocks legitimate traffic"
   Bad: 1 request/minute on public API
   Good: Match expected usage (100/minute for public, 10,000 for internal)

2. "No distinction between client types"
   Bad: Free user and premium user same limit
   Good: Premium gets higher limit, free gets lower

3. "Rate limits not visible"
   Bad: Client gets 429 with no explanation
   Good: Send X-RateLimit headers + Retry-After

4. "In-memory only on single server"
   Bad: Multiple servers, each has separate limits
   Good: Use Redis for distributed counting

5. "No graceful degradation"
   Bad: Instant reject when at limit
   Good: Queue requests, process in order
```

---

### Pattern: Cache-Aside

**Problem:** Database is slow, customers wait. Same queries run repeatedly.

**Solution:** Check cache first, if miss, fetch from DB and cache it.

**Tools:**
- Redis (fast, flexible, recommended)
- Memcached (simple, fast)
- Database query cache (depends on database)

**Pros:**
- Simple to implement
- Scales well (distribute caches across servers)

**Cons:**
- Stale data (cache might be old)
- Cache invalidation (when data changes)
- Memory cost (storing data twice)

**Gotchas:**
```
1. "Cache stampede"
   Bad: Key expires, 100 requests hit DB simultaneously
   Good: Use locks (only 1 request queries DB, others wait for cache)

2. "Stale data"
   Bad: User updates profile, sees old data
   Good: Invalidate cache on write (delete from cache)

3. "Unbounded growth"
   Bad: Cache grows until server runs out of memory
   Good: Set TTL (time to live) on all cache entries
```

---

### Pattern: Bulkhead

**Problem:** One part fails, brings down whole system. (If payments service crashes, orders service affected?)

**Solution:** Isolate resources. If one part is slow, doesn't affect others.

**When to use:**
- Protecting against resource exhaustion
- Services with different loads (payment slow, orders fast)
- Critical systems that must stay available

---

## Related Commands

- `/pb-patterns-core` - Core architectural patterns (SOA, Event-Driven, Repository, DTO)
- `/pb-patterns-distributed` - Distributed patterns (Saga, CQRS, Eventual Consistency)
- `/pb-patterns-async` - Asynchronous patterns (Job Queues, Reactive Streams)
- `/pb-hardening` - Production security hardening
- `/pb-incident` - Incident response and recovery
