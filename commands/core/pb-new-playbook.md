# New Playbook

**Purpose:** Meta-playbook for creating new playbook commands. Ensures every new command meets quality standards, follows conventions, and integrates coherently with the existing ecosystem.

**Mindset:** Playbooks should exemplify what they preach. Apply `/pb-preamble` thinking (clear reasoning invites challenge—your playbook should be easy to critique and improve) and `/pb-design-rules` thinking (Clarity, Modularity, Representation: structure should make intent obvious).

Before writing a playbook, understand what type it is. Classification drives structure.

---

## When to Use

- **Creating a new pb-* command** — Before writing any new playbook
- **Restructuring existing playbook** — When refactoring a command
- **Reviewing playbook quality** — As a reference for standards
- **Onboarding contributors** — Teaching playbook conventions

---

## Step 1: Classify Your Playbook

What type of playbook is this? Classification determines required sections.

| Type | Description | Key Characteristic | Examples |
|------|-------------|-------------------|----------|
| **Executor** | Runs a specific workflow | Has steps/process to follow | pb-commit, pb-deployment, pb-start |
| **Orchestrator** | Coordinates multiple commands | References other pb-* commands | pb-release, pb-ship, pb-repo-enhance |
| **Guide** | Provides philosophy/framework | Principles over procedures | pb-guide, pb-preamble, pb-design-rules |
| **Reference** | Pattern library, templates | Lookup material | `pb-patterns-*`, pb-templates |
| **Review** | Evaluates against criteria | Checklists and deliverables | `pb-review-*`, pb-security |

**Decision aid:**
- Does it have steps to execute? → **Executor**
- Does it mainly call other commands? → **Orchestrator**
- Does it explain philosophy/principles? → **Guide**
- Is it lookup/reference material? → **Reference**
- Does it evaluate/audit something? → **Review**

---

## Step 2: Name Your Playbook

### Naming Patterns

| Pattern | Use When | Examples |
|---------|----------|----------|
| `pb-<action>` | Single clear action | pb-commit, pb-ship, pb-deploy |
| `pb-<noun>` | Concept or thing | pb-security, pb-testing |
| `pb-<category>-<target>` | Part of a family | pb-review-code, pb-patterns-api |
| `pb-<noun>-<noun>` | Compound concept | pb-design-rules, pb-knowledge-transfer |

### Naming Rules

- Lowercase only, hyphens between words
- Verb-first for actions (pb-commit, pb-deploy, pb-review)
- Noun-first for concepts (pb-security, pb-patterns)
- Avoid generic names (not pb-do-stuff, pb-misc)
- Match existing family patterns (`pb-review-*` for reviews, `pb-patterns-*` for patterns)

### Category Placement

| Category | Purpose | Examples |
|----------|---------|----------|
| `core/` | Foundation, philosophy, meta | pb-guide, pb-preamble, pb-standards |
| `planning/` | Architecture, patterns, decisions | pb-plan, pb-adr, `pb-patterns-*` |
| `development/` | Daily workflow commands | pb-start, pb-commit, pb-cycle |
| `deployment/` | Release, ops, infrastructure | pb-deployment, pb-release, pb-incident |
| `reviews/` | Quality gates, audits | `pb-review-*`, pb-security |
| `repo/` | Repository management | pb-repo-init, pb-repo-enhance |
| `people/` | Team operations | pb-team, pb-onboarding |
| `templates/` | Context generators | pb-claude-global, pb-context |
| `utilities/` | System maintenance | pb-doctor, pb-storage, pb-ports |

---

## Step 3: Required Sections

### Universal (All Playbooks)

Every playbook must have:

```markdown
# [Title]

**Purpose:** [1-2 sentences: what this does and why it matters]

**Mindset:** Apply /pb-preamble thinking ([specific aspect]) and /pb-design-rules thinking ([relevant rules]).

[1-2 sentence orienting statement]

---

## When to Use

- [Scenario 1]
- [Scenario 2]
- [Scenario 3]

---

[MAIN CONTENT - varies by classification]

---

## Related Commands

- /pb-related-1 — [Brief description]
- /pb-related-2 — [Brief description]

---

**Last Updated:** [Date]
**Version:** X.Y.Z
```

