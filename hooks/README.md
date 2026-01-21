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
- Command receives context via environment variables

---

## Example Patterns

See `examples/patterns.json` for minimal templates. These are **patterns to adapt**, not production-ready configs.

### Pattern 1: Console.log Detection (PostToolUse)

Warn when edited files contain debug statements:

```json
{
  "PostToolUse": [{
    "matcher": "Edit|Write",
    "hooks": [{
      "type": "command",
      "command": "grep -l 'console.log' \"$CLAUDE_FILE_PATH\" 2>/dev/null && echo '[WARN] console.log detected in edited file'"
    }]
  }]
}
```

### Pattern 2: Long-Running Command Reminder (PreToolUse)

Remind to use tmux for commands that may run long:

```json
{
  "PreToolUse": [{
    "matcher": "Bash",
    "hooks": [{
      "type": "command",
      "command": "echo \"$CLAUDE_COMMAND\" | grep -qE '(npm install|cargo build|pytest|make)' && echo '[TIP] Consider running in tmux for long commands'"
    }]
  }]
}
```

### Pattern 3: Session State Preservation (PreCompact)

Save context before compaction:

```json
{
  "PreCompact": [{
    "matcher": "*",
    "hooks": [{
      "type": "command",
      "command": "echo \"[$(date)] Compaction triggered\" >> ~/.claude/compaction-log.txt"
    }]
  }]
}
```

---

## Installation

Hooks are **not auto-installed** by the playbook install script. They require manual setup:

1. Review patterns in `examples/patterns.json`
2. Adapt to your workflow and environment
3. Add to your `~/.claude/settings.json`
4. Test with a sample session

**Why manual?** Hooks interact with your shell environment and may need project-specific paths. Copy-and-adapt is safer than auto-install.

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
- Over-automation that hides what Claude is doing

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
