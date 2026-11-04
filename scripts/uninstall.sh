#!/bin/bash

# Engineering Playbook Uninstaller
# Removes the command, skill and DX script links install.sh made

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
COMMANDS_DIR="$REPO_DIR/commands"
TARGET_DIR="$HOME/.claude/commands"
# shellcheck source-path=SCRIPTDIR source=lib/link-owner.sh
source "$SCRIPT_DIR/lib/link-owner.sh"

echo "Engineering Playbook Uninstaller"
echo "================================"
echo ""

# Validate commands directory exists
if [ ! -d "$COMMANDS_DIR" ]; then
    echo "Error: Commands directory not found at $COMMANDS_DIR"
    exit 1
fi

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
        if ! link_owned_by "$target" "$COMMANDS_PHYS" 2; then
            echo "  ⚠ Skipped: $filename (symlink not owned by this repo)"
            skipped=$((skipped + 1))
            continue
        fi
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

# Skill and DX script links, when they point into this repo
SKILLS_DIR="$REPO_DIR/skills"
if [ -d "$SKILLS_DIR" ]; then
    SKILLS_PHYS="$(cd "$SKILLS_DIR" && pwd -P)"
    for link in "$HOME/.claude/skills"/*; do
        if [ -L "$link" ] && link_owned_by "$link" "$SKILLS_PHYS" 1; then
            rm -f "$link"
            echo "  ✓ Removed: ~/.claude/skills/$(basename "$link")"
            removed=$((removed + 1))
        fi
    done
fi
SCRIPTS_PHYS="$(cd "$SCRIPT_DIR" && pwd -P)"
for script in context-bar.sh check-context.sh; do
    link="$HOME/.claude/$script"
    if [ -L "$link" ] && link_owned_by "$link" "$SCRIPTS_PHYS" 1; then
        rm -f "$link"
        echo "  ✓ Removed: ~/.claude/$script"
        removed=$((removed + 1))
    fi
done

echo ""
echo "Uninstall Summary:"
echo "  Removed: $removed"
echo "  Skipped: $skipped (same-named, not ours; still installed)"
echo "  Not found: $not_found"
echo ""
echo "Left in place: ~/.claude/hooks/external-action-gate.sh (a copy) and its settings.json"
echo "entry. Removing the copy alone leaves settings.json calling a missing hook; remove both"
echo "by hand to turn the gate off."
