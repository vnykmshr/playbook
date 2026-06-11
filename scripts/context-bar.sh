#!/bin/bash
# Context bar for Claude Code status line.
# Shows: branch | uncommitted | model | turns | token usage bar
# Install: symlink to ~/.claude/context-bar.sh via ./scripts/install.sh

# Claude Code pipes the status-line JSON payload on stdin.
input=$(cat 2>/dev/null)

# --- Git info ---
branch=$(git branch --show-current 2>/dev/null) || branch=""
if [[ -n "$branch" ]]; then
  dirty=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
  if [[ "$dirty" -gt 0 ]]; then
    git_info="${branch} ${dirty}m"
  else
    git_info="${branch}"
  fi
else
  git_info=""
fi

# --- Token usage + context window ---
# Authoritative source: the payload's context_window object. context_window_size
# is the REAL window (200000 or 1000000), so 200K vs the 1M tier is correct
# without guessing -- the [1m] tier is not encoded in the model id, so it can
# never be inferred from the model name. Falls back to the transcript for older
# Claude Code versions that don't emit context_window.
pct=0
context_length=0
max_context=200000
model_name=""
transcript=""
turn_count=0
cw_size=""; cw_used=""; cw_pct=""

if [[ -n "$input" ]]; then
  # One jq call, line-per-field; grouped reads keep empty fields aligned (bash 3.2).
  { IFS= read -r model_name
    IFS= read -r transcript
    IFS= read -r cw_size
    IFS= read -r cw_used
    IFS= read -r cw_pct
  } < <(jq -r '
    (.model.id // ""),
    (.transcript_path // ""),
    (.context_window.context_window_size // ""),
    (.context_window.total_input_tokens // ""),
    (.context_window.used_percentage // "")
  ' <<<"$input" 2>/dev/null)
fi

if [[ "$cw_size" =~ ^[0-9]+$ && "$cw_size" -gt 0 ]]; then
  # Authoritative path.
  max_context="$cw_size"
  [[ "$cw_used" =~ ^[0-9]+$ ]] && context_length="$cw_used"
  pct="${cw_pct%.*}"   # used_percentage is a float; truncate to int
  # Cache the real window for check-context.sh -- the Stop hook's payload does
  # not carry context_window, so it can't learn 200K-vs-1M any other way.
  echo "$max_context" > "$HOME/.claude/.context-window" 2>/dev/null
else
  # Fallback: parse the transcript. The window is not authoritative here, so infer
  # only what's certain -- exceeding 200K is possible solely on the 1M window.
  if [[ -z "$transcript" ]]; then
    project_dir="$HOME/.claude/projects/$(echo "$PWD" | tr '/' '-')"
    [[ -d "$project_dir" ]] && transcript=$(find "$project_dir" -maxdepth 1 -name "*.jsonl" -print0 2>/dev/null \
      | xargs -0 ls -t 2>/dev/null | head -1)
  fi
  if [[ -n "$transcript" && -f "$transcript" ]]; then
    read -r context_length tmodel < <(tail -200 "$transcript" \
      | jq -rs '
        map(select(.type == "assistant" and .message.usage)) | last // {} |
        if .message.usage then
          [((.message.usage.input_tokens // 0) +
            (.message.usage.cache_read_input_tokens // 0) +
            (.message.usage.cache_creation_input_tokens // 0)),
           (.message.model // "")]
        else [0, ""] end | "\(.[0]) \(.[1])"
      ' 2>/dev/null) || { context_length=0; tmodel=""; }
    [[ -z "$model_name" ]] && model_name="$tmodel"
    [[ "$context_length" =~ ^[0-9]+$ ]] || context_length=0
    [[ "$context_length" -gt 200000 ]] && max_context=1000000
    [[ "$context_length" -gt 0 ]] && pct=$((context_length * 100 / max_context))
  fi
fi

# Model tier: single char (O/S/H) from model name
case "$model_name" in
  *opus*)   model_tier="O" ;;
  *sonnet*) model_tier="S" ;;
  *haiku*)  model_tier="H" ;;
  *)        model_tier="" ;;
esac

# Turn count: user messages in the transcript (if known)
if [[ -n "$transcript" && -f "$transcript" ]]; then
  turn_count=$(grep -c '"type":"user"' "$transcript" 2>/dev/null) || turn_count=0
fi

# Sanity guards before arithmetic
[[ "$pct" =~ ^[0-9]+$ ]] || pct=0
[[ "$context_length" =~ ^[0-9]+$ ]] || context_length=0

# --- Progress bar ---
bar_width=10
filled=$((pct * bar_width / 100))
[[ "$filled" -gt "$bar_width" ]] && filled="$bar_width"   # cap if pct somehow >100
empty=$((bar_width - filled))
[[ "$empty" -lt 0 ]] && empty=0

bar=""
[[ "$filled" -gt 0 ]] && bar=$(printf '%0.s█' $(seq 1 "$filled"))
[[ "$empty" -gt 0 ]] && bar+=$(printf '%0.s░' $(seq 1 "$empty"))

# Token count in K
tokens_k=$((context_length / 1000))

# --- Assemble ---
parts=()
[[ -n "$git_info" ]] && parts+=("$git_info")
[[ -n "$model_tier" ]] && parts+=("$model_tier")
[[ "$turn_count" -gt 0 ]] && parts+=("t${turn_count}")
parts+=("${bar} ${pct}% ${tokens_k}k")

echo "${parts[*]}"
