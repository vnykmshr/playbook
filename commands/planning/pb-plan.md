# New Focus Area Planning Prompt (Generic)

A reusable prompt for planning release focus areas across any project. Emphasizes **alignment before implementation**, **surgical execution**, and **meaningful outcomes over busywork**.

---

## Philosophy

**Foundation:** This planning assumes `/pb-preamble` thinking (transparent reasoning, peer challenge) and `/pb-design-rules` thinking (clarity, simplicity, modularity).

Clarify means asking hard questions and challenging assumptions. Align means surfacing disagreement early—especially about design. Do not skip this phase to appear productive. Time spent here saves weeks later.

### Core Principles

1. **Clarify, Don't Assume** - When in doubt, ask. Assumptions compound into wasted work.

2. **Align Before You Build** - Full agreement on scope, approach, and success criteria before writing code. Misalignment mid-implementation is expensive.

3. **Surgical Execution** - Make the smallest change that achieves the goal. Every line added is a line to maintain.

4. **Avoid Bloat, Promote Reuse** - Before writing new code, ask: "Does this already exist? Can I extend something?"

5. **Tests That Matter** - Write tests that catch real bugs and prevent regressions. Coverage numbers mean nothing if tests don't exercise meaningful behavior.

6. **Do Less, Better** - A focused release that ships completely is better than an ambitious release that ships partially.

---

## Phase 1: Discovery

### Before Any Analysis

Start by gathering context. Do not proceed until these questions are answered:

#### 1. What Problem Are We Solving?

```
- What is the user/business problem?
- Why now? What's the trigger for this work?
- What happens if we don't do this?
- Is this the right solution, or are there alternatives?
```

#### 2. What Are the Boundaries?

```
- What is explicitly IN scope?
- What is explicitly OUT of scope?
- Are there dependencies on other work?
- Are there time-sensitive constraints (not estimates, but hard deadlines)?
```

#### 3. What Freedom Do We Have?

```
- Can we make breaking changes to APIs/interfaces?
- Can we refactor existing code?
- Can we change data models/schemas?
- Can we update/remove dependencies?
- Can we delete unused code?
```

#### 4. How Will We Know We're Done?

```
- What are the acceptance criteria?
- Are there measurable success metrics?
- Who signs off on completion?
- What does "good enough" look like vs. "perfect"?
```

**Stop here if any answers are unclear.** Use clarifying questions to resolve ambiguity before proceeding.

---

## Phase 2: Multi-Perspective Analysis

Examine the focus area from multiple angles. The goal is to **surface hidden complexity** and **identify the minimal path forward**.

### Engineering Perspective

| Question | Why It Matters |
|----------|----------------|
| What existing code changes? | Understand blast radius |
| What new code is needed? | Estimate scope |
| What can we delete? | Reduce maintenance burden |
| What can we reuse? | Avoid reinventing |
| What are the risks/unknowns? | Plan for contingencies |

### Architecture Perspective

| Question | Why It Matters |
|----------|----------------|
| Does this change system boundaries? | Affects integration points |
| Are there scalability implications? | Avoid painting into corners |
| Does this add new dependencies? | Dependencies are liabilities |
| Is this consistent with existing patterns? | Consistency aids maintainability |

### Product Perspective

| Question | Why It Matters |
|----------|----------------|
| Who benefits and how? | Validates the work |
| What's the user-facing impact? | Prioritize visible value |
| What documentation is needed? | Users need to know about changes |
| Does this align with product direction? | Avoid orphaned work |

### Operations Perspective

| Question | Why It Matters |
|----------|----------------|
| Does deployment change? | Affects release process |
| Are there monitoring needs? | You can't fix what you can't see |
| What's the rollback plan? | Always have an escape hatch |
| Performance implications? | Avoid surprise degradation |

---

## Phase 3: Scope Locking

Before implementation, explicitly lock scope:

### Scope Lock Checklist

