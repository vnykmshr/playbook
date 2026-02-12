---
name: "pb-review-playbook"
title: "Playbook Command Review"
category: "reviews"
difficulty: "advanced"
model_hint: "opus"
execution_pattern: "sequential"
related_commands: ['pb-new-playbook', 'pb-claude-orchestration', 'pb-review-docs', 'pb-standards', 'pb-design-rules']
last_reviewed: "2026-02-09"
last_evolved: ""
version: "1.0.0"
version_notes: "v2.10.0 baseline"
breaking_changes: []
---
# Playbook Command Review

**Purpose:** Comprehensive multi-perspective review of playbook commands to ensure correct intent, quality implementation, and ecosystem coherence.

**When to Use:** Periodically (monthly), after adding multiple commands, or before major releases.

**Mindset:** Apply `/pb-preamble` thinking (challenge assumptions, surface flaws) and `/pb-design-rules` principles to the playbook itself. The playbook should exemplify what it preaches.

**Resource Hint:** opus — meta-review of playbook commands requires nuanced evaluation of intent, design alignment, and ecosystem coherence

---

## When to Use

- After adding multiple new commands to the playbook
- Before major playbook releases
- Monthly playbook health check
- When commands feel overlapping or inconsistent

---

## Review Perspectives

Launch the following review perspectives. For large command sets, batch by category.

### 1. Intent Clarity
Does the command name match what it does?

