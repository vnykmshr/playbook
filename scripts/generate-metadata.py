#!/usr/bin/env python3
"""
Generate metadata suggestions for all commands.

This script reads all command files and generates YAML front-matter metadata
suggestions based on filename, title, and content analysis.

Usage:
    python3 scripts/generate-metadata.py > metadata-suggestions.yaml
    python3 scripts/generate-metadata.py --apply  # Apply suggestions to files
"""

import os
import re
import sys
from pathlib import Path
from collections import defaultdict

# Category mappings
CATEGORIES = {
    "core": 14,
    "planning": 17,
    "development": 13,
    "deployment": 10,
    "reviews": 12,
    "repo": 7,
    "people": 3,
    "templates": 4,
    "utilities": 6,
}

# Model hints by category
MODEL_HINTS = {
    "core": "sonnet",
    "planning": "opus",
    "development": "sonnet",
    "deployment": "opus",
    "reviews": "opus",
    "repo": "sonnet",
    "people": "sonnet",
    "templates": "haiku",
    "utilities": "haiku",
}

# Execution patterns by command name
EXECUTION_PATTERNS = {
    "pb-think": "interactive",
    "pb-plan": "sequential",
    "pb-adr": "sequential",
    "pb-cycle": "sequential",
    "pb-start": "sequential",
    "pb-resume": "sequential",
    "pb-pause": "sequential",
    "pb-commit": "sequential",
    "pb-pr": "sequential",
    "pb-review": "reference",
    "pb-patterns": "reference",
    "pb-guide": "reference",
    "pb-standards": "reference",
    "pb-design": "reference",
    "pb-preamble": "reference",
}

# Difficulty by category (typical)
DIFFICULTY_HINTS = {
    "core": "beginner",
    "planning": "advanced",
    "development": "intermediate",
    "deployment": "advanced",
    "reviews": "advanced",
    "repo": "intermediate",
    "people": "intermediate",
    "templates": "beginner",
    "utilities": "intermediate",
}

