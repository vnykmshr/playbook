---
name: "pb-start"
title: "Start Development Work"
category: "development"
difficulty: "advanced"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-resume', 'pb-cycle', 'pb-commit', 'pb-plan', 'pb-standup']
last_reviewed: "2026-02-09"
last_evolved: ""
---
# Start Development Work

Begin iterative development on a feature, enhancement, or fix. This command establishes the rhythm for quality-focused, incremental work.

**Mindset:** Development assumes both `/pb-preamble` thinking (challenge assumptions, peer collaboration) and `/pb-design-rules` thinking. Each iteration verifies that code embodies Clarity, Simplicity, and Robustness.

**Resource Hint:** sonnet — routine development workflow orchestration

---

## When to Use

- Starting a new feature, enhancement, or bug fix from scratch
- Establishing branch strategy and iteration rhythm for a work item
- Onboarding to a codebase and need the full development ceremony

---

## Pre-Start Checklist

Before writing code, confirm:

- [ ] Scope is clear (what's in, what's out)
- [ ] Feature branch created from main
- [ ] Working context reviewed (see below)
- [ ] Acceptance criteria understood
- [ ] Team alignment: assumptions are explicit, disagreements surfaced (see `/pb-preamble`)
- [ ] **Outcomes clarified** (see section below) — Don't skip this
- [ ] Success criteria measurable (not vague)
- [ ] Approval path defined (who needs to approve before merging?)

---

## Outcome Clarification (Critical)

**Before writing a single line of code, define what success looks like.**

This prevents drift, scope creep, and surprises at review time.

### Step 1: Define the Outcome (Not the Solution)

**Bad (solution-focused):**
- "Refactor the payment service to use async/await"
- "Add dark mode toggle to UI"

**Good (outcome-focused):**
- "Payment processing latency < 500ms under peak load"
- "40% of users who use app at night have a way to reduce eye strain"

The difference: Outcomes define what success looks like. Solutions are how you achieve it.

### Step 2: Define Success Criteria (Measurable)

For the outcome above, what proves you succeeded?

**Payment example:**
- [ ] P95 latency ≤ 500ms (measured in production)
- [ ] No performance degradation vs current async/await version
- [ ] All existing tests pass
- [ ] Load test to 10k requests/min shows consistent latency

**Dark mode example:**
- [ ] Dark mode toggle present in settings
- [ ] All UI components render correctly in dark mode
- [ ] User preference persists across sessions
- [ ] Accessibility contrast ratios maintained in dark mode

**Anti-pattern:** "Code compiles" or "tests pass" (these are prerequisites, not outcomes)

### Step 3: Define the Approval Path

Who needs to approve this work before it ships?

**Example approval workflow:**
1. **Self-review (you)** — Does code match the planned approach?
2. **Peer review (Linus/Alex/Maya/etc)** — Is design sound? Are assumptions valid?
3. **Product approval (if needed)** — Does this solve the problem we committed to?
4. **QA verification (if needed)** — Do success criteria pass?

**Document this upfront.** Prevents "surprise denials" at the end.

### Step 4: Identify Blockers

What could prevent you from achieving the outcome?

**Examples:**
- "Need database access to staging environment"
- "Waiting on API from third-party service"
- "Need design approval from team lead"

**If blockers exist, resolve them now.** Don't start coding with unknown blockers.

### Step 5: Define the Definition of Done

What does "finished" look like? Be specific.

**Bad:** "Implement the feature"
**Good:**
- Code is written and tested
- Success criteria are verified
- Documentation is updated
- PR is reviewed and approved
- Deployed to staging and verified
- Ready to merge to main

### Outcome Documentation Template

Create `todos/work/[task-date]-outcome.md`:

