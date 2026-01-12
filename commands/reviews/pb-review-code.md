# Periodic Repository Review Prompt

You are a senior software engineer performing a **periodic repository review** before starting a fresh round of development.
The goal is to ensure the project remains clean, consistent, and maintainable over time.

**Mindset:** This review embodies `/pb-preamble` thinking. Challenge architectural choices. Point out duplication and complexity. Surface flaws directly. This is how you maintain code quality over time.

---

## 1. Repository Health Check
- Verify repo structure aligns with best practices (scripts, configs, docs clearly separated).
- Confirm versioning, tags, and branches are clear and consistent.
- Validate documentation accuracy (README, usage, setup, troubleshooting).
- Ensure project goals and direction in the README are still reflected in the implementation.
- Check for presence and relevance of licensing, contributing guidelines, and changelog.

---

## 2. Code Review & Cleanup
- Remove duplication across scripts or modules (dedupe functions, configs).
- Consolidate constants, paths, and config variables into a single source of truth.
- Strip unused code, comments, or placeholders left from prior iterations.
- Refactor overly complex logic into simple, maintainable patterns.
- Preserve `todos/` directory (dev-only and git-ignored).

---

## 3. Reduce AI-Assisted or Boilerplate Bloat
- Identify code that looks verbose, redundant, or unnaturally generated.
- Rewrite into concise, idiomatic Bash/Python/Go (as applicable).
- Enforce consistent, human-readable naming conventions.
- Remove unnecessary abstractions, favoring straightforward solutions.

---

## 4. Telltale Signs to Catch
- Generic error handling that hides useful context.
- Repeated boilerplate where a function or loop is better.
- Over-commenting or comments that state the obvious.
- Long or inconsistent variable names.
- Copy-paste leftovers from unrelated projects.

---

## 5. Human-Level Sanity Check
- **Readability**: Can another engineer grasp intent at a glance?
- **Minimalism**: Does each line have a purpose?
- **Maintainability**: Can future contributors extend it easily?
- **Consistency**: Does the repo feel like it was written by one person?

---

### Deliverable
A repository that is **clean, consistent, and ready for the next wave of development** — not release prep, but ensuring a solid foundation to build on.
