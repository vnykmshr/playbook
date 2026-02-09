#!/usr/bin/env python3
"""
Remove tags from metadata (currently noisy, same 8 tags on 80+ commands).

Tags will be added back in a future pass with per-command curation.

Usage:
    python3 scripts/cleanup-tags.py
"""

import re
from pathlib import Path


def remove_tags_from_metadata(content: str) -> str:
    """Remove tags line from YAML front-matter."""
    # Match the tags line (can span multiple lines with array syntax)
    pattern = r'^tags:\s*\[.*?\]\s*\n'
    return re.sub(pattern, '', content, flags=re.MULTILINE)


def main():
    root = Path(__file__).parent.parent
    commands_dir = root / "commands"

    count = 0
    for filepath in sorted(commands_dir.glob("**/pb-*.md")):
        with open(filepath) as f:
            content = f.read()

        # Check if it has tags
        if re.search(r'^tags:', content, re.MULTILINE):
            updated_content = remove_tags_from_metadata(content)

            with open(filepath, 'w') as f:
                f.write(updated_content)

            print(f"✅ {filepath.name}")
            count += 1

    print(f"\n✅ Removed tags from {count} commands.\n")


if __name__ == "__main__":
    main()
