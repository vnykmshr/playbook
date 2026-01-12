# Design Rules Quick Reference

**One-page guide to 17 design rules. For detailed guidance, see `/pb-design-rules`.**

---

## The 4 Clusters

| Cluster | Rules | Focus | When It Matters |
|---------|-------|-------|-----------------|
| **CLARITY** | Clarity, Least Surprise, Silence, Representation | Understandability | APIs, interfaces, code readability |
| **SIMPLICITY** | Simplicity, Parsimony, Separation, Composition | Design Discipline | Architecture, scope, features |
| **RESILIENCE** | Robustness, Repair, Diversity, Optimization | Reliability & Evolution | Error handling, failures, learning |
| **EXTENSIBILITY** | Modularity, Economy, Generation, Extensibility | Long-term Growth | Architecture, future features |

---

## All 17 Rules at a Glance

| # | Rule | Principle | Anti-Pattern |
|---|------|-----------|--------------|
| 1 | **Clarity** | Clarity is better than cleverness | Cryptic, clever code that only the author understands |
| 2 | **Least Surprise** | Always do the least surprising thing | APIs that behave unexpectedly |
| 3 | **Silence** | When there's nothing to say, say nothing | Verbose output that masks real problems |
| 4 | **Representation** | Fold knowledge into data | Complex logic that could be simple with better data structures |
| 5 | **Simplicity** | Design for simplicity; add complexity only where you must | Over-engineered solutions |
| 6 | **Parsimony** | Write big programs only when clearly nothing else will do | Monoliths when smaller services would work |
| 7 | **Separation** | Separate policy from mechanism; separate interfaces from engines | Tangled abstractions; implementation details in interfaces |
| 8 | **Composition** | Design programs to be connected to other programs | Monolithic designs that can't be reused |
| 9 | **Robustness** | Robustness is the child of transparency and simplicity | Complex error handling without understanding the problem |
| 10 | **Repair** | When you must fail, fail noisily and as soon as possible | Silent failures that compound |
| 11 | **Diversity** | Distrust all claims for "one true way" | Dogmatic adherence to patterns that don't fit |
| 12 | **Optimization** | Prototype before polishing; get it working before you optimize | Premature optimization |
| 13 | **Modularity** | Write simple parts connected by clean interfaces | Tightly-coupled monoliths |
| 14 | **Economy** | Programmer time is expensive; conserve it | Hand-hacking when a library or tool exists |
| 15 | **Generation** | Avoid hand-hacking; write programs to write programs | Repetitive, error-prone manual code |
| 16 | **Extensibility** | Design for the future, because it will be here sooner than you think | Brittle designs that break with small changes |
| 17 | **Transparency** | Design for visibility to make inspection and debugging easier | Opaque systems that require debuggers to understand |

---

## Decision Tree: Which Rule Applies?

### **Are you designing an interface or API?**
- ✓ Clarity: Is the interface obviously correct?
- ✓ Least Surprise: Does it behave as expected?
- ✓ Composition: Will other systems want to use this?

### **Are you deciding on architecture or scope?**
- ✓ Simplicity: Is this the simplest solution?
- ✓ Parsimony: Do we need this complexity?
- ✓ Separation: Are concerns cleanly separated?
- ✓ Modularity: Are parts independent?

### **Are you dealing with errors or failures?**
- ✓ Repair: Are failures loud and clear?
- ✓ Robustness: Is simplicity enabling reliability?
- ✓ Transparency: Can we see what went wrong?

### **Are you thinking about the future?**
- ✓ Extensibility: Will changes require rebuilds?
- ✓ Economy: Are we investing programmer time wisely?
- ✓ Generation: Are we avoiding hand-hacking?

### **Are you optimizing performance?**
- ✓ Optimization: Have we measured the bottleneck?
- ✓ Simplicity: Is complexity adding real value?
- ✓ Economy: Is the speedup worth the cost?

---

## Rule-by-Rule Quick Guidance

### CLARITY Cluster

