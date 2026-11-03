#!/bin/bash
# External Action Gate -- PreToolUse hook on Bash.
# A match prints permissionDecision "ask" and exits 0: Claude Code shows a permission
# prompt, in auto mode too. Exit 2 would mean deny (hard block), and exit 0 with only
# stderr does nothing -- see code.claude.com/docs/en/hooks, PreToolUse decision control.
# Patterns are EREs, matched case-insensitively anywhere in the command line, so a mention
# after a space, slash or separator asks even inside quotes. A quote or backslash right
# before the command word does not (sh -c "git push"). tests/test_gate_hook.py lists the
# shapes it misses.

uninspected() {
  printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"ask","permissionDecisionReason":"external-action-gate: %s, command not inspected"}}\n' "$1"
  exit 0
}

command -v jq >/dev/null || uninspected "jq missing"
COMMAND=$(jq -r '.tool_input.command // empty' 2>/dev/null) || uninspected "input not parsed"
[ -z "$COMMAND" ] && exit 0

S='[[:space:]]'
B='(^|[;&|(`$[:space:]/])'                                       # command boundary; / catches /usr/bin/git
GIT="${B}git(${S}+(-[Cc]${S}+[^[:space:]]+|-[[:alpha:]]|--[a-z-]+(=[^[:space:]]+|${S}+[^-[:space:]][^[:space:]]*)?))*${S}+"  # git + global opts
GH="${B}gh(${S}+(-R|--repo)(${S}+|=)[^[:space:]]+)*${S}+"        # gh + -R/--repo
shopt -s nocasematch                                             # GIT runs git on a case-insensitive filesystem

# label|regex -- every matching label is reported.
RULES=(
  "git push|${GIT}push([^[:alnum:]_-]|$)"
  "git send-pack|${GIT}send-pack([^[:alnum:]_-]|$)"
  "git reset --hard|${GIT}reset${S}(.*${S})?--hard"
  "git checkout/restore .|${GIT}(checkout(${S}+--)?|restore)${S}+\."
  "git clean -f|${GIT}clean${S}(.*${S})?(-[[:alpha:]]*f|--force)"
  "gh pr/issue write|${GH}(pr|issue)${S}+(create|merge|close|reopen|comment|review|edit|delete|transfer)"
  "gh release write|${GH}release${S}+(create|edit|delete|upload)"
  "gh repo write|${GH}repo${S}+(create|delete|edit|rename|archive)"
  "gh workflow run|${GH}(workflow${S}+run|run${S}+rerun)"
  "gh api write method|${GH}api${S}.*(-X|--method)(${S}+|=)?(POST|PUT|PATCH|DELETE)"
  "gh api with fields (defaults to POST)|${GH}api${S}.*${S}(-f|-F|--field|--raw-field|--input)(${S}|=|$)"
  "publish|${B}((p?npm|yarn)${S}+publish|docker${S}+push|cargo${S}+publish|twine${S}+upload)"
  "worker deploy|worker:deploy|${B}wrangler(@[^[:space:]]+)?${S}(.*${S})?(deploy|publish)(${S}|$)"
  "rm -r|${B}rm(${S}+[^;&|[:space:]]+)*${S}+(-[[:alpha:]]*[rR][[:alpha:]]*|--recursive)(${S}|$)"
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
