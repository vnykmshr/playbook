#!/bin/bash
# External Action Gate -- PreToolUse hook on Bash.
# A match prints permissionDecision "ask" and exits 0: Claude Code shows a permission
# prompt, in auto mode too. Exit 2 would mean deny (hard block), and exit 0 with only
# stderr does nothing -- see code.claude.com/docs/en/hooks, PreToolUse decision control.
# Patterns are ERE matched anywhere in the command line, so a mention after a space or
# separator asks even inside quotes. A quote or backslash right before the command word
# does not (sh -c "git push"). tests/test_gate_hook.py lists the shapes it misses.

uninspected() {
  printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"ask","permissionDecisionReason":"external-action-gate: %s, command not inspected"}}\n' "$1"
  exit 0
}

command -v jq >/dev/null || uninspected "jq missing"
COMMAND=$(jq -r '.tool_input.command // empty' 2>/dev/null) || uninspected "input not parsed"
[ -z "$COMMAND" ] && exit 0

S='[[:space:]]'
B='(^|[;&|(`$[:space:]])'                                        # command boundary
GIT="${B}git(${S}+(-[Cc]${S}+[^[:space:]]+|--[a-z-]+(=[^[:space:]]+)?))*${S}+"  # git + global opts (-C, -c, --git-dir=...)

# label|regex -- every matching label is reported.
RULES=(
  "git push|${GIT}push([^[:alnum:]_-]|$)"
  "git send-pack|${GIT}send-pack([^[:alnum:]_-]|$)"
  "git reset --hard|${GIT}reset${S}(.*${S})?--hard"
  "git checkout -- .|${GIT}checkout${S}+--${S}+\."
  "git clean -f|${GIT}clean${S}(.*${S})?-[[:alpha:]]*f"
  "gh pr/issue write|${B}gh${S}+(pr|issue)${S}+(create|merge|close|reopen|comment|review|edit)"
  "gh release write|${B}gh${S}+release${S}+(create|edit|delete|upload)"
  "gh repo write|${B}gh${S}+repo${S}+(create|delete|edit|rename|archive)"
  "gh workflow run|${B}gh${S}+(workflow${S}+run|run${S}+rerun)"
  "gh api write method|${B}gh${S}+api${S}.*(-X|--method)(${S}+|=)?(POST|PUT|PATCH|DELETE)"
  "gh api with fields (defaults to POST)|${B}gh${S}+api${S}.*${S}(-f|-F|--field|--raw-field|--input)(${S}|=|$)"
  "publish|${B}(npm${S}+publish|docker${S}+push|cargo${S}+publish|twine${S}+upload)"
  "worker deploy|worker:deploy|${B}wrangler(@[^[:space:]]+)?${S}(.*${S})?(deploy|publish)(${S}|$)"
  "rm -rf|${B}rm${S}+(-[[:alpha:]]+${S}+)*-[[:alpha:]]*(r[[:alpha:]]*f|f[[:alpha:]]*r)"
  "rm -r -f|${B}rm${S}+(-[[:alpha:]]+${S}+)*-[rR]${S}+(-[[:alpha:]]+${S}+)*-f"
)

matched=()
for rule in "${RULES[@]}"; do
  label=${rule%%|*}
  re=${rule#*|}
  [[ "$COMMAND" =~ $re ]] && matched+=("$label")
done

[ ${#matched[@]} -eq 0 ] && exit 0

labels=$(printf '%s; ' "${matched[@]}")
jq -n --arg r "external-action-gate: ${labels%; } -- needs your explicit go" \
  '{hookSpecificOutput: {hookEventName: "PreToolUse", permissionDecision: "ask", permissionDecisionReason: $r}}'
exit 0
