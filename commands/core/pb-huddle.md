---
name: "pb-huddle"
title: "Multi-Perspective Decision Session"
category: "core"
difficulty: "intermediate"
model_hint: "opus"
execution_pattern: "parallel-then-sequential"
related_commands: ['pb-think', 'pb-preamble', 'pb-linus-agent', 'pb-maya-product', 'pb-adr']
last_reviewed: "2026-03-24"
last_evolved: ""
version: "1.0.0"
version_notes: "Initial: multi-persona decision framework with persona selection guide."
breaking_changes: []
---
# Multi-Perspective Decision Session

Multi-persona thinking session for strategic decisions. Not a review gate -- a collaborative exploration where personas argue, disagree, and find the approach that survives scrutiny.

Use `/pb-think` for structured problem decomposition. Huddle is for decisions where relationships, timing, and perception matter as much as correctness.

**Resource Hint:** opus -- Complex multi-persona reasoning, tension synthesis, strategic judgment.

---

## Mindset

Apply `/pb-preamble` thinking: best ideas win regardless of source. Personas should genuinely disagree -- forced consensus defeats the purpose. Apply `/pb-design-rules` thinking: distrust "one true way" (that's why we run multiple lenses), fail noisily (surface irreconcilable tensions, don't paper over them).

---

## When to Use

- Before strategic decisions that affect relationships or positioning
- When there are genuine trade-offs with no obvious answer
- When gut instinct needs stress-testing
- When pacing, framing, or sequencing matters as much as content

**Do NOT use for:** routine code review, simple go/no-go decisions, or when the answer is obvious. Use `/pb-linus-agent` for technical review, `/pb-voice` for writing quality. Huddle is for strategy.

---

## Procedure

### Step 1: Frame the Question

Before framing, search previous decisions for this topic. Don't re-derive what was already decided -- build on it.

State the question clearly. Not "what should we do?" but the specific tension:
- "Should we refactor the auth module before adding OAuth support?"
- "How do we communicate this breaking API change to existing clients?"
- "Do we optimize for developer experience or runtime performance in the SDK?"

The question must have genuine tension -- if there's an obvious answer, skip the huddle.

### Step 2: Load Context

Read relevant state files. The huddle is only as good as the context loaded. Personas can't argue well without knowing the situation.

If no relevant context exists for this question, spend five minutes writing it first. A context-free huddle is worse than no huddle.

### Step 3: Select and Run Personas

Pick 3-4 personas whose lenses match the decision's dimensions. Each persona gets the SAME brief. Disagreement is expected and valuable.

**Selection guide:**

| Decision type | Recommended personas |
|---------------|---------------------|
| Technical trade-off | Linus + Jordan + Alex |
| External-facing (launch, comms) | Kai + Maya + Sam |
| Architecture / system design | Linus + Alex + Jordan |
| Strategic positioning | Kai + Maya + Linus |
| Quality / reliability concern | Jordan + Linus + Sam |
| Documentation / clarity | Sam + Maya + Kai |

**Available personas:** `/pb-linus-agent`, `/pb-jordan-testing`, `/pb-kai-reach`, `/pb-maya-product`, `/pb-sam-documentation`, `/pb-alex-infra`

Run personas in parallel when possible. Give each equal treatment -- don't let the first response anchor the others. Claude plays the synthesis role, not another persona.

### Step 4: Find the Tensions

After personas argue, identify:
- Where do they agree? (high-confidence signals)
- Where do they disagree? (genuine trade-offs)
- What are the irreconcilable tensions? (requires a decision, not more analysis)

### Step 5: Synthesize

Don't average the opinions. Find the approach that survives all selected lenses. If no single approach satisfies all, state the trade-off explicitly and recommend which lens to prioritize for THIS decision.

### Step 6: Record

Save the decision and rationale to the relevant project doc. Future sessions should find this decision, not re-derive it. Consider `/pb-adr` for architecture-level decisions.

---

## Output Format

```
## Huddle: [question]

### Context loaded
[list of files read]

### [Persona 1]
[2-4 paragraphs, from their lens]

### [Persona 2]
[2-4 paragraphs, from their lens]

### [Persona 3]
[2-4 paragraphs, from their lens]

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
| Let one persona dominate | Force all selected lenses, even when one feels "right" |
| All personas agree too easily | Generate the best counterargument before synthesizing |
| Average the opinions | Find the approach that survives all lenses |
| Huddle without loaded context | Read all relevant state files first |
| Skip recording the decision | Write it to the project doc immediately |
| Re-huddle the same question | Read the previous decision and build on it |
| Use huddle as a delay tactic | If you're stalling, just do the work |

---

## Examples

```
/pb-huddle "Should we refactor the auth module before adding OAuth support?"
/pb-huddle "How do we communicate this breaking API change to existing clients?"
/pb-huddle "Do we optimize for developer experience or runtime performance in the SDK?"
```

---

## Related Commands

- `/pb-think` -- Structured problem decomposition (solo reasoning)
- `/pb-preamble` -- Collaboration philosophy (challenge assumptions)
- `/pb-linus-agent` -- Technical peer review persona
- `/pb-maya-product` -- Product and org dynamics persona
- `/pb-adr` -- Architecture Decision Records (for recording decisions)

---

*Huddle is for decisions that affect trajectory, not tasks that need execution. After the huddle, do the work.*
