---
name: "pb-resume"
title: "Resume Development Work"
category: "development"
difficulty: "advanced"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-start', 'pb-pause', 'pb-cycle']
last_reviewed: "2026-02-13"
last_evolved: "2026-02-13"
version: "1.2.0"
version_notes: "v2.13.0: Streamlined context loading — reports actual sizes, flags stale data, concise health check"
breaking_changes: []
---
# Resume Development Work

Quickly get back into context after a break. Use this to resume work on an existing feature branch.

**Mindset:** Resuming requires understanding assumptions made and verifying context is complete. Apply `/pb-preamble` thinking: challenge what was decided and why. Apply `/pb-design-rules` thinking: is the code clear, simple, and robust?

**Resource Hint:** sonnet — context recovery, state assessment, health check

---

## When to Use

- Returning to work after a break (hours, days, or weeks)
- Picking up someone else's in-progress feature branch
- Resuming after a session compaction or context window reset

---

## Quick Context Recovery

### Step 1: Check Current State

```bash
# What branch am I on?
git branch --show-current

# What's the status?
git status

# What did I do last?
git log --oneline -5

# Any stashed work?
git stash list
```

### Step 2: Sync with Remote

```bash
# Fetch latest from origin
git fetch origin

# Check if main has moved
git log --oneline HEAD..origin/main

# Rebase if needed
git rebase origin/main
```

### Step 3: Review Recent Work

```bash
# See what changed on this branch
git log origin/main..HEAD --oneline

# See uncommitted changes
git diff

# See staged changes
git diff --staged
```

---

### Step 3.5: Load Session State + Context Health Check

Read the session state files and check context health.

**Load session state:**

```bash
# Read working context (project snapshot)
cat todos/1-working-context.md

# Read latest pause notes (where you left off)
cat todos/pause-notes.md
```

**Context health check — report actual sizes:**

```bash
# Auto-loaded layers (already in context):
wc -l ~/.claude/CLAUDE.md            # Global principles (target: ~140)
wc -l .claude/CLAUDE.md              # Project guardrails (target: ~160)
# memory/MEMORY.md                   # Auto-loaded by Claude (target: ~100)

# Session state (loaded manually):
wc -l todos/1-working-context.md     # Project snapshot (target: ~50)
wc -l todos/pause-notes.md           # Latest pause entry (target: ~30)
```

**Flag issues:**
- Working context version doesn't match `git describe --tags` → run `/pb-context`
- Pause notes has multiple entries → old entries should have been archived by `/pb-pause`
- Any layer missing → run the appropriate regeneration command

**Recovery if context is stale:**
- `/pb-context` — regenerate working context
- `/pb-claude-project` — regenerate project CLAUDE.md
- `/pb-claude-global` — regenerate global CLAUDE.md

---

## Session Context Template

When resuming, establish context:

```
Resuming work on: [branch-name]

## Where I Left Off
- Last commit: [commit message]
- In progress: [what was being worked on]
- Blocked on: [if anything]

## Current Status
- [ ] Task 1: [status]
- [ ] Task 2: [status]
- [ ] Task 3: [status]

## Next Steps
1. [Immediate next action]
2. [Following action]

## Open Questions
- [Any unresolved questions]
```

---

## Common Resume Scenarios

### Scenario A: Clean Stop (all committed)

```bash
# Just verify and continue
git status                    # Should be clean
git log --oneline -3          # Review last commits
# Continue with next task
```

### Scenario B: Work in Progress (uncommitted changes)

```bash
# Review what's uncommitted
git diff
git diff --staged

# Option 1: Continue where you left off
# Just keep working

# Option 2: Stash and start fresh
git stash push -m "WIP: description"
# Work on something else
git stash pop  # When ready to resume
```

### Scenario C: Main Has Moved Ahead

```bash
# Rebase your branch
git fetch origin
git rebase origin/main

# Resolve conflicts if any
# Continue working
```

### Scenario D: Long Break (days/weeks)

```bash
# Full context recovery
git fetch origin
git log --oneline origin/main..HEAD  # Your changes
git log --oneline HEAD..origin/main  # What you missed

# Check for pause notes (left by /pb-pause)
cat todos/pause-notes.md 2>/dev/null | tail -50

# Read relevant docs/issues for context
# Review your branch changes thoroughly
git diff origin/main...HEAD

# Rebase and continue
git rebase origin/main
```

**If pause notes exist:** Follow documented next steps, verify blockers resolved.

---

## Recovery Checklist