- [ ] Focus area clearly defined in one sentence
- [ ] Success criteria are measurable and agreed
- [ ] Out-of-scope items explicitly listed
- [ ] Risks identified with mitigations
- [ ] Phases ordered by priority (do P1 first, P3 can be cut)
- [ ] Each phase is independently shippable
- [ ] Stakeholders aligned on scope

### Scope Lock Statement

Write a clear statement:

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

Signed off by: [Names/roles]
Date locked: [Date]
```

**Do not proceed to implementation until scope is locked.**

---

## Phase 4: Release Documentation

Create structured documentation for tracking and execution.

### Directory Structure

```
todos/releases/vX.Y.Z/
├── 00-master-tracker.md    # Overview, phases, checkpoints
├── phase-1-*.md            # Detailed phase 1 tasks
├── phase-2-*.md            # Detailed phase 2 tasks
└── ...
```

### Master Tracker Template

```markdown
# vX.Y.Z - [Release Theme]

## Overview

[One paragraph: what, why, expected outcome]

**Tier**: [S/M/L] - [Brief justification]
**Focus**: [Primary focus area]

---

## Scope Lock

**Goal**: [One sentence]

**In Scope**:
- [Item]

**Out of Scope**:
- [Item]

**Success Criteria**:
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

### Phase Document Template

```markdown
# Phase N: [Name]

## Overview

[What this phase achieves]
**Effort**: [Estimate range]
**Priority**: [P1/P2/P3]

---

## Tasks

### Task 1: [Name]

**Problem**: [What's wrong or missing]
**Solution**: [What we'll do]
**Files**: [Specific file:line references]

**Acceptance Criteria**:
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

## SDLC Best Practices

### Planning

- **Break work into phases** - Each phase should be independently shippable
- **Order by priority** - P1 first, P3 can be cut if needed
- **Size tasks for single sessions** - If a task takes multiple days, break it down
- **Document decisions** - Future you (or someone else) will thank you

### Implementation

- **One concern per commit** - Atomic changes are easier to review and revert
- **Verify as you go** - Run tests after each change, not at the end
- **Update docs alongside code** - Stale docs are worse than no docs
- **Delete aggressively** - Unused code is a liability, not an asset

### Testing

**Write tests that matter:**

| Good Test | Bad Test |
|-----------|----------|
| Tests user-facing behavior | Tests implementation details |
| Catches real bugs | Chases coverage numbers |
| Runs fast, fails clearly | Slow, flaky, cryptic failures |
| Documents expected behavior | Duplicates what code already says |

**Test priority:**
1. Critical paths users depend on
2. Edge cases that have caused bugs
3. Complex logic that's easy to break
4. Integration points with external systems

**Skip:**
- Trivial getters/setters
- Framework code (test your code, not React)
- Tests that just assert the code does what the code does

### Code Changes

**Before adding code, ask:**
- Can I solve this by removing code instead?
- Does something similar already exist?
- Is this the simplest solution?
- Will this be easy to delete later if wrong?

**Before adding dependencies:**
- Is this dependency actively maintained?
- What's the size/complexity tradeoff?
- Can I use what's already installed?
- What happens if this dependency dies?

### Review & Merge

- **Small PRs merge faster** - 200 lines reviewed well beats 2000 lines skimmed
- **Describe the "why"** - Code shows what, PR description explains why
- **Address feedback promptly** - Stale PRs are merge-conflict magnets
- **Verify in production** - Your job isn't done until it works in prod

---

## Execution Mindset

### Surgical Precision

```
[NO] "While I'm here, I'll also refactor this other thing"
[YES] "This change does exactly one thing: [X]"

[NO] "Let me add comprehensive error handling everywhere"
[YES] "This endpoint needs validation because users hit this error"

[NO] "We should add tests for all the things"
[YES] "This specific behavior broke before, adding a regression test"
```

### Scope Discipline

```
[NO] "This is related, so let's include it"
[YES] "That's valuable, but out of scope. Adding to backlog."

