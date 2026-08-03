---
name: "pb-standards"
title: "Project Guidelines & Working Principles"
category: "core"
difficulty: "beginner"
model_hint: "sonnet"
execution_pattern: "reference"
related_commands: ['pb-preamble', 'pb-design-rules', 'pb-handcraft', 'pb-voice', 'pb-testing']
last_reviewed: "2026-08-03"
last_evolved: "2026-08-03"
version: "1.3.0"
version_notes: "v1.3.0: Trim IV and VIII. Stack guidance now points at the playbooks that own it (Node keeps its three rules, having no guide yet); VIII keeps only what /pb-cycle and the Non-Negotiables BEACON do not already carry. Removes a duplicated non-negotiables list, an ASCII cycle diagram, a Make-specific gate block and a redundant quick-reference table. 303 -> 257 lines. v1.2.0: Add the Register section -- how authored output reads (minimal sufficient, humble-best, peer-to-peer), covering code, comments and prose, deferring to a project register where one exists, with a falsifiable delete-and-ask test. Fix two defects: the [Country] placeholder shipped as a standard, and an unpunctuated docs rule that could not be parsed. v1.1.0: Added Calm Quality Bar to MLP criteria (playbook v2.12.0)."
breaking_changes: []
---
# Project Guidelines & Working Principles

**See `/pb-preamble` and `/pb-design-rules` first.** These standards assume you're operating from both mindsets:
- **Preamble**: Challenge assumptions, prefer correctness over agreement, think like peers
- **Design Rules**: Build systems that are clear, simple, modular, robust, and extensible

**Resource Hint:** sonnet - Practical standards reference; implementation-level guidance.

## When to Use

- Setting up project conventions for a new codebase
- Reviewing code against quality and collaboration standards
- Resolving disagreements about coding practices or workflow norms
- Onboarding team members to working principles

---

## I. Collaboration & Decision Making

### Decision Making
* **Always Ask Clarifying Questions** when input is needed. If a task takes longer than 4 hours to spec out, it requires synchronous discussion.
* **Present Available Options** with clear **Pros/Cons** to enable informed choices.
* **Make Informed Choices Together:** No assumptions without discussion.
* **Document Key Decisions (ADR):** Use the **Architecture Decision Record** format to capture the rationale behind major choices (Decisions as Code).

### Communication Style
* **Be Concise but Thorough:** Explain trade-offs clearly and surface ambiguities early.
* **Asynchronous First:** Use issue tracking for standard tasks; reserve synchronous meetings for high-stakes decisions.
* **Propose Recommendations** but defer to user/stakeholder judgment on final direction.

---

## II. Strategic Focus & Scope Management

### Project Motivation & North Star
* **Consult `project-description.md`:** This is the single source of truth for scope. Any feature must directly serve the documented goals.
* **Goal:** Deliver a **clean, practical, self-contained solution** demonstrating strong backend engineering and production-ready architecture.
* **Anti-Bloat Principle (YAGNI):** Focus on real value. Do not implement features or abstract solutions for problems that do not exist yet. **Over-engineering is technical debt.**

### Target Market & Localization
* **Name the primary userbase and ecosystem explicitly, then design for it.** A project serving one region, regulatory regime, or device class has different defaults than a global one. Record the choice where scope lives; unstated assumptions about the user are the ones that survive longest unchallenged.

### Working Memory & Development Control
* **Todos are Dev-Only:** The `todos/` folder is for development notes only and must be `.git-ignored`. Never commit temporary files.
* **Do not add published docs unprompted.** Anything landing in `docs/` is a tracked artifact and needs confirmation. Status reports, working notes and draft ADRs belong in `todos/` until they are asked for.
* **Time-Boxed Prototyping:** Use temporary branches for experiments.
* **Task Output:** Each task or todo must result in demonstrably working, testable code.

---

## III. Quality Standards & Implementation

