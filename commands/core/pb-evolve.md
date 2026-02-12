---
name: "pb-evolve"
title: "Evolve Playbooks to Match Claude Capabilities"
category: "core"
difficulty: "beginner"
model_hint: "opus"
execution_pattern: "sequential"
related_commands: ['pb-claude-global', 'pb-claude-project', 'pb-standards', 'pb-preamble', 'pb-design-rules']
last_reviewed: "2026-02-09"
last_evolved: ""
version: "1.1.0"
version_notes: "Initial v2.11.0 (Phase 1-4 enhancements)"
breaking_changes: []
---

# Evolve Playbooks to Match Claude Capabilities

**Purpose:** Quarterly (or on-demand) review of Claude capability updates and playbook regeneration to maintain alignment and maximize efficiency.

**Mindset:** Self-healing, self-improving system. Playbooks exist to serve users. As Claude improves, playbooks should improve automatically. Apply `/pb-preamble` thinking (challenge assumptions about what's still true) and `/pb-design-rules` thinking (does every playbook still embody Clarity, Simplicity, Resilience?).

**Core Principle:** We don't freeze playbooks at a point-in-time. We evolve them continuously as Claude capabilities improve. This is how we stay efficient.

**Resource Hint:** opus — Strategic evolution; capability assessment and design decisions.

---

## When to Use

- **Quarterly schedule** — Feb, May, Aug, Nov (fixed calendar)
- **Major Claude version release** — When Claude 4.6 → 4.7 drops
- **Context limit stress** — If hitting session limits regularly
- **Latency complaints** — If playbooks feel slow
- **User feedback** — When patterns don't work in practice

---

## Quick Start: Run Evolution Cycle

### Step 1: Prepare Environment

```bash
# Ensure clean state
git status                                    # Must be clean
git checkout main && git pull origin main     # On latest main

# Create evolution branch
git checkout -b evolve/$(date +%Y-%m-%d) main

# Load metadata schema and examples
cat .playbook-metadata-schema.yaml            # Review schema
ls docs/metadata-example-*.md                 # Review examples
```

### Step 1.5: Snapshot Before Evolution

**Critical:** Create a snapshot before making changes. This enables safe rollback if anything breaks.

```bash
# Create snapshot of current state
python3 scripts/evolution-snapshot.py \
  --create "Before Q1 2026 evolution"

# Record the evolution cycle in structured log
python3 scripts/evolution-log.py \
  --record-cycle "2026-Q1" \
  --trigger quarterly \
  --capability-changes "Sonnet 4.6: 30% faster, no cost change"
```

This creates:
- **Git tag** as backup (can revert to this if needed)
- **Snapshot metadata** for audit trail
- **Evolution log entry** to track this cycle

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

- **Claude model versions:** Run `pbai --version` or check recent announcements
- **Speed improvements:** Sonnet faster? Opus cost-effective for more tasks?
- **Context windows:** Larger windows change what you can keep in main context
- **Latency profile:** Different models, different speeds
- **Reasoning depth:** Better reasoning changes what model to use for what task

Document findings in `todos/evolution-log.md`:

```markdown
## Evolution Cycle: 2026-Q2

### Capability Changes Since Last Cycle
- Claude Sonnet 4.5 → 4.6: 30% faster, same cost
- Context window: 200K → 200K (no change)
- Reasoning: Better at multi-step planning

### Implications
- Parallelization now viable (Sonnet fast enough)
- Model routing: Haiku can take more routine tasks
- Context efficiency: Still critical (not changed)
```

### Step 4: Audit Playbooks Against New Capabilities

For each major playbook category, ask:

**Development playbooks** (pb-start, pb-cycle, pb-commit, pb-pr)
- Can Sonnet 4.6 now handle complex design reviews that needed Opus before?
- Are our model hints still accurate?
- Should parallelization be standard pattern?

**Review playbooks** (pb-review-code, pb-security, pb-voice)
- Should code review default to Sonnet (vs Opus)?
- Is parallel review (multiple agents) now viable?
- Are detection patterns still current?

**Planning playbooks** (pb-plan, pb-adr, pb-think)
- Does Sonnet 4.6 handle ideation/synthesis better?
- Should we escalate fewer things to Opus?
- Can we simplify playbooks for routine decisions?

**Utilities** (pb-patterns, pb-guidance, pb-learn)
- Are best practices still current?
- Do patterns still make sense?
- Are examples still best-practice?

### Step 5: Propose Changes

Document each opportunity:

```markdown
### Opportunity 1: Model Routing Update

**Current:** pb-start says "use Sonnet"
**Capability change:** Sonnet 4.6 is 30% faster
**Proposal:** Update model routing to:
  - Haiku for file search, status checks (unchanged)
  - Sonnet for development (unchanged)
  - Opus for security/architecture (unchanged)

**Rationale:** No change needed; Sonnet still correct model

---

### Opportunity 2: Parallel Research Pattern

**Current:** Sequential agent execution in /pb-claude-orchestration
**Capability change:** Sonnet 4.6 fast enough for parallel fan-out
**Proposal:** Add "Parallel Research Pattern" section:
  1. Main launches 3 agents simultaneously
  2. Each agent explores independently
  3. Results merged in synthesis stage

**Impact:** Session runtime -30% for exploration tasks
**Confidence:** High (pattern validated in playbook development)
```

### Step 6: Test Proposed Changes

For each significant change, validate on 2-3 real tasks:

```bash
# Example: Test parallel research pattern
# 1. Identify a task that would benefit
# 2. Run with old (sequential) approach
# 3. Time: 15 minutes
# 4. Run with new (parallel) approach
# 5. Time: 10 minutes
# 6. Document: "Parallel X saved Y minutes"
```

Record results:

```markdown
### Validation: Parallel Research Pattern

**Task:** Investigate codebase for X feature
**Old pattern (sequential):** 20 min (Agent A) + 15 min (Agent B) = 35 min total
**New pattern (parallel):** max(20 min, 15 min) = 20 min total

**Result:** 43% faster. Impact = HIGH. Implement.
```

### Step 7: Generate Diff and Request Approval

**Before applying changes**, generate a diff to see exactly what will change:

```bash
# Generate detailed diff comparing current to proposed
python3 scripts/evolution-diff.py \
  --detailed main HEAD

# Generate markdown report for PR
python3 scripts/evolution-diff.py \
  --report main HEAD
```

This creates `todos/evolution-diff-report.md` showing:
- Which playbooks are affected
- What fields change (old → new values)
- Why changes are being proposed

**GOVERNANCE GATE:** Create a PR and request peer review BEFORE applying changes.

```bash
# Create feature branch for changes
git checkout -b evolution/$(date +%Y-Q$((($(date +%m)-1)/3+1)))

# Commit proposed changes
git add commands/
git commit -m "evolution: proposed changes for review"

# Push and create PR
git push origin evolution/...
gh pr create --title "evolution(quarterly): Q1 2026" \
  --body "See todos/evolution-diff-report.md for details"
```

**Peer review checklist:**
- ✅ Capability changes documented accurately
- ✅ Proposed changes make sense given new capabilities
- ✅ No unintended side effects
- ✅ Metadata is consistent (run test suite)
- ✅ Related commands still exist and are reachable

**Only proceed after peer approval and merge to main.**

### Step 7.5: Apply Approved Changes

Once PR is approved and merged to main, apply the changes:

```bash
# Example: Update pb-claude-orchestration
# 1. Add "Parallel Research Pattern" section
# 2. Update examples to use parallel where applicable
# 3. Regenerate CLAUDE.md
# 4. Update MEMORY.md with new strategy

# Regenerate metadata-driven files
python3 scripts/evolve.py --generate

# Validate all metadata
python3 scripts/evolve.py --validate
```

### Step 8: Update Metadata

For each playbook that changed:

```bash
# Example: Update pb-start metadata
# - Update last_reviewed date
# - Update execution_time_estimate if timing changed
# - Add last_evolved date
# - Update summary if scope changed
# - Update related_commands if topology changed
```

Run validation:

```bash
python3 scripts/evolve.py --validate
```

### Step 9: Regenerate Auto-Generated Files

```bash
# Regenerate all auto-generated indices
python3 scripts/evolve.py --generate

# Regenerate project CLAUDE.md
/pb-claude-project

# Regenerate global CLAUDE.md
/pb-claude-global

# Run docs build
mkdocs build --strict
```

### Step 10: Complete Evolution Cycle

```bash
# Stage changes
git add commands/ docs/ scripts/ .claude/ CHANGELOG.md

# Commit with evolution note
git commit -m "evolve(quarterly): $(date +%Y-Q$((($(date +%m)-1)/3+1)))"

# Tag release (if this is a versioned release)
git tag -a v2.X.0 -m "v2.X.0: Q1 2026 evolution"

# Record cycle completion
python3 scripts/evolution-log.py \
  --complete "2026-Q1" \
  --pr <pr-number>

# Push
git push origin main --tags
```

### Step 11: If Evolution Breaks Something (Rollback)

If you discover issues after applying evolution changes:

```bash
# List available snapshots
python3 scripts/evolution-snapshot.py --list

# Show details of specific snapshot
python3 scripts/evolution-snapshot.py --show evolution-20260209-HHMMSS

# Rollback to snapshot (interactive confirmation)
python3 scripts/evolution-snapshot.py --rollback evolution-20260209-HHMMSS

# Or force rollback without confirmation
python3 scripts/evolution-snapshot.py --rollback evolution-20260209-HHMMSS --force

# Record the revert in evolution log
python3 scripts/evolution-log.py \
  --revert "2026-Q1" \
  --reason "Parallel patterns caused context bloat; needs refinement"

# Push rollback commit
git push origin main
```

---

## Anatomy of a Good Evolution

### What Changed?

- New Claude capabilities (model speed, reasoning, capabilities)
- User feedback (patterns that don't work, confusing guidance)
- Tech debt (playbooks that have become stale)
- New patterns discovered in practice

### How to Spot Evolution Opportunities?

**Pattern 1: Capability-Execution Mismatch**
- You say "use Sonnet for X" but Sonnet 4.6 can now do Y (more complex) just as well
- **Fix:** Update model hint, regenerate CLAUDE.md

**Pattern 2: Manual Work That Could Automate**
- You're manually updating 5 playbooks when you could update metadata + regenerate
- **Fix:** Metadata-driven auto-generation, one source of truth

**Pattern 3: Complexity That Could Simplify**
- Playbook has 10 decision trees but Sonnet 4.6 can handle the full decision at once
- **Fix:** Consolidate into single decision, simpler playbook

**Pattern 4: Serialization That Could Parallelize**
- You launch Agent A, wait for result, then launch Agent B
- But now both could launch simultaneously, merge results
- **Fix:** Document parallel pattern, add to orchestration guide

**Pattern 5: Context That Could Compress**
- Main context has 50K tokens of file content
- Could move to subagent (returns compression summary)
- **Fix:** Update context strategy in pb-claude-orchestration

### What Doesn't Change?

- **Preamble thinking** (challenge assumptions, peer collaboration) — timeless
- **Design rules** (clarity, simplicity, robustness) — timeless
- **Atomic commits, quality gates** — foundational, not outdated by capability
- **Test-first discipline** — still best practice

---

## Evolution Log Structure

The evolution system maintains **two logs**:

### 1. Structured Audit Log (todos/evolution-audit.json)

Machine-readable JSON format for pattern analysis and automation:

```json
{
  "cycles": [
    {
      "cycle": "2026-Q1",
      "started_at": "2026-02-09T12:00:00",
      "trigger": "quarterly",
      "capability_changes": "Sonnet 4.6: 30% faster, same cost",
      "changes": [
        {
          "command": "pb-claude-orchestration",
          "field": "execution_pattern",
          "before": "sequential",
          "after": "parallel",
          "rationale": "Sonnet 4.6 fast enough for concurrent agents"
        }
      ],
      "status": "completed",
      "snapshot_id": "evolution-20260209-143022",
      "pr_number": 42
    }
  ]
}
```

**Use this log to:**
- Detect patterns (what fields change most often?)
- Measure impact (did evolution help or hurt?)
- Enable automation (future cycles can suggest changes)
- Audit decisions (why did we make this change?)

```bash
# View evolution history
python3 scripts/evolution-log.py --show

# Analyze patterns
python3 scripts/evolution-log.py --analyze

# Export timeline
python3 scripts/evolution-log.py --export
```

### 2. Narrative Release Notes (CHANGELOG.md)

Human-readable summary for each release:

```markdown
## v2.11.0 (2026-05-15) — Q2 Evolution

### Capability Changes
- Sonnet 4.6 → 4.7: +15% reasoning depth
- No speed or cost changes
- New tool: structured output

### Improvements
- Parallel research patterns now standard in exploration tasks
- Model routing optimized (Haiku handles 10 more utility cases)
- Context efficiency improved 12% via better compression

### Metrics
- Average session time: -8% (from 32 min to 29 min)
- Cost per session: -3% (minor optimization)
- User satisfaction: +5% (feedback survey)
```

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

**Signal:** "Claude context now 400K tokens (was 200K)"

**Analysis:**
- Can now keep more files in main context
- Compression strategy becomes optional
- But context efficiency still matters (cost)

**Action:**
- Update context loading strategy
- Test keeping full codebase in context
- Measure tokens used; may stay selective
- Update MEMORY.md with new patterns

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

## Evolution Release Strategy

### Regular Releases (Every Quarter)

- Run pb-evolve on fixed schedule
- Document capability changes
- Implement small improvements
- Release as minor version bump (v2.X.0)

### Emergency Evolution (New Capability)

- Outside normal schedule
- When major capability lands
- Run full pb-evolve cycle
- Release as patch or minor (v2.X.Y)

### Versioning

- v2.X.0: Quarterly evolution
- v2.X.Y: Emergency evolution or small fix
- v1.X.0: Major architectural change

---

## Success Criteria for Evolution

Before publishing an evolution cycle, define and verify success metrics:

### For Capability-Driven Evolution (e.g., Claude 4.6 release)

**Define:**
- "What efficiency improvements do we expect?" (e.g., 15% faster sessions)
- "Which playbooks can be simplified?" (list specific commands)
- "Will model routing change?" (document before/after)

**Verify:**
- [ ] Session timing improved by X% (measured on real tasks)
- [ ] User satisfaction feedback positive
- [ ] Cost per session unchanged or lower
- [ ] No regressions in code quality

### For User Feedback Evolution (e.g., Patterns don't work)

**Define:**
- "What feedback were we acting on?" (reference issue/comment)
- "What's the new pattern?" (specific changes to command)
- "Who validates the fix?" (team member, user, or self-test)

**Verify:**
- [ ] User can achieve the goal using updated docs/command
- [ ] New pattern validated with 2+ real use cases
- [ ] Existing related commands still work with new approach

### For Technical Debt Evolution (e.g., Stale patterns)

**Define:**
- "What pattern is now outdated?" (specific reason)
- "What replaces it?" (new approach, with rationale)
- "Is this a breaking change?" (affects users? need migration guide?)

**Verify:**
- [ ] Migration guide written (if breaking)
- [ ] Existing projects tested with new approach
- [ ] Related commands still integrate properly

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
- [ ] Tests pass
- [ ] Tested on 2-3 real tasks

---

## Related Commands

- `/pb-claude-global` — Regenerate global CLAUDE.md
- `/pb-claude-project` — Regenerate project CLAUDE.md
- `/pb-standards` — Quality standards (validated by evolution)
- `/pb-preamble` — Thinking philosophy (doesn't change)
- `/pb-design-rules` — Design principles (doesn't change)

---

## Tips for Sustainable Evolution

1. **Make metadata source of truth** — Everything derives from metadata
2. **Automate what's repetitive** — scripts/evolve.py handles index generation
3. **Document rationale** — Every change explains why (for future evolution)
4. **Test before releasing** — Validate on real tasks
5. **Measure impact** — Track efficiency gains
6. **Collect feedback** — Users will find patterns that don't work
7. **Iterate publicly** — Share evolution log so users understand changes

---

## How This Works in Practice

Imagine Sonnet 4.6 is released and it's 30% faster.

1. **pb-evolve runs** → analyzes capability changes
2. **Opportunity identified** → "Can now parallelize more tasks"
3. **Pattern validated** → tests on real task, confirms 30% speedup
4. **Playbook updated** → adds parallel pattern to pb-claude-orchestration
5. **Metadata updated** → updates execution_time_estimate, last_evolved
6. **Files regenerated** → mkdocs build, scripts/evolve.py --generate
7. **Committed** → git commit, tagged v2.10.0
8. **Users benefit** → faster sessions, happier users, sustainable excellence

This is self-healing DNA in action.

---

## What Gets Evolved?

- Command metadata (last_reviewed, execution_time_estimate, difficulty)
- Model routing decisions (when to use Haiku vs Sonnet vs Opus)
- Execution patterns (when to parallelize, when to serialize)
- Context loading strategy (what to load in main, what to defer)
- Best practices (patterns that work in practice)
- Examples (keep them current)

## What Doesn't Get Evolved?

- Preamble thinking (timeless)
- Design rules (timeless)
- Command structure (breaking change, very rare)
- Commit discipline (timeless)
- Testing standards (timeless)

---

**Last Updated:** 2026-02-09
**Version:** 1.0 (Foundation Release)

*Self-improvement is how we stay relevant. When Claude evolves, we evolve. When users teach us better patterns, we implement them. This playbook is never "done"—it's always improving.*
