# Asynchronous Patterns

Non-blocking execution patterns for concurrent operations. Essential for scalable systems.

**Trade-offs exist:** Async patterns add complexity. Use `/pb-preamble` thinking (challenge assumptions) and `/pb-design-rules` thinking (especially Simplicity—do you need this complexity?).

Question whether async is necessary. Challenge the complexity cost. Understand the actual constraints before choosing.

---

## Purpose

Async patterns:
- **Improve responsiveness** - Non-blocking operations don't freeze the application
- **Scale concurrency** - Handle thousands of operations with few threads
- **Prevent deadlocks** - Avoid blocking on I/O, allowing other work to proceed
- **Enable parallelism** - Leverage multi-core processors effectively
- **Improve user experience** - Applications stay responsive under load

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

**JavaScript Example:**
```javascript
function fetchUser(userId, callback) {
  fetch(`/api/users/${userId}`)
    .then(response => response.json())
    .then(user => callback(null, user))
    .catch(error => callback(error));
}

// Usage
fetchUser(123, (error, user) => {
  if (error) {
    console.error('Failed to fetch user:', error);
  } else {
    console.log('User:', user);
  }
});
```

**Python:** Use `threading.Thread` with callback function, or prefer `asyncio` for modern async.

**Callback Hell (Anti-pattern):**
```javascript
// [NO] Nested callbacks - hard to read and maintain
fetchUser(123, (error, user) => {
  if (error) {
    handleError(error);
  } else {
    fetchOrders(user.id, (error, orders) => {
      if (error) {
        handleError(error);
      } else {
        fetchPayments(orders[0].id, (error, payments) => {
          if (error) {
            handleError(error);
          } else {
            console.log('All data:', user, orders, payments);
          }
        });
      }
    });
  }
});

// [YES] Better: Use Promises or async/await instead
```

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

**JavaScript Example:**
```javascript
function fetchUser(userId) {
  return fetch(`/api/users/${userId}`)
    .then(response => response.json());
}

// Chain operations
fetchUser(123)
  .then(user => {
    console.log('User:', user);
    return fetchOrders(user.id);  // Chain next promise
  })
  .then(orders => {
    console.log('Orders:', orders);
    return fetchPayments(orders[0].id);  // Chain next promise
  })
  .then(payments => {
    console.log('Payments:', payments);
  })
  .catch(error => {
    // Single error handler for all
    console.error('Failed:', error);
  });
```

**Parallel Operations with Promise.all:**
```javascript
// Run multiple operations in parallel
Promise.all([
  fetchUser(123),
  fetchOrders(123),
  fetchPayments(123)
])
  .then(([user, orders, payments]) => {
    console.log('All data:', user, orders, payments);
  })
  .catch(error => {
    console.error('One of the operations failed:', error);
  });
```

**Promise.race (first to complete):**
```javascript
// Use whichever completes first
const fast = Promise.race([
  fetchFromServer1(),
  fetchFromServer2(),
  fetchFromServer3()
]);
```

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

**JavaScript Example:**
```javascript
async function processOrder(orderId) {
  try {
    // Fetch data sequentially
    const order = await fetchOrder(orderId);
    const customer = await fetchCustomer(order.customerId);
    const payment = await processPayment(order.total);

    console.log('Order:', order);
    console.log('Customer:', customer);
    console.log('Payment:', payment);

    return { order, customer, payment };
  } catch (error) {
    console.error('Failed to process order:', error);
    throw error;
  }
}

// Usage
processOrder(123).then(result => {
  console.log('Success:', result);
});
```

**Python:** Use `asyncio` with `async def` / `await` syntax. Run with `asyncio.run(coro())`.

**Parallel Operations with async/await:**
```javascript
async function processOrder(orderId) {
  try {
    const order = await fetchOrder(orderId);

    // Run in parallel (not sequential)
    const [customer, payment] = await Promise.all([
      fetchCustomer(order.customerId),
      processPayment(order.total)
    ]);

    return { order, customer, payment };
  } catch (error) {
    console.error('Failed:', error);
    throw error;
  }
}
```

**Python Parallel:** Use `asyncio.gather(coro1(), coro2())` for concurrent execution.

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

