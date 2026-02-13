---
name: "pb-pause"
title: "Pause Development Work"
category: "development"
difficulty: "advanced"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-resume', 'pb-start', 'pb-standup']
last_reviewed: "2026-02-13"
last_evolved: "2026-02-13"
version: "1.2.0"
version_notes: "v2.13.0: Context hygiene integrated — archives old pause entries, reports context health, trims session state"
breaking_changes: []
---
# Pause Development Work

Gracefully pause or conclude work on a project. Use this when stepping away for an extended period (days, weeks) or wrapping up a phase of work.

**Mindset:** Future you will resume this. Leave breadcrumbs that make recovery effortless. Apply `/pb-preamble` thinking: be honest about blockers. Apply `/pb-design-rules` thinking: document decisions and trade-offs.

**Resource Hint:** sonnet — state preservation, context hygiene, handoff documentation

---

## When to Use This Command

- **End of day** — Wrapping up work for the day
- **End of week** — Before weekend/time off
- **End of phase** — Completing a milestone or release phase
- **Context switch** — Moving to a different project
- **Extended break** — Vacation, leave, or long pause
- **Handoff** — Passing work to another developer

---

## Pause Checklist

### Step 1: Preserve Work State

Ensure no work is lost and current state is recoverable.

```bash
# Check current state
git status
git stash list

# Option A: Commit work in progress (preferred)
git add -A
git commit -m "wip: [describe current state]"

# Option B: Stash if not ready to commit
git stash push -m "WIP: [describe what's stashed]"

# Push to remote (backup)
git push origin $(git branch --show-current)
```

**Rule:** Never leave uncommitted work on a local-only branch overnight.

---

### Step 2: Update Trackers and Task Lists

Review and update all relevant tracking documents.

```bash
# Find project trackers
ls todos/*.md
ls todos/releases/*/

# Common tracker locations:
# - todos/project-review-*.md
# - todos/releases/vX.Y.Z/00-master-tracker.md
# - GitHub Issues / Project boards
```

**Update in trackers:**
- [ ] Mark completed tasks as done
- [ ] Update status of in-progress items
- [ ] Document blockers with specifics
- [ ] Note any scope changes
- [ ] Add newly discovered tasks

**Tracker update template:**
```markdown
## Status Update: [Date]

**Completed:**
- [x] Task A — finished [brief note]
- [x] Task B — finished [brief note]

**In Progress:**
- [ ] Task C — 70% complete, [what remains]

**Blocked:**
- [ ] Task D — blocked on [specific blocker]

**Discovered:**
- [ ] New task E — [discovered during work]

**Next Session:**
- Resume Task C
- [Priority items]
```

---

### Step 3: Review Project Documentation

Check that project review docs are current.

```bash
# Find the latest project review doc
ls -lt todos/project-review-*.md | head -1

# Or check for release-specific review
ls todos/releases/v*/project-review-*.md
```

**Review and update:**
- [ ] Decisions made during this session
- [ ] Technical debt identified
- [ ] Architecture considerations
- [ ] Open questions that need resolution
- [ ] Risks or concerns surfaced

---

### Step 4: Update Working Context

Run `/pb-context` to review and update the working context document.

```bash
# Verify working context exists
ls todos/*working-context*.md

# Check currency against actual state
git describe --tags
git log --oneline -5
```

**Update in working context:**
- [ ] Current version (if changed)
- [ ] Recent commits section
- [ ] Active development section
- [ ] Session checklist commands still work
- [ ] Any new patterns or conventions

---

### Step 5: Update CLAUDE.md (If Needed)

Run `/pb-claude-project` if significant changes were made:

- New patterns or conventions introduced
- Architecture changes
- Tech stack additions
- Workflow changes
- New commands or scripts

**When to skip:** Minor bug fixes, small features, no structural changes.

---

### Step 6: Write Pause Notes + Context Hygiene

This step does three things: writes the new pause entry, archives old entries, and reports context health.

**6a. Write concise pause entry:**

Replace the contents of `todos/pause-notes.md` (keep only the latest entry):

```markdown
# Pause Notes

Latest session pause context. Old entries archived to `todos/done/`.

---

## Pause: [Date] ([context])

**Branch:** [name] | **Commit:** [hash] - [message]

### Where I Left Off
- Working on: [what]
- Progress: [status]
- Blocked on: [if anything]

### Next Steps
1. [Immediate next action]
2. [Following action]

### Open Questions
- [Question] — [context]
```

