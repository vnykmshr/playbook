---
name: "pb-patterns-async"
title: "Asynchronous Patterns"
category: "planning"
difficulty: "advanced"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-patterns-core', 'pb-patterns-resilience', 'pb-patterns-distributed', 'pb-observability']
last_reviewed: "2026-11-04"
last_evolved: ""
version: "2.0.0"
version_notes: "v2.0.0: Cut from 715 to 222 lines: example code, walkthroughs and language sections removed; decisions, gotchas and when-to-use kept."
breaking_changes: ['Example code, walkthroughs and language sections removed; decisions and gotchas kept, constraints from removed code restated; deploy checklists live in /pb-preflight and /pb-deployment.']
---
# Asynchronous Patterns

Non-blocking execution patterns for concurrent operations. Essential for scalable systems.

**Trade-offs exist:** Async patterns add complexity. Use `/pb-preamble` thinking (challenge assumptions) and `/pb-design-rules` thinking (especially Simplicity: do you need this complexity?).

Question whether async is necessary. Challenge the complexity cost. Understand the actual constraints before choosing.

**Resource Hint:** sonnet - Async pattern reference; implementation-level concurrency decisions.

---

## When to Use Async

**Use async when:**
- I/O operations (network, database, file system)
- Operations take unpredictable time
- System needs to handle many concurrent requests
- Want to avoid blocking the event loop / main thread

**Don't use async when:**
- Operation completes instantly
- System is single-threaded and simple
- Complexity outweighs benefits
- CPU-bound work (use parallel processing instead)

---

## Callback Pattern

**Problem:** Need to execute code after an async operation completes.

**Solution:** Pass a function to be called when done.

**Pros:**
- Simple concept
- No special syntax needed
- Works in all JavaScript environments

**Cons:**
- Error handling repetitive
- Callback hell (deeply nested)
- Hard to sequence operations
- Hard to parallelize operations

**When to use:**
- Simple one-off async operations
- Event handlers
- Generally avoid in favor of Promises/async-await

---

## Promise Pattern

**Problem:** Callbacks get messy with multiple async operations.

**Solution:** Promise object represents future value, can be chained.

**Gotchas:**
```
1. "Unhandled rejection"
   Bad: Promise error not caught, silent failure
   Good: Always add .catch() or use async/await with try/catch

2. "Swallowed errors"
   Bad: Returning promise in .then() but not awaiting
   Good: Ensure error flows through chain

3. "Parallel instead of sequential"
   Bad: .then(op1).then(op2) if op2 doesn't need op1 result
   Good: Use Promise.all() for independent operations
```

**Pros:**
- Cleaner than callbacks
- Easy to chain operations
- Easy to parallelize with Promise.all()
- Standardized error handling

**Cons:**
- Still somewhat verbose
- Easy to get wrong (unhandled rejections)
- Hard to debug (.then() chains)

**When to use:**
- Multiple async operations to sequence
- Parallel operations with Promise.all()
- Legacy code (before async/await available)

---

## Async/Await Pattern

**Problem:** Promises still verbose and hard to read. Want synchronous-looking code.

**Solution:** async/await keywords make promises look like synchronous code.

**Gotchas:**
```
1. "Sequential instead of parallel"
   Bad: result = await op1(); await op2(); (2 seconds if each 1 second)
   Good: result = await Promise.all([op1(), op2()]); (1 second)

2. "Forgetting async"
   Bad: function processOrder() { ... await fetchOrder(...) }
   Good: async function processOrder() { ... await fetchOrder(...) }

3. "No timeout"
   Bad: await operation() // hangs forever if operation hangs
   Good: await Promise.race([operation(), timeout(5000)])
```

**Pros:**
- Reads like synchronous code
- Easy to understand flow
- Standard try/catch error handling
- Easy to parallelize with Promise.all()

**Cons:**
- Can accidentally serialize operations (using await sequentially)
- No built-in timeout mechanism
- Can hide performance issues

**When to use:**
- Most modern async code
- Cleaner than callbacks/promises
- When code structure matches sequential thinking

---

## Reactive/Observable Pattern

**Problem:** Complex event streams (multiple events, transformations, filtering).

**Solution:** Treat events as streams, apply functional transformations.

**Pros:**
- Powerful for complex event flows
- Functional transformations (map, filter, etc.)
- Built-in operators (debounce, throttle, etc.)

**Cons:**
- Steep learning curve
- Can be overkill for simple cases
- Error handling can be tricky
- Debugging observable chains difficult

**When to use:**
- Complex event streams (user input, WebSocket messages)
- Multiple transformations needed
- Avoid for simple fetch operations

---

## Worker Threads / Processes

**Problem:** CPU-bound work blocks event loop / main thread.

**Solution:** Offload work to separate thread or process.

**Pros:**
- Parallel execution on multiple cores
- Event loop doesn't block
- True parallelism (not just concurrency)

**Cons:**
- Communication overhead (passing data)
- Can't share memory directly
- More resource intensive

**When to use:**
- CPU-intensive work (calculations, image processing)
- Long-running tasks
- Not for I/O operations (use async instead)

---

## Job Queue Pattern

**Problem:** Many tasks, can't process all simultaneously. Need background processing.

**Solution:** Queue tasks, process with limited workers.

**Pros:**
- Handles burst loads (queue absorbs spikes)
- Automatic retries
- Can scale workers independently
- Decouples producer from consumer

**Cons:**
- Requires external service (Redis, RabbitMQ)
- More operational complexity
- Eventual consistency (task might not execute immediately)

**When to use:**
- Background tasks (emails, notifications)
- Rate limiting (only N tasks at a time)
- Deferred processing (process later, not now)
- Retryable operations

---

## Related Commands

- `/pb-patterns-core` - Foundation patterns (SOA, Event-Driven, Repository)
- `/pb-patterns-resilience` - Resilience patterns (Retry, Circuit Breaker, Cache-Aside)
- `/pb-patterns-distributed` - Distributed patterns that build on async
- `/pb-observability` - Monitor and trace async operations
