---
name: "pb-pause"
title: "Pause Development Work"
category: "development"
difficulty: "advanced"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-resume', 'pb-start', 'pb-standup']
last_reviewed: "2026-02-09"
last_evolved: ""
---
# Pause Development Work

Gracefully pause or conclude work on a project. Use this when stepping away for an extended period (days, weeks) or wrapping up a phase of work.

**Mindset:** Future you (or a teammate) will resume this work. Leave breadcrumbs that make context recovery effortless.

Use `/pb-preamble` thinking: be honest about blockers and incomplete work. Use `/pb-design-rules` thinking: document decisions and trade-offs made during development.

**Resource Hint:** sonnet — state preservation and handoff documentation

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

### Step 6: Document Handoff Context

Leave clear notes for resumption (yourself or others).

**Pause notes location:** `todos/pause-notes.md` (append to this file)

```bash
# Create or append to pause notes
cat >> todos/pause-notes.md << 'EOF'
---
EOF
```

**Pause note template** (matches what `/pb-resume` expects):
```markdown
## Pause Context: [Date]

**Branch:** [branch-name]
**Last commit:** [commit hash + message]

### Where I Left Off
- Last commit: [commit message]
- In progress: [what was being worked on]
- Blocked on: [if anything]

### Current Status
- [x] Task 1: completed
- [ ] Task 2: [status/progress]
- [ ] Task 3: pending

### Next Steps
1. [Immediate next action when resuming]
2. [Following action]
3. [Third priority]

### Open Questions
- [Question 1 — who can answer]
- [Question 2 — needs investigation]

### Gotchas / Things to Remember
- [Non-obvious thing that might be forgotten]
- [Workaround or temporary hack to be aware of]

### Environment Notes
- [Any special setup needed]
- [Services that need to be running]
```

**Tip:** `/pb-resume` will look for this file — keep notes structured for easy scanning.

### Context State Preservation

Before pausing, assess context health. See `/pb-claude-orchestration` for detailed context management strategies.

**Quick rule:** If the session was long (many file reads, multiple iterations), update tracker with exact next step and commit hash. Preserve state in files, not conversation.

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
