# Metadata Quality Rules

This document defines validation rules and quality standards for playbook command metadata. These rules ensure that extracted metadata is accurate, complete, and useful for discovery tools.

---

## Overview

Metadata quality is measured on two dimensions:

1. **Structural Quality**: Is the metadata valid and well-formed?
2. **Semantic Quality**: Is the metadata accurate and useful?

All extracted metadata must pass structural quality checks before use.

---

## Field-Level Rules

### Identity Fields

#### `command`
**Purpose**: Unique command identifier
**Rule**: Extract from filename `pb-<name>.md` → `pb-<name>`

**Quality Criteria**:
- ✅ Matches filename exactly
- ✅ Format: `pb-` prefix + lowercase letters/hyphens
- ✅ No special characters except hyphen
- ✅ 4-50 characters total
- ✅ Unique across all 49 commands

**Validation**:
```python
assert re.match(r'^pb-[a-z-]{2,48}$', command)
assert command_exists_in_files
assert command_is_unique
```

**Examples**:
- ✅ `pb-start`, `pb-cycle`, `pb-review-code`
- ❌ `pb_start`, `pb-Start`, `pb-`, `pbstart`

---

#### `title`
**Purpose**: Human-readable command name
**Rule**: First h1 heading in markdown file

**Quality Criteria**:
- ✅ Extracted from `# ...` markdown heading
- ✅ No markdown syntax in value (plain text)
- ✅ 5-80 characters
- ✅ Starts with capital letter
- ✅ Action-oriented (verb-first preferred)
- ✅ Unique or near-unique (no duplicate titles)
- ✅ No generic words like "Help", "Guide", "Information"

**Validation**:
```python
assert len(title) >= 5 and len(title) <= 80
assert title[0].isupper()
assert not any(word in title.lower() for word in ["help", "guide", "information"])
assert title.count('**') == 0  # No markdown
```

**Examples**:
- ✅ "Start Development Work"
- ✅ "Engineering SDLC Playbook"
- ❌ "Help" (too generic)
- ❌ "Command #1" (not descriptive)

---

#### `category`
**Purpose**: Command classification
**Rule**: Parent directory name from `commands/<category>/pb-<name>.md`

**Quality Criteria**:
- ✅ Must be one of: core, development, planning, reviews, release, deployment, repo, people, templates
- ✅ Matches directory structure exactly
- ✅ No ambiguity (1:1 with directory)
- ✅ Consistent across all commands

**Validation**:
```python
valid_categories = {
    "core", "development", "planning", "reviews",
    "release", "deployment", "repo", "people", "templates"
}
assert category in valid_categories
```

**Command Distribution** (Expected):
- core: 4 commands
- development: 8 commands
- planning: 8+ commands
- reviews: 9+ commands
- release: 1 command
- deployment: 2 commands
- repo: 6+ commands
- people: 2 commands
- templates: 1+ commands
- **Total**: 49 commands

---

### Description Fields

#### `purpose`
**Purpose**: One-sentence summary of what the command does
**Rule**: First non-heading paragraph after h1 (before `---`)

**Quality Criteria**:
- ✅ Extracted as plain text (no markdown)
- ✅ 20-300 characters
- ✅ Complete sentence with subject and verb
- ✅ Describes action/outcome, not implementation
- ✅ No acronyms without explanation
- ✅ No TODO/FIXME comments
- ✅ Unique or near-unique across commands

**Validation**:
```python
assert 20 <= len(purpose) <= 300
assert purpose[-1] in '.!?'  # Ends with punctuation
assert 'TODO' not in purpose.upper()
assert 'FIXME' not in purpose.upper()
# Should contain action verb
verbs = ['begin', 'create', 'start', 'build', 'review', 'write', 'run', 'execute']
assert any(verb in purpose.lower() for verb in verbs)
```

**Examples**:
- ✅ "Begin iterative development on a feature, enhancement, or fix."
- ✅ "Automate release validation and deployment to production."
- ❌ "This command does development work" (vague action)
- ❌ "TODO: add description" (incomplete)

---

### Complexity Fields

#### `tier`
**Purpose**: Complexity tier(s) this command applies to
**Rule**: Extract from explicit tier mentions or complexity indicators

