# Generate Project CLAUDE.md

Generate a project-specific `.claude/CLAUDE.md` by analyzing the current project structure, tech stack, and patterns.

**Purpose:** Create project-specific context that complements global CLAUDE.md with details relevant to THIS project.

**Philosophy:** Project CLAUDE.md should capture what's unique about this project—tech stack, structure, commands, patterns—so Claude Code understands the project context across sessions.

**Context efficiency:** This file is loaded every conversation turn. Keep it **under 2K tokens** (~150 lines). Move detailed documentation to `docs/` and reference it.

**Mindset:** Design Rules emphasize "clarity over cleverness" — generated context should be immediately useful, not comprehensive.

**Resource Hint:** sonnet — project analysis and template generation from existing structure.

---

## When to Use

- Setting up a new project for Claude Code workflow
- After major project restructuring
- When onboarding to an existing project
- Periodically to refresh project context as it evolves

---

## Analysis Process

### Step 1: Detect Tech Stack

Check for these files to identify language and framework:

| File | Indicates |
|------|-----------|
| `package.json` | Node.js/JavaScript/TypeScript |
| `pyproject.toml` or `requirements.txt` | Python |
| `go.mod` | Go |
| `Cargo.toml` | Rust |
| `pom.xml` or `build.gradle` | Java |
| `Gemfile` | Ruby |
| `composer.json` | PHP |

**Read the file** to extract:
- Project name
- Version
- Key dependencies (framework, testing, etc.)
- Scripts/commands

### Step 2: Identify Framework

From dependencies, identify the framework:

| Dependency | Framework |
|------------|-----------|
| `fastapi`, `flask`, `django` | Python web |
| `express`, `fastify`, `nestjs` | Node.js web |
| `gin`, `echo`, `fiber` | Go web |
| `react`, `vue`, `angular` | Frontend |
| `sqlalchemy`, `prisma`, `gorm` | ORM |

### Step 3: Map Directory Structure

List top-level directories and identify patterns:

```bash
ls -la
```

Common patterns to recognize:
- `src/` or `lib/` — Source code
- `tests/` or `test/` or `__tests__/` — Tests
- `docs/` — Documentation
- `scripts/` — Automation scripts
- `config/` or `conf/` — Configuration
- `api/` or `routes/` — API endpoints
- `models/` — Data models
- `services/` — Business logic
- `utils/` or `helpers/` — Utilities

### Step 4: Analyze Testing Patterns

Find test files and understand patterns:

```bash
find . -name "*test*" -o -name "*spec*" | head -20
```

Read one representative test file to understand:
- Test framework (pytest, jest, go test, etc.)
- Test structure (describe/it, test functions, table-driven)
- Mocking patterns
- Assertion style

### Step 5: Identify Build/Run Commands

Check these sources for commands:

| Source | Commands |
|--------|----------|
| `Makefile` | `make <target>` |
| `package.json` scripts | `npm run <script>` |
| `pyproject.toml` scripts | `poetry run <script>` |
| `docker-compose.yml` | `docker-compose up` |
| `README.md` | Setup/run instructions |

### Step 6: Check for Existing Context

Look for existing documentation:
- `README.md` — Project overview
- `CONTRIBUTING.md` — Contribution guidelines
- `docs/` — Additional documentation
- `.env.example` — Environment variables needed

**Working Context Discovery:**
Check for working context documents that provide rich project state:

```bash
ls todos/*working-context*.md 2>/dev/null
```

Common locations: `todos/working-context.md`, `todos/1-working-context.md`

If a working context exists:
1. **Read it first** — It contains current version, active development context, and session checklists
2. **Check currency** — Compare version/date with git tags and recent commits
3. **Update if stale** — If working context is outdated, update it as part of generation
4. **Extract key info** — Use it to populate Tech Stack, Commands, and Active Development sections

### Step 7: Detect CI/CD

