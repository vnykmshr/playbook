---
name: "pb-git-signals"
title: "Extract Git History Signals"
category: "core"
difficulty: "beginner"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-evolve', 'pb-context', 'pb-learn', 'pb-cycle']
last_reviewed: "2026-02-14"
last_evolved: "2026-02-14"
version: "1.0.0"
version_notes: "v2.12.0 Phase 3: Complete workflow integration with quarterly evolution planning, pain score response framework, and real-world examples"
breaking_changes: []
---

# Extract Git History Signals

**Purpose:** Analyze git history to extract adoption, churn, and pain point signals for data-driven decision making.

**Mindset:** Use git history as a source of truth for understanding what's actually used, what changes frequently, and where pain points exist. These signals inform quarterly evolution planning and ad-hoc investigations.

Apply `/pb-preamble` thinking: challenge what the signals reveal about project health. Apply `/pb-design-rules` thinking: are we building the right things? Are we fixing the same areas repeatedly?

**Resource Hint:** sonnet - Git history analysis; pattern recognition from commit signals.

---

## When to Use

- **Weekly check** - "What's been hot this week?"
- **Before quarterly planning** - Input for `/pb-evolve` decision making
- **After incidents** - Investigate pain patterns
- **Before refactoring** - Identify high-churn areas
- **Onboarding** - Show new team members what's active
- **Ad-hoc investigation** - "Why is this area changing so much?"

---

## Quick Start

### One-Time Run (Latest Analysis)

```bash
python scripts/git-signals.py
```

Outputs to `todos/git-signals/latest/`:
- `adoption-metrics.json` - Which commands/files are most touched
- `churn-analysis.json` - Which areas change frequently
- `pain-points-report.json` - Reverts, bug fixes, hotfixes
- `signals-summary.md` - Human-readable overview

### With Custom Time Range

```bash
python scripts/git-signals.py --since "3 months ago"
python scripts/git-signals.py --since "2025-01-01"
```

### Create Snapshot (Preserve Results)

```bash
python scripts/git-signals.py --snapshot 2026-02-12
```

Creates copy in `todos/git-signals/2026-02-12/` for historical comparison.

### Full CLI Help

```bash
python scripts/git-signals.py --help
```

---

## Understanding the Output

### Adoption Metrics (`adoption-metrics.json`)

**What it shows:** Which commands and files get the most attention

**Key fields:**
- `commands_by_touch_frequency` - Top 20 commands by git touches (all commits mentioning that file)
- `files_by_change_frequency` - Top 20 files by modification count
- `authors_per_command` - How many unique authors touched each command
- `least_active_commands` - Bottom 10 (candidates for review or removal)

**How to interpret:**
- High touch frequency = well-maintained or frequently used
- Low frequency = stale, abandoned, or stable
- Single author = potential knowledge bottleneck

**Example** (from playbook repository, 2026-02-12):
```
Most active: pb-guide (47 touches, 8 authors)
  → Core content, actively maintained, distributed ownership
Least active: pb-legacy-tool (2 touches, 1 author)
  → Likely deprecated or superseded
```

**Note:** Examples show data from a specific point in time. Your repository will show different values. Run `python scripts/git-signals.py` on your own project to see current signals.

### Churn Analysis (`churn-analysis.json`)

**What it shows:** Which areas change frequently (high volatility)

**Key fields:**
- `files_by_commit_frequency` - How many commits touch each file
- `files_by_line_changes` - Total lines added/deleted per file
- `high_churn_areas` - Files with most activity (lines + commit frequency combined)

**How to interpret:**
- High churn = active development, frequent refactoring, or instability
- High commit frequency + low line changes = many small tweaks
- High line changes + low commit frequency = rare but large changes

**Example:**
```
High churn: commands/core/pb-guide.md (150 commits, 5000 line changes)
  → Frequently updated, heavily maintained
Stable: commands/templates/pb-old.md (2 commits, 10 line changes)
  → Set and forget, unlikely to need updates
```

