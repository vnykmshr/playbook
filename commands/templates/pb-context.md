---
name: "pb-context"
title: "[Project Name] Working Context"
category: "templates"
difficulty: "beginner"
model_hint: "haiku"
execution_pattern: "sequential"
related_commands: ['pb-claude-project', 'pb-start', 'pb-resume', 'pb-onboarding']
tags: ['design', 'testing', 'security', 'workflow', 'review']
last_reviewed: "2026-02-09"
last_evolved: ""
---
# [Project Name] Working Context

> **Purpose:** Onboarding context for new developers and session refresh for ongoing work.
> **Current Version:** vX.Y.Z | **Last Updated:** YYYY-MM-DD
>
> **Mindset:** This context assumes both `/pb-preamble` and `/pb-design-rules` thinking.
>
> New developers should: (1) Challenge stated assumptions, question the architecture, surface issues; (2) Understand design principles guiding the system (Clarity, Simplicity, Modularity, Robustness).
>
> **Related Docs:** `pb-guide` (SDLC tiers, gates, checklists) | `pb-standards` (coding standards, conventions) | `pb-design-rules` (technical design principles)

**Resource Hint:** sonnet — project analysis and context generation require balanced judgment.

---

## Working Context Guidelines

**Location:** `todos/` directory (gitignored, not tracked in repo)

**Common filenames:** `working-context.md`, `1-working-context.md`

**When to use this command:**
- Starting a new session (run `/pb-context` to review and update)
- After completing a release (update version, release history)
- Onboarding to a project (read existing context, then update if stale)
- Resuming work after a break (verify context is current)

**Currency check:** Before using this context, verify it's up to date:
```bash
git describe --tags                    # Compare to version in header
git log --oneline -5                   # Compare to recent commits section
```

If the working context is stale (version mismatch, outdated commits), update it before proceeding.

**Integration with other playbooks:**
- `/pb-claude-project` — Checks for working context during CLAUDE.md generation
- `/pb-start` — Should review working context before starting work
- `/pb-resume` — Should check and update working context when resuming

---

## What is [Project Name]

[One-line description of what the project does]

**Key User Journeys:**
1. **[Journey 1]** — [Brief description]
2. **[Journey 2]** — [Brief description]

**Philosophy:** [Core principles, e.g., "Mobile-first, Offline-capable, Privacy-focused"]

**Live:** [Production URL] | **Docs:** [Documentation URL]

---

## Architecture

```
[Simple ASCII diagram showing how components connect]

Example:
Frontend (React) → Backend (FastAPI) → Database (PostgreSQL)
                         ↓
                   External Services
```

**Services:** [List key services/containers]

---

## Tech Stack

| Layer | Tech |
|-------|------|
| Frontend | [e.g., React, TypeScript, Vite, Tailwind] |
| Backend | [e.g., FastAPI, Python, SQLAlchemy] |
| Database | [e.g., PostgreSQL, Redis] |
| Testing | [e.g., Vitest, pytest] |
| Analytics | [e.g., Umami, Mixpanel] |
| CI/CD | [e.g., GitHub Actions] |

---

## Getting Started

**Prerequisites:** [e.g., Docker, Node 20+, Python 3.11+]

**Setup:**
```bash
cp .env.example .env      # Copy template, add your secrets
make dev                  # Start all services
```

> `.env.local` contains prod deploy host info. `.env` is gitignored and holds local secrets.

**Common Commands:**
```bash
make dev                  # Start development environment
make test                 # Run all tests
make lint                 # Lint check
make logs                 # View all service logs
make db-shell             # Database shell
make db-migrate           # Run migrations
```

**Secrets Management:**
```bash
make secrets              # Decrypt .env for production
```

**Deployment:**
```bash
make deploy               # Push, rebuild, health check on server
make rollback             # Restore previous images
```

> **Guideline:** Always prefer `make` targets over direct commands. Make targets ensure repeatable patterns, correct environment setup, and consistent behavior across dev/CI/prod. Run `make help` to see all available targets.

**After setup:**
- Frontend: http://localhost:[PORT]
- Backend API: http://localhost:[PORT]/api/docs
- [Any additional setup steps, e.g., pulling ML models, seeding data]

---

## Development Workflow (SDLC)

**Philosophy:** Stay committed to full SDLC flow — no shortcuts. Strive for bug-free, quality releases.

> **Work Tiers:** S (small, <2h) | M (medium, phased) | L (large, multi-week). See `pb-guide` for tier definitions, gates, and checklists.

### 1. Planning
- Define focus area and scope
- Prepare phase-wise breakdown for M/L tier work
- Document in `todos/releases/vX.Y.Z/00-master-tracker.md` for tracked releases
- Lock scope before development begins

