---
name: "pb-llm-guidelines"
title: "LLM Coding Guidelines"
category: "development"
difficulty: "beginner"
model_hint: "sonnet"
execution_pattern: "reference"
related_commands: ['pb-preamble', 'pb-design-rules', 'pb-handcraft', 'pb-start', 'pb-forge']
last_reviewed: "2026-07-31"
last_evolved: ""
version: "1.3.0"
version_notes: "v1.3.0: a deliberate mutation is cleanup you have not done yet -- the restore runs last, so a timeout or a Ctrl-C kills exactly the step that undoes the experiment; put it in a finally or outside the bound, and verify the tree rather than the script's cleanup. v1.2.0: a watch that matches only progress is silent on a stall -- silence and health are indistinguishable unless the filter also matches failure signatures or the watch carries a deadline. v1.1.0: verify the thing, not the signal that reports it -- a piped build exits with the pipe's status and a dropped watch reports failure on a green run, so a completion notification is a hint rather than a verdict. Initial: 4 behavioral guidelines for reducing LLM coding mistakes, sourced from Karpathy's observations, cross-referenced with existing playbook commands."
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

**A deliberate mutation is cleanup you have not done yet.** Editing source to prove something -- a harness checking that a test can actually fail, a guard disabled to force a branch -- is the one case where residue is the default outcome rather than a slip: the restore runs last, so it is exactly what a timeout, a `Ctrl-C`, or a raised exception kills. Put the restore in a `finally` or outside whatever bounds the experiment, then confirm the tree with `git diff --stat` instead of trusting the script's own cleanup. A killed harness once left a *disabled production guard* in a tree another session was committing from; the mutation was intentional and reviewed, and the residue still nearly shipped.

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

**Verify the thing, not the signal that reports it.** A verification step is only as good as what carries its result. A build piped through `tail` exits with `tail`'s status, so it reports success on a failure one second in. A `gh run watch` whose connection drops reports failure on a green run. When an outcome arrives as a notification rather than as something you observed, check the underlying state independently before acting on it: the notification is a hint, not a verdict. When you write the wrapper, carry the exit code through, because a pipeline discards it silently.

**A watch that matches only progress is silent on a stall.** The same discipline applies to filters. A monitor keyed to `^  chunk` and a completion line reports nothing when the run hangs for 25 minutes -- and nothing is exactly what a healthy quiet run also produces, so silence carries no information. Match the failure signatures too (timeout, retry, traceback, the empty-output case), or give the watch a deadline, so that "no news" cannot mean both states at once.

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

**Playbook coverage:** `/pb-start` asks "how will you know it's done?" to establish verifiable success criteria before coding. `/pb-forge` step-runner enforces verify-per-step. `/pb-testing` covers test-after-reproduce patterns. `/pb-debug` uses repro-first methodology.

---

## Integration

These guidelines are ambient. They apply every time you code with an LLM, regardless of which command you're running. They don't add ceremony; they're a lens.

| Principle | Primary commands |
|-----------|-----------------|
| Think before coding | `/pb-preamble`, `/pb-think`, `/pb-sketch`, `/pb-start` |
| Simplicity first | `/pb-design-rules`, `/pb-standards`, `/pb-handcraft`, `/pb-caveman` |
| Surgical changes | `/pb-handcraft` (Surgeon Rule + Scope Guard) |
| Goal-driven execution | `/pb-start` (success criteria), `/pb-forge` (verify-per-step) |

---

## Related Commands

- `/pb-preamble` - Collaboration philosophy (challenge assumptions)
- `/pb-design-rules` - Technical principles (clarity, simplicity, modularity)
- `/pb-handcraft` - AI output quality gate (surgical precision, convention match)
- `/pb-start` - Begin work with scope and success criteria
- `/pb-forge` - Step-runner with verification per stage

---

*Guidelines bias toward caution. For trivial tasks, use judgment.*
