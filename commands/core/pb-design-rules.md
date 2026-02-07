# Design Rules: Core Technical Principles

> **The preamble tells us HOW teams think together. Design rules tell us WHAT we build. Together, they form the complete framework for engineering excellence.**

**Resource Hint:** sonnet — Reference material for applying established design principles.

## When to Use

- Making architectural or design trade-off decisions
- Reviewing code or designs against core principles
- Settling disagreements about "the right way" to build something
- Onboarding engineers to the team's technical philosophy

---

## Anchor: Why These 17 Rules Matter

These are 17 classical software design principles that have proven themselves across decades of software engineering. They're not new. They're not trendy. But they're foundational because they describe how to build systems that work, last, and adapt.

**The critical insight:** When a team uses preamble thinking (challenge assumptions, prefer correctness over agreement, think like peers), they need design rules to guide WHAT they're building. Without design rules, good collaboration produces poorly-designed systems. Without preamble thinking, teams debate design rules endlessly without resolution.

**How they apply to everything:**
- **Planning** — Design decisions embody these rules from the start
- **Development** — Every architectural choice reflects these principles
- **Review** — Reviewers challenge based on which rules are violated
- **Operations** — Systems designed by these rules stay maintainable and adaptable

**The four clusters** below group the 17 rules into memorable themes: CLARITY, SIMPLICITY, RESILIENCE, and EXTENSIBILITY. Together, they provide a complete framework for technical decision-making.

---

## Cluster 1: CLARITY — Design for Understandability

### 1. Rule of Clarity: Clarity is Better Than Cleverness

**The Principle:**
When you have a choice between a clever solution and a clear solution, choose clarity every time. Clever solutions impress the author; clear solutions serve everyone who reads the code.

**Why It Matters:**
Code is read far more often than it's written. A clever solution that only the author understands becomes a liability: it's hard to debug, hard to modify, hard to teach. A clear solution is learned once and used forever.

**In Practice:**
- Explicit variable names beat cryptic abbreviations
- Simple control flow beats nested ternaries
- Obvious patterns beat surprising optimizations
- Readable code beats compressed code

**When It Costs:**
Clarity sometimes means writing more code. Sometimes it means passing more parameters. That's a trade-off you accept because clarity enables all future work on this code.

---

### 2. Rule of Least Surprise: Always Do the Least Surprising Thing

**The Principle:**
In interface design and API design, always choose the behavior users would expect. Don't surprise them, even in clever ways.

**Why It Matters:**
Surprise is context-switching. When an API behaves unexpectedly, developers stop working and debug. "Oh, that function modifies the original list" or "Oh, that parameter counts from zero" takes mental energy. Expected behavior is automatic; unexpected behavior is cognitive load.

**In Practice:**
- Convention over configuration (use industry standards)
- Consistent patterns across your codebase
- Clear error messages that explain what went wrong
- Predictable state transitions

**Example:**
Don't write a `map()` function that deletes elements. Write a `filter()` function instead. Users expect `map()` to transform without removing.

---

### 3. Rule of Silence: When There's Nothing to Say, Say Nothing

**The Principle:**
Programs should be quiet unless they have something important to communicate. Excessive logging, warnings, and output become noise that masks actual problems.

**Why It Matters:**
When everything outputs constantly, important signals disappear. Someone runs the program, gets 50 lines of output, and can't tell which lines matter. Real problems get missed because they're drowned out by chatter.

**In Practice:**
- Verbose logging during development, silent in production
- Errors are loud; normal operation is quiet
- No progress messages for fast operations
- No warnings for expected edge cases

**Example:**
A deployment that succeeds produces zero output. A deployment that fails produces a clear error. Not the reverse.

---

### 4. Rule of Representation: Fold Knowledge Into Data

**The Principle:**
Make the data structure so clear that the logic becomes simple. The work of your program should be visible in the data, not hidden in the code.

**Why It Matters:**
Logic is hard to reason about. Data structures are easy to reason about. When you push knowledge into data, the program becomes obviously correct instead of mysteriously working.

