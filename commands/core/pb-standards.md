# Project Guidelines & Working Principles

**See `/pb-preamble` and `/pb-design-rules` first.** These standards assume you're operating from both mindsets:
- **Preamble**: Challenge assumptions, prefer correctness over agreement, think like peers
- **Design Rules**: Build systems that are clear, simple, modular, robust, and extensible

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
* The **primary userbase and workflow is [Country]-centric**. All design decisions must prioritize the local ecosystem requirements.

### Working Memory & Development Control
* **Todos are Dev-Only:** The `todos/` folder is for development notes only and must be `.git-ignored`. Never commit temporary files.
* **Never add new docs** Anything published to docs/ must be confirmed, status report, working docs, ADR can be saved to todos/ for local reviews.
* **Time-Boxed Prototyping:** Use temporary branches for experiments.
* **Task Output:** Each task or todo must result in demonstrably working, testable code.

---

## III. Quality Standards & Implementation

### Core Quality Standards
* **Maintainability Over Complexity:** Prefer clean, readable implementation. Code should be **easy to delete**.
* **DRY Principle:** Strictly adhere to **Don't Repeat Yourself** to minimize knowledge duplication.
* **Test Incrementally:** Write automated tests (Unit, Integration) concurrently with the code. No significant feature is complete without passing tests.
* **Commit Hygiene:** Commit small, logical units frequently. Use **Conventional Commit** format (e.g., `feat:`, `fix:`, `refactor:`) for clear history.

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

### A. Go (Microservices & High Performance)
* **Concurrency:** Use `sync.WaitGroup` and `context` to manage Goroutine lifecycles. Prevent leaks.
* **Error Handling:** Use `errors.Is` and `errors.As`. **Do not use panic** for expected runtime errors. Wrap errors with context.
* **Architecture:** Favor **Interfaces over concrete types** for dependency injection and testability.

### B. Node.js (APIs & Event-Driven)
* **Async/Await:** **Never block the Event Loop.** Always use `async/await` for I/O operations.
* **Separation of Concerns:** Use a layered structure (Controller-Service-Repository). Never put business logic in Express middleware.
* **Security:** Centralize error handling. Use libraries like Helmet for headers and implement rate limiting.

### C. Python (Data & Automation)
* **Environment:** Always use a **Virtual Environment** (`venv`) and lock files.
* **Typing:** Use **Type Hinting** extensively (e.g., `def func(x: int) -> bool:`) to improve readability and tooling support.
* **Frameworks:** Prefer lightweight frameworks (FastAPI, Flask) for microservices over monolithic structures.

### D. Frontend & Mobile Decisions
* **Styling:** Standardize on **Component-Based Styling** (CSS Modules, Styled Components, Tailwind). Avoid global stylesheets.
* **Data Fetching:** Use dedicated libraries (React Query, SWR) for API state management to handle caching and loading states automatically.

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

## VII. SDLC Discipline & Code Quality Commitment

### Our Commitment
We commit to **bug-free, rock-solid results** through disciplined adherence to a full Software Development Life Cycle. Every iteration, regardless of size, follows the same rigorous process. We do not cut corners.

### Development Workflow

**Start work:** `/pb-start` — Creates feature branch, establishes iteration rhythm

**Each iteration:** `/pb-cycle` — Guides through develop → self-review → peer review → commit

**Release:** `/pb-release` — Pre-release checks, deployment

### Iteration Cycle (Mandatory for All Changes)

```
┌─────────────────────────────────────────────────────────────┐
│  1. DEVELOP      Write code following standards             │
│         ↓                                                    │
│  2. SELF-REVIEW  Review your own changes critically         │
│         ↓                                                    │
│  3. TEST         Verify: lint, typecheck, tests pass        │
│         ↓                                                    │
│  4. PEER REVIEW  Get feedback on approach and quality       │
│         ↓                                                    │
│  5. COMMIT       Logical, atomic commit with clear message  │
└─────────────────────────────────────────────────────────────┘
```

**Run `/pb-cycle` for detailed checklists at each iteration.**

### Quality Gates

Run after each iteration:
```bash
make lint        # Lint check passes
make typecheck   # Type check passes
make test        # All tests pass
```

**All gates must pass before proceeding. Fix issues immediately.**

### Commit Discipline

* **One concern per commit** — Each commit addresses a single feature, fix, or refactor
* **Always deployable** — Every commit leaves the codebase working
* **Conventional format** — Use `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:` prefixes
* **Never use git add .** — Add specific files that belong together

**Commit timing:** After each meaningful unit of work, not at end of session.

### The Non-Negotiables

* **Never ship known bugs** — Fix or explicitly defer with ticket
* **Never skip testing** — Manual QA minimum, automated preferred
* **Never ignore warnings** — Warnings become bugs
* **Never "just push it"** — Every change deserves the full cycle

### Quick Reference

| Action | Command |
|--------|---------|
| Start development | `/pb-start` |
| Iteration cycle | `/pb-cycle` |
| Release prep | `/pb-release` |
| Full review | `/pb-review` |

---

## Related Commands

- `/pb-preamble` — Collaboration philosophy (mindset)
- `/pb-design-rules` — Technical principles (clarity, simplicity, modularity)
- `/pb-guide` — Master SDLC framework
- `/pb-cycle` — Development iteration loop
- `/pb-review-hygiene` — Code quality review
- `/pb-commit` — Atomic commit practices
- `/pb-testing` — Test patterns and strategies
