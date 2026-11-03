---
name: "pb-forge"
title: "Lifecycle Step-Runner"
category: "development"
difficulty: "advanced"
model_hint: "opus"
execution_pattern: "interactive"
related_commands: ['pb-what-next', 'pb-review', 'pb-huddle', 'pb-preflight', 'pb-ship']
last_reviewed: "2026-11-03"
last_evolved: "2026-09-24"
version: "1.5.0"
version_notes: "v1.5.0: Self-gate is find, vet and fix, judge. Self-review, code-review and handcraft report without editing; one panel vet rules on every finding and the user confirms; fixes pass the tests, then an independent re-review scoped to the fixes, stopping when a vet takes nothing or after two rounds, when forge proposes a guard; signoff checks the rulings landed. Code-review runs when Land includes a release. Sub-stages are named, and old numbered cursor records run the full chain. Code-review's trigger adds docs that record rulings, decisions or quotations: a misplaced quote is a correctness bug that prose gates read past. A SHIPPED cursor is archived to `todos/done/forge-<slug>.md` rather than deleted: delete commands are commonly denied; a taken name gets a date-and-time suffix, since a plain `mv` overwrites silently. Leg boundaries: Plan→Execute and Execute→Self-gate end a leg. At Plan→Execute forge writes the cursor -- next action, decisions, paths of everything the next leg needs -- says the context can be compacted or the session ended, and stops before /pb-start; the Execute hand-off says the same for Execute→Self-gate, where forge is not running; at Peer, only the stopping half. Mid-stage compaction loses the conversation the stage is still using. v1.4.0: Sub-stage 2 no longer claims to be unexercised: the first run to reach it, in another project, took the offer, got real findings, and the offer-not-run default held (n=1). Peer row: a project with no remote skips Peer, and Land is the local merge. The cursor gets a terminal stage: SHIPPED, set after the last Land stop the deliverable needs, then the file is deleted; a denied delete leaves the SHIPPED cursor for /pb-resume to offer. The Red Flag that owned no deletion is gone. v1.3.0: Sub-stage 2 is an offer, not a run. /code-review became assistant-invocable (Claude Code v2.1.246), which closes the gap that forced forge to stop there -- and the huddle declined to replace a forced stop with an automatic pass, because a model that already verifies its own work does not need a fifth self-check on every broad-trigger diff. Unexercised: no run has reached it. v1.2.1: Sub-stage 5's trigger says why Always is honest now that /pb-preflight scopes itself in Step 0. Forge had been describing preflight as a wiring check in wording preflight did not carry; preflight v1.1.0 now owns that framing. v1.2.0: Slice escape added — the front arc now carries an iteration tally, and forge stops at three to propose the smallest executable slice. Acceptance gates must state a falsifier before their first run. Cursor records the tally and the falsifier."
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
| Self-gate | Find, vet and fix, judge (see "Self-Gate Chain" below) | vet rulings, signoff |
| Peer | `/pb-pr` opens the PR. No remote: skipped, and Land is the local merge | external -- approve |
| Land | merge, then sync, then release | external -- each separate |

The arc is the default for new, non-trivial work. Triage decides how much of the front you actually run.

---

## Self-Gate Chain

Self-gate runs in three phases: find, then vet and fix, then judge. Every gate that edits runs before the last gate that judges. Sub-stages are named, and the cursor records them by name.

**Find.** Each finder reports; none edits.

| Sub-stage | What it catches | Trigger |
|-----------|----------------|---------|
| self-review (`/pb-review`) | Lint, tests, conventions | Always. Inside forge it reports code-changing fixes instead of applying them |
| code-review (`/code-review` at high effort) | Bugs and correctness: an independent pass | `>3 files` or `>50 LOC` or new command or security/auth/regex in diff, or docs that record rulings, decisions or quotations (a misplaced quote is a correctness bug that prose gates read past). Runs when the cursor's Land includes a release; otherwise forge offers it and runs it on the user's yes |
| handcraft (`/pb-handcraft`) | Prose quality, voice, clarity | Content/docs changes (markdown commands, prose in any file) |

**Vet and fix.** When the finders report at least one finding:

1. **Vet.** A panel rules on every finding, run as `/pb-huddle` runs one (a lead from the finding's lane, two or three lenses): TAKE with the fix, REJECT with why, or DEFER with where it goes. Forge stops once with the rulings; the user confirms or overrides them.
2. **Fix.** Record the pre-fix SHA in the cursor, land the TAKEs, and count the fix done only when the project's tests pass on their exit code (`/pb-review --no-auto-commit` holds the commit if the user wants signoff first).
3. **Re-review.** An independent pass on `<pre-fix SHA>..HEAD` only: the fixes are a new surface. Its findings go back to the vet.

Stop when a vet takes nothing. At most two re-review rounds: if a third is needed, forge stops and proposes a guard or test for that defect class, and the user decides -- the escalation `/pb-review`'s loop detection makes.

**Judge.**

| Sub-stage | What it checks | Trigger |
|-----------|----------------|---------|
| signoff | The vet's lead reads the diff against the vet record: every TAKE landed and nothing outside the rulings changed. Go, or reopen a named finding | A fix landed. If the vet took nothing, its record is the signoff |
| preflight (`/pb-preflight`) | Ship-readiness wiring: gaps, not issues | Always -- its Step 0 scopes the gate to your surface, which is what makes Always honest on a non-service project |

**Triggers are concrete OR gates, not judgment calls.** "My diff is 3 files and 40 lines" → no code-review. "I added a new command" → code-review. No "should I?" hand-wringing.

**Belt-and-suspenders exit.** If the user stops at any sub-stage ("fix the code-review findings first"), forge records it as done in the cursor and the next as pending, by name. Re-invoking forge resumes at the pending sub-stage, not the start of Self-gate.

**Tail mode.** `--arc tail` on already-completed work skips sub-stages recorded as done in the cursor. A cursor with no sub-stage records, or one that records them by the old numbers, runs the full chain -- the user can skip explicitly.

---

## Triage: How Much Arc to Run

Forge reuses the scope signal `/pb-start` already establishes (size: small/medium/large; mode: expand/hold/reduce) to decide how much arc to run -- no new triage taxonomy.

- **Small and obvious** -> skip the front (think/huddle/plan), hand straight to the inner loop.
- **Medium or large, or a genuine fork in the approach** -> run the full arc.
- **Override:** `--arc full | build | tail` when you already know.
  - `full` -- every stage. `build` -- skip the front, start at execute. `tail` -- review -> land only, for work already done.

If triage keeps short-circuiting to the tail on your real work, that's the signal the front arc isn't earning its place here.

---

## The Slice Escape

The front arc -- Frame, Pressure-test, Plan -- produces text about work. Nothing in it can fail, so it can iterate indefinitely and feel productive the entire time. Forge counts the iterations and forces the question.

**The counter.** The arc cursor keeps a front-arc tally: increment it each time forge re-enters Frame, Pressure-test, or Plan for the same deliverable without having reached Execute in between. Revisions inside one stage count. A re-run the user asked for counts.

| Tally | Forge |
|-------|-------|
| 1 | proceeds normally |
| 2 | states the count, asks what this round will find that the last did not, and offers the slice |
| 3 | **stops.** Proposes the smallest slice that executes; does not re-enter the front arc until it is built or explicitly declined |

A front-arc gate that returns a verdict of *not ready* moves the tally regardless of which stage produced it. Two rounds is the point to reach for an executable -- not five.

**The slice** is the smallest thing that runs against real inputs: real data, real files, the real adjacent system. Not a mock, not a skeleton returning constants. Its job is to produce artifacts a review cannot -- something that fails, or passes when it should not. Prefer the path that is also the production path; a slice built on a shortcut proves the shortcut.

**Every acceptance gate states its falsifier before it is run the first time.** "Done when X," where X is observable and could come out either way. A gate phrased as an open question -- *could a reader who has never seen this implement it?* -- has no failing condition and therefore no passing one. It returns NO for as many rounds as it is run, and each NO reads as a finding rather than as evidence the instrument is broken. If you cannot state what would end the gate, the gate is not ready to run.

**The tell is usually in your own writing.** "Another round will likely find another layer" is not a plan; it is a prediction that the loop does not converge. Read it as the stop signal it is.

---

## Execute Hand-off

Execute is where forge gets out of the way. It invokes `/pb-start` (or `/pb-todo-implement` when a plan exists), records the branch and plan path in the arc cursor, and releases control. From there the inner loop and `/pb-pause` / `/pb-resume` own session continuity exactly as they do today -- forge does not wrap or micromanage your coding.

Forge treats execute as complete when you say so. Hints it offers but never acts on alone: the plan's tasks are all checked, or the tree is clean and ahead of main. When execute is done, put anything the commits do not show (deviations, open findings) in the cursor, compact the context or start fresh, then re-invoke `/pb-forge` to pick the arc back up at the next stage.

---

## The Arc Cursor

Forge keeps one file per deliverable at `todos/forge/{slug}.md` -- under the dev-only `todos/` tree, gitignored, not a tracked artifact. It holds:

- current stage, ending at `SHIPPED`
- front-arc tally (see "The Slice Escape") -- reset to 0 on reaching Execute
- whether Land includes a release (set at Plan; it decides whether code-review runs or is offered)
- Self-gate progress by sub-stage name, the pre-fix SHA, and each vet round's rulings
- deliverable paths as they appear: sketch -> plan -> branch -> PR
- the falsifier stated for any acceptance gate the front arc runs
- decisions resolved at each seam, written as they are made
- the next action, and the path of everything the next leg needs (briefs, panel records, measurements) -- under `todos/`, never only in the conversation or a session scratchpad
- one log line per stage transition

This file is the `/pb-resume` hook for the arc. Where `/pb-resume` tells you the session state (branch, uncommitted work), the cursor tells you the arc state (which stage, what's next) -- one command to resume a deliverable you left days ago, no reconstruction.

**Leg boundaries.** Plan→Execute and Execute→Self-gate end a leg: the next stage needs nothing from the conversation that the cursor does not hold. At Plan→Execute, forge writes the cursor, says one line, and stops: "Leg done, cursor current. Continuing now: compact the context, then re-invoke `/pb-forge <slug>`. Stopping: start fresh later and re-invoke it." `/pb-start` runs on the re-invoke. Forge is not running when Execute ends, so the Execute hand-off carries that boundary. At Peer, which can wait days on approval, forge says the stopping half. Never mid-stage.

**Closing the cursor.** After the last Land stop the deliverable needs (the release if it ships one, the merge if not), set the stage to `SHIPPED`, then move the file to `todos/done/forge-<slug>.md` -- `mkdir -p todos/done` first; if that name is taken, suffix the date and time (`-YYYYMMDD-HHMM`); never overwrite an archive. Move, never delete: delete commands are commonly denied. A deferred release is still needed, so the cursor stays at Land. If the move fails, leave the `SHIPPED` cursor: `/pb-resume` lists it and offers the move. `SHIPPED` is the stage resume keys on, so do not mark a finished arc any other way.

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

Re-invoking `/pb-forge` on a deliverable with an existing cursor resumes at the recorded stage. Forge reads the cursor, confirms the stage with you, and continues. It does not re-run completed stages. A `SHIPPED` cursor has no next stage: forge offers to archive it.

---

## Red Flags

- **Forge auto-advanced a seam.** It picked a fork, accepted a review finding, or pushed without asking. That's a bug, not a convenience -- the seam stops are the whole contract.
- **Triage always lands on tail.** Most of your work skips the front arc, so forge wraps the review chain + PR + release. The compound self-gate is the meat of the tail, not thin ceremony. Still, if you never need think/huddle/plan, the front arc may not earn its place for this project.
- **The front-arc tally is climbing.** Plan is iterating on itself. The spec is growing and nothing has run. Take the slice escape; the thing that has never executed is where the defects are.
- **An acceptance gate has returned the same verdict twice.** Check whether it can return the other one. A gate with no falsifier is not a finding generator, it is a loop.

---

## Related Commands

- `/pb-what-next` - The recommending twin; suggests the next command without running it.
- `/pb-review` - Self-review, the first finder in Self-gate.
- `/pb-huddle` - How Self-gate's vet panel runs (a lead plus lenses).
- `/pb-preflight` - Ship-readiness, Self-gate's last gate before Peer.
- `/pb-ship` - The ship workflow (PR -> merge -> release) forge's tail stages map to.

---

*Drive the arc. Stop where you decide. Resume where you left off.*