Check for CI configuration:
- `.github/workflows/` — GitHub Actions
- `.gitlab-ci.yml` — GitLab CI
- `Jenkinsfile` — Jenkins
- `.circleci/` — CircleCI

---

## Generate CLAUDE.md

Create `.claude/CLAUDE.md` with this structure:

```markdown
# [Project Name] Development Context

> Generated: YYYY-MM-DD
> Tech Stack: [Language] + [Framework]
>
> This file provides project-specific context for Claude Code.
> Global guidelines: ~/.claude/CLAUDE.md

---

## Project Overview

[One-line description from README or package.json]

**Repository:** [URL if available]
**Status:** [Active development / Maintenance / etc.]

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Language | [e.g., Python 3.11] |
| Framework | [e.g., FastAPI] |
| Database | [e.g., PostgreSQL] |
| ORM | [e.g., SQLAlchemy] |
| Testing | [e.g., pytest] |
| CI/CD | [e.g., GitHub Actions] |

---

## Project Structure

```
[project-name]/
├── [dir]/          # [Description]
├── [dir]/          # [Description]
├── [dir]/          # [Description]
└── [file]          # [Description]
```

**Key locations:**
- Source code: `[path]`
- Tests: `[path]`
- Configuration: `[path]`
- Documentation: `[path]`

---

## Commands

**Development:**
```bash
[command]           # Start development server
[command]           # Run tests
[command]           # Lint/format code
```

**Build & Deploy:**
```bash
[command]           # Build for production
[command]           # Deploy
```

---

## Testing

**Framework:** [pytest/jest/go test/etc.]

**Run tests:**
```bash
[command]
```

**Test patterns:**
- [Describe test organization]
- [Describe mocking approach]
- [Coverage expectations]

---

## Environment

**Required variables:**
```bash
[VAR_NAME]          # [Description]
[VAR_NAME]          # [Description]
```

**Setup:**
```bash
cp .env.example .env
# Edit .env with your values
```

---

## Relevant Playbooks

Based on this project's tech stack:

| Command | Relevance |
|---------|-----------|
| `/pb-guide-[lang]` | Language-specific SDLC |
| `/pb-patterns-[type]` | Applicable patterns |
| `/pb-testing` | Testing guidance |
| `/pb-security` | Security checklist |

---

## Guardrails

[Project-specific safety constraints — customize as needed]

- **Infrastructure** — [Lock level: strict/moderate/flexible]
- **Dependencies** — [Approval required: yes/no]
- **Ports** — [List fixed ports if any]
- **Data** — [Database modification rules]

---

## Project Guardrails

Project-specific safety constraints (supplement global guardrails):

```markdown
## Guardrails

- **Infrastructure lock** — No Docker/DB/environment changes without approval
- **Dependency lock** — No new dependencies without approval
- **Port lock** — Backend: [port], Frontend: [port] — do not change
- **Design system** — Follow existing UI patterns in [path]
- **Data safety** — No database deletions without explicit approval
```

Customize based on project needs. Remove irrelevant constraints.

---

## Project-Specific Guidelines

### [Area 1]
[Any project-specific conventions or overrides]

### [Area 2]
[Any project-specific conventions or overrides]

---

## Overrides from Global

[Document any intentional deviations from global CLAUDE.md]

Example:
- **Commit scope:** This project uses `module:` prefix instead of `feat:`
- **Test coverage:** This project requires 90% coverage (vs global 80%)

---

## Session Quick Start

```bash
# Get oriented
git status
[command to run tests]

# Start development
[command to start dev server]
```

---

*Regenerate with `/pb-claude-project` when project structure changes significantly.*
```

---

## Conciseness Guidelines

**Target: Under 2K tokens (~150 lines)**

Project CLAUDE.md is loaded every turn. Large files consume context that could be used for actual work.

**Keep in CLAUDE.md:**
- Tech stack table (essential)
- Key commands (daily use)
- Project structure (high-level only)
- Current version and status
- Critical patterns unique to this project

