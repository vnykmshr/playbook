---
name: "pb-git-signals"
title: "Extract Git History Signals"
category: "core"
difficulty: "beginner"
model_hint: "haiku"
execution_pattern: "sequential"
related_commands: ['pb-evolve', 'pb-context', 'pb-learn']
last_reviewed: "2026-02-12"
last_evolved: ""
version: "1.0.0"
version_notes: "v2.12.0 Phase 3: Initial release with adoption, churn, pain point analysis"
breaking_changes: []
---

# Extract Git History Signals

**Purpose:** Analyze git history to extract adoption, churn, and pain point signals for data-driven decision making.

**Mindset:** Use git history as a source of truth for understanding what's actually used, what changes frequently, and where pain points exist. These signals inform quarterly evolution planning and ad-hoc investigations.

Apply `/pb-preamble` thinking: challenge what the signals reveal about project health. Apply `/pb-design-rules` thinking: are we building the right things? Are we fixing the same areas repeatedly?

**Resource Hint:** haiku — Git history analysis; structured data extraction from commit patterns

---

## When to Use

- **Weekly check** — "What's been hot this week?"
- **Before quarterly planning** — Input for `/pb-evolve` decision making
- **After incidents** — Investigate pain patterns
- **Before refactoring** — Identify high-churn areas
- **Onboarding** — Show new team members what's active
- **Ad-hoc investigation** — "Why is this area changing so much?"

---

## Quick Start

### One-Time Run (Latest Analysis)

```bash
python scripts/git-signals.py
```

Outputs to `todos/git-signals/latest/`:
- `adoption-metrics.json` — Which commands/files are most touched
- `churn-analysis.json` — Which areas change frequently
- `pain-points-report.json` — Reverts, bug fixes, hotfixes
- `signals-summary.md` — Human-readable overview

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
- `commands_by_touch_frequency` — Top 20 commands by git touches (all commits mentioning that file)
- `files_by_change_frequency` — Top 20 files by modification count
- `authors_per_command` — How many unique authors touched each command
- `least_active_commands` — Bottom 10 (candidates for review or removal)

**How to interpret:**
- High touch frequency = well-maintained or frequently used
- Low frequency = stale, abandoned, or stable
- Single author = potential knowledge bottleneck

**Example:**
```
Most active: pb-guide (47 touches, 8 authors)
  → Core content, actively maintained, distributed ownership
Least active: pb-legacy-tool (2 touches, 1 author)
  → Likely deprecated or superseded
```

### Churn Analysis (`churn-analysis.json`)

**What it shows:** Which areas change frequently (high volatility)

**Key fields:**
- `files_by_commit_frequency` — How many commits touch each file
- `files_by_line_changes` — Total lines added/deleted per file
- `high_churn_areas` — Files with most activity (lines + commit frequency combined)

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
- `reverted_commits` — Commits that were later reverted (explicit undo)
- `bug_fix_patterns` — Commits with 'fix:', 'bug:', or 'bugfix' in subject
- `hotfix_patterns` — Urgent fixes ('hotfix', 'critical', 'p0:', 'p1:')
- `pain_score_by_file` — Composite score based on fixes+reverts
- `summary` — Counts of each pattern type

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
- Action: Investigate — is this active work or a problem?
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
- Action: Root cause analysis — process, design, or testing issue?
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

- `/pb-evolve` — Quarterly planning that uses signals as input
- `/pb-context` — Project context and working state
- `/pb-learn` — Learning patterns from playbooks
- `/pb-cycle` — Development workflow (where the git history comes from)

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
