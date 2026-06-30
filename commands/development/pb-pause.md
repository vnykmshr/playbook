---
name: "pb-pause"
title: "Pause Development Work"
category: "development"
difficulty: "advanced"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-resume', 'pb-start', 'pb-standup']
last_reviewed: "2026-04-26"
last_evolved: "2026-06-30"
version: "1.5.0"
version_notes: "v1.5.0: Add Session Recap step — assistant-driven reflection surfaced at resume."
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

**When to use deep:** After releases, heavy sessions with structural changes, or before extended breaks. Standard mode's health check will flag stale context layers — that's your signal.

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

# Push to remote
git push origin $(git branch --show-current)
```

**Rule:** Never leave uncommitted work on a local-only branch overnight.

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

**3a. Write pause entry** — replace contents of `todos/pause-notes.md`:

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

**3b. Archive old entries** — if pause-notes has entries beyond the latest, move old entries to `todos/done/pause-notes-archive-YYYY-MM-DD.md`.

**3c. Context health check:**

```bash
wc -l ~/.claude/CLAUDE.md            # Global (target: ~160)
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

After the pause entry is written, reflect on the session and fill in the `### Session Recap` section of the pause notes. This is assistant-driven — the user does not fill it in.

**What to include:** Key observations (what was learned, what went wrong, what surprised you, what you'd do differently) and patterns/playbook feedback (did a playbook command mislead or help? is a command missing or wrong? did a workflow deviate and need correction?). Observations can target playbook commands, project workflows, or personal patterns.

**Depth:** Thorough reflection. Analyze the session's git log, conversation, decisions made, and paths not taken. If nothing meaningful happened, the section can be brief or omitted.

The recap is surfaced at `/pb-resume` and archived to `memory/lessons.md` after review.

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

---

*Future you will thank present you. Leave context, not mysteries.*
