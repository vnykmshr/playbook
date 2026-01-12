You are a senior software engineer preparing for a **production release**.
Perform a final code review and cleanup of the current repository.

**Principle:** Pre-release review is where `/pb-preamble` thinking (challenge readiness assumptions) and `/pb-design-rules` thinking (verify Robustness, verify Clarity) are most critical. Surface risks directly. This is the last gate—don't hide issues.

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
- Rewrite sections into concise, idiomatic Bash/Python/Go (as applicable).
- Ensure naming conventions are consistent and human-readable.
- Remove unnecessary abstractions and keep things as straightforward as possible.

### 4. Telltale Signs to Check
- Overly generic error handling (e.g., “Something went wrong”).
- Repeated boilerplate blocks where a function or loop is better.
- Over-commenting or comments that explain the obvious.
- Long variable names or inconsistent style.
- Copy-pasted patterns from unrelated codebases.

### 5. Final Human Pass
- Readability: Is the code understandable by another engineer at a glance?
- Minimalism: Does every line serve a purpose?
- Maintainability: Would future contributors be able to extend it easily?
- Consistency: Does the repo feel like it was written by one person, not stitched together?

Deliverable:
A **release-ready codebase** that is clean, deduped, minimal, and maintainable, with docs and repo structure polished for production release.
