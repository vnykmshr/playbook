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
