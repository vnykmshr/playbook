---
name: "pb-forge"
title: "Lifecycle Step-Runner"
category: "development"
difficulty: "advanced"
model_hint: "opus"
execution_pattern: "interactive"
related_commands: ['pb-what-next', 'pb-review', 'pb-huddle', 'pb-preflight', 'pb-ship']
last_reviewed: "2026-07-03"
last_evolved: "2026-06-10"
version: "1.1.0"
version_notes: "Review arc formalized: Self-gate is now a compound verify stage (review → code-review → handcraft → huddle signoff → preflight). Each sub-stage runs conditionally on concrete triggers; sub-stages compound — each catches what the prior missed. Cursor tracks sub-stage progress for correct resumption. Peer simplifies to /pb-pr only."
breaking_changes: []
---
# Lifecycle Step-Runner

`/pb-forge` drives one deliverable to its next stage and runs it -- the executing twin of `/pb-what-next`. Where what-next tells you which command to run, forge runs it, remembers where you are in the arc, and stops where you need to decide.

**Resource Hint:** opus -- judgment at the seams (genuine fork? execute done? finding real?) plus orchestration of architect-tier sub-skills.

**Tool-agnostic:** Claude Code users invoke as `/pb-forge`. Using another tool? Read this file and drive the stages yourself; the arc cursor is a plain markdown file you can keep by hand.

---

## Mindset

