#!/usr/bin/env python3
"""
Simple YAML front-matter parser for the metadata subset used in playbooks.

No external dependencies. Handles only the specific YAML format we use in metadata.

Usage:
    python3 scripts/parse-metadata.py  # Parse all commands and print metadata
"""

import re
from pathlib import Path
from collections import defaultdict


def parse_frontmatter(content: str) -> dict:
    """Parse YAML front-matter from command file.

    Handles our specific simple format:
    ---
    name: "value"
    title: "value"
    category: "value"
    related_commands: ['item1', 'item2']
    tags: ['tag1', 'tag2']
    last_reviewed: "2026-02-09"
    last_evolved: ""
    ---

    Returns dict or None if no front-matter found.
    """
    if not content.startswith("---"):
        return None

    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not match:
        return None

    yaml_content = match.group(1)
    metadata = {}

    for line in yaml_content.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        # Parse key: value pairs
        if ':' not in line:
            continue

        key, _, value = line.partition(':')
        key = key.strip()
        value = value.strip()

        # Handle arrays
        if value.startswith('[') and value.endswith(']'):
            # Parse array: ['item1', 'item2']
            items_str = value[1:-1]  # Remove brackets
            items = []
            for item in items_str.split(','):
                item = item.strip()
                if item.startswith("'") and item.endswith("'"):
                    items.append(item[1:-1])
                elif item.startswith('"') and item.endswith('"'):
                    items.append(item[1:-1])
            metadata[key] = items
        # Handle strings
        elif value.startswith('"') and value.endswith('"'):
            metadata[key] = value[1:-1]
        elif value.startswith("'") and value.endswith("'"):
            metadata[key] = value[1:-1]
        else:
            # Bare value
            metadata[key] = value

    return metadata


def load_all_metadata():
    """Load metadata from all command files."""
    root = Path(__file__).parent.parent
    commands_dir = root / "commands"
    all_metadata = {}

    for filepath in sorted(commands_dir.glob("**/pb-*.md")):
        with open(filepath) as f:
            content = f.read()

        meta = parse_frontmatter(content)
        if meta:
            all_metadata[filepath.name] = {
                "path": filepath,
                "metadata": meta
            }

    return all_metadata


def print_metadata_table(all_metadata: dict):
    """Print metadata in table format."""
    print("\n" + "="*100)
    print(f"{'Command':<35} {'Category':<15} {'Difficulty':<12} {'Model':<8} {'Exec':<12}")
    print("="*100)

    for filename in sorted(all_metadata.keys()):
        item = all_metadata[filename]
        meta = item["metadata"]
        name = meta.get("name", "?")
        category = meta.get("category", "?")
        difficulty = meta.get("difficulty", "?")
        model = meta.get("model_hint", "?")
        execution = meta.get("execution_pattern", "?")[:10]

        print(f"{name:<35} {category:<15} {difficulty:<12} {model:<8} {execution:<12}")

    print("="*100 + "\n")


def generate_command_index(all_metadata: dict) -> str:
    """Generate command-index.md from metadata."""
    index = "# Command Index\n\n"
    index += "_Auto-generated from command metadata. Last updated: 2026-02-09_\n\n"

    # Group by category
    by_category = defaultdict(list)
    for filename, item in all_metadata.items():
        meta = item["metadata"]
        category = meta.get("category", "unknown")
        by_category[category].append((filename, meta))

    # Sort categories in preferred order
    category_order = ["core", "planning", "development", "deployment", "reviews",
                     "repo", "people", "templates", "utilities"]

    for category in category_order:
        if category not in by_category:
            continue

        commands = by_category[category]
        count = len(commands)
        index += f"## {category.title()} ({count} commands)\n\n"

        for filename, meta in sorted(commands):
            name = meta.get("name", filename)
            title = meta.get("title", name)
            difficulty = meta.get("difficulty", "")
            badge = ""
            if difficulty == "beginner":
                badge = "🟢"
            elif difficulty == "intermediate":
                badge = "🟡"
            elif difficulty == "advanced":
                badge = "🔴"

            index += f"- **`{name}`** {badge} — {title}\n"

        index += "\n"

    return index


def generate_stats(all_metadata: dict) -> str:
    """Generate statistics section for CLAUDE.md."""
    stats = "## Command Statistics\n\n"

    # Count by category
    by_cat = defaultdict(int)
    by_diff = defaultdict(int)
    by_model = defaultdict(int)
    by_exec = defaultdict(int)

    for item in all_metadata.values():
        meta = item["metadata"]
        by_cat[meta.get("category", "unknown")] += 1
        by_diff[meta.get("difficulty", "unknown")] += 1
        by_model[meta.get("model_hint", "unknown")] += 1
        by_exec[meta.get("execution_pattern", "unknown")] += 1

    total = len(all_metadata)
    stats += f"**Total:** {total} commands\n\n"

    stats += "### By Category\n"
    for cat in ["core", "planning", "development", "deployment", "reviews",
                "repo", "people", "templates", "utilities"]:
        if cat in by_cat:
            count = by_cat[cat]
            pct = (count / total * 100)
            stats += f"- {cat}: {count} ({pct:.1f}%)\n"

    stats += "\n### By Difficulty\n"
    for diff in ["beginner", "intermediate", "advanced", "expert"]:
        if diff in by_diff:
            count = by_diff[diff]
            pct = (count / total * 100)
            stats += f"- {diff}: {count} ({pct:.1f}%)\n"

    stats += "\n### By Model Hint\n"
    for model in ["haiku", "sonnet", "opus"]:
        if model in by_model:
            count = by_model[model]
            pct = (count / total * 100)
            stats += f"- {model}: {count} ({pct:.1f}%)\n"

    stats += "\n### By Execution Pattern\n"
    for exec_type in sorted(by_exec.keys()):
        count = by_exec[exec_type]
        pct = (count / total * 100)
        stats += f"- {exec_type}: {count} ({pct:.1f}%)\n"

    return stats


def main():
    import sys

    all_metadata = load_all_metadata()

    if len(sys.argv) > 1 and sys.argv[1] == "--index":
        index = generate_command_index(all_metadata)
        print(index)
    elif len(sys.argv) > 1 and sys.argv[1] == "--stats":
        stats = generate_stats(all_metadata)
        print(stats)
    else:
        print(f"Loaded metadata from {len(all_metadata)} commands")
        print_metadata_table(all_metadata)


if __name__ == "__main__":
    main()
