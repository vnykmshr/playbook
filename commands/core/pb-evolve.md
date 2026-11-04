---
name: "pb-evolve"
title: "Evolve Playbooks to Match Claude Capabilities"
category: "core"
difficulty: "beginner"
model_hint: "opus"
execution_pattern: "sequential"
related_commands: ['pb-claude-global', 'pb-claude-project', 'pb-standards', 'pb-preamble', 'pb-design-rules']
last_reviewed: "2026-11-04"
version: "2.0.0"
version_notes: "v2.0.0: Team machinery cut: calendar, Evolution Manager, snapshot/log/diff steps, report and dashboard templates, mkdocs and pbai."
breaking_changes: []
---

# Evolve Playbooks to Match Claude Capabilities

**Purpose:** Quarterly (or on-demand) review of Claude capability updates and playbook regeneration to maintain alignment and maximize efficiency.

**Mindset:** Self-healing, self-improving system. Playbooks exist to serve users. As Claude improves, playbooks should improve automatically. Apply `/pb-preamble` thinking (challenge assumptions about what's still true) and `/pb-design-rules` thinking (does every playbook still embody Clarity, Simplicity, Resilience?).

**Resource Hint:** opus - Strategic evolution; capability assessment and design decisions.

---

## When to Use

- **Quarterly schedule** - Feb, May, Aug, Nov (fixed calendar)
- **Major Claude version release** - When Claude 4.6 → 4.7 drops
- **Context limit stress** - If hitting session limits regularly
- **Latency complaints** - If playbooks feel slow
- **User feedback** - When patterns don't work in practice

---

## Quick Start: Run Evolution Cycle

### Step 1: Prepare Environment

```bash
# Ensure clean state
git status                                    # Must be clean
git checkout main && git pull origin main     # On latest main
```
### Step 2: Run Analysis

```bash
# Analyze current state
python3 scripts/evolve.py --analyze

# View detailed report
cat todos/evolution-analysis.json | jq '.'

# Check validation
python3 scripts/evolve.py --validate
```

### Step 3: Review Capability Changes

Since last evolution, what has changed?

- **Speed improvements:** Sonnet faster? Opus cost-effective for more tasks?
- **Context windows:** Larger windows change what you can keep in main context
- **Latency profile:** Different models, different speeds
- **Reasoning depth:** Better reasoning changes what model to use for what task


### Step 3.5: Help or Constrain (Standing, Every Cycle)

**The question:** does each playbook surface still structure and check the model's work, or has it become a constraint that keeps a stronger model from its best work? It runs every cycle, including cycles with no model release: a harness change or a session's evidence moves the line as much as a new model does.

**Ground truth first.** Fetch the vendor's current prompting guidance and harness docs to disk and extract a ground-truth file. The model under review is not a reliable witness to its own capabilities: the 2026-06 Fable trial and a 2026-09 research subagent both asserted capability facts the docs contradicted. A capability claim that is not in the ground-truth file does not enter the review.

**The line.** A surface earns its place when it carries what the model cannot derive from the repo or would not do by default:

- Decisions and consent boundaries the owner made
- This project's conventions, couplings and gotchas
- Behaviours the vendor documents as needing instruction (response length and scope, as of 2026-09)
- Checks that execute: a test, a guard, a hook

It constrains when it:

- Re-teaches what the model does natively or what the harness already does
- Instructs re-verification of work the model already verifies
- Prescribes reasoning steps where stating the outcome would do
- States facts that rot (model versions, SHAs, counts) in a file loaded every session

**Where to look, by cost.** Auto-loaded surfaces first (generated global and project CLAUDE.md, the memory index): every line is paid every session and cannot be corrected mid-session. Then commands that chain or stack checks. On-demand reference commands last: they cost nothing until invoked, so review them only when a finding points there.

**Two-sided, by rule.** Before proposing any cut, name at least one place where the model needs *more* structure, with evidence, or state that you looked and found none. A review that only deletes is a prune machine run one line at a time. The 2026-09 panel of four argued deletion and nobody argued addition, while the one addition that cycle (a scope rule) answered a documented weakness.

**Deletion needs evidence, not self-report.** The model judging the rules is the model the rules govern, and "I would do that anyway" is the one claim it cannot make about itself. Cut a behavioural rule on vendor documentation or on observed sessions, never on the model's account of its own defaults. The 2026-09 session that argued verification is native also repeated the cheapest-surface mistake its own memory warned about.

**Scope:** this review changes what commands say. It does not retire commands; retirement stays a single human decision.

**Run it as a huddle** (`/pb-huddle`): same brief to every panelist, ground-truth file attached, this question alongside the cycle's own. Record a trend row in the cycle record so the next cycle compares rather than re-derives:

| Measure | Q3 2026 baseline |
|---------|------------------|
| Global CLAUDE.md, generated lines | 158 |
| Project CLAUDE.md (the playbook's own), lines | 86 |
| Verify-instructions in auto-loaded files | 0 (was 4) |
| Model-version strings in generator templates | 0 (`TestTemplateCurrency`) |
| Structure added / cut | 1 / ~12 |

### Step 9: Regenerate Auto-Generated Files

```bash
# Regenerate all auto-generated indices
python3 scripts/evolve.py --generate

# Regenerate project CLAUDE.md
/pb-claude-project

# Regenerate global CLAUDE.md
/pb-claude-global

```
---
### What Doesn't Change?

- **Preamble thinking** (challenge assumptions, peer collaboration) - timeless
- **Design rules** (clarity, simplicity, robustness) - timeless
- **Atomic commits, quality gates** - foundational, not outdated by capability
- **Test-first discipline** - still best practice

---
## Common Evolution Scenarios

### Scenario A: Speed Improvement (e.g., Sonnet 4.5 → 4.6)

**Signal:** "New Sonnet is 30% faster, same cost"

**Analysis:**
- What was Sonnet+Opus before might be Sonnet-only now
- Parallelization becomes more viable
- Session times drop

**Action:**
- Revisit model routing decisions
- Test parallelization patterns
- Update execution time estimates
- Document efficiency gains

### Scenario B: Context Window Expansion

**Signal:** "Opus 4.7 offers a 1M-context variant (`[1m]` tier) alongside the 200K default"

**Analysis:**
- Default window unchanged (200K); 1M is opt-in, not automatic
- Compression and subagent delegation still correct for the default
- Cost scales with context size: 1M is not free headroom

**Action:**
- Reframe context-budget guidance to acknowledge the tier without softening hygiene
- Document which workflows justify opting into `[1m]` (deep-repo audits, long-horizon synthesis)
- Status-line tooling must recognize the new model identifiers
- Leave compression patterns in place; treat 1M as reserved headroom

### Scenario C: User Feedback (Patterns Don't Work)

**Signal:** "This playbook guidance is confusing, I did it differently"

**Analysis:**
- Reality doesn't match documentation
- Users are finding better way
- Playbook is stale or unclear

**Action:**
- Interview users on what worked
- Update playbook with real pattern
- Validate on 3+ users
- Simplify if new pattern is simpler

### Scenario D: New Capability (e.g., Tool Use, Custom Models)

**Signal:** "Claude now supports X"

**Analysis:**
- This changes what's possible
- May enable new playbooks or patterns
- May make old patterns obsolete

**Action:**
- Research capability thoroughly
- Design playbooks for new capability
- Test extensively before releasing
- Document when this capability became available

---
## Checklist: Before Publishing Evolution

- [ ] Success criteria defined (see section above)
- [ ] Success criteria verified
- [ ] All playbooks validated (python3 scripts/evolve.py --validate)
- [ ] No circular cross-references
- [ ] Metadata coverage > 95%
- [ ] mkdocs build --strict passes
- [ ] markdownlint passes
- [ ] CHANGELOG updated
- [ ] MEMORY.md updated with lessons
- [ ] Evolution log entry written
- [ ] Help-or-constrain review run (Step 3.5): ground-truth-backed, two-sided, trend row recorded
- [ ] Tests pass
- [ ] Tested on 2-3 real tasks

---
---

## Related Commands

- `/pb-claude-global` - Regenerate global CLAUDE.md
- `/pb-claude-project` - Regenerate project CLAUDE.md
- `/pb-standards` - Quality standards (validated by evolution)
- `/pb-preamble` - Thinking philosophy (doesn't change)
- `/pb-design-rules` - Design principles (doesn't change)

---

*Self-improvement is how we stay relevant. When Claude evolves, we evolve. When users teach us better patterns, we implement them. This playbook is never "done"-it's always improving.*