- [ ] Name follows `pb-<action>` or `pb-<category>-<target>` pattern
- [ ] Purpose statement is clear in first 10 seconds of reading
- [ ] "What" and "Why" are immediately obvious
- [ ] No misleading names (e.g., "review" that doesn't review, "deploy" that only documents)
- [ ] Verb choice matches action (reference vs execute vs orchestrate)

**Red flags:** Vague names, purpose buried in content, name/content mismatch.

### 2. Actionability
Is this an executable prompt or just reference material?

- [ ] Can be invoked and produces useful output
- [ ] Has clear phases/steps that guide execution
- [ ] Includes concrete actions, not just principles
- [ ] Distinguishes between "do this" vs "read this for context"

**Classification:**
- **Executor** — Runs a workflow (pb-deployment, pb-commit)
- **Orchestrator** — Coordinates other commands (pb-release, pb-ship)
- **Guide** — Provides framework/philosophy (pb-guide, pb-preamble)
- **Reference** — Pattern library, checklists (pb-patterns-*, pb-templates)
- **Review** — Evaluates against criteria (pb-review-*, pb-security)

**Red flag:** Command claims to "do" something but only provides reading material.

### 3. Design Rules Alignment
Does the command honor what we preach?

| Rule | Check |
|------|-------|
| **Clarity** | Is the command obviously correct? No ambiguity? |
| **Simplicity** | Minimal complexity for the task? No bloat? |
| **Modularity** | Single responsibility? Clean boundaries? |
| **Robustness** | Handles edge cases? Fails gracefully? |
| **Separation** | Policy (what) separate from mechanism (how)? |

**Red flag:** 1000+ line reference doc masquerading as actionable command.

### 4. Preamble Alignment
Does the command enable the collaboration philosophy?

- [ ] Encourages challenge and dissent, not compliance
- [ ] Frames work as peer-to-peer, not hierarchical
- [ ] Surfaces trade-offs explicitly
- [ ] Invites critique of its own recommendations
- [ ] Treats failures as learning, not blame

**Red flag:** Command that prescribes "the one right way" without alternatives.

### 5. Overlap Analysis
Is there redundancy or blurred responsibilities?

- [ ] No significant content duplication with other commands
- [ ] Clear boundary with related commands
- [ ] Complementary, not competing, with similar commands
- [ ] If overlap exists, one should reference the other (not duplicate)

**Check matrix:** Compare against commands in same category and related categories.

**Red flag:** Two commands that could be merged, or one that should be split.

### 6. Cross-reference Accuracy
Do links work and make sense?

- [ ] All `/pb-*` references point to existing commands
- [ ] Related commands are linked (not orphaned)
- [ ] References are bidirectional where appropriate
- [ ] No circular dependencies that confuse users

**Validation:** `grep -r "/pb-" commands/ | extract unique refs | verify each exists`

### 7. Structure Consistency
Does it follow playbook patterns?

- [ ] Title is `# Command Name` (not description)
- [ ] Has Purpose/When to Use at top
- [ ] Uses `---` dividers between major sections
- [ ] Headings follow hierarchy (H2 for sections, H3 for subsections)
- [ ] Tone is professional, concise, no fluff
- [ ] No emojis (unless explicitly part of output format)
- [ ] Examples are practical and runnable
- [ ] Ends with Related Commands section

### 8. Completeness
Does it adequately cover the topic?

- [ ] Core use case fully addressed
- [ ] Common variations/options covered
- [ ] Edge cases acknowledged
- [ ] Examples for non-obvious scenarios
- [ ] No "TODO" or placeholder sections

**Red flag:** Command that stops halfway through a workflow.

### 9. User Journey Fit
Does it integrate into workflows naturally?

- [ ] Listed in `/docs/command-index.md`
- [ ] Appears in `/docs/decision-guide.md` where relevant
- [ ] Workflow placement is logical (when would user invoke this?)
- [ ] Entry points are clear (how do users discover this?)
- [ ] Exit points connect to next logical command

### 10. DRY Compliance
Is content duplicated unnecessarily?

- [ ] Checklists not copy-pasted across commands
- [ ] Shared concepts reference canonical source
- [ ] If same content in 2+ places, extract to one and reference
- [ ] Templates are in pb-templates, not scattered

---

## Quick Review Mode

For reviewing a small number of changed commands (after adding 1-3 commands or making targeted edits), use this abbreviated flow instead of the full review process.

### Scope

```bash
# Find commands changed since last tag
git diff $(git describe --tags --abbrev=0)..HEAD --name-only -- commands/
```

### Abbreviated Perspectives (4 of 10)

Apply these four perspectives to each changed command:

1. **Intent Clarity** — Name matches action? Purpose obvious in 10 seconds?
2. **Structure Consistency** — Follows heading/section patterns?
3. **Cross-reference Accuracy** — All `/pb-*` refs valid? Bidirectional links?
4. **Completeness** — Core use case covered? No TODOs?

### Escalation to Full Review

Escalate to the full review process if:

- More than 5 commands changed
- New category added or existing category restructured
- Cross-category dependencies modified
- Preparing for a major release

---

## Review Process

### Phase 1: Automated Checks

**Resource:** Delegate to haiku via Task tool — mechanical checks.

```bash
# Count commands
find commands -name "*.md" | wc -l

# Find all cross-references
grep -roh "/pb-[a-z-]*" commands/ | sort | uniq -c | sort -rn

# Find potential duplicates (similar content)
# Manual review required for semantic similarity

# Check for orphaned commands (not in index)
diff <(find commands -name "pb-*.md" -exec basename {} .md \; | sort) \
     <(grep -oh "pb-[a-z-]*" docs/command-index.md | sort | uniq)
```

### Phase 2: Category-by-Category Review

**Resource:** Use opus — nuanced evaluation of intent, quality, design alignment.

Review commands by category, applying all 10 perspectives:

```bash
# Get current counts per category
for dir in commands/*/; do
  category=$(basename "$dir")
  count=$(find "$dir" -name "*.md" | wc -l | tr -d ' ')
  echo "$count $category"
done
```

1. **Core** — Foundation, philosophy, meta-playbook commands
2. **Planning** — Architecture, patterns, decisions
3. **Development** — Daily workflow commands
4. **Deployment** — Release, operations, infrastructure
5. **Reviews** — Quality gates, audits
6. **Repo** — Repository management
7. **People** — Team operations
8. **Templates** — Context generators, Claude Code configuration
9. **Utilities** — System maintenance

### Phase 3: Cross-Category Analysis

**Resource:** Use opus in main context — cross-cutting pattern recognition.

After individual review:

- Identify commands that should be merged
- Identify commands that should be split
- Identify missing commands (gaps in workflows)
- Verify workflow continuity (can user flow through without dead ends?)

**Self-improvement trigger:** After review, record systemic patterns in auto-memory. If a gap appears in 3+ commands, propose a playbook update rather than noting the same issue repeatedly.

---

## Output Format

### Per-Command Assessment

```
## pb-command-name

**Category:** [category]
**Classification:** Executor | Orchestrator | Guide | Reference | Review

### Verdict: [PASS | NEEDS WORK | RESTRUCTURE | DEPRECATE]

### Scores (1-5)
| Perspective | Score | Notes |
|-------------|-------|-------|
| Intent Clarity | X | |
| Actionability | X | |
| Design Rules | X | |
| Preamble | X | |
| Overlap | X | |
| Cross-refs | X | |
| Structure | X | |
| Completeness | X | |
| Journey Fit | X | |
| DRY | X | |

### Issues Found
- [CRITICAL] ...
- [HIGH] ...
- [MEDIUM] ...
- [LOW] ...

### Recommendations
1. ...
2. ...
```

### Consolidated Report

```
# Playbook Review: [Date]

## Executive Summary
- Commands reviewed: X
- Pass: X | Needs Work: X | Restructure: X | Deprecate: X
- Overall health: [A-F]

## Critical Issues (address immediately)
| # | Command | Issue | Recommendation |
|---|---------|-------|----------------|

## Structural Changes Needed
| Action | Commands | Rationale |
|--------|----------|-----------|
| Merge | pb-a + pb-b | Overlapping responsibility |
| Split | pb-c | Two concerns in one |
| Rename | pb-d → pb-e | Name doesn't match intent |
| Create | pb-new | Gap in workflow |

## Quick Wins
- [ ] Fix in <15 min...

## Backlog Items
- [ ] Larger refactoring...

## Category Health
| Category | Commands | Avg Score | Top Issue |
|----------|----------|-----------|-----------|
```

---

## Review Tracking

Create review document at `todos/playbook-review-YYYY-MM-DD.md`:
- Session progress
- Commands reviewed
- Issues found
- Actions taken
- Remaining work

---

## Related Commands

- `/pb-new-playbook` — Create new playbooks (classification, scaffold, validation)
- `/pb-claude-orchestration` — Model delegation guidance for review phases
- `/pb-review-docs` — Documentation quality review
- `/pb-standards` — Quality standards the playbook should meet
- `/pb-design-rules` — Principles commands should embody