**In Practice:**
- Data structures that represent the problem domain
- Enums instead of magic numbers
- Explicit state in data structures, not implicit in control flow
- Type systems that enforce constraints

**Example:**
Don't represent "user role" as strings that you check with `if role == "admin"`. Represent it as an enum:
```
enum Role { Admin, User, Guest }
```
Now the code is obviously correct: you can't forget a case.

---

## Cluster 2: SIMPLICITY — Design for Discipline

### 5. Rule of Simplicity: Design for Simplicity; Add Complexity Only Where You Must

**The Principle:**
Simpler is better. Every line of code adds cost: reading, debugging, testing, maintaining. Before adding complexity, justify it.

**Why It Matters:**
Complex systems fail in ways you didn't anticipate. Simple systems fail in ways you can predict. A simple system with a known limitation is more reliable than a complex system that *tries* to handle everything.

**In Practice:**
- Start with the simplest solution that works
- Add features when you need them, not when you might
- Delete code that isn't used
- Refuse "nice to have" complexity

**When It's Hard:**
Simplicity requires discipline. It's harder in the moment: "Let me add support for X even though we don't need it yet." But you're paying a cost every single day the code exists. That one "nice to have" feature might never be needed and costs you 1000 days of maintenance.

---

### 6. Rule of Parsimony: Write Big Programs Only When Clearly Nothing Else Will Do

**The Principle:**
Before writing a big, complex system, prove that nothing simpler will work. Most monoliths started as microservices in someone's head but couldn't be simplified.

**Why It Matters:**
Big programs are exponentially harder to understand and maintain. Before you choose this path, prove it's necessary. Most of the time, three focused small programs beat one big one.

**In Practice:**
- Can you build this as an add-on? Do that instead.
- Can you use a library? Use it instead of writing it.
- Can you simplify the requirements? Do that before building big.

**The Anti-pattern:**
"We'll build a flexible framework that handles all possible cases." You won't use 80% of it. Delete it.

---

### 7. Rule of Separation: Separate Policy From Mechanism; Separate Interfaces From Engines

**The Principle:**
Don't mix different levels of abstraction. Keep the "what should happen" separate from "how it happens." Keep the interface separate from the implementation.

**Why It Matters:**
When you mix abstraction levels, changes ripple everywhere. When you expose implementation details, clients depend on them. You lose the ability to change anything without breaking everything.

**In Practice:**
- Interfaces that describe contracts
- Implementations that fulfill contracts
- Don't leak implementation details
- Don't require callers to understand how it works

**Example:**
```
Good: public interface List<T> { void add(T item); }
Bad:  public interface List<T> { void add(T item); void resize(); }
```
The bad version exposes that lists resize internally. Now clients can't be changed without breaking code.

---

### 8. Rule of Composition: Design Programs to Be Connected to Other Programs

**The Principle:**
Build things that work well together. Design systems as components, not monoliths. Make your output useful as someone else's input.

**Why It Matters:**
The moment you design for composition, you get reusability, modularity, and flexibility for free. Monolithic design requires you to do everything yourself.

**In Practice:**
- Clean interfaces between components
- Use standard data formats
- Unix philosophy: do one thing well
- Components that are useful independently

**Example:**
A linting tool that writes JSON output can be used with any downstream tool. A tool that writes HTML can't be piped to anything else.

---

## Cluster 3: RESILIENCE — Design for Reliability and Evolution

### 9. Rule of Robustness: Robustness Is the Child of Transparency and Simplicity

**The Principle:**
You build robust systems not by adding error handling everywhere, but by making systems so transparent and simple that errors are obvious and handling is straightforward.

**Why It Matters:**
Complex error handling hides bugs. Transparent systems reveal bugs immediately. Simple systems fail predictably. The path to robust systems is NOT "more error handling," it's "less hidden complexity."

**In Practice:**
- Fail fast and loudly
- Make state changes explicit
- Simple error handling (not nested try-catch blocks)
- Transparency enables quick recovery