**JavaScript/RxJS Example:**
```javascript
import { from, interval } from 'rxjs';
import { map, filter, take } from 'rxjs/operators';

// Stream of events
const numbers = interval(1000);  // Emit 0, 1, 2, 3... every second

numbers
  .pipe(
    take(5),              // Only first 5
    filter(n => n % 2 === 0),  // Only even
    map(n => n * 2)       // Multiply by 2
  )
  .subscribe(
    value => console.log('Value:', value),      // Next
    error => console.error('Error:', error),    // Error
    () => console.log('Complete')               // Complete
  );

// Output:
// Value: 0
// Value: 4
// Value: 8
// Complete
```

**Real-World Example: User Input Stream**
```javascript
import { fromEvent } from 'rxjs';
import { debounceTime, map, distinctUntilChanged } from 'rxjs/operators';

// Convert input element to stream
const searchInput = document.getElementById('search');
const searchStream = fromEvent(searchInput, 'input');

searchStream
  .pipe(
    map(event => event.target.value),           // Extract value
    debounceTime(300),                          // Wait 300ms after last char
    distinctUntilChanged(),                     // Only if value changed
    map(query => fetchSearchResults(query))     // Fetch results
  )
  .subscribe(
    results => displayResults(results),
    error => console.error('Search failed:', error)
  );
```

**Python:** Use `aiostream` library for reactive streams, or `async for` with async generators.

**Pros:**
- Powerful for complex event flows
- Functional transformations (map, filter, etc.)
- Built-in operators (debounce, throttle, etc.)
- Handles backpressure automatically

**Cons:**
- Steep learning curve
- Can be overkill for simple cases
- Error handling can be tricky
- Debugging observable chains difficult

**When to use:**
- Complex event streams (user input, WebSocket messages)
- Multiple transformations needed
- Backpressure handling needed
- Avoid for simple fetch operations

---

## Worker Threads / Processes

**Problem:** CPU-bound work blocks event loop / main thread.

**Solution:** Offload work to separate thread or process.

**JavaScript Worker Thread Example:**
```javascript
// main.js
const { Worker } = require('worker_threads');

const worker = new Worker('./worker.js');

// Send data to worker
worker.postMessage({ data: [1, 2, 3, 4, 5] });

// Receive result from worker
worker.on('message', result => {
  console.log('Worker result:', result);
});

worker.on('error', error => {
  console.error('Worker error:', error);
});

// worker.js (runs in separate thread)
const { parentPort } = require('worker_threads');

parentPort.on('message', (message) => {
  // CPU-intensive work in background
  const result = message.data.map(x => x * x);
  parentPort.postMessage(result);
});
```

**Python Multiprocessing Example:**
```python
from multiprocessing import Pool
import math

def cpu_intensive(n):
    """CPU-intensive calculation."""
    return sum(1 for i in range(n) if i % 2 == 0)

# Use multiple processes
with Pool(4) as pool:
    results = pool.map(cpu_intensive, [1000000, 2000000, 3000000])
    print(f"Results: {results}")

# Or use concurrent.futures
from concurrent.futures import ProcessPoolExecutor

with ProcessPoolExecutor(max_workers=4) as executor:
    futures = [
        executor.submit(cpu_intensive, 1000000),
        executor.submit(cpu_intensive, 2000000),
        executor.submit(cpu_intensive, 3000000)
    ]
    results = [f.result() for f in futures]
    print(f"Results: {results}")
```

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

**JavaScript Example (using Bull queue with Redis):**
```javascript
const Queue = require('bull');

// Create queue
const emailQueue = new Queue('emails', {
  redis: { host: 'localhost', port: 6379 }
});

// Add jobs to queue
async function sendEmail(to, subject, body) {
  const job = await emailQueue.add(
    { to, subject, body },
    { attempts: 3, backoff: { type: 'exponential', delay: 2000 } }
  );
  return job.id;
}

// Process jobs (limited concurrency)
emailQueue.process(5, async (job) => {
  const { to, subject, body } = job.data;

  try {
    await sendEmailViaProvider(to, subject, body);
    return { success: true };
  } catch (error) {
    throw error;  // Retry automatically
  }
});

// Track progress
emailQueue.on('completed', (job) => {
  console.log(`Email ${job.id} sent successfully`);
});

emailQueue.on('failed', (job, error) => {
  console.error(`Email ${job.id} failed:`, error);
});
```

