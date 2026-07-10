---
name: "pb-handcraft"
title: "AI Output Quality Gate"
category: "development"
difficulty: "intermediate"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-voice', 'pb-review', 'pb-linus-agent', 'pb-commit', 'pb-llm-guidelines']
last_reviewed: "2026-07-10"
last_evolved: "2026-07-10"
version: "1.5.0"
version_notes: "v1.5.0: Voice pass is now a required lens (was conditional 'if configured'). /pb-voice fires on every prose-bearing artifact. Prose/structure/typography tell blocks removed from Lens 2, delegated to pb-voice's canonical Categories 1-12 (kills the duplicate). Lens 2 keeps code/comment tells plus new code-specific tells (comments explain what-not-why, commit body re-narrates diff, over-descriptive identifiers). Lens 6 defers register calibration to the voice pass. Shapes-over-words meta-principle echoed."
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

**Do NOT use for:** finding bugs (use `/pb-review`), voice-only checks on a piece of prose (run `/pb-voice` directly; handcraft fires it for you as part of the full pass), or peer review (use `/pb-linus-agent`). Handcraft is specifically about making AI-assisted output indistinguishable from hand-written.

---

## Relationship to Existing Commands

- `/pb-voice` is the canonical prose-tell engine. `/pb-handcraft` runs it as a required lens (Lens 2) and layers code, convention, PoC, and scope checks on top. Voice owns prose; handcraft owns the whole artifact.
- `/pb-review` catches bugs and logic issues. `/pb-handcraft` catches machine fingerprints.
- `/pb-linus-agent` is a peer review persona. `/pb-handcraft` is a self-review process.
- `/pb-commit` formats the message. `/pb-handcraft` ensures the message reads like a human wrote it.

---

## The Surgeon Rule

Minimal sufficient. No bloat. No clipping.

---

## The Badge Test

One question stands behind all seven lenses: **would you defend every line of this as your own in review -- without "the AI wrote that part"?** If any line fails, it is not done.

This is ambient, not a step you invoke. It holds for every artifact -- code, commit, PR, comment, report -- whether or not the project asks for it. The lenses are how you make it true; the question is the bar. Beyond clean prose, work that carries your name is:

- **Self-evidencing** -- claims backed by a test, a repro, or a measurement, not "should work."
- **Scope-honest** -- name what you did not do; no silent truncation.
- **One voice** -- code, commit, and PR read as one hand wrote them.
- **Ceremony-free** -- the absence of scaffolding and attribution footers is the signature.

---

## No AI Policy

Treat ALL output as subject to manual quality review -- not just projects that explicitly require it. This is deliberate practice: consistent application builds the muscle that prevents AI tells from creeping in. If we only handcraft when forced to, the muscle atrophies and the tells creep back.

Some projects enforce this explicitly. Most don't but will judge it. The standard is the same either way.

---

## Horizontal Sweep (External Code Contributions)

Before the seven lenses, sweep horizontally: does the new code follow existing idioms, or does it introduce new ways of doing old things?

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