**Clarity: Clarity is better than cleverness**
- When: Choosing between implementations
- Action: Pick the obvious version
- Test: Would a new developer understand it in 5 minutes?

**Least Surprise: Always do the least surprising thing**
- When: Designing APIs and interfaces
- Action: Use conventions; do what's expected
- Test: Does this match what users expect?

**Silence: When there's nothing to say, say nothing**
- When: Designing output and logging
- Action: Only output when there's information
- Test: Does normal operation produce zero output?

**Representation: Fold knowledge into data**
- When: Designing data structures
- Action: Let the data structure encode constraints
- Test: Does the code read obviously from the data?

### SIMPLICITY Cluster

**Simplicity: Design for simplicity; add complexity only where you must**
- When: Making any design decision
- Action: Start simple; justify each addition
- Test: Can you remove anything without breaking requirements?

**Parsimony: Write big programs only when clearly nothing else will do**
- When: Choosing scope and scale
- Action: Start small; split only if necessary
- Test: Can this be three focused programs instead of one big one?

**Separation: Separate policy from mechanism**
- When: Designing layered architectures
- Action: Keep "what should happen" separate from "how"
- Test: Can you change the implementation without touching the interface?

**Composition: Design programs to be connected**
- When: Deciding on integration points
- Action: Design for reusability
- Test: Can other systems easily use this?

### RESILIENCE Cluster

**Robustness: Robustness is the child of transparency and simplicity**
- When: Building reliable systems
- Action: Make systems transparent first
- Test: Can you see what's happening without debugging?

**Repair: When you must fail, fail noisily**
- When: Designing error handling
- Action: Errors should be loud and immediate
- Test: Do problems surface where they start, not downstream?

**Diversity: Distrust all claims for "one true way"**
- When: Evaluating architectural approaches
- Action: Understand trade-offs; don't follow dogma
- Test: Can you explain why this is right for OUR context?

**Optimization: Prototype before polishing**
- When: Considering performance improvements
- Action: Measure first; optimize second
- Test: Do you have data showing this is the bottleneck?

### EXTENSIBILITY Cluster

**Modularity: Write simple parts connected by clean interfaces**
- When: Designing the overall structure
- Action: Build small, focused modules
- Test: Can you understand each module independently?

**Economy: Programmer time is expensive**
- When: Choosing between building vs. using
- Action: Use libraries; generate code; automate repetition
- Test: Are we writing code that a library could provide?

**Generation: Avoid hand-hacking**
- When: Doing the same thing repeatedly
- Action: Write code to generate the code
- Test: Is this pattern repeated more than once?

**Extensibility: Design for the future**
- When: Making structural decisions
- Action: Plan for adaptation without rebuilds
- Test: Can new requirements be added without changing core code?

**Transparency: Design for visibility**
- When: Building systems to be operated
- Action: Systems should be observable
- Test: Can you understand the system's state without a debugger?

---

## Trade-off Matrix: When Rules Conflict

| Conflict | Rule A | vs. | Rule B | Decision Framework |
|----------|--------|------|--------|-------------------|
| **Simplicity vs. Robustness** | "Keep it simple" | vs. | "Handle all failures" | Use preamble: surface trade-off explicitly. Usually: simple systems with clear failures beat complex error handling |
| **Clarity vs. Economy** | "Use one-liners" | vs. | "Use explicit names" | Prefer clarity. Accept more lines. Economy is about not writing unnecessary code, not about brevity |
| **Modularity vs. Performance** | "Separate concerns" | vs. | "Merge for speed" | Measure first. Usually modularity isn't the bottleneck. Only optimize after profiling |
| **Extensibility vs. Simplicity** | "Design for futures" | vs. | "Keep it minimal" | Design for modularity (enables extension), not flexibility (adds complexity). Build blocks that adapt, not flexible frameworks |
| **Generation vs. Clarity** | "Generate all code" | vs. | "Write clear code" | Generated code is fine if the generator is clear. Humans shouldn't read generated code |

---

## Failure Modes Diagnosis

