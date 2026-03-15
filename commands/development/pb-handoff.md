---
name: "pb-handoff"
title: "Structured Work Handoff"
category: "development"
difficulty: "intermediate"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-start', 'pb-pause', 'pb-plan', 'pb-preamble', 'pb-voice']
last_reviewed: "2026-03-05"
last_evolved: ""
version: "1.0.0"
version_notes: "Initial: universal handoff pattern with acceptance criteria and constraints"
breaking_changes: []
---

# Structured Work Handoff

Transfer work between contexts -- agents, sessions, teammates, or future-you. Creates a self-contained document that initiates work without requiring the original conversation. The receiving context starts building, not re-discovering.

**Resource Hint:** sonnet -- Synthesis, context compression, reasoning preservation.

---

## Mindset

Apply `/pb-preamble` thinking: The receiving context has zero shared history. Every assumption must be made explicit. Reasoning is the payload -- code is easy to re-derive, but the *why* behind decisions is what's hard to reconstruct and easy to lose. Apply `/pb-design-rules` thinking: Clarity over cleverness (the document must stand alone), simplicity (skip sections that have no content), fail noisily (if the handoff is too thin, say so).

---

## When to Use

- **Delegating work to another agent or session** -- Context doesn't transfer automatically
- **Handing off to a teammate** -- They weren't in your head during research
- **Resuming complex work after a long break** -- Future-you doesn't remember the nuances
- **Cross-project work** -- Research in one repo, execution in another

---

## Quality Gate

Before writing a handoff, verify substance exists. A handoff needs at minimum:

- A clear problem, goal, or idea
- At least one of: research findings, design direction, or a well-framed question

If the work is too thin to hand off, say so: "Not enough substance to hand off yet. Discuss further or provide more context." Do not generate a hollow document. A bad handoff is worse than no handoff -- it wastes the receiver's time re-discovering what you should have documented.

---

## Two Speeds

**Directed handoff** -- You know what needs doing. Receiver executes in the right context. Includes specific findings, decisions, and concrete guidance. The Direction section has step-by-step work items.

**Exploratory handoff** -- You're passing an idea, direction, or early research. Receiver owns the investigation, planning, and execution. The Direction section has open questions and loose guidance. Receiver should use `/pb-plan` or `/pb-start` to build the execution plan.

Most handoffs fall somewhere between. Include whatever the source session produced -- detailed steps if they exist, loose direction if not. The receiver adapts.

---

## Document Structure

Save to: `todos/handoff-YYYY-MM-DD-<slug>.md`

The slug comes from the brief description (lowercase, hyphens, 3-5 words max).

Adapt the structure to the content. Skip sections that have no meaningful content. An idea handoff may have no findings. A bug-fix handoff may have no research. Don't manufacture filler to match a template.

```markdown
# Handoff: <brief title>

> From: <source context>, <date>
> For: <target context>
> Type: directed | exploratory

## Motivation

Why this work matters. What triggered it. 1-2 paragraphs max.

## Context

What was researched, explored, or discovered. Include enough detail that
the receiver doesn't need to re-do the research, but not so much that
it's a conversation dump. Link to external resources rather than inlining
them.

## Findings

Key discoveries. Bullet points or short paragraphs. Include code snippets
only when essential for understanding.

## Decisions

Choices already made and why. Format: "Chose X over Y because Z."
The receiver should respect these unless they find a strong reason not to.
For exploratory handoffs, this section may be empty.

## Direction

For directed handoffs: specific guidance, file paths, approach.
For exploratory handoffs: the idea, loose direction, open questions.

### Acceptance Criteria (directed handoffs)

3-5 measurable checkboxes that define "done." Not required for
exploratory handoffs. Required for directed ones.

- [ ] Criterion 1
- [ ] Criterion 2

### Constraints (optional)

Technical, timeline, or resource constraints that shape execution without
limiting direction. Examples: "Must work on Go 1.25+", "Don't introduce
new dependencies", "Timeline: this week."

## Scope

**In scope:** What the receiver should focus on.
**Out of scope:** What to explicitly skip (prevents scope creep).

## References

- Links, file paths, PR/issue URLs (all resolvable from target project)
- Any artifacts created during the source session
```

---

## Writing Rules

**Self-contained.** The receiver has zero conversation context. Never reference the source session as something the receiver can consult. It won't exist.

**Reasoning is the payload.** The *why* behind decisions, not just the *what*. "Chose X over Y because Z" lets the receiver challenge decisions intelligently. "Use X" gives them no basis to evaluate.

**All references must be resolvable.** Use full URLs for external repos, not bare relative paths. File paths must make sense from the target project.

**No template filler.** Every line earns its keep. If a section heading has nothing meaningful under it, drop the section.

**One handoff, one concern.** Don't bundle unrelated work. Two handoffs to the same project is fine.

**Dated, not versioned.** Handoffs are point-in-time artifacts. If the work evolves, write a new handoff, don't update the old one.

**Apply `/pb-voice`.** Organic prose, no em dashes in the template (use -- instead), free-flowing reasoning.

---

## Procedure

### Step 1: Verify substance (quality gate)

Scan the current conversation for substance. If it's too thin, stop and say so.

### Step 2: Determine handoff type

Based on how much has been resolved: directed (approach decided, execution needs context) or exploratory (idea needs investigation with project context).

### Step 3: Synthesize

Review the conversation to extract:
1. What triggered this work
2. Research done
3. Key findings
4. Decisions made (with reasoning)
5. Direction for the receiver
6. References (URLs, file paths, code snippets)

### Step 4: Write the document

Follow the document structure above. For focused tasks (bug fix, small change), use a compact structure. For research-heavy transfers, use the full structure where separation adds clarity.

For directed handoffs, include acceptance criteria -- 3-5 measurable checkboxes. For security work, always include reproduction steps and impact.

### Step 5: Suggest the entry point

After writing, tell the receiver how to start:

```
Handoff written: todos/handoff-YYYY-MM-DD-<slug>.md

Start with:
  Read todos/handoff-YYYY-MM-DD-<slug>.md and execute the next steps.
```

---

## Design Principles

1. **Handoff initiates, receiver decides.** The handoff starts work, it doesn't prescribe every step. The receiver has context the source doesn't. Trust them to make execution decisions.
2. **Self-contained over complete.** Better to link to a 500-line analysis than inline it. The receiver can read files.
3. **Reasoning is the payload.** Code is easy to re-derive. The reasoning behind decisions is what's hard to reconstruct and easy to lose.
4. **Dated, not versioned.** Handoffs are point-in-time artifacts. If the work evolves, write a new handoff.
5. **One handoff, one concern.** Don't bundle unrelated work.
6. **Two speeds.** Detailed when the source has done the thinking, exploratory when the idea needs context to develop. Both are valid.

---

## Related Commands

- `/pb-start` -- Begin work from a handoff (receiver's first step)
- `/pb-pause` -- Preserve context before stepping away (complementary to handoff)
- `/pb-plan` -- Build execution plan from an exploratory handoff
- `/pb-preamble` -- Challenge assumptions (apply to handoff decisions)
- `/pb-voice` -- Apply organic prose style to handoff writing

---

*Context transfers cleanly. Receivers start building, not re-discovering. | v1.0.0*
