---
name: "pb-pause"
title: "Pause Development Work"
category: "development"
difficulty: "advanced"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-resume', 'pb-start', 'pb-standup']
last_reviewed: "2026-03-28"
last_evolved: "2026-03-28"
version: "1.3.0"
version_notes: "v2.20.0: Two-tier mode system (standard/deep), content consolidation, leaner pause notes template"
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
git add -A && git commit -m "wip: [current state]" && git push
```

That's it. No pause notes, no health check. Use `/pb-pause` when you need to preserve context for future-you or someone else.

---

## Standard Mode (Default)

### Step 1: Preserve Work State

```bash
git status
git stash list

# Option A: Commit (preferred)
git add -A
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
```

Target: ~20-30 lines. Be specific about what's next. Skip sections that don't apply.

**3b. Archive old entries** — if pause-notes has entries beyond the latest, move old entries to `todos/done/pause-notes-archive-YYYY-MM-DD.md`.

**3c. Context health check:**

```bash
wc -l ~/.claude/CLAUDE.md            # Global (target: ~140)
wc -l .claude/CLAUDE.md              # Project (target: ~160)
# memory/MEMORY.md                   # Auto-loaded (target: ~100)
wc -l todos/1-working-context.md     # Working context (target: ~50)
wc -l todos/pause-notes.md           # Pause notes (target: ~30)
```

Flag if:
- Working context version doesn't match `git describe --tags` → stale, consider `/pb-pause deep`
- Pause notes has multiple entries → archive old ones
- Any layer significantly over its soft budget

---

## Deep Mode

Run standard mode first, then continue with these steps.

### Step 4: Refresh Working Context

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

### Step 5: Update Project CLAUDE.md

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