class MetadataGenerator:
    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.commands_dir = self.root / "commands"
        self.commands = {}
        self.related_map = defaultdict(set)

    def discover_commands(self):
        """Find all command files."""
        return sorted(self.commands_dir.glob("**/pb-*.md"))

    def extract_title(self, content: str) -> str:
        """Extract title from markdown (first # heading)."""
        match = re.search(r'^# (.+)$', content, re.MULTILINE)
        return match.group(1) if match else "Unknown"

    def extract_related_commands(self, content: str) -> list:
        """Extract related commands from markdown."""
        related = []
        # Look for Related Commands section
        match = re.search(r'## Related Commands\n([\s\S]*?)(?:\n---|\Z)', content)
        if match:
            section = match.group(1)
            # Extract pb-* references
            refs = re.findall(r'`/pb-([a-z0-9-]+)`', section)
            related = [f"pb-{ref}" for ref in refs][:5]  # Max 5
        return related

    def extract_tags(self, content: str, title: str, name: str) -> list:
        """Generate tags from title and content."""
        tags = []

        # Add tags based on content keywords
        keywords = {
            "design": ["architecture", "pattern", "design"],
            "testing": ["test", "validation"],
            "security": ["security", "encrypt", "auth"],
            "workflow": ["start", "cycle", "commit", "pr", "pause", "resume"],
            "review": ["review", "audit", "check"],
            "deployment": ["deploy", "release", "ship"],
            "documentation": ["doc", "guide", "readme"],
            "optimization": ["performance", "scale", "efficient"],
            "debugging": ["debug", "troubleshoot"],
        }

        lower_content = (title + " " + content).lower()
        for tag, keywords_list in keywords.items():
            if any(kw in lower_content for kw in keywords_list):
                if tag not in tags:
                    tags.append(tag)

        return tags[:5]  # Max 5 tags

    def categorize_difficulty(self, name: str, category: str, content: str) -> str:
        """Estimate difficulty level."""
        # More heuristics would go here; for now use category hint
        base = DIFFICULTY_HINTS.get(category, "intermediate")

        # Adjust based on content complexity
        has_advanced = any(phrase in content.lower() for phrase in
                          ["architecture", "design", "security", "performance", "distributed"])

        if has_advanced and base == "intermediate":
            return "advanced"
        return base

    def generate_metadata(self, filepath: Path) -> dict:
        """Generate metadata for a single command."""
        with open(filepath) as f:
            content = f.read()

        name = filepath.stem
        category = filepath.parent.name
        title = self.extract_title(content)
        related = self.extract_related_commands(content)
        tags = self.extract_tags(content, title, name)

        # Store for cross-references
        self.related_map[name] = set(related)

        # Determine execution pattern
        execution_pattern = EXECUTION_PATTERNS.get(name, "sequential")
        if any(pattern in name for pattern in ["think", "plan", "debug"]):
            execution_pattern = "interactive"

        # Determine difficulty
        difficulty = self.categorize_difficulty(name, category, content)

        # Determine model hint
        model_hint = MODEL_HINTS.get(category, "sonnet")

        return {
            "name": name,
            "title": title,
            "category": category,
            "difficulty": difficulty,
            "model_hint": model_hint,
            "execution_pattern": execution_pattern,
            "related_commands": related,
            "tags": tags,
            "last_reviewed": "2026-02-09",  # Today
            "last_evolved": "",
        }

    def generate_all(self):
        """Generate metadata for all commands."""
        all_metadata = {}
        for filepath in self.discover_commands():
            metadata = self.generate_metadata(filepath)
            all_metadata[filepath.stem] = metadata
            self.commands[filepath] = metadata

        return all_metadata

    def generate_yaml_front_matter(self, metadata: dict) -> str:
        """Convert metadata dict to YAML front-matter."""
        lines = ["---"]
        for key in ["name", "title", "category", "difficulty", "model_hint",
                   "execution_pattern", "related_commands", "tags",
                   "last_reviewed", "last_evolved"]:
            value = metadata.get(key)
            if key in ["related_commands", "tags"]:
                if value:
                    lines.append(f"{key}: {value}")
                else:
                    lines.append(f"{key}: []")
            elif key == "last_evolved" and value == "":
                lines.append(f'{key}: ""')
            elif isinstance(value, str):
                lines.append(f'{key}: "{value}"')
            else:
                lines.append(f"{key}: {value}")
        lines.append("---")
        return "\n".join(lines)

    def apply_to_file(self, filepath: Path, metadata: dict):
        """Apply metadata to a command file."""
        with open(filepath) as f:
            content = f.read()

        # Remove existing front-matter if any
        if content.startswith("---"):
            match = re.match(r'^---\n.*?\n---\n', content, re.DOTALL)
            if match:
                content = content[match.end():]

        # Add new front-matter
        front_matter = self.generate_yaml_front_matter(metadata)
        new_content = front_matter + "\n" + content

        with open(filepath, 'w') as f:
            f.write(new_content)

    def report_summary(self, all_metadata: dict):
        """Print summary of generated metadata."""
        print("\n" + "="*70)
        print("METADATA GENERATION SUMMARY")
        print("="*70 + "\n")

        print(f"Total commands: {len(all_metadata)}")
        print(f"\nBy category:")
        by_cat = defaultdict(int)
        for meta in all_metadata.values():
            by_cat[meta["category"]] += 1
        for cat in sorted(by_cat.keys()):
            print(f"  {cat:15s}: {by_cat[cat]:3d}")

        print(f"\nBy difficulty:")
        by_diff = defaultdict(int)
        for meta in all_metadata.values():
            by_diff[meta["difficulty"]] += 1
        for diff in ["beginner", "intermediate", "advanced", "expert"]:
            if diff in by_diff:
                print(f"  {diff:15s}: {by_diff[diff]:3d}")

        print(f"\nBy model hint:")
        by_model = defaultdict(int)
        for meta in all_metadata.values():
            by_model[meta["model_hint"]] += 1
        for model in ["haiku", "sonnet", "opus"]:
            if model in by_model:
                print(f"  {model:15s}: {by_model[model]:3d}")

        print(f"\nBy execution pattern:")
        by_exec = defaultdict(int)
        for meta in all_metadata.values():
            by_exec[meta["execution_pattern"]] += 1
        for exec_type in sorted(by_exec.keys()):
            print(f"  {exec_type:15s}: {by_exec[exec_type]:3d}")

        print("\n" + "="*70 + "\n")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Generate metadata for commands")
    parser.add_argument("--apply", action="store_true", help="Apply to files")
    parser.add_argument("--summary", action="store_true", help="Show summary only")

    args = parser.parse_args()

    gen = MetadataGenerator()
    all_metadata = gen.generate_all()

    gen.report_summary(all_metadata)

    if args.apply:
        print("Applying metadata to files...")
        for filepath, metadata in gen.commands.items():
            gen.apply_to_file(filepath, metadata)
            print(f"  ✓ {filepath.name}")
        print(f"\nApplied metadata to {len(gen.commands)} files")


if __name__ == "__main__":
    main()
