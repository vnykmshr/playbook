---
name: "pb-voice"
title: "Voice Review"
category: "reviews"
difficulty: "advanced"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-think', 'pb-review-docs', 'pb-documentation', 'pb-design-rules', 'pb-preamble']
last_reviewed: "2026-02-09"
last_evolved: ""
version: "1.0.0"
version_notes: "v2.10.0 baseline"
breaking_changes: []
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

---

## Pipeline Overview

```
Input → DETECT → annotated flags → REWRITE (flagged only) → VERIFY → output
```

Three stages when used interactively via `/pb-voice`. Run `mode=detect` first for visibility, then `mode=fix` on flagged sections. The CLI script (`voice-review.sh`) runs a single-pass for convenience — use `--detect` first if you want the full pipeline.

### Modes

| Mode | What It Does | When to Use |
|------|-------------|-------------|
| `detect` | Flag AI patterns, score text, no changes | Quick audit, learning your tells |
| `fix` (default) | Detect + rewrite flagged sections only | Standard post-processing |
| `profile` | Analyze sample writing to build voice reference | One-time setup or periodic refresh |

**Usage:**

- `/pb-voice` — Full detect + fix on provided text or file
- `/pb-voice mode=detect` — Detection and scoring only
- `/pb-voice mode=profile` — Build voice profile from samples
- `/pb-voice persona=/path/to/persona.md` — Calibrate to author voice

---

## Stage 1: Detect

Scan text for AI-generated patterns. Flag each occurrence with category and severity. Do not fix anything in this stage.

### Category 1: Dead Giveaway Vocabulary (HIGH)

Words and phrases that almost never appear in natural writing but are statistically overrepresented in LLM output.

**Words:** delve, utilize, leverage, foster, robust, comprehensive, nuanced, streamline, facilitate, underscores, pivotal, multifaceted, holistic, synergy, paradigm, ecosystem (outside tech), landscape (metaphorical), tapestry, intricate, embark, unleash, realm, testament, cornerstone, spearhead, bolster, resonate, proliferate, aligns, crucial (outside technical context)

**Phrases:**

- "It's worth noting that..."
- "It's important to note..."
- "It's crucial/essential to..."
- "In today's [X] landscape..."
- "Let's dive into..."
- "Let me explain/walk you through..."
- "At the end of the day..."
- "This is a game-changer"
- "Take it to the next level"
- "Moving forward"
- "In this article, we will..."
- "Without further ado"
- "Here's the thing"
- "That being said"
- "It goes without saying"
- "Stands as a testament to"
- "When it comes to..."
- "Plays a crucial role"
- "In order to" (where "to" suffices)
- "As we explore/discussed..."
- "Whether you're [X] or [Y]..."
- "The reality is..."
- "By doing [X], you can [Y]..."

**Note:** In technical contexts (RFCs, architecture docs), words like "robust" and "leverage" may be legitimate. Reduce severity to MEDIUM when surrounding text is also technical.

**Action:** Flag every occurrence. Replace or delete.

### Category 2: Structural Tells (HIGH)

Patterns in organization that reveal algorithmic generation.

- **Uniform paragraph length** — Every paragraph 3-4 sentences. Real writing has 1-sentence paragraphs next to 6-sentence ones.
- **Topic-support-transition** — Each paragraph opens with topic sentence, supports it, transitions. Textbook structure. Real writing meanders.
- **Lists of exactly 3** — AI loves triplets. "Three key considerations..." Real lists are 2, or 4, or 7.
- **Symmetrical sections** — All H2s same length. All bullets identical grammar.
- **Colon introductions** — "Several factors to consider: X, Y, and Z." AI's favorite sentence.
- **Parallel openings** — Consecutive paragraphs starting the same way ("This approach...", "This method...", "This strategy...").

**Action:** Restructure. Make one paragraph a fragment. Make another twice as long. Break the template.

### Category 3: Hedging Density (MEDIUM)

AI hedges constantly to avoid being wrong. Humans hedge strategically — only when genuinely uncertain.

- More than 2 hedges per paragraph: "may," "might," "could potentially," "it's possible that"
- Qualifying needlessly: "This can be useful" vs "This is useful"
- Double hedges: "might potentially," "could possibly," "may help to some extent"
- Preemptive disclaimers: "While this isn't always the case..."