### Core Quality Standards
* **Maintainability Over Complexity:** Prefer clean, readable implementation. Code should be **easy to delete**.
* **DRY Principle:** Strictly adhere to **Don't Repeat Yourself** to minimize knowledge duplication.
* **Test Incrementally:** Write automated tests (Unit, Integration) concurrently with the code. No significant feature is complete without passing tests.
* **Commit Hygiene:** Commit small, logical units frequently. Use **Conventional Commit** format (e.g., `feat:`, `fix:`, `refactor:`) for clear history.

### Register: How Output Reads

Standards above govern *what* you produce. This governs *how it reads*, and it applies to everything you author: code, comments, commit messages, PRs, issues, docs, and user-facing prose.

**If the project maintains its own register, that register wins.** This is the default for projects that do not.

Three properties, in priority order:

* **Minimal sufficient.** Say what fully serves the reader, then stop. **Sufficiency is the floor, minimality is the ceiling, and the order matters:** omitting a load-bearing constraint is not minimal, it is wrong. Cutting a passenger word is minimal. When both are satisfied, stop writing.
* **Humble-best.** Do the best work you can without performing it. No self-congratulation, no hedging, no defensive over-explanation, no salesmanship. Confidence without display. The work carries itself or it does not.
* **Peer-to-peer.** The reader is a competent colleague who is short on time. Do not re-explain what the artifact already shows, do not condescend, do not sell.

**In code**, register is naming, function length, and structure. A codebase that reads like it is showing off fails this standard exactly as a comment that does.

**The test, so this is falsifiable rather than admirable:** delete any sentence, comment, or line and ask whether a competent reader now makes a worse decision. If not, it was a passenger and it goes. Apply it to your own output before shipping, not only in review.

**Failure modes, by name:** narration ("I examined...", "After analysis..."), restating the diff, severity adjectives standing in for evidence, closing summaries that repeat the opening, comments that argue a decision instead of naming a constraint, and prose that sells rather than states.

### Test Quality Standards
Tests should catch bugs, not chase coverage numbers.

**Test What Matters:**
* Error handling and edge cases
* State transitions and side effects
* Business logic and security-sensitive paths
* Integration points (API, storage)

**Avoid Low-Value Tests:**
* Static data validation (config, constants)
* Implementation details / re-implemented internal functions
* Every input permutation (use representative samples)
* Trivial code paths

**Maintain Test Health:**
* Prune low-value tests periodically
* Speed up slow tests with proper mocking
* Fix or quarantine flaky tests immediately

### Accessibility Standards
* **Keyboard First:** All interactive elements must work with keyboard (Enter/Space for actions)
* **Focus Management:** Modals trap focus; closing restores focus to trigger
* **ARIA Labels:** Icon-only buttons need `aria-label`; decorative icons use `aria-hidden`
* **Visible Focus:** Focus rings visible in both light and dark modes
* **Touch Targets:** Minimum 44x44px for mobile

---

## IV. Technology-Specific Standards

Stack-level guidance lives in its own playbook, so it can go deep without drifting from a summary kept here:

| Stack | Playbook |
|-------|----------|
| Go | `/pb-guide-go` |
| Python | `/pb-guide-python` |
| Frontend | `/pb-patterns-frontend` |
| APIs, async, data, resilience | `/pb-patterns-api`, `/pb-patterns-async`, `/pb-patterns-db`, `/pb-patterns-resilience` |

**Node.js has no dedicated guide yet**, so its three load-bearing rules stay here until one exists:

* **Never block the event loop.** `async/await` for all I/O.
* **Layer it:** controller, service, repository. Business logic never lives in middleware.
* **Centralize error handling**, set security headers, rate-limit at the edge.

---

## V. Live Documentation

### Principles
**`project-description.md` is a living document** and the authoritative manual.
* **Compact & Focused:** Document only significant decisions and rationale.
* **Actionable:** Future developers must understand the **"why,"** not just the "what."