### Pain Point Signals (`pain-points-report.json`)

**What it shows:** Problem areas - where bugs and reversions happen

**Key fields:**
- `reverted_commits` - Commits that were later reverted (explicit undo)
- `bug_fix_patterns` - Commits with 'fix:', 'bug:', or 'bugfix' in subject
- `hotfix_patterns` - Urgent fixes ('hotfix', 'critical', 'p0:', 'p1:')
- `pain_score_by_file` - Composite score based on fixes+reverts
- `summary` - Counts of each pattern type

**How to interpret:**
- Reverts = clear mistakes that needed undoing
- Bug fixes = problems in the commit messages, doesn't mean problems with code
- Hotfixes = urgent issues requiring immediate attention
- Pain score = combines all three (higher = more problematic area)

**Example:**
```
Top pain areas:
  pb-guide.md: pain score 8 (3 fixes, 1 revert, 2 hotfixes)
    → Consider refactoring or splitting
  pb-standards.md: pain score 5 (4 fixes, 1 hotfix)
    → Frequently patched, maybe needs clarity
```

---

## Interpretation Guide

### Adoption Signals

**High adoption + High churn** = Active, evolving area
- Likely: Heavily maintained, responding to user feedback
- Action: Invest in stability, clear documentation
- Risk: Frequent changes might confuse users

**High adoption + Low churn** = Stable, well-designed area
- Likely: Solved problem, trusted by users
- Action: Minimal changes, preserve carefully
- Risk: May be overlooked in planning

**Low adoption + High churn** = Experimental or problematic
- Likely: New feature being refined, OR area with pain points
- Action: Investigate - is this active work or a problem?
- Risk: May indicate design issues

**Low adoption + Low churn** = Stale or deprecated
- Likely: Completed work, superseded feature, or unused pattern
- Action: Consider deprecation, removal, or revival
- Risk: Knowledge loss if removed

### Churn Signals

**High line changes + High commit frequency** = Volatile area
- Consider: Is this expected? Refactoring? Or instability?
- Action: Review recent commits for quality/coherence
- Risk: May accumulate technical debt

**High line changes + Low commit frequency** = Large-scale changes
- Consider: Was this planned? Major refactor?
- Action: Ensure tests cover the changes
- Risk: May introduce regressions

**Low line changes + High commit frequency** = Many small tweaks
- Consider: Polishing phase? Lots of small fixes?
- Action: Consider consolidating into fewer commits
- Risk: Fine details changing frequently

### Pain Point Signals

**Multiple reverts** = Systemic issues
- Indicator: Fix often doesn't work first time
- Action: Root cause analysis - process, design, or testing issue?
- Risk: Loss of trust in that area

**Clustered bug fixes** = Known problematic area
- Indicator: Same area repeatedly needs fixes
- Action: Consider redesign, not more patches
- Risk: Pattern of problems recurring

**Frequent hotfixes** = Lack of QA or design
- Indicator: Issues reach production, requiring urgent fixes
- Action: Improve testing, design review
- Risk: Quality and stability concerns

---

## Operational Workflow: How to Adopt Git-Signals

### Weekly Adoption Routine

Run signals every week to stay aware of what's actually happening:

```bash
# Every Monday or Friday (pick a consistent day)
python scripts/git-signals.py

# Review the summary
cat todos/git-signals/latest/signals-summary.md

# Check top pain areas this week
python3 -c "import json; \
  data = json.load(open('todos/git-signals/latest/pain-points-report.json')); \
  [print(f\"{x['file']}: pain={x['pain_score']}\") for x in data['pain_score_by_file'][:5]]"

# Reflect: What surprised you? What's worth investigating?
```

**Weekly Check Questions:**
- What files changed the most? Is that expected?
- Any new high-pain areas? Should we investigate?
- Adoption shifting? Are we working in the right areas?

### Quarterly Planning Workflow (Integration with `/pb-evolve`)

Before running `/pb-evolve` quarterly evolution, get fresh signals:

