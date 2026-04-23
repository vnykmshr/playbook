---
name: "pb-plan"
title: "New Focus Area Planning Prompt (Wrapper)"
category: "planning"
difficulty: "advanced"
model_hint: "opus"
execution_pattern: "interactive"
related_commands: ['pb-sketch', 'pb-spec', 'pb-adr', 'pb-todo-implement', 'pb-think', 'pb-start']
last_reviewed: "2026-04-23"
last_evolved: "2026-04-23"
version: "2.0.0"
version_notes: "v2.21.0: Rewrite as orchestrator. Delegates to /pb-sketch (decision forks) + /pb-spec (detailed plan). Preserves muscle memory: typing /pb-plan still produces end-to-end plan."
breaking_changes:
  - "Content moved out of this file. /pb-plan no longer contains Phase 1-4 framework; it orchestrates /pb-sketch and /pb-spec. Direct readers looking for the discovery/analysis framework: see /pb-sketch. Direct readers looking for scope-lock/release-doc templates: see /pb-spec."
---
# New Focus Area Planning Prompt (Wrapper)

`/pb-plan` is the muscle-memory entry point for planning a focus area. It orchestrates two focused skills: `/pb-sketch` (surface unknowns + enumerate decision forks) and `/pb-spec` (write the detailed plan from resolved decisions).

**Resource Hint:** opus - Architect-tier reasoning required by both sub-skills.

**Tool-agnostic:** This wrapper works with any tool. Claude Code users invoke as `/pb-plan`. Using another tool? Read `/pb-sketch` and `/pb-spec` directly and sequence them yourself.

---

## Why a Wrapper

Planning is two jobs, not one:

1. **Sketch job:** What's the problem, what are the forks, which option do we recommend? Exploratory. Research unstable facts. Enumerate decision points.
2. **Spec job:** Given resolved decisions, what are the numbered steps, verification, and rollback? Committed. Named artifacts.

When planning conflates these, the plan gets written around the first viable approach instead of the best one. Splitting them forces decisions to happen *before* step-writing.

The wrapper preserves muscle memory: `/pb-plan` still produces an end-to-end plan. Advanced users can call `/pb-sketch` or `/pb-spec` directly when they want one half of the work.

---

## Workflow

### Step 1: Discover context

Ask the user (or confirm from provided context):
- What's the focus area?
- What's the trigger (why now)?
- Any constraints or boundaries already known?

If the user has done `/pb-start` or similar, context may already be loaded. Don't re-ask.

### Step 2: Run `/pb-sketch`

Invoke `/pb-sketch` with the focus area. This produces:
- A sketch file at `sketch/{name}.md`
- Decision Forks (2-4 options per fork, recommended tagged)
- Recommended picks (copy/paste line)

Read the sketch output. If it says "No genuine forks," skip to Step 4.

### Step 3: Present decisions to user

Print the Decision Forks block. Ask:

> Confirm recommended picks `{label-list}`, or override with specific labels. Type the labels (e.g., `1-a, 2-b`) or `default` to accept recommendations.

Wait for user response. Update the sketch's `Recommended Picks` line with the resolved labels. Mark sketch status: `decisions resolved`.

### Step 4: Run `/pb-spec`

Invoke `/pb-spec` with the resolved sketch. This produces:
- **Path A (small feature):** single file at `plan/{name}.md`
- **Path B (release cycle):** directory at `todos/releases/vX.Y.Z/`

Hand off the plan path to the user.

### Step 5: Confirm completion

Print the plan path(s). Suggest the next command:
- For small features: `/pb-todo-implement` or manual execution
- For release cycles: `/pb-start` on the first phase, or direct `/pb-todo-implement`

---

## When NOT to Wrap

Use the sub-skills directly when:

- **You already know the approach** - skip `/pb-sketch`; invoke `/pb-spec` with a brief description or minimal sketch file.
- **You're exploring without committing** - use `/pb-sketch` standalone. Don't write the spec until you're ready to commit.
- **You need to re-plan one phase** - invoke `/pb-spec` on the existing sketch with the changed fork decision.
- **The work is a one-liner** - skip planning entirely; just do it.

---

## Core Principles (shared across sub-skills)

1. **Clarify, don't assume** - Assumptions compound into wasted work.
2. **Align before you build** - Full agreement on scope before implementation.
3. **Surgical execution** - Smallest change that achieves the goal.
4. **Do less, better** - A focused release that ships beats an ambitious release that partially ships.

Full framework lives in `/pb-sketch` (discovery + decisions) and `/pb-spec` (scope lock + steps + verification + rollback).

---

## Resumption

If the user invokes `/pb-plan` on a focus area that already has a sketch or spec:

- **Sketch exists, decisions unresolved:** jump to Step 3 (present decisions).
- **Sketch exists, decisions resolved, no spec:** jump to Step 4 (run `/pb-spec`).
- **Spec exists:** confirm and suggest next action (implement, re-plan a phase, or start over).

Don't re-run sketch on existing resolved work.

---

## Red Flags

### Sketch skipped when forks existed

- **Signal:** spec has ambiguity about approach mid-way through implementation.
- **Response:** stop, run `/pb-sketch` on the ambiguous area, resolve, update spec.

### Decisions collapsed in wrapper

- **Signal:** wrapper auto-picks without asking, user disagreed later.
- **Response:** always surface the Decision Forks block verbatim unless running in an explicit non-interactive mode (e.g., automation wrapper that auto-picks recommendations).

### Wrapper used when sub-skill would be clearer

- **Signal:** users say "I just wanted the forks, not the whole plan."
- **Response:** point them at `/pb-sketch` directly.

---

## Related Commands

- `/pb-sketch` - Decision forks, bounded research, recommended picks. Step 2 of this wrapper.
- `/pb-spec` - Detailed implementation plan with size-gate. Step 4 of this wrapper.
- `/pb-adr` - Document architecture decisions formally for significant forks.
- `/pb-think` - Deep thinking when forks themselves are ambiguous.
- `/pb-start` - Alternate entry point; begins work from a plan.
- `/pb-todo-implement` - Executes a plan phase-by-phase with commits.
