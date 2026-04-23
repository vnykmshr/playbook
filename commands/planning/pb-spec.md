---
name: "pb-spec"
title: "Implementation Spec: Detailed Plan from Resolved Sketch"
category: "planning"
difficulty: "advanced"
model_hint: "opus"
execution_pattern: "interactive"
related_commands: ['pb-plan', 'pb-sketch', 'pb-adr', 'pb-todo-implement', 'pb-start']
last_reviewed: "2026-04-23"
last_evolved: "2026-04-23"
version: "1.0.0"
version_notes: "v2.21.0: New skill. Extracted from pb-plan Phases 3-4, plus size-gate (small feature vs release cycle). Pairs with pb-sketch via pb-plan wrapper."
breaking_changes: []
---
# Implementation Spec: Detailed Plan from Resolved Sketch

Produces the committed, numbered implementation plan. Input: a sketch with resolved decision forks (from `/pb-sketch`) or equivalent clarity. Output: a plan document ready for `/pb-todo-implement` or manual execution.

**Resource Hint:** opus - Architect-tier work: scope-locking, phase sequencing, verification and rollback design.

**Tool-agnostic:** Spec framework (scope lock, phase breakdown, verification, rollback) works with any tool. Claude Code users invoke as `/pb-spec`. Using another tool? Read this file as Markdown for the framework. See [`/docs/using-with-other-tools.md`](/docs/using-with-other-tools.md).

---

## When to Use

- **After `/pb-sketch` with resolved forks** -- decisions are settled; turn them into numbered steps
- **Via `/pb-plan` wrapper** -- muscle memory; wrapper runs sketch → presents decisions → spec
- **When sketch is unnecessary** -- the approach is already obvious; skip sketch, spec directly
- **Before `/pb-todo-implement`** -- spec provides the structure that todo-implement executes

**Don't use for:**
- Plans that still have unresolved decision forks (run `/pb-sketch` first)
- Exploratory research (use `/pb-sketch` or `/pb-think`)

---

## Philosophy

**Foundation:** Assumes sketch-level clarity. The spec is the committed plan -- each phase should be independently shippable, verifiable, and rollback-safe.

### Core Principles

1. **Lock scope before specifying** - Scope lock comes first. Without it, the spec drifts.
2. **Atomic phases** - Each phase is one concern. One commit's worth of work or a tight sequence of related commits.
3. **Verification per phase** - Each phase says how to know it worked. "Passes tests" is not enough -- name the tests, or the manual check, or the output signal.
4. **Rollback per phase** - Each phase says how to undo. Most rollbacks are `git revert <sha>`; some need data migrations or config reverts.
5. **Size-gate the output** - A 2-file bugfix doesn't need a release tracker. Match the spec artifact to the work.

---

## Phase 1: Scope Lock (always run)

Before writing steps, lock scope explicitly. This guards against drift during implementation.

### Scope Lock Checklist

- [ ] Focus area clearly defined in one sentence
- [ ] Success criteria are measurable and agreed
- [ ] Out-of-scope items explicitly listed
- [ ] Risks identified with mitigations
- [ ] Phases ordered by priority (do P1 first, P3 can be cut)
- [ ] Each phase is independently shippable
- [ ] Stakeholders aligned on scope (or noted as solo work)

### Scope Lock Statement

```
v[X.Y.Z] - [Theme]

Goal: [One sentence description of what we're achieving]

In Scope:
- [Specific item 1]
- [Specific item 2]

Out of Scope:
- [Explicit exclusion 1]
- [Explicit exclusion 2]

Success Criteria:
- [Measurable outcome 1]
- [Measurable outcome 2]

Signed off by: [Names/roles or "solo"]
Date locked: [Date]
```

**Do not proceed to step-writing until scope is locked.**

---

## Phase 2: Size Gate

Match the spec artifact to the work. Two paths:

### Path A: Small Feature / Bugfix

**When:** single concern, 1-3 files, one or two commits, no release cycle