**Move to docs/:**
- Full API reference
- Detailed architecture explanations
- All environment variables (keep only critical ones)
- Extended examples
- Historical context

**Trim aggressively:**
- Remove sections that duplicate global CLAUDE.md
- Collapse verbose explanations to one-liners
- Use tables over prose
- Reference playbooks instead of repeating their content

**Example trimming:**
```markdown
# Before (verbose)
## Environment Variables
The following environment variables are required for the application to function...
DATABASE_URL - The PostgreSQL connection string...
[20 more lines]

# After (concise)
## Environment
See `.env.example`. Critical: `DATABASE_URL`, `API_KEY`, `JWT_SECRET`
```

---

## Output Location

Write to: `.claude/CLAUDE.md` in project root

```bash
mkdir -p .claude
# Write generated content to .claude/CLAUDE.md
```

If file exists, back it up:
```bash
cp .claude/CLAUDE.md .claude/CLAUDE.md.backup
```

---

## Verification Checklist

After generation, verify:

- [ ] `.claude/CLAUDE.md` exists in project root
- [ ] **File is under 150 lines / 2K tokens** (critical for context efficiency)
- [ ] Tech stack is correctly identified
- [ ] Key commands are accurate and work
- [ ] Directory structure matches reality (high-level only)
- [ ] Test commands run successfully
- [ ] Relevant playbooks are appropriate for this stack
- [ ] Working context (if exists) is current and referenced
- [ ] Detailed docs moved to `docs/`, not duplicated in CLAUDE.md

---

## Customization

After generation, manually add:

- **Team conventions** specific to this project
- **Known gotchas** or quirks
- **Architecture decisions** not captured elsewhere
- **Integration details** (external services, APIs)

Mark manual sections:
```markdown
## Custom (Manual)
[Preserved on regeneration]
```

---

## Maintenance

**When to regenerate:**
- After major refactoring
- When adding new major dependencies
- When changing build/test tooling
- Quarterly refresh

**Working context maintenance:**
If the project has a working context document (typically in `todos/`):
- Check if it's current before regenerating CLAUDE.md
- Update working context if version/date is stale
- Use `/pb-context` command to refresh working context

**Partial updates:**
For minor changes, edit the file directly rather than full regeneration.

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

- `/pb-claude-global` — Generate/update global CLAUDE.md
- `/pb-claude-orchestration` — Model selection and resource efficiency guide
- `/pb-context` — Project working context template
- `/pb-onboarding` — New developer onboarding
- `/pb-repo-init` — Initialize new project structure

---

## Example: Python FastAPI Project

After analyzing a Python FastAPI project, generated CLAUDE.md might look like:

```markdown
# UserService Development Context

> Generated: 2026-01-13
> Tech Stack: Python 3.11 + FastAPI

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.11 |
| Framework | FastAPI 0.109 |
| Database | PostgreSQL 15 |
| ORM | SQLAlchemy 2.0 |
| Testing | pytest + httpx |
| CI/CD | GitHub Actions |

---

## Project Structure

```
userservice/
├── app/
│   ├── api/        # Route handlers
│   ├── models/     # SQLAlchemy models
│   ├── services/   # Business logic
│   └── main.py     # Application entry
├── tests/          # pytest tests
├── alembic/        # Database migrations
└── docker-compose.yml
```

---

## Commands

```bash
make dev            # Start with hot reload
make test           # Run pytest
make lint           # Run ruff + mypy
make migrate        # Run alembic migrations
```

---

## Relevant Playbooks

| Command | Relevance |
|---------|-----------|
| `/pb-guide-python` | Python SDLC patterns |
| `/pb-patterns-db` | Database patterns |
| `/pb-patterns-async` | Async patterns (FastAPI is async) |

---
```

---

*This command generates project-specific Claude Code context through systematic analysis.*
