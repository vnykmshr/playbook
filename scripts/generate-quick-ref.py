#!/usr/bin/env python3
"""
Quick Reference Generator

Auto-generates .playbook-quick-ref.md from extracted metadata.
Creates workflows, decision trees, and command browser from actual command relationships.

Usage:
    python scripts/generate-quick-ref.py
    python scripts/generate-quick-ref.py --metadata custom.json
    python scripts/generate-quick-ref.py --output custom-ref.md
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple
import logging

from playbook_utils import setup_logger, load_metadata, get_tier_time_string


class QuickRefGenerator:
    """Generate quick reference documentation from playbook metadata."""

    def __init__(self, metadata_file: Path = None, verbose: bool = False):
        """Initialize generator."""
        self.metadata_file = metadata_file or Path(".playbook-metadata.json")
        self.logger = self._setup_logging(verbose)
        self.metadata = {}
        self.commands = {}
        self.categories = {}

    def _setup_logging(self, verbose: bool) -> logging.Logger:
        """Setup logging."""
        return setup_logger("quick-ref-generator", verbose)

    def load_metadata(self) -> bool:
        """Load extracted metadata from JSON file."""
        self.metadata = load_metadata(self.metadata_file)
        if not self.metadata:
            return False

        self.commands = self.metadata.get("commands", {})
        self.categories = self.metadata.get("categories", {})
        self.logger.info(f"Loaded metadata for {len(self.commands)} commands")
        return True

    def generate(self) -> str:
        """Generate quick reference markdown content."""
        sections = []

        # Header
        sections.append(self._generate_header())

        # Quick Workflows (auto-detected)
        sections.append(self._generate_workflows())

        # Command Browser by Category
        sections.append(self._generate_command_browser())

        # Decision Trees
        sections.append(self._generate_decision_trees())

        # Footer
        sections.append(self._generate_footer())

        return "\n\n".join(sections)

    def _generate_header(self) -> str:
        """Generate document header."""
        avg_confidence = self.metadata.get("extraction_report", {}).get(
            "average_confidence", 0
        )
        lines = [
            "# Playbook Quick Reference",
            "",
            "> **Auto-generated from command metadata**",
            f"> Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            f"> Extraction confidence: {avg_confidence:.0%} average",
            "> This file updates automatically when commands change. Do not edit manually.",
            "",
            "---",
            "",
            "This quick reference shows the most common workflows and decision trees",
            "automatically derived from how commands relate to each other.",
        ]
        return "\n".join(lines)

    def _generate_workflows(self) -> str:
        """Generate common workflows from command relationships."""
        sections = ["## Quick Workflows", "", "Auto-generated from command relationships."]

        # Find hub commands (most referenced)
        workflows = self._detect_workflows()

        for workflow_name, commands_in_workflow in workflows:
            sections.append(self._format_workflow(workflow_name, commands_in_workflow))

        return "\n".join(sections)

    def _detect_workflows(self) -> List[Tuple[str, List[str]]]:
        """
        Detect common workflows by analyzing command relationships.
        Returns list of (workflow_name, [commands])
        """
        workflows = []

        # Development workflow: start → cycle → testing → commit → pr
        dev_workflow = ["pb-start", "pb-cycle", "pb-testing", "pb-commit", "pb-pr"]
        if all(cmd in self.commands for cmd in dev_workflow):
            workflows.append(("Daily Development", dev_workflow))

        # Code review workflow
        review_workflow = ["pb-review-code", "pb-review-tests", "pb-security"]
        if all(cmd in self.commands for cmd in review_workflow[:2]):
            workflows.append(("Code Review", review_workflow))

        # Planning workflow
        planning_workflow = ["pb-plan", "pb-adr", "pb-patterns"]
        if all(cmd in self.commands for cmd in planning_workflow):
            workflows.append(("Architecture Planning", planning_workflow))

        return workflows

    def _format_workflow(self, name: str, commands: List[str]) -> str:
        """Format a workflow as markdown."""
        lines = [f"### {name} Workflow"]

        # Get timing estimate
        timing = self._estimate_workflow_time(commands)
        if timing:
            lines.append(f"**Timeline**: {timing}")

        lines.append("")
        cmd_links = ' → '.join(f'/pb-{cmd.split("-", 1)[1]}' for cmd in commands)
        lines.append(f"Based on: {cmd_links}")
        lines.append("")

        # Add each command with purpose and timing
        for idx, cmd in enumerate(commands, 1):
            if cmd in self.commands:
                meta = self.commands[cmd]
                lines.append(
                    f"{idx}. **`/{cmd}`** — {meta.get('title', cmd)} ({self._get_tier_time(meta.get('tier'))})"
                )
                lines.append(f"   - {meta.get('purpose', '')[:100]}")

        return "\n".join(lines)

    def _estimate_workflow_time(self, commands: List[str]) -> str:
        """Estimate total time for workflow."""
        tier_times = {"XS": 5, "S": 10, "M": 25, "L": 45}
        total = 0

        for cmd in commands:
            if cmd in self.commands:
                tier = self.commands[cmd].get("tier")
                if tier:
                    if isinstance(tier, list):
                        tier = tier[0]
                else:
                    tier = "M"
                total += tier_times.get(tier, 15)

        if total < 30:
            return f"{total}-{total + 10} minutes"
        elif total < 120:
            return f"{total // 60}-{(total + 30) // 60} hours"
        else:
            return f"{total // 60}+ hours"

    def _get_tier_time(self, tier: Any) -> str:
        """Get estimated time for a tier."""
        return get_tier_time_string(tier)

    def _generate_command_browser(self) -> str:
        """Generate command browser by category."""
        sections = [
            "## Command Browser by Category",
            "",
            "All commands organized by category with quick reference info.",
        ]

        for category in sorted(self.categories.keys()):
            cat_data = self.categories[category]
            commands = cat_data.get("commands", [])

            if not commands:
                continue

            sections.append(f"### {category.title()} ({len(commands)} commands)")
            sections.append("")
            sections.append("| Command | Purpose | Tier | Frequency |")
            sections.append("|---------|---------|------|-----------|")

            for cmd_name in sorted(commands):
                if cmd_name in self.commands:
                    meta = self.commands[cmd_name]
                    cmd = f"`/{cmd_name}`"
                    purpose = (meta.get("purpose") or "")[:50]
                    tier = self._format_tier(meta.get("tier"))
                    freq = meta.get("frequency", "as-needed")
                    sections.append(f"| {cmd} | {purpose}... | {tier} | {freq} |")

            sections.append("")

        return "\n".join(sections)

    def _format_tier(self, tier: Any) -> str:
        """Format tier for display."""
        if tier is None:
            return "—"
        if isinstance(tier, list):
            if not tier:
                return "—"
            return "/".join(str(t) for t in tier)
        if isinstance(tier, str):
            return tier
        return "—"

    def _generate_decision_trees(self) -> str:
        """Generate decision trees from command relationships."""
        sections = [
            "## Decision Tree: Choose the Right Command",
            "",
            "Auto-derived from command metadata and relationships.",
        ]

        # Development decision tree
        sections.append("### Are you starting development work?")
        sections.append("")
        sections.append("→ Use this workflow:")
        sections.append("")
        sections.append("1. `/pb-start` — Create feature branch")
        sections.append("2. `/pb-cycle` — Iterate on changes (repeat 3-5 times)")
        sections.append("3. `/pb-testing` — Verify test coverage")
        sections.append("4. `/pb-commit` — Create atomic commits")
        sections.append("5. `/pb-pr` — Create pull request")
        sections.append("")

        # Review decision tree
        sections.append("### Do you need to review code?")
        sections.append("")
        sections.append("**Quick review (10-15 minutes)?**")
        sections.append("→ `/pb-review-code` only")
        sections.append("")
        sections.append("**Comprehensive review (30+ minutes)?**")
        sections.append("→ Use all:")
        sections.append("- `/pb-review-code` — Logic and patterns")
        sections.append("- `/pb-review-tests` — Test coverage")
        sections.append("- `/pb-security` — Security implications")
        sections.append("- `/pb-performance` — Performance impact (if applicable)")
        sections.append("")

        # Planning decision tree
        sections.append("### Planning a new feature or major change?")
        sections.append("")
        sections.append("→ Use this sequence:")
        sections.append("")
        sections.append("1. `/pb-plan` — Define scope and requirements")
        sections.append("2. `/pb-adr` — Document design decisions")
        sections.append("3. `/pb-patterns` — Review relevant patterns")
        sections.append("4. `/pb-security` — Plan security review")

        return "\n".join(sections)

    def _generate_footer(self) -> str:
        """Generate document footer."""
        lines = [
            "---",
            "",
            "## How to Use This Guide",
            "",
            "1. **Find your situation** in the decision tree above",
            "2. **Follow the workflow** step-by-step",
            "3. **Refer to each command** for detailed guidance",
            "4. **Iterate** as needed (most work is iterative)",
            "",
            "## Need More Help?",
            "",
            "- See `docs/command-index.md` for complete command reference",
            "- See `docs/playbook-in-action.md` for real-world examples",
            "- Run `/pb-what-next` for context-aware recommendations",
            "",
            "*This quick reference was auto-generated from playbook command metadata.*",
            f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
        ]
        return "\n".join(lines)

    def save(self, output_path: Path) -> bool:
        """Save generated quick reference to file."""
        import traceback
        try:
            content = self.generate()
            output_path.write_text(content, encoding="utf-8")
            self.logger.info(f"Quick reference saved to {output_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error saving quick reference: {e}")
            traceback.print_exc()
            return False


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Generate playbook quick reference")
    parser.add_argument(
        "--metadata",
        type=Path,
        default=Path(".playbook-metadata.json"),
        help="Path to metadata JSON file",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(".playbook-quick-ref.md"),
        help="Output file path",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()

    # Generate
    generator = QuickRefGenerator(metadata_file=args.metadata, verbose=args.verbose)

    if not generator.load_metadata():
        return 1

    if not generator.save(args.output):
        return 1

    print(f"\n✅ Quick reference generated: {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
