---
name: "pb-huddle"
title: "Multi-Perspective Decision Session"
category: "core"
difficulty: "intermediate"
model_hint: "opus"
execution_pattern: "parallel-then-sequential"
related_commands: ['pb-think', 'pb-preamble', 'pb-clara-curator', 'pb-maya-product', 'pb-adr']
last_reviewed: "2026-11-03"
version: "1.8.0"
version_notes: "v1.8.0: Spaced double hyphens replaced."
breaking_changes: []
---
# Multi-Perspective Decision Session

Multi-persona thinking session for strategic decisions. Not a review gate: a collaborative exploration where personas argue, disagree, and find the approach that survives scrutiny.

Use `/pb-think` for structured problem decomposition. Huddle is for decisions where relationships, timing, and perception matter as much as correctness.

**Resource Hint:** opus - Complex multi-persona reasoning, tension synthesis, strategic judgment.

---

## Mindset

Apply `/pb-preamble` thinking: best ideas win regardless of source. Personas should genuinely disagree; forced consensus defeats the purpose. Apply `/pb-design-rules` thinking: distrust "one true way" (that's why we run multiple lenses), fail noisily (surface irreconcilable tensions, don't paper over them).

---

## When to Use

- Before strategic decisions that affect relationships or positioning
- When there are genuine trade-offs with no obvious answer
- When gut instinct needs stress-testing
- When pacing, framing, or sequencing matters as much as content

**Do NOT use for:** routine code review (vetting disputed review findings at a `/pb-forge` Self-gate is the exception: the panel rules on findings, it does not re-review), simple go/no-go decisions, or when the answer is obvious. Use `/pb-linus-agent` for technical review, `/pb-voice` for writing quality. Huddle is for strategy.

---

## Modes

```
/pb-huddle "question"             → Standard (default): full huddle with context loading
/pb-huddle --re-huddle "question" → Re-huddle: refined follow-up, same personas, lighter context
```

**Natural-language trigger:** `"re-huddle: new focus question"` also invokes re-huddle mode. The flag and the prefix are equivalent; use whichever reads more naturally.

---

### Re-Huddle Mode

When a huddle's synthesis identifies a refined follow-up question, run a re-huddle instead of a full huddle. It reuses the persona set and context from the prior huddle, focusing only on the new question.

**When to use:**
- The prior huddle surfaced a refined question worth deeper exploration
- The same personas should weigh in on the follow-up
- The context hasn't changed (same session, same files)

**What changes:**
- **Skip context loading** (Step 2): personas already have the background from the prior huddle
- **Shorter persona prompts**: reference the prior huddle output instead of re-loading raw context
- **Keep framing** (Step 1): the refined question still needs clear framing; it's a different question from the original

**What stays the same:**
- Full huddle output format (persona arguments, tensions, synthesis, decision, recording)
- Steps 3-6 run identically to standard mode

**Guardrails:**
- **Same-conversation only**: re-huddle depends on the personas having the prior huddle's context in memory. Across sessions, run a full huddle.
- **Fall back to full huddle** if the prior huddle output can't be found or persona names can't be extracted. If in doubt, ask which personas to use.

**How it works:**
1. Read the most recent huddle output from the conversation
2. Extract the persona names used
3. Frame the new question (Step 1)
4. Run personas with abbreviated prompts that reference the prior output (Step 3). If the panel ran as agents that are still addressable, message those same agents (in Claude Code, `SendMessage` to each agent) rather than spawning new ones: each keeps the brief and its own argument, so the follow-up costs one message per lens
5. Find tensions, synthesize, record (Steps 4-6)

---

## Procedure

### Step 1: Frame the Question

Before framing, search previous decisions and the current plan for this topic; a plan often already says what to do once its condition is met. Don't re-derive what was already decided; build on it.

State the question clearly. Not "what should we do?" but the specific tension:
- "Should we refactor the auth module before adding OAuth support?"
- "How do we communicate this breaking API change to existing clients?"
- "Do we optimize for developer experience or runtime performance in the SDK?"