**Example:**
Bad: Complex error handling that tries to recover from any failure
Good: Fail immediately when invariants are violated, so you know exactly what went wrong

---

### 10. Rule of Repair: When You Must Fail, Fail Noisily and As Soon As Possible

**The Principle:**
Errors that hide are worse than errors that scream. When something goes wrong, make it obvious immediately, not hours later when data is corrupted.

**Why It Matters:**
Silent failures compound. By the time you discover a problem, you've processed gigabytes of corrupted data. Loud failures let you fix the problem at the source, while the scope is still manageable.

**In Practice:**
- Assertions and checks
- Fail-fast validation
- Explicit error handling
- Clear error messages

**Example:**
Don't silently return null. Throw an exception. The exception tells you where the real problem is; null hides the problem until it causes cascading failures.

---

### 11. Rule of Diversity: Distrust All Claims for "One True Way"

**The Principle:**
Any claim that there's ONE best way to do something is probably wrong. Most meaningful choices have trade-offs. Understand the trade-offs instead of following dogma.

**Why It Matters:**
Dogma kills thinking. "We always use X" prevents you from choosing the right tool for the job. "Best practices are law" prevents you from adapting to your context.

**In Practice:**
- Understand why you're choosing something
- Be prepared to choose differently for different contexts
- Challenge architectural dogma
- Use preamble thinking: question assumptions, don't just follow rules

**Example:**
Microservices aren't always better than monoliths. Sometimes a monolith is the right choice. Understand the trade-offs for YOUR problem, then decide.

---

### 12. Rule of Optimization: Prototype Before Polishing. Get It Working Before You Optimize It

**The Principle:**
Build it first. Make it work. Make it clear. THEN optimize, but only if you measure and find a real bottleneck.

**Why It Matters:**
Optimization is expensive: added complexity, reduced readability, hard-to-predict failures. Most programs spend 80% of time in 20% of the code. Optimizing randomly costs you everywhere and helps nowhere.

**In Practice:**
- Measure before optimizing
- Profile to find the real bottleneck
- Optimize only the bottleneck
- Document why this code is optimized

**The Anti-pattern:**
"This might be slow, so let me optimize it." You're adding complexity to solve a problem that doesn't exist.

---

## Cluster 4: EXTENSIBILITY — Design for Long-Term Growth

### 13. Rule of Modularity: Write Simple Parts Connected by Clean Interfaces

**The Principle:**
Build systems as a collection of simple modules that communicate through clear, stable interfaces. This is the foundation of all other extensibility.

**Why It Matters:**
Modular systems are:
- Easier to understand (one module at a time)
- Easier to test (test each module independently)
- Easier to change (change one module)
- Easier to reuse (use the module elsewhere)

**In Practice:**
- High cohesion within modules (similar things together)
- Low coupling between modules (minimal dependencies)
- Explicit interfaces (clear contracts)
- Clear boundaries

**Example:**
A payment module doesn't know about logging. Logging doesn't know about payments. They communicate through agreed-on interfaces.

---

### 14. Rule of Economy: Programmer Time Is Expensive; Conserve It in Preference to Machine Time

**The Principle:**
If you have to choose between using more CPU/memory/network and saving programmer time, choose to save programmer time. Machines are cheap; programmers are expensive.

**Why It Matters:**
A slow program that you can understand and modify is more valuable than a fast program that's impossible to understand. The opposite used to be true when computers were expensive and programmers were cheap. That world is gone.

**In Practice:**
- Use high-level languages and frameworks
- Let the computer do grunt work (generate code, optimize, etc.)
- Don't optimize prematurely
- Use libraries instead of building from scratch

**Example:**
Use an ORM instead of hand-writing SQL, even though raw SQL might be slightly faster. Your programmer can modify it in minutes instead of hours.

---

### 15. Rule of Generation: Avoid Hand-Hacking; Write Programs to Write Programs When You Can

**The Principle:**
If you're doing the same thing repeatedly, write a program to do it. Code generation, templating, configuration files—use these instead of manual repetition.

