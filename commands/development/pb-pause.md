---
name: "pb-pause"
title: "Pause Development Work"
category: "development"
difficulty: "advanced"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-resume', 'pb-start', 'pb-standup', 'pb-handoff']
last_reviewed: "2026-08-04"
last_evolved: "2026-08-04"
version: "1.9.2"
version_notes: "v1.9.2: Step 4 names the archive's owner -- the recap stays in pause notes, /pb-resume Step 0 writes it. Pre-archiving at pause trips Step 0a's dedup check, which then correctly skips a recap that was never surfaced or classified. Observed 2026-08-04. v1.9.1: Health-check global CLAUDE.md target ~160 -> ~200, tracking the raised gate in /pb-claude-global. v1.9.0: Step 1 gates the push. The commit stays automatic -- preserving work state is what the command was invoked for -- but publishing is a separate decision, and pause runs at the moment a bad one is least likely to be caught: end of session, on whatever branch is checked out. Unpushed is now a complete pause rather than a failed one. v1.8.0: Step 4 archives to the project's existing recap archive rather than a fixed path; `todos/done/lessons.md` is the default for a project that has none. Matches /pb-resume v1.8.0. v1.7.0: Deep Step 7 runs any handoff the session wrote, from the receiver's directory. A document verified only from inside the repo that produced it passes every runnable claim it makes. v1.6.2: Deep Step 6 no longer routes around the generator -- pb-claude-project v1.2.0 preserves `## Custom (Manual)` blocks, so regenerate-then-diff replaces the hand-edit caveat. v1.6.1: An existing memory/lessons.md stays put and is linked from the new archive -- the path move must not fork a project's history silently. v1.6.0: Step 0 bootstraps the todos/ tree — a first pause no longer assumes todos/done/ and the working context already exist. Recap archive path moves to todos/done/lessons.md. v1.5.1: Deep-mode Step 6 caveat — diff before regenerating a hand-evolved project CLAUDE.md."
breaking_changes: []
---
# Pause Development Work

Gracefully pause work. Use before stepping away for hours, days, or longer.

**Mindset:** Future you will resume this. Leave breadcrumbs that make recovery effortless. Apply `/pb-preamble` thinking: be honest about blockers. Apply `/pb-design-rules` thinking: document decisions and trade-offs.

**Resource Hint:** sonnet - state preservation, context hygiene, handoff documentation

---

## Modes

```
/pb-pause              → Standard (default): commit, push, pause note, health check
/pb-pause deep         → Deep: standard + refresh working context + update CLAUDE.md
```

**When to use deep:** After releases, heavy sessions with structural changes, or before extended breaks. Standard mode's health check will flag stale context layers. That's your signal.

---

## Short Breaks (No Command Needed)

For breaks of a few hours:

```bash
git status                          # verify what's modified
git add <specific files>            # stage your in-flight work; never git add -A
git commit -m "wip: [current state]"
git push
```

That's it. No pause notes, no health check. Use `/pb-pause` when you need to preserve context for future-you or someone else.

---

## Standard Mode (Default)

### Step 0: Bootstrap the `todos/` Tree

The rest of this command writes into `todos/`. On a project's **first** pause none of it exists yet, so create what is missing before writing:

```bash
mkdir -p todos/done
# todos/pause-notes.md and todos/1-working-context.md are created by Steps 3 and 6.
```

Confirm `todos/` is gitignored. If it is not, add it -- `todos/` is the dev-only tree: position, scratch, and reflection, never a tracked artifact. Anything durable that lands there belongs in `docs/` instead.

Do not treat a missing file as "nothing to preserve." A first pause is exactly when the breadcrumbs matter most.

---

### Step 1: Preserve Work State

```bash
git status
git stash list

# Option A: Commit (preferred)
git status                              # verify what's modified
git add <specific files in your scope>  # never git add -A
git commit -m "wip: [describe current state]"

# Option B: Stash if not ready to commit
git stash push -m "WIP: [describe what's stashed]"
```

**Rule:** Never leave uncommitted work on a local-only branch overnight.

**The commit is automatic; the push is not.** Preserving work state is what you invoked this command for, so committing needs no further permission. Publishing is a separate decision with a different blast radius, and pause runs at the moment you are least able to catch a bad one -- end of session, on whatever branch you happen to be on, which is sometimes `main`.

State the branch and what would be pushed, then wait for an explicit go in a new message:

```bash
git log --oneline @{u}..HEAD 2>/dev/null || git log --oneline -5   # what would publish
git push origin $(git branch --show-current)                       # only after a go
```

If the go does not come, say the work is committed locally and unpushed. That is a complete pause, not a failed one.

---

### Step 2: Update Tracking (If Applicable)

If the project has trackers (`todos/*.md`, GitHub Issues, project boards):

- Mark completed tasks as done
- Update status of in-progress items
- Document blockers with specifics
- Note scope changes or newly discovered tasks

Skip this step if there are no active trackers.

---

### Step 3: Write Pause Notes + Context Hygiene

**3a. Write pause entry** -- replace contents of `todos/pause-notes.md`:

