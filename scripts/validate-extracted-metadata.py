#!/usr/bin/env python3
"""
Playbook Metadata Validation Script

Validates extracted metadata against quality rules.
Generates improvement suggestions for low-confidence fields.

Usage:
    python scripts/validate-extracted-metadata.py .playbook-metadata.json
    python scripts/validate-extracted-metadata.py --report validation_report.txt
    python scripts/validate-extracted-metadata.py --strict (fails on warnings)
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
import logging


class MetadataValidator:
    """Validates extracted playbook metadata."""

    def __init__(self, verbose: bool = False):
        """Initialize validator."""
        self.logger = self._setup_logging(verbose)
        self.errors: List[Dict[str, Any]] = []
        self.warnings: List[Dict[str, Any]] = []
        self.suggestions: List[Dict[str, str]] = []
        self.metrics = {}

    def _setup_logging(self, verbose: bool) -> logging.Logger:
        """Setup logging."""
        logger = logging.getLogger("metadata-validator")
        logger.setLevel(logging.DEBUG if verbose else logging.INFO)

        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger

    def validate(self, metadata: Dict[str, Any]) -> bool:
        """
        Validate metadata structure and quality.

        Returns:
            True if all critical checks pass, False otherwise
        """
        self.logger.info("Starting metadata validation...")

        # Extract commands and build valid set
        commands = metadata.get("commands", {})
        valid_commands = set(commands.keys())

        self.logger.info(f"Validating {len(commands)} commands")

        # Validate each command
        for command_name, command_meta in commands.items():
            self._validate_command(command_name, command_meta, valid_commands)

        # Cross-validate references
        self._validate_references(commands, valid_commands)

        # Generate metrics
        self._generate_metrics(commands)

        # Generate improvement suggestions
        self._generate_suggestions(commands)

        has_critical_errors = len(self.errors) > 0
        return not has_critical_errors

    def _validate_command(
        self, command: str, metadata: Dict[str, Any], valid_commands: Set[str]
    ) -> None:
        """Validate a single command's metadata."""
        # Required fields
        required_fields = ["command", "title", "category", "purpose"]
        for field in required_fields:
            if not metadata.get(field):
                self.errors.append(
                    {
                        "command": command,
                        "type": "missing_required_field",
                        "field": field,
                        "severity": "critical",
                    }
                )

        # Field value validation
        if metadata.get("command") != command:
            self.errors.append(
                {
                    "command": command,
                    "type": "invalid_field_value",
                    "field": "command",
                    "expected": command,
                    "actual": metadata.get("command"),
                    "severity": "critical",
                }
            )

        # Category validation
        valid_categories = {
            "core", "development", "planning", "reviews",
            "release", "deployment", "repo", "people", "templates"
        }
        if metadata.get("category") not in valid_categories:
            self.errors.append(
                {
                    "command": command,
                    "type": "invalid_category",
                    "category": metadata.get("category"),
                    "valid_categories": list(valid_categories),
                    "severity": "critical",
                }
            )

        # Tier validation (if present)
        if metadata.get("tier"):
            valid_tiers = {"XS", "S", "M", "L"}
            tiers = metadata.get("tier")
            if isinstance(tiers, list):
                for tier in tiers:
                    if tier not in valid_tiers:
                        self.errors.append(
                            {
                                "command": command,
                                "type": "invalid_tier",
                                "tier": tier,
                                "valid_tiers": list(valid_tiers),
                                "severity": "error",
                            }
                        )
            elif tiers not in valid_tiers:
                self.errors.append(
                    {
                        "command": command,
                        "type": "invalid_tier",
                        "tier": tiers,
                        "valid_tiers": list(valid_tiers),
                        "severity": "error",
                    }
                )

        # Frequency validation (if present)
        if metadata.get("frequency"):
            valid_frequencies = {
                "daily", "weekly", "start-of-feature", "per-iteration",
                "per-pr", "pre-release", "on-incident", "one-time", "as-needed"
            }
            if metadata["frequency"] not in valid_frequencies:
                self.warnings.append(
                    {
                        "command": command,
                        "type": "invalid_frequency",
                        "frequency": metadata.get("frequency"),
                        "valid_frequencies": list(valid_frequencies),
                        "severity": "warning",
                    }
                )

        # Confidence validation
        confidence_scores = metadata.get("confidence_scores", {})
        avg_confidence = metadata.get("average_confidence", 0)

        # Critical fields must have high confidence
        critical_fields = {"command", "title", "category", "purpose"}
        for field in critical_fields:
            score = confidence_scores.get(field, 0)
            if field in ["command", "title", "category"] and score < 0.99:
                self.errors.append(
                    {
                        "command": command,
                        "type": "low_confidence_critical_field",
                        "field": field,
                        "confidence": score,
                        "severity": "critical",
                    }
                )

        # Warn on low average confidence
        if avg_confidence < 0.70:
            self.warnings.append(
                {
                    "command": command,
                    "type": "low_average_confidence",
                    "confidence": round(avg_confidence, 2),
                    "severity": "warning",
                }
            )

    def _validate_references(
        self, commands: Dict[str, Any], valid_commands: Set[str]
    ) -> None:
        """Validate cross-references between commands."""
        for command, metadata in commands.items():
            # Validate related_commands
            for ref in metadata.get("related_commands") or []:
                cmd_name = ref.lstrip("/")
                if cmd_name not in valid_commands and cmd_name != command:
                    self.warnings.append(
                        {
                            "command": command,
                            "type": "invalid_reference",
                            "field": "related_commands",
                            "reference": ref,
                            "severity": "warning",
                        }
                    )

            # Validate next_steps
            for ref in metadata.get("next_steps") or []:
                cmd_name = ref.lstrip("/")
                if cmd_name not in valid_commands:
                    self.warnings.append(
                        {
                            "command": command,
                            "type": "invalid_reference",
                            "field": "next_steps",
                            "reference": ref,
                            "severity": "warning",
                        }
                    )

            # Validate prerequisites
            for ref in metadata.get("prerequisites") or []:
                cmd_name = ref.lstrip("/")
                if cmd_name not in valid_commands:
                    self.warnings.append(
                        {
                            "command": command,
                            "type": "invalid_reference",
                            "field": "prerequisites",
                            "reference": ref,
                            "severity": "warning",
                        }
                    )

    def _generate_metrics(self, commands: Dict[str, Any]) -> None:
        """Generate quality metrics."""
        total = len(commands)
        if total == 0:
            return

        # Count commands by category
        categories = {}
        for cmd, metadata in commands.items():
            cat = metadata.get("category", "unknown")
            categories[cat] = categories.get(cat, 0) + 1

        # Calculate average confidence
        confidences = [m.get("average_confidence", 0) for m in commands.values()]
        avg_conf = sum(confidences) / len(confidences) if confidences else 0

        # Count fields present
        has_tier = sum(1 for m in commands.values() if m.get("tier"))
        has_examples = sum(1 for m in commands.values() if m.get("has_examples"))
        has_checklist = sum(1 for m in commands.values() if m.get("has_checklist"))
        has_next_steps = sum(1 for m in commands.values() if m.get("next_steps"))

        self.metrics = {
            "total_commands": total,
            "categories": categories,
            "average_confidence": round(avg_conf, 4),
            "field_completeness": {
                "tier": f"{has_tier}/{total}",
                "examples": f"{has_examples}/{total}",
                "checklist": f"{has_checklist}/{total}",
                "next_steps": f"{has_next_steps}/{total}",
            },
            "low_confidence_commands": [
                (cmd, round(m.get("average_confidence", 0), 2))
                for cmd, m in commands.items()
                if m.get("average_confidence", 1) < 0.80
            ],
        }

    def _generate_suggestions(self, commands: Dict[str, Any]) -> None:
        """Generate improvement suggestions for low-confidence fields."""
        for command, metadata in commands.items():
            confidence_scores = metadata.get("confidence_scores", {})

            # Missing tier (and category suggests it might be needed)
            if (
                not metadata.get("tier")
                and metadata.get("category") in {"core", "development", "planning"}
            ):
                self.suggestions.append(
                    {
                        "command": command,
                        "field": "tier",
                        "suggestion": "Add explicit tier information (XS/S/M/L) or complexity mention",
                        "improvement_potential": "Confidence: 0% → 85-95%",
                        "action": "Add 'Tier: S' or 'Tier: [S, M, L]' to command file",
                    }
                )

            # Missing examples
            if (
                not metadata.get("has_examples")
                and metadata.get("category") not in {"templates"}
            ):
                self.suggestions.append(
                    {
                        "command": command,
                        "field": "has_examples",
                        "suggestion": "Add code examples or concrete usage examples",
                        "improvement_potential": "Makes command more practical and discoverable",
                        "action": "Include at least one code block (```) with real-world example",
                    }
                )

            # Missing next_steps
            if (
                not metadata.get("next_steps")
                and metadata.get("category") in {"development", "planning"}
            ):
                self.suggestions.append(
                    {
                        "command": command,
                        "field": "next_steps",
                        "suggestion": "Add 'Next Steps' section showing workflow progression",
                        "improvement_potential": "Confidence: 0% → 80-90%",
                        "action": "Add '## Next Steps' section with /pb-* references",
                    }
                )

            # Low purpose confidence
            if confidence_scores.get("purpose", 0) < 0.90:
                self.suggestions.append(
                    {
                        "command": command,
                        "field": "purpose",
                        "suggestion": "Clarify purpose statement - be more specific about action/outcome",
                        "improvement_potential": "Confidence: {:.0%} → 95%+".format(
                            confidence_scores.get("purpose", 0)
                        ),
                        "action": "Ensure first paragraph after h1 is a complete, specific sentence",
                    }
                )

    def generate_report(self, output_file: Optional[Path] = None) -> str:
        """Generate human-readable validation report."""
        report_lines = []
        report_lines.append("=" * 70)
        report_lines.append("PLAYBOOK METADATA VALIDATION REPORT")
        report_lines.append(f"Generated: {datetime.now().isoformat()}")
        report_lines.append("=" * 70)
        report_lines.append("")

        # Summary
        report_lines.append("SUMMARY")
        report_lines.append("-" * 70)
        report_lines.append(f"Total Commands: {self.metrics.get('total_commands', 0)}")
        report_lines.append(f"Average Confidence: {self.metrics.get('average_confidence', 0):.2%}")
        report_lines.append(f"Critical Errors: {len(self.errors)}")
        report_lines.append(f"Warnings: {len(self.warnings)}")
        report_lines.append(f"Improvement Suggestions: {len(self.suggestions)}")
        report_lines.append("")

        # Categories
        if self.metrics.get("categories"):
            report_lines.append("COMMAND DISTRIBUTION BY CATEGORY")
            report_lines.append("-" * 70)
            for cat, count in sorted(self.metrics["categories"].items()):
                report_lines.append(f"  {cat:20} {count:3} commands")
            report_lines.append("")

        # Errors
        if self.errors:
            report_lines.append("CRITICAL ERRORS (Must Fix)")
            report_lines.append("-" * 70)
            for error in self.errors[:20]:
                report_lines.append(f"  Command: {error.get('command')}")
                report_lines.append(f"  Type: {error.get('type')}")
                if "field" in error:
                    report_lines.append(f"  Field: {error.get('field')}")
                report_lines.append("")

        # Warnings
        if self.warnings:
            report_lines.append("WARNINGS (Should Address)")
            report_lines.append("-" * 70)
            # Group by type
            by_type = {}
            for warning in self.warnings:
                wtype = warning.get("type", "unknown")
                if wtype not in by_type:
                    by_type[wtype] = []
                by_type[wtype].append(warning)

            for wtype, warnings_list in sorted(by_type.items()):
                report_lines.append(f"  {wtype} ({len(warnings_list)})")
                for warning in warnings_list[:3]:  # Show first 3
                    report_lines.append(
                        f"    - {warning.get('command', 'N/A')}: {warning.get('field', 'N/A')}"
                    )
                if len(warnings_list) > 3:
                    report_lines.append(f"    ... and {len(warnings_list) - 3} more")
                report_lines.append("")

        # Low confidence commands
        if self.metrics.get("low_confidence_commands"):
            report_lines.append("LOW CONFIDENCE COMMANDS (< 80%)")
            report_lines.append("-" * 70)
            for cmd, conf in self.metrics["low_confidence_commands"][:10]:
                report_lines.append(f"  {cmd:30} {conf:.2%}")
            report_lines.append("")

        # Suggestions
        if self.suggestions:
            report_lines.append("IMPROVEMENT SUGGESTIONS (Top Priority)")
            report_lines.append("-" * 70)
            # Group by field
            by_field = {}
            for suggestion in self.suggestions:
                field = suggestion.get("field", "unknown")
                if field not in by_field:
                    by_field[field] = []
                by_field[field].append(suggestion)

            for field, suggestions_list in sorted(by_field.items()):
                count = len(suggestions_list)
                report_lines.append(f"  {field} ({count} commands need improvement)")
                for suggestion in suggestions_list[:2]:  # Show first 2
                    report_lines.append(f"    - {suggestion.get('command')}: {suggestion.get('suggestion')}")
                if len(suggestions_list) > 2:
                    report_lines.append(f"    ... and {len(suggestions_list) - 2} more")
                report_lines.append("")

        # Completion
        report_lines.append("=" * 70)
        status = "✅ PASS" if len(self.errors) == 0 else "❌ FAIL"
        report_lines.append(f"Status: {status}")
        report_lines.append("=" * 70)

        report_text = "\n".join(report_lines)

        if output_file:
            output_file.write_text(report_text, encoding="utf-8")
            print(f"Report saved to {output_file}")

        return report_text

    def print_report(self) -> None:
        """Print report to stdout."""
        print(self.generate_report())


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Validate playbook metadata"
    )
    parser.add_argument(
        "metadata_file",
        type=Path,
        help="Path to .playbook-metadata.json",
    )
    parser.add_argument(
        "--report",
        type=Path,
        help="Output report file",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail on warnings (not just errors)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    args = parser.parse_args()

    # Load metadata
    try:
        with open(args.metadata_file, "r", encoding="utf-8") as f:
            metadata = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found {args.metadata_file}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {args.metadata_file}: {e}", file=sys.stderr)
        return 1

    # Validate
    validator = MetadataValidator(verbose=args.verbose)
    success = validator.validate(metadata)

    # Generate report
    if args.report:
        validator.generate_report(args.report)
    else:
        validator.print_report()

    # Exit code
    if args.strict and len(validator.warnings) > 0:
        return 1
    if not success:
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
