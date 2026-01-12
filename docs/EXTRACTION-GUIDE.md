# Command Extraction Guide

This guide helps you write commands that enable high-confidence automated metadata extraction. The Playbook uses intelligent extraction to derive metadata from command structure—not manual entry. Write your commands with extraction in mind to maximize metadata quality.

---

## Quick Principles

1. **Structure First**: Use consistent markdown structure
2. **Be Explicit**: State context, decisions, and workflows clearly
3. **Reference Commands**: Link related /pb-* commands throughout
4. **Use Sections**: Organize with ## headings
5. **List Workflows**: Show step-by-step processes in order

---

## Command Structure (Template)

This is the foundation for high-confidence extraction:

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

What must be done first (if anything):
- Related commands to run: `use /pb-something first`
- Setup steps

---

## Core Workflow

Main workflow with /pb-* references:

1. Do something using `/pb-related-command`
2. Next step
3. Final step, then `/pb-next-command`

---

## [Other sections as needed]

Include sections like:
- Checklist
- Examples
- Troubleshooting

---

## Next Steps

After completing this command:
1. Run `/pb-next-command` for X
2. Use `/pb-another-command` if Y
```

---

## Detailed Guidelines

### 1. Title (h1)

**Format**: `# Clear, Actionable Title`

**Rules**:
- Must be 5-80 characters
- Start with action verb (Start, Build, Review, Create, Fix, etc.)
- Avoid generic titles like "Help" or "Guide"
- Title + purpose combined should be complete thought

**Examples**:
- ✅ "# Start Development Work" — Clear action
- ✅ "# Engineering SDLC Playbook" — Clear scope
- ❌ "# Help" — Too vague
- ❌ "# Command" — Not descriptive

### 2. Purpose (First Paragraph)

**Rules**:
- Place immediately after h1, before any ---
- 20-300 characters
- Complete sentence explaining what command does
- Can reference context or related concepts
- Keep to 1-2 sentences

**Examples**:
```markdown
# Start Development Work

Begin iterative development on a feature, enhancement, or fix.
This command establishes the rhythm for quality-focused, incremental work.
```

✅ Good: Clear purpose in context

```markdown
# Review Code

Get feedback on your code changes from peers and leads.
```

✅ Good: Explains outcome

```markdown
# Security Check

Check if your code has any security issues.
```

❌ Poor: Vague. What kind of issues? How?

### 3. When to Use Section

**Format**: Explicit conditions for when to use this command

**Rules**:
- Use as h2 section: `## When to Use`
- List specific scenarios
- Include tier information if applicable (XS, S, M, L)
- State what NOT to use it for if important
- Use clear, scannable format (bullet points)

**Examples**:

```markdown
## When to Use

Use `/pb-start` when:
- Beginning work on a new feature
- Starting a bug fix
- Planning a refactor of existing code

Do NOT use when:
- Responding to production incidents (use `/pb-release`)
- Writing documentation only (use `/pb-documentation`)

**Tier Assignment:**
- XS/S: Use `/pb-cycle` for self-review, skip peer review if minor
- M: Use full `/pb-cycle` with peer review
- L: Use `/pb-cycle` + `/pb-review` for comprehensive feedback
```

✅ Good: Explicit conditions and tier guidance

```markdown
## When to Use

This command is useful for various scenarios where you need to...
```

❌ Poor: Vague. What scenarios?

### 4. Prerequisites Section

**Format**: What must be done first

**Rules**:
- Use `## Prerequisites` or `## Pre-Start Checklist`
- Include related /pb-* commands that should run first
- Use checklist format for steps
- Reference other commands with `/pb-name`

**Examples**:

```markdown
## Prerequisites

Before running this command:
- [ ] Determine change tier (XS/S/M/L) using `/pb-guide`
- [ ] Create feature branch using `/pb-start`
- [ ] Review standards using `/pb-standards`
```

✅ Good: Clear ordered prerequisites with command references

```markdown
## Pre-Start Checklist

- [ ] Scope is clear
- [ ] Branch created from main using `/pb-start`
- [ ] Context reviewed
```