```bash
# Step 1: Run signals with 3-month time range
python scripts/git-signals.py --since "3 months ago"

# Step 2: Save as snapshot for this quarter
python scripts/git-signals.py --snapshot $(date +%Y-Q$((($(($(date +%m)-1)/3))+1)))

# Step 3: Extract key inputs for evolution planning
python3 << 'SIGNALS_EXTRACT'
import json
signals = json.load(open('todos/git-signals/latest/pain-points-report.json'))
print("\n=== PAIN SCORE PRIORITIES FOR EVOLUTION ===")
for item in signals['pain_score_by_file'][:10]:
    print(f"{item['file']}: {item['pain_score']}")
SIGNALS_EXTRACT

# Step 4: Use pain scores to guide /pb-evolve priorities
# Run /pb-evolve and reference pain_score_by_file in decisions
```

**Quarterly Planning Questions:**
- Which high-pain areas should be our evolution focus this quarter?
- Are there stale areas that should be deprecated?
- Which adoption patterns surprise us?

### Ad-Hoc Investigation Workflow

When you notice a specific problem or want to investigate an area:

```bash
# 1. Analyze the specific area's history
python scripts/git-signals.py --since "6 months ago"

# 2. Extract metrics for that file
git log --oneline commands/area/specific-file.md | wc -l  # Total commits
git log --follow -p commands/area/specific-file.md | grep -c "^+" # Lines added
git log --oneline commands/area/specific-file.md | grep -i "fix\|bug" | wc -l  # Fixes

# 3. Review the commits
git log --oneline commands/area/specific-file.md | head -20

# 4. Examine specific fixes
git log --oneline -p commands/area/specific-file.md | grep -B5 -A5 "fix\|bug" | head -50

# 5. Determine action
# Based on patterns, decide: refactor, deprecate, monitor, or accept
```

---

## Pain Score Response Framework

### Understanding Pain Scores

Pain scores combine three signals: **reverts** + **bug fixes** + **hotfixes**

A file with pain_score 6 might have:
- 2 commits that were reverted (explicitly undone)
- 3 commits tagged "fix:" (identified problems)
- 1 commit tagged "hotfix:" (urgent fixes)

**Total pain = 2 + 3 + 1 = 6**

### Response Matrix by Score Range

| Pain Score | Status | What It Means | Recommended Action | Priority |
|-----------|--------|---------------|-------------------|----------|
| **0-2** | Healthy | Stable, working well, minimal fixes | Monitor only. Make changes carefully | Low |
| **3-5** | Moderate | Some issues but manageable | Review recent changes. Monitor for patterns | Medium |
| **6-8** | High | Area has real problems | Investigate root cause. Plan refactoring | High |
| **9-10** | Critical | Systemic issues, repeatedly broken | Urgent: redesign or rewrite required | Critical |

### Response Actions by Score

**Score 0-2 (Healthy):**
- ✓ Stable foundation, trusted implementation
- ✓ Preserve carefully, minimal changes
- → Action: Review before changes, light touch

**Score 3-5 (Moderate):**
- ⚠ Occasional issues, worth monitoring
- ⚠ May need attention in next quarter
- → Action: Track trends, review commits, prioritize in next cycle

**Score 6-8 (High):**
- ⚠️ Real problems, needs investigation
- ⚠️ Candidate for refactoring or redesign
- → Action: Deep investigation → refactoring plan → prioritize in quarterly evolution

**Score 9-10 (Critical):**
- 🚨 Systemic failure, cannot continue as-is
- 🚨 Urgent: affecting reliability or productivity
- → Action: Root cause analysis → redesign/rewrite → make it priority this quarter

---

## Signal Response Decision Trees

### Decision Tree 1: High Adoption + Any Pain Score

