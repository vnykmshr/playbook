---
name: "beacon-verification"
title: "BEACON Verification at Session Boundaries"
category: "documentation"
document_type: "guide"
audience: ["developers", "claude-code-users"]
related_commands: ['pb-pause', 'pb-resume', 'pb-context', 'pb-claude-project']
last_reviewed: "2026-02-12"
version: "1.0.0"
version_notes: "v2.12.0 Phase 1: Foundation for BEACON system"
---

# BEACON Verification at Session Boundaries

**Context:** This guide explains how the BEACON system (critical guidelines) works at pause/resume boundaries to prevent silent loss of important constraints during session transitions.

---

## What Are BEACONs?

BEACONs are critical, always-active guidelines that are explicitly marked in CLAUDE.md context files. Each BEACON has **dual presence:**
- **Summary in context files** — Quick reference (prevents forgetting)
- **Full detail in playbooks** — Comprehensive guidance (prevents misunderstanding)

This dual-presence architecture ensures guidelines are never silently lost, even when context switches.

### Why BEACONs Matter at Pause/Resume Boundaries

When you pause work (end of day, context switch, extended break), your session ends and context is unloaded. When you resume, you must reload that context. **Without explicit BEACON verification:**
- Guidelines become invisible during the switch
- You might forget important constraints
- Code quality or safety standards could be violated
- Architectural decisions could be circumvented

**With BEACON verification at boundaries:**
- Guidelines are explicitly listed before pausing
- Guidelines are explicitly verified on resuming
- Silent loss is prevented
- Safety is maintained

---

## Four-Layer Context Architecture

Understanding how context layers work is essential for proper BEACON verification.

### Layer 1: Global Context (~/.claude/CLAUDE.md)

**Purpose:** Universal principles that apply to ALL projects

**Content (190 lines):**
- 6 global BEACONs
- Universal development philosophy
- Design principles
- Code quality standards

**6 Global BEACONs:**
1. **BEACON: Preamble** — How we think (challenge assumptions, peer collaboration)
2. **BEACON: Design Rules** — What we build (Clarity, Simplicity, Resilience)
3. **BEACON: Code Quality** — How we write (no dead code, atomic changes)
4. **BEACON: Non-Negotiables** — Minimum bar (never ship bugs, always test)
5. **BEACON: Quality Bar (MLP)** — Completion criteria (would you use daily?)
6. **BEACON: Model Selection** — Resource routing (Opus/Sonnet/Haiku)

**Location:** `~/.claude/CLAUDE.md` (user config, not in repository)

**Update frequency:** Quarterly (with each Claude capability update)

---

### Layer 2: Project Context (.claude/CLAUDE.md)

**Purpose:** Project-specific structure, patterns, and conventions

**Content (178 lines):**
- 3 project BEACONs
- Tech stack and tools
- Project structure
- Key commands
- Project-specific patterns

**3 Project BEACONs:**
1. **BEACON: Project Guardrails** — Structural constraints (command count, categories, metadata)
2. **BEACON: Audit Conventions** — Quality enforcement (274 automated verifications)
3. **BEACON: Key Patterns** — Operational consistency (bidirectional links, MkDocs anchors)

**Location:** `.claude/CLAUDE.md` (in repository root)

**Update frequency:** Per release or major structural change

---

### Layer 3: Memory (memory/MEMORY.md)

**Purpose:** Persistent patterns and BEACON quick reference

**Content (336 lines):**
- BEACON Quick Reference (all 9 BEACONs listed)
- Workflow lessons and patterns
- Verification sequences
- Project conventions
- Audit guidelines

**What it contains:**
- Complete list of all 9 BEACONs with descriptions
- When to apply each BEACON
- Links to full playbook details
- Why each BEACON is critical

**Location:** `memory/MEMORY.md` (auto-memory directory, persists across sessions)

**Update frequency:** Continuous (as patterns are learned)

**Special role in pause/resume:** Serves as BEACON reference card for verification

