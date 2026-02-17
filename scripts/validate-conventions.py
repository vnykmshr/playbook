#!/usr/bin/env python3
"""
Playbook Convention Validation Script

Verifies all command files follow audit conventions:
- Resource Hint present with valid model tier
- When to Use section present (or recognized variant)
- Related Commands count within limits

Usage:
    python scripts/validate-conventions.py
    python scripts/validate-conventions.py --verbose
"""

import argparse
import sys
from pathlib import Path

from playbook_utils import setup_logger

COMMANDS_DIR = Path(__file__).parent.parent / "commands"
EXPECTED_COUNT = 97  # Updated for v2.12.0: 94 baseline + 3 new

# Hub commands allowed to exceed the 5-link limit
HUB_COMMANDS = {"pb-patterns.md"}
RELATED_LIMIT = 5
HUB_RELATED_LIMIT = 10

VALID_MODELS = {"opus", "sonnet", "haiku"}

# Recognized "When to Use" heading variants (lowercase substring match)
WHEN_TO_USE_VARIANTS = [
    "## when to use",
    "## when to read",
    "## when to write",
    "## when to deprecate",
    "## when to optimize",
    "## when to create",
    "### when to use",
    "**when to use",
]


class ConventionValidator:
    """Validates playbook command conventions."""

    def __init__(self, verbose: bool = False):
        self.logger = setup_logger("convention-validator", verbose)
        self.errors = []
        self.warnings = []
        self.passed = 0

    def _pass(self, msg: str):
        self.passed += 1
        self.logger.debug(f"  PASS: {msg}")

    def _fail(self, msg: str):
        self.errors.append(msg)
        self.logger.error(f"  FAIL: {msg}")

    def _warn(self, msg: str):
        self.warnings.append(msg)
        self.logger.warning(f"  WARN: {msg}")

    def validate_count(self, files: list) -> None:
        """Check expected number of command files."""
        count = len(files)
        if count == EXPECTED_COUNT:
            self._pass(f"Command count: {count}")
        else:
            self._fail(f"Expected {EXPECTED_COUNT} commands, found {count}")

    def validate_resource_hint(self, path: Path, content: str) -> None:
        """Check Resource Hint presence and valid model."""
        name = path.name
        if "**Resource Hint:**" not in content:
            self._fail(f"{name}: missing **Resource Hint:**")
            return

        for line in content.splitlines():
            if "**Resource Hint:**" in line:
                line_lower = line.lower()
                models_found = [m for m in VALID_MODELS if m in line_lower]
                if models_found:
                    self._pass(f"{name}: Resource Hint ({models_found[0]})")
                else:
                    self._fail(
                        f"{name}: Resource Hint missing model "
                        f"(opus/sonnet/haiku): {line.strip()}"
                    )
                return

    def validate_when_to_use(self, path: Path, content: str) -> None:
        """Check When to Use section or recognized variant."""
        name = path.name
        content_lower = content.lower()
        if any(v in content_lower for v in WHEN_TO_USE_VARIANTS):
            self._pass(f"{name}: When to Use present")
        else:
            self._fail(f"{name}: missing When to Use section")

    def validate_related_commands(self, path: Path, content: str) -> None:
        """Check Related Commands count within limits."""
        name = path.name
        lines = content.splitlines()

        in_section = False
        link_count = 0
        for line in lines:
            if line.strip().startswith("## Related Commands"):
                in_section = True
                continue
            if in_section:
                if line.startswith("## ") or line.startswith("---"):
                    break
                if line.strip().startswith("- `/pb-"):
                    link_count += 1

        if link_count == 0:
            self._warn(f"{name}: no standard Related Commands section found")
            return

        is_hub = name in HUB_COMMANDS
        limit = HUB_RELATED_LIMIT if is_hub else RELATED_LIMIT
        if link_count <= limit:
            self._pass(f"{name}: Related Commands ({link_count}/{limit})")
        else:
            self._fail(
                f"{name}: {link_count} Related Commands exceeds "
                f"limit of {limit}"
            )

    def run(self) -> bool:
        """Run all convention checks. Returns True if all pass."""
        files = sorted(COMMANDS_DIR.rglob("*.md"))

        self.logger.info(f"Validating conventions for {len(files)} commands")
        self.logger.info(f"Commands directory: {COMMANDS_DIR}")
        self.logger.info("")

        # Count check
        self.validate_count(files)

        # Per-file checks
        for path in files:
            content = path.read_text()
            self.validate_resource_hint(path, content)
            self.validate_when_to_use(path, content)
            self.validate_related_commands(path, content)

        # Report
        self.logger.info("")
        self.logger.info("=" * 50)
        self.logger.info("Convention Validation Summary")
        self.logger.info("=" * 50)
        self.logger.info(f"  Passed:   {self.passed}")
        self.logger.info(f"  Warnings: {len(self.warnings)}")
        self.logger.info(f"  Errors:   {len(self.errors)}")

        if self.errors:
            self.logger.info("")
            self.logger.info("Errors:")
            for err in self.errors:
                self.logger.info(f"  - {err}")

        if self.warnings:
            self.logger.info("")
            self.logger.info("Warnings:")
            for warn in self.warnings:
                self.logger.info(f"  - {warn}")

        self.logger.info("")
        if self.errors:
            self.logger.info("RESULT: FAIL")
        else:
            self.logger.info("RESULT: PASS")

        return len(self.errors) == 0


def main():
    parser = argparse.ArgumentParser(
        description="Validate playbook command conventions"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show all checks"
    )
    args = parser.parse_args()

    validator = ConventionValidator(verbose=args.verbose)
    success = validator.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
