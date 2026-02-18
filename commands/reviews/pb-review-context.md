---
name: "pb-review-context"
title: "Context Audit from Conversation History"
category: "reviews"
difficulty: "intermediate"
model_hint: "sonnet"
execution_pattern: "parallel"
related_commands: ['pb-context-review', 'pb-claude-global', 'pb-claude-project', 'pb-evolve']
last_reviewed: "2026-02-18"
last_evolved: ""
version: "1.0.0"
version_notes: "Initial release — conversation-driven CLAUDE.md audit"
breaking_changes: []
---
# Context Audit from Conversation History

Reads recent conversation transcripts and finds where your CLAUDE.md instructions were violated, patterns that should be added, and guidance that's gone stale. Turns context maintenance from gut-feel into data.

**Mindset:** Apply `/pb-preamble` thinking — challenge whether your CLAUDE.md actually influences behavior. Apply `/pb-design-rules` thinking — context that doesn't earn its place should be removed. Every line in CLAUDE.md costs tokens on every turn.

**Resource Hint:** sonnet — parallel subagent analysis of conversation batches

---

## When to Use

- Quarterly, alongside `/pb-evolve` — data-driven evolution input
- After noticing Claude repeatedly ignoring a guideline
- Before regenerating CLAUDE.md files (`/pb-claude-global`, `/pb-claude-project`)
- When context feels bloated but you're not sure what to cut

---

## How It Works

```
┌──────────────────────────────────────────────┐
│  1. LOCATE    Find project conversation logs │
│       ↓                                      │
│  2. EXTRACT   Parse 15-20 recent sessions    │
│       ↓                                      │
│  3. ANALYZE   Parallel subagents audit each  │
│               batch against CLAUDE.md files  │
│       ↓                                      │
│  4. REPORT    Aggregate into actionable list │
└──────────────────────────────────────────────┘
```

---

## Step 1: Locate Conversation History

Claude Code stores conversation transcripts as `.jsonl` files under `~/.claude/projects/`. The folder name is the project path with slashes replaced by dashes.

```bash
# Find the project's conversation folder
PROJECT_PATH=$(pwd | sed 's|/|-|g' | sed 's|^-||')
CONVO_DIR=~/.claude/projects/-${PROJECT_PATH}

# List recent conversations
ls -lt "$CONVO_DIR"/*.jsonl 2>/dev/null | head -20
```

If no conversations found, there's nothing to audit. Run this after you've accumulated 10+ sessions.

---

## Step 2: Extract Recent Conversations

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

---

## Step 3: Analyze with Parallel Subagents

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

---

## Step 4: Aggregate and Report

Combine findings from all agents. Deduplicate. Rank by frequency (violations seen across multiple conversations rank higher than one-offs).

### Report Format

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

---

## After the Audit

Based on findings:

1. **Violated instructions** → Reword for clarity or move to a more prominent location. If a BEACON guideline is being violated, that's a signal it needs reinforcement in the BEACON summary, not just the full command.

2. **Missing patterns** → Add to the appropriate CLAUDE.md. Use `/pb-claude-global` or `/pb-claude-project` to regenerate, or edit directly.

3. **Stale content** → Remove or archive. Every stale line costs tokens and dilutes signal.

4. **Feed into /pb-evolve** → If findings suggest structural changes (new BEACONs, reclassified commands, workflow shifts), queue them for the next quarterly evolution.

---

## Integration with Evolution Cycle

This command produces the raw data that `/pb-evolve` uses for evidence-based decisions:

```
/pb-review-context           → Data: what's working, what's not
/pb-git-signals              → Data: what's being used, what's dormant
/pb-evolve                   → Decision: what changes for next quarter
/pb-claude-global            → Output: regenerated global context
/pb-claude-project           → Output: regenerated project context
```

Run this before `/pb-evolve`, not after.

---

## Cleanup

```bash
# Remove temporary conversation extracts
rm -rf /tmp/context-audit-*
```

---

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Run daily | Run quarterly or when something feels off |
| Add every finding to CLAUDE.md | Prioritize by frequency — one-offs are noise |
| Skip the stale check | Removing bad guidance is as valuable as adding good guidance |
| Audit without acting | The report is useless if nothing changes |

---

## Related Commands

- `/pb-context-review` — Manual context layer audit (sizes, duplication, archival)
- `/pb-claude-global` — Regenerate global CLAUDE.md from playbooks
- `/pb-claude-project` — Regenerate project CLAUDE.md from codebase
- `/pb-evolve` — Quarterly evolution cycle (consumes this audit's output)

---

**Last Updated:** 2026-02-18
**Version:** 1.0.0
