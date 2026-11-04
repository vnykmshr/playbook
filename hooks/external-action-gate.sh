#!/bin/bash
# External Action Gate -- PreToolUse hook on Bash.
# A match prints permissionDecision "ask" and exits 0: Claude Code shows a permission
# prompt, in auto mode too. Exit 2 would mean deny (hard block), and exit 0 with only
# stderr does nothing -- see code.claude.com/docs/en/hooks, PreToolUse decision control.
# The command is normalised once: backslash-newline joins with a space and the text is
# lowercased, so every pattern is a lowercase ERE. A command word matches anywhere in the
# line, so a mention after a space, slash or separator asks even inside quotes. A quote or
# backslash right before the command word does not (sh -c "git push"). A rule's later
# words must sit in the same command segment: SEG stops at an unquoted ; & | or newline.
# tests/test_gate_hook.py lists the shapes it misses and the ones it asks on wrongly.

uninspected() {
  printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"ask","permissionDecisionReason":"external-action-gate: %s, command not inspected"}}\n' "$1"
  exit 0
}

command -v jq >/dev/null || uninspected "jq missing"
COMMAND=$(jq -er '.tool_input.command' 2>/dev/null) || uninspected "input not parsed"
[ -z "$COMMAND" ] && exit 0
NL=$'\n'
COMMAND=${COMMAND//\\$NL/ }                                         # a space, not "": echo C:\\<nl>rm stays two words
COMMAND=$(printf '%s' "$COMMAND" | tr '[:upper:]' '[:lower:]') || uninspected "normalise failed"  # bash 3.2 has no ${x,,}

S='[[:space:]]'
Q="'"
SEG="([^;&|${NL}${Q}\"]|${Q}[^${Q}]*${Q}|\"[^\"]*\")*"                   # rest of one command segment, quotes kept whole
B='(^|[;&|(`$[:space:]/])'                                       # command boundary; / catches /usr/bin/git
VALOPT='--(git-dir|work-tree|namespace|config-env)'               # git long opts that take a separate value
GIT="${B}git(${S}+(-c${S}+[^[:space:]]+|-[[:alpha:]]|--[a-z-]+(=[^[:space:]]+)?|${VALOPT}${S}+[^[:space:]]+))*${S}+"
GH="${B}gh(${S}+(-r${S}*|--repo(${S}+|=))[^[:space:]]+)*${S}+"   # gh + -R/--repo

# label|regex -- every matching label is reported.
RULES=(
  "git push|${GIT}push([^[:alnum:]_-]|$)"
  "git send-pack|${GIT}send-pack([^[:alnum:]_-]|$)"
  "git reset --hard|${GIT}reset${S}(${SEG}${S})?--hard"
  "git checkout/restore .|${GIT}(checkout|restore)(${S}+--)?${S}+\."
  "git clean -f|${GIT}clean${S}(${SEG}${S})?(-[[:alpha:]]*f|--force)"
  "gh pr/issue write|${GH}(pr|issue)${S}+(create|merge|close|reopen|comment|review|edit|delete|transfer)"
  "gh release write|${GH}release${S}+(create|edit|delete|upload)"
  "gh repo write|${GH}repo${S}+(create|delete|edit|rename|archive)"
  "gh workflow run|${GH}(workflow${S}+run|run${S}+rerun)"
  "gh api write method|${GH}api${S}${SEG}(-x|--method)(${S}+|=)?(post|put|patch|delete)"
  "gh api with fields (defaults to POST)|${GH}api${S}${SEG}${S}(-f|--field|--raw-field|--input)(${S}|=|$)"
  "publish|${B}((p?npm|yarn)${S}+publish|docker${S}+push|cargo${S}+publish|twine${S}+upload)"
  "worker deploy|worker:deploy|${B}wrangler(@[^[:space:]]+)?${S}(${SEG}${S})?(deploy|publish)(${S}|$)"
  "rm -r|${B}rm([[:blank:]]+[^;&|()\`[:space:]]+)*[[:blank:]]+(-[[:alpha:]]*r|--r)"  # --r: GNU takes any prefix of --recursive
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
