# Resume Development Work (v2.12.0 Enhanced)

Quickly get back into context after a break. Use this to resume work on an existing feature branch.

**Mindset:** Resuming work requires understanding assumptions and decisions made.

Use `/pb-preamble` thinking: challenge your assumptions about what was decided and why. Use `/pb-design-rules` thinking: understand how the design embodies Clarity (is the code obvious?), Simplicity (are we solving this the simplest way?), and Robustness (are error cases handled?).

**Resource Hint:** sonnet — context recovery and state assessment

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

### Step 3.5: Load All Context Layers in Sequence (NEW - v2.12.0)

Before proceeding, load and verify all 4 layers of project context.

**Four-Layer Context Architecture:**

Layer loading sequence for optimal context recovery:

```
Layer 1: Global CLAUDE.md (190 lines)
  → Universal principles, 6 global BEACONs
  → Location: ~/.claude/CLAUDE.md
  → Content: How We Work, Design Rules, Code Quality, Non-Negotiables, Quality Bar, Model Selection

Layer 2: Project CLAUDE.md (178 lines)
  → Project structure and patterns, 3 project BEACONs
  → Location: .claude/CLAUDE.md (in repository)
  → Content: Tech Stack, Project Structure, Commands, Guardrails, Audit Conventions, Key Patterns

Layer 3: Memory (336 lines)
  → Persistent learned patterns, BEACON Quick Reference
  → Location: memory/MEMORY.md (auto-memory)
  → Content: Operational patterns, BEACON reference, templates, session context strategy

Layer 4: Session State
  → Durable (working-context.md) + Ephemeral (pause-notes.md)
  → Location: todos/1-working-context.md, todos/pause-notes.md
  → Content: Project state, version info, pause checkpoints, next steps
```

**Loading display (show to user):**

```
=== RESUMING: Loading Context Layers ===

Loading context layers in sequence...

Layer 1: Global (~/.claude/CLAUDE.md)
  Principles loaded: ✓
  BEACONs loaded: ✓ (6 global)
  Size: 190 lines

Layer 2: Project (.claude/CLAUDE.md)
  Structure loaded: ✓
  BEACONs loaded: ✓ (3 project)
  Size: 178 lines

Layer 3: Memory (memory/MEMORY.md)
  Patterns loaded: ✓
  BEACON Reference loaded: ✓
  Size: 336 lines

Layer 4: Session State (todos/)
  Working-context loaded: ✓
  Pause-notes loaded: ✓
  Status: Available for review

=== Context Layers: ALL LOADED ===
```

**Verify context layers loaded:**

```bash
# Verify each layer exists and is readable
[ -f ~/.claude/CLAUDE.md ] && echo "✓ Global context found"
[ -f ./.claude/CLAUDE.md ] && echo "✓ Project context found"
[ -f ./memory/MEMORY.md ] && echo "✓ Memory found"
[ -f ./todos/1-working-context.md ] || [ -f ./todos/working-context.md ] && echo "✓ Working context found"
[ -f ./todos/pause-notes.md ] && echo "✓ Pause-notes found"
```

**If layer missing:**
```
⚠️  CONTEXT LAYER MISSING
Missing: [Layer name]
Run: /pb-context (to refresh working context)
Run: /pb-claude-project (to refresh project CLAUDE.md)
```

---

### Step 3.6: Confirm All BEACONs Active (NEW - v2.12.0)

After loading all 4 context layers, verify all 9 critical guidelines are active.

**What are BEACONs?** Critical guidelines explicitly marked in CLAUDE.md files to prevent oversight when guidance is deferred to playbooks.

**Verify all 9 BEACONs:**

```
=== BEACON VERIFICATION ===

Global BEACONs (6) from ~/.claude/CLAUDE.md:
✓ BEACON: Preamble — Challenge assumptions, think like peers
✓ BEACON: Design Rules — Clarity, Simplicity, Resilience, Extensibility
✓ BEACON: Code Quality — No dead code, atomic changes, error handling
✓ BEACON: Non-Negotiables — Never ship bugs, always test, always verify
✓ BEACON: Quality Bar (MLP) — Would you use daily? Can recommend? Minimal?
✓ BEACON: Model Selection — Opus/Sonnet/Haiku routing

Project BEACONs (3) from .claude/CLAUDE.md:
✓ BEACON: Project Guardrails — Command count, categories, metadata, linting
✓ BEACON: Audit Conventions — 274 automated verifications
✓ BEACON: Key Patterns — Bidirectional links, dropped references, anchors

All 9 BEACONs verified and active ✓
```

**If BEACON missing:**

```
⚠️  BEACON VERIFICATION FAILED
Missing: [BEACON name]
Severity: [Critical / High / Medium]
Guidance: See `/pb-[command]` for full guidance
Action required: Read BEACON definition before proceeding
```

**Recovery if BEACONs incomplete:**
1. Run `/pb-context` to refresh working context
2. Run `/pb-claude-project` to refresh project CLAUDE.md
3. Re-read memory/MEMORY.md to restore operational patterns
4. Re-verify all 9 BEACONs before continuing

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

## BEACONs Status
- [x] All 9 BEACONs verified and active
- Guidelines loaded and ready
```

---

## Common Resume Scenarios

### Scenario A: Clean Stop (all committed)

```bash
# Just verify and continue
git status                    # Should be clean
git log --oneline -3          # Review last commits
# Load context layers (Step 3.5-3.6)
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
# Load context layers (Step 3.5-3.6)
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

# Load context layers (Step 3.5-3.6)
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
- [ ] **All 4 context layers loaded** ← NEW
- [ ] **All 9 BEACONs verified active** ← NEW
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
- **BEACONs Verified checkpoint** ← NEW

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

# 4. Load context layers (Step 3.5-3.6)
# 5. Read the working context
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
5. **Verify BEACONs** — Confirm all 9 guidelines loaded and documented ← NEW

**Quick pause (short breaks):**
```bash
git add -A && git commit -m "wip: [state]" && git push
```

### When Resuming

1. **Start with status** - `git status` first
2. **Load context layers** - Steps 3.5-3.6 ← NEW
3. **Verify BEACONs** - Confirm all 9 guidelines active ← NEW
4. **Read before writing** - Review recent commits
5. **Verify environment** - Ensure services running
6. **Run tests** - Confirm baseline is green
7. **Post standup** - Write /pb-standup to align with team

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
- `/pb-pause` — Gracefully pause work and preserve context (now with BEACON verification)
- `/pb-cycle` — Self-review and peer review during development

---

*Context is expensive to rebuild. Leave breadcrumbs for future you. Load all layers. Verify BEACONs.*

---

**Version:** 2.12.0 (Phase 2 Enhancement)
**Last Updated:** 2026-02-12
