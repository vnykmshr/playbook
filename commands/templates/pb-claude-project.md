---
name: "pb-claude-project"
title: "Generate Project CLAUDE.md"
category: "templates"
difficulty: "beginner"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-claude-global', 'pb-claude-orchestration', 'pb-context', 'pb-onboarding', 'pb-greenfield']
last_reviewed: "2026-09-24"
last_evolved: "2026-09-24"
version: "1.4.0"
version_notes: "v1.4.0: Q3 2026 -- the template stops asking for what the rules forbid. It listed Current version and status under Keep and carried a Status placeholder, so generated files pinned a commit and went stale; per-commit state is now banned and the working context is linked, not copied. The stack-detection tables collapse to one step: record only what a reader would not find in one pass. The skeleton drops Testing, Environment and Session Quick Start (duplicates of Commands) and makes Tech Stack and Structure optional. The BEACON compression claim is deleted -- the root file is re-read after compaction regardless. Maintenance no longer contradicts Step 0. The example shows Custom (Manual), Generated Artifacts and Guardrails, the sections the contract protects. Size gate: under 200 lines, Anthropic's figure. v1.3.0: raise the size gate to 180 lines / 3K tokens (was 150/2K, stated in three places that now agree). The token half bound first at ~145 lines, so the line figure was decorative; both halves now carry weight. v1.2.0: wire the preservation contract that was only ever described. Step 0 reads the file being replaced and inventories `## Custom (Manual)` blocks; the generated structure carries that section; the checklist verifies the blocks survived. Regeneration is now the default path rather than a hazard. v2.10.0 baseline; v1.1.0 collapse duplicate Guardrails, add BEACON marker alignment"
breaking_changes: []
---
# Generate Project CLAUDE.md

Generate a project-specific `.claude/CLAUDE.md` by analyzing the current project structure, tech stack, and patterns.

**Purpose:** Create project-specific context that complements global CLAUDE.md with details relevant to THIS project.

**Philosophy:** Project CLAUDE.md should capture what's unique about this project (tech stack, structure, commands, patterns) so Claude Code understands the project context across sessions.

**Context efficiency:** This file is loaded into every session. Keep it **under 200 lines** -- Anthropic's published target; longer files consume more context and reduce adherence. Move reference material to `docs/` and link it.

**Mindset:** Design Rules emphasize "clarity over cleverness" - generated context should be immediately useful, not comprehensive.

**Resource Hint:** sonnet - project analysis and template generation from existing structure.

---

## When to Use

- Setting up a new project for Claude Code workflow
- After major project restructuring
- When onboarding to an existing project
- Periodically to refresh project context as it evolves

---

## Analysis Process

### Step 0: Read the File You Are About to Replace

Regeneration overwrites. Before analyzing anything, read the existing `.claude/CLAUDE.md` if there is one, and inventory what must survive.

```bash
grep -n '^## ' .claude/CLAUDE.md 2>/dev/null
```

**The contract, in one line:** this command owns the structural sections; the author owns every `## Custom (Manual)` block, and those are carried across verbatim.

Copy each `## Custom (Manual)` block out before you write, and paste it back into the generated file unchanged. Do not paraphrase, reorder, or "improve" it -- it is there because analysis could not derive it.

**If the existing file has hand-written content that is *not* under that marker**, stop and resolve it before regenerating. Three outcomes, in order of preference:

