# Hook Patterns

Hooks automate enforcement of development practices by triggering actions on Claude Code tool events. This directory provides pattern documentation and minimal examples — adapt them to your workflow.

---

## What Are Hooks?

Claude Code hooks are shell commands or scripts that execute automatically when specific events occur during a session. They enable:

- **Enforcement** — Block or warn before problematic actions
- **Automation** — Format code, run checks after edits
- **Continuity** — Save/restore session state across compaction

---

## Hook Lifecycles

| Lifecycle | When It Fires | Common Use Cases |
|-----------|---------------|------------------|
| **PreToolUse** | Before a tool executes | Block dangerous operations, remind about practices |
| **PostToolUse** | After a tool completes | Validate output, format code, run checks |
| **PreCompact** | Before context compaction | Save session state, persist important context |
| **SessionStart** | When a new session begins | Load previous context, restore state |
| **Stop** | When session ends | Final cleanup, persist learnings |

---

## Configuration

Hooks are configured in `~/.claude/settings.json` under the `hooks` key:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "your-command-here"
          }
        ]
      }
    ]
  }
}
```

### Matcher Patterns

- `"Edit"` — Match specific tool
- `"Edit|Write"` — Match multiple tools (OR)
- `"*"` — Match all tools

### Hook Types

- `"type": "command"` — Execute shell command
- The command receives the event as JSON on stdin (`tool_name`, `tool_input`); `external-action-gate.sh` reads it with `jq`

---

## Installation

The install script does not wire hooks into `settings.json`. They require manual setup:

1. Adapt a hook to your workflow and environment
2. Add it to your `~/.claude/settings.json`
3. Test it by piping a sample event: `echo '{"tool_input":{"command":"git push"}}' | bash hook.sh`

**Why manual?** Hooks interact with your shell environment and may need project-specific paths. Copy-and-adapt is safer than auto-install.

### External action gate

`external-action-gate.sh` is the one hook shipped ready to use. On a Bash command that pushes, merges, releases, publishes, deploys or deletes, it makes Claude Code show a permission prompt (auto mode included). `scripts/install.sh` copies it to `~/.claude/hooks/` (a copy, so checking out an old tag cannot remove the live gate). An existing copy that matches a committed version of the hook is replaced, so re-running install updates it. A copy that matches none is your edit and is skipped: diff it, move it aside, re-run. You wire it yourself:

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{ "type": "command", "command": "bash ~/.claude/hooks/external-action-gate.sh" }]
    }]
  }
}
```

It needs `jq`; without it, every Bash command asks. It catches known command shapes, not intent: quoting, `sh -c`, wrapper scripts, raw HTTP and non-Bash tools pass it. `tests/test_gate_hook.py` lists each known miss.

---

## Best Practices

### Do

- Keep hooks fast (they run synchronously)
- Use hooks for enforcement, not complex logic
- Log hook actions for debugging
- Test hooks in isolation before adding to settings

### Avoid

- Blocking hooks that take more than a few seconds
- Complex scripts that may fail silently
- Hooks that modify files without user awareness
- Over-automation that hides what the assistant is doing

---

## Debugging Hooks

If hooks aren't working:

1. **Check syntax** — Validate JSON in settings.json
2. **Test command** — Run the command manually in terminal
3. **Check matcher** — Ensure tool name matches exactly
4. **Review logs** — Add echo statements to trace execution

---

## Official Documentation

For comprehensive hook documentation, environment variables, and advanced patterns:

- Claude Code documentation (check for latest hooks reference)
- `claude --help` for CLI options

---

## Related Commands

- `/pb-resume` — Session continuity guidance (uses PreCompact, SessionStart patterns)
- `/pb-standards` — Principles that hooks can enforce
- `/pb-review-code` — Review practices that PostToolUse can validate

---

*Hooks enforce what playbooks teach. Use them to automate discipline, not replace judgment.*