**Python Example (using Celery with Redis):**
```python
from celery import Celery

# Configure Celery
app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task(bind=True, max_retries=3)
def send_email(self, to, subject, body):
    """Send email asynchronously."""
    try:
        # Simulate sending email
        import time
        time.sleep(1)

        if not email_provider.send(to, subject, body):
            raise Exception("Email provider failed")

        return {"success": True}
    except Exception as e:
        # Retry with exponential backoff
        self.retry(exc=e, countdown=2 ** self.request.retries)

# Usage
from tasks import send_email

# Queue task
send_email.delay('user@example.com', 'Welcome', 'Welcome to our app!')

# Or schedule for later
send_email.apply_async(
    args=('user@example.com', 'Welcome', 'Welcome to our app!'),
    countdown=60  # Execute after 60 seconds
)
```

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

## Pattern Interactions

**How to combine async patterns:**

**Scenario: Fetch user, their orders (parallel), then process each order**
```javascript
async function processUserOrders(userId) {
  try {
    // 1. Fetch user
    const user = await fetchUser(userId);

    // 2. Fetch orders in parallel
    const orders = await fetchOrders(userId);

    // 3. Process each order asynchronously (limited concurrency)
    const results = await Promise.all(
      orders.map(order => processOrderWithQueue(order))
    );

    return { user, orders: results };
  } catch (error) {
    console.error('Failed:', error);
    throw error;
  }
}
```

**Scenario: Real-time search with debounce and cancellation**
```javascript
let currentAbortController;

async function searchWithDebounce(query) {
  // Cancel previous request
  if (currentAbortController) {
    currentAbortController.abort();
  }

  currentAbortController = new AbortController();

  try {
    const response = await fetch(`/api/search?q=${query}`, {
      signal: currentAbortController.signal
    });

    const results = await response.json();
    displayResults(results);
  } catch (error) {
    if (error.name !== 'AbortError') {
      console.error('Search failed:', error);
    }
  }
}

// Debounce input
let timeout;
searchInput.addEventListener('input', (e) => {
  clearTimeout(timeout);
  timeout = setTimeout(() => {
    searchWithDebounce(e.target.value);
  }, 300);
});
```

---

## Antipatterns

**Mixing async and sync (confusing code):**
```javascript
// [NO] Bad: async function called without await
function processUser(userId) {
  const user = fetchUser(userId);  // Missing await!
  console.log(user);  // Promise, not user object
}

// [YES] Good: Properly await
async function processUser(userId) {
  const user = await fetchUser(userId);
  console.log(user);  // User object
}
```

**Swallowing errors:**
```javascript
// [NO] Bad: Error not caught
fetchUser(userId).then(user => {
  console.log(user);
});  // If fetchUser fails, error is uncaught

// [YES] Good: Error handled
fetchUser(userId)
  .then(user => console.log(user))
  .catch(error => console.error('Failed:', error));

// Or with async/await
try {
  const user = await fetchUser(userId);
  console.log(user);
} catch (error) {
  console.error('Failed:', error);
}
```

**Creating promise per iteration:**
```javascript
// [NO] Bad: Creates promise for each item (slow)
for (const userId of userIds) {
  await fetchUser(userId);  // Sequential, not parallel
}

// [YES] Good: Parallel execution
await Promise.all(
  userIds.map(userId => fetchUser(userId))
);
```

---

---

## Go Concurrency

Go uses goroutines and channels for concurrency. Key patterns:
- Use `go func()` for concurrent operations
- Use channels for communication between goroutines
- Use `context.Context` for cancellation and timeouts
- Use `sync.WaitGroup` to wait for multiple goroutines
- Use `errgroup` for error handling in concurrent operations

---

## Integration with Playbook

**Related to async patterns:**
- `/pb-performance` — Async for scalability
- `/pb-guide` — Testing async code and Go goroutine patterns
- `/pb-testing` — Async test patterns
- `/pb-patterns-core` — Core architectural patterns
- `/pb-patterns-db` — Database async operations

**Decision points:**
- When to use callbacks vs promises (JavaScript) vs goroutines (Go)
- When to introduce job queues or worker pools
- How to handle backpressure
- Error handling in async flows
- Context usage for timeouts and cancellation

---

## Related Commands

- `/pb-patterns-core` — Foundation patterns (SOA, Event-Driven, Retry)
- `/pb-patterns-distributed` — Distributed patterns that build on async
- `/pb-observability` — Monitor and trace async operations

---

*Created: 2026-01-11 | Category: Architecture | Tier: L*
*Updated: 2026-01-11 | Added Go examples*

