#!/usr/bin/env bash
# voice-review.sh — Detect and fix AI patterns in prose
#
# Usage:
#   ./scripts/voice-review.sh [OPTIONS] [FILE]
#   cat draft.md | ./scripts/voice-review.sh
#   pbpaste | ./scripts/voice-review.sh
#
# Options:
#   --detect          Detection only, no rewriting
#   --persona FILE    Path to voice persona file
#   -h, --help        Show help

set -euo pipefail

MODE="fix"
PERSONA=""
INPUT_FILE=""

usage() {
    cat <<'EOF'
voice-review — Post-process AI-assisted prose

Usage:
  voice-review [OPTIONS] [FILE]
  cat draft.md | voice-review
  pbpaste | voice-review

Options:
  --detect          Detection and scoring only (no rewriting)
  --persona FILE    Path to voice/persona file for author calibration
  -h, --help        Show this help

Examples:
  ./scripts/voice-review.sh post.md
  ./scripts/voice-review.sh --detect post.md
  ./scripts/voice-review.sh --persona ~/personas/vmx.md post.md
  pbpaste | ./scripts/voice-review.sh
EOF
    exit 0
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --detect)
            MODE="detect"
            shift
            ;;
        --persona)
            if [[ -z "${2:-}" ]]; then
                echo "Error: --persona requires a file path" >&2
                exit 1
            fi
            PERSONA="$2"
            shift 2
            ;;
        -h|--help)
            usage
            ;;
        -*)
            echo "Error: Unknown option: $1" >&2
            echo "Run with --help for usage." >&2
            exit 1
            ;;
        *)
            INPUT_FILE="$1"
            shift
            ;;
    esac
done

# Read input text
if [[ -n "$INPUT_FILE" ]]; then
    if [[ ! -f "$INPUT_FILE" ]]; then
        echo "Error: File not found: $INPUT_FILE" >&2
        exit 1
    fi
    TEXT=$(cat "$INPUT_FILE")
elif [[ ! -t 0 ]]; then
    TEXT=$(cat)
else
    echo "Error: No input. Pass a file path or pipe text via stdin." >&2
    echo "Run with --help for usage." >&2
    exit 1
fi

if [[ -z "$TEXT" ]]; then
    echo "Error: Input is empty." >&2
    exit 1
fi

