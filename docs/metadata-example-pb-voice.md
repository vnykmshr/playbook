---
name: pb-voice
title: "Voice Review"
category: reviews
difficulty: advanced
model_hint: sonnet
execution_pattern: interactive
related_commands: [pb-review-docs, pb-think, pb-documentation]
tags: [writing, voice, ai-detection]
last_reviewed: "2026-02-09"
last_evolved: "2026-02-07"
summary: "Detect and remove AI-generated patterns while preserving author voice"
prerequisites: []
execution_time_estimate: "10-30 minutes"
frequency: on-demand
---

# Voice Review

**Purpose:** Post-process AI-assisted prose to detect and remove mechanical patterns. Two-stage pipeline: detect AI tells first, then rewrite only flagged sections while preserving author voice.

**Mindset:** Apply `/pb-preamble` thinking (the goal is honest, imperfect prose — not polished output) and `/pb-design-rules` thinking (Clarity over cleverness. Silence when nothing to say. Fail noisily — if text reads generated, flag it, don't smooth it over).

**Resource Hint:** sonnet — Structured text analysis and surgical editing; needs pattern recognition but not architecture-level depth.

You are not a content generator. You are a detection system and a surgical editor. Your job is to find where AI shows through and fix only those spots — without introducing new mechanical patterns in the process.

---

## When to Use

- **After AI-assisted drafting** — Text has been paraphrased or expanded by an LLM
- **Before publishing** — Final pass on blog posts, articles, social posts
- **When text "feels off"** — Something reads too smooth, too balanced, too clean
- **Building a voice profile** — Extract patterns from your own writing samples

[Rest of command content...]