[NO] "We might need this later"
[YES] "We'll add it when we need it"

[NO] "Let's make it configurable"
[YES] "Let's hardcode the only value we use"
```

### Progress Over Perfection

```
[NO] Wait for perfect solution
[YES] Ship good-enough solution, iterate

[NO] Batch all improvements into one release
[YES] Ship improvements incrementally

[NO] Plan for every edge case upfront
[YES] Handle edge cases when they occur
```

---

## Usage Examples

### Starting a New Focus Area

```
I want to plan a new focus area: [DESCRIPTION]

Context:
- Project: [Name and brief description]
- Current state: [Relevant background]
- Trigger: [Why this work, why now]

Constraints:
- [Any hard requirements or limitations]
- [Dependencies or blockers]

Freedom level:
- [Can we make breaking changes?]
- [Can we refactor/delete existing code?]

Please:
1. Ask clarifying questions before making assumptions
2. Conduct multi-perspective analysis
3. Propose phases with clear priorities
4. Prepare release documentation structure
```

### Clarifying Before Proceeding

```
Before we continue, I need to clarify:

1. [Specific question about scope]
2. [Specific question about constraints]
3. [Specific question about success criteria]

Please answer these so we can lock scope and proceed.
```

### Locking Scope

```
Based on our discussion, here's the proposed scope lock:

Goal: [One sentence]

In Scope:
- [Specific item]

Out of Scope:
- [Explicit exclusion]

Success Criteria:
- [Measurable outcome]

Do you agree with this scope? Any adjustments before we proceed?
```

### Resuming Work

```
Continuing work on v[X.Y.Z] - [Theme]

Current status:
- Phase [N] is [in progress/blocked/complete]
- [Any context changes since last session]

Next: [What we're doing this session]
```

---

## Next Step: Implementation

After planning is complete and scope is locked, implement individual todos using **`/pb-todo-implement`**:

### When to Use `/pb-todo-implement`

Once you have:
- Scope locked
- Phases defined
- Todos broken down into concrete tasks

Then for each todo:

```
/pb-todo-implement
```

This workflow:
1. Analyzes codebase to find exactly what needs to change
2. Drafts implementation plan with specific file:line references
3. Guides implementation checkpoint-by-checkpoint
4. Commits changes with full audit trail
5. Maintains historical record of completed work

**Integration**: Plan → **Implement** → Self-Review → Peer Review → Commit/Release

---

## Red Flags to Watch For

### Scope Creep

- "While we're at it..."
- "It would be easy to also..."
- "Users might want..."
- "Future-proofing for..."

**Response**: "That's valuable. Let's add it to the backlog and keep this release focused."

### Analysis Paralysis

- "We need to research more options"
- "What if we're wrong about..."
- "Let's wait until we know..."

**Response**: "What's the smallest thing we can ship to learn if we're on the right track?"

### Gold Plating

- "It should also handle..."
- "Let's make it configurable..."
- "We should add comprehensive..."

**Response**: "Is this needed for the success criteria we defined? If not, it's out of scope."

### Missing Alignment

- "I thought we were doing X"
- "Wait, that's not what I meant"
- "Didn't we decide..."

**Response**: "Let's pause and re-align. What specifically are we trying to achieve?"

---

## Summary

1. **Clarify first** - Ask questions, don't assume
2. **Align fully** - Lock scope before implementation
3. **Plan meticulously** - Document phases, criteria, risks
4. **Execute surgically** - Smallest change that achieves the goal
5. **Test meaningfully** - Catch real bugs, not coverage numbers
6. **Ship incrementally** - Working software over comprehensive plans
7. **Delete liberally** - Less code is better code

---

## Related Commands

- `/pb-adr` — Document architectural decisions made during planning
- `/pb-todo-implement` — Implement individual todos from the planning phases
- `/pb-cycle` — Iterate through development with self-review and peer review
- `/pb-think` — Deep thinking for complex planning decisions
- `/pb-patterns-core` — Reference architectural patterns during design
