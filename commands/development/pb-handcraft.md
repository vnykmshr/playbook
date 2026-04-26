---
name: "pb-handcraft"
title: "AI Output Quality Gate"
category: "development"
difficulty: "intermediate"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-voice', 'pb-review', 'pb-linus-agent', 'pb-commit']
last_reviewed: "2026-04-26"
last_evolved: "2026-04-26"
version: "1.2.0"
version_notes: "v1.2.0: Lens 6 cross-references global GitHub Artifact Register rule for commits/PRs/issues/comments; AI tell scan tightens commit-body identification."
breaking_changes: []
---
# AI Output Quality Gate

Computer surgeon pass. Everything we produce -- code, messages, reports, PoCs, commit messages -- must read as hand-written by a developer. Surgical precision, minimal sufficient output, zero AI tells.

**Resource Hint:** sonnet -- Sequential quality pass, convention matching, AI tell detection.

---

## Mindset

Apply `/pb-preamble` thinking: challenge your own output before anyone else does. Apply `/pb-design-rules` thinking: clarity over cleverness (write like a person), simplicity (cut what doesn't earn its place), fail noisily (flag quality gaps, don't hide them).

---

## When to Use

- After any work is functionally complete, before presenting externally
- Before submitting PRs, reports, emails, or any public-facing output
- When contributing to external projects where convention match matters
- As the final pass before `/pb-commit` or `/pb-pr`

**Do NOT use for:** finding bugs (use `/pb-review`), voice-only checks (use `/pb-voice`), or peer review (use `/pb-linus-agent`). Handcraft is specifically about making AI-assisted output indistinguishable from hand-written.

---

## Relationship to Existing Commands

- `/pb-voice` is the voice-only subset. `/pb-handcraft` is the comprehensive pass (voice + code + structure + conventions).
- `/pb-review` catches bugs and logic issues. `/pb-handcraft` catches machine fingerprints.
- `/pb-linus-agent` is a peer review persona. `/pb-handcraft` is a self-review process.
- `/pb-commit` formats the message. `/pb-handcraft` ensures the message reads like a human wrote it.

---

## The Surgeon Rule

A surgeon doesn't narrate while cutting. Doesn't explain the scalpel. Doesn't add tissue. Doesn't nick adjacent structures.

Minimal sufficient. No bloat. No clipping.

---

## No AI Policy

Treat ALL output as subject to manual quality review -- not just projects that explicitly require it. This is deliberate practice: consistent application builds the muscle that prevents AI tells from creeping in. If we only handcraft when forced to, the muscle atrophies and the tells creep back.

Some projects enforce this explicitly. Most don't but will judge it. The standard is the same either way.

---

## Horizontal Sweep (External Code Contributions)

Before the six lenses, sweep horizontally: does the new code follow existing idioms, or does it introduce new ways of doing old things?

- How does the project parse directives? Use the same parser.
- How does the project manage slice fields on structs? Add the same lifecycle methods.
- How does the project name test struct fields? Match exactly.
- How does the project handle serialization, error wrapping, helpers?

New code that works differently from adjacent code signals an outsider. The sweep catches convention drift that line-by-line review misses.

---

## The 7-Lens Pass

Read the work through seven lenses, in order. Fix as you go.

### Lens 1: Convention Match

The work must be indistinguishable from what the target maintainer would write themselves.

**For external code contributions:**
- Read 3-5 recent commits by the primary maintainer (not other contributors)
- Match: comment case, variable naming, test structure, blank line patterns, import grouping, error message format
- Match: commit message style, PR description style
- If the project has a CONTRIBUTING.md, follow it to the letter

**For your own code/docs:**
- Match existing patterns in the repo
- Consistent with prior work in the same file/directory

