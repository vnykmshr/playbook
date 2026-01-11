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

# Validate commands directory exists
if [ ! -d "$COMMANDS_DIR" ]; then
    echo "Error: Commands directory not found at $COMMANDS_DIR"
    exit 1
fi

# Track uninstall stats
removed=0
not_found=0

# Find all .md files in commands/ and remove their symlinks
while IFS= read -r file; do
    filename=$(basename "$file")
    target="$TARGET_DIR/$filename"

    if [ -L "$target" ]; then
        rm -f "$target"
        echo "  ✓ Removed: $filename"
        removed=$((removed + 1))
    elif [ -e "$target" ]; then
        echo "  ⚠ Skipped: $filename (existing file, not symlink)"
        not_found=$((not_found + 1))
    else
        not_found=$((not_found + 1))
    fi
done < <(find "$COMMANDS_DIR" -name "*.md" -type f | sort)

echo ""
echo "Uninstall Summary:"
echo "  Removed: $removed"
echo "  Not found: $not_found"
echo ""
echo "Uninstall complete!"