**Quality Criteria**:
- ✅ One or more of: XS, S, M, L
- ✅ If multiple, ordered as: [XS, S, M, L]
- ✅ Matches content context (e.g., `/pb-guide` should have all tiers)
- ✅ If confidence < 0.70, not included in metadata

**Extraction Confidence by Pattern**:
- 100%: Explicit "Tier: X" or table with tiers
- 85%: Complexity keywords (simple, medium, large)
- 75%: Scope indicators (single-file, multi-file, service-wide)
- 60%: Inferred from category/content

**Validation**:
```python
valid_tiers = {'XS', 'S', 'M', 'L'}
if tier:
    for t in tier:
        assert t in valid_tiers
    # If multiple, must be in order
    tier_order = {'XS': 0, 'S': 1, 'M': 2, 'L': 3}
    assert [tier_order[t] for t in tier] == sorted([tier_order[t] for t in tier])
```

**Examples**:
- ✅ "S" (applies to small changes)
- ✅ ["S", "M", "L"] (applies to multiple tiers)
- ✅ None (if not applicable or unclear)
- ❌ ["M", "S"] (wrong order)

---

### Relationship Fields

#### `related_commands`
**Purpose**: Other /pb-* commands mentioned in this command
**Rule**: All /pb-<name> references found in markdown text

**Quality Criteria**:
- ✅ Format: `/pb-<name>` (with slash prefix)
- ✅ Each command must exist in commands/ directory
- ✅ Excludes the command's own name
- ✅ No duplicates
- ✅ Sorted alphabetically
- ✅ Typically 3-15 related commands
- ✅ None are circular (no A→B→A→B chains)

**Extraction Confidence**:
- 100%: Pattern matching on /pb-<name> format
- Variable: Cross-validation against actual command files

**Validation**:
```python
for cmd in related_commands:
    assert re.match(r'^/pb-[a-z-]+$', cmd)
    assert cmd != f"/{command}"  # Not self-reference
    assert cmd_exists(cmd)  # Must exist
assert len(related_commands) == len(set(related_commands))  # No duplicates
assert related_commands == sorted(related_commands)
```

**Example**:
```python
related_commands = [
    "/pb-commit",
    "/pb-cycle",
    "/pb-standards",
    "/pb-testing"
]
```

---

#### `next_steps`
**Purpose**: Workflow sequence - commands to run after this one
**Rule**: Extract from "Next Steps" section, "then use", workflow sequences

**Quality Criteria**:
- ✅ Format: List of `/pb-<name>` commands
- ✅ Each command must exist
- ✅ Order indicates workflow sequence (important)
- ✅ Typically 1-5 commands
- ✅ Should match next steps documented in command
- ✅ Confidence depends on clarity of workflow
- ✅ If unclear, confidence < 0.70, exclude from metadata

**Extraction Confidence**:
- 100%: Explicit "Next Steps" section with ordered /pb-* references
- 85%: "Then use" or "Next:" patterns in workflow
- 70%: Related commands inferred from context
- <70%: Exclude if unclear

**Validation**:
```python
if next_steps:
    for cmd in next_steps:
        assert cmd_exists(cmd)
    assert len(next_steps) <= 5
    # No duplicates
    assert len(next_steps) == len(set(next_steps))
```

**Example**:
```python
next_steps = ["/pb-cycle", "/pb-commit", "/pb-pr"]
```

---

#### `prerequisites`
**Purpose**: Commands that should run before this one
**Rule**: Extract from "Prerequisites" or "Before" sections

**Quality Criteria**:
- ✅ Format: List of `/pb-<name>` commands
- ✅ Each must exist
- ✅ Order indicates execution sequence
- ✅ Typically 0-3 commands
- ✅ Only if explicitly required (not optional)

**Validation**:
```python
if prerequisites:
    for cmd in prerequisites:
        assert cmd_exists(cmd)
    assert len(prerequisites) <= 3
```

**Example**:
```python
prerequisites = ["/pb-guide", "/pb-start"]
```

---

### Usage Pattern Fields

#### `frequency`
**Purpose**: How often this command is used
**Rule**: Extract from "When to Use" section or frequency keywords

**Quality Criteria**:
- ✅ One of: daily, weekly, start-of-feature, per-iteration, per-pr, pre-release, on-incident, one-time, as-needed
- ✅ Matches actual usage patterns
- ✅ Confidence < 0.70 if unclear

