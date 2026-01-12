# Start Development Work

Begin iterative development on a feature, enhancement, or fix. This command establishes the rhythm for quality-focused, incremental work.

---

## Pre-Start Checklist

Before writing code, confirm:

- [ ] Scope is clear (what's in, what's out)
- [ ] Feature branch created from main
- [ ] Working context reviewed (`/pb-standards`)
- [ ] Acceptance criteria understood
- [ ] Team alignment: assumptions are explicit, disagreements surfaced (see `/pb-preamble`)

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

Every change follows this cycle without shortcuts:

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

**Run `/pb-cycle` for guided self-review and peer review at each iteration.**

---

## Commit Discipline

**One concern per commit:**
- Each commit addresses a single feature, fix, or refactor
- Every commit leaves the codebase in a working state
- Never batch unrelated changes into one commit

**Commit Message Format:**
```
<type>(<scope>): <subject>

<body - what and why>
```

**Types:** `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`

**Examples:**
```
feat(audio): add study mode section tracking

- SectionTrack component with labeled pipeline
- Progress calculation across sections
- Visual states: completed, current, upcoming

fix(auth): handle expired token redirect loop

- Check token expiry before redirect
- Clear stale tokens on 401 response
```

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

*Every iteration deserves the full cycle. Quality over speed.*