1. It is derivable from the project -- let generation reproduce it, and drop the hand-written copy.
2. It is knowledge analysis cannot reach (tribal conventions, gotchas, a rule that lives in someone's head) -- move it under `## Custom (Manual)` first, then regenerate.
3. It is reference material rather than per-turn context -- move it to `docs/` and link it. The line budget below is the forcing function.

A file that cannot survive its own generator is a defect in one of them. Resolve which, rather than hand-editing forever.

### Step 1: Read the Project

Read the manifests, build files, CI config, README and CONTRIBUTING. The model generating this file can find the stack and the layout in one pass, and so can the model that will read it -- so record only what that reader would **not** find in one pass or would get wrong:

- The commands that actually work (build, test, lint, run), verified by running them
- Paths that are generated output and must never be edited or committed
- Conventions, couplings and gotchas: files that change together, ordering rules, what a green CI run does *not* prove
- Guardrails: what needs the owner's approval before it is touched

Stack and structure earn a line only where the manifests mislead -- a vendored fork, a monorepo whose root manifest is not the build, a directory whose name lies about its contents.

### Step 2: Point at State, Do Not Copy It

If a working context exists (`todos/*working-context*.md`), link it from the generated file. Do not copy its version, commit, counts or status into this file: state changes every commit, this file is loaded every session, and a stale claim here is read as fact until someone regenerates. The working context is refreshed by `/pb-context`; this command does not touch it.

---

## Generate CLAUDE.md

Create `.claude/CLAUDE.md` with this structure. Every section is optional except Commands; delete what the project does not need.

```markdown
# [Project Name] Development Context

> Generated: YYYY-MM-DD · Global guidelines: ~/.claude/CLAUDE.md
> Current state: `todos/1-working-context.md` (if the project keeps one)

[One or two lines: what this project is, and anything about it a reader would get wrong from the README.]

---

## Commands

```bash
[command]           # Run tests
[command]           # Lint/format
[command]           # Build / run
```

[Only non-obvious notes: a command that must run before another, one that is slow, one whose green result proves less than it looks.]

---

## Generated Artifacts (do not commit)

[Paths that are build or generated output, never source. Delete this section if none.]

---

## Relevant Playbooks

| Command | Relevance |
|---------|-----------|
| `/pb-guide-[lang]` | Language-specific SDLC |
| `/pb-patterns-[type]` | Applicable patterns |

---

## BEACON: Project Guardrails

- **Dependency lock** - No new dependencies without approval
- **Infrastructure lock** - No Docker/DB/environment changes without approval
- **Data safety** - No database deletions without explicit approval
[Customize; remove what does not apply.]

---

## Custom (Manual)

[Preserved verbatim on regeneration. Everything analysis cannot derive belongs here:
project conventions, known gotchas, files that must be touched together, decisions whose
rationale lives nowhere else. Carried across from Step 0 -- never rewritten.]

---

## Overrides from Global

[Each intentional deviation from ~/.claude/CLAUDE.md, named. Delete if none.]
- **Commit scope:** This project uses `module:` prefix instead of `feat:`

---

*Regenerate with `/pb-claude-project` when project structure changes significantly.*
```

The `BEACON:` prefix is a reader's marker for load-bearing sections, matching the global file. It has no mechanical effect: the root CLAUDE.md is re-read from disk after compaction whatever its headings say.

---

## Conciseness Guidelines

**Target: under 200 lines.** The test for every line is the global file's derive-or-decide test: would the model reading this file find it in the repo in one pass, or do it by default? Then it is a passenger.

**Keep:** commands that work, generated paths, guardrails, conventions and couplings, overrides.

**Never:** anything that changes per commit -- version, SHA, test count, status. It goes stale in a file loaded every session, and a stale fact here is read as current. Link the working context instead.

**Move to `docs/`:** API reference, architecture explanations, full environment variable lists, extended examples, history.

```markdown
# Before
## Environment Variables
The following environment variables are required for the application to function...
[20 lines]

# After
See `.env.example`. Critical: `DATABASE_URL`, `API_KEY`, `JWT_SECRET`
```

---

## Output Location

Write to: `.claude/CLAUDE.md` in project root

```bash
mkdir -p .claude
# Write generated content to .claude/CLAUDE.md
```

If file exists, back it up and diff afterwards -- the backup is worthless if nobody compares:

```bash
cp .claude/CLAUDE.md .claude/CLAUDE.md.backup
# ... generate ...
diff .claude/CLAUDE.md.backup .claude/CLAUDE.md
```

Read the diff for content that vanished rather than changed. Anything lost that was not
derivable belonged under `## Custom (Manual)` and did not get there -- fix that, not the
output. Delete the backup once the diff is clean.

---

## Verification Checklist

- [ ] **Under 200 lines**
- [ ] Every command listed was run and works
- [ ] No per-commit state (version, SHA, counts, status) in the file
- [ ] Every line passes derive-or-decide
- [ ] **Every `## Custom (Manual)` block from Step 0 is present, verbatim** -- diff against the backup and confirm nothing vanished
- [ ] No hand-written content survives *outside* that marker; if any does, it was resolved via Step 0's three outcomes rather than left to erode

---

## Customization

Hand-written content goes under `## Custom (Manual)` -- the section in the generated
structure above, inventoried by Step 0 and verified by the checklist. That is the whole
mechanism; there is nowhere else that survives a regeneration.

What belongs there:

- **Team conventions** specific to this project
- **Known gotchas** or quirks
- **Files that must be touched together** and other tribal ordering rules
- **Architecture decisions** not captured elsewhere
- **Integration details** (external services, APIs)

What does not: anything analysis can derive (stack, structure, commands, CI) -- let
generation own it, so it updates itself. And anything a reader consults rather than needs
every turn -- that goes to `docs/` and gets linked.

---

## Maintenance

**Regenerate** after a structural change: new tooling, a moved build, a new generated path. Minor changes go under `## Custom (Manual)` or wait for the next regeneration -- a hand edit outside that marker is overwritten by the next run.

---

## Integration with Global

Project CLAUDE.md complements global:

```
~/.claude/CLAUDE.md          → Universal principles (commits, PRs, design rules)
.claude/CLAUDE.md            → Project specifics (stack, commands, structure)
```

**Precedence:** Project-specific guidelines override global when they conflict.

**Example override:**
```markdown
## Overrides from Global

- **Commits:** This project uses `[JIRA-123]` prefix for all commits
- **Testing:** Skip E2E tests locally; CI handles them
```

---

## Related Commands

- `/pb-claude-global` - Generate/update global CLAUDE.md
- `/pb-claude-orchestration` - Model selection and resource efficiency guide
- `/pb-context` - Project working context template
- `/pb-onboarding` - New developer onboarding
- `/pb-greenfield` - New project from an idea (hands off to this command for the project CLAUDE.md)

---

## Example: Python FastAPI Project

```markdown
# UserService Development Context

> Generated: 2026-01-13 · Global guidelines: ~/.claude/CLAUDE.md

FastAPI service for user accounts. Async throughout; the sync SQLAlchemy session in `app/legacy/` is the exception, not a pattern.

---

## Commands

```bash
make dev            # Start with hot reload
make test           # pytest -- needs `docker compose up db` first
make lint           # ruff + mypy
make migrate        # alembic upgrade head
```

---

## Generated Artifacts (do not commit)

- `alembic/versions/*_autogen.py` -- review, rename, then commit; never commit raw
- `openapi.json` -- built by `make docs`

---

## BEACON: Project Guardrails

- **Migration lock** - No schema change without a reviewed migration
- **Dependency lock** - No new dependencies without approval

---

## Custom (Manual)

- `app/models/` and `alembic/versions/` change together; a model edit without a migration passes tests and fails deploy
- Rate limits live in `config/limits.toml`, not in code

---

## Relevant Playbooks

| Command | Relevance |
|---------|-----------|
| `/pb-guide-python` | Python SDLC patterns |
| `/pb-patterns-db` | Database patterns |
```

---

*This command generates project-specific Claude Code context through systematic analysis.*