Target: ~20-30 lines. Be specific about what's next. Skip sections that don't apply.

**6b. Archive old entries:**

If `todos/pause-notes.md` has entries beyond the latest, move old entries to `todos/done/`:

```bash
# Archive if needed (pb-pause should do this automatically)
# Old entries go to: todos/done/pause-notes-archive-YYYY-MM-DD.md
```

**6c. Report context health:**

Check all context layer sizes and flag anything that needs attention:

```bash
# Context health report
wc -l ~/.claude/CLAUDE.md                              # Global (target: ~140)
wc -l .claude/CLAUDE.md                                # Project (target: ~160)
# Memory is auto-managed (target: ~100)
wc -l todos/1-working-context.md                       # Working context (target: ~50)
wc -l todos/pause-notes.md                             # Pause notes (target: ~30)
```

**Flag if:**
- Working context hasn't been updated since last release → suggest `/pb-context`
- Pause notes has multiple entries → archive old ones
- Any context file is significantly over its soft budget

**Quick rule:** If the session was long, update working context with exact next step. Preserve state in files, not conversation.

---

### Step 7: Clean Up (Optional)

For end-of-phase or extended pauses:

```bash
# Review branches
git branch -a | grep -E "(feature|fix)/"

# Delete merged branches
git branch --merged main | grep -v main | xargs git branch -d

# Review stash
git stash list
git stash drop stash@{n}  # Drop old/irrelevant stashes

# Clean up local artifacts
make clean  # If available
rm -rf .cache/ tmp/  # Project-specific temp dirs
```

---

## Quick Pause (Short Breaks)

For short breaks (hours, not days):

```bash
# Minimum viable pause
git add -A
git commit -m "wip: [current state]" || git stash push -m "WIP: [state]"
git push origin $(git branch --show-current)

# Quick note in tracker
echo "## $(date): paused on [task], resume [next step]" >> todos/quick-notes.md
```

---

## Extended Pause Checklist

For vacations, handoffs, or long breaks:

- [ ] All work committed and pushed
- [ ] Trackers updated with current status
- [ ] Project review doc current
- [ ] Working context updated (`/pb-context`)
- [ ] CLAUDE.md updated if needed (`/pb-claude-project`)
- [ ] Handoff notes written
- [ ] Team notified (Slack, standup, etc.)
- [ ] PR status clear (draft/ready/blocked)
- [ ] CI passing on current branch
- [ ] No orphaned branches
- [ ] Stashes cleaned up or documented

---

## Pause vs. Stop

| Pause | Stop |
|-------|------|
| Temporary break | End of engagement |
| Context preserved | Context transferred |
| Branch stays active | Branch merged or closed |
| Minimal cleanup | Full cleanup |
| Update trackers | Archive trackers |

---

## Integration with Playbook

**Part of development workflow:**
```
/pb-start → /pb-cycle → /pb-commit → /pb-ship
     ↑                                   │
     │         ┌─────────────┐           │
     │         │   SESSION   │           ↓
     └─────────│   BOUNDARY  │       Reviews →
               └─────────────┘       PR → Merge →
                     ↑               Release
                     ↓
              /pb-resume ←──────── /pb-pause
              (recover)            (preserve)
```

**Commands:**
- `/pb-start` → Begin work, establish rhythm
- `/pb-resume` → Get back in context after break
- `/pb-cycle` → Iterate with reviews
- **`/pb-pause`** → Gracefully pause work (YOU ARE HERE)
- `/pb-commit` → Atomic commits
- `/pb-ship` → Full review → PR → release workflow

**Commands to run during pause:**
- `/pb-context` — Update working context
- `/pb-claude-project` — Update CLAUDE.md (if needed)

## Related Commands

- `/pb-resume` — Get back into context after a break
- `/pb-start` — Begin work on a new feature or fix
- `/pb-standup` — Post async status update to team

---

## Tips for Better Pauses

### Do
- Commit or stash everything
- Push to remote
- Update trackers immediately (don't defer)
- Write notes while context is fresh
- Be specific about blockers

### Don't
- Leave uncommitted work on local only
- Say "I'll remember" — you won't
- Skip tracker updates
- Leave WIP commits without explanation
- Assume context will be obvious later

---

## Recovery After Pause

When resuming, use `/pb-resume` to:
1. Check git state (branch, status, stash)
2. Sync with remote
3. Review working context
4. Read handoff notes
5. Verify environment
6. Run tests
7. Continue from documented next steps

---

*Future you will thank present you. Leave context, not mysteries.*