---

### Layer 4: Session State

**Purpose:** Temporary state for current session and handoff to next session

**Durable (survives sessions):**
- **Location:** `todos/1-working-context.md`
- **Content:** Project state, version info, active development, next release planning
- **Maintenance:** Updated on releases, quarterly reviews, major changes
- **Never delete:** Accumulates project history

**Ephemeral (can be archived after use):**
- **Location:** `todos/pause-notes.md`
- **Content:** Where work left off, current status, next steps, blockers, environment notes
- **Maintenance:** Updated at each pause via `/pb-pause`
- **Lifecycle:** Append, read on `/pb-resume`, archive after resumption

**Special role in pause/resume:** Records BEACON verification checkpoint

---

## BEACON Verification at Pause Boundary

### When to Pause

Common scenarios:
- End of workday
- End of week (Friday evening)
- Extended time off (vacation, leave)
- Context switch (moving to different project)
- End of development phase

### What Happens at Pause

**Step 1: Preserve Work**
```bash
git commit -m "wip: [state]"
git push origin [branch]
```

**Step 2-6: Update Context**
- Update project trackers
- Update working-context
- Update CLAUDE.md if needed
- Write pause-notes with next steps

**NEW Step 6.5: Verify BEACONs**

```
Display to user:
=== PAUSING: Verifying Active BEACONs ===

Global BEACONs (6):
✓ BEACON: Preamble
✓ BEACON: Design Rules
✓ BEACON: Code Quality
✓ BEACON: Non-Negotiables
✓ BEACON: Quality Bar (MLP)
✓ BEACON: Model Selection

Project BEACONs (3):
✓ BEACON: Project Guardrails
✓ BEACON: Audit Conventions
✓ BEACON: Key Patterns

Critical guidelines preserved: All 9 BEACONs loaded ✓
```

**Add to pause-notes:**
```markdown
### BEACONs Verified
- [x] All 9 critical guidelines loaded and active
- Guidelines preserved for resume session
- Status: Ready for context switch
```

### Why BEACON Verification Before Pausing?

1. **Confirms guidelines are in context** — Not forgotten
2. **Creates handoff checkpoint** — Next session knows guidelines were verified
3. **Prevents silent loss** — If BEACON missing, you'll be warned before pausing
4. **Documents state** — Pause-notes checkpoint proves guidelines were preserved

---

## BEACON Verification at Resume Boundary

### When to Resume

Common scenarios:
- Same day, coming back after break
- Next day, resuming yesterday's work
- After context switch, returning to project
- After context compaction, restoring session

### What Happens at Resume

**Step 1-3: Recover Git State**
```bash
git status
git fetch origin
git log origin/main..HEAD
```

**NEW Step 3.5: Load All Context Layers in Sequence**

Display to user:
```
=== RESUMING: Loading Context Layers ===

Layer 1: Global (~/.claude/CLAUDE.md)
  Principles: ✓ | BEACONs: ✓ (6) | Size: 190 lines

Layer 2: Project (.claude/CLAUDE.md)
  Structure: ✓ | BEACONs: ✓ (3) | Size: 178 lines

Layer 3: Memory (memory/MEMORY.md)
  Patterns: ✓ | BEACON Reference: ✓ | Size: 336 lines

Layer 4: Session State (todos/)
  Working-context: ✓ | Pause-notes: ✓

=== All Context Layers: LOADED ===
```

**NEW Step 3.6: Verify All BEACONs Active**

Display to user:
```
=== BEACON VERIFICATION ===

Global BEACONs (6):
✓ BEACON: Preamble
✓ BEACON: Design Rules
✓ BEACON: Code Quality
✓ BEACON: Non-Negotiables
✓ BEACON: Quality Bar (MLP)
✓ BEACON: Model Selection

Project BEACONs (3):
✓ BEACON: Project Guardrails
✓ BEACON: Audit Conventions
✓ BEACON: Key Patterns

All 9 BEACONs verified and active ✓
Session ready to continue.
```