Before continuing work:

- [ ] On correct branch
- [ ] Branch is up to date with main
- [ ] Checked pause notes (`todos/pause-notes.md`)
- [ ] Understand what was last done
- [ ] Know what's next
- [ ] Working context is current (if project has one)
- [ ] Dev environment running (`make dev`)
- [ ] Tests pass (`make test`)

---

## Quick Commands

| Action | Command |
|--------|---------|
| Current branch | `git branch --show-current` |
| Recent commits | `git log --oneline -5` |
| Uncommitted changes | `git diff` |
| Staged changes | `git diff --staged` |
| Stash list | `git stash list` |
| Pop stash | `git stash pop` |
| Fetch origin | `git fetch origin` |
| Rebase on main | `git rebase origin/main` |

---

## Reading and Updating Working Context

For project-level context:

```bash
# Check for working context (location and naming may vary)
ls todos/*working-context*.md 2>/dev/null

# Read project working context (or run /pb-context)
cat todos/working-context.md

# Check release tracker if on a release branch
cat todos/releases/v1.X.0/00-master-tracker.md
```

**Common locations:** `todos/working-context.md`, `todos/1-working-context.md`

**Working context currency check:**
```bash
# Compare working context version with actual state
git describe --tags                    # Current version
git log --oneline -5                   # Recent commits
```

If the working context is stale (version mismatch, outdated commits, missing recent releases):
1. Run `/pb-context` to review and update
2. Update version, date, recent commits, and active development sections
3. Verify session checklist commands still work

---

## Reading Pause Notes

If you (or someone else) used `/pb-pause` before stopping, look for handoff context:

```bash
# Check for pause notes
cat todos/pause-notes.md 2>/dev/null | tail -50

# Or grep for your branch
grep -A 30 "$(git branch --show-current)" todos/pause-notes.md
```

**Pause notes contain:**
- Where work left off (last commit, in-progress items)
- Current task status
- Next steps (prioritized)
- Open questions and blockers
- Gotchas and environment notes

**After reading pause notes:**
1. Verify current state matches documented state
2. Check if blockers have been resolved
3. Review next steps and adjust if needed
4. Clear old pause notes once context is recovered

```bash
# Archive old pause notes (optional)
mv todos/pause-notes.md todos/pause-notes-$(date +%Y%m%d).md
```

---

## If Completely Lost

```bash
# 1. What branches exist?
git branch -a

# 2. What branch was I on?
git reflog | head -20

# 3. What work exists?
git log --all --oneline --graph -20

# 4. Read the working context
# /pb-standards for patterns
# /pb-context for project context and decision log
# /pb-guide for SDLC framework reference
```

---

## Session State Preservation

See `/pb-claude-orchestration` for comprehensive context management strategies including:
- What to preserve before ending a session
- Strategic compaction timing (when to compact vs. when not to)
- Session notes template
- Resuming after compaction

**Key insight**: Compact at logical transition points, not mid-task. Manual compaction at boundaries preserves context better than automatic compaction at arbitrary points.

---

## Tips for Better Resume

### Before Stopping Work (Use `/pb-pause`)

Run `/pb-pause` before stepping away. It guides you through:

1. **Preserve work state** — Commit or stash, push to remote
2. **Update trackers** — Mark progress, document blockers
3. **Update context** — Run `/pb-context`, `/pb-claude-project` if needed
4. **Write pause notes** — Document where you left off in `todos/pause-notes.md`

**Quick pause (short breaks):**
```bash
git add -A && git commit -m "wip: [state]" && git push
```

### When Resuming

1. **Start with status** - `git status` first
2. **Read before writing** - Review recent commits
3. **Verify environment** - Ensure services running
4. **Run tests** - Confirm baseline is green
5. **Post standup** - Write /pb-standup to align with team

### Context Efficiency on Resume

If previous session was long or context-heavy:

1. **Start fresh** — Don't try to continue exhausted context
2. **Load minimal context** — Tracker + active file only
3. **Reference by commit** — Use git log, not re-reading entire files
4. **Use subagents** — Exploration tasks in separate context

See `/pb-cycle` Step 7 for context checkpoint guidance.
See `/pb-claude-global` Context Management section for efficiency patterns.

---

## Related Commands

- `/pb-start` — Begin work on a new feature or fix
- `/pb-pause` — Gracefully pause work and preserve context
- `/pb-cycle` — Self-review and peer review during development

---

*Context is expensive to rebuild. Leave breadcrumbs for future you.*
