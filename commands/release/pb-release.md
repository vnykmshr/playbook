Lets prepare and make prod release. We will perform pre-release checks, and release code review by a software engineer (instruction follows below), identiy and address gaps, fix issues, ensure ci is success. Review and add crisp updates to project readme, documents under docs/ (only relevant sections updated, created, while ensuring the document itself is structurally is in correct and natural order. Update charts and diagrams, if relevant updates present). Finally we deploy to prod. Run by engineering playbook as applicable.

**Preparation mindset:** This is where `/pb-preamble` thinking (challenge readiness assumptions, surface risks) and `/pb-design-rules` thinking (verify Robustness, verify Clarity, verify systems fail loudly) become critical.

Don't hide issues to seem "ready." Surface risks directly. Systems should fail loudly, not silently.

You are a senior software engineer preparing for a **production release**.
Perform a final code review and cleanup of the current repository.

Focus on the following:

### 1. Release Checklist
- Confirm repo structure matches best practices (scripts, configs, docs).
- Ensure versioning and tagging are consistent (v1.0.0).
- Validate documentation accuracy (README, usage, troubleshooting).
- Confirm implementation embodies the mission outlined in project readme.
- Verify licensing, contributing guidelines, and changelog are present.

### 2. Code Review & Cleanup
- Remove duplication across scripts (dedupe functions, configs).
- Consolidate constants, paths, and configuration variables into a single source.
- Strip unused code, comments, or placeholders left from earlier iterations.
- Simplify overly complex logic into clear, maintainable patterns.
- Don't remove todos/ directory, its dev-only and git-ignored.

### 3. Reduce AI-Assisted Bloat
- Look for auto-generated or AI-patterned code that feels verbose, redundant, or unnatural.
- Rewrite sections into concise, idiomatic Bash/Python/Go/TypeScript (as applicable).
- Ensure naming conventions are consistent and human-readable.
- Remove unnecessary abstractions and keep things as straightforward as possible.

### 4. Telltale Signs to Check
- Overly generic error handling (e.g., "Something went wrong").
- Repeated boilerplate blocks where a function or loop is better.
- Over-commenting or comments that explain the obvious.
- Long variable names or inconsistent style.
- Copy-pasted patterns from unrelated codebases.

### 5. Security & Performance
- No secrets, credentials, or API keys in code (use environment variables).
- Input validation at system boundaries (user input, external APIs).
- SQL queries parameterized (no string concatenation).
- Rate limiting on public endpoints.
- Database queries optimized (N+1 queries, missing indexes).
- Caching strategy reviewed (TTLs appropriate, invalidation correct).

### 6. Testing & CI
- All tests passing locally and in CI.
- Critical paths have test coverage.
- Flaky tests identified and fixed or quarantined.
- CI pipeline runs lint, typecheck, tests, security scan.

### 7. Stack-Specific Checks

**Backend (Python/FastAPI):**
- Type hints on public functions.
- Async endpoints don't block the event loop.
- Database migrations are reversible.
- Background tasks properly queued.

**Frontend (React/TypeScript):**
- No TypeScript `any` without justification.
- Components follow design system (refer to docs/design.md if present).
- State management consolidated (no duplicate stores for same data).
- Accessibility basics: focus states, ARIA labels, keyboard navigation.

**Infrastructure:**
- Docker images use specific versions, not `latest`.
- Health checks configured for all services.
- Rollback plan documented and tested.

### 8. Final Human Pass
- Readability: Is the code understandable by another engineer at a glance?
- Minimalism: Does every line serve a purpose?
- Maintainability: Would future contributors be able to extend it easily?
- Consistency: Does the repo feel like it was written by one person, not stitched together?

Deliverable:
A **release-ready codebase** that is clean, deduped, minimal, and maintainable, with docs and repo structure polished for production release.
