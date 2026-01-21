# Debugging Methodology

Systematic approach to finding and fixing bugs. Hypothesis-driven, reproducible, methodical.

**Debugging is not random poking.** It's a structured process: observe, hypothesize, test, repeat.

**Mindset:** Use `/pb-preamble` thinking to challenge your assumptions about what's broken. Use `/pb-design-rules` thinking — especially Transparency (make the invisible visible), Repair (fail noisily to aid debugging), and Clarity (simple code is easier to debug).

---

## The Debugging Process

### 1. Reproduce

**Before anything else, reproduce the bug reliably.**

```
Can you reproduce it?
├─ Yes → Continue to Step 2
└─ No → Gather more information
    ├─ What were the exact steps?
    ├─ What environment? (browser, OS, user)
    ├─ What was the system state? (logged in, data present)
    └─ Was there anything unusual? (network, timing)
```

**No reproduction = No debugging.** If you can't reproduce it, you can't verify the fix.

### 2. Isolate

**Narrow down the problem space.**

**Binary search:** Cut the problem in half repeatedly.

```
Is it frontend or backend?
├─ Frontend → Is it JavaScript or CSS?
│   ├─ JavaScript → Is it this component or its parent?
│   └─ CSS → Is it this rule or inherited?
└─ Backend → Is it the API handler or the database?
    ├─ API handler → Is it request parsing or response?
    └─ Database → Is it the query or the data?
```

**Minimal reproduction:** Remove code until the bug disappears, then add it back.

### 3. Hypothesize

**Form a specific, testable hypothesis.**

```
# [NO] Vague
"Something is wrong with the login."

# [YES] Specific
"The login fails because the session cookie is not being set
when the SameSite attribute is 'Strict' and the request
comes from a different origin."
```

**Good hypothesis properties:**
- Specific (points to a cause)
- Testable (can be proven/disproven)
- Explains the symptoms

### 4. Test

**Test ONE variable at a time.**

```
# [NO] Multiple changes
"I added logging, fixed the null check, and changed the query."

# [YES] Single change
"I added logging to see if the value is null."
→ Value is null
"Now I'll check where the null comes from."
```

**Record your tests:** What you tried, what you observed.

### 5. Fix and Verify

**Fix the root cause, not the symptom.**

```
# [NO] Symptom fix
if (user === null) return;  // Hide the crash

# [YES] Root cause fix
// Ensure user is loaded before this function is called
// Add proper error handling upstream
```

**Verify:**
- Bug no longer reproduces
- No new bugs introduced
- Related functionality still works

### 6. Prevent

**After fixing, prevent recurrence.**

- Add a test that would have caught this
- Improve error messages to aid future debugging
- Document in code comments if the fix is non-obvious
- Consider: Is this a pattern? Should we lint for it?

---

## Debugging Techniques

### Print Debugging (Console/Log)

The simplest tool, often the most effective:

```javascript
// Strategic logging
console.log('[DEBUG] fetchUser called with:', { userId, options });

// With timestamps
console.log(`[${new Date().toISOString()}] State changed:`, newState);

// Conditional logging
if (DEBUG) console.log('Expensive debug info:', computeDebugInfo());
```

**Best practices:**
- Include context (function name, relevant values)
- Use structured data (objects, not string concatenation)
- Add timestamps for timing issues
- Clean up before committing

### Debugger (Breakpoints)

**When to use debugger instead of console.log:**
- Need to inspect complex state
- Need to step through logic
- Need to examine call stack
- Console.log would need many iterations

**JavaScript:**
```javascript
function processOrder(order) {
  debugger;  // Pause here in DevTools
  // Or set breakpoint in DevTools directly
}
```

**Python:**
```python
def process_order(order):
    import pdb; pdb.set_trace()  # Interactive debugger
    # Or use breakpoint() in Python 3.7+
```

**Go:**
```go
// Use Delve debugger
// dlv debug main.go
// break main.processOrder
// continue
```

### Network Debugging

**Browser DevTools → Network tab:**
- Request/response headers
- Request/response body
- Timing breakdown
- CORS issues (check console too)

**cURL for API debugging:**
```bash
# See full request/response
curl -v https://api.example.com/users

# With headers
curl -H "Authorization: Bearer token" https://api.example.com/users

# POST with data
curl -X POST -H "Content-Type: application/json" \
  -d '{"name":"test"}' https://api.example.com/users
```