The question must have genuine tension. If there's an obvious answer, skip the huddle. A check already in the repo that fails the proposal (a test, a CI assertion, a lint rule) is an obvious answer.

**Bring a proposal to break, not a blank page.** A panel is sharpest when it is adversarial against something concrete (a specific resolution, a written rule, a chosen default) and weakest when asked to generate options from nothing. If you have no candidate answer yet, write the worst defensible one and hand the panel that; being wrong in a specific direction gives every lens something to push on.

### Step 2: Load Context

Read relevant state files. The huddle is only as good as the context loaded. Personas can't argue well without knowing the situation.

A sketch or brief is a claim about the work, not a record of it. Treat files that *describe* the work (sketches, briefs, summaries) as claims: open the artifacts a claim rests on, and check what a status claim ('sketch complete since X') belongs to, before briefing the panel.

If the user overrode a standing rule this session, the brief states the rule and the override. The panel can read the rule; it cannot read the session.

The brief you write is a claim too. Each fact in it names how it was checked: the command run or the file opened. A fact with no check is labelled unverified.

**Measure before you brief.** If the question turns on a number one command can produce (how often a rule fires, how many cases pass), run it and put the result in the brief. A panel handed an opinion a measurement would settle spends its round arguing the opinion. When the question is whether the work already exists (a corpus, a codebase, a prior decision), measure by thesis, not topic: a keyword grep is a measurement, and it passes the collision it cannot see.

If no relevant context exists for this question, spend five minutes writing it first. A context-free huddle is worse than no huddle.

### Step 3: Assign Roles and Select the Panel

A huddle has four roles. Two are fixed; two are chosen per decision.

| Role | Who | Job |
|---|---|---|
| **Process orchestrator** | Claude | Neutral engine: run the panel in parallel, prevent anchoring, record, execute |
| **Curatorial orchestrator** | Clara (`/pb-clara-curator`) | The whole-system voice at synthesis: does it belong, what does it cost to carry, are these voices actually disagreeing |
| **Lead** | topic-selected domain authority | Decisive in-lane. Not first-and-loudest: the panel challenges in parallel before the lead rebuts and closes. In-lane authority, not a cross-domain veto |
| **Panel** | 2-4 other lenses | Challenge from their lanes |

Name the lead by the decision's center of gravity and record it ("Lead: Travis, trust-boundary decision"). The user can override. When the topic genuinely is the whole (scope, lifecycle, coherence), Clara is both orchestrator and lead, and Claude stays the second, neutral orchestrator to keep her honest.

**Lead and panel by decision type:**

| Decision type | Lead | Panel |
|---|---|---|
| Technical / architecture | Linus | Jordan + Alex + Travis |
| Security / trust boundary | Travis | Linus + Alex |
| Testing / reliability | Jordan | Linus + Alex |
| Infrastructure / resilience | Alex | Jordan + Linus |
| Product / user value | Maya | Sam + Kai + Elena |
| Design / UX / brand | Elena | Maya + Sam |
| Distribution / launch | Kai | Maya + Sam |
| Documentation / clarity | Sam | Maya + Elena |
| Scope / lifecycle / coherence | Clara | Maya + Linus |

**Roster (9):** `/pb-linus-agent`, `/pb-travis-security`, `/pb-jordan-testing`, `/pb-alex-infra`, `/pb-maya-product`, `/pb-elena-design`, `/pb-kai-reach`, `/pb-sam-documentation`, `/pb-clara-curator`.

Each persona gets the SAME brief; disagreement is expected and valuable. Run the panel in parallel so the first response doesn't anchor the others. The lead rebuts and closes in its lane; the orchestrators synthesize.

**Fact-check before the lead.** When the panel returns, the process orchestrator checks the load-bearing claims that name no check, in the brief or in a panelist's argument, before the lead sees them. A wrong fact inside one lens reads as a position, and the other lenses argue with it instead of checking it. A check names its instrument, and the instrument must answer the claim: `git log -S` counts occurrences, so it cannot show when a line was last edited (`-G` can). Evidence that lands after the panel ran goes to the lead and synthesis labelled *the panel did not see this*.

