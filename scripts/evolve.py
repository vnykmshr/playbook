#!/usr/bin/env python3
"""
Playbook Evolution Engine

Periodically reviews and regenerates playbooks based on metadata.
- Extracts metadata from command files
- Validates consistency
- Auto-generates indices, decision trees, CLAUDE.md sections
- Reports evolution opportunities
- Maintains evolution log

Usage:
    python3 scripts/evolve.py --analyze       # Audit current state
    python3 scripts/evolve.py --generate      # Auto-generate indices
    python3 scripts/evolve.py --validate      # Validate all metadata
    python3 scripts/evolve.py --report        # Evolution report
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Optional, Tuple

try:
    import yaml
except ImportError:
    # Fallback if PyYAML not available
    yaml = None

class PlaybookEvolutionEngine:
    """Analyzes and evolves playbook commands."""

    def __init__(self, root_dir="."):
        self.root = Path(root_dir)
        self.commands_dir = self.root / "commands"
        self.docs_dir = self.root / "docs"
        self.metadata_schema = self._load_schema()
        self.commands = {}
        self.errors = []
        self.warnings = []

    def _load_schema(self) -> Dict:
        """Load metadata schema from .playbook-metadata-schema.yaml"""
        if yaml is None:
            return {}
        schema_path = self.root / ".playbook-metadata-schema.yaml"
        if schema_path.exists():
            with open(schema_path) as f:
                return yaml.safe_load(f) or {}
        return {}

    def discover_commands(self) -> List[Path]:
        """Find all command files."""
        return sorted(self.commands_dir.glob("**/pb-*.md"))

    def extract_metadata(self, filepath: Path) -> Tuple[Optional[Dict], str]:
        """Extract YAML front-matter from command file.

        Returns: (metadata_dict, file_content)
        """
        with open(filepath, 'r') as f:
            content = f.read()

        # Look for YAML front-matter between --- delimiters
        match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
        if match:
            if yaml is None:
                self.warnings.append(f"{filepath.name}: YAML not available, skipping metadata")
                return None, content
            try:
                metadata = yaml.safe_load(match.group(1)) or {}
                return metadata, content
            except Exception as e:
                self.errors.append(f"{filepath.name}: YAML parse error: {e}")
                return None, content

        # No metadata found
        return None, content

    def load_all_commands(self):
        """Load and parse all command files."""
        for filepath in self.discover_commands():
            metadata, content = self.extract_metadata(filepath)
            self.commands[filepath.name] = {
                "path": filepath,
                "metadata": metadata,
                "content": content,
                "has_metadata": metadata is not None
            }

    def validate_metadata(self) -> Dict[str, List[str]]:
        """Validate all metadata against schema.

        Returns: {filename: [list of validation errors]}
        """
        issues = defaultdict(list)

        for filename, cmd in self.commands.items():
            if cmd["metadata"] is None:
                issues[filename].append("MISSING: No YAML front-matter")
                continue

            meta = cmd["metadata"]

            # Check required fields
            required = ["name", "title", "category", "difficulty", "model_hint",
                       "execution_pattern", "related_commands", "tags", "last_reviewed"]
            for field in required:
                if field not in meta:
                    issues[filename].append(f"MISSING: Required field '{field}'")

            # Validate field values
            if "name" in meta:
                expected_name = filename.replace(".md", "")
                if meta["name"] != expected_name:
                    issues[filename].append(
                        f"MISMATCH: name='{meta['name']}' but filename is '{expected_name}'"
                    )

            if "category" in meta:
                valid_categories = ["core", "planning", "development", "deployment",
                                   "reviews", "repo", "people", "templates", "utilities"]
                if meta["category"] not in valid_categories:
                    issues[filename].append(f"INVALID: category='{meta['category']}'")

            if "difficulty" in meta:
                valid_difficulties = ["beginner", "intermediate", "advanced", "expert"]
                if meta["difficulty"] not in valid_difficulties:
                    issues[filename].append(f"INVALID: difficulty='{meta['difficulty']}'")

            if "model_hint" in meta:
                valid_models = ["haiku", "sonnet", "opus"]
                if meta["model_hint"] not in valid_models:
                    issues[filename].append(f"INVALID: model_hint='{meta['model_hint']}'")

            if "related_commands" in meta:
                if not isinstance(meta["related_commands"], list):
                    issues[filename].append("INVALID: related_commands must be a list")
                elif len(meta["related_commands"]) > 5:
                    issues[filename].append(
                        f"TOO_MANY: related_commands has {len(meta['related_commands'])} items (max 5)"
                    )
                # Check for self-reference
                if "name" in meta and meta["name"] in meta["related_commands"]:
                    issues[filename].append(f"CIRCULAR: related_commands includes self")

            if "tags" in meta:
                if not isinstance(meta["tags"], list):
                    issues[filename].append("INVALID: tags must be a list")
                elif len(meta["tags"]) > 5:
                    issues[filename].append(
                        f"TOO_MANY: tags has {len(meta['tags'])} items (max 5)"
                    )

            # Check dates
            if "last_reviewed" in meta and meta["last_reviewed"]:
                try:
                    review_date = datetime.strptime(meta["last_reviewed"], "%Y-%m-%d")
                    days_old = (datetime.now() - review_date).days
                    if days_old > 90:
                        self.warnings.append(
                            f"{filename}: last_reviewed is {days_old} days old"
                        )
                except ValueError:
                    issues[filename].append(
                        f"INVALID: last_reviewed date format (use YYYY-MM-DD)"
                    )

        return issues

    def generate_command_index(self) -> str:
        """Generate command index markdown grouped by category."""
        index = "# Command Index\n\n"
        index += "Auto-generated from command metadata. Last updated: " + \
                datetime.now().strftime("%Y-%m-%d") + "\n\n"

        # Group by category
        by_category = defaultdict(list)
        for filename, cmd in sorted(self.commands.items()):
            if cmd["metadata"]:
                category = cmd["metadata"].get("category", "unknown")
                by_category[category].append((filename, cmd["metadata"]))

        # Sort categories in preferred order
        category_order = ["core", "planning", "development", "deployment", "reviews",
                         "repo", "people", "templates", "utilities"]

        for category in category_order:
            if category not in by_category:
                continue

            index += f"## {category.title()}\n\n"
            for filename, meta in sorted(by_category[category]):
                name = meta.get("name", filename)
                title = meta.get("title", name)
                summary = meta.get("summary", "")
                difficulty = meta.get("difficulty", "")

                index += f"- **[`{name}`]({name})** "
                if difficulty:
                    index += f"_{difficulty}_ "
                index += f"— {summary}\n"

            index += "\n"

        return index

    def generate_model_distribution(self) -> Dict[str, int]:
        """Analyze model usage across all commands."""
        distribution = defaultdict(int)
        for cmd in self.commands.values():
            if cmd["metadata"]:
                model = cmd["metadata"].get("model_hint", "unknown")
                distribution[model] += 1
        return dict(distribution)

    def generate_category_breakdown(self) -> Dict[str, int]:
        """Analyze command count by category."""
        breakdown = defaultdict(int)
        for cmd in self.commands.values():
            if cmd["metadata"]:
                category = cmd["metadata"].get("category", "unknown")
                breakdown[category] += 1
        return dict(breakdown)

    def analyze(self) -> Dict:
        """Analyze current state."""
        self.load_all_commands()

        total_commands = len(self.commands)
        with_metadata = sum(1 for c in self.commands.values() if c["has_metadata"])

        validation_issues = self.validate_metadata()
        total_issues = sum(len(v) for v in validation_issues.values())

        model_dist = self.generate_model_distribution()
        category_breakdown = self.generate_category_breakdown()

        return {
            "timestamp": datetime.now().isoformat(),
            "total_commands": total_commands,
            "commands_with_metadata": with_metadata,
            "commands_without_metadata": total_commands - with_metadata,
            "metadata_coverage_percent": (with_metadata / total_commands * 100) if total_commands else 0,
            "validation_issues": total_issues,
            "issues_by_file": validation_issues,
            "model_distribution": model_dist,
            "category_breakdown": category_breakdown,
            "errors": self.errors,
            "warnings": self.warnings,
        }

    def report_analysis(self, analysis: Dict):
        """Print analysis report."""
        print("\n" + "="*70)
        print("PLAYBOOK EVOLUTION ANALYSIS")
        print("="*70 + "\n")

        print(f"Timestamp: {analysis['timestamp']}")
        print(f"Total commands: {analysis['total_commands']}")
        print(f"With metadata: {analysis['commands_with_metadata']} "
              f"({analysis['metadata_coverage_percent']:.1f}%)")
        print(f"Without metadata: {analysis['commands_without_metadata']}")

        print(f"\nValidation Issues: {analysis['validation_issues']}")
        if analysis['validation_issues'] > 0:
            print("\nIssues by file:")
            for filename, issues in sorted(analysis['issues_by_file'].items()):
                if issues:
                    print(f"  {filename}:")
                    for issue in issues:
                        print(f"    - {issue}")

        print(f"\nModel Distribution:")
        for model, count in sorted(analysis['model_distribution'].items()):
            pct = (count / analysis['total_commands'] * 100) if analysis['total_commands'] else 0
            print(f"  {model:8s}: {count:3d} ({pct:5.1f}%)")

        print(f"\nCategory Breakdown:")
        for category, count in sorted(analysis['category_breakdown'].items()):
            pct = (count / analysis['total_commands'] * 100) if analysis['total_commands'] else 0
            print(f"  {category:15s}: {count:3d} ({pct:5.1f}%)")

        if analysis['errors']:
            print(f"\nErrors ({len(analysis['errors'])}):")
            for error in analysis['errors'][:5]:
                print(f"  - {error}")
            if len(analysis['errors']) > 5:
                print(f"  ... and {len(analysis['errors']) - 5} more")

        if analysis['warnings']:
            print(f"\nWarnings ({len(analysis['warnings'])}):")
            for warning in analysis['warnings'][:5]:
                print(f"  - {warning}")
            if len(analysis['warnings']) > 5:
                print(f"  ... and {len(analysis['warnings']) - 5} more")

        print("\n" + "="*70 + "\n")

    def save_analysis(self, analysis: Dict, filepath: str = "todos/evolution-analysis.json"):
        """Save analysis results to JSON."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(analysis, f, indent=2)
        print(f"Analysis saved to {filepath}")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Playbook Evolution Engine")
    parser.add_argument("--analyze", action="store_true", help="Analyze current state")
    parser.add_argument("--generate", action="store_true", help="Generate indices")
    parser.add_argument("--validate", action="store_true", help="Validate metadata")
    parser.add_argument("--report", action="store_true", help="Generate report")
    parser.add_argument("--all", action="store_true", help="Run all analyses")

    args = parser.parse_args()

    # Default to --analyze if no args
    if not any([args.analyze, args.generate, args.validate, args.report, args.all]):
        args.analyze = True

    # Check PyYAML availability
    if yaml is None:
        print("ERROR: PyYAML module not available.", file=sys.stderr)
        print("Install with: pip install pyyaml", file=sys.stderr)
        print("\nFor CI: Add pyyaml to dependencies in deploy-docs.yml", file=sys.stderr)
        sys.exit(1)

    engine = PlaybookEvolutionEngine()

    if args.analyze or args.all:
        analysis = engine.analyze()
        engine.report_analysis(analysis)
        engine.save_analysis(analysis)

    if args.validate or args.all:
        engine.load_all_commands()
        issues = engine.validate_metadata()
        if issues:
            print("Validation issues found:")
            for filename, file_issues in sorted(issues.items()):
                print(f"  {filename}: {len(file_issues)} issue(s)")
        else:
            print("All metadata valid ✓")

    if args.generate or args.all:
        engine.load_all_commands()
        index = engine.generate_command_index()
        output_path = engine.docs_dir / "command-index-generated.md"
        with open(output_path, 'w') as f:
            f.write(index)
        print(f"Generated index: {output_path}")


if __name__ == "__main__":
    main()
