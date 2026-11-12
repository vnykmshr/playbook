---
name: "pb-huddle"
title: "Multi-Perspective Decision Session"
category: "core"
difficulty: "intermediate"
model_hint: "opus"
execution_pattern: "parallel-then-sequential"
related_commands: ['pb-think', 'pb-preamble', 'pb-clara-curator', 'pb-maya-product', 'pb-adr']
last_reviewed: "2026-11-12"
version: "1.10.0"
version_notes: "v1.10.0: The brief carries the ask verbatim and constraints from the project's instructions, with what the public may see during a visibility move; persona prompts name the review; a panel that agrees, its opposition seat included, seats one against the agreement; agreement is not a check, and a run cannot verify 'only', 'never' or 'always'. A panelist reads its persona file from disk; a persona's model hint is its standalone default; a persona file has three modes; the output has one section per panelist; the Examples block is gone."
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
/pb-huddle --quick "question"     → Quick: inline, the lead plus two lenses, same steps and output
```

**Quick** fits a question one lane owns with one cross-lane risk. It skips the agents, not the steps: the brief, the fact-check and the record still run.

**Natural-language trigger:** `"re-huddle: new focus question"` also invokes re-huddle mode. The flag and the prefix are equivalent; use whichever reads more naturally.

---

### Re-Huddle Mode

When a huddle's synthesis identifies a refined follow-up question, run a re-huddle instead of a full huddle. It reuses the persona set and context from the prior huddle, focusing only on the new question.

**When to use:**
- The prior huddle surfaced a refined question worth deeper exploration
- The same personas should weigh in on the follow-up
- The context hasn't changed (same files)

**What changes:**
- **Skip context loading** (Step 2): personas already have the background from the prior huddle
- **Still write the brief and findings file** (Step 2's write): the next round, or fresh agents, read them from disk
- **Shorter persona prompts**: reference the prior huddle output instead of re-loading raw context
- **Keep framing** (Step 1): the refined question still needs clear framing; it's a different question from the original

**What stays the same:**
- Full huddle output format (persona arguments, tensions, synthesis, decision, recording)
- Steps 3-6 run identically to standard mode

**Guardrails:**
- **Agents gone** (a new session, `/clear`, a usage limit): spawn fresh agents with the brief and the prior round's findings file, both on disk (Step 2). Re-run only the voices whose results are missing.
- **Fall back to full huddle** if the prior huddle output can't be found or persona names can't be extracted. If in doubt, ask which personas to use.

**Late evidence against a closed ruling** reopens it by re-huddle, with the evidence as the new question. It is never folded into the record quietly.

**How it works:**
1. Read the most recent huddle output: the recorded findings file (Step 2), or the conversation while the panel is in it
2. Extract the persona names used
3. Frame the new question (Step 1)
4. Run personas with abbreviated prompts that reference the prior output (Step 3). If the panel ran as agents that are still addressable, message those same agents (in Claude Code, `SendMessage` to each agent) rather than spawning new ones: each keeps the brief and its own argument, so the follow-up costs one message per lens. Name any file changed since spawn and tell the agent to `cat` it: a resumed agent holds spawn-time state, not disk. One follow-up per agent: past that, a resumed agent carries every round in its context, so spawn fresh ones from the brief and findings files
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

The brief you write is a claim too. Each fact in it names how it was checked: the command run or the file opened, marked measured or inferred. A fact with no check is labelled unverified, and every "unverified" is resolved or carried into the decision before the close. Ask panelists to mark the same; "stated from reading, not run" gets them to run things. The brief also states:
- what the artifact under review is for, and where anything distilled from elsewhere came from;
- the user's ask, verbatim, which each lens answers as stated before narrowing it;
- the hard constraints (visibility, host, budget, identity or privacy), gathered from the user and the project's instructions before any option: constraints that arrive one at a time void the options built before them. For a move in visibility or hosting, include what the public may see while it changes (pushes, tags, DNS);
- for a change to an interface, its callers (one grep);
- your own list of what you suspect you missed;
- the question as coverage ("does it handle all N things it was built for?"), not go/no-go; and that the answer may sit outside the options offered.

Write the brief to disk, and each round's findings to a file beside it, so the panel can be re-briefed from files rather than memory.

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

Name the lead by the decision's center of gravity and record it ("Lead: Tavis, trust-boundary decision"). The user can override. When the topic genuinely is the whole (scope, lifecycle, coherence), Clara is both orchestrator and lead, and Claude stays the second, neutral orchestrator to keep her honest.

**Lead and panel by decision type:**

| Decision type | Lead | Panel |
|---|---|---|
| Technical / architecture | Linus | Jordan + Alex + Tavis |
| Security / trust boundary | Tavis | Linus + Alex |
| Testing / reliability | Jordan | Linus + Alex |
| Infrastructure / resilience | Alex | Jordan + Linus |
| Product / user value | Maya | Sam + Kai + Elena |
| Design / UX / brand | Elena | Maya + Sam |
| Distribution / launch | Kai | Maya + Sam |
| Documentation / clarity | Sam | Maya + Elena |
| Scope / lifecycle / coherence | Clara | Maya + Linus |

**Roster (9):** `/pb-linus-agent`, `/pb-tavis-security`, `/pb-jordan-testing`, `/pb-alex-infra`, `/pb-maya-product`, `/pb-elena-design`, `/pb-kai-reach`, `/pb-sam-documentation`, `/pb-clara-curator`.

Each persona gets the SAME brief; disagreement is expected and valuable. Name the round (review or cycle) in each persona's prompt, not only the brief: a lens that does not know it defers items to the round it is in. Run the panel in parallel so the first response doesn't anchor the others, as separate agents when the ruling binds. Each panelist's prompt names its persona file and tells the agent to read it from disk: an agent spawned mid-session can hold an earlier copy. A persona's `model_hint` is its default when run alone; on a panel, panelists run on sonnet and the lead and synthesis on opus, and the brief records any seat raised. The lead rebuts and closes in its lane; the orchestrators synthesize.

**One file, three modes.** A persona file is used three ways: a full review (the file on a diff, alone), a lens (its Lens Mode, inline while the work is done, three observations at most), and a panel seat (the file plus the brief, argued in lane; the three-observation cap is the lens's alone). The lane, the routes and the evidence it owes are the same in all three; only the depth changes.

**Seats:**
- **Opposition.** When the proposal has an obvious overreach (a cut, a rewrite, minimalism winning unopposed), one lens is assigned the opposite position. A panel that agrees easily, its opposition seat included, seats one after the fact against what it agreed on, before synthesis.
- **Fresh eyes.** A huddle reviewing work seats at least one panelist who did not plan it.

**Fact-check before the lead.** When the panel returns, the process orchestrator checks the load-bearing claims that name no check, in the brief or in a panelist's argument, before the lead sees them; agreement among lenses is not a check. A wrong fact inside one lens reads as a position, and the other lenses argue with it instead of checking it. A check names its instrument, and the instrument must answer the claim: `git log -S` counts occurrences, so it cannot show when a line was last edited (`-G` can). A run shows one path, so it cannot verify "only", "never" or "always": read every path. Evidence that lands after the panel ran goes to the lead and synthesis labelled *the panel did not see this*. A panelist who finds a live defect reports it as a finding; argued as rhetoric, the best-argued room walks past the bug. The lead gets the panelists' verbatim text, not a paraphrase.

**Fact-check the close too.** Agents see the state as of their spawn, so re-read disk first, then check the lead's close for its claims and for what it leaves out. A command the close rules (a filter, a conflict resolution, a script) is code: dry-run it and diff the result against the untouched base, never against the output of the same filter.

**One question is standing, whoever leads: what should be deleted rather than maintained?** Put it in every brief. A deletion owes the same evidence as any other finding: the concrete failure it removes. It is Clara's lens, but Clara synthesizes rather than argues, so on a technical or infrastructure huddle it never enters the room, and a panel asked only what to build will answer only what to build. The candidate proposed in Step 1 is not the only thing on the table; the code already carrying the problem is too.

### Step 4: Find the Tensions

After personas argue, put every finding in one counted bucket (agreed, disputed, deleted, dropped) and report the counts. Then identify:
- Where do they agree? (high-confidence signals)
- Where do they disagree? (genuine trade-offs)
- What are the irreconcilable tensions? (requires a decision, not more analysis; "key off X, not Y" often resolves as both)
- What did they name for deletion? (a deletion is a decision: record it, or it gets re-proposed as new work next quarter)

### Step 5: Synthesize

Clara (curatorial orchestrator) synthesizes; Claude records. Don't average the opinions. Find the approach that survives all selected lenses. If no single approach satisfies all, surface the dissent and the irreconcilable trade-off explicitly, and recommend which lens to prioritize for THIS decision; the domain owner's call is decisive in-lane. Synthesis that smooths disagreement into consensus is the failure mode; a huddle that agreed too easily did not huddle.

### Step 6: Record

After the close, never before it, save the decision and rationale to the relevant project doc. Future sessions should find this decision, not re-derive it. Consider `/pb-adr` for architecture-level decisions.

**If the decision overrides something the user explicitly agreed** (an order, a list, a scope, approved copy), or removes something reachable (a URL, a command) because nothing shows it is used, hold it for the user and state the deviation before acting on it. The panel's ruling can be right and still not be the user's agreement.

---

## Output Format

```
## Huddle: [question]

