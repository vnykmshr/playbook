---
name: "pb-claude-orchestration"
title: "Claude Code Orchestration"
category: "templates"
difficulty: "beginner"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-claude-global', 'pb-claude-project', 'pb-learn', 'pb-review-playbook', 'pb-new-playbook']
last_reviewed: "2026-09-24"
last_evolved: "2026-09-24"
version: "1.5.0"
version_notes: "v1.5.0: Q3 2026 -- Harness Reality is dated rather than named after a model, and states only what the docs support: the default a session runs depends on plan, not a flat Opus claim. Delegation gains a cap -- current Opus over-delegates, and a subagent that checks your own work is documented to add cost without quality -- so validation leaves the Scout tier and the delegate list. Project budget <200 to match the single CLAUDE.md figure. Task tool naming retired. v1.4.1: Sync the context budget table to the generating commands (global <200, project <180); it had drifted to <150 for both. v1.4.0: Size the Pass, Not the Agent — inline the evidence and narrow the question; the whole-repo-reading subagent is the one that dies late. v1.3.0: Q2 2026 capability refresh -- Harness Reality to Opus 4.8 GA; corrected /fast (keeps Opus with faster output, no Sonnet downgrade); [1m] 1M-context framing; brief Fable 5 note (Opus stays default). v1.2.0: add Output Discipline subsection to Task Delegation Patterns -- accept subagent summaries as context, do not pipe raw tool output back into main conversation."
breaking_changes: []
---
# Claude Code Orchestration

**Purpose:** Guide model selection, task delegation, context management, and continuous self-improvement for efficient Claude Code usage.

**Mindset:** Apply `/pb-design-rules` thinking (Simplicity - cheapest model that produces correct results; Clarity - make delegation explicit) and `/pb-preamble` thinking (challenge assumptions about model choice - is opus actually needed here, or is it habit?).

**Resource Hint:** sonnet - reference guide for model selection and delegation patterns.

---

## When to Use

- Starting a session with mixed-complexity tasks
- Planning workflows that involve subagent delegation
- Reviewing resource efficiency after a session
- Generating or updating CLAUDE.md templates
- After a session where model choice caused issues (wrong model, wasted tokens)

---

## Model Tiers

| Tier | Model | Role | Strengths | Trade-off |
|------|-------|------|-----------|-----------|
| Architect | opus | Planner, reviewer, decision-maker | Deep reasoning, nuance, trade-offs | Highest cost, slowest |
| Engineer | sonnet | Implementer, coder, analyst | Code generation, balanced judgment | Medium cost, medium speed |
| Scout | haiku | Runner, searcher, formatter | File search, formatting, mechanical | Lowest cost, fastest |

Opus reasons. Sonnet builds. Haiku runs.

### Harness Reality (as of 2026-09-24)

The table above is cost guidance, not a description of what the harness runs: which model a session starts on depends on plan and configuration, and `/model` shows it. Current at this date, from Anthropic's docs:

- **Opus 5.5** is the default Opus model and Anthropic's recommended starting point; **Fable 5.1** is the default Fable model, for demanding long-horizon work. Both, and Sonnet 5, carry a 1M context window.
- Fable 5.1 lists at 2.5x Opus 5.5 ($10/$50 vs $4/$20 per Mtok). The playbook's own June head-to-head found the union of two models caught the most real bugs and neither alone did, so Fable is a second lens in deliberate deep audits, not a default.
- `/fast` speeds output on models that support it; it does not switch to a smaller model.

When cost discipline matters (routine dev loop, CI, automation), switch to Sonnet explicitly rather than relying on the harness default. Haiku remains subagent-only.

---

## Model Selection Strategy

### By Task Type

| Task | Model | Why |
|------|-------|-----|
| Architecture decisions, complex planning | opus | Multi-step reasoning, trade-off analysis |
| Security deep-dives, threat modeling | opus | Correctness stakes are high |
| Code review (critical paths) | opus | Judgment about design, not just correctness |
| Code implementation, refactoring | sonnet | Well-defined task, good balance |
| Test writing, documentation | sonnet | Pattern application, not invention |
| Routine code review | sonnet | Standard checklist evaluation |
| File search, codebase exploration | haiku | Mechanical, no reasoning needed |
| Linting, formatting | haiku | Rule application, not judgment |
| Status checks, simple lookups | haiku | Information retrieval only |

### Decision Criteria

Ask these in order (first match wins):

