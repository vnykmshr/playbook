#!/usr/bin/env python3
"""
Evolution Diff Tool

Show exactly what will change when evolution is applied.
Compare current playbook state with proposed evolved state.

Usage:
    # Show diff between current and evolved commands
    python3 scripts/evolution-diff.py --compare <base-commit> <evolved-commit>

    # Show which commands would change
    python3 scripts/evolution-diff.py --changed <base-commit> <evolved-commit>

    # Generate detailed diff for review
    python3 scripts/evolution-diff.py --detailed <base-commit> <evolved-commit>
"""

import json
import re
import sys
import subprocess
from pathlib import Path
from collections import defaultdict


class EvolutionDiff:
    """Analyze differences between evolution stages."""

    def __init__(self):
        self.commands_dir = Path("commands")

    def extract_metadata(self, content: str) -> dict | None:
        """Extract YAML front-matter from markdown."""
        match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
        if not match:
            return None

        metadata = {}
        for line in match.group(1).split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if ':' not in line:
                continue

            key, _, value = line.partition(':')
            key = key.strip()
            value = value.strip().strip('"')
            metadata[key] = value

        return metadata

    def get_command_metadata_at_commit(self, commit: str, filename: str) -> dict | None:
        """Get metadata for a command at a specific git commit."""
        try:
            content = subprocess.check_output(
                ["git", "show", f"{commit}:{filename}"],
                text=True,
                stderr=subprocess.DEVNULL
            )
            return self.extract_metadata(content)
        except subprocess.CalledProcessError:
            return None

    def get_changed_commands(self, base_commit: str, evolved_commit: str) -> dict:
        """Find commands that changed between commits."""
        try:
            # Get list of changed files
            diff_output = subprocess.check_output(
                ["git", "diff", "--name-only", f"{base_commit}...{evolved_commit}"],
                text=True
            ).strip()

            changed_files = [f for f in diff_output.split('\n') if f.startswith('commands/')]
            changes = {}

            for filepath in changed_files:
                base_meta = self.get_command_metadata_at_commit(base_commit, filepath)
                evolved_meta = self.get_command_metadata_at_commit(evolved_commit, filepath)

                if base_meta and evolved_meta:
                    # Find field-level changes
                    field_changes = {}
                    all_keys = set(base_meta.keys()) | set(evolved_meta.keys())

                    for key in all_keys:
                        base_val = base_meta.get(key)
                        evolved_val = evolved_meta.get(key)
                        if base_val != evolved_val:
                            field_changes[key] = {
                                'before': base_val,
                                'after': evolved_val
                            }

                    if field_changes:
                        cmd_name = evolved_meta.get('name', 'unknown')
                        changes[cmd_name] = {
                            'filepath': filepath,
                            'fields': field_changes
                        }

            return changes

        except subprocess.CalledProcessError as e:
            print(f"❌ Error getting diff: {e}\n")
            return {}

    def print_summary(self, changes: dict):
        """Print summary of changes."""
        if not changes:
            print("✅ No metadata changes detected.\n")
            return

        print(f"\n📊 Evolution Diff Summary\n")
        print(f"Total commands changed: {len(changes)}\n")

        # Group by field type
        field_changes = defaultdict(list)
        for cmd_name, change in changes.items():
            for field, values in change['fields'].items():
                field_changes[field].append((cmd_name, values))

        print("Changes by field type:\n")
        for field in sorted(field_changes.keys()):
            count = len(field_changes[field])
            print(f"  {field}: {count} command(s)")

    def print_changed_commands(self, changes: dict):
        """List commands that changed."""
        if not changes:
            print("✅ No changes.\n")
            return

        print(f"\n📝 Commands Changed: {len(changes)}\n")
        for cmd_name in sorted(changes.keys()):
            print(f"  • {cmd_name}")

        print()

    def print_detailed(self, changes: dict):
        """Print detailed diff for each change."""
        if not changes:
            print("✅ No changes.\n")
            return

        print(f"\n🔍 Detailed Evolution Diff\n")
        print("=" * 70)

        for cmd_name in sorted(changes.keys()):
            change = changes[cmd_name]
            fields = change['fields']

            print(f"\n### {cmd_name}\n")

            for field in sorted(fields.keys()):
                before = fields[field]['before']
                after = fields[field]['after']

                print(f"**{field}:**")
                print(f"  - Before: `{before}`")
                print(f"  - After:  `{after}`")
                print()

        print("=" * 70)
        print()

    def generate_markdown_report(self, changes: dict, output_file: str = "todos/evolution-diff-report.md"):
        """Generate markdown report of evolution diff."""
        with open(output_file, 'w') as f:
            f.write("# Evolution Diff Report\n\n")
            f.write(f"**Generated:** {Path('').absolute().name}\n")
            f.write(f"**Total Changes:** {len(changes)}\n\n")

            # Summary by field
            field_changes = defaultdict(list)
            for cmd_name, change in changes.items():
                for field, values in change['fields'].items():
                    field_changes[field].append((cmd_name, values))

            f.write("## Changes by Field\n\n")
            for field in sorted(field_changes.keys()):
                items = field_changes[field]
                f.write(f"### {field} ({len(items)} changes)\n\n")

                for cmd_name, values in sorted(items):
                    before = values['before']
                    after = values['after']
                    f.write(f"- **{cmd_name}**: `{before}` → `{after}`\n")

                f.write("\n")

            # Detailed changes
            f.write("## Detailed Changes\n\n")
            for cmd_name in sorted(changes.keys()):
                change = changes[cmd_name]
                fields = change['fields']

                f.write(f"### {cmd_name}\n\n")
                for field in sorted(fields.keys()):
                    before = fields[field]['before']
                    after = fields[field]['after']
                    f.write(f"**{field}:**\n")
                    f.write(f"- Before: `{before}`\n")
                    f.write(f"- After: `{after}`\n\n")

        print(f"✅ Diff report saved to: {output_file}\n")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Evolution Diff Tool"
    )
    parser.add_argument(
        "--compare",
        nargs=2,
        metavar=("BASE", "EVOLVED"),
        help="Compare two commits"
    )
    parser.add_argument(
        "--changed",
        nargs=2,
        metavar=("BASE", "EVOLVED"),
        help="Show which commands changed"
    )
    parser.add_argument(
        "--detailed",
        nargs=2,
        metavar=("BASE", "EVOLVED"),
        help="Show detailed field-by-field diff"
    )
    parser.add_argument(
        "--report",
        nargs=2,
        metavar=("BASE", "EVOLVED"),
        help="Generate markdown report"
    )

    args = parser.parse_args()

    diff = EvolutionDiff()

    if args.compare:
        changes = diff.get_changed_commands(args.compare[0], args.compare[1])
        diff.print_summary(changes)
        diff.print_changed_commands(changes)
        sys.exit(0)

    elif args.changed:
        changes = diff.get_changed_commands(args.changed[0], args.changed[1])
        diff.print_changed_commands(changes)
        sys.exit(0)

    elif args.detailed:
        changes = diff.get_changed_commands(args.detailed[0], args.detailed[1])
        diff.print_detailed(changes)
        sys.exit(0)

    elif args.report:
        changes = diff.get_changed_commands(args.report[0], args.report[1])
        diff.print_detailed(changes)
        diff.generate_markdown_report(changes)
        sys.exit(0)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
