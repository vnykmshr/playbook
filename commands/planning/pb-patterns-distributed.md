---
name: "pb-patterns-distributed"
title: "Distributed Patterns"
category: "planning"
difficulty: "advanced"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-patterns-core', 'pb-patterns-async', 'pb-patterns-security', 'pb-observability']
last_reviewed: "2026-11-04"
last_evolved: ""
version: "2.0.0"
version_notes: "v2.0.0: Cut from 1136 to 242 lines: example code, walkthroughs and language sections removed; decisions, gotchas and when-to-use kept. Saga idempotency dedupes on a request ID in the effect's transaction; the outbox writes in the state change's transaction and consumers dedupe by event ID; 2PC never rolls back after a participant commits; sagas stay short."
breaking_changes: ['Example code, walkthroughs and language sections removed; decisions and gotchas kept, constraints from removed code restated; deploy checklists live in /pb-preflight and /pb-deployment.']
---
# Distributed Patterns

Patterns for coordinating operations across multiple services/databases.

**Caveat:** Distributed patterns add significant complexity. Use `/pb-preamble` thinking (challenge assumptions) and `/pb-design-rules` thinking (especially Simplicity and Resilience: can you achieve your goals with simpler approaches?).

Question whether you truly need distributed systems. Challenge the assumption that you can't keep things simple. Understand the real constraints before choosing.

**Resource Hint:** sonnet - Distributed pattern reference; implementation-level coordination decisions.

---

## When to Use Distributed Patterns

**Use when:**
- System spans multiple services/databases
- Operations must coordinate across boundaries
- Consistency matters but flexibility needed
- Need visibility into distributed transactions

**Don't use when:**
- Single database sufficient
- Operations are local
- Simple solutions available
- System complexity not justified

---

## Saga Pattern

**Problem:** Multi-step transaction spans multiple services. Standard ACID transaction won't work.

**Solution:** Choreograph steps, with compensating actions for rollback.

### 1. Choreography (Event-Based)

Services listen for events and trigger next step.

**Pros:**
- Loose coupling (services don't know about each other)
- Scalable (add new steps without changing others)
- Decentralized (no orchestrator)

**Cons:**
- Hard to track state (which step are we in?)
- Hard to debug (events scattered across services)
- Difficult to add timeouts/retries

### 2. Orchestration (Centralized)

One service orchestrates the saga steps.

**Pros:**
- Easy to track state (one place)
- Easy to debug (centralized logic)
- Easy to add timeouts/retries

**Cons:**
- Tight coupling (orchestrator knows all services)
- Single point of failure (orchestrator goes down)
- Orchestrator becomes bottleneck

**Gotchas:**
```
1. "Idempotency"
   Bad: If step retries, might charge payment twice
   Good: Make operations idempotent (same operation twice = safe)

2. "Timeout"
   Bad: Payment charged but timeout before marking complete
   Good: Set timeouts, have compensating action for timeout

3. "Cascading failures"
   Bad: One service down brings whole saga down
   Good: Timeouts and fallbacks

4. "Long sagas"
   Bad: Ten steps, each a failure point with its own compensation
   Good: Keep a saga to a few steps; split a long one at a business boundary so each part is tested alone
```

### Saga Idempotency Pattern

**Problem:** Saga step retries. Payment charged twice. Inventory decremented twice.

**Solution:** Ensure each step is idempotent. Running same operation twice = running it once.

Dedupe on a caller-supplied request ID, recorded in the same transaction as the effect. A lookup-then-write outside that transaction races, and `count = count - 10` is not idempotent without the ID guard.

**When to implement:**
- All saga steps (payment, inventory, shipping)
- Any operation that might retry
- Multi-step workflows

---

## Event Versioning

**Problem:** Event format changes. Old events become unreadable. New services can't handle old events.

**Solution:** Version events. Support multiple versions simultaneously.

**Migration strategy:**
```
Phase 1: Add version field to events
  Existing events: version = 1
  New events: version = 2

Phase 2: Support both versions in consumers
  Consumers handle v1 and v2

Phase 3: Migrate old events
  Background job upgrades v1 → v2

Phase 4: Remove v1 support
  Only v2+ consumers exist
```

---

## Outbox Pattern

**Problem:** Publishing event fails after database commit. Event lost. Inconsistency.

**Solution:** Insert the event into an outbox table in the same transaction as the state change; a relay publishes it after commit.

**Gotchas:**
```
1. "Polling lag"
   Bad: Polling every 10 seconds, events delayed
   Good: Poll every 1-5 seconds, or use change data capture

2. "Outbox grows unbounded"
   Bad: Published events never deleted
   Good: Archive/delete old published events after 1-2 weeks

3. "Duplicate publishing"
   Bad: Network hiccup, publish twice
   Good: Consumers dedupe by event ID; the relay is at-least-once
```

---

## CQRS (Command Query Responsibility Segregation)

**Problem:** Same data model used for reads and writes. Causes complexity and inconsistency.

**Solution:** Separate models - one for writes, one for reads.

**Pros:**
- Optimize reads and writes separately
- Read model can be denormalized (fast reads)
- Event sourcing enables audit trail
- Scale reads and writes independently

**Cons:**
- Eventual consistency (read model behind write model)
- Complex to implement
- More storage (storing events + read model)
- Hard to delete data (audit trail preserved)

**Gotchas:**
```
1. "Eventual consistency"
   Bad: Write data, read immediately sees old data
   Good: Accept slight delay, or read from write model

2. "Event versioning"
   Bad: Change event format, old events can't be read
   Good: Version events, have migration logic

3. "Read model rebuild"
   Bad: Read model corrupted, no way to recover
   Good: Rebuild from event stream (events are source of truth)
```

---

## Eventual Consistency

**Problem:** Can't always have strong consistency across services. Too slow, too complex.

**Solution:** Accept eventual consistency. Data will be consistent eventually.

**Trade-offs:**
- Users see temporary inconsistency
- Complex to reason about
- Requires compensating actions for errors

---

## Two-Phase Commit (2PC)

**Problem:** Transaction spans multiple databases. Need all-or-nothing.

**Solution:** Coordinator asks all parties to prepare, then commit/rollback.

**Pros:**
- Strong consistency (all-or-nothing)
- ACID guarantees across services

**Cons:**
- Slow (two round-trips)
- Blocking (locks held during prepare phase)
- Coordinator failure means stuck transaction
- Poor availability (one service down fails whole transaction)

**Gotchas:**
```
1. "Heuristic completion"
   Problem: Coordinator crashes after services prepare but before commit
   Services locked, manual intervention needed

2. "Timeout"
   Bad: Service takes too long to prepare, whole transaction blocks
   Good: Timeouts, fallback to eventual consistency

3. "Deadlock"
   Bad: Multiple concurrent transactions, resources locked in different order
   Good: Consistent lock ordering, or use MVCC

4. "Rollback after commit"
   Bad: A participant fails during commit, so the coordinator rolls the rest back
   Good: Once the coordinator logs commit, it drives every participant to commit, retrying; it never rolls back after any participant has committed
```

**When to use:**
- Strong consistency critical (financial transactions)
- Prefer Saga for loosely coupled services

---

## Related Commands

- `/pb-patterns-core` - Foundation patterns (SOA, Event-Driven)
- `/pb-patterns-async` - Async patterns needed for distributed operations
- `/pb-patterns-security` - Security patterns for microservice architectures
- `/pb-observability` - Tracing and monitoring distributed systems