**Output:** single file at `plan/{generated-kebab-case-name}.md` using the **Single-Plan Template** below.

### Path B: Release Cycle / Multi-Phase Work

**When:** multiple phases, >3 files, shippable over several sessions, release versioning involved

**Output:** directory scaffold at `todos/releases/vX.Y.Z/` using the **Release Scaffold** below.

### Size Signals (pick path by gut; don't over-index)

| Signal | Path A | Path B |
|---|---|---|
| Lines of code | <200 | 200+ |
| Files touched | 1-3 | 4+ |
| Commits expected | 1-2 | 3+ |
| Independent phases | 1 | 2+ |
| Release tag | no | likely yes |
| Multiple sessions | no | yes |

**When in doubt, start Path A.** Promote to Path B if the spec outgrows it. Don't scaffold a release tracker for a two-file fix.

---

## Phase 3: Write the Spec

### Path A: Single-Plan Template

Write to `plan/{name}.md`:

```markdown
# Plan: {Title}

**Created:** {YYYY-MM-DD}
**Scope Lock:** locked {YYYY-MM-DD}
**Sketch:** (optional) `sketch/{name}.md`

## Goal

{One sentence from Scope Lock.}

## Scope

**In:** {bullet or inline list}
**Out:** {bullet or inline list}

## Approach

{2-4 sentences. Reference resolved forks from sketch if applicable.}

## Steps

1. **{Step name}** -- {what, where, why}
   - Files: `{path}`
   - Action: {edit/create/delete}
2. **{Step name}** -- {...}
3. **{Step name}** -- {...}

## Verification

- [ ] {How to confirm step 1 worked -- test name, command output, manual check}
- [ ] {...}

## Rollback

{git revert, or specific steps if more involved}

## Notes

{design decisions, trade-offs, out-of-band references -- keep short}
```

### Path B: Release Scaffold

Directory structure:

```
todos/releases/vX.Y.Z/
├── 00-master-tracker.md    # Overview, phases, checkpoints, CURRENT STATUS
├── phase-1-{slug}.md       # Detailed phase 1 tasks
├── phase-2-{slug}.md       # Detailed phase 2 tasks
├── done/                   # Completed phases (archived)
└── ...
```

#### Context-Efficient Plan Structure

Plans get loaded into conversation context. Structure them for **resumability without full reload**:

1. **Current state at top** - What phase, what's done, what's next
2. **Completed work collapsed** - Move done phases to `done/` or bottom of master-tracker
3. **Active phase expanded** - Only current phase needs full detail
4. **Scope lock is permanent** - Don't repeat in every session

**Anti-pattern:** Full plan in every session consumes context for work already done.
**Pattern:** Master tracker with current status + pointer to active phase file.

#### Master Tracker Template

```markdown
# vX.Y.Z - [Release Theme]

## Current Status (Update Each Session)

**Phase:** [N] - [Name]
**Last commit:** [hash] - [date]
**Next:** [Specific next task]

> Entry point. Update each session so resuming is instant.

---

## Overview

[One paragraph: what, why, expected outcome]

**Tier:** [S/M/L] - [Brief justification]
**Focus:** [Primary focus area]

---

## Scope Lock

**Goal:** [One sentence]

**In Scope:**
- [Item]

**Out of Scope:**
- [Item]

**Success Criteria:**
- [Measurable outcome]

---

## Phases

| Phase | Focus | Priority | Status |
|-------|-------|----------|--------|
| 1 | [Name] | P1 | pending |
| 2 | [Name] | P2 | pending |

---

## Checkpoints

| Gate | After | Sign-off | Status |
|------|-------|----------|--------|
| Scope Lock | Planning | [Who] | pending |
| Ready for QA | Implementation | [Who] | pending |
| Ready for Release | QA | [Who] | pending |

---

## Changelog

| Date | Phase | Notes |
|------|-------|-------|
| YYYY-MM-DD | - | Initial planning |
```

#### Phase Document Template

