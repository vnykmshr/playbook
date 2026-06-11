#!/bin/bash
# Advisory context usage hook for Claude Code.
# Fires on Stop events. Warns when context usage is high.
# Never blocks — just advises.
#
# 80%: Gentle reminder to consider /pb-pause
# 90%: Stronger suggestion to /compact or /pb-pause
#
# Install: symlink to ~/.claude/check-context.sh via ./scripts/install.sh
# Configure in ~/.claude/settings.json under hooks.Stop

input=$(cat)

# Prevent infinite loops from stop hook re-triggering
stop_hook_active=$(echo "$input" | jq -r '.stop_hook_active // false' 2>/dev/null)
if [[ "$stop_hook_active" == "true" ]]; then
  exit 0
fi

transcript_path=$(echo "$input" | jq -r '.transcript_path // empty' 2>/dev/null)
if [[ -z "$transcript_path" || ! -f "$transcript_path" ]]; then
  exit 0
fi

# The Stop hook payload carries no context_window (status-line-only), so read the
# real window cached by context-bar.sh; a usage-based fallback is applied below.
max_context=$(cat "$HOME/.claude/.context-window" 2>/dev/null)

# Get token count from the last assistant message with usage data
context_length=$(tail -200 "$transcript_path" \
  | jq -s '
    map(select(.type == "assistant" and .message.usage)) |
    last // {} |
    if .message.usage then
      (.message.usage.input_tokens // 0) +
      (.message.usage.cache_read_input_tokens // 0) +
      (.message.usage.cache_creation_input_tokens // 0)
    else 0 end
  ' 2>/dev/null) || context_length=0

if ! [[ "$context_length" =~ ^[0-9]+$ ]] || [[ "$context_length" -eq 0 ]]; then
  exit 0
fi

# No cached window yet? Infer what's certain: exceeding 200K is only possible on
# the 1M window. Below 200K, assume the 200K default.
if ! [[ "$max_context" =~ ^[0-9]+$ && "$max_context" -gt 0 ]]; then
  if [[ "$context_length" -gt 200000 ]]; then max_context=1000000; else max_context=200000; fi
fi

pct=$((context_length * 100 / max_context))

if [[ $pct -ge 90 ]]; then
  echo "Context at ${pct}%. Run /pb-pause to save state, then /compact or start a fresh session."
elif [[ $pct -ge 80 ]]; then
  echo "Context at ${pct}%. Consider /pb-pause soon to preserve state before compaction."
fi