### If BEACON Missing on Resume

If `/pb-resume` detects a BEACON missing:

```
⚠️  BEACON VERIFICATION FAILED
Missing: [BEACON name]
Severity: [Critical / High]

Recovery:
1. Run: /pb-context (refresh working-context)
2. Run: /pb-claude-project (refresh project CLAUDE.md)
3. Re-read: memory/MEMORY.md (restore patterns)
4. Re-verify BEACONs before proceeding

Guidance: Read /pb-[command] for full BEACON details
```

**Common causes and fixes:**

| Missing BEACON | Cause | Fix |
|---|---|---|
| Preamble / Design Rules | Global context not loaded | Run `/pb-claude-global` |
| Project Guardrails | Project context stale | Run `/pb-claude-project` |
| Audit Conventions | CLAUDE.md not updated | Run `/pb-claude-project` |
| Any BEACON | Context compaction | Start fresh session |

---

## Real-World Example: Pause→Resume Cycle

### Scenario: Pausing Friday Evening

**5:00 PM Friday: Developer pauses work**

```
User runs: /pb-pause

System displays:
  ✓ Work state preserved (committed and pushed)
  ✓ Trackers updated
  ✓ Pause-notes written
  ✓ BEACONs verified: All 9 loaded ✓

Pause-notes captures:
  Branch: feature/user-auth
  Last commit: "feat: add password validation"
  Next steps:
    1. Add email verification endpoint
    2. Write integration tests
    3. Update API docs
  BEACONs Verified: All 9 active ✓
  Checkpoint: Ready for Monday resume
```

**Developer closes laptop. Session ends. Context unloaded.**

---

### Scenario: Resuming Monday Morning

**9:00 AM Monday: Developer resumes work**

```
User runs: /pb-resume

System displays:
  ✓ Git state checked (branch: feature/user-auth)
  ✓ Remote synced

  === RESUMING: Loading Context Layers ===

  Layer 1: Global (~/.claude/CLAUDE.md) ✓
  Layer 2: Project (.claude/CLAUDE.md) ✓
  Layer 3: Memory (memory/MEMORY.md) ✓
  Layer 4: Session State (todos/) ✓

  === All Context Layers: LOADED ===

  === BEACON VERIFICATION ===

  Global (6): ✓ All active
  Project (3): ✓ All active

  All 9 BEACONs verified and active ✓
  Session ready to continue.

Recovered context:
  - Last commit: "feat: add password validation"
  - Next steps (from pause-notes):
    1. Add email verification endpoint
    2. Write integration tests
    3. Update API docs
  - BEACONs reminder: Never ship without comprehensive tests (Non-Negotiables)
```

**Developer is fully oriented. No guideline loss. Safe to continue.**

---

## BEACON Mapping to Pause/Resume Flow

Here's how each BEACON applies at boundaries:

### Global BEACONs

1. **BEACON: Preamble** at pause/resume
   - Before pausing: "Have I documented my assumptions clearly?"
   - On resume: "What assumptions did I make? Are they still valid?"

2. **BEACON: Design Rules** at pause/resume
   - Before pausing: "Is my design clear and simple?"
   - On resume: "Do I still understand why I designed it this way?"

3. **BEACON: Code Quality** at pause/resume
   - Before pausing: "No debug artifacts or dead code?"
   - On resume: "What quality standards apply to my next changes?"

4. **BEACON: Non-Negotiables** at pause/resume
   - Before pausing: "All tests passing?"
   - On resume: "What's the minimum quality bar?"

5. **BEACON: Quality Bar** at pause/resume
   - Before pausing: "Would I use this? Can I recommend it?"
   - On resume: "How complete is this work?"

6. **BEACON: Model Selection** at pause/resume
   - Before pausing: "What resources did I use?"
   - On resume: "What resources should I use?"

### Project BEACONs

