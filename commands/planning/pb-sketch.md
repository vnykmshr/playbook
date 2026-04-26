---
name: "pb-sketch"
title: "Planning Sketch: Decision Forks Before Implementation"
category: "planning"
difficulty: "advanced"
model_hint: "opus"
execution_pattern: "interactive"
related_commands: ['pb-plan', 'pb-spec', 'pb-think', 'pb-adr']
last_reviewed: "2026-04-23"
last_evolved: "2026-04-23"
version: "1.0.0"
version_notes: "v2.21.0: New skill. Extracted from pb-plan Phases 1-2, plus Decision Forks pattern. Pairs with pb-spec via pb-plan wrapper."
breaking_changes: []
---
# Planning Sketch: Decision Forks Before Implementation

A high-level exploration of a focus area that surfaces hidden complexity, identifies decision forks, and produces a **sketch** artifact with recommended picks for the hard calls. The sketch exists so decisions happen **before** detailed planning, not during implementation.

**Resource Hint:** opus - Architect-tier work: surface unknowns, enumerate decision forks, tag recommendations with reasoning.

**Tool-agnostic:** Sketching phases (discovery, analysis, decision forks) work with any development methodology. Claude Code users invoke as `/pb-sketch`. Using another tool? Read this file as Markdown for the framework. See [`/docs/using-with-other-tools.md`](/docs/using-with-other-tools.md).

---

## When to Use

- **Before `/pb-spec`** -- decide the hard calls first, then write the detailed plan
- **Via `/pb-plan` wrapper** -- muscle memory; wrapper runs sketch → presents decisions → spec
- **Standalone research sketch** -- when you want to enumerate decision forks without committing to implementation detail yet
- **Before `/pb-adr`** -- sketch the forks, choose one, then document the decision formally

**Don't use for:**
- Decisions with one obvious path (just implement it)
- Pure documentation or config changes
- Bug fixes where the fix is a single line

---

## Philosophy

**Foundation:** Assumes `/pb-preamble` thinking (transparent reasoning, challenge assumptions) and `/pb-design-rules` thinking (clarity, simplicity, modularity).

**The sketch exists to prevent premature commitment.** When planning conflates "what approach?" with "what are the numbered steps?", the plan gets written around the first viable approach instead of the best one. Sketching separates these phases: enumerate forks, tag recommendations, get user decision, *then* spec.

### Core Principles

1. **Surface unknowns first** - Research unstable facts (pricing, APIs, version constraints) before planning around them.
2. **Enumerate decision forks** - Where are there 2-4 genuinely viable paths? Name them. Don't collapse early.
3. **Recommend, don't decide** - The sketch recommends; the user chooses. Sketch is advisory.
4. **Bounded research** - Use official docs and authoritative sources. Don't spiral into exhaustive literature review.
5. **Hand-off is the product** - Sketch output must be consumable by `/pb-spec` (or a human operator) to produce the detailed plan.

---

## Phase 1: Discovery

Gather context. Do not proceed to analysis until these are answered:

### 1. What Problem Are We Solving?

```
- What is the user/business problem?
- Why now? What's the trigger for this work?
- What happens if we don't do this?
- Is this the right solution, or are there alternatives?
```

### 2. What Are the Boundaries?

```
- What is explicitly IN scope?
- What is explicitly OUT of scope?
- Are there dependencies on other work?
- Are there time-sensitive constraints (not estimates, but hard deadlines)?
```

### 3. What Freedom Do We Have?

```
- Can we make breaking changes to APIs/interfaces?
- Can we refactor existing code?
- Can we change data models/schemas?
- Can we update/remove dependencies?
- Can we delete unused code?
```

### 4. How Will We Know We're Done?

```
- What are the acceptance criteria?
- Are there measurable success metrics?
- Who signs off on completion?
- What does "good enough" look like vs. "perfect"?
```

**Stop if unclear.** Clarify before proceeding. Assumptions compound into wasted work.

---

## Phase 2: Multi-Perspective Analysis

Run the focus area through four lenses; each catches what the others miss.

- **Engineering** - What existing code changes, what's new, what can be deleted or reused, what are the unknowns?
- **Architecture** - Does this cross a system boundary, add a dependency, or break an existing pattern?
- **Product** - Who benefits, what's the user-facing impact, what needs documenting?
- **Operations** - Does deployment change, what monitoring is needed, what's the rollback, any performance cliff?

Name the lens where the biggest risk sits. That focuses the rest of the sketch.

---

## Phase 3: Bounded Research (Optional)

When the analysis hits unstable facts -- pricing, API surface, version constraints, deprecations -- research them before committing to an approach. Keep research bounded.

**In scope:**
- Official docs (vendor, library, framework)
- Current CLI/tooling behavior for the target version
- Deprecation notices and migration paths
- Authoritative community sources (canonical Stack Overflow answers, maintainer blog posts)

**Out of scope:**
- Exhaustive literature review
- Searching for secrets, PII, or proprietary internals
- Speculative research on hypothetical future versions

**Signal to stop:** You can name the concrete options and their trade-offs. Further research produces diminishing returns. Write down the unresolved items as Open Questions.

---

## Phase 4: Decision Forks

**This is where sketch earns its place.** Identify every point where 2-4 genuinely viable paths exist. Name them. Recommend one with reasoning. Let the user decide.

### Fork Structure

For each fork, produce:

```markdown
### Fork N: {one-line decision}

**Why this fork exists:** {the constraint or trade-off that forces a choice}

Options:
- N-a) {Option name} -- {one-sentence description}
    - Recommended if {condition}. Reasoning: {why}
- N-b) {Option name} -- {one-sentence description}
    - Recommended if {condition}. Reasoning: {why}
- N-c) {Option name} -- {one-sentence description}

**Recommended:** N-a (default). Reasoning: {one sentence}.
```