**Exit:** Did you read the target codebase, or match from memory? (Fails when you match from memory — you'll miss convention drift.)

### Lens 2: AI Tell Scan

Read every line looking for machine patterns. If a line makes you think "a human wouldn't write it that way," rewrite it. These patterns rotate every model generation, so weight the *shapes* (copula avoidance, antithesis density, participial padding, inline-header lists, metronomic rhythm) over any single word. The word lists age; the shapes don't.

**Prose, structure, typography, and register tells: run the voice pass.** `/pb-voice` owns the canonical list (Categories 1-12): dead-giveaway vocabulary, copula avoidance, antithesis, participial clauses, hedging density, stock transitions, metronomic rhythm, abstraction, inline-header lists, em-dashes, title case, summary endings, register mismatch. It runs on **every** prose-bearing artifact: commit, PR, report, doc, issue, comment prose. Not optional. Do not re-list or re-fix prose tells here; that duplicates voice and drifts. Handcraft owns only what voice can't see, in code and comments:

**Comment tells:**
- "Split on X to separate Y from Z" -- the code says that
- "Parse challenge types from the first part" -- obvious narration
- "This is the auth bypass guard" -- dramatic labeling
- Comments that explain *what* the code does, never *why*; the mechanism is visible, the rationale and the edge case are not
- Multi-line docstrings on internal functions that need 1-2 lines; ceremonial Args/Returns blocks on trivial helpers
- "Example directives:" as a label -- just show the directives

**Code tells:**
- Exhaustive test permutations (3 cases cover it, don't write 12)
- Labeled sections in PoCs ("--- Extracted from ---", "// VULNERABLE:")
- 30-line header comments explaining what the code proves
- Over-descriptive identifiers (`total_user_input_character_count`) that read like a contract
- Perfectly uniform formatting that no human would produce
- Over-defensive error handling in places that can't fail

**Commit and PR tells:**
- Commit body re-narrates the diff ("This commit adds...", "The following changes were made"). The diff shows what; the body is for why. It should be explainable from the message in a line or two, not a paragraph-by-paragraph replay.
- PR template-header boilerplate (`## Changes` / `## Motivation` / `## Testing`) on a small change
- Attribution trailers (`Co-Authored-By`, `🤖 Generated with`); strip per the GitHub Artifact Register

**Exit:** Did the voice pass run on the prose, and did you flag at least one code/comment tell you initially overlooked? (Fails when you skip the voice pass, or when you've read so much AI output you've normalized the patterns.)

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

**The structure test:** scan section openings. If the voice pass flagged repeated section anatomy or uniform structure (voice Cat 2), verify you broke at least one section's rhythm. Uniform structure is bloat regardless of who (or what) wrote it.

**Exit:** Did you remove anything, or did everything earn its place on first pass? (Fails when attachment to your own prose makes every line feel load-bearing.)

### Lens 4: Clipping Check

Verify nothing was accidentally removed.

- Did the refactor preserve all original behavior?
- Did the trim remove a needed qualifier or caveat?
- Did the style fix break a test case?
- Is there a blank line or import that was load-bearing?

**The test:** diff against the original. For each removed line, confirm it's genuinely unnecessary.

**Exit:** Did you diff against the original and confirm every removal? (Fails when the diff is large and you skim instead of checking each line.)

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

**Exit:** Did you cut anything that explained the reader's domain back to them? (Fails when you assume the reader needs context you'd find condescending if roles were reversed.)

### Lens 6: Register Check

Register is calibrated by the voice pass (`/pb-voice` Step 0 + Category 12), which already ran in Lens 2; it reads the target register from the artifact type or persona and flags register mismatch. This lens applies the handcraft-specific register concerns voice doesn't own: the GitHub Artifact Register ceilings for commits/PRs/issues, and the dev-to-dev defaults for code-adjacent output.

General dev-to-dev register:
- No named transitions
- Let the work credential you (don't list prior work)
- Hedge-free conditionals
- Mechanism before impact in technical reports
- Scope unknowns explicitly
- Use dev abbreviations (PoC, SSRF, authz, impl, etc.)

**For GitHub artifacts** (commits, PRs, issues, PR/review/inline comments): `~/.claude/CLAUDE.md` § GitHub Artifact Register sets the ceilings, strip list, and never-write list.

**Conversational check:** read the output aloud as if saying it to a colleague over a drink. Mouth the words — silent reading skips what the tongue catches.

- Would you actually say this sentence to another human in conversation?
- Would they check their phone midway through?
- Does it sound like you typed this live, or like a generated artifact?

If the conversational check flags something your eye skipped, the problem is register, not cadence. Fix it here.

**Exit:** Would you say every sentence aloud to a colleague without hedging or apologizing? (Fails when you read silently — your eye skips what your tongue would catch.)

### Lens 7: Read-Aloud Check

This is a detection method, not a problem category. Your eyes skip what your tongue catches — reading aloud surfaces issues the other lenses miss, regardless of what kind of issue it is.

Read the output as if speaking it to the maintainer over a call.

- Does any sentence feel robotic when spoken?
- Are sentence lengths varied, or is it mechanical?
- Does the flow have rhythm, or does it plod?

If it sounds like a press release, rewrite until it sounds like a person.

**For conversational artifacts (PR/issue comments, emails, Slack):** beyond spoken rhythm, check the shape. Does it read like someone typed this live, or like a generated review artifact with section headers and bullet padding? Scene-setter up front, specific pointers, flowing prose. Structured submissions (GHSA fields, VRP forms) skip this sub-check -- required sections drive their shape.

**Exit:** Did reading aloud catch something silent reading skipped? (Fails when you mutter instead of reading aloud — whispering is still silent reading.)

### Final Re-Read

Not an eighth lens — a closing sweep. After all seven lenses, re-read the final output once from top to bottom. You changed things. Confirm the fixes didn't introduce new tells. If you find one, fix it and re-read; one clean pass is enough. Don't restart the lens pass.

---

## Submission Quality Gate (Security Reports)

Before any security submission -- GHSA, bounty platform, email -- verify these in addition to the seven lenses:

- **PoC or traced input path.** "I tested this" or "I traced input from annotation to fmt.Sprintf with no sanitization." Code analysis is silver; observable output is gold. Prefer gold.
- **Realistic scenario.** What does the attacker do, what breaks. State preconditions (RBAC, auth, config).
- **Not a false positive.** Check for sanitization you missed, config flags that disable the path, unreachable preconditions.
- **Timing judgment.** Don't submit known-class bugs in pre-release code the maintainer will likely catch. Hold and watch the release. Submit if it ships unfixed.
- **Impact field isolation.** Platform triagers read Impact separately from Description. Read the Impact field with zero other context. Two tests: (a) does a triager who reads ONLY this field understand the attack? (b) can they dismiss it without reading Description? If yes to (b), rewrite until the answer is no. Name the actor, the action, the blast radius, and the preconditions in the Impact field itself.
- **PoC code as evidence.** Run Lens 2 (AI Tell Scan) separately on all PoC code. Docstrings, argparse, class hierarchies, try/except with helpful messages, unused imports, and trailing summaries are the most common AI tells in PoC scripts. The PoC is what the triager scrutinizes most -- a clean report with an over-engineered PoC gets flagged.
- **Comparison case.** Show what the code DOES handle correctly next to what it misses. Vulnerable line vs safe alternative. Blocked path vs bypassed path. This demonstrates manual code reading and is the strongest signal that you understand the codebase.

---

## Per-Artifact

Extensions for specific artifact types that need more than the seven lenses.

### Review Comments

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
- Delete pre-existing dead code (mention it, don't delete unless asked)
- Execute any external action

If the handcraft pass reveals a real issue (missing test case, logic bug), fix it -- but don't use it as an excuse to expand scope.

---

## Integration

Run after work is functionally complete, before presenting externally. Integrates naturally with:
- `/pb-review` (code quality) -> `/pb-handcraft` (human quality) -> `/pb-commit` (messages) -> `/pb-pr` (PR descriptions)

---

## Related Commands

- `/pb-voice` -- Canonical prose-tell engine; handcraft fires it as a required lens (Lens 2)
- `/pb-review` -- Code review (bugs, logic, tests)
- `/pb-linus-agent` -- Peer review persona
- `/pb-commit` -- Commit message quality
- `/pb-llm-guidelines` -- LLM coding guardrails referenced in Scope Guard

---

*The best AI-assisted work is the kind nobody can tell was AI-assisted.*