### Roles
Lead: [persona] -- [why this lane leads]. Orchestrators: Clara (curatorial) + Claude (process). Panel: [list].

### Context loaded
[list of files read]

### [Panelist]
[one section per panelist: 2-4 paragraphs, from its lane]

### Fact-check
[claims checked; any that failed, and whose]

### Lead: [persona]
[rebuttal and close, in-lane, on the panel's output and the fact-check]

### Tensions
- Counts: agreed N, disputed N, deleted N, dropped N
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
| Average the opinions | Find the approach that survives all lenses |
| Huddle without loaded context | Read all relevant state files first |
| Ask the panel to generate from a blank page | Hand it a concrete proposal to break |
| Skip recording the decision | Write it to the project doc immediately |
| Re-huddle the same question unchanged | Read the previous decision and build on it |
| Run full huddle for a refined follow-up question | Use re-huddle mode (`--re-huddle`): reuse personas, skip context reloading |
| Use huddle as a delay tactic | If you're stalling, just do the work |

---

## Related Commands

- `/pb-think` - Structured problem decomposition (solo reasoning)
- `/pb-preamble` - Collaboration philosophy (challenge assumptions)
- `/pb-clara-curator` - Curator and huddle orchestrator (the synthesis seat)
- `/pb-maya-product` - Product and user strategy persona
- `/pb-adr` - Architecture Decision Records (for recording decisions)