```
High Adoption area with pain score?

├─ Pain 0-2?
│  └─ "Solved problem" - Keep working carefully
│     • Light changes only
│     • Extensive testing for any modifications
│
├─ Pain 3-5?
│  └─ "Active area with some issues"
│     • Monitor trends closely
│     • Plan improvements for next quarter
│     • Document workarounds
│
├─ Pain 6-8?
│  └─ "High-value target for improvement"
│     • This is where evolution effort pays off
│     • High adoption = impact is significant
│     • Prioritize in quarterly planning
│
└─ Pain 9+?
   └─ "URGENT: Used heavily but broken"
      • Reliability risk
      • Prioritize immediately
      • Consider temporary workarounds while fixing
```

### Decision Tree 2: Responding to Churn

```
Found an area with high churn?

├─ High commits + High lines changed?
│  └─ "Volatile area"
│     • Is this refactoring? If yes, normal
│     • Is this instability? If yes, investigate quality
│     • Check: Are tests adequate?
│     • Check: Is design clear?
│
├─ Many small commits + Few lines?
│  └─ "Polishing phase"
│     • Normal for stable areas getting refinement
│     • Could consolidate commits for cleaner history
│
└─ Few commits + Many lines?
   └─ "Large infrequent changes"
      • Was this planned? If yes, normal
      • Is this technical debt accumulating? If yes, address
      • Check: Are changes coherent and well-tested?
```

### Decision Tree 3: Responding to Pain Signals

```
Found high pain score?

├─ Multiple reverts (fixes undone)?
│  └─ "Systemic issue - solutions don't work"
│     • Root cause: Design flaw? Testing gap? Unclear requirements?
│     • Action: Don't patch more - redesign
│
├─ Clustered bug fixes (many small fixes)?
│  └─ "Area has real problems"
│     • Root cause: Complexity too high? Wrong approach?
│     • Action: Consider refactoring vs rewrite
│
└─ Frequent hotfixes (urgent patches)?
   └─ "Quality issue - reaching production broken"
      • Root cause: Testing gap? Process issue?
      • Action: Improve testing + review before action
```

---

## Using Signals for Decisions

### Before `/pb-evolve` Quarterly Planning

Run git-signals to inform what to prioritize:

```bash
# Get latest signals
python scripts/git-signals.py

# Review adoption to see what's active
cat todos/git-signals/latest/signals-summary.md

# Review pain points to see what needs work
python3 -c "import json; data = json.load(open('todos/git-signals/latest/pain-points-report.json')); print([x['file'] for x in data['pain_score_by_file'][:10]])"

# Use signals to guide evolution priorities
# Example: If pb-guide has pain_score 8, consider refactoring in Q2
```

**Pain Score Interpretation Guide:**
| Score | Status | Action |
|-------|--------|--------|
| 0-2 | Healthy | No action needed |
| 3-5 | Monitor | May need attention in next cycle |
| 6-8 | Investigate | Consider for next quarter's evolution work |
| 9+ | Priority | Address soon; may indicate systemic issues |

### When Investigating an Area

```bash
# Get churn history
python scripts/git-signals.py --since "6 months ago"

# Check adoption in that area
python scripts/git-signals.py

# Use git commands for manual investigation
git log --follow commands/area/file.md  # See file history
git log --oneline -p commands/area/file.md | grep -i "fix\|bug" | head -20  # Recent fixes
```

### When Planning Refactoring

Prioritize high-churn, high-pain areas:

```bash
# Get signals
python scripts/git-signals.py

# Identify candidates (high churn + high pain)
# These are "hot spots" that would benefit most from refactoring
```

---

## Output Files Reference

### `adoption-metrics.json` Structure

```json
{
  "commands_by_touch_frequency": [
    {
      "command": "pb-guide",
      "touches": 47
    }
  ],
  "files_by_change_frequency": [
    {
      "file": "commands/core/pb-guide.md",
      "changes": 45
    }
  ],
  "authors_per_command": {
    "pb-guide": 8,
    "pb-preamble": 5
  },
  "least_active_commands": [
    {
      "command": "pb-legacy",
      "touches": 2
    }
  ]
}
```

### `churn-analysis.json` Structure