```markdown
# [Task Name] — Outcome Clarification

## Outcome
[What success looks like, not how to achieve it]

## Success Criteria
- [ ] [Measurable criterion 1]
- [ ] [Measurable criterion 2]
- [ ] [Measurable criterion 3]

## Approval Path
1. Self-review (author)
2. Peer review (Linus agent for security-critical)
3. [Product approval / QA verification / etc]

## Blockers & Dependencies
- [Blocker 1 and resolution plan]
- [Dependency 2 and timeline]

## Definition of Done
- [ ] Code written and tested
- [ ] Success criteria verified
- [ ] Docs updated
- [ ] PR reviewed and approved
- [ ] Ready to merge

## Notes
[Any assumptions, trade-offs, or context]
```

---

## Working Context Check

Before starting work, check if the project has a working context document:

```bash
# Check for working context (location and naming may vary)
ls todos/*working-context*.md 2>/dev/null
```

**Common locations:** `todos/working-context.md`, `todos/1-working-context.md`

If working context exists:
1. **Review it** — Understand current version, active development, recent commits
2. **Verify currency** — Compare version with `git describe --tags`
3. **Update if stale** — Run `/pb-context` to refresh if outdated

If no working context exists:
- For established projects, consider creating one using `/pb-context`
- For small tasks, `/pb-standards` provides sufficient context

---

## Branch Strategy

```bash
# For features (new functionality)
git checkout -b feature/v1.X.0-short-description main

# For fixes (bug repairs)
git checkout -b fix/short-description main

# For refactors (no behavior change)
git checkout -b refactor/short-description main
```

**Naming Convention:**
- Features: `feature/v1.X.0-topic` (tied to release version)
- Fixes: `fix/issue-description`
- Refactors: `refactor/what-changed`

---

## Iteration Cycle

See `/pb-cycle` for the full iteration workflow (develop, self-review, test, peer review, commit, update tracker).

---

## Commit Discipline

See `/pb-commit` for atomic commit practices, staging discipline, and message format.

---

## Quality Gates (Check After Each Iteration)

Before moving to next task:

```bash
make lint        # Lint check passes
make typecheck   # Type check passes
make test        # All tests pass
```

**If any gate fails, fix before proceeding. Never accumulate debt.**

---

## Tests That Matter

Write tests alongside code, not after. Focus on:

**DO Test:**
- Error handling and edge cases
- State transitions and side effects
- Business logic and calculations
- Integration points (API, storage)
- Security-sensitive paths

**DON'T Test:**
- Static data (configs, constants)
- Implementation details
- Every input permutation
- Trivial getters/setters

**Goal:** Tests catch real bugs, not chase coverage numbers.

---

## Feature Branch Hygiene

**During development:**
- Keep branch up to date with main
- Resolve conflicts early and often
- Push regularly (enables collaboration, backup)

**Before PR:**
- Squash WIP commits into logical units
- Ensure all quality gates pass
- Self-review one final time

---

## When to Ask for Help

Stop and ask when:
- Requirements are ambiguous
- Approach has multiple valid options
- Change impacts architecture
- Stuck for >30 minutes
- Scope seems to be growing

**Don't guess. Don't assume. Ask.**

---

## Quick Reference

| Action | Command |
|--------|---------|
| Start iteration cycle | `/pb-cycle` |
| Check quality gates | `make lint && make typecheck && make test` |
| Self-review checklist | See `/pb-cycle` |
| Create PR | `/pb-pr` |
| Make release | `/pb-release` |

---

## Session Start Template

When resuming work:

```
Resuming development on [branch-name]

Current status:
- [x] Task 1 complete
- [ ] Task 2 in progress - [specific status]
- [ ] Task 3 pending

Next: [What I'm doing this session]
```

---

## Related Commands

- `/pb-resume` — Get back into context after a break
- `/pb-cycle` — Self-review and peer review during development
- `/pb-commit` — Craft atomic, well-explained commits
- `/pb-plan` — Plan new features before starting work
- `/pb-standup` — Post async status updates to team

---

*Every iteration deserves the full cycle. Quality over speed.*