### 2. Development
- Create feature branch: `feature/vX.Y.Z-short-description` (e.g., `feature/v1.2.0-auth`)
- For fixes: `fix/short-description` (e.g., `fix/login-redirect`)
- Proceed incrementally with logical, atomic commits
- Follow conventional commits: `feat:`, `fix:`, `perf:`, `chore:`, `docs:`, `test:`
- Keep PRs focused — one concern per PR

### 3. Quality Checks (before every commit)
```bash
make lint                 # Lint check
make typecheck            # Type check
make format               # Format code
make test                 # Run all tests
```

### 4. Self Review
- Review your own diff before pushing
- Check for: dead code, debug logs, hardcoded values, missing error handling
- Verify tests cover the change

### 5. Create PR
- Push feature branch, create PR to `main`
- Write clear PR description (what, why, how to test)
- CI runs: lint, typecheck, tests, security scan
- Ensure all checks green before requesting review

### 6. Peer Review
- Senior engineer reviews for: correctness, edge cases, security, performance
- Address feedback — fix gaps/issues identified
- Iterate until approved
- Merge strategy: **squash merge** to keep main history clean

### 7. Pre-Release Checks
- Bump version in `package.json` / `pyproject.toml`
- Update `CHANGELOG.md` with release notes
- Verify all tests pass, lint clean
- Update relevant docs if needed

### 8. Release & Deploy
```bash
# After PR merged to main
git tag -a vX.Y.Z -m "vX.Y.Z - Brief description"
git push origin vX.Y.Z
gh release create vX.Y.Z --title "vX.Y.Z - Title" --notes "..."
make deploy               # Deploy to production
```

### 9. Post-Deploy Verification
- Verify prod health: `curl .../api/health`
- Smoke test critical flows
- Monitor for errors (logs, dashboards)
- For performance releases: verify metrics improved

### Periodic Maintenance
- **Hygiene releases** — Periodic code cleanup, test organization, dependency updates
- **Periodic reviews** — Use `/pb-review-*` commands for structured codebase reviews
- **Performance audits** — Regular performance scans to catch regressions

> **No shortcuts.** Every release follows this flow. Quality over speed.

---

## Key Directory Structure

```
backend/
├── api/           # API routes/endpoints
├── services/      # Business logic
├── models/        # Database models
├── utils/         # Shared utilities
├── config/        # Configuration files
└── tests/         # pytest tests (mirrors source structure)

frontend/src/
├── pages/         # Page components
├── components/    # Reusable components
├── hooks/         # Custom React hooks
├── lib/           # Utilities, API client, helpers
├── contexts/      # React contexts
└── styles/        # CSS, tokens, themes

# Tests: co-located *.test.ts files next to source files
```

---

## Core Features

### [Feature Area 1]
- [Key capability]
- [Key capability]

### [Feature Area 2]
- [Key capability]
- [Key capability]

### [Feature Area 3]
- [Key capability]
- [Key capability]

---

## API Quick Reference

| Category | Key Endpoints |
|----------|---------------|
| [Resource 1] | `GET /resource`, `POST /resource`, `PUT /resource/{id}` |
| [Resource 2] | `GET /resource`, `POST /resource` |
| Auth | `POST /signup`, `POST /login`, `POST /logout` |
| Health | `GET /health`, `GET /status` |

Base: `/api/v1/`

---

## Database Models

```
[Primary Entity] (field1, field2, field3)
  ├── [Related Entity] (field1, field2)
  └── [Related Entity] (field1, field2)

[Another Entity] (field1, field2, field3)
```

**Key Status Flows:** `[status1] → [status2] → [status3]`

---

## Operations

**Server:** [Server location/provider]

**Crons:**
- [Scheduled job description and timing]
- [Scheduled job description and timing]

**Monitoring:** [Monitoring tools and dashboards]

**Performance:** `make perf-report` runs [performance tool]

---

## Key Patterns

| Pattern | Implementation |
|---------|----------------|
| Error handling | [How errors are handled] |
| Authentication | [Auth strategy] |
| Caching | [Caching approach] |
| Rate limiting | [Rate limit rules] |
| Logging | [Logging strategy] |
| Feature flags | [Feature flag system if any] |

---

## Release History

| Version | Date | Highlights |
|---------|------|------------|
| vX.Y.Z | YYYY-MM-DD | [Brief description] |
| vX.Y.Z | YYYY-MM-DD | [Brief description] |
| vX.Y.Z | YYYY-MM-DD | [Brief description] |

---

## Session Checklist

```bash
git describe --tags                    # Current version
gh run list --limit 1                  # CI status
curl -s [PROD_URL]/api/health | jq     # Prod health
git log --oneline -10                  # Recent commits
```

---

## Related Commands

- `/pb-claude-project` — Generate project CLAUDE.md
- `/pb-start` — Begin development work
- `/pb-resume` — Resume after break
- `/pb-onboarding` — New team member integration

---

*Update when making significant changes.*
