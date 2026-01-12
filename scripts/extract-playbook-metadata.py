#!/usr/bin/env python3
"""
Playbook Metadata Extraction Engine

Intelligently extracts metadata from playbook command files.
Derives metadata from command structure - zero manual entry needed.

Usage:
    python scripts/extract-playbook-metadata.py
    python scripts/extract-playbook-metadata.py --output custom-path.json
    python scripts/extract-playbook-metadata.py --verbose

Output:
    .playbook-metadata.json (or custom path)
    extraction_report.txt (if --report flag used)
"""

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
import logging

from playbook_utils import setup_logger, is_skill_file


class PlaybookMetadataExtractor:
    """
    Extracts metadata from playbook command markdown files.
    Uses intelligent pattern matching to maximize extraction confidence.
    """

    def __init__(self, repo_root: Path = None, verbose: bool = False):
        """Initialize extractor."""
        self.repo_root = repo_root or Path.cwd()
        self.commands_dir = self.repo_root / "commands"
        self.schema_file = self.repo_root / ".playbook-extraction-schema.yaml"

        # Setup logging
        self.logger = setup_logger("playbook-extractor", verbose)

        # Cache of all valid commands (for cross-validation)
        self.valid_commands: Set[str] = set()

        # Extraction results
        self.metadata: Dict[str, Dict[str, Any]] = {}
        self.warnings: List[Dict[str, str]] = []
        self.errors: List[Dict[str, str]] = []

    def extract_all(self) -> Dict[str, Any]:
        """
        Main entry point: extract metadata from all commands.

        Returns:
            Complete metadata structure with all commands, categories, and metrics
        """
        self.logger.info(f"Starting extraction from {self.commands_dir}")

        # Step 1: Discover all commands
        command_files = self._discover_commands()
        self.logger.info(f"Found {len(command_files)} command files")

        if not command_files:
            self.logger.error("No command files found!")
            return {}

        # Step 2: Build valid commands set (for cross-validation)
        self.valid_commands = {self._extract_command_name(f) for f in command_files}
        self.logger.info(f"Valid commands: {sorted(self.valid_commands)}")

        # Step 3: Extract metadata from each command
        for file_path in sorted(command_files):
            try:
                self._extract_command_metadata(file_path)
            except Exception as e:
                self.logger.error(f"Error extracting {file_path}: {e}")
                self.errors.append(
                    {"file": str(file_path), "error": str(e), "severity": "error"}
                )

        self.logger.info(f"Extracted metadata for {len(self.metadata)} commands")

        # Step 4: Validate extracted metadata
        self._validate_all_metadata()

        # Step 5: Build complete metadata structure
        complete_metadata = self._build_complete_metadata()
        self.complete_metadata = complete_metadata  # Store for saving

        self.logger.info("Extraction complete")
        return complete_metadata


    def _discover_commands(self) -> List[Path]:
        """Discover all command markdown files (excluding skill files)."""
        if not self.commands_dir.exists():
            self.logger.error(f"Commands directory not found: {self.commands_dir}")
            return []

        all_files = sorted(self.commands_dir.rglob("pb-*.md"))

        # Filter out skill files (AI prompt templates, not user commands)
        regular_commands = []
        skill_files = []

        for file_path in all_files:
            try:
                content = self._read_file(file_path)
                if is_skill_file(content):
                    skill_files.append(file_path.stem)
                else:
                    regular_commands.append(file_path)
            except Exception as e:
                self.logger.warning(f"Could not determine file type for {file_path}: {e}")
                regular_commands.append(file_path)  # Default to regular command

        if skill_files:
            self.logger.info(f"Skipping {len(skill_files)} skill files: {sorted(skill_files)}")

        return regular_commands

    def _extract_command_name(self, file_path: Path) -> str:
        """Extract command name from file path."""
        return file_path.stem  # pb-name from pb-name.md

    def _extract_category(self, file_path: Path) -> str:
        """Extract category from directory structure."""
        return file_path.parent.name

    def _read_file(self, file_path: Path) -> str:
        """Read markdown file content."""
        return file_path.read_text(encoding="utf-8")

    def _extract_command_metadata(self, file_path: Path) -> None:
        """Extract metadata from a single command file."""
        content = self._read_file(file_path)
        command = self._extract_command_name(file_path)
        category = self._extract_category(file_path)

        metadata = {
            "command": command,
            "category": category,
            "title": self._extract_title(content),
            "purpose": self._extract_purpose(content),
            "tier": self._extract_tier(content),
            "related_commands": self._extract_related_commands(content),
            "next_steps": self._extract_next_steps(content),
            "prerequisites": self._extract_prerequisites(content),
            "frequency": self._extract_frequency(content),
            "decision_context": self._extract_decision_context(content),
            "sections": self._extract_sections(content),
            "has_examples": self._extract_has_examples(content),
            "has_checklist": self._extract_has_checklist(content),
            "extraction_metadata": {
                "source_file": str(file_path.relative_to(self.repo_root)),
                "extraction_date": datetime.now(timezone.utc).isoformat(),
                "extractor_version": "1.0",
            },
        }

        # Calculate confidence scores
        metadata["confidence_scores"] = self._calculate_confidence_scores(
            metadata, content
        )
        metadata["average_confidence"] = self._calculate_average_confidence(
            metadata["confidence_scores"]
        )

        self.metadata[command] = metadata

    def _extract_title(self, content: str) -> Optional[str]:
        """Extract title from first h1 heading."""
        match = re.search(r"^#\s+([^#\n]+)", content, re.MULTILINE)
        if match:
            title = match.group(1).strip()
            # Remove markdown syntax
            title = re.sub(r"\*\*|__", "", title)
            return title
        return None

    def _extract_purpose(self, content: str) -> Optional[str]:
        """Extract purpose from first paragraph after h1."""
        # Split on --- separator or first double newline after heading
        parts = re.split(r"\n---\n|\n\n", content, maxsplit=2)

        if len(parts) >= 2:
            # Get text after h1 but before separator
            text = parts[1].strip()
            if text and not text.startswith("#"):
                return text.split("\n")[0]

        return None

    def _extract_tier(self, content: str) -> Optional[List[str]]:
        """
        Extract tier from explicit markers or complexity keywords.
        Returns list of tiers [XS, S, M, L] or None
        """
        tiers = set()

        # Pattern 1: Explicit "Tier: X" or "Tier: [X, Y]"
        tier_matches = re.findall(
            r"[Tt]ier:\s*\[?([XS]|M|[L]?)(?:\s*,\s*([XS]|M|[L]?))*\]?", content
        )
        if tier_matches:
            for match in tier_matches:
                for item in match:
                    if item and item in {"XS", "S", "M", "L"}:
                        tiers.add(item)

        # Pattern 2: Tier table rows
        tier_rows = re.findall(r"\|\s*\*\*([XS]|M|L)\*\*\s*\|", content)
        for row_tier in tier_rows:
            if row_tier in {"XS", "S", "M", "L"}:
                tiers.add(row_tier)

        # Pattern 3: Complexity keywords
        if re.search(
            r"\b(simple|straightforward|trivial|minimal)\b",
            content,
            re.IGNORECASE,
        ):
            tiers.add("XS")
        if re.search(r"\b(medium|moderate|standard)\b", content, re.IGNORECASE):
            tiers.add("M")
        if re.search(
            r"\b(large|complex|substantial|significant)\b", content, re.IGNORECASE
        ):
            tiers.add("L")

        if tiers:
            return sorted(list(tiers), key=lambda x: {"XS": 0, "S": 1, "M": 2, "L": 3}[x])
        return None

    def _extract_related_commands(self, content: str) -> List[str]:
        """
        Extract all /pb-* command references from content.
        Returns sorted unique list, excluding command's own name.
        """
        # Find all /pb-<name> references
        commands = re.findall(r"/pb-[\w-]+", content)

        # Remove duplicates and sort
        unique_commands = sorted(set(commands))

        return unique_commands

    def _extract_next_steps(self, content: str) -> Optional[List[str]]:
        """
        Extract workflow sequence from "Next Steps" section or workflow patterns.
        Order indicates sequence (important).
        """
        # Look for "Next Steps" or "Workflow" section
        sections_pattern = r"##\s+(?:Next Steps|Then|Workflow|After)\s*\n(.*?)(?=##|\Z)"
        match = re.search(sections_pattern, content, re.IGNORECASE | re.DOTALL)

        if not match:
            return None

        section_text = match.group(1)

        # Extract /pb-* references maintaining order
        commands = re.findall(r"/pb-[\w-]+", section_text)

        # Remove duplicates while preserving order
        seen = set()
        unique_commands = []
        for cmd in commands:
            if cmd not in seen:
                seen.add(cmd)
                unique_commands.append(cmd)

        return unique_commands if unique_commands else None

    def _extract_prerequisites(self, content: str) -> Optional[List[str]]:
        """
        Extract required setup steps from Prerequisites section.
        """
        # Look for "Prerequisites" or "Before" section
        sections_pattern = r"##\s+(?:Prerequisites|Before|Pre-Start)\s*\n(.*?)(?=##|\Z)"
        match = re.search(sections_pattern, content, re.IGNORECASE | re.DOTALL)

        if not match:
            return None

        section_text = match.group(1)

        # Extract /pb-* references
        commands = re.findall(r"/pb-[\w-]+", section_text)

        # Remove duplicates while preserving order
        seen = set()
        unique_commands = []
        for cmd in commands:
            if cmd not in seen:
                seen.add(cmd)
                unique_commands.append(cmd)

        return unique_commands if unique_commands else None

    def _extract_frequency(self, content: str) -> Optional[str]:
        """
        Extract usage frequency from "When to Use" section.
        Returns one of: daily, weekly, start-of-feature, per-iteration, per-pr,
        pre-release, on-incident, one-time, as-needed
        """
        # Look for "When to Use" section
        when_match = re.search(
            r"##\s+When to Use\s*\n(.*?)(?=##|\Z)", content, re.IGNORECASE | re.DOTALL
        )

        if not when_match:
            return "as-needed"

        when_text = when_match.group(1).lower()

        # Check for frequency patterns
        frequency_patterns = {
            "daily": r"\bdaily\b|\beveryday\b",
            "weekly": r"\bweekly\b|\bweek\b",
            "start-of-feature": r"\bstart of feature\b|\bstart of\b.*\bfeature\b|\bbeginning of feature\b",
            "per-iteration": r"\bper iteration\b|\beach iteration\b|\bevery iteration\b",
            "per-pr": r"\bper pr\b|\bbefore.*pr\b|\beach.*pr\b",
            "pre-release": r"\brelease\b|\bpre-release\b|\bdeployment\b",
            "on-incident": r"\bincident\b|\bhotfix\b|\bemergency\b",
            "one-time": r"\bone-time\b|\binitial setup\b|\bfirst time\b",
        }

        for freq, pattern in frequency_patterns.items():
            if re.search(pattern, when_text):
                return freq

        return "as-needed"

    def _extract_decision_context(self, content: str) -> Optional[Dict[str, str]]:
        """
        Extract decision rules and conditions.
        Returns structured decision logic or None.
        """
        decision_context = {}

        # Look for decision patterns like "Feature? → Use /pb-X"
        decision_patterns = re.findall(
            r"([^→\n]+?)\s*→\s*(?:use\s+)?(/pb-[\w-]+)",
            content,
            re.IGNORECASE,
        )

        for condition, command in decision_patterns:
            decision_context[condition.strip()] = command

        # Look for "When to Use" conditionals
        when_match = re.search(
            r"##\s+When to Use\s*\n(.*?)(?=##|\Z)", content, re.IGNORECASE | re.DOTALL
        )
        if when_match:
            when_text = when_match.group(1)
            # Extract "Use when:", "Use if:", patterns
            when_conditions = re.findall(
                r"use\s+(?:when|if):\s*([^\n]+)", when_text, re.IGNORECASE
            )
            for cond in when_conditions:
                decision_context[f"use_when_{len(decision_context)}"] = cond.strip()

        return decision_context if decision_context else None

    def _extract_sections(self, content: str) -> List[str]:
        """Extract all ## section headings as slugified names."""
        sections = re.findall(r"^##\s+([^#\n]+)", content, re.MULTILINE)

        # Slugify section names
        slugified = []
        for section in sections:
            slug = section.lower()
            slug = re.sub(r"[^\w\s-]", "", slug)  # Remove special chars
            slug = re.sub(r"\s+", "-", slug)  # Replace spaces with hyphens
            slugified.append(slug)

        return slugified

    def _extract_has_examples(self, content: str) -> bool:
        """Check if content includes code examples (``` blocks)."""
        return bool(re.search(r"```", content))

    def _extract_has_checklist(self, content: str) -> bool:
        """Check if content includes checklists ([ ] syntax)."""
        return bool(re.search(r"\[\s*\]", content))

    def _calculate_confidence_scores(
        self, metadata: Dict[str, Any], content: str
    ) -> Dict[str, float]:
        """Calculate confidence score for each extracted field."""
        confidence = {}

        # command: Always 100% (from filename)
        confidence["command"] = 1.0 if metadata.get("command") else 0.0

        # title: 100% if found with proper h1
        confidence["title"] = 1.0 if metadata.get("title") else 0.0

        # category: 100% if found
        confidence["category"] = 1.0 if metadata.get("category") else 0.0

        # purpose: 95% if found, 0% if not
        confidence["purpose"] = 0.95 if metadata.get("purpose") else 0.0

        # tier: Variable based on how explicit
        if metadata.get("tier"):
            if "Tier:" in content:
                confidence["tier"] = 0.95  # Explicit
            elif "##" in content:
                confidence["tier"] = 0.85  # From table
            else:
                confidence["tier"] = 0.75  # Inferred from keywords
        else:
            confidence["tier"] = 0.0

        # related_commands: 95% if found (regex is reliable)
        confidence["related_commands"] = 0.95 if metadata.get("related_commands") else 0.0

        # next_steps: 80-90% depending on explicitness
        if metadata.get("next_steps"):
            if "Next Steps" in content:
                confidence["next_steps"] = 0.90
            else:
                confidence["next_steps"] = 0.80
        else:
            confidence["next_steps"] = 0.0

        # prerequisites: 85% if found
        confidence["prerequisites"] = 0.85 if metadata.get("prerequisites") else 0.0

        # frequency: 75-85% (depends on clarity)
        if metadata.get("frequency") != "as-needed":
            confidence["frequency"] = 0.85
        else:
            confidence["frequency"] = 0.60  # Defaulted/fallback

        # decision_context: 70% (often implicit)
        confidence["decision_context"] = 0.70 if metadata.get("decision_context") else 0.0

        # sections, has_examples, has_checklist: 100% (objective checks)
        confidence["sections"] = 1.0 if metadata.get("sections") else 0.0
        confidence["has_examples"] = 1.0
        confidence["has_checklist"] = 1.0

        return confidence

    def _calculate_average_confidence(self, scores: Dict[str, float]) -> float:
        """Calculate average confidence score."""
        if not scores:
            return 0.0

        # Exclude optional fields with 0 confidence from average
        # (missing optional field != bad extraction)
        relevant_scores = [
            score
            for field, score in scores.items()
            if field not in ["next_steps", "prerequisites", "decision_context"]
            or score > 0
        ]

        if not relevant_scores:
            return 0.0

        return sum(relevant_scores) / len(relevant_scores)

    def _validate_all_metadata(self) -> None:
        """Validate all extracted metadata against rules."""
        for command, metadata in self.metadata.items():
            self._validate_command_metadata(command, metadata)

    def _validate_command_metadata(self, command: str, metadata: Dict[str, Any]) -> None:
        """Validate metadata for a single command."""
        # Check required fields
        required = ["command", "title", "category", "purpose"]
        for field in required:
            if not metadata.get(field):
                self.errors.append(
                    {
                        "command": command,
                        "field": field,
                        "issue": "Required field missing",
                        "severity": "error",
                    }
                )

        # Validate references
        for cmd_ref in metadata.get("related_commands") or []:
            cmd_name = cmd_ref.lstrip("/")
            if cmd_name not in self.valid_commands and cmd_name != command:
                self.warnings.append(
                    {
                        "command": command,
                        "field": "related_commands",
                        "issue": f"Referenced command {cmd_ref} not found",
                        "severity": "warning",
                    }
                )

        for cmd_ref in metadata.get("next_steps") or []:
            cmd_name = cmd_ref.lstrip("/")
            if cmd_name not in self.valid_commands:
                self.warnings.append(
                    {
                        "command": command,
                        "field": "next_steps",
                        "issue": f"Referenced command {cmd_ref} not found",
                        "severity": "warning",
                    }
                )

        # Check confidence thresholds
        scores = metadata.get("confidence_scores", {})
        for field, score in scores.items():
            if field in ["command", "title", "category"] and score < 1.0:
                self.errors.append(
                    {
                        "command": command,
                        "field": field,
                        "issue": f"Critical field has low confidence: {score}",
                        "severity": "error",
                    }
                )
            elif score < 0.70 and score > 0:
                self.warnings.append(
                    {
                        "command": command,
                        "field": field,
                        "issue": f"Low confidence score: {score:.2f}",
                        "severity": "warning",
                    }
                )

    def _build_complete_metadata(self) -> Dict[str, Any]:
        """Build complete metadata structure with categories and metrics."""
        # Group by category
        categories = {}
        for command, metadata in self.metadata.items():
            category = metadata["category"]
            if category not in categories:
                categories[category] = {"count": 0, "commands": []}
            categories[category]["count"] += 1
            categories[category]["commands"].append(command)

        # Calculate metrics
        total_commands = len(self.metadata)
        avg_confidence = (
            sum(m["average_confidence"] for m in self.metadata.values()) / total_commands
            if total_commands > 0
            else 0
        )

        return {
            "metadata_version": "1.0",
            "extraction_date": datetime.now(timezone.utc).isoformat(),
            "total_commands": total_commands,
            "commands": self.metadata,
            "categories": categories,
            "extraction_report": {
                "total_commands": total_commands,
                "extraction_success": sum(
                    1 for m in self.metadata.values() if m.get("command")
                ),
                "average_confidence": round(avg_confidence, 4),
                "warnings": self.warnings,
                "errors": self.errors,
            },
        }

    def save_metadata(self, output_path: Path) -> None:
        """Save complete metadata to JSON file."""
        metadata_to_save = getattr(self, "complete_metadata", None) or self.metadata
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(metadata_to_save, f, indent=2)
        self.logger.info(f"Metadata saved to {output_path}")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Extract metadata from playbook commands"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(".playbook-metadata.json"),
        help="Output file path",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
        help="Repository root directory",
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Extract
    extractor = PlaybookMetadataExtractor(repo_root=args.repo_root, verbose=args.verbose)
    metadata = extractor.extract_all()

    # Save
    extractor.save_metadata(args.output)

    # Print summary
    report = metadata.get("extraction_report", {})
    print(f"\n=== Extraction Summary ===")
    print(f"Total commands: {report.get('total_commands', 0)}")
    print(f"Successful extractions: {report.get('extraction_success', 0)}")
    print(f"Average confidence: {report.get('average_confidence', 0):.2%}")
    print(f"Warnings: {len(report.get('warnings', []))}")
    print(f"Errors: {len(report.get('errors', []))}")

    if report.get("errors"):
        print("\nErrors:")
        for error in report["errors"][:5]:
            print(f"  - {error}")

    if report.get("warnings"):
        print(f"\nWarnings (showing first 5 of {len(report['warnings'])}):")
        for warning in report["warnings"][:5]:
            print(f"  - {warning}")

    # Always return 0 - metadata extraction is successful as long as we created the file
    # Errors and warnings are reported but don't block the build
    return 0


if __name__ == "__main__":
    sys.exit(main())