**Your system violates design rules if you see:**

| Symptom | Broken Rules | Fix |
|---------|--------------|-----|
| "This code is impossible to understand" | Clarity | Rewrite for explicitness; reject clever |
| "This API surprises everyone" | Least Surprise | Document expected behavior; change API to match expectations |
| "Output is too verbose; problems get lost" | Silence | Disable debug output in production; be selectively verbose |
| "Logic is tangled; data is unclear" | Representation | Redesign data structures to encode constraints |
| "Every change requires rebuilding everything" | Separation, Modularity | Refactor into independent pieces with clean interfaces |
| "The system is too complex; even we don't understand it" | Simplicity, Robustness | Delete features; simplify core; redesign for transparency |
| "We're paying high server costs for a problem we can't solve" | Optimization, Measurement | Measure before optimizing; profile to find the bottleneck |
| "Errors hide until they've caused major damage" | Repair, Transparency | Fail fast; log state changes; make failures loud |
| "We can't add features without breaking existing ones" | Extensibility, Modularity | Design for composition; build new features as separate modules |
| "We hand-write boilerplate over and over" | Generation | Write a generator; use templates; automate the pattern |

---

## Quick Checklist: Are You Following Design Rules?

- [ ] Interfaces and APIs are obvious and unsurprising
- [ ] Code is readable by someone unfamiliar with it
- [ ] Data structures encode the problem clearly
- [ ] You've justified every piece of complexity
- [ ] Architecture separates concerns clearly
- [ ] Modules are independent and reusable
- [ ] Errors are loud and immediate
- [ ] The system is observable without special tools
- [ ] You've measured before optimizing
- [ ] You've designed for future adaptation without adding flexibility now

**Yes to most?** You're following design rules.
**No to several?** Read the full guidance: `/pb-design-rules`

---

## Integration with Preamble

**Preamble** (HOW teams think together):
- Challenge assumptions
- Think like peers
- Prefer correctness over agreement

**Design Rules** (WHAT systems are built):
- Clarity enables teams to challenge architectural decisions
- Simplicity enables teams to question complexity
- Transparency enables teams to discuss based on data

**Together:**
A team using preamble thinking with design rules awareness makes better decisions faster. Preamble thinking without design discipline builds wrong things. Design rules without preamble thinking get debated endlessly.

---

## Quick Navigation: Find What You Need

| I need guidance on... | Read this |
|----------------------|-----------|
| Making APIs obvious | Rules 1-4 (CLARITY) |
| Deciding on architecture | Rules 5-8 (SIMPLICITY) |
| Error handling | Rules 9-12 (RESILIENCE) |
| Long-term design | Rules 13-17 (EXTENSIBILITY) |
| Choosing between options | Trade-off Matrix (above) |
| Understanding what went wrong | Failure Modes Diagnosis (above) |

---

## The Test: Are You Following Design Rules?

**Good signs:**
- New developers understand the code quickly
- Errors point to the real problem
- Adding features doesn't require rewriting core code
- The system is obviously correct, not mysteriously working
- Performance matches requirements; no premature optimization
- Modules can be understood independently

**Warning signs:**
- "Only [person] understands this code"
- Errors hide until they cause cascading failures
- Every change touches multiple unrelated files
- You're hand-writing the same pattern repeatedly
- "It's fast, but I don't know why"
- Modules depend on each other's internals

---

## Remember

**Design Rules are:**
- About building systems that work, last, and adapt
- Complementary to preamble thinking (team collaboration)
- Trade-offs to understand, not laws to obey
- Applied in context, not dogmatically
- Visible in the patterns and practices throughout the playbook

**Design Rules are NOT:**
- Rigid laws that apply the same everywhere
- Reasons to over-engineer
- Excuses for missing deadlines
- Arguments to win; they're frameworks to think with

**The goal:** Build systems that are clear, simple, reliable, and adaptable. Design rules guide that thinking.

---

*Design Rules Quick Reference — For complete guidance, read `/pb-design-rules`.*