**What to check:**
- Comment capitalization (some maintainers: lowercase. Go stdlib: uppercase.)
- Variable names (descriptive but matching the project's style)
- Test naming (descriptive phrases vs TestCase1)
- Struct tags (json+xml+yaml triple? json only?)
- Error wrapping style (project's error package or stdlib?)
- Import grouping (stdlib / external / internal?)

### Lens 2: AI Tell Scan

Read every line looking for machine patterns. If a line makes you think "a human wouldn't write it that way," rewrite it.

**Comment tells:**
- "Split on X to separate Y from Z" -- the code says that
- "Parse challenge types from the first part" -- obvious narration
- "This is the auth bypass guard" -- dramatic labeling
- Multi-line docstrings on internal functions that need 1-2 lines
- "Example directives:" as a label -- just show the directives

**Prose tells:**
- Named transitions ("To set the context", "A quick note on")
- Triple declarative sentences with no contractions
- "It's important to note" / "It's worth mentioning"
- Hedge words before accurate claims ("potentially", "consider")
- Resume-listing prior work to establish credibility
- Perfectly parallel bullet points (same length, same structure)
- `## Summary` / `## Test plan` headers on small fixes

**Code tells:**
- Exhaustive test permutations (3 cases cover it, don't write 12)
- Labeled sections in PoCs ("--- Extracted from ---", "// VULNERABLE:")
- 30-line header comments explaining what the code proves
- Perfectly uniform formatting that no human would produce
- Over-defensive error handling in places that can't fail

**Structure tells:**
- Every paragraph the same length
- Every section with a header
- Numbered lists where prose would be more natural
- Summary at the end restating what was just said
- Opener repetition across posts (scan last 5 before writing new)

**Typography tells:**
- Em dashes anywhere -- use `--` for internal docs, match project conventions for external output
- Exotic/unicode symbols -- stick to ASCII

### Lens 3: Bloat Check

Remove anything that doesn't earn its place.

- Comments that restate the code
- Blank lines between every 3 lines of code (AI spacing pattern)
- Trailing summaries ("In summary, we...")
- Preamble before the actual content
- "Let me know if you need more" closers
- Multiple ways of saying the same thing
- PoC code that explains instead of demonstrates -- strip to minimum viable reproduction

**The test:** cover each line with your hand. Does removing it lose information? If no, cut it.

### Lens 4: Clipping Check

Verify nothing was accidentally removed.

- Did the refactor preserve all original behavior?
- Did the trim remove a needed qualifier or caveat?
- Did the style fix break a test case?
- Is there a blank line or import that was load-bearing?

**The test:** diff against the original. For each removed line, confirm it's genuinely unnecessary.

### Lens 5: Scope Check

The reader built the system. Don't explain their code, their spec, their domain, or their role back to them.

**Cut sentences that:**

- Explain how their own library/API works ("the Authenticate method handles...")
- Teach their domain back to them (OIDC primer to an auth maintainer, SDP sizes to a WebRTC author)
- Interpret their intent ("this suggests it was missed rather than intentional")
- Describe their own role/permission model
- Reference "as documented in..." / "per the RFC..." to justify a point they authored
- Prescribe specific fix values they would choose themselves ("64KB-256KB would cover...")

**The test:** remove the sentence. Can the reader still reproduce, understand, and fix the issue? If yes, cut.

**Why it matters:** Reviewer text that explains a maintainer's own system back reads as outsider, AI-assisted, or condescending -- even when factually correct. The strongest review comments show the bug, the proof, and the fix without restating what the reader built.

### Lens 6: Register Check

Apply project-specific voice guidelines. If the project defines a voice guide or `/pb-voice` has been configured, use those rules. Otherwise, match the register of the target project's existing docs and comments.

General dev-to-dev register:
- No named transitions
- Let the work credential you (don't list prior work)
- Hedge-free conditionals
- Mechanism before impact in technical reports
- Scope unknowns explicitly
- Use dev abbreviations (PoC, SSRF, authz, impl, etc.)

**For GitHub artifacts** (commits, PRs, issues, PR/review/inline comments) the global rule (`~/.claude/CLAUDE.md` § GitHub Artifact Register) sets numeric length ceilings -- subject-only commits, one-paragraph PR bodies for small PRs, one sentence per review-comment finding. Strip assistant-attribution footers, narration, severity adjectives, and restatements of what the diff shows.

### Lens 7: Read-Aloud Check

Read the output as if speaking it to the maintainer over a call.

- Does any sentence feel robotic when spoken?
- Are sentence lengths varied, or is it mechanical?
- Does the flow have rhythm, or does it plod?
- Would you actually say this to a colleague?

If it sounds like a press release, rewrite until it sounds like a person.

**For conversational artifacts (PR/issue comments, emails, Slack):** beyond spoken rhythm, check the shape. Does it read like someone typed this live, or like a generated review artifact with section headers and bullet padding? Scene-setter up front, specific pointers, flowing prose. Structured submissions (GHSA fields, VRP forms) skip this sub-check -- required sections drive their shape.

---

## Submission Quality Gate (Security Reports)

Before any security submission -- GHSA, bounty platform, email -- verify these in addition to the six lenses:

- **PoC or traced input path.** "I tested this" or "I traced input from annotation to fmt.Sprintf with no sanitization." Code analysis is silver; observable output is gold. Prefer gold.
- **Realistic scenario.** What does the attacker do, what breaks. State preconditions (RBAC, auth, config).
- **Not a false positive.** Check for sanitization you missed, config flags that disable the path, unreachable preconditions.
- **Timing judgment.** Don't submit known-class bugs in pre-release code the maintainer will likely catch. Hold and watch the release. Submit if it ships unfixed.
- **Impact field isolation.** Platform triagers read Impact separately from Description. Read the Impact field with zero other context. Two tests: (a) does a triager who reads ONLY this field understand the attack? (b) can they dismiss it without reading Description? If yes to (b), rewrite until the answer is no. Name the actor, the action, the blast radius, and the preconditions in the Impact field itself.
- **PoC code as evidence.** Run Lens 2 (AI Tell Scan) separately on all PoC code. Docstrings, argparse, class hierarchies, try/except with helpful messages, unused imports, and trailing summaries are the most common AI tells in PoC scripts. The PoC is what the triager scrutinizes most -- a clean report with an over-engineered PoC gets flagged.
- **Comparison case.** Show what the code DOES handle correctly next to what it misses. Vulnerable line vs safe alternative. Blocked path vs bypassed path. This demonstrates manual code reading and is the strongest signal that you understand the codebase.

---

## Review Comment Craft

Before posting any review comment on a PR, issue, or thread, check:

- **One load-bearing observation per comment, not a list.** If three concerns arise, pick the most load-bearing and raise the others only after the first is resolved.
- **No performative hedge.** "Just wanted to flag..." or "This might be wrong, but..." weakens signal without softening tone. Either state the observation or don't raise it.
- **Opinion flagged as opinion.** "I'd be tempted to X" or "My lean would be X" signals personal preference and leaves the maintainer room to disagree. Better than either a flat demand or a hedged question.
- **No closing ceremony.** "Happy to pair", "Let me know if...", "Hope this helps" -- strip unless the offer is concrete and specific to this thread.
- **Paired options or single opinionated lean.** Not a multi-section review with headers. A PR comment should read like a typed message, not a consulting deliverable.
- **Scene-setter up front.** Open with evidence or a specific file/function pointer, not a preamble. "Pulled locally; suite runs green" beats "Thanks for the contribution! I took a look at..."

**The test:** does the comment read like a dev typed this into the GitHub box, or like a generated review artifact? If the latter, reshape until it reads typed.

---

## After the Pass

Optional: run `/pb-linus-agent` for peer review. Present final work to the reviewer before any external action.

All work stays local until explicitly approved for external action. No auto-push, no auto-send, no auto-create.

---

## Scope Guard

**Do during /pb-handcraft:**
- Read and fix the current work product
- Match conventions by reading the target codebase
- Remove AI tells, bloat, clipping
- Present fixed work for review

**Do NOT during /pb-handcraft:**
- Add new functionality
- Expand scope
- Write additional tests beyond what the change requires
- Refactor adjacent code
- Execute any external action

If the handcraft pass reveals a real issue (missing test case, logic bug), fix it -- but don't use it as an excuse to expand scope.

---

## Integration

Run after work is functionally complete, before presenting externally. Integrates naturally with:
- `/pb-review` (code quality) -> `/pb-handcraft` (human quality) -> `/pb-commit` (messages) -> `/pb-pr` (PR descriptions)

---

## Related Commands

- `/pb-voice` -- Voice-only subset of the handcraft pass
- `/pb-review` -- Code review (bugs, logic, tests)
- `/pb-linus-agent` -- Peer review persona
- `/pb-commit` -- Commit message quality

---

*The best AI-assisted work is the kind nobody can tell was AI-assisted.*
