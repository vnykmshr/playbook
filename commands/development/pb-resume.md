---
name: "pb-resume"
title: "Resume Development Work"
category: "development"
difficulty: "advanced"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-start', 'pb-pause', 'pb-cycle', 'pb-review-incoming']
last_reviewed: "2026-08-03"
last_evolved: "2026-08-03"
version: "1.9.0"
version_notes: "v1.9.0: Standard mode ends in a proposal, not a change. Step 0b becomes CLASSIFY rather than ACT (the SURFACE-ACT-ARCHIVE model cuts to SURFACE-ARCHIVE, with acting relocated behind one gate), Step 3's /pb-review-incoming routing demotes from imperative to detection, and a new terminal Step 5 consolidates everything into a single proposal and stops. The act/propose test is a property of the action -- could the user undo it without knowing it happened -- not of whether a file is gitignored. Deep mode is unchanged and ungated: its authorization is the invocation. Also: findings from unprescribed investigation are proposals, never actions; Quick Commands deleted (6 of 6 rows duplicated Steps 1-3). v1.8.0: The recap archive is the project's existing archive, not a fixed path -- Step 0a's dedup and Step 0c's write now name one location instead of diverging, and the v1.6.1 fork-and-point-back rule is gone (it created the split it cited as the hazard). `memory/` in a consumer project may be an auto-memory directory outside the repo, which the v1.6.0 rationale was not about. v1.7.0: Step 3 routes an unratified batch to /pb-review-incoming -- commits authored in another project's session arrive with sound content and undrifted conformance, and resume is where they surface. v1.6.1: An existing memory/lessons.md stays put and is linked from the new archive -- the path move must not fork a project's history silently. v1.6.0: Recap archive moves from memory/lessons.md to todos/done/lessons.md — session and lesson notes stay in the gitignored dev tree. Strip now means remove the body, not comment it out. v1.5.0: Restructure Step 0 — SURFACE→ACT→ARCHIVE phases with dedup check, archive-failure handling, and Recap Disposition summary."
breaking_changes: ['Step 0b changes from ACT to CLASSIFY -- standard mode no longer applies fixes or commits while surfacing the recap; the SURFACE-ACT-ARCHIVE model becomes SURFACE-ARCHIVE', 'Standard mode gains a terminal Step 5 and ends there; deep-mode steps renumber 5-6 to 6-7', 'Quick Commands section removed -- every row duplicated a command already in Steps 1-3']
---
# Resume Development Work

Quickly get back into context after a break. Use this to resume work on an existing feature or branch.

**Mindset:** Resuming requires understanding assumptions made and verifying context is complete. Apply `/pb-preamble` thinking: challenge what was decided and why. Apply `/pb-design-rules` thinking: is the code clear, simple, and robust?

**Resource Hint:** sonnet - context recovery, state assessment, health check

---

## Modes

```
/pb-resume             → Standard (default): recap review, git state, sync, load context, health check
/pb-resume deep        → Deep: standard + verify/regenerate stale layers + run tests
```

**When to use deep:** After long breaks (days/weeks), picking up someone else's work, or when standard mode flags stale context layers.

**Standard mode ends in a proposal, not a change.** Everything before Step 5 is read-only. Resume exists to rebuild context and hand it back, and the person who paused knows things the repository does not -- what the batch was for, what they had already decided to do with it. A command that starts fixing what it finds spends that context before it is offered.

**Deep mode is different, and the difference is consent:** typing `/pb-resume deep` is the instruction to regenerate stale layers and run the baseline. That authorization is in the invocation, so Steps 6 and 7 act without asking again.

---

## Standard Mode (Default)

### Step 0: Session Recap Review

Read the `### Session Recap` section from `todos/pause-notes.md`.

**If no Session Recap section exists:** skip to Step 1. (First-time use with pre-v1.5.0 pause notes: say "Session Recap: none - recaps are written by `/pb-pause` when a session produces learnings." Once.)

---

#### 0a. SURFACE: Present Findings

