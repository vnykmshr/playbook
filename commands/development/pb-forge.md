---
name: "pb-forge"
title: "Lifecycle Step-Runner"
category: "development"
difficulty: "advanced"
model_hint: "opus"
execution_pattern: "interactive"
related_commands: ['pb-what-next', 'pb-plan', 'pb-start', 'pb-review', 'pb-ship']
last_reviewed: "2026-06-10"
last_evolved: "2026-06-10"
version: "1.0.0"
version_notes: "Initial: stateful step-runner that drives the per-deliverable outer arc (think -> ... -> release), the executing twin of /pb-what-next. Auto-drives mechanical stages, hands off to the inner loop during execute, stops hard at judgment seams and external actions."
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
| Self-gate | `/pb-review` + `/pb-handcraft` | accept/reject findings |
| Peer | `/pb-pr` opens the PR; `/code-review` independent pass | external -- approve |
| Land | merge, then sync, then release | external -- each separate |

The arc is the default for new, non-trivial work. Triage decides how much of the front you actually run.

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
- **Triage always lands on tail.** Most of your work skips the front arc, so forge wraps two stages. Shrink it to the tail or drop it for that work.
- **Cursor outlived the deliverable.** A stale `todos/forge/*.md` for shipped work is a position, not an archive -- delete it.

---

## Related Commands

- `/pb-what-next` - The recommending twin; suggests the next command without running it.
- `/pb-plan` - The planning stage forge drives (sketch + spec).
- `/pb-start` - The execute entry forge hands off to.
- `/pb-review` - The self-gate stage.
- `/pb-ship` - The ship workflow (PR -> merge -> release) forge's tail stages map to.

---

*Drive the arc. Stop where you decide. Resume where you left off.*