**Action:** Replace one hedge per paragraph with a direct statement. Keep hedges only where real uncertainty exists.

### Category 4: Transition Formality (MEDIUM)

Stock transitions humans rarely use in professional writing.

**Flag:** Moreover, Furthermore, Additionally, In conclusion, To summarize, That said, Having established, It is worth mentioning, Consequently, Subsequently, Notably, Importantly, Interestingly, Conversely, Nevertheless, Notwithstanding

**Action:** Delete most. If connection needed, use "But," "And," "So," "Still" — or restructure.

### Category 5: Enthusiasm and Padding (HIGH)

AI is trained helpful and positive. This creates distinctive filler.

- **Affirmations:** "Great question!", "Absolutely!", "That's a fantastic approach"
- **Preamble:** "I'd be happy to help with that," "Let me break this down"
- **Conclusion padding:** "I hope this helps!", "Feel free to ask"
- **Excitement inflation:** "exciting," "powerful," "amazing" for mundane things

**Action:** Delete entirely. Zero information content.

### Category 6: Rhythm and Cadence (MEDIUM)

AI produces unnaturally even rhythm.

- **Consistent sentence length** — Every sentence 15-25 words. No short punches. No long sprawls.
- **Clean clause structure** — Subject-verb-object, consistently. No interruptions or asides.
- **No fragments** — AI almost never writes incomplete sentences. Humans do it constantly.
- **No contractions** — "It is" instead of "it's." "Do not" instead of "don't."
- **Over-complete thoughts** — Every idea fully resolved in one sentence. No trailing thoughts.

**Action:** Vary length deliberately. Let a thought stand incomplete rather than forcing it to resolve. Contract where natural. Let a thought trail off.

### Category 7: Abstraction Level (MEDIUM)

AI defaults to conceptual language. Humans anchor in specifics.

- **No concrete nouns** — Paragraph has no numbers, names, tools, dates, or places
- **Generic examples** — "For instance, in many organizations..." instead of naming one
- **Conceptual hand-waving** — "Improves efficiency" without saying how much or for whom
- **Category language** — "Various factors," "multiple considerations," "several approaches"

**Action:** One concrete anchor per paragraph. A number, tool, date, name, or constraint from lived experience.

### Category 8: Summary Endings (HIGH)

The most reliable AI tell. LLMs almost always end with a summary paragraph restating what was already said.

- "In summary, ..."
- "To conclude, ..."
- "Overall, ..."
- Final paragraph adds no new information
- Restatement of the opening thesis

**Action:** Delete the summary paragraph. End on the last substantive point. Unresolved endings, open questions, abrupt stops — all fine.

### Detection Output Format

Score calibration:

| Score | Description |
|-------|-------------|
| 1-2 | Multiple dead giveaways per paragraph, summary ending, no specifics |
| 3-4 | Structural tells dominate, some giveaway vocab, uniform hedging |
| 5-6 | Reads okay on first pass, but pattern tells accumulate — uniform structure, stock transitions, even rhythm |
| 7-8 | Individual tells only, most text is natural, voice present |
| 9-10 | No detectable patterns, distinct voice, could not be flagged by a reader |

```
## Voice Review: Detection Report

**Overall Score:** [X/10] (1 = clearly AI, 10 = indistinguishable from human)

### Flags

[P1] Line 3: "delve into the nuanced landscape" — Dead giveaway vocabulary (HIGH)
[P2] Lines 7-9: Uniform 3-sentence paragraphs — Structural tell (HIGH)
[P3] Line 12: "It's worth noting that" — Dead giveaway phrase (HIGH)
[P4] Line 15: "may potentially help" — Double hedge (MEDIUM)
[P5] Lines 22-24: Summary paragraph restating opening — Summary ending (HIGH)

### Summary

- HIGH severity flags: [N]
- MEDIUM severity flags: [N]
- Estimated rewrite effort: [Light / Moderate / Heavy]

### Recommendations

[2-3 specific suggestions for this text]
```

---

## Stage 2: Rewrite

Fix only flagged sections. Preserve everything else verbatim.

### Editing Rules

**Rule 0: Do not add ideas.** Subtraction and restructuring only. If the author didn't say it, don't introduce it.

**Rule 1: Cut first.** Most AI text is 20-40% longer than needed. Removing padding, filler transitions, and summary paragraphs is the highest-leverage edit. If cutting a sentence loses no meaning, cut it.