**Extraction Confidence**:
- 100%: Explicit frequency in text
- 85%: Inferred from "When to Use" keywords
- 75%: Inferred from command purpose
- <70%: Default to "as-needed"

**Valid Values**:
```python
valid_frequencies = {
    "daily",              # Everyday routine
    "weekly",             # Weekly activity
    "start-of-feature",   # Feature kickoff
    "per-iteration",      # Each iteration
    "per-pr",             # Before PR
    "pre-release",        # Release prep
    "on-incident",        # During incident
    "one-time",           # Initial setup
    "as-needed"           # Situational
}
```

**Example**:
- `/pb-start` → `start-of-feature`
- `/pb-cycle` → `per-iteration`
- `/pb-release` → `pre-release`

---

#### `decision_context`
**Purpose**: Conditions for choosing this command vs alternatives
**Rule**: Extract from "When to Use", conditional logic, binary choices

**Quality Criteria**:
- ✅ Clear decision rules or conditions
- ✅ Shows when to use this vs alternatives
- ✅ Structured as key-value pairs or branches
- ✅ Confidence < 0.70 if implicit or unclear

**Extraction Confidence**:
- 85%: Explicit decision tables ("feature→X", "hotfix→Y")
- 75%: Clear "When to Use" section with conditions
- 70%: Implicit decision logic
- <70%: Exclude if unclear

**Example**:
```python
decision_context = {
    "feature_work": "/pb-cycle",
    "hotfix": "/pb-release",
    "security_critical": "/pb-security",
    "performance_sensitive": "/pb-performance"
}
```

---

### Content Fields

#### `sections`
**Purpose**: List of h2 sections in command
**Rule**: Extract all `##` headings

**Quality Criteria**:
- ✅ Slugified names (lowercase, hyphens)
- ✅ In order of appearance
- ✅ Reflects command structure

**Example**:
```python
sections = [
    "when-to-use",
    "prerequisites",
    "core-workflow",
    "examples",
    "next-steps"
]
```

---

#### `has_examples`
**Purpose**: Whether command includes code examples
**Rule**: Boolean - true if ``` code blocks found

**Quality Criteria**:
- ✅ Boolean value
- ✅ 100% confidence (objective check)
- ✅ Examples should be realistic and runnable

---

#### `has_checklist`
**Purpose**: Whether command includes action checklist
**Rule**: Boolean - true if [ ] checkbox syntax found

**Quality Criteria**:
- ✅ Boolean value
- ✅ 100% confidence
- ✅ Checklists should be actionable

---

## Cross-Field Validation Rules

### Rule: No Self-References
```
related_commands must NOT include the command's own name
```

### Rule: Valid Command References
```
All /pb-* references in related_commands, next_steps, prerequisites
must exist as actual command files
```

### Rule: No Circular Dependencies
```
If A→B and B→C, then C should not→A
(Workflows should have clear end points)
```

### Rule: Tier Consistency
```
If tier specified, content must match tier descriptions
(e.g., "M" tier should mention multi-file changes)
```

### Rule: Frequency Alignment
```
Frequency must make sense with "When to Use" context
(e.g., "daily" should not be marked "one-time")
```

### Rule: Decision Context Consistency
```
Alternative commands referenced in decision_context
must be valid /pb-* commands
```

---

## Data Quality Metrics

### Extraction Success Rate
```python
success_rate = (commands_extracted_successfully / total_commands) * 100

Target: 100%
Acceptable: ≥ 95%
Action if below: Review extraction script for issues
```

### Average Confidence Score
```python
avg_confidence = sum(confidence_scores) / len(confidence_scores)

Target: ≥ 0.90
Acceptable: ≥ 0.80
Action if below 0.80:
  - Review low-confidence fields
  - Provide suggestions to command authors
  - Schedule command structure improvements
```

### Per-Field Confidence
```python
Minimum acceptable by field:
  - command: 1.0 (100%)
  - title: 1.0 (100%)
  - category: 1.0 (100%)
  - purpose: 0.95 (95%)
  - tier: 0.70 (70%)
  - related_commands: 0.95 (95%)
  - next_steps: 0.75 (75%)
  - frequency: 0.70 (70%)
  - decision_context: 0.70 (70%)