**Why It Matters:**
Hand-hacked code is full of subtle variations: copy-paste mistakes, inconsistencies, forgotten updates. Generated code is consistent: the pattern is written once and applied everywhere.

**In Practice:**
- Makefiles and build scripts
- Code generators
- Configuration files
- Templates and scaffolding

**Example:**
Don't write database access code by hand for each entity. Generate it from a schema. One mistake in the generator is one mistake fixed; one mistake in hand-written code is one mistake per entity.

---

### 16. Rule of Extensibility: Design for the Future, Because It Will Be Here Sooner Than You Think

**The Principle:**
Systems outlive your assumptions about them. Design so that the next person (or future you) can add features without rebuilding from scratch.

**Why It Matters:**
Software that served one purpose often needs to serve another. Features that seemed impossible now seem essential. Systems must be designed for adaptation.

**In Practice:**
- Clean interfaces enable new uses
- Modular design enables new components
- Clear separation of concerns enables new policies
- Documentation of assumptions enables future understanding

**Example:**
When you design a logging system, assume it will need to:
- Write to files
- Write to cloud services
- Be filtered by severity
- Be enriched with context

Design for these possibilities now, even if you don't need them yet.

---

### 17. Rule of Transparency: Design for Visibility to Make Inspection and Debugging Easier

**The Principle:**
System behavior should be observable. You should be able to see what's happening without guessing or inserting debugging code.

**Why It Matters:**
Debugging invisible systems takes forever. Systems designed for transparency reveal their state and behavior clearly, making problems obvious when they occur.

**In Practice:**
- Logging at appropriate levels
- Metrics and observability
- Clear state representations
- Explicit error messages
- Debuggable interfaces

**Example:**
A system that logs every significant state change is much easier to debug than a system that requires stepping through a debugger.

---

## Decision Framework: When Rules Conflict

These 17 rules don't always agree with each other. Understanding the trade-offs is critical.

### Common Tensions

**Simplicity vs. Robustness**
- Simple systems sometimes need complex error handling
- Robust systems sometimes need complex logic

**Solution:** Use preamble thinking. Surface the trade-off explicitly. Challenge assumptions: "Do we actually need this robustness?" Document the choice so future work understands why.

**Clarity vs. Economy**
- Explicit code is clearer but longer
- Concise code is shorter but less clear

**Solution:** Optimize for understanding first. Accept more code if it means clarity. Economy is about not writing unnecessary code, not about writing concise code.

**Modularity vs. Performance**
- Modular systems have function-call overhead
- Optimized systems sometimes require merging modules

**Solution:** Measure first (Rule of Optimization). Don't assume modularity is slow. Only optimize after profiling. Even then, keep the modular design and optimize carefully within it.

**Extensibility vs. Simplicity**
- Designing for future extensions adds complexity now
- Simple designs don't anticipate future needs

**Solution:** Design for extensibility through modularity, not through flexibility. Don't try to handle all possible futures. Build modules that new code can extend without modifying existing code.

---

## How Rules Apply Across the Playbook

### In Planning (`/pb-plan`, `/pb-adr`)
- **Clarity**: ADRs document decisions explicitly
- **Representation**: Design documents show data structures clearly
- **Separation**: Separate concerns in the architecture

### In Development (`/pb-start`, `/pb-cycle`)
- **Simplicity**: Start simple; add features when needed
- **Modularity**: Build small, focused pieces
- **Optimization**: Test first; optimize only if measured

### In Review (`/pb-review-hygiene`, `/pb-review-product`)
- **Clarity**: Code is understandable
- **Robustness**: Error handling is appropriate
- **Modularity**: Pieces are independent
- **Extensibility**: Changes can be made without rebuilding

### In Operations (`/pb-incident`, `/pb-observability`)
- **Transparency**: Systems are observable
- **Repair**: Failures are loud and clear
- **Simplicity**: Operational procedures are straightforward

---

## Examples: Rules in Action