**Rule 2: Reclaim author phrasing.** If the original draft had a rougher but more genuine phrase, prefer it. The AI "improved" it by making it generic.

**Rule 3: Break structural patterns.** If three consecutive paragraphs follow the same shape, restructure one. Make a paragraph a single sentence. Let another run long.

**Rule 4: Flag missing anchors.** If a paragraph has no concrete detail (number, tool, date, name), flag it for the author to fix. Do not fabricate specifics — only the author has lived experience to draw from.

**Rule 5: Vary rhythm.** Short sentence. Then a longer one that takes its time. Fragment. Back to medium.

**Rule 6: Flag uniform hedging.** If hedges are distributed evenly rather than concentrated where genuine uncertainty exists, flag the pattern. Let the author decide which hedges to strengthen into direct statements.

**Rule 7: Contractions are natural.** "It's" not "It is." "Don't" not "Do not." Unless formality is specifically required.

**Rule 8: Kill the ending.** If the last paragraph is a summary, delete it. End on the last point that adds information.

### Voice Profile Integration

When a persona file is provided, calibrate rewrites to match the author's documented voice.

1. **Read the persona** — Extract sentence patterns, vocabulary, punctuation habits, tone markers
2. **Identify signatures** — What makes this author recognizable? Comma-connected thoughts? Programming metaphors? Trailing endings?
3. **Apply during rewrite** — Match the author's patterns, not generic "human" patterns
4. **Preserve looseness** — If the voice is informal and unpolished, don't tighten. The looseness is the voice.

If no persona provided, apply general human-voice heuristics without author-specific calibration.

### What NOT to Do

| Don't | Why |
|-------|-----|
| Rewrite unflagged sections | Introduces new mechanical patterns |
| Add content | You're an editor, not a writer |
| Over-correct into "quirky" | Forced imperfection is as detectable as AI smoothness |
| Remove all structure | Break patterns, don't eliminate organization |
| Add slang unless the voice is genuinely informal | Unnatural informality is a tell too |
| Touch technical content | Facts, code, specs — leave alone |

---

## Stage 3: Verify

After rewriting, validate the output.

### Checks

1. **Re-score** — Run detection on rewritten text. Score should improve by at least 2 points.
2. **Diff review** — Show what changed. Author sees exactly which sentences were touched and why.
3. **Read-aloud test** — Would the author say this to a colleague? If it sounds like a press release, it failed.
4. **Meaning preservation** — Every claim in the original survives in the output.
5. **Length check** — Output should be shorter than input (typically 10-30% shorter). Longer means something went wrong.

### Verification Output

```
## Voice Review: Verification

**Before:** [X/10] → **After:** [Y/10] (+[N] points)

**Edits Made:**
- Removed [N] dead giveaway terms
- Broke [N] structural patterns
- Deleted summary ending
- Added [N] concrete anchors
- Varied sentence length in paragraphs [X, Y]

**Length:** [original] → [final] words ([N]% reduction)
**Remaining flags:** [any unresolved items and why kept]
```

---

## Quick Reference: AI Tell Lexicon

### Instant Tells (remove on sight)

| Tell | Example | Fix |
|------|---------|-----|
| "Delve" | "Let's delve into..." | Delete or rephrase |
| "Landscape" | "In today's tech landscape" | Name the specific context |
| "Leverage" (verb) | "Leverage this approach" | "Use" |
| "Utilize" | "Utilize the framework" | "Use" |
| "Robust" | "A robust solution" | Say what makes it strong |
| "Comprehensive" | "A comprehensive guide" | Name what it covers |
| "Nuanced" | "A nuanced approach" | Name the actual nuances |
| "Streamline" | "Streamline the process" | "Speed up" or "simplify" |
| Summary paragraph | Last graf restates intro | Delete entirely |
| "In this article" | "We will explore..." | Delete, start with content |

### Pattern Tells (restructure when detected)

| Tell | Fix |
|------|-----|
| Uniform paragraphs (all 3-4 sentences) | Vary: 1-sentence, 5-sentence, fragment |
| Lists of exactly 3 | Make it 2 or 4. Or don't list. |
| Parallel openings | Rewrite one paragraph's opening |
| No contractions | Contract naturally |
| No fragments | Add one where it fits |
| Even sentence length | Short punch (3-5 words) and long sprawl (30+) |