✅ Good: Checklist format with command reference

### 5. Workflow Section

**Format**: Step-by-step process with command references

**Rules**:
- Use numbered list: `1.`, `2.`, `3.` (shows sequence)
- Include /pb-* references at logical points
- Use action verbs: "Write", "Run", "Review", "Commit"
- Each step should be a complete thought
- Order indicates workflow sequence (important for extraction)

**Examples**:

```markdown
## Development Workflow

1. Write feature code following `/pb-standards`
2. Self-review changes using `/pb-cycle`
3. Run tests and type checking with `make test`
4. Get peer feedback using `/pb-cycle`
5. Create atomic commit using `/pb-commit`
6. Repeat steps 1-5 for each logical change
```

✅ Good: Clear numbered sequence with command references

```markdown
## Workflow

Then you can use `/pb-testing` for testing.
Next, run `/pb-commit` to make a commit.
```

❌ Poor: No numbered sequence, vague order

### 6. Related Commands

**Rules**:
- Include /pb-* references naturally in text
- Every reference is extracted as a related command
- Mention early if it's a "must do", later if "optional"
- Link by putting /pb-name in text

**Examples**:

```markdown
For comprehensive testing, use `/pb-testing`.
After your changes are solid, create a PR using `/pb-pr`.
Most features require `/pb-cycle` for self-review and peer feedback.
```

✅ Good: Natural references with context

```markdown
/pb-cycle /pb-testing /pb-commit
```

❌ Poor: References without context (hard to extract intent)

### 7. Tier Information

**Format**: Explicit tier declarations

**Rules**:
- State if command applies to specific tiers (XS/S/M/L)
- Use format: `Tier: S` or `Tier: [S, M, L]`
- Or include in tier table showing what's required per tier
- Reference `/pb-guide` for tier definitions

**Examples**:

```markdown
## Tiers & Requirements

| Tier | Use This Command | Notes |
|------|------------------|-------|
| XS   | Optional | Skip if trivial |
| S    | Required | Peer review |
| M    | Required | Tech lead review |
| L    | Required | Multiple reviewers |
```

✅ Good: Clear table showing tier applicability

```markdown
Tier: S, M, L (XS can skip if minimal change)
```

✅ Good: Explicit tier ranges

### 8. Decision Context

**Format**: Conditional logic for choosing this command

**Rules**:
- Show "if...then" decision trees
- Use when command competes with alternatives
- Show what makes this command the right choice
- Use clear decision branches

**Examples**:

```markdown
## Choosing the Right Review Command

- **Feature work?** → Use `/pb-cycle` + `/pb-review`
- **Security-critical?** → Also use `/pb-security`
- **Database changes?** → Also use `/pb-patterns-db`
- **Performance-sensitive?** → Also use `/pb-performance`
- **Hotfix?** → Skip to `/pb-release` instead
```

✅ Good: Clear conditional logic

### 9. Section Organization

**Format**: Standard h2 sections

**Rules**:
- Use clear, scannable headings
- Organize in logical order
- Common sections: When to Use, Prerequisites, Workflow, Examples, Troubleshooting, Next Steps
- Keep sections focused

**Examples**:

```markdown
## Quick Reference
## When to Use
## Prerequisites
## Core Workflow
## Step-by-Step Guide
## Examples
## Troubleshooting
## Next Steps
```

✅ Good: Clear, scannable structure

### 10. Examples & Code

**Format**: Concrete examples of usage