### Fork Quality Bar

- **2-4 options per fork.** More than 4 usually means the fork isn't real (collapse similar options) or you need sub-forks (split them).
- **Options must be mutually exclusive.** If two options can coexist, they're not forks -- they're independent choices.
- **Reasoning must name the trade-off.** "Option A is simpler" is weak. "Option A is simpler; Option B scales to N=10k but we only need N=100" is the trade-off.
- **Recommendation is advisory, not mandatory.** The user overrides freely.

### When There Are No Forks

If analysis produces a single obvious path, say so:

```markdown
## Decision Forks

No forks. Path is: {one-sentence description}. Rationale: {why no forks}.
```

Proceed to sketch output with no forks to resolve.

---

## Sketch Output

Write the sketch to `sketch/{generated-kebab-case-name}.md` (create `sketch/` if it doesn't exist).

### Sketch File Structure

```markdown
# Sketch: {Title}

**Created:** {YYYY-MM-DD}
**Status:** decisions pending | decisions resolved

## Problem

{2-3 sentences from Phase 1 Discovery -- what, why now, success criteria}

## Scope Summary

**In Scope:** {one line or bulleted list}
**Out of Scope:** {one line or bulleted list}

## Approach Summary

{2-4 sentences describing the high-level approach, mentioning forks by number}

## Decision Forks

{Fork 1: ...}
{Fork 2: ...}
{Fork N: ...}

## Recommended Picks (copy/paste)

`1-a, 2-b, 3-a`

## Open Questions

- {Unresolved items that don't rise to full forks}

## Feeds Into

- `/pb-spec` -- takes this sketch + resolved decisions, produces detailed plan
- `/pb-adr` -- if any fork decision warrants formal architecture record
```

### Interactive Mode

When run interactively, after writing the sketch:
1. Print the sketch file path.
2. Print the Decision Forks block verbatim.
3. Ask: "Confirm recommended picks `1-a, 2-b` (use actual fork-option labels), or override with specific labels."
4. On user response, update sketch status to `decisions resolved` and append the resolved picks.
5. Hand off to `/pb-spec` (via `/pb-plan` wrapper) or stop if used standalone.

### Non-Interactive Mode (automation)

When run non-interactively (via a wrapper that auto-picks recommendations), extract labels tagged `Recommended` and use them directly. Skip step 3-4 above; update status to `decisions resolved (auto)`.

---

## Decision Forks: Worked Example

**Context:** Adding caching to an API endpoint. Discovery done, scope locked.

### Fork 1: Cache location

**Why this fork exists:** The endpoint reads from Postgres and CPU-renders a response. Cache can live at multiple layers.

Options:
- 1-a) In-process LRU (Go `sync.Map` + TTL) -- zero infra, lost on restart.
    - Recommended if request volume fits single process and stale-on-restart is acceptable. Reasoning: simplest, fastest, no new deps.
- 1-b) Redis -- shared across replicas, survives restarts, adds a dep.
    - Recommended if we already run Redis or expect multi-replica. Reasoning: shared cache earns its place only at multi-replica.
- 1-c) CDN edge cache -- zero backend involvement, coarse invalidation.
    - Recommended if responses are truly static per URL. Reasoning: free scale but weak invalidation.

**Recommended:** 1-a (default). Reasoning: single replica, stale-on-restart is fine for this endpoint.

### Fork 2: Invalidation strategy

**Why this fork exists:** Underlying data can change; stale cache must eventually clear.

Options:
- 2-a) TTL only (e.g., 60s) -- simple, slightly stale data.
- 2-b) Event-driven (invalidate on write) -- fresh, requires write-path hook.

**Recommended:** 2-a. Reasoning: stale-by-60s is acceptable; write-path hook is out of scope.

### Recommended picks (copy/paste)

`1-a, 2-a`

---

## Red Flags in Sketching

### False Forks

- "Should we use Option A or Option A with a slightly different config?" -- not a fork; it's a parameter.
- "Should we use TypeScript or JavaScript?" -- not a fork if the project is already TypeScript; it's noise.

**Response:** Collapse. The fork wasn't real.

### Premature Commitment

- "I already know we're using X, so forks don't matter." -- if X is settled, say so explicitly in Approach Summary and move on. But be honest: is X settled, or are you avoiding the work of enumerating alternatives?

### Analysis Paralysis

- "We need to research every possible option." -- bounded research. Stop when the trade-offs are nameable.

### Sketch Bloat

- Sketch > 2 pages. You're writing the spec, not the sketch. Move detail to `/pb-spec`.

---

## Hand-off to `/pb-spec`

Sketch is complete when:
- [ ] Problem, Scope Summary, Approach Summary written
- [ ] Decision Forks enumerated (or explicitly marked "no forks")
- [ ] Recommended Picks listed (if forks exist)
- [ ] Open Questions captured (if any)
- [ ] File saved at `sketch/{name}.md`
- [ ] User has resolved decisions (interactive mode) OR auto-picks applied (non-interactive mode)

Then invoke `/pb-spec sketch/{name}.md` (or let the `/pb-plan` wrapper do it).

---

## Related Commands

- `/pb-plan` - Orchestrating wrapper; runs this skill, surfaces decisions, hands off to spec.
- `/pb-spec` - Detailed implementation plan from a resolved sketch.
- `/pb-think` - Deep thinking when a fork itself is ambiguous.
- `/pb-adr` - Document architecture decisions formally after a fork resolves.
- `/pb-design-rules` - Technical principles that inform option evaluation.