### Database Debugging

**Log the actual queries:**
```sql
-- PostgreSQL: Enable query logging
SET log_statement = 'all';

-- MySQL: Enable general log
SET GLOBAL general_log = 'ON';
```

**Explain the query:**
```sql
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';
```

**Check for:**
- Full table scans (missing index)
- Unexpected NULL handling
- Type coercion issues
- Lock contention

### Performance Profiling

**When the bug is "it's slow":**

**JavaScript (Browser):**
```javascript
// Console timing
console.time('operation');
doExpensiveOperation();
console.timeEnd('operation');

// Performance API
performance.mark('start');
doExpensiveOperation();
performance.mark('end');
performance.measure('operation', 'start', 'end');
```

**Python:**
```python
import cProfile
cProfile.run('expensive_function()')

# Or with context manager
import time
start = time.perf_counter()
expensive_function()
print(f"Took {time.perf_counter() - start:.3f}s")
```

**Go:**
```go
import "runtime/pprof"

// CPU profiling
f, _ := os.Create("cpu.prof")
pprof.StartCPUProfile(f)
defer pprof.StopCPUProfile()

// Then: go tool pprof cpu.prof
```

### Frontend Debugging

**Browser DevTools (F12):**

| Tab | Use For |
|-----|---------|
| Elements | DOM inspection, CSS debugging, layout issues |
| Console | JavaScript errors, logging, REPL |
| Network | API calls, timing, headers, CORS issues |
| Performance | Rendering bottlenecks, long tasks |
| Application | Storage, cookies, service workers |
| Sources | Breakpoints, source maps, call stack |

**Network waterfall analysis:**
```
1. Check for failed requests (red)
2. Look for slow requests (long bars)
3. Check CORS errors in Console
4. Verify request/response headers
5. Inspect payload for unexpected data
```

**Framework DevTools:**

**React DevTools:**
```
- Components tab: Inspect component tree, props, state
- Profiler tab: Identify re-render bottlenecks
- Highlight updates: See what re-renders on each change
```

**Vue DevTools:**
```
- Components: Inspect component hierarchy and data
- Vuex/Pinia: Track state mutations
- Timeline: Event and mutation history
```

**Component re-render debugging (React):**

```javascript
// Why did this render?
import { useRef, useEffect } from 'react';

function useWhyDidYouRender(name, props) {
  const prevProps = useRef(props);

  useEffect(() => {
    const changes = {};
    for (const key in props) {
      if (prevProps.current[key] !== props[key]) {
        changes[key] = { from: prevProps.current[key], to: props[key] };
      }
    }
    if (Object.keys(changes).length > 0) {
      console.log(`[${name}] re-rendered:`, changes);
    }
    prevProps.current = props;
  });
}

// Usage
function MyComponent(props) {
  useWhyDidYouRender('MyComponent', props);
  return <div>...</div>;
}
```

**Source maps:**
- Enable "Enable JavaScript source maps" in DevTools settings
- Build tools should generate `.map` files in development
- Breakpoints work on original source, not bundled code

---

## Common Bug Patterns

### Null/Undefined Reference

**Symptom:** `Cannot read property 'x' of undefined`

**Check:**
1. Is the object actually defined?
2. Is the async operation complete?
3. Is the property name correct?
4. Is there a race condition?

```javascript
// [NO] Assuming data exists
const name = user.profile.name;

// [YES] Defensive access
const name = user?.profile?.name ?? 'Unknown';
```

### Off-by-One Errors

**Symptom:** Missing first/last item, index out of bounds

**Check:**
1. Loop bounds: `< length` vs `<= length`
2. Array indexing: 0-based vs 1-based confusion
3. Substring: inclusive vs exclusive end

```javascript
// Common mistake
for (let i = 0; i <= arr.length; i++) // [NO] <= causes overflow

// Correct
for (let i = 0; i < arr.length; i++)  // [YES] <
```

### Race Conditions

**Symptom:** Works sometimes, fails other times

**Check:**
1. Async operations completing in unexpected order
2. State mutations during async operations
3. Missing await/promise handling

```javascript
// Race condition
let data;
fetchData().then(d => data = d);
console.log(data);  // undefined! (async not complete)

// Fixed
const data = await fetchData();
console.log(data);  // Has value
```

### State Mutation Bugs

**Symptom:** Unexpected state changes, "stale" data

