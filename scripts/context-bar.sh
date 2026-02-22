#!/bin/bash
# Context bar for Claude Code status line.
# Shows: branch | uncommitted | token usage bar
# Install: symlink to ~/.claude/context-bar.sh via ./scripts/install.sh

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

# --- Token usage from transcript ---
max_context=200000
pct=0
context_length=0

# Derive project directory from CWD (matches Claude Code's path encoding)
claude_dir="$HOME/.claude"
project_dir="${claude_dir}/projects/$(echo "$PWD" | tr '/' '-')"

if [[ -d "$project_dir" ]]; then
  # Find most recent transcript for THIS project only (excludes subagent transcripts)
  transcript=$(find "$project_dir" -maxdepth 1 -name "*.jsonl" -print0 2>/dev/null \
    | xargs -0 ls -t 2>/dev/null | head -1) || transcript=""

  if [[ -n "$transcript" && -f "$transcript" ]]; then
    # Extract token count from last assistant message with usage data.
    # tail -200 covers tool-heavy conversations where assistant messages are sparse.
    context_length=$(tail -200 "$transcript" \
      | jq -s '
        map(select(.type == "assistant" and .message.usage)) |
        last // {} |
        if .message.usage then
          (.message.usage.input_tokens // 0) +
          (.message.usage.cache_read_input_tokens // 0) +
          (.message.usage.cache_creation_input_tokens // 0)
        else 0 end
      ' 2>/dev/null) || context_length=0

    # Validate numeric before arithmetic
    if [[ "$context_length" =~ ^[0-9]+$ && "$context_length" -gt 0 ]]; then
      pct=$((context_length * 100 / max_context))
    fi
  fi
fi

# --- Progress bar ---
bar_width=10
filled=$((pct * bar_width / 100))
empty=$((bar_width - filled))

bar=""
[[ "$filled" -gt 0 ]] && bar=$(printf '%0.s█' $(seq 1 "$filled"))
[[ "$empty" -gt 0 ]] && bar+=$(printf '%0.s░' $(seq 1 "$empty"))

# Token count in K
tokens_k=$((context_length / 1000))

# --- Assemble ---
parts=()
[[ -n "$git_info" ]] && parts+=("$git_info")
parts+=("${bar} ${pct}% ${tokens_k}k")

echo "${parts[*]}"