### Subtle Tells (address when accumulation is high)

| Tell | Fix |
|------|-----|
| Over-hedging (>2 per paragraph) | Replace one with direct statement |
| Stock transitions | "But," "And," "So" — or delete |
| No concrete nouns in paragraph | Add a number, tool, date, or name |
| Clean endings on every section | Let one end on a question or trailing thought |

---

## CLI Script

A companion script at `scripts/voice-review.sh` provides terminal access outside Claude Code sessions.

```bash
# Review a file
./scripts/voice-review.sh post.md

# Detection only
./scripts/voice-review.sh --detect post.md

# With persona
./scripts/voice-review.sh --persona ~/personas/vmx.md post.md

# From clipboard (macOS)
pbpaste | ./scripts/voice-review.sh

# From stdin
cat draft.md | ./scripts/voice-review.sh
```

See `scripts/voice-review.sh` for implementation details.

---

## Examples

### Example 1: Blog Post Opening

**Input:**

```
In today's rapidly evolving tech landscape, developers are increasingly
leveraging AI tools to streamline their workflows. It's worth noting that
while these tools offer comprehensive capabilities, they may not always
align with individual coding styles. In this article, we'll delve into
practical strategies for maintaining your unique voice while utilizing
AI assistance effectively.
```

**Detection:** Score 2/10. Eight HIGH flags — dead giveaway vocabulary saturates every sentence.

**Output:**

```
I've been using AI tools for most of my writing this past year. They're
fast. They're also making everything sound the same. Grammar gets better,
sure, but my posts read like a committee wrote them.
```

Score: 2/10 → 8/10. Shorter. Specific. Has a voice.

### Example 2: Technical Paragraph

**Input:**

```
When implementing microservices architecture, it is essential to consider
several key factors. First, service boundaries should be carefully defined
to ensure proper separation of concerns. Second, inter-service communication
patterns must be robust and resilient. Third, monitoring and observability
should be comprehensive to facilitate troubleshooting.
```

**Detection:** Score 3/10. "Robust," "comprehensive," list-of-3 structure, no contractions, no concrete detail.

**Output (with persona):**

```
Microservices get messy at the boundaries. Where one service ends and
another begins — that's where most teams burn months. We got this wrong
twice before settling on domain events as the contract. Monitoring matters
too, but get the boundaries right first.
```

Score: 3/10 → 8/10. Concrete experience, opinionated, uneven structure.

---

## Voice Profile: Building One

When running `mode=profile`, provide 5-10 samples of writing you're satisfied with. The system extracts:

| Dimension | What It Captures |
|-----------|-----------------|
| **Sentence patterns** | Average length, variance, fragment frequency |
| **Vocabulary** | Words you use naturally, words you never use |
| **Punctuation** | Comma habits, dash usage, parenthetical frequency |
| **Paragraph shape** | Length range, length variance |
| **Openings** | How you start paragraphs and pieces |
| **Closings** | How you end — trailing thoughts, abrupt stops, questions |
| **Tone markers** | Formality level, humor, directness |
| **Contractions** | Frequency and which ones |
| **Specificity** | How concrete your references are |

The profile becomes a calibration reference that detection and rewrite stages use to target *your* voice, not generic "human."

---

## Anti-Patterns

| Anti-Pattern | Problem | Do Instead |
|--------------|---------|------------|
| Rewriting everything | New mechanical patterns | Fix only flagged sections |
| Forcing quirky fragments | Detectable as fake-casual | Imperfections only where natural |
| Removing all structure | Unreadable | Break patterns, keep organization |
| Single-pass detect+fix | No visibility into changes | Separate the stages |
| Ignoring author voice | Generic "human" isn't specific enough | Use persona when available |
| Over-shortening | Losing meaning | Cut padding, keep substance |
| Fixing subtle tells first | Low impact | Fix HIGH severity first |

---

## Related Commands

- `/pb-think` — General thinking toolkit; use `mode=refine` for output refinement
- `/pb-review-docs` — Documentation quality review (structural, not voice)
- `/pb-documentation` — Writing engineering documentation
- `/pb-design-rules` — Clarity over cleverness applies to prose
- `/pb-preamble` — Honest, direct communication philosophy

---

**Last Updated:** 2026-02-09
**Version:** 1.0.0