**One question is standing, whoever leads: what should be deleted rather than maintained?** Put it in every brief. It is Clara's lens, but Clara synthesizes rather than argues, so on a technical or infrastructure huddle it never enters the room, and a panel asked only what to build will answer only what to build. The candidate proposed in Step 1 is not the only thing on the table; the code already carrying the problem is too.

### Step 4: Find the Tensions

After personas argue, identify:
- Where do they agree? (high-confidence signals)
- Where do they disagree? (genuine trade-offs)
- What are the irreconcilable tensions? (requires a decision, not more analysis)
- What did they name for deletion? (a deletion is a decision: record it, or it gets re-proposed as new work next quarter)

### Step 5: Synthesize

Clara (curatorial orchestrator) synthesizes; Claude records. Don't average the opinions. Find the approach that survives all selected lenses. If no single approach satisfies all, surface the dissent and the irreconcilable trade-off explicitly, and recommend which lens to prioritize for THIS decision; the domain owner's call is decisive in-lane. Synthesis that smooths disagreement into consensus is the failure mode; a huddle that agreed too easily did not huddle.

### Step 6: Record

Save the decision and rationale to the relevant project doc. Future sessions should find this decision, not re-derive it. Consider `/pb-adr` for architecture-level decisions.

**If the decision overrides something the user explicitly agreed** (an order, a list, a scope), state the deviation to the user before acting on it. The panel's ruling can be right and still not be the user's agreement.

---

## Output Format

```
## Huddle: [question]

### Roles
Lead: [persona] -- [why this lane leads]. Orchestrators: Clara (curatorial) + Claude (process). Panel: [list].

### Context loaded
[list of files read]

### [Persona 1]
[2-4 paragraphs, from their lens]

### [Persona 2]
[2-4 paragraphs, from their lens]

### [Persona 3]
[2-4 paragraphs, from their lens]

### Fact-check
[claims checked; any that failed, and whose]

### Lead: [persona]
[rebuttal and close, in-lane, on the panel's output and the fact-check]

### Tensions
- [where they agree]
- [where they disagree]
- [irreconcilable trade-offs]

### Synthesis
[the recommended approach, with rationale from each lens]

### Decision
[one paragraph: what we're doing and why]

### Recorded to
[which file was updated with this decision]
```

---

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Run huddle on routine decisions | Use direct review (Linus, voice pass) |
| Lead anchors the round or overrules cross-lane | Lead rebuts and closes in-lane; panel challenges in parallel; Clara arbitrates across lanes |
| All personas agree too easily | Generate the best counterargument before synthesizing |
| Average the opinions | Find the approach that survives all lenses |
| Huddle without loaded context | Read all relevant state files first |
| Ask the panel to generate from a blank page | Hand it a concrete proposal to break |
| Skip recording the decision | Write it to the project doc immediately |
| Re-huddle the same question unchanged | Read the previous decision and build on it |
| Run full huddle for a refined follow-up question | Use re-huddle mode (`--re-huddle`): reuse personas, skip context reloading |
| Use huddle as a delay tactic | If you're stalling, just do the work |

---

## Examples

```
/pb-huddle "Should we refactor the auth module before adding OAuth support?"
/pb-huddle "How do we communicate this breaking API change to existing clients?"
/pb-huddle "Do we optimize for developer experience or runtime performance in the SDK?"
/pb-huddle --re-huddle "Given we picked DX over perf, how should we measure the trade-off?"
/pb-huddle "re-huddle: Given we picked DX over perf, how should we measure the trade-off?"
```

---

## Related Commands

- `/pb-think` - Structured problem decomposition (solo reasoning)
- `/pb-preamble` - Collaboration philosophy (challenge assumptions)
- `/pb-clara-curator` - Curator and huddle orchestrator (the synthesis seat)
- `/pb-maya-product` - Product and user strategy persona
- `/pb-adr` - Architecture Decision Records (for recording decisions)

---

*Huddle is for decisions that affect trajectory, not tasks that need execution. After the huddle, do the work.*
