---
name: "pb-context-review"
title: "Context Layer Review & Hygiene"
category: "templates"
difficulty: "intermediate"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-pause', 'pb-resume', 'pb-context', 'pb-claude-global', 'pb-claude-project']
last_reviewed: "2026-02-13"
last_evolved: ""
version: "1.0.0"
version_notes: "Initial release — context layer audit, deduplication, archival, health reporting"
breaking_changes: []
---
# Context Layer Review & Hygiene

**Purpose:** Audit, trim, and maintain all context layers. Keeps auto-loaded context lean and session state clean. Run after releases, quarterly, or when sessions feel slow to start.

**Mindset:** Context is necessary but expensive. Every line loaded into a session competes for attention. Apply `/pb-design-rules` thinking: Simplicity (remove what doesn't earn its place) and Clarity (what remains should be immediately useful). Apply `/pb-preamble` thinking: challenge whether each section is still relevant.

**Resource Hint:** sonnet — structured audit and maintenance workflow

---

## When to Use

- **After a release** — Trim release-specific details that are now historical
- **Quarterly** — Aligned with evolution cycles (Feb, May, Aug, Nov)
- **When sessions start slow** — Context bloat makes resumption expensive
- **Before starting a new evolution cycle** — Clean baseline for planning

---

## Context Architecture Reference

```
AUTO-LOADED (every session — budget matters most here):
  ~/.claude/CLAUDE.md              Global principles, BEACONs       ~140 lines
  .claude/CLAUDE.md                Project guardrails, tech stack    ~160 lines
  memory/MEMORY.md                 Index + active patterns           ~100 lines
                                                          Target: ~400 total

LOADED VIA /pb-resume (small, focused):
  todos/*working-context*          Project snapshot                   ~50 lines
  todos/pause-notes.md             Latest pause entry only            ~30 lines
                                                          Target:  ~80 total

ON-DEMAND (not auto-loaded — no budget pressure):
  memory/release-history.md        Ship logs by version
  memory/beacon-reference.md       Full 9-BEACON reference
  memory/session-templates.md      Templates for working-context + pause-notes
  memory/project-patterns.md       MkDocs anchors, conventions, verification
  memory/orchestration-lessons.md  Model selection, subagent patterns
  todos/done/*.md                  Archived session data
```

Targets are soft guidelines, not hard limits. Signal density matters more than line count.

---

## Step 1: Audit Layer Sizes

Report current sizes against targets.

```bash
# Auto-loaded layers
echo "=== Auto-loaded Context ==="
wc -l ~/.claude/CLAUDE.md                        # Target: ~140
wc -l .claude/CLAUDE.md                          # Target: ~160
wc -l <memory-path>/MEMORY.md                    # Target: ~100

# Session state (working-context filename varies by project)
echo "=== Session State ==="
ls -lh todos/*working-context* | head -1         # Locate working context file
wc -l todos/pause-notes.md                       # Target: ~30

# On-demand (informational only)
echo "=== On-demand Reference ==="
wc -l <memory-path>/*.md 2>/dev/null
ls -la todos/done/*.md 2>/dev/null | wc -l
```

**Interpret results:**

| Layer | Under Target | At Target | Over Target |
|-------|-------------|-----------|-------------|
| Auto-loaded | No action | No action | Review content, move details to topic files |
| Session state | No action | No action | Archive old entries, trim to snapshot |
| On-demand | No action | No action | No concern (not auto-loaded) |

---

## Step 2: Check for Duplication

Look for the same information repeated across layers. Common duplications:

**Version/release details:**
- Should appear in: working context (1 line per release)
- Should NOT appear in: Global CLAUDE.md, MEMORY.md (move to release-history.md)

**Project metrics (command count, test count):**
- Should appear in: working context (current state table)
- Should NOT appear in: Multiple places in MEMORY.md and CLAUDE.md

**BEACON definitions:**
- Should appear in: Global/Project CLAUDE.md (summaries only)
- Full reference in: memory/beacon-reference.md (on-demand)
- Should NOT appear in: MEMORY.md index

**Session management explanation:**
- Should NOT appear in: any auto-loaded file (the system works without explaining itself)
- Reference in: memory/session-templates.md (on-demand) or docs/

**Detection method:**
```bash
# Find repeated phrases across context files
# Look for version numbers, release dates, command counts
grep -l "v2.12.0" ~/.claude/CLAUDE.md .claude/CLAUDE.md <memory-path>/MEMORY.md todos/*working-context*
grep -l "98 commands" ~/.claude/CLAUDE.md .claude/CLAUDE.md <memory-path>/MEMORY.md todos/*working-context*
```

**Rule of thumb:** Each fact should have ONE canonical home. Other files cross-reference, not copy.

---

## Step 3: Archive Stale Session Data

Move completed work out of active files.

**Pause notes:**
```bash
# If pause-notes.md has more than 1 entry, archive old ones
# Keep only the latest entry in the active file
# Move old entries to: todos/done/pause-notes-archive-YYYY-MM-DD.md
```

**Working context sections:**
- Remove detailed task checklists for completed phases
- Remove quality gate logs for shipped releases
- Keep: version, status, metrics table, focus areas, next steps

**Todos directory cleanup:**
```bash
# Count files in todos/ (excluding subdirectories)
ls todos/*.md | wc -l

# Identify files older than current release cycle
ls -lt todos/*.md | tail -20

# Move completed session summaries, old implementation plans
# to todos/done/ or delete if archived elsewhere
```

---

## Step 4: Trim Auto-loaded Layers

For each auto-loaded file over its soft target, review content:

### Global CLAUDE.md (~/.claude/CLAUDE.md)

**Should contain:** BEACONs (6), operational guardrails, workflow commands, session ritual
**Should NOT contain:** Version-specific details, session management explanations, release promo

**Action:** If over ~140 lines, review and trim or regenerate via `/pb-claude-global`. If at target, no action needed.

### Project CLAUDE.md (.claude/CLAUDE.md)

**Should contain:** Tech stack, project structure, BEACONs (3), verification commands, relevant playbooks
**Should NOT contain:** Detailed phase descriptions, session management explanations, capability promo

**Action:** If over ~160 lines, review and trim or regenerate via `/pb-claude-project`. If at target, no action needed.

### Memory Index (memory/MEMORY.md)

**Should contain:** Current state (4 lines), active patterns, context architecture diagram, verification sequence, workflow lessons, context hygiene reminders, next evolution
**Should NOT contain:** Release histories (move to release-history.md), BEACON full reference (move to beacon-reference.md), templates (move to session-templates.md)

**Managed by:** Claude auto-memory (trim manually when over ~100 lines)

---

## Step 5: Verify Nothing Critical Was Lost

After trimming, verify:

```bash
# BEACONs still present in auto-loaded files
grep -c "BEACON" ~/.claude/CLAUDE.md              # Should be 6+
grep -c "BEACON" .claude/CLAUDE.md                 # Should be 3+

# Key commands still referenced
grep -c "/pb-" ~/.claude/CLAUDE.md                 # Should be 10+

# Project structure still documented
grep -c "commands/" .claude/CLAUDE.md              # Should be 1+

# Working context has current version (locate file for your project)
head -5 todos/*working-context* 2>/dev/null

# Memory index has architecture diagram
grep -c "AUTO-LOADED" <memory-path>/MEMORY.md      # Should be 1+
```

**If something critical was removed:** Check topic files (memory/*.md) and archives (todos/done/) — content was moved, not deleted.

---

## Step 6: Report

Summarize the review. Use this template:

```markdown
## Context Review: YYYY-MM-DD

### Layer Sizes (Before → After)
| Layer | Before | After | Target | Status |
|-------|--------|-------|--------|--------|
| Global CLAUDE.md | X | Y | ~140 | OK/OVER |
| Project CLAUDE.md | X | Y | ~160 | OK/OVER |
| Memory index | X | Y | ~100 | OK/OVER |
| Working context | X | Y | ~50 | OK/OVER |
| Pause notes | X | Y | ~30 | OK/OVER |
| **Auto-loaded total** | **X** | **Y** | **~400** | |

### Actions Taken
- [Action 1]
- [Action 2]

### Duplication Found
- [What was duplicated and where it was consolidated]

### Archived
- [What was moved to todos/done/ or topic files]
```

---

## Integration with /pb-pause

Daily context hygiene is embedded in `/pb-pause` (Step 6):
- Writes concise pause entry
- Archives old pause entries
- Reports context layer sizes

`/pb-context-review` is the **deeper audit** — run it quarterly or after releases for thorough cross-layer analysis. `/pb-pause` handles the daily maintenance.

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Never archiving pause notes | 650+ lines of historical entries | Archive after each resume |
| Copying info across layers | Same facts in 4 files | One canonical home, others cross-reference |
| Detailed task logs in working context | 243 lines when target is 50 | Keep snapshot, move details to done/ |
| Explaining the context system in context | Meta-context burns budget | System works without self-description |
| Hard line-count limits | Chasing numbers over signal | Soft targets, prioritize density |

---

## Related Commands

- `/pb-pause` — Daily context hygiene (archive + report) embedded in session boundary
- `/pb-resume` — Context loading with health check at session start
- `/pb-context` — Regenerate working context on release/milestone
- `/pb-claude-global` — Regenerate global CLAUDE.md from playbooks
- `/pb-claude-project` — Regenerate project CLAUDE.md from codebase analysis

---

**Last Updated:** 2026-02-13
**Version:** 1.0.0