### By Classification

#### Executor (Additional Required)

```markdown
## Process / Steps

### Step 1: [Name]
[What to do]

### Step 2: [Name]
[What to do]

---

## Verification

How to confirm this worked:
- [ ] [Check 1]
- [ ] [Check 2]
```

#### Orchestrator (Additional Required)

```markdown
## Tasks

### 1. [Task Name]
**Reference:** /pb-specific-command

- [What this task accomplishes]
- [Key subtasks]

### 2. [Task Name]
**Reference:** /pb-another-command

---

## Output Checklist

After completion, verify:
- [ ] [Outcome 1]
- [ ] [Outcome 2]
```

#### Guide (Additional Required)

```markdown
## Principles

### Principle 1: [Name]
[Explanation with reasoning]

### Principle 2: [Name]
[Explanation with reasoning]

---

## Guidelines

**Do:**
- [Positive guidance]

**Don't:**
- [Anti-pattern to avoid]

---

## Examples

[Practical examples demonstrating principles]
```

#### Reference (Additional Required)

```markdown
## [Content Type]

### [Category/Item 1]

[Reference content: patterns, templates, etc.]

### [Category/Item 2]

[Reference content]

---

## Usage Examples

[How to apply this reference material]
```

#### Review (Additional Required)

```markdown
## Review Checklist

### [Category 1]
- [ ] [Check item with clear pass/fail criteria]
- [ ] [Check item]

### [Category 2]
- [ ] [Check item]

---

## Deliverables

### [Output 1: e.g., Summary Report]

```template
[Format/structure for this deliverable]
```

### [Output 2: e.g., Findings List]

[Format specification]
```

---

## Step 4: Write Content

### Tone Guidelines

| Do | Don't |
|----|-------|
| Professional, direct | Casual, chatty |
| Concise, specific | Verbose, vague |
| Imperative mood ("Run X") | Passive ("X should be run") |
| State facts | Hedge with "maybe", "might" |

**Banned phrases:**
- "Let's dive in"
- "It's important to note"
- "As you can see"
- "Simply" / "Just" / "Easily"
- "Best practices" (be specific instead)

### Structure Guidelines

| Element | Rule |
|---------|------|
| Title | H1, imperative or noun phrase |
| Major sections | H2, separated by `---` |
| Subsections | H3, no divider needed |
| Lists | Use for 3+ parallel items |
| Tables | Use for structured comparisons |
| Code blocks | Use for commands, examples, templates |
| Checklists | Use `- [ ]` for verification items |

### Cross-References

- Use `/pb-command-name` format in text
- List related commands in dedicated section at end
- Ensure bidirectional links (if A references B, B should reference A)
- Only reference commands that exist

### Examples

Every playbook should include at least one example:

- Make examples practical and realistic
- Show both input and expected output where applicable
- For pattern guidance, show good AND bad examples
- Use real-world scenarios, not "foo/bar" abstractions

---

## Step 5: Scaffold Template

Copy this template and fill in:

```markdown
# [Command Title]

**Purpose:** [What this does and why it matters]

**Mindset:** Apply /pb-preamble thinking ([aspect]) and /pb-design-rules thinking ([rules]).

[Orienting statement]

---

## When to Use

- [Scenario 1]
- [Scenario 2]
- [Scenario 3]

---

## [Main Section 1]

[Content]

---

## [Main Section 2]

[Content]

---

## [Main Section 3]

[Content]

---

## Related Commands

- /pb-related — [Description]

---

**Last Updated:** YYYY-MM-DD
**Version:** 1.0.0
```

---

## Step 6: Validate

Run this checklist before finalizing:

### Structure Validation

- [ ] Title is H1, clear and specific
- [ ] Purpose statement exists and is concise
- [ ] Mindset links to /pb-preamble and /pb-design-rules
- [ ] "When to Use" section exists with 3+ scenarios
- [ ] Major sections separated by `---`
- [ ] Related Commands section at end
- [ ] Version and date in footer

### Content Validation

- [ ] Classification-appropriate sections present
- [ ] At least one practical example
- [ ] No placeholder text ("TBD", "TODO", "[fill in]")
- [ ] No duplicate content from other playbooks
- [ ] Specific and actionable, not vague philosophy
- [ ] Commands/code are tested and work

