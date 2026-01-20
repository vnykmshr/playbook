# Metadata Extraction

The Playbook automatically extracts metadata from command files to enable discovery, search, and workflow automation. This guide explains the system and how to write extraction-friendly commands.

---

## How It Works

**Extraction runs automatically during docs deployment** (`deploy-docs.yml`).

```
commands/*.md → extract-playbook-metadata.py → .playbook-metadata.json
```

**What gets extracted:**
- Command name, title, category
- Purpose (first paragraph)
- Related commands (all `/pb-*` references)
- Workflow sequences (next steps, prerequisites)
- Tier applicability (XS, S, M, L)
- Content metadata (has examples, has checklist)

**Validation** can be run manually via `validate-metadata.yml` workflow (manual trigger) or locally:

```bash
python scripts/extract-playbook-metadata.py --verbose
python scripts/validate-extracted-metadata.py
```

---

## Writing Extraction-Friendly Commands

Follow this structure for high-confidence metadata extraction:

```markdown
# Command Title

One-line purpose that describes what this command does.

---

## When to Use

Clear guidance on when to use this command:
- Specific scenarios
- Types of work (feature, fix, refactor)
- Tiers if applicable (XS, S, M, L)

---

## Prerequisites

What must be done first:
- Related commands to run: `/pb-something`
- Setup steps

---

## Core Workflow

1. First step using `/pb-related-command`
2. Next step
3. Final step, then `/pb-next-command`

---

## Next Steps

After completing this command:
1. Run `/pb-next-command` for X
2. Use `/pb-another-command` if Y
```

---

## Quick Principles

1. **Structure First** — Use consistent markdown structure
2. **Be Explicit** — State context, decisions, and workflows clearly
3. **Reference Commands** — Link related `/pb-*` commands throughout
4. **Use Sections** — Organize with `##` headings
5. **List Workflows** — Show step-by-step processes in numbered order

---

## Field-Specific Guidance

### Title (h1)
- 5-80 characters
- Start with action verb (Start, Build, Review, Create)
- Avoid generic titles ("Help", "Guide")

### Purpose (First Paragraph)
- 20-300 characters
- Complete sentence explaining what command does
- Place immediately after h1, before `---`

### When to Use Section
- List specific scenarios
- Include tier info if applicable
- State what NOT to use it for

### Workflow Section
- Use numbered lists (shows sequence)
- Include `/pb-*` references at logical points
- Each step should be a complete action

### Related Commands
- Reference naturally in text: "Use `/pb-cycle` for review"
- Every `/pb-*` mention is extracted as a relationship

### Tier Information
- Explicit: `Tier: S` or `Tier: [S, M, L]`
- Or include in a table showing requirements per tier

---

## Authoring Checklist

When writing or updating commands:

- [ ] Title: Clear, 5-80 chars, starts with action verb
- [ ] Purpose: First paragraph, 20-300 chars, complete sentence
- [ ] When to Use: Explicit conditions, tier guidance if applicable
- [ ] Prerequisites: Clear `/pb-*` references for required setup
- [ ] Workflow: Numbered steps with `/pb-*` references
- [ ] Related Commands: 3-10 `/pb-*` references naturally placed
- [ ] Examples: At least one code block
- [ ] Next Steps: Clear path to next command(s)
- [ ] No TODOs: Remove TODO/FIXME comments before committing

---

## Quality Expectations

**Extraction targets:**
- All commands extracted successfully
- Average confidence >= 80%
- Zero critical errors (missing required fields)

**Required fields** (must be present):
- `command` (from filename)
- `title` (from h1)
- `category` (from directory)
- `purpose` (from first paragraph)

**Optional fields** (extracted when clear):
- `tier`, `related_commands`, `next_steps`, `prerequisites`
- `frequency`, `decision_context`
- `has_examples`, `has_checklist`

---

## Common Mistakes

| Mistake | Instead |
|---------|---------|
| Generic titles ("Help", "Guide") | Action-oriented ("Create Production Release") |
| Vague purpose ("Does things") | Specific ("Automate release validation") |
| Missing "When to Use" | List explicit scenarios |
| Orphaned references (`/pb-xyz` alone) | Context: "Use `/pb-cycle` for peer feedback" |
| Unordered workflows (bullets) | Numbered lists for sequences |
| No examples | Include concrete code blocks |

---

## Validation Workflow

The `validate-metadata.yml` workflow is available for manual triggering:

1. Extracts metadata from all commands
2. Validates against quality rules
3. Reports confidence scores and errors
4. Generates quality report

**To run locally:**
```bash
# Extract metadata
python scripts/extract-playbook-metadata.py --verbose

# Validate extracted metadata
python scripts/validate-extracted-metadata.py

# Check the output
cat .playbook-metadata.json | python -m json.tool | head -50
```

---

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `extract-playbook-metadata.py` | Extract metadata from commands |
| `validate-extracted-metadata.py` | Validate metadata quality |
| `generate-quick-ref.py` | Generate quick reference from metadata |

---

*The detailed validation rules are implemented in the scripts themselves. This guide focuses on what command authors need to know.*