1. Does this require architectural judgment or trade-off analysis? → opus
2. Does this require code generation or analytical reasoning? → sonnet
3. Is this mechanical (search, format, scaffold)? → haiku

When unsure, start with sonnet. Upgrade to opus if results lack depth. Downgrade to haiku if the task is mechanical.

---

## Task Delegation Patterns

### When to Delegate

Current Opus delegates more readily than earlier models, and delegation multiplies cost and time on small tasks. Delegate only large, genuinely independent tracks. **Never delegate checking your own work** -- the model already verifies its output, and a verifier subagent is documented to add cost without adding quality. The deterministic caps are `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` and `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`.

**Delegate to subagents:**

- Independent research or codebase exploration too wide to hold in main context
- File search across many files
- Parallel information gathering
- Work that would pollute main context with noise

**Keep in main context:**

- Decisions that affect subsequent steps
- Architecture and planning
- Work requiring conversational continuity with the user
- Anything where the user needs to see the reasoning

### Output Discipline

When a subagent returns a summary, **accept the summary as context**. Do not pipe raw tool output, diffs, or file dumps back into the main conversation unless verification explicitly requires it. Context is finite; delegation is the exchange -- pay for it once, not twice.

### Size the Pass, Not the Agent

The subagent that has to read a whole repo before it can answer is the one that dies mid-run on an API error -- and it is the expensive one to lose, because it dies late.

**Inline the evidence, narrow the question.** Paste the file excerpt, the failing output, the rule text you already have, and ask one specific thing. Several lean passes beat one heavy pass that reconstructs context from disk: they finish, they are cheap to retry, and a failure costs one narrow answer instead of the whole analysis.

Reserve broad exploratory delegation for when you genuinely do not know where to look. Once you know, stop delegating the search and delegate the judgment.

### Parallel vs Sequential

| Pattern | When | Example |
|---------|------|---------|
| Parallel subagents | Independent queries, no shared state | Search 3 directories simultaneously |
| Sequential subagents | Output of one feeds into next | Explore → then Plan based on findings |
| Main context only | User interaction needed, judgment calls | Architecture review with the user |

### Model Assignment for Subagents

```
model: "haiku"   → Explore agents, file search, grep
model: "sonnet"  → Code writing, analysis, standard reviews
(default/opus)   → Planning, architecture, complex analysis
```

---

## Context Budget Management

### Budget Awareness

| Context Load | Budget | Frequency |
|-------------|--------|-----------|
| Global CLAUDE.md | <200 lines | Every turn, every session |
| Project CLAUDE.md | <200 lines | Every turn, every session |
| Auto-memory MEMORY.md | <200 lines | Every turn, every session |
| Session context | Finite, compaction is lossy | Fills during session |

Every unnecessary line in CLAUDE.md or MEMORY.md costs tokens on every single turn. Be ruthlessly concise in persistent files.

A 1M window does not retire this hygiene. Compaction is still lossy, every turn still pays the tokens, and Anthropic's own guidance is that longer CLAUDE.md files reduce adherence, not only budget.

### Efficiency Principles