1. **BEACON: Project Guardrails** at pause/resume
   - Before pausing: "Have I maintained project stability?"
   - On resume: "What project constraints apply?"

2. **BEACON: Audit Conventions** at pause/resume
   - Before pausing: "Do all my changes meet conventions?"
   - On resume: "What conventions must I follow?"

3. **BEACON: Key Patterns** at pause/resume
   - Before pausing: "Are all references bidirectional?"
   - On resume: "What patterns should I follow?"

---

## Troubleshooting: "What If a BEACON Is Missing?"

### Scenario 1: BEACON Missing on Pause

**Symptom:** Running `/pb-pause` shows BEACON not loaded

**Recovery:**
```bash
# Option A: Load the BEACON immediately
/pb-context                  # Refresh working-context
/pb-claude-project          # Refresh project CLAUDE.md

# Option B: Skip pause, get context first
# (Recommended for critical BEACONs)
```

**Prevention:** Don't pause until all BEACONs show as loaded

---

### Scenario 2: BEACON Missing on Resume

**Symptom:** Running `/pb-resume` reports missing BEACON

**Recovery:**
```bash
# Step 1: Identify which layers need reloading
/pb-claude-global           # Reload global guidelines
/pb-claude-project          # Reload project structure
/pb-context                 # Refresh working-context

# Step 2: Read the missing BEACON
# (e.g., if "Design Rules" missing, read /pb-design-rules)

# Step 3: Re-verify BEACONs
/pb-resume                  # Re-run resume with refreshed context
```

**Prevention:** Run `/pb-context` and `/pb-claude-project` at start of each day

---

### Scenario 3: Context Compaction Lost BEACONs

**Symptom:** Session resumed after context compaction, BEACONs not found

**Recovery:**
```bash
# Context compaction cleared old context, start fresh

# Step 1: Reload all layers fresh
Start new session, which loads:
  - ~/.claude/CLAUDE.md (fresh)
  - ./.claude/CLAUDE.md (fresh)
  - memory/MEMORY.md (fresh)
  - todos/ (fresh)

# Step 2: Verify BEACONs
All 9 should be present in fresh layers

# Step 3: Read pause-notes for context
cat todos/pause-notes.md | tail -30
```

**Prevention:** Save pause-notes checkpoint before extended sessions that might trigger compaction

---

## Key Takeaways

1. **BEACONs prevent silent guideline loss** at session boundaries
2. **Pause verifies** guidelines are loaded before context switches
3. **Resume confirms** guidelines are active after context restores
4. **Four layers** ensure complete context recovery
5. **All 9 BEACONs** must be verified at boundaries
6. **Documentation** (pause-notes) ensures nothing is forgotten

---

## Integration with Development Workflow

```
/pb-start (begin work)
    ↓
/pb-cycle (iterate)
    ↓
/pb-pause (end session)
    ├─ Step 6.5: Verify 9 BEACONs ← YOU ARE HERE
    └─ checkpoint: BEACONs preserved

    [Time passes, context lost]

/pb-resume (restart session)
    ├─ Step 3.5: Load 4-layer context
    ├─ Step 3.6: Verify 9 BEACONs ← AND HERE
    └─ continue with next steps
```

---

## Related Commands

- `/pb-pause` — Pause work with BEACON verification
- `/pb-resume` — Resume work with BEACON loading
- `/pb-preamble` — Full Preamble BEACON details
- `/pb-design-rules` — Full Design Rules BEACON details
- `/pb-standards` — Full Code Quality BEACON details
- `/pb-guide` — Full Non-Negotiables & Quality Bar
- `/pb-claude-orchestration` — Model Selection BEACON details
- `/pb-context` — Update working context (refresh BEACONs)
- `/pb-claude-project` — Update project CLAUDE.md (refresh BEACONs)

---

**Version:** 2.12.0 (Phase 2 - Pause/Resume Enhancement)
**Last Updated:** 2026-02-12
**Status:** Implementation Guide
