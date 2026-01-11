#!/bin/bash

# Engineering Playbook Uninstaller
# Removes symlinks from ~/.claude/commands/

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
COMMANDS_DIR="$REPO_DIR/commands"
TARGET_DIR="$HOME/.claude/commands"

echo "Engineering Playbook Uninstaller"
echo "================================"
echo ""

# Find all .md files in commands/ and remove their symlinks
find "$COMMANDS_DIR" -name "*.md" -type f | while read -r file; do
    filename=$(basename "$file")
    target="$TARGET_DIR/$filename"

    if [ -L "$target" ]; then
        rm -f "$target"
        echo "  Removed: $filename"
    fi
done

echo ""
echo "Uninstall complete!"
