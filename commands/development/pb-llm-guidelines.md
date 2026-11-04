---
name: "pb-llm-guidelines"
title: "LLM Coding Guidelines"
category: "development"
difficulty: "beginner"
model_hint: "sonnet"
execution_pattern: "reference"
related_commands: ['pb-preamble', 'pb-design-rules', 'pb-handcraft', 'pb-start', 'pb-forge']
last_reviewed: "2026-11-04"
version: "1.4.0"
version_notes: "v1.4.0: Verify the referent, not a proxy (second probe for absence, origin after a seen fetch, sample size, pipes, background tail, stalled watches); prove the instrument can fail (known answer, re-break, invariant, red on main, isolated evals); mutating commands check where and how often they run. The Integration table, which repeated each section's coverage line, is gone."
breaking_changes: []
---
# LLM Coding Guidelines

Behavioral guidelines to reduce common LLM coding mistakes, derived from [Andrej Karpathy's observations](https://x.com/karpathy/status/2015883857489522876) on LLM coding pitfalls. These principles bias toward caution over speed. For trivial tasks, use judgment.

**Mindset:** Apply `/pb-preamble` thinking (challenge assumptions, surface trade-offs) and `/pb-design-rules` thinking (clarity over cleverness, simplicity by default). These guidelines are a complementary lens. They don't replace existing commands; they reinforce the behaviors those commands already expect.

**Resource Hint:** sonnet - Reference guidelines for coding discipline; no architecture judgment.

---

## When to Use

- Reviewing LLM-generated code for common failure patterns
- Teaching LLMs to behave like disciplined engineers
- Self-checking your own LLM-assisted output
- Onboarding teams to LLM collaboration anti-patterns

---

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface trade-offs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them. Don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

**Playbook coverage:** `/pb-preamble` (challenge assumptions, critical peer), `/pb-think` (ideate 10+ options before converging), `/pb-sketch` (enumerate decision forks, recommend don't decide), `/pb-start` (scope questions surface assumptions).

---

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

**Playbook coverage:** `/pb-design-rules` Rule 5 (Simplicity), Rule 6 (Parsimony), `/pb-standards` YAGNI principle, `/pb-handcraft` Bloat Check and Scope Check, `/pb-caveman` (ultra-minimal output for internal work).

---

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it. Don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

Before a mutating command, check where and how often it runs: an unchecked `cd` once ran a git command in the wrong repo; re-running a command to see its output again repeats its side effect (a paid call), so keep the first result; importing a repo's script writes `__pycache__` into it, so run Python with `-B`.

**A deliberate mutation is cleanup you have not done yet.** Editing source to prove something (a harness checking that a test can actually fail, a guard disabled to force a branch) is the one case where residue is the default outcome rather than a slip: the restore runs last, so it is exactly what a timeout, a `Ctrl-C`, or a raised exception kills. Put the restore in a `finally` or outside whatever bounds the experiment, then confirm the tree with `git diff --stat` instead of trusting the script's own cleanup. A killed harness once left a *disabled production guard* in a tree another session was committing from; the mutation was intentional and reviewed, and the residue still nearly shipped.

**Playbook coverage:** `/pb-handcraft` Surgeon Rule, Convention Match, Scope Guard (do NOT refactor adjacent code). The "mention dead code, don't delete it" convention is explicitly in Scope Guard.

---

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:

```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

**Verify the referent, not a proxy.** A proxy (an HTTP 200, a flag, "0 failures" beside zero runs, a grep miss, a README, a stale checkout) does not answer a state question. The test: could the signal come back the same if the answer were no?
- A claim that something does not exist takes a second probe (a synonym, the owning file) before it drives action.
- An upstream claim reads `origin/<default>` after a fetch you saw land.
- A conclusion states its sample size and how faithful its setup was: 3 runs hid a cause that 8 found, and local limits flipped a result.
- A pipeline exits with its last command's status, so `build | tail` reports success on a failure: carry the exit code through. A dropped `gh run watch` reports failure on a green run; a notification is a hint, not a verdict.
- `| tail` on a background job shows nothing until it ends: `tee` to a file and read the file.
- A watch that matches only progress is silent on a stall: match the failure signatures too (timeout, retry, traceback, empty output), or give it a deadline.

**Prove the instrument can fail.** Run a new measurement on a case with a known answer before trusting it, and re-break a fix to watch its new assertion fail. Mutation-check every new guard, aim the mutants at seams, and assert the invariant, not a symptom: a "content differs" check passes anything idempotent. A new gate goes red on main once before it is trusted. Agent evals run isolated, with the transcript read before scoring.

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

**Playbook coverage:** `/pb-start` asks "how will you know it's done?" to establish verifiable success criteria before coding. `/pb-forge` step-runner enforces verify-per-step. `/pb-testing` covers test-after-reproduce patterns. `/pb-debug` uses repro-first methodology.

---

## Related Commands

- `/pb-preamble` - Collaboration philosophy (challenge assumptions)
- `/pb-design-rules` - Technical principles (clarity, simplicity, modularity)
- `/pb-handcraft` - AI output quality gate (surgical precision, convention match)
- `/pb-start` - Begin work with scope and success criteria
- `/pb-forge` - Step-runner with verification per stage

---

*Guidelines bias toward caution. For trivial tasks, use judgment.*