```markdown
# Pause Notes

Latest session pause context. Old entries archived to `todos/done/`.

---

## Pause: [Date] ([context])

**Branch:** [name] | **Commit:** [hash] | **Status:** Clean/WIP

### Where I Left Off
- Working on: [what]
- Progress: [status]
- Blocked on: [if anything]

### What Shipped (if applicable)
- [version]: [what shipped]

### Next Session
1. [Immediate next action]
2. [Following action]

### Open Questions (if any)
- [Question] - [context]

### Session Recap
*(Assistant-written -- thorough reflection on the session)*

Key observations:
- [observation]

Patterns / playbook feedback:
- [pattern or playbook command that needs attention]
```

Target: ~30-40 lines. Be specific about what's next. Skip sections that don't apply. The Session Recap section is written by the assistant, not the user -- it is a thorough analysis, not a quick skim.

**3b. Archive old entries** -- if pause-notes has entries beyond the latest, move old entries to `todos/done/pause-notes-archive-YYYY-MM-DD.md`.

**3c. Context health check:**

```bash
wc -l ~/.claude/CLAUDE.md            # Global (target: ~200)
wc -l .claude/CLAUDE.md              # Project (target: ~180)
# memory/MEMORY.md                   # Auto-loaded (target: ~100)
wc -l todos/1-working-context.md     # Working context (target: ~50)
wc -l todos/pause-notes.md           # Pause notes (target: ~30)
```

Flag if:
- Working context version doesn't match `git describe --tags` → stale, consider `/pb-pause deep`
- Pause notes has multiple entries → archive old ones
- Any layer significantly over its soft budget

---

### Step 4: Write Session Recap

After the pause entry is written, reflect on the session and fill in the `### Session Recap` section of the pause notes. This is assistant-driven. The user does not fill it in.

**What to include:** Key observations (what was learned, what went wrong, what surprised you, what you'd do differently) and patterns/playbook feedback (did a playbook command mislead or help? is a command missing or wrong? did a workflow deviate and need correction?). Observations can target playbook commands, project workflows, or personal patterns.

**Depth:** Thorough reflection. Analyze the session's git log, conversation, decisions made, and paths not taken. If nothing meaningful happened, the section can be brief or omitted.

**Leave the recap in the pause notes. `/pb-resume` Step 0 owns the archive write, not this command.** Step 0 surfaces the recap, classifies each finding, then archives it. Archiving it here skips all three: Step 0a's dedup check finds the entry already in the archive and correctly moves on, so the findings are never surfaced and never classified. Pre-archiving defeats the surfacing the archive exists to feed.

Where it lands is `/pb-resume`'s decision -- the project's recap archive, wherever this project's recaps already go. A project that has none starts one at `todos/done/lessons.md`, the default because `todos/` is gitignored and already holds the pause notes these continue. An existing archive stays where it is and keeps receiving entries: a second location forks the record whether or not a pointer connects them.

---

## Deep Mode

Run standard mode first, then continue with these steps.

### Step 5: Refresh Working Context

Run `/pb-context` to update the working context document:

```bash
# Verify currency
git describe --tags
git log --oneline -5
```

Update in working context:
- Current version (if changed)
- Recent commits section
- Active development section
- Session checklist commands still work

---

### Step 6: Update Project CLAUDE.md

Run `/pb-claude-project` if the session introduced:

- New patterns or conventions
- Architecture or structural changes
- Tech stack additions
- New commands or scripts
- Workflow changes

**When to skip:** Minor bug fixes, small features, no structural changes.

**Regenerate, then diff** -- `/pb-claude-project` preserves every `## Custom (Manual)` block verbatim, so a regen is the normal path, not a hazard. Compare against the backup and read for content that *vanished* rather than changed. Anything lost that analysis could not have derived belongs under that marker and never got there: put it there and regenerate again. Hand-editing around the generator is what lets the two drift apart in the first place.

---

### Step 7: Run any handoff the session wrote

Skip when the session produced no document another repo or person will follow. Otherwise `cd` to where the receiver will be standing and execute its opening moves -- see `/pb-handoff` Step 6.

A handoff pauses cleanly and reads correctly from inside the repo that wrote it, because that repo supplies every working directory, installed package and credential its instructions assume. Writing it is not verifying it, and the gap surfaces on the receiver's first five minutes rather than on yours.

---

## Cleanup (Optional, Extended Breaks)

For vacations, handoffs, or long breaks:

```bash
# Delete merged branches
git branch --merged main | grep -v main | xargs git branch -d

# Review and drop old stashes
git stash list
git stash drop stash@{n}
```

Additional checks:
- All work committed and pushed
- CI passing on current branch
- PR status clear (draft/ready/blocked)
- Team notified if applicable

---

## Integration with Playbook

```
/pb-start → [develop] → /pb-review → /pb-commit → /pb-ship
                ↕
        /pb-pause ←→ /pb-resume
```

**Deep mode runs:** `/pb-context` + `/pb-claude-project` (if needed)

---

## Related Commands

- `/pb-resume` - Get back into context after a break
- `/pb-start` - Begin work on a new feature or fix
- `/pb-standup` - Post async status update to team
- `/pb-handoff` - Write a handoff for another repo or person (deep Step 7 runs it)

---

*Future you will thank present you. Leave context, not mysteries.*