Apply `/pb-preamble` thinking (challenge each stage -- skip what doesn't earn its place) and `/pb-design-rules` thinking (simple by default, fail noisily at the seams, distrust "one true way"). Forge drives; it does not think for you. Every point where you'd exercise judgment is a stop, not an auto-advance.

---

## When to Use

- A deliverable (idea, PRD, issue, feature) that crosses several stages and you don't want to hold the sequence in your head.
- The outer arc -- think -> ... -> release -- which you run rarely enough that it never becomes muscle memory, unlike the daily start/review/commit inner loop.
- Resuming a deliverable mid-arc: forge knows the stage so you don't have to reconstruct it.

Skip it for one-liners and single-stage work -- invoke that one stage directly.

---

## The Arc

Forge walks these stages. It auto-runs the mechanical ones, hands off during execute, and stops hard wherever judgment or an external action is involved.

| Stage | Forge runs | Stops at |
|-------|-----------|----------|
| Frame | `/pb-think` on the deliverable | confirm direction |
| Pressure-test | `/pb-huddle` -- only when a genuine fork exists; else skips | resolve forks |
| Plan | `/pb-plan` (sketch + spec) | confirm picks |
| Execute | hands off to `/pb-start` or `/pb-todo-implement`; releases control | inner loop owns it |
| Self-gate | Compound verify (see "Self-Gate Chain" below) | accept/reject findings |
| Peer | `/pb-pr` opens the PR | external -- approve |
| Land | merge, then sync, then release | external -- each separate |

The arc is the default for new, non-trivial work. Triage decides how much of the front you actually run.

---

## Self-Gate Chain

Self-gate is a compound stage of ordered sub-stages. Each catches what the prior missed — they compound, they don't overlap. Forge auto-advances through clean sub-stages and stops when a finding needs a decision.

| # | Sub-stage | What it catches | Trigger |
|---|-----------|----------------|---------|
| 1 | `/pb-review` | Lint, tests, conventions — the quick mechanical gate | Always |
| 2 | `/code-review` at high effort | Bugs, correctness, efficiency — independent adversarial pass | `>3 files` or `>50 LOC` or new command or security/auth/regex in diff |
| 3 | `/pb-handcraft` | Prose quality, voice, clarity — form, not function | Content/docs changes (markdown commands, prose in any file) |
| 4 | Huddle signoff | Design coherence across the whole diff — intent, not content | `/code-review` or handcraft reports ≥1 finding where the fix isn't obvious from the diff |
| 5 | `/pb-preflight` | Ship-readiness wiring check — gaps, not issues | Always (last gate before Peer) |

**Order matters.** Run cheap automated gates first (review, code-review), then form gates (handcraft), then judgment gates (huddle), then the final wiring check (preflight). The compound chain reduces the surface area each huddle needs to cover: by the time you reach sub-stage 4, the obvious bugs and prose issues are already fixed.

**Sub-stage triggers are concrete OR gates, not judgment calls.** "My diff is 3 files and 40 lines" → skip code-review. "I added a new command" → run code-review. No "should I?" hand-wringing.

**Belt-and-suspenders exit.** If the user stops at any sub-stage ("fix the code-review findings first"), forge records the sub-stage as done in the cursor and the next as pending. Re-invoking forge resumes at the pending sub-stage, not the start of Self-gate.

**Tail mode.** `--arc tail` on already-completed work skips sub-stages recorded as done in the cursor. If the cursor has no sub-stage records (pre-v1.1.0), forge runs the full chain — the user can skip explicitly.

---

## Triage: How Much Arc to Run

Forge reuses the scope signal `/pb-start` already establishes (size: small/medium/large; mode: expand/hold/reduce) to decide how much arc to run -- no new triage taxonomy.

- **Small and obvious** -> skip the front (think/huddle/plan), hand straight to the inner loop.
- **Medium or large, or a genuine fork in the approach** -> run the full arc.
- **Override:** `--arc full | build | tail` when you already know.
  - `full` -- every stage. `build` -- skip the front, start at execute. `tail` -- review -> land only, for work already done.

If triage keeps short-circuiting to the tail on your real work, that's the signal the front arc isn't earning its place here.

---

## Execute Hand-off

Execute is where forge gets out of the way. It invokes `/pb-start` (or `/pb-todo-implement` when a plan exists), records the branch and plan path in the arc cursor, and releases control. From there the inner loop and `/pb-pause` / `/pb-resume` own session continuity exactly as they do today -- forge does not wrap or micromanage your coding.

Forge treats execute as complete when you say so. Hints it offers but never acts on alone: the plan's tasks are all checked, or the tree is clean and ahead of main. Re-invoke `/pb-forge` to pick the arc back up at the next stage.

---

## The Arc Cursor

Forge keeps one file per deliverable at `todos/forge/{slug}.md` -- under the dev-only `todos/` tree, gitignored, not a tracked artifact. It holds:

- current stage
- sub-stage progress within Self-gate (which sub-stages completed, which is pending)
- deliverable paths as they appear: sketch -> plan -> branch -> PR
- decisions resolved at each seam
- one log line per stage transition

This file is the `/pb-resume` hook for the arc. Where `/pb-resume` tells you the session state (branch, uncommitted work), the cursor tells you the arc state (which stage, what's next) -- one command to resume a deliverable you left days ago, no reconstruction.

---

## External Actions Stop Hard

Opening a PR, merging, syncing to remote, and releasing are each a separate stop. Forge states what it is about to do and waits for an explicit go in a new message. It never batches them -- not push+PR, not merge+release. This is the global External Action Gate; forge enforces it so you never tag a release on a reflex. The gate and the GitHub Artifact Register (the rules for commit/PR/release messages) live in `~/.claude/CLAUDE.md`.

---

## `/pb-forge` vs `/pb-what-next`

| | recommends | drives | holds state |
|-|:-:|:-:|:-:|
| `/pb-what-next` | yes | no | no -- reads git each run |
| `/pb-forge` | -- | yes | yes -- the arc cursor |

what-next answers "what command next?" from git state, statelessly. forge runs the next stage and remembers the arc across stages and sessions. Reach for what-next when you want a suggestion; reach for forge when you want the arc driven.

---

## When NOT to Use Forge

- One-liner or single-stage work -- run that stage directly (`/pb-review`, `/pb-pr`, ...).
- You want a recommendation, not execution -- use `/pb-what-next`.
- You're deep in execute -- stay in the inner loop; forge is waiting and resumes when you call it.

---

## Resumption

Re-invoking `/pb-forge` on a deliverable with an existing cursor resumes at the recorded stage. Forge reads the cursor, confirms the stage with you, and continues. It does not re-run completed stages.

---

## Red Flags

- **Forge auto-advanced a seam.** It picked a fork, accepted a review finding, or pushed without asking. That's a bug, not a convenience -- the seam stops are the whole contract.
- **Triage always lands on tail.** Most of your work skips the front arc, so forge wraps the review chain + PR + release. The compound self-gate is the meat of the tail — not thin ceremony. Still, if you never need think/huddle/plan, the front arc may not earn its place for this project.
- **Cursor outlived the deliverable.** A stale `todos/forge/*.md` for shipped work is a position, not an archive -- delete it.

---

## Related Commands

- `/pb-what-next` - The recommending twin; suggests the next command without running it.
- `/pb-review` - First sub-stage of Self-gate (quick mechanical gate).
- `/pb-huddle` - Huddle signoff sub-stage of Self-gate (design coherence on non-obvious findings).
- `/pb-preflight` - Ship-readiness sub-stage of Self-gate (last gate before Peer).
- `/pb-ship` - The ship workflow (PR -> merge -> release) forge's tail stages map to.

---

*Drive the arc. Stop where you decide. Resume where you left off.*