Before surfacing, check for duplicates: if the recap content already appears as the most recent entry in **the project's recap archive** (Step 0c names it), skip to Step 1 (already processed on a prior resume).

Otherwise, surface the recap visibly. Present findings as a structured summary. The recap is a learning loop, not a write-only log:

```
## Session Recap (from last session)

Key observations:
- [what was observed]

**Finding:** [observation with playbook/project implication] → [action to take]
**Finding:** [observation] → [action to take]
```

Findings that need action should be called out explicitly. Observations with no action item can be summarized briefly.

---

#### 0b. CLASSIFY: Sort Each Finding

Sort every finding into one of four dispositions. **Do not execute any of them here** -- they are carried to Step 5 and proposed as one list, alongside whatever Steps 1-4 turn up:

- **Fixable now** (wording, guardrail, convention) → goes to Step 5 as a proposed change, with the file and the edit named
- **Worth doing, needs planning** → goes to Step 5 as a proposed working-context entry under Next
- **Q3 candidate** → note it; `/pb-evolve` mines quarterly. No proposal needed
- **No action** → state explicitly: "Archived only - no immediate action"

A finding is a claim about what should change. Reading it is not the same as being authorized to make the change, and the gap between those two is where the person who paused gets to speak.

---

#### 0c. ARCHIVE: Append → Strip

1. **Append to the project's recap archive** first - prevents data loss if interrupted. **The archive is wherever this project's recaps already go.** A project that has none starts one at `todos/done/lessons.md`, the default because `todos/` is gitignored and keeps session narrative out of the repo. Step 0a's dedup check reads the same file this step writes; if you find yourself reading one path and writing another, that is the bug.

   Do not relocate an existing archive to match the default. Moving history to chase a path change is churn, and writing new entries to a second location forks the record whether or not you leave a pointer behind. If an existing archive genuinely violates the property above - tracked, leaking session narrative into git - moving it is a decision to raise with the user, not a silent migration.
   ```markdown
   ## [YYYY-MM-DD] — [session context]
   [recap content]
   ```
2. **If the append fails:** leave the recap in pause notes, flag the error. Do not strip.
3. **Strip from pause notes** only after confirming the archive write succeeded. Strip means remove the body and leave a one-line pointer to the archive - not a comment marker around retained text.

Session notes and lesson notes are position and reflection, not tracked artifacts; anything durable belongs in `docs/`. `todos/` is the default home because it already carries the pause notes they continue and inherits its gitignore - but a project whose archive lives outside the repo entirely (a Claude Code auto-memory directory, for instance) already satisfies that, and `memory/` in such a project is not the repo directory this rule was written about.

---

#### 0d. Recap Disposition

After archiving, report how each finding was **classified** -- not what was done to it:

```
## Recap Disposition

- Finding 1: proposed fix → <file>, carried to Step 5
- Finding 2: proposed for working context under Next
- Finding 3: Q3 candidate noted
- Finding 4: archived only
```

The archive itself is the one thing this step does rather than proposes. It is the command's declared job, it is announced in the same breath, and it is reversible -- which is the test Step 5 states.

Then proceed to Step 1.

---

### Step 1: Check Current State

```bash
git branch --show-current
git status
git log --oneline -5
git stash list
```

### Step 2: Sync with Remote

```bash
git fetch origin
git log --oneline HEAD..origin/main
```

If main has moved ahead, review what changed before rebasing:

```bash
git log --oneline HEAD..origin/main    # What you missed
git diff origin/main...HEAD            # Your full branch diff
git rebase origin/main
```

### Step 3: Review Recent Work

```bash
git log origin/main..HEAD --oneline    # Branch commits
git diff                                # Uncommitted changes
git diff --staged                       # Staged changes
```

**Detection, not action:** if commits here have not been ratified against this project's conventions -- authored in another project's session, or simply never reviewed here -- record that and carry `/pb-review-incoming` to Step 5 as a proposed next command. The author had the evidence and not your conventions, so the content is usually sound and the conformance is where it drifts.