**Check:**
1. Direct mutation vs immutable update
2. Reference sharing between objects
3. Closure capturing outdated value

```javascript
// Bug: Direct mutation
function addItem(arr, item) {
  arr.push(item);  // Mutates original
  return arr;
}

// Fixed: Immutable
function addItem(arr, item) {
  return [...arr, item];  // New array
}
```

### Character Encoding Issues

**Symptom:** Garbled text, unexpected characters

**Check:**
1. Database encoding (UTF-8?)
2. HTTP Content-Type header
3. File encoding
4. String comparison with invisible characters

```bash
# Check for hidden characters
cat -A file.txt
hexdump -C file.txt | head
```

### Timezone Bugs

**Symptom:** Times off by hours, different on different machines

**Check:**
1. Server vs client timezone
2. UTC vs local time confusion
3. Daylight saving time handling

```javascript
// Always work in UTC internally
const utcDate = new Date().toISOString();

// Convert to local only for display
const localDate = new Date(utcDate).toLocaleString();
```

---

## Production Debugging

### Safe Investigation

**Never debug production by:**
- Adding console.log and deploying
- Connecting debugger directly
- Running random queries against prod database

**Instead:**
1. **Check existing logs** — What do we already capture?
2. **Check metrics** — Latency spikes? Error rates?
3. **Reproduce in staging** — With production-like data
4. **Add targeted logging** — Feature-flagged, for specific users/requests

### Log Analysis

```bash
# Search for errors
grep -i "error" /var/log/app.log | tail -100

# Count by type
grep -i "error" /var/log/app.log | sort | uniq -c | sort -rn

# Around a timestamp
grep -A5 -B5 "2024-01-15 10:30" /var/log/app.log

# Follow in real-time
tail -f /var/log/app.log | grep --line-buffered "user_123"
```

### Distributed Tracing

For microservices, use trace IDs:

```
# Request flow
API Gateway (trace: abc123)
  → User Service (trace: abc123)
    → Database (trace: abc123)
  → Order Service (trace: abc123)
    → Payment Service (trace: abc123)
```

**Tools:** Jaeger, Zipkin, Datadog, Honeycomb

See `/pb-observability` for detailed tracing guidance.

### Incident Debugging

When production is down, see `/pb-incident` for the full process. Quick reminder:

1. **Mitigate first** — Rollback, disable feature, scale up
2. **Investigate second** — After bleeding is stopped
3. **Document everything** — For post-incident review

---

## Debugging Checklist

### Before Debugging

- [ ] Can I reproduce the bug?
- [ ] Do I have logs/errors from the failure?
- [ ] Do I understand what SHOULD happen?
- [ ] Is this the right environment? (local, staging, prod)

### During Debugging

- [ ] Am I changing ONE thing at a time?
- [ ] Am I recording what I've tried?
- [ ] Do I have a specific hypothesis?
- [ ] Am I avoiding assumptions?

### After Fixing

- [ ] Does the bug still reproduce? (It shouldn't)
- [ ] Did I add a regression test?
- [ ] Did I fix the root cause, not just the symptom?
- [ ] Is there cleanup needed? (debug logs, temporary code)

---

## Tools Quick Reference

| Category | Tool | Use |
|----------|------|-----|
| Browser | DevTools (F12) | JS debugging, network, performance |
| Node.js | `--inspect` | Chrome DevTools for Node |
| Python | pdb, ipdb | Interactive debugger |
| Go | Delve (dlv) | Go debugger |
| Database | EXPLAIN ANALYZE | Query performance |
| Network | cURL, Postman | API debugging |
| Logs | grep, jq | Log analysis |
| Tracing | Jaeger, Zipkin | Distributed tracing |

---

## Related Commands

- `/pb-logging` — Effective logging for debugging
- `/pb-observability` — Metrics and tracing
- `/pb-incident` — Production incident response
- `/pb-testing` — Tests that catch bugs early
- `/pb-learn` — Capture debugging patterns for future reuse

---

## Design Rules Applied

| Rule | Application |
|------|-------------|
| **Transparency** | Make the invisible visible through logging and tracing |
| **Repair** | Fail noisily with useful error messages |
| **Clarity** | Simple code is easier to debug |
| **Economy** | Measure before optimizing; hypothesis before fixing |

---

**Last Updated:** 2026-01-19
**Version:** 1.0