### Quality Validation

- [ ] Passes markdownlint (no lint errors)
- [ ] No emojis
- [ ] Professional tone throughout
- [ ] No banned phrases
- [ ] Could be understood by someone new to the playbook

### Integration Validation

- [ ] File in correct category folder
- [ ] Filename matches command name (pb-foo.md for /pb-foo)
- [ ] All /pb-* references point to existing commands
- [ ] Added to `docs/command-index.md`
- [ ] At least one other command references this (edit a related command's "Related Commands" section to add back-link)

### Final Test

```bash
# Lint check
markdownlint commands/[category]/pb-new-command.md

# Install and verify
./scripts/install.sh

# Test invocation (in Claude Code)
# /pb-new-command
```

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Vague title | "pb-helper" tells nothing | Be specific: "pb-lint-setup" |
| Missing "When to Use" | Reader doesn't know if relevant | Add 3+ clear scenarios |
| Philosophy dump | 2000 words, no actions | Add concrete steps |
| Duplicate content | Same checklist in 3 playbooks | Extract to one, reference |
| No examples | All abstract | Add realistic examples |
| Orphan command | No Related Commands | Connect to ecosystem |
| Wrong category | Review in development/ | Move to reviews/ |
| Inconsistent structure | Random heading levels | Follow H1/H2/H3 pattern |
| Stale references | Links to deleted commands | Audit before publishing |

---

## Playbook Lifecycle

### Updating Existing Playbooks

When modifying an existing playbook:

1. **Minor updates** (typos, clarifications): Update directly, bump patch version
2. **New sections or features**: Update, bump minor version, note in commit
3. **Breaking changes** (renamed, restructured, different behavior): Bump major version, document migration path

### Deprecating Playbooks

When a playbook is no longer needed:

1. Add deprecation notice at top: `**DEPRECATED:** Use /pb-replacement instead. This command will be removed in vX.Y.`
2. Update referencing commands to point to replacement
3. Remove from `docs/command-index.md` (or mark deprecated)
4. After grace period, delete file and remove symlink

### Version Convention

```
**Version:** MAJOR.MINOR.PATCH

MAJOR: Breaking changes, significant restructure
MINOR: New sections, expanded content
PATCH: Typos, clarifications, minor fixes
```

---

## Example: Creating a New Playbook

**Scenario:** Create a playbook for setting up linting in a project.

### Step 1: Classify
- Runs a workflow with steps → **Executor**

### Step 2: Name
- Action-oriented → `pb-lint-setup`
- Category → `development/` (daily workflow)

### Step 3: Required Sections
- Universal sections (Purpose, When to Use, Related)
- Executor sections (Process/Steps, Verification)

### Step 4: Write

```markdown
# Lint Setup

**Purpose:** Configure linting for consistent code style...

## When to Use
- Starting new project
- Adding linting to existing codebase
- Standardizing team code style

## Process

### Step 1: Choose Linter
[Based on language...]

### Step 2: Install
[Commands...]

### Step 3: Configure
[Config files...]

## Verification
- [ ] Linter runs without errors
- [ ] Pre-commit hook installed

## Related Commands
- /pb-repo-init — Project initialization
```

### Step 5: Validate
- Run checklist
- Test with markdownlint
- Install and invoke

---

## Playbook Quality Tiers

Reference for appropriate depth:

| Tier | Line Count | When to Use |
|------|------------|-------------|
| **Minimal** | 50-100 | Simple, focused commands |
| **Standard** | 100-300 | Most commands |
| **Comprehensive** | 300-600 | Complex workflows, guides |
| **Reference** | 600+ | Pattern libraries, extensive guides |

Match depth to purpose. Simple commands don't need 500 lines.

---

## Related Commands

- `/pb-review-playbook` — Review existing playbooks for quality
- `/pb-templates` — Reusable templates and patterns
- `/pb-standards` — Code quality standards
- `/pb-documentation` — Writing great documentation
- `/pb-design-rules` — Technical principles for clarity and simplicity

---

**Last Updated:** 2026-01-24
**Version:** 1.0.0