```

### Data Completeness
```python
required_fields_present = [
    command_present,
    title_present,
    category_present,
    purpose_present
]

assert all(required_fields_present), "Missing required fields"

optional_fields_present = [
    tier, related_commands, next_steps,
    frequency, decision_context, etc.
]

completeness = len([f for f in optional_fields_present if f]) / len(optional_fields_present)
Target: ≥ 0.70 (at least 70% of optional fields)
```

---

## Error Levels

### CRITICAL (Block Release)
- Any required field missing
- Invalid category value
- Command doesn't exist (for references)
- Circular dependencies detected
- Confidence 0% on command/title/category

**Action**: Halt extraction, fix source command, re-run

### WARNING (Include in Report)
- Confidence < 0.70 on any field
- Missing optional fields
- Inconsistent tier/purpose
- Related commands not found (maybe typo)

**Action**: Suggest improvements, include in report

### INFO (Log Only)
- Low confidence on inferred fields
- Suggestions for extraction improvement
- Metadata quality improvements

**Action**: Track, report to command authors

---

## Quality Improvement Process

### When Average Confidence < 0.90

1. **Identify low-confidence fields**:
   ```python
   low_confidence = [
       (cmd, field, score)
       for cmd, fields in metadata.items()
       for field, score in fields.items()
       if score < 0.80
   ]
   ```

2. **Generate improvement suggestions**:
   - Missing "When to Use" section
   - Vague purpose statement
   - No tier specification
   - Missing /pb-* references

3. **Provide to command authors**:
   - Specific suggestions
   - Reference EXTRACTION-GUIDE.md
   - Show before/after examples

4. **Re-extract after improvements**:
   - Re-run extraction script
   - Verify confidence improvements
   - Update .playbook-metadata.json

---

## Validation Checklist

Before accepting extracted metadata:

- [ ] All 49 commands extracted
- [ ] Zero CRITICAL errors
- [ ] All required fields present for all commands
- [ ] Average confidence ≥ 0.90
- [ ] All command references are valid
- [ ] No circular dependencies
- [ ] Category distribution matches expected counts
- [ ] .playbook-metadata.json is valid JSON
- [ ] No hardcoded secrets in metadata
- [ ] Extraction report generated

---

## Examples

### High Quality Metadata
```json
{
  "command": "pb-start",
  "title": "Start Development Work",
  "category": "development",
  "purpose": "Begin iterative development on a feature, enhancement, or fix.",
  "tier": ["S", "M", "L"],
  "related_commands": ["/pb-cycle", "/pb-commit", "/pb-standards"],
  "next_steps": ["/pb-cycle"],
  "frequency": "start-of-feature",
  "has_examples": true,
  "has_checklist": true,
  "confidence_scores": {
    "command": 1.0,
    "title": 1.0,
    "category": 1.0,
    "purpose": 0.98,
    "tier": 0.95,
    "related_commands": 0.98,
    "next_steps": 0.90,
    "frequency": 0.85
  },
  "average_confidence": 0.95
}
```

### Low Confidence Metadata
```json
{
  "command": "pb-example",
  "title": "Example Command",
  "category": "development",
  "purpose": "Do something.",
  "tier": null,  # No tier info
  "related_commands": [],  # No references
  "next_steps": null,  # No workflow
  "frequency": "as-needed",  # Default fallback
  "confidence_scores": {
    "command": 1.0,
    "title": 1.0,
    "category": 1.0,
    "purpose": 0.60,  # Too vague
    "tier": 0.0,  # Not found
    "related_commands": 0.0,  # No references
    "next_steps": 0.0,  # No workflow
    "frequency": 0.30  # Defaulted
  },
  "average_confidence": 0.44,
  "warnings": [
    "Purpose too vague. Add context about what command does.",
    "No tier information. Add 'Tier: S' or 'Tier: M' to command.",
    "No related commands found. Add /pb-* references to show context.",
    "No workflow defined. Add 'Next Steps' section."
  ]
}
```

---

## For Implementation

These rules are enforced in:
- `scripts/extract-playbook-metadata.py` — Extraction logic
- `scripts/validate-extracted-metadata.py` — Validation & reporting
- CI/CD pipeline — Automated validation on every push

---

*Last Updated: 2026-01-12*
*Used by: Extraction and validation scripts*
