---
name: "pb-caveman"
title: "Caveman Filter (Ultra-Minimal Output)"
category: "development"
difficulty: "beginner"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-handcraft', 'pb-voice', 'pb-review', 'pb-commit']
last_reviewed: "2026-04-10"
last_evolved: ""
version: "1.0.0"
version_notes: "Initial: ultra-minimal filter pass for ephemeral dev-loop output. Two modes (lite, full). Deliberate counterweight to /pb-handcraft."
breaking_changes: []
---
# Caveman Filter (Ultra-Minimal Output)

Strip output to the bone for ephemeral dev-loop work. Kill articles, transitions, pleasantries. Keep signal. For throwaway 1-liners and in-session chatter where tokens cost more than re-reading.

**Resource Hint:** sonnet -- Mechanical text reduction; pattern-level filtering, no architecture judgment.

---

## Mindset

Apply `/pb-preamble` thinking: density is not cleverness; it is respect for the reader's time *when the reader is you, thirty seconds from now*. Apply `/pb-design-rules` thinking: simplicity (cut what doesn't earn its place), silence when nothing to say.

This command is the deliberate opposite of `/pb-handcraft`. Handcraft aims at *indistinguishable from hand-written*. Caveman aims at *maximum signal per byte*. They cover different surfaces. See *When NOT to Use* below.

---

## When to Use

- In-session debug chat, scratch notes, status pings to yourself
- 1-line code comments where the codebase already leans terse
- TODO/FIXME/NOTE annotations
- Internal tool output, CLI glue, bot notifications nobody will read cold
- Bullet-form standup lines where prose is overhead

## When NOT to Use

- PR descriptions, commit messages -- use `/pb-handcraft` and `/pb-commit`
- Docstrings on public APIs, shipped documentation, release notes, ADRs
- Anything a teammate will read cold in 6 months
- External reports, security submissions, user-facing copy
- Any codebase whose comment style is sentence-case prose (match local style)

If in doubt, `/pb-handcraft` wins.

---

## The Caveman Rule

Words cost. Signal is free. Write for the reader who already knows the context, because that reader is you in the next message.

BEACON reconciliation: *clarity over cleverness* still holds. Terseness IS clarity when the reader has the context loaded. Terseness BECOMES damage the moment context has to be rebuilt from the text alone. The command scope exists to keep those two cases separate.

---

## Modes

```
/pb-caveman             -> lite (default): drop filler, keep grammar
/pb-caveman full        -> full: fragments, abbreviations, telegraphic
```

### Lite

Drop the filler; keep the sentences grammatical. Reads as a terse developer, not a robot.

**Rules:**
- Strip pleasantries, hedges, transitions ("Let's", "I think", "It seems", "To be clear")
- Cut articles only where removal does not hurt reading speed
- One idea per line; no trailing summaries
- No preamble; lead with the thing
- Keep code, identifiers, commands, paths untouched

**Before:**
> I think the issue is probably that the cache is returning stale data when the TTL expires. Let's try invalidating it manually to confirm.

**After:**
> Cache returning stale data on TTL expiry. Invalidate manually to confirm.

### Full

Telegraphic. Fragments allowed. Abbreviations allowed. Symbols allowed where unambiguous. Only for output you control the read context of.

**Rules:**
- Fragments over sentences
- Drop articles, auxiliaries, most pronouns
- Dev abbreviations: auth, impl, repro, ctx, req, resp, cfg, env
- Symbols where crisp: `->`, `L42`, `~`, `!=`
- Still keep code, identifiers, commands, paths untouched
- Still no filler, no narration, no summaries

**Before:**
> The test is failing because the mock returns null when we expect an empty array. I need to update the mock setup in the beforeEach block.

**After:**
> Test fails: mock returns null, expect `[]`. Fix beforeEach.

---

## The Filter Pass

1. **Read the draft.** Identify the reader: is it you-in-30-seconds or someone reading cold? If cold, stop -- wrong command.
2. **Cut the opener.** No "Sure," "Here's," "I'll," "Let's."
3. **Cut the closer.** No "Hope this helps," "Let me know," trailing summary.
4. **Cut hedges.** "probably," "it seems," "I think" -- delete or replace with confidence level only if load-bearing.
5. **Cut transitions.** "Additionally," "Moreover," "To be clear," "That said" -- almost always deletable.
6. **Collapse sentences.** Two short sentences > one long one with a conjunction.
7. **Preserve code verbatim.** Never abbreviate identifiers, paths, commands, error messages, or anything inside backticks.
8. **Read aloud test (inverted).** If it sounds natural as spoken English, you are probably in lite mode. If it sounds like a telegram, you are in full mode. Neither is wrong; pick deliberately.

---

## Preservation Guarantees

Caveman MUST NOT touch:
- Code blocks and inline code
- File paths, identifiers, URLs
- Error messages and log lines (quote exactly)
- Version numbers, commit SHAs, ticket IDs
- Direct quotes from users, docs, or specs
- Load-bearing qualifiers (security caveats, correctness conditions, "only if")

If stripping a word changes the truth value of the sentence, put it back.

---

## Horizontal Sweep (Code Comments)

Before applying to code comments, sweep the surrounding file and 2-3 nearby files. Match the existing register.

- If the codebase uses full sentences with punctuation, do not caveman.
- If the codebase uses terse fragments, caveman-lite is already the house style -- use it.
- Never introduce caveman-full into a repo whose comment culture is prose. Convention match beats compression.

---

## Scope Guard

**Do during /pb-caveman:**
- Strip the current draft
- Preserve code, identifiers, truth-conditions
- Respect the mode (lite vs full) you picked
- Flag the output as caveman-mode if the reader might not know

**Do NOT during /pb-caveman:**
- Apply it to anything in the *When NOT to Use* list
- Strip load-bearing qualifiers
- Invent abbreviations the reader will not recognize
- Use it as a shortcut around actually thinking about what to say

---

## Integration

`/pb-caveman` is ephemeral by design. It does not replace `/pb-handcraft` in any workflow. If the output is about to cross a boundary (PR, commit, doc, external message), switch to `/pb-handcraft` for the final pass.

```
in-session scratch -> /pb-caveman (optional)
work complete     -> /pb-review -> /pb-handcraft -> /pb-commit -> /pb-pr
```

---

## Related Commands

- `/pb-handcraft` -- Counterweight. If in doubt, handcraft wins.
- `/pb-voice` -- Dev-to-dev register for prose that still needs to read naturally
- `/pb-review` -- Upstream quality pass on the underlying work
- `/pb-commit` -- Commit messages (never caveman these)

---

*Same fix. Less word. Only where less word means clearer signal.*