### Example 1: API Design (Clarity, Composition, Least Surprise)

**Problem:** You're designing an API for user authentication.

**Bad Design (Violates Clarity & Least Surprise):**
```
POST /auth with body { user: "...", pass: "..." }
Returns 200 with { token: "...", etc: "..." } on success
Returns 200 with empty body on failure (unclear!)
Token expires silently; caller has no warning
```

**Good Design (Follows Clarity & Least Surprise):**
```
POST /auth with clear request body
Returns 200 with { token, expiresAt, refreshToken }
Returns 401 with { error, errorDescription } on failure
Includes expiresAt so caller can proactively refresh
```

**Rules Applied:**
- **Clarity**: API is obviously correct. No surprises.
- **Least Surprise**: Errors are clear; expiration is explicit
- **Composition**: Other systems can easily use this API
- **Silence**: Success returns just what's needed

---

### Example 2: Refactoring (Simplicity, Modularity, Repair)

**Problem:** You have a 500-line function that handles user creation, validation, logging, and error reporting.

**Bad Approach (Violates Simplicity & Modularity):**
Try to optimize the function. Add more error handling. Make it more robust by adding checks everywhere.

**Good Approach (Follows Design Rules):**
1. Separate validation from creation
2. Separate logging from business logic
3. Separate error handling from happy path
4. Test each piece independently
5. Now you have five simple functions instead of one complex one

**Rules Applied:**
- **Simplicity**: Each function is simple
- **Separation**: Concerns are separate
- **Modularity**: Each function is independent
- **Repair**: Errors are clear at each step

---

### Example 3: System Architecture (Separation, Composition, Extensibility)

**Problem:** You're designing a notification system (emails, SMS, Slack).

**Bad Design (Violates Separation & Modularity):**
One service handles all notification types. Each new type requires modifying core code. Logic is tangled.

**Good Design (Follows Design Rules):**
```
NotificationService (interface)
├── EmailNotification (implementation)
├── SMSNotification (implementation)
└── SlackNotification (implementation)

New notification types extend the interface, don't modify existing code
```

**Rules Applied:**
- **Separation**: Policy (when to notify) from mechanism (how)
- **Composition**: New types compose into the system
- **Modularity**: Each implementation is independent
- **Extensibility**: Adding new types doesn't touch old code

---

### Example 4: Documentation (Clarity, Representation, Least Surprise)

**Problem:** You're documenting a library's error handling.

**Bad Documentation (Violates Clarity):**
"This function may throw errors. Handle appropriately."

**Good Documentation (Follows Clarity):**
```
Throws ValidationError if input is invalid
Throws TimeoutError if operation exceeds 30 seconds
Throws ConnectionError if database is unavailable
Returns null if resource not found

All errors include error.code and error.message for handling
```

**Rules Applied:**
- **Clarity**: Errors are completely clear
- **Representation**: Error types encode the problem
- **Least Surprise**: Caller expects exactly these errors
- **Silence**: Documentation says only what matters

---

### Example 5: Error Handling (Repair, Transparency, Robustness)

**Problem:** Your system has a bug where corrupted data silently accumulates.

**Bad Response (Violates Repair):**
Add more error handling downstream hoping to catch it eventually.

**Good Response (Follows Design Rules):**
1. Add validation at the source (Repair: fail immediately)
2. Add logging so problems are visible (Transparency)
3. Make the corruption obvious, not subtle (Robustness through transparency)
4. Fix the root cause; don't try to recover silently

**Rules Applied:**
- **Repair**: Fail noisily at the source
- **Transparency**: Log what's happening
- **Robustness**: Visible failures are more robust than silent ones

---

## Related Commands

- `/pb-preamble` — How teams think together (complement to design rules)
- `/pb-adr` — Architecture decisions document rules
- `/pb-patterns` — Patterns show rules in practice
- `/pb-review-hygiene` — Code review checks rules
- `/pb-standards` — Working principles and code quality

---

*Design Rules — Technical principles that complement preamble thinking and guide every engineering decision.*