```markdown
# Phase N: [Name]

## Overview

[What this phase achieves]
**Effort:** [Estimate range]
**Priority:** [P1/P2/P3]

---

## Tasks

### Task 1: [Name]

**Problem:** [What's wrong or missing]
**Solution:** [What we'll do]
**Files:** [Specific file:line references]

**Acceptance Criteria:**
- [ ] [Specific, verifiable outcome]

---

## Verification

- [ ] [How to verify changes work]
- [ ] [Tests that must pass]

---

## Rollback

[How to undo if needed]
```

---

## Verification Design (applies to both paths)

Each phase (or step in Path A) needs a verification signal. Weak → Strong:

| Weak | Strong |
|---|---|
| "Tests pass" | "`pytest tests/auth/ -k test_login` passes" |
| "It works" | "`curl /api/v1/users/1` returns 200 with expected fields" |
| "No regressions" | "Full suite runs green; manually verified flows: login, signup, password reset" |
| "Code reviewed" | "Self-reviewed; run `/pb-review`; no open issues" |

**Rule:** If verification is a sentence, it's not verification. Name the test, the command, or the signal.

---

## Rollback Design (applies to both paths)

Every phase (or step in Path A) needs a rollback path.

**Common rollbacks (cheap):**
- `git revert <sha>` for code-only changes
- `git reset --hard <sha>` before push (destructive -- requires explicit approval)
- Config revert: restore previous `.env` or settings value

**Expensive rollbacks (require explicit plan):**
- Database migrations: need a reverse migration
- Third-party API changes: need a rollback call or feature flag
- User-visible changes: need communication plan

**Rule:** If rollback is expensive, say so in the spec and design a feature flag or phased release.

---

## Hand-off to Implementation

Spec is complete when:
- [ ] Scope lock signed
- [ ] Size gate decided (Path A or Path B)
- [ ] All steps/tasks written with files and actions
- [ ] Verification defined per step/phase
- [ ] Rollback defined per step/phase
- [ ] File(s) saved at the correct location

Then invoke `/pb-todo-implement` (or execute manually). For very small changes, the spec itself may be the commit message draft.

---

## Red Flags in Spec Writing

### Spec Bloat

- Spec longer than the code change it produces.
- **Response:** collapse steps, shorten descriptions, trust the reader.

### Missing Verification

- Every step says "tests pass" verbatim.
- **Response:** name the test, the command, or the signal.

### Missing Rollback

- "If it breaks, we'll figure it out."
- **Response:** at minimum `git revert <sha>`. Expensive rollbacks need explicit plans.

### Scope Creep in the Spec Itself

- "While writing this step, I realized we should also..."
- **Response:** add to backlog. Reopen scope lock explicitly if genuinely required.

### Wrong Size Path

- Release tracker scaffold for a two-file fix.
- **Response:** demote to Path A. Release scaffold is for multi-phase work.

---

## SDLC Notes

### Planning Discipline

- **Break work into phases** - Each phase independently shippable
- **Order by priority** - P1 first, P3 can be cut
- **Size tasks for single sessions** - If a task takes multiple days, break it down

### Implementation Discipline

- **One concern per commit** - Atomic changes are easier to review and revert
- **Verify as you go** - Run verification after each step, not at the end
- **Update docs alongside code** - Stale docs are worse than no docs
- **Delete aggressively** - Unused code is a liability

### Testing Priorities

1. Critical paths users depend on
2. Edge cases that have caused bugs
3. Complex logic that's easy to break
4. Integration points with external systems

Skip: trivial getters/setters, framework code, tests that duplicate what the code says.

---

## Related Commands

- `/pb-plan` - Orchestrating wrapper; runs decide then hands a resolved sketch to this skill.
- `/pb-sketch` - Produces the resolved sketch this skill consumes.
- `/pb-adr` - Document architecture decisions for significant forks.
- `/pb-todo-implement` - Executes the spec phase-by-phase with commits.
- `/pb-start` - Alternate entry point for beginning work from a spec.