### Mandatory Update Points
Update documentation after:
* **Key design decisions** are finalized.
* **Architecture changes** are implemented.
* **New components** are added.
* **Core patterns** are changed.
* **Major milestones** are completed.

---

## VI. Release Planning & Tracking

### Release Structure
Each release (v1.X.0) follows a structured approach:

```
todos/releases/v1.X.0/
├── 00-master-tracker.md    # Overview, success criteria, changelog
├── phase-1-*.md            # Detailed phase documentation
├── phase-2-*.md            # Tasks, verification, files to modify
└── ...
```

### Phase Documentation
Each phase doc includes:
* **Objective** - What and why
* **Tasks** - Specific work items with checkboxes
* **Verification** - How to confirm completion
* **Files to Modify** - Concrete list of changes
* **Rollback Plan** - How to undo if needed

### Iterative Workflow
1. **Plan** - Create master tracker and phase docs
2. **Implement** - Work through phases, update checkboxes
3. **Self-Review** - Verify against phase criteria
4. **Commit** - Logical commits after each task
5. **Update Tracker** - Mark phases complete, add changelog entries
6. **Deploy** - Tag release, deploy, verify

### Tracker Maintenance
* Update phase status as work progresses
* Add changelog entries for significant work
* Mark Definition of Done items when complete
* Document deferred items for next release

---

## VII. Quality Bar: Minimum Lovable

Design Rules tell you *how* to build. This tells you *when you're done*.

### The MLP Criteria

Before declaring work complete, ask:

- **Would you use this daily without frustration?** - Not just functional, but pleasant
- **Can you recommend it without apology?** - "It works, but..." means it's not done
- **Did you build the smallest thing that feels complete?** - Scope discipline, not scope creep

If any answer is "no": keep refining. If all are "yes": ship it.

### Calm Quality Bar (v2.12.0)

Extend the MLP criteria with attention-respect:

- **Does this respect user attention?** - Works silently? Alerts only when critical? Optional instead of mandatory?
- **Are errors clear and recoverable?** - User knows what went wrong and what to do next?
- **Does this fail gracefully?** - Does it degrade to partial functionality, or does it break completely?
- **Would you use this daily without thinking about it?** - Does it recede into the background?

See `/pb-calm-design` for the complete 10-question calm design checklist and philosophy.

### What MLP Is Not

- **Feature-rich** - MLP is about care, not quantity
- **Polished to perfection** - Good enough to love, not flawless
- **Over-engineered** - Simplicity is part of lovability

### The Mindset Shift

| MVP Thinking | MLP Thinking |
|--------------|--------------|
| "It works" | "It works well" |
| "We'll fix it later" | "We'll ship when it's ready" |
| "Users won't care" | "Would we use this?" |
| "Just an MVP" | "Is this lovable?" |

MLP is a discipline, not a milestone. Build less. Care more.

---

## VIII. SDLC Discipline

The cycle itself lives in `/pb-cycle` (develop, self-review, test, peer review, commit) and is entered by `/pb-start`, closed by `/pb-release`. What follows is only what those commands do not already carry.

**Quality gates.** Lint, typecheck and tests all pass before the work proceeds, every iteration, regardless of size. Wire them to one command the project already has; the runner is a project choice, the gate is not.

**Commit discipline.** One concern per commit, every commit deployable, conventional prefix, and **never `git add .`** -- stage the specific files that belong together. Commit after each meaningful unit of work, not at end of session.

**Command quality.** Every multi-step command carries a Definition of Done checklist. Execution gates on the boxes, not on a judgment that it feels done.

Non-negotiables (never ship known bugs, never skip testing, never ignore warnings) are stated once in the global CLAUDE.md Non-Negotiables BEACON and are not repeated here.

---

## Related Commands

- `/pb-preamble` - Collaboration philosophy (mindset)
- `/pb-design-rules` - Technical principles (clarity, simplicity, modularity)
- `/pb-guide` - Master SDLC framework
- `/pb-commit` - Atomic commit practices
- `/pb-testing` - Test patterns and strategies
