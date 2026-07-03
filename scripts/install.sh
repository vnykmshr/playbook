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

# Validate commands directory exists
if [ ! -d "$COMMANDS_DIR" ]; then
    echo "Error: Commands directory not found at $COMMANDS_DIR"
    exit 1
fi

# Create target directory if it doesn't exist
mkdir -p "$TARGET_DIR"

# Count commands
command_count=$(find "$COMMANDS_DIR" -name "*.md" -type f | wc -l)
if [ "$command_count" -eq 0 ]; then
    echo "Error: No command files (.md) found in $COMMANDS_DIR"
    exit 1
fi

echo "Found $command_count commands to install"
echo ""

# Track installation stats
installed=0
replaced=0
failed=0

# Find all .md files in commands/ and symlink them
while IFS= read -r file; do
    filename=$(basename "$file")
    target="$TARGET_DIR/$filename"

    # Check if file/symlink already exists
    if [ -e "$target" ] || [ -L "$target" ]; then
        if [ -L "$target" ]; then
            echo "  → Replaced: $filename"
            replaced=$((replaced + 1))
        else
            echo "  ⚠ Skipped: $filename (existing file, not symlink)"
            failed=$((failed + 1))
            continue
        fi
        rm -f "$target"
    else
        echo "  ✓ Installed: $filename"
        installed=$((installed + 1))
    fi

    # Create symlink
    if ! ln -s "$file" "$target"; then
        echo "  ✗ Failed: $filename (symlink creation failed)"
        failed=$((failed + 1))
    fi
done < <(find "$COMMANDS_DIR" -name "*.md" -type f | sort)

echo ""
echo "Installation Summary:"
echo "  Installed: $installed"
echo "  Replaced:  $replaced"
echo "  Failed:    $failed"
echo ""
echo "Commands available in: $TARGET_DIR"

# --- Skills: executable compound commands with workflows ---
SKILLS_DIR="$REPO_DIR/skills"
SKILLS_TARGET="$HOME/.claude/skills"

if [ -d "$SKILLS_DIR" ]; then
    skill_count=$(find "$SKILLS_DIR" -name "SKILL.md" -type f | wc -l | tr -d ' ')
    echo ""
    echo "Installing $skill_count skill(s)..."

    while IFS= read -r skill_md; do
        skill_name=$(basename "$(dirname "$skill_md")")
        target_dir="$SKILLS_TARGET/$skill_name"

        # Remove old symlink or directory
        if [ -L "$target_dir" ] || [ -d "$target_dir" ]; then
            rm -rf "$target_dir"
        fi

        mkdir -p "$(dirname "$target_dir")"
        ln -sfn "$(dirname "$skill_md")" "$target_dir"
        echo "  ✓ Installed: ~/.claude/skills/$skill_name"
    done < <(find "$SKILLS_DIR" -name "SKILL.md" -type f | sort)

    # Create project-local symlink if running inside the playbook repo
    local_link="$REPO_DIR/.claude/skills"
    if [ -d "$REPO_DIR/.claude" ] && [ ! -e "$local_link" ]; then
        ln -sfn "$SKILLS_DIR" "$local_link"
        echo "  ✓ Linked: .claude/skills → skills/"
    fi
fi

# --- DX Scripts: context bar + context hook ---
SCRIPTS_DIR="$REPO_DIR/scripts"
CLAUDE_HOME="$HOME/.claude"

for script in context-bar.sh check-context.sh; do
    src="$SCRIPTS_DIR/$script"
    dest="$CLAUDE_HOME/$script"
    if [ -f "$src" ]; then
        ln -sf "$src" "$dest"
        echo "  ✓ Linked: ~/.claude/$script"
    fi
done

echo ""
echo "Quick start:"
echo "  /pb-start    - Begin development work"
echo "  /pb-review   - Automatic quality gate"
echo "  /pb-pr       - Create a pull request"
echo "  /pb-release  - Prepare and deploy release"
