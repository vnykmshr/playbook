#!/bin/bash

# Engineering Playbook Installer
# Symlinks command files to ~/.claude/commands/

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
COMMANDS_DIR="$REPO_DIR/commands"
TARGET_DIR="$HOME/.claude/commands"

echo "Engineering Playbook Installer"
echo "=============================="
echo ""

# Create target directory if it doesn't exist
mkdir -p "$TARGET_DIR"

# Counter for installed commands
count=0

# Find all .md files in commands/ and symlink them
find "$COMMANDS_DIR" -name "*.md" -type f | while read -r file; do
    filename=$(basename "$file")

    # Remove existing file/symlink if present
    if [ -e "$TARGET_DIR/$filename" ] || [ -L "$TARGET_DIR/$filename" ]; then
        rm -f "$TARGET_DIR/$filename"
    fi

    # Create symlink
    ln -s "$file" "$TARGET_DIR/$filename"
    echo "  Linked: $filename"
    ((count++)) || true
done

echo ""
echo "Installation complete!"
echo "Commands available in: $TARGET_DIR"
echo ""
echo "Quick start:"
echo "  /pb-start    - Begin development work"
echo "  /pb-cycle    - Self-review + peer review iteration"
echo "  /pb-pr       - Create a pull request"
echo "  /pb-release  - Prepare and deploy release"
