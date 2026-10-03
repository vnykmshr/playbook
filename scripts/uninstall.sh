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

# Physical path, so links made through a symlinked repo path still match.
COMMANDS_PHYS="$(cd "$COMMANDS_DIR" && pwd -P)"

# Track uninstall stats
removed=0
skipped=0
not_found=0

# Find all .md files in commands/ and remove their symlinks
while IFS= read -r file; do
    filename=$(basename "$file")
    target="$TARGET_DIR/$filename"

    if [ -L "$target" ]; then
        # Ours = the link's directory resolves into the repo. realpath is avoided: older
        # macOS lacks it, and a failing substitution aborts the loop under set -e.
        link_dir=$(cd "$TARGET_DIR" && cd "$(dirname "$(readlink "$target")")" 2>/dev/null && pwd -P) || link_dir=""
        case "$link_dir/" in
            "$COMMANDS_PHYS"/*) ;;
            *)
                echo "  ⚠ Skipped: $filename (symlink not owned by this repo)"
                skipped=$((skipped + 1))
                continue
                ;;
        esac
        rm -f "$target"
        echo "  ✓ Removed: $filename"
        removed=$((removed + 1))
    elif [ -e "$target" ]; then
        echo "  ⚠ Skipped: $filename (existing file, not symlink)"
        skipped=$((skipped + 1))
    else
        not_found=$((not_found + 1))
    fi
done < <(find "$COMMANDS_DIR" -name "*.md" -type f | sort)

echo ""
echo "Uninstall Summary:"
echo "  Removed: $removed"
echo "  Skipped: $skipped (same-named, not ours -- still installed)"
echo "  Not found: $not_found"
echo ""
echo "Uninstall complete!"