```json
{
  "files_by_commit_frequency": [
    {
      "file": "commands/core/pb-guide.md",
      "commits": 150
    }
  ],
  "files_by_line_changes": [
    {
      "file": "commands/core/pb-guide.md",
      "line_changes": 5000
    }
  ],
  "high_churn_areas": [
    {
      "file": "commands/core/pb-guide.md",
      "line_changes": 5000,
      "commits": 150,
      "avg_change_per_commit": 33
    }
  ]
}
```

### `pain-points-report.json` Structure

```json
{
  "reverted_commits": [
    {
      "hash": "abc1234",
      "subject": "Revert \"feat: add feature\"",
      "date": "2025-01-10",
      "author": "Jane Doe"
    }
  ],
  "bug_fix_patterns": [
    {
      "hash": "def5678",
      "subject": "fix: resolve bug",
      "date": "2025-01-05"
    }
  ],
  "hotfix_patterns": [
    {
      "hash": "ghi9012",
      "subject": "hotfix: critical issue",
      "date": "2025-01-01"
    }
  ],
  "pain_score_by_file": [
    {
      "file": "commands/core/pb-guide.md",
      "pain_score": 8
    }
  ],
  "summary": {
    "total_reverts": 12,
    "total_bug_fixes": 47,
    "total_hotfixes": 5
  }
}
```

---

## Examples

### Example 1: Checking What's Hot This Week

```bash
$ python scripts/git-signals.py --since "1 week ago"

# Review the summary
$ cat todos/git-signals/latest/signals-summary.md

# Output shows:
# - pb-guide had 12 touches in the past week
# - commands/development/ is highest churn area
# - 2 bug fixes in that area
#
# Insight: Development area is getting active work, likely preparing for release
```

### Example 2: Identifying Stale Commands

```bash
# Run signals
$ python scripts/git-signals.py

# Check least active
$ python3 -c "import json; data=json.load(open('todos/git-signals/latest/adoption-metrics.json')); print('Least active commands:', [c['command'] for c in data['least_active_commands'][:5]])"

# Output:
# Least active commands: ['pb-old-pattern', 'pb-legacy-tool', 'pb-deprecated']
#
# Action: Review these for potential deprecation or removal
```

### Example 3: Finding Problematic Areas Before Refactoring

```bash
# Get signals with 6-month history
$ python scripts/git-signals.py --since "6 months ago"

# Check high-pain areas
$ python3 -c "import json; data=json.load(open('todos/git-signals/latest/pain-points-report.json')); areas=[x for x in data['pain_score_by_file'] if x['pain_score'] > 5]; print('Problem areas:', areas)"

# Output:
# Problem areas: [
#   {'file': 'commands/core/pb-standards.md', 'pain_score': 12},
#   {'file': 'scripts/validate.py', 'pain_score': 8}
# ]
#
# Action: These are candidates for refactoring/redesign
```

---

## Integration with /pb-evolve: Quarterly Planning

Git signals exist to feed data-driven decision-making into quarterly playbook evolution cycles.

### Before Running /pb-evolve

**Step 1: Generate signals with 3-month window**

```bash
# Get quarterly data for planning input
python scripts/git-signals.py --since "3 months ago"

# Verify outputs exist
ls -la todos/git-signals/latest/
# Should show: adoption-metrics.json, churn-analysis.json, pain-points-report.json, signals-summary.md
```

**Step 2: Analyze pain_score_by_file**

```bash
# Extract high-pain areas
python3 << 'EOF'
import json

with open('todos/git-signals/latest/pain-points-report.json') as f:
    data = json.load(f)

# Sort by pain score descending
pain_areas = sorted(data['pain_score_by_file'], key=lambda x: x['pain_score'], reverse=True)

print("=== HIGH-PAIN EVOLUTION CANDIDATES ===\n")
for area in pain_areas[:10]:
    score = area['pain_score']
    file = area['file']
    status = "CRITICAL" if score >= 9 else "HIGH" if score >= 6 else "MODERATE"
    print(f"{status:10} | Score: {score:2} | {file}")
EOF
```

### Using Signals to Shape /pb-evolve