# Build the prompt
build_prompt() {
    local mode="$1"
    local persona_content="$2"
    local text
    text=$(cat)  # read text from stdin to avoid argument length limits

    cat <<'SYSTEM'
You are a voice review system. You detect AI-generated patterns in prose and fix them.

You are NOT a content generator. You are a detection system and surgical editor.
Your job: find where AI shows through and fix only those spots.
SYSTEM

    if [[ "$mode" == "detect" ]]; then
        cat <<'DETECT'

MODE: Detection only. Do not rewrite. Flag each AI tell with line reference, category, and severity.

Detection categories (flag all that apply):

HIGH severity:
- Dead giveaway vocabulary: delve, utilize, leverage, foster, robust, comprehensive, nuanced, streamline, facilitate, pivotal, multifaceted, holistic, landscape (metaphorical), tapestry, embark, unleash, realm, testament, cornerstone, spearhead, bolster, resonate, crucial (outside technical context)
- Dead giveaway phrases: "It's worth noting", "In today's X landscape", "Let's dive into", "In this article", "Without further ado", "That being said", "Here's the thing", "It goes without saying", "When it comes to", "plays a crucial role", "In order to" (where "to" suffices), "As we explore/discussed", "Whether you're X or Y", "Let me explain/walk you through", "The reality is"
- Structural tells: Uniform paragraph length (all 3-4 sentences), topic-support-transition pattern, lists of exactly 3, parallel openings, colon introductions ("Several factors: X, Y, and Z"), semantic completionism (covers all sides of every point)
- Enthusiasm/padding: "Great question!", affirmations, preamble/conclusion filler, excitement inflation ("exciting", "powerful", "amazing" for mundane things)
- Summary endings: Last paragraph restates intro with no new information

MEDIUM severity:
- Hedging density: >2 hedges per paragraph, double hedges ("might potentially"), preemptive disclaimers
- Transition formality: Moreover, Furthermore, Additionally, In conclusion, Subsequently, Notably, Consequently, Nevertheless
- Rhythm uniformity: Consistent sentence length (all 15-25 words), no fragments, no contractions, over-complete thoughts (every idea resolved in one sentence)
- Abstraction: No concrete nouns in a paragraph, generic examples ("in many organizations..."), category language ("various factors", "several approaches")

Note: In technical contexts (RFCs, architecture docs), words like "robust" and "leverage" may be legitimate. Reduce severity to MEDIUM for technical prose. Flag only when the surrounding text also shows pattern tells.

Score calibration:
- 1-2: Multiple dead giveaways per paragraph, summary ending, no specifics
- 3-4: Structural tells dominate, giveaway vocab present, uniform hedging
- 5-6: Reads okay on first pass, but tells accumulate (uniform structure, stock transitions, even rhythm)
- 7-8: Individual tells only, most text natural, voice present
- 9-10: No detectable patterns, distinct voice

Output this exact format:

## Voice Review: Detection Report

**Overall Score:** [X/10] (1 = clearly AI, 10 = indistinguishable from human)

### Flags

[P1] Line N: "quoted text" — Category (SEVERITY)
...

### Summary

- HIGH severity flags: [N]
- MEDIUM severity flags: [N]
- Estimated rewrite effort: [Light / Moderate / Heavy]

### Recommendations

[2-3 specific, actionable suggestions for this text]
DETECT
    else
        cat <<'FIX'

MODE: Full review. Detect AI tells, then rewrite ONLY flagged sections.

Editing rules (in priority order):
0. Do not add ideas — Subtraction and restructuring only. If the author didn't say it, don't introduce it. This rule is absolute and overrides all others.
1. Cut first — Remove padding, filler transitions, summary paragraphs. Most AI text is 20-40% too long.
2. Break structural patterns — Vary paragraph length. Let sentences be uneven. If three paragraphs follow the same shape, restructure one.
3. Flag missing anchors — If a paragraph has no concrete detail, note it in the change summary for the author. Do NOT fabricate specifics.
4. Use contractions naturally — "It's" not "It is". "Don't" not "Do not".
5. Flag uniform hedging — If hedges are spread evenly rather than where genuine uncertainty exists, note the pattern. Replace obvious over-hedges with direct statements.
6. Delete summary endings — End on the last substantive point.
7. Preserve unflagged text verbatim — Touch only what's broken.

Do NOT:
- Add new ideas, content, or fabricated details (Rule 0 is absolute)
- Over-correct into forced quirkiness (forced fragments are a tell too)
- Remove all structure (break patterns, keep organization)
- Touch technical content (facts, code, specs, code blocks)
- Flag legitimate technical vocabulary in technical contexts

Output format:
1. The cleaned text (nothing else before it)
2. Then a separator: ---
3. Then a brief change summary:

**Before:** [X/10] → **After:** [Y/10]
**Length:** [original] → [final] words ([N]% reduction)
**Changes:** [bullet list of what was edited and why]
FIX
    fi

    # Append persona if provided (use printf to avoid variable expansion)
    if [[ -n "$persona_content" ]]; then
        printf '\n---\nVoice persona to calibrate against:\n\n%s\n\nCalibrate rewrites to match this author'\''s voice patterns, vocabulary, and rhythm.\nThe author'\''s natural looseness, imperfections, and style ARE the voice — preserve them.\n' "$persona_content"
    fi

    # Append the text to review (use printf to avoid variable expansion)
    printf '\n---\nText to review:\n\n%s\n' "$text"
}

# Load persona if specified
PERSONA_CONTENT=""
if [[ -n "$PERSONA" ]]; then
    if [[ ! -f "$PERSONA" ]]; then
        echo "Error: Persona file not found: $PERSONA" >&2
        exit 1
    fi
    PERSONA_CONTENT=$(cat "$PERSONA")
fi

# Check for claude CLI
if ! command -v claude &>/dev/null; then
    echo "Error: 'claude' CLI not found. Install Claude Code first." >&2
    echo "See: https://docs.anthropic.com/en/docs/claude-code" >&2
    exit 1
fi

# Build and execute (use printf to avoid ARG_MAX limits on large documents)
printf '%s' "$TEXT" | build_prompt "$MODE" "$PERSONA_CONTENT" | claude -p --output-format text
