---
name: "pb-context-review"
title: "Context Layer Review & Hygiene"
category: "templates"
difficulty: "intermediate"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-pause', 'pb-resume', 'pb-context', 'pb-claude-global', 'pb-evolve']
last_reviewed: "2026-02-18"
last_evolved: ""
version: "2.0.0"
version_notes: "Consolidated: merged automated conversation audit into single command with structural and behavioral modes"
breaking_changes: ["pb-review-context merged into this command; use `--violations` mode instead"]
---
# Context Layer Review & Hygiene

**Purpose:** Comprehensive audit of all context layers—both structural (sizes, duplication, archival) and behavioral (CLAUDE.md violations, staleness). Run quarterly before `/pb-evolve` to ensure context earns its space and actually works.

**Mindset:** Context is necessary but expensive. Every line loaded competes for attention. Every guideline either influences behavior or should be deleted. Apply `/pb-design-rules` thinking: Simplicity (remove what doesn't earn its place) and Clarity (what remains should be immediately useful). Apply `/pb-preamble` thinking: challenge whether each section is still relevant.

**Resource Hint:** sonnet — structured audit and maintenance workflow (sequential manual, parallel subagents for violations)

---

## When to Use

- **Quarterly, before /pb-evolve** — Data-driven evolution planning (Feb, May, Aug, Nov)
- **After a release** — Trim release-specific details, verify context still works
- **When sessions start slow** — Diagnose context bloat (structural or behavioral)
- **When Claude ignores a guideline** — Check if CLAUDE.md is stale or misguided

---

## Three Ways to Run

### Mode 1: Full Audit (Default)
```bash
/pb-context-review
```
Runs both structural and behavioral analysis in sequence. Manual inspection first provides context for automated violations analysis. Output: consolidated report with both findings.

### Mode 2: Structural Only
```bash
/pb-context-review --structure
```
Fast review of layer sizes, duplication, and archival opportunities. Use when you don't have conversation history or want quick baseline.

### Mode 3: Violations Only
```bash
/pb-context-review --violations
```
Analyze recent conversations for CLAUDE.md violations, missing patterns, and stale guidance. Requires 10+ accumulated sessions.

---

## Structural Audit Workflow (--structure or part of full)

### Context Architecture Reference

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

## Violations Audit Workflow (--violations or part of full)

Analyze recent conversations to find where CLAUDE.md instructions were violated, patterns that should be added, and guidance that's gone stale. Turns context maintenance from gut-feel into data.

### Step 1: Locate Conversation History

Claude Code stores conversation transcripts as `.jsonl` files under `~/.claude/projects/`. The folder name is the project path with slashes replaced by dashes.

```bash
# Find the project's conversation folder
PROJECT_PATH=$(pwd | sed 's|/|-|g' | sed 's|^-||')
CONVO_DIR=~/.claude/projects/-${PROJECT_PATH}

# List recent conversations
ls -lt "$CONVO_DIR"/*.jsonl 2>/dev/null | head -20
```

If no conversations found, there's nothing to audit. Run this after you've accumulated 10+ sessions.

### Step 2: Extract Recent Conversations

Pull the 15-20 most recent sessions (excluding the current one) into a temporary working directory. Extract only the human-readable parts — user messages and assistant text responses.

```bash
SCRATCH=/tmp/context-audit-$(date +%s)
mkdir -p "$SCRATCH"

for f in $(ls -t "$CONVO_DIR"/*.jsonl | tail -n +2 | head -20); do
  base=$(basename "$f" .jsonl)
  jq -r '
    if .type == "user" then
      "USER: " + (.message.content // "")
    elif .type == "assistant" then
      "ASSISTANT: " + ((.message.content // []) | map(select(.type == "text") | .text) | join("\n"))
    else
      empty
    end
  ' "$f" 2>/dev/null | grep -v "^ASSISTANT: $" > "$SCRATCH/${base}.txt"
done

# Show what we're working with
echo "Extracted $(ls "$SCRATCH"/*.txt | wc -l) conversations"
ls -lhS "$SCRATCH"/*.txt | head -10
```

### Step 3: Analyze with Parallel Subagents

Launch 3-5 sonnet subagents in parallel. Each gets:
- The global CLAUDE.md (`~/.claude/CLAUDE.md`)
- The project CLAUDE.md (`.claude/CLAUDE.md`)
- A batch of conversation files

Batch by size to keep each agent's context manageable:
- Large conversations (>100KB): 1-2 per agent
- Medium (10-100KB): 3-5 per agent
- Small (<10KB): 5-10 per agent

Each agent's prompt:

```
Read the CLAUDE.md files (global and project). Then read each conversation.

For each conversation, find:

1. VIOLATED — Instructions in CLAUDE.md that the assistant didn't follow.
   Include: which instruction, what happened instead, how often.

2. MISSING (LOCAL) — Patterns you see repeated across conversations that
   should be in the project CLAUDE.md but aren't. Project-specific only.

3. MISSING (GLOBAL) — Patterns that apply to any project, not just this one.

4. STALE — Anything in either CLAUDE.md that conversations suggest is
   outdated, irrelevant, or contradicted by actual practice.

Be specific. Quote the instruction and the violation. One bullet per finding.
```

### Step 4: Aggregate and Report

Combine findings from all agents. Deduplicate. Rank by frequency (violations seen across multiple conversations rank higher than one-offs).

**Report Format:**

```markdown
## Context Audit: YYYY-MM-DD
Analyzed: N conversations over M days

### Violated Instructions (need reinforcement)
| Instruction | Source | Violations | Example |
|-------------|--------|------------|---------|
| [rule text] | global/project | N times | [what happened] |

### Missing Patterns — Project
- [pattern]: seen in N conversations. Suggested wording: "..."

### Missing Patterns — Global
- [pattern]: seen in N conversations. Suggested wording: "..."

### Potentially Stale
- [instruction] in [file]: last relevant in conversations from [date].
  No violations because it's not being tested — likely outdated.
```

### After the Audit

Based on findings:

1. **Violated instructions** → Reword for clarity or move to a more prominent location. If a BEACON guideline is being violated, that's a signal it needs reinforcement in the BEACON summary, not just the full command.

2. **Missing patterns** → Add to the appropriate CLAUDE.md. Use `/pb-claude-global` or `/pb-claude-project` to regenerate, or edit directly.

3. **Stale content** → Remove or archive. Every stale line costs tokens and dilutes signal.

4. **Feed into /pb-evolve** → If findings suggest structural changes (new BEACONs, reclassified commands, workflow shifts), queue them for the next quarterly evolution.

```bash
# Cleanup temporary conversation extracts
rm -rf /tmp/context-audit-*
```

---

## Integration with /pb-pause and /pb-evolve

Daily context hygiene is embedded in `/pb-pause` (Step 6):
- Writes concise pause entry
- Archives old pause entries
- Reports context layer sizes

`/pb-context-review` is the **deeper quarterly audit** — run before `/pb-evolve` to ensure context is both structurally lean AND behaviorally sound. `/pb-pause` handles the daily maintenance.

**Evolution cycle flow:**
```
/pb-context-review --structure    → Identify bloat
/pb-context-review --violations   → Find stale/violated guidance
/pb-evolve                        → Make decisions based on both
/pb-claude-global                 → Regenerate if needed
/pb-claude-project                → Regenerate if needed
```

---

## Anti-Patterns

### Structural Audit
| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Never archiving pause notes | 650+ lines of historical entries | Archive after each resume |
| Copying info across layers | Same facts in 4 files | One canonical home, others cross-reference |
| Detailed task logs in working context | 243 lines when target is 50 | Keep snapshot, move details to done/ |
| Explaining the context system in context | Meta-context burns budget | System works without self-description |
| Hard line-count limits | Chasing numbers over signal | Soft targets, prioritize density |

### Violations Audit
| Don't | Do Instead |
|-------|------------|
| Run daily | Run quarterly or when something feels off |
| Add every finding to CLAUDE.md | Prioritize by frequency — one-offs are noise |
| Skip the stale check | Removing bad guidance is as valuable as adding good guidance |
| Audit without acting | The report is useless if nothing changes |

---

## Related Commands

- `/pb-pause` — Daily context hygiene (archive + report) embedded in session boundary
- `/pb-resume` — Context loading with health check at session start
- `/pb-context` — Regenerate working context on release/milestone
- `/pb-claude-global` — Regenerate global CLAUDE.md from playbooks
- `/pb-evolve` — Quarterly evolution cycle (consumes this audit's output)

---

**Last Updated:** 2026-02-18
**Version:** 2.0.0
**Note:** pb-review-context merged into this command. Use `--violations` mode for automated audit.