**Before the evolution session, create an input document:**

```markdown
# Input to /pb-evolve: Signal-Based Priorities

## Critical Pain Areas (Score 9-10)
- [file]: [pain_score] - [reverts/bug_fixes/hotfixes pattern]
  - Action: Review for redesign or rewrite
  - Effort: Likely 4+ hours

## High Pain Areas (Score 6-8)
- [file]: [pain_score] - [pattern]
  - Action: Plan refactoring
  - Effort: 2-4 hours

## High-Activity Areas (Many touches, low pain)
- [file]: [touches] touches - Stable, working well
  - Action: Monitor for performance regression
  - Action: Use as exemplar pattern

## Stale Areas (Low activity, no pain)
- [file]: [touches] touches - Candidate for deprecation
  - Action: Review for removal
  - Action: Archive if not needed
```

**During /pb-evolve, these become:**
- **Priority 1 (Critical):** Redesign/rewrite high-pain areas
- **Priority 2 (Optimization):** Refactor high-churn areas
- **Priority 3 (Monitoring):** Verify stable high-activity areas stay healthy
- **Priority 4 (Deprecation):** Remove or archive stale code

### Real Quarterly Evolution Workflow

**Month 1 of quarter (e.g., February):**
```bash
# Week 1
python scripts/git-signals.py --since "3 months ago"
# Analyze outputs, create priority document

# Week 2: Kickoff /pb-evolve session
/pb-evolve
# Use signal-based priorities to shape decisions
# Update playbooks based on findings

# Week 3-4: Implement evolution changes
# Per the /pb-evolve decisions
```

**Integration checkpoint:**

Before committing evolution changes, verify:
- [ ] Evolution decisions referenced pain scores where applicable
- [ ] High-pain areas from signals are addressed
- [ ] Evolution changelog documents signal-based prioritization
- [ ] Next quarter's signals will measure evolution impact

---

## Real-World Workflow Example

### Scenario: Playbook Quarterly Evolution (Q1 → Q2)

**Monday, May 5 (Start of Q2)**

Developer runs:
```bash
python scripts/git-signals.py --since "3 months ago"
cat todos/git-signals/latest/signals-summary.md
```

Output shows:
```
ADOPTION SIGNALS (Q1):
- pb-guide: 47 touches (most active)
- pb-cycle: 32 touches
- pb-pause: 18 touches
- pb-legacy-pattern: 2 touches (candidate for removal)

CHURN ANALYSIS:
- commands/core/pb-guide.md: 5000 line changes (high activity)
- commands/development/pb-cycle.md: 3200 line changes
- scripts/validate.py: 2100 line changes

PAIN SCORE ANALYSIS:
- commands/core/pb-guide.md: pain_score 8 (3 reverts, 5 bug fixes)
- commands/planning/pb-plan.md: pain_score 6 (2 reverts, 3 bug fixes)
- commands/core/pb-patterns.md: pain_score 3 (stable)
- commands/legacy/pb-old-pattern.md: pain_score 0 (stale, no activity)
```

**Tuesday, May 6 (Analysis & Planning)**

Developer reviews and documents:
```markdown
# Q1 Signal Analysis → Q2 Evolution Priorities

## Critical Areas Needing Attention
1. **pb-guide** (pain_score 8)
   - Issue: Multiple reverts and fixes in Q1
   - Root cause: Ambiguous wording in several sections
   - Action: Clarity refactor, simplify sections 3-5
   - Effort: 2-3 hours

2. **pb-plan** (pain_score 6)
   - Issue: Users reported confusion in planning workflow
   - Root cause: Missing decision trees and examples
   - Action: Add concrete examples, clarify decision paths
   - Effort: 1-2 hours

## Stable Areas (Monitor)
3. **pb-patterns** (pain_score 3)
   - Status: Working well, few issues
   - Action: Use as exemplar pattern for future commands
   - Next: Expand with new patterns discovered this quarter

## Deprecation Candidates
4. **pb-old-pattern** (pain_score 0, 2 touches in 6 months)
   - Status: Stale, no adoption
   - Action: Archive or remove in Q2
   - Effort: 30 minutes
```