Do not begin ratifying here. The user may already know what this batch is for and what they intend to do with it, and that intent is cheaper to receive than to reconstruct.

### Step 4: Load Session State + Context Health Check

**Load session state:**

```bash
cat todos/1-working-context.md         # Project snapshot
cat todos/pause-notes.md               # Where you left off
```

**If pause notes exist:** Follow documented next steps, verify blockers resolved.

**Context health check - report actual sizes:**

```bash
wc -l ~/.claude/CLAUDE.md              # Global (target: ~160)
wc -l .claude/CLAUDE.md                # Project (target: ~180)
# memory/MEMORY.md                     # Auto-loaded (target: ~100)
wc -l todos/1-working-context.md       # Working context (target: ~50)
wc -l todos/pause-notes.md             # Pause notes (target: ~30)
```

**Flag issues:**
- Working context version doesn't match `git describe --tags` → stale, consider `/pb-resume deep`
- Pause notes has multiple entries → old entries should have been archived by `/pb-pause`
- Any layer missing → run the appropriate regeneration command

---

### Step 5: Propose and Stop

This is the only step that produces an output, and standard mode ends here. Consolidate everything Steps 0-4 turned up into **one** proposal, then stop and wait.

```
## Resume Complete — proposed next actions

State: <branch>, <ahead>/<behind>, <clean|N modified>, <N> commits since <tag>
Flagged: <stale layers, unratified batch, anything the health check surfaced>

Proposed:
1. <action> — <why, in one line>
2. <action> — <why>

Nothing has been changed. What do you want to pick up, and what do you know
about this state that I don't?
```

**The act/propose test: could the user undo this without knowing it happened?** If not, it is a proposal. A commit is trivially reversible and completely invisible, which is the combination that costs someone their afternoon; an append to a gitignored log announced in the same breath is neither. The test is a property of the *action*, not of the file it touches -- do not reduce it to whether something is gitignored.

**Findings from investigation this command did not prescribe are proposals, never actions.** Nothing stops you running the test suite, `gh run list`, or a linter during a standard resume, and nothing should. But a red result you went looking for does not authorize you to fix it -- that is a separate decision, and it belongs in the list above. Going looking is cheap and often right; acting on what you find is what needed permission.

*(This rule generalizes past resume -- it governs any session that goes looking. It lives here at n=1, where the evidence is; promoting it is a `/pb-evolve` question, not a claim this command should make.)*

---

## Deep Mode

Run standard mode first, then continue with these steps. **Deep mode's authorization is the invocation** -- `/pb-resume deep` is the instruction to regenerate and verify, so these two steps act without a second gate.

### Step 6: Verify and Regenerate Context Layers

Check each layer for staleness and regenerate as needed:

```bash
git describe --tags                    # Current version
```

- **Working context stale** (version mismatch) → run `/pb-context`
- **Project CLAUDE.md stale** (structural changes since last update) → run `/pb-claude-project`
- **Global CLAUDE.md stale** (playbook version changed) → run `/pb-claude-global`

### Step 7: Verify Baseline

```bash
# Run project tests (adapt to your project)
python3 -m pytest tests/ -q            # or: make test, npm test, go test ./...

# Verify CI status
gh run list --limit 1
```

Confirm baseline is green before starting new work.

---

## Recovery Checklist

Before continuing work:

- [ ] On correct branch
- [ ] Branch is up to date with main
- [ ] Checked pause notes
- [ ] Understand what was last done
- [ ] Know what's next
- [ ] Working context is current

---

## If Completely Lost

```bash
git branch -a                          # What branches exist?
git reflog | head -20                  # What branch was I on?
git log --all --oneline --graph -20    # What work exists?
cat todos/pause-notes.md               # Any breadcrumbs?
```

---

## Related Commands

- `/pb-start` - Begin work on a new feature or fix
- `/pb-pause` - Gracefully pause work and preserve context
- `/pb-cycle` - Self-review and peer review during development
- `/pb-review-incoming` - Ratify commits authored in another project's session

---

*Context is expensive to rebuild. Leave breadcrumbs for future you.*