- Subagents for exploration (separate context window, doesn't pollute main)
- Surgical file reads (offset + limit, not full files when you know the area)
- Plans in files, not in chat (reference by path, not by pasting)
- Compact at natural breakpoints (after commit, after phase - not mid-task)
- Commit frequently (each commit is a context checkpoint)
- Reference by commit hash (not by re-reading entire files)

---

## Playbook-to-Model Mapping

| Classification | Example Commands | Default Model | Delegation |
|---------------|-----------------|---------------|------------|
| Executor | pb-commit, pb-start, pb-deploy | sonnet | Procedural steps, well-defined |
| Orchestrator | pb-release, pb-ship, pb-review | opus (main) | Delegates subtasks to sonnet/haiku |
| Guide | pb-preamble, pb-design-rules | opus | Deep reasoning about principles |
| Reference | `pb-patterns-*`, pb-templates | sonnet | Pattern application, lookup |
| Review | `pb-review-*`, pb-security | opus + haiku | Phase 1: haiku automated; Phase 2-3: opus |

---

## Self-Healing and Continuous Learning

The orchestrator is not static. It learns, adapts, and improves.

### Operational Self-Awareness

After each significant workflow, reflect:

| Question | Action if Yes |
|----------|---------------|
| Did a model choice produce poor results? | Record in auto-memory, adjust default for that task type |
| Did a subagent return insufficient results? | Note the prompt pattern that failed, try broader/narrower next time |
| Did context fill up mid-task? | Record breakpoint strategy, compact earlier next session |
| Was a playbook missing or insufficient? | Note the gap, suggest improvement to user |
| Did the workflow take more turns than expected? | Analyze why - wrong model? Missing information? Poor delegation? |

### Auto-Memory as Learning Journal

Use the auto-memory directory (`~/.claude/projects/<project>/memory/`) to persist operational learnings:

**MEMORY.md** (loaded every session, <200 lines):

- Model selection adjustments discovered through experience
- Playbook gaps encountered and workarounds used
- Project-specific orchestration preferences
- Context management lessons learned

**Topic files** (referenced from MEMORY.md, loaded on demand):

- `orchestration-lessons.md` - Model choice outcomes, delegation pattern results
- `playbook-gaps.md` - Missing guidance discovered during workflows
- `project-patterns.md` - Project-specific efficiency patterns

### Feedback Loop

```
Execute workflow
    |
    v
Observe outcome
    |
    v
Was it efficient? Correct? Right model?
    |           |
    YES         NO
    |           |
    v           v
Continue    Record learning in auto-memory
            Adjust approach for next time
            Surface playbook gap to user if systemic
```

### Self-Healing Behaviors

| Trigger | Self-Healing Response |
|---------|----------------------|
| Subagent returns empty/useless results | Retry with adjusted prompt or different model tier |
| Context approaching limit mid-task | Proactively compact, checkpoint state in files |
| Playbook command produces unexpected output | Note in memory, suggest playbook update |
| Model produces shallow reasoning | Escalate to higher tier, record the task type |
| Repeated pattern across sessions | Extract to auto-memory for persistent learning |
| Stale information in MEMORY.md | Prune during session start, keep only current learnings |

### Suggesting Playbook Improvements

When the orchestrator discovers gaps during operation:

1. **Note the gap** - What was missing, what workaround was used
2. **Assess frequency** - One-off vs recurring need
3. **Propose to user** - "Encountered [gap] during [workflow]. Suggest updating [playbook] with [specific addition]."
4. **Don't self-modify playbooks silently** - Propose, don't assume

This creates a virtuous cycle: use playbooks → discover gaps → propose improvements → playbooks get better → usage gets better.

---

## Anti-Patterns

| Anti-Pattern | Why It Hurts | Better Approach |
|-------------|--------------|-----------------|
| Opus for file search | Expensive, no reasoning advantage | haiku subagent |
| Haiku for architecture | Shallow reasoning, bad decisions | opus in main context |
| Serializing independent subagents | Wastes wall-clock time | Parallel Task calls |
| Loading full files for 10 lines | Context waste | Read with offset + limit |
| Pasting plans into chat | Consumes context every turn | Store in files, reference by path |
| Skipping compaction until forced | Lossy emergency compaction | Compact at natural breakpoints |
| Same model for everything | Wastes cost or quality | Match model to task |
| Never recording what worked | Same mistakes repeated | Use auto-memory feedback loop |
| Ignoring playbook friction | Workarounds accumulate silently | Surface gaps, propose fixes |

---

## Examples

### Example 1: Feature Implementation Workflow

1. `/pb-plan` - opus (main context): architecture decisions, trade-offs
2. Explore codebase - haiku (2-3 parallel subagents): find relevant files
3. Implementation - sonnet (main context): write code
4. Write tests - sonnet subagent: parallel test generation
5. Self-review - opus (main context): critical evaluation
6. `/pb-commit` - sonnet: procedural commit workflow

**Post-session reflection:**

- Did haiku find what was needed? (If not, adjust search prompts in memory)
- Did sonnet's code need significant opus review fixes? (If yes, consider opus for complex implementation next time)

### Example 2: Playbook Review with Model Delegation

- Phase 1 automated checks - haiku subagent: count commands, validate cross-refs
- Phase 2 category review - opus (main context): nuanced evaluation of intent, quality
- Phase 3 cross-category - opus (main context): holistic pattern recognition

---

## Related Commands

- `/pb-claude-global` - Generate global CLAUDE.md (concise orchestration rules)
- `/pb-claude-project` - Generate project CLAUDE.md
- `/pb-learn` - Pattern learning from debugging (complements operational learning here)
- `/pb-review-playbook` - Playbook review (model delegation by phase)
- `/pb-new-playbook` - Meta-playbook (resource hint in scaffold)