**Wednesday-Friday, May 7-9 (Evolution Implementation)**

1. Run `/pb-evolve` with signal-based priorities as input
2. Implement changes to pb-guide (clarity refactoring)
3. Implement changes to pb-plan (add examples)
4. Archive pb-old-pattern
5. Update CHANGELOG with evolution summary

**Friday, May 9 (Signal-Based Outcome Measurement)**

Document in evolution log:
```
## Evolution Impact (Q2 Planning)

**Input signals:**
- pb-guide pain_score: 8 (3 reverts, 5 bug fixes)
- pb-plan pain_score: 6 (2 reverts, 3 bug fixes)

**Changes made:**
- Rewrote pb-guide sections 3-5 for clarity
- Added decision trees to pb-plan
- Removed pb-old-pattern (stale)

**Success metrics (check in 4 weeks):**
- pb-guide pain_score should drop to ≤4
- pb-plan usage and quality feedback improve
- No new reverts in updated sections

**Measurement date: June 6 (Check after 4 weeks of Q2 usage)**
```

**June 6 (Validate Evolution Impact)**

```bash
# Check if pain scores improved
python scripts/git-signals.py --since "4 weeks ago"

# Expected outcome:
# pb-guide pain_score: 2-3 (down from 8) ← Evolution worked
# pb-plan pain_score: 3-4 (down from 6) ← Evolution helped
# pb-old-pattern: 0 (removed) ← Deprecation successful

# If scores didn't improve:
# - Root cause analysis
# - Plan additional work for Q2
# - Document learning in evolution log
```

### Integration Verification Checklist

✅ **Signal Generation Phase**
- [ ] Signals run with correct time window (--since "3 months ago")
- [ ] pain_score_by_file analyzed for evolution input
- [ ] High-pain areas documented with context

✅ **Evolution Planning Phase**
- [ ] /pb-evolve uses signal-based priorities
- [ ] Evolution decisions reference specific pain scores
- [ ] Critical areas (score 6+) addressed in evolution plan

✅ **Evolution Implementation Phase**
- [ ] Changes implemented per signal-informed priorities
- [ ] Evolution log documents signal input

✅ **Outcome Measurement Phase**
- [ ] Signals rerun after 4 weeks
- [ ] Pain scores tracked for improved vs stable vs regressed
- [ ] Learning documented for next evolution cycle

---

## Limitations & Caveats

**What signals can tell you:**
- Historical frequency and patterns
- Relative activity levels
- Explicit problems (reverts, bug keywords)

**What signals cannot tell you:**
- Quality or correctness of code
- Architectural soundness
- User satisfaction
- Future maintenance costs
- Impact of changes

**Use with:**
- Manual code review (signals point you there)
- Team discussion (why is this area high-churn?)
- Other data sources (user feedback, support tickets)
- Your judgment (signals inform, not decide)

---

## Related Commands

- `/pb-evolve` - Quarterly planning that uses signals as input
- `/pb-context` - Project context and working state
- `/pb-learn` - Learning patterns from playbooks
- `/pb-cycle` - Development workflow (where the git history comes from)

---

## FAQ

**Q: How often should I run this?**
A: Weekly for trend spotting, before quarterly planning for strategic input. Ad-hoc when investigating.

**Q: Why is command X high-touch but I never use it?**
A: High touch = edited frequently, not necessarily used. Could be frequently fixed or updated.

**Q: Can I use this for my own projects?**
A: Yes! The script works on any git repository. Just run it in your project root.

**Q: What time range should I analyze?**
A: Weekly (1 week) for trends, quarterly (3 months) for planning, annually (1 year) for patterns.

**Q: How do I integrate with /pb-evolve?**
A: Run signals before evolve planning session, reference pain_score_by_file as priority input.

---

*Git history reveals truth about what we actually build and maintain, not what we intended to build.*