**Rules**:
- Include code blocks (```language) to enable has_examples detection
- Show before/after
- Include command examples
- Make examples realistic

**Examples**:

````markdown
## Examples

**Example 1: Starting a feature**
```bash
# Create feature branch
git checkout -b feature/v1.3.0-user-profiles main

# Follow workflow from "Development Workflow" section
```

**Example 2: Starting a bug fix**
```bash
git checkout -b fix/email-validation main
```
````

✅ Good: Concrete, reproducible examples

### 11. Next Steps Section

**Format**: What to do after completing this command

**Rules**:
- Use clear workflow sequence
- Include /pb-* references for next commands
- Show both primary path and alternatives
- Use numbered or bulleted list

**Examples**:

```markdown
## Next Steps

After using `/pb-start`:
1. Follow the development workflow outlined above
2. Use `/pb-cycle` for self and peer review
3. Create PR using `/pb-pr` when ready
4. Merge and deploy using `/pb-release`
```

✅ Good: Clear workflow path with command references

```markdown
## Next Steps

- Depending on your tier, use `/pb-cycle` or skip to `/pb-testing`
- If working on security-critical code, also use `/pb-security`
- Always `/pb-commit` before pushing
```

✅ Good: Conditional next steps with command references

---

## Checklist for Writing Extraction-Friendly Commands

Use this checklist when writing or updating commands:

- [ ] **Title**: Clear, 5-80 chars, starts with action verb
- [ ] **Purpose**: First paragraph, 20-300 chars, complete sentence
- [ ] **When to Use**: Explicit conditions, tier guidance if applicable
- [ ] **Prerequisites**: Clear /pb-* references for required setup
- [ ] **Workflow**: Numbered steps with /pb-* references in logical order
- [ ] **Related Commands**: 3-10 /pb-* references naturally placed
- [ ] **Tier Info**: Explicit (Table, "Tier: X", or tier-specific sections)
- [ ] **Decision Context**: Show when to use this vs alternatives
- [ ] **Examples**: At least one code block or concrete example
- [ ] **Next Steps**: Clear path to next command(s) with references
- [ ] **Sections**: Using ## headings, organized logically
- [ ] **No TODOs**: Remove TODO/FIXME comments

---

## Testing Your Command's Extractability

After writing a command, test it:

1. **Read for clarity**: Does someone new understand when to use it?
2. **Check structure**: Does it follow the template?
3. **Verify references**: Are /pb-* commands properly referenced?
4. **Validate sections**: Are ## headings clear and scannable?
5. **Review purpose**: Is the first paragraph a complete thought?
6. **Test extraction**: Run extraction script and review confidence scores

---

## Common Mistakes to Avoid

❌ **Generic titles**: "Help", "Guide", "Information"
- Instead: "Create Production Release", "Review Code Quality"

❌ **Vague purpose**: "This command does things"
- Instead: "Automate release validation and deployment to production"

❌ **Missing "When to Use"**: No clear conditions
- Instead: "Use when starting feature work", "Do not use for hotfixes"

❌ **Orphaned references**: /pb-xyz mentioned with no context
- Instead: "Use `/pb-cycle` for peer feedback"

❌ **Unordered workflows**: Bullet points when sequence matters
- Instead: Use numbered lists `1.`, `2.`, `3.`

❌ **No examples**: Theory without practice
- Instead: Include at least one concrete code block example

❌ **Missing tier guidance**: No indication of when it applies
- Instead: "Tier: M, L" or "Required for S and above"

---

## Questions for Command Authors

When writing a command, ask:

1. **Who uses this?** (developers, leads, teams)
2. **When do they use it?** (start of feature, per PR, release, etc.)
3. **What comes before?** (prerequisites, related commands)
4. **What's the workflow?** (step-by-step with 3-8 clear steps)
5. **What comes next?** (follow-up commands, continued workflow)
6. **What are alternatives?** (when NOT to use, use something else instead)
7. **Can I show an example?** (concrete, runnable code or steps)
8. **Does tier matter?** (different for XS/S/M/L?)

---

## For Extraction Engine Developers

This guide helps maintainers of extraction scripts understand what commands **should** contain and what patterns to look for:

- **Confidence Boosters**: Structure, tier info, examples, numbered workflows
- **Confidence Detractors**: Vague titles, missing examples, no tier guidance
- **High-Confidence Fields**: Title (100%), command name (100%), category (100%)
- **Medium-Confidence Fields**: Purpose (95%), tier (85%), frequency (75%)
- **Low-Confidence Fields**: Decision context (70%), next_steps ordering (80%)

Extraction confidence can always be improved by making commands follow this guide.

---

*Last Updated: 2026-01-12*
*Used by: scripts/extract-playbook-metadata.py*
