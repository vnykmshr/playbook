#!/usr/bin/env python3
"""
Convention validation tests for playbook command files.

Verifies all command files follow audit conventions established in v2.8.0:
- Resource Hint present with valid model tier
- When to Use section present (or recognized variant)
- Related Commands count within limits
- Expected command count
- Metadata model_hint matches body Resource Hint (consistency)
"""

import re
from pathlib import Path

import pytest

COMMANDS_DIR = Path(__file__).parent.parent / "commands"
EXPECTED_COUNT = 101  # Updated for v2.13.3: 100 baseline + pb-zero-stack

# Hub commands allowed to exceed the 5-link limit
HUB_COMMANDS = {"pb-patterns.md"}
RELATED_LIMIT = 5
HUB_RELATED_LIMIT = 10

VALID_MODELS = {"opus", "sonnet", "haiku"}

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


def get_command_files():
    """Return sorted list of all command markdown files."""
    return sorted(COMMANDS_DIR.rglob("*.md"))


def get_related_commands_count(content: str) -> int:
    """Count Related Commands links in standard section."""
    in_section = False
    count = 0
    for line in content.splitlines():
        if line.strip().startswith("## Related Commands"):
            in_section = True
            continue
        if in_section:
            if line.startswith("## ") or line.startswith("---"):
                break
            if line.strip().startswith("- `/pb-"):
                count += 1
    return count


class TestCommandCount:
    def test_expected_command_count(self):
        files = get_command_files()
        assert len(files) == EXPECTED_COUNT, (
            f"Expected {EXPECTED_COUNT} commands, found {len(files)}"
        )


class TestResourceHint:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.files = get_command_files()

    def test_all_commands_have_resource_hint(self):
        missing = []
        for path in self.files:
            content = path.read_text()
            if "**Resource Hint:**" not in content:
                missing.append(path.name)
        assert not missing, f"Missing Resource Hint: {missing}"

    def test_resource_hints_have_valid_model(self):
        invalid = []
        for path in self.files:
            content = path.read_text()
            for line in content.splitlines():
                if "**Resource Hint:**" in line:
                    line_lower = line.lower()
                    if not any(m in line_lower for m in VALID_MODELS):
                        invalid.append(path.name)
                    break
        assert not invalid, f"Invalid model in Resource Hint: {invalid}"


class TestWhenToUse:
    def test_all_commands_have_when_to_use(self):
        missing = []
        for path in get_command_files():
            content_lower = path.read_text().lower()
            if not any(v in content_lower for v in WHEN_TO_USE_VARIANTS):
                missing.append(path.name)
        assert not missing, f"Missing When to Use: {missing}"


class TestRelatedCommands:
    def test_related_commands_within_limits(self):
        over_limit = []
        for path in get_command_files():
            content = path.read_text()
            count = get_related_commands_count(content)
            if count == 0:
                continue
            is_hub = path.name in HUB_COMMANDS
            limit = HUB_RELATED_LIMIT if is_hub else RELATED_LIMIT
            if count > limit:
                over_limit.append(f"{path.name} ({count}/{limit})")
        assert not over_limit, f"Over Related Commands limit: {over_limit}"


class TestMetadataConsistency:
    """Verify metadata front-matter matches body Resource Hint.

    This prevents regressions where bulk metadata generation overwrites
    carefully audited Resource Hints from v2.8.0 audit.
    """

    @staticmethod
    def extract_body_resource_hint(content: str) -> str | None:
        """Extract model from body Resource Hint line."""
        match = re.search(r'\*\*Resource Hint:\*\*\s+(sonnet|opus|haiku)', content)
        return match.group(1) if match else None

    @staticmethod
    def extract_metadata_model_hint(content: str) -> str | None:
        """Extract model_hint from YAML front-matter."""
        match = re.search(r'^model_hint:\s*"([^"]+)"', content, re.MULTILINE)
        return match.group(1) if match else None

    def test_metadata_matches_body_resource_hint(self):
        """All commands must have consistent model_hint in metadata and body."""
        conflicts = []
        for path in get_command_files():
            content = path.read_text()
            body_hint = self.extract_body_resource_hint(content)
            meta_hint = self.extract_metadata_model_hint(content)

            if body_hint and meta_hint and body_hint != meta_hint:
                conflicts.append(
                    f"{path.name}: body={body_hint}, metadata={meta_hint}"
                )

        assert not conflicts, f"Metadata-body conflicts:\n" + "\n".join(
            f"  {c}" for c in conflicts
        )


class TestPersonaIntegrity:
    """Validate persona agent structure and consistency."""

    # Persona agents introduced in v2.11.0 Phase 1
    PERSONA_COMMANDS = {
        "pb-linus-agent.md": {"model": "opus", "category": "reviews", "difficulty": "advanced"},
        "pb-alex-infra.md": {"model": "opus", "category": "deployment", "difficulty": "advanced"},
        "pb-maya-product.md": {"model": "sonnet", "category": "planning", "difficulty": "intermediate"},
        "pb-sam-documentation.md": {"model": "sonnet", "category": "core", "difficulty": "intermediate"},
        "pb-jordan-testing.md": {"model": "opus", "category": "development", "difficulty": "advanced"},
    }

    def test_persona_agents_exist(self):
        """Ensure all 5 persona agents are present."""
        files = get_command_files()
        file_names = {f.name for f in files}
        missing = []
        for persona_name in self.PERSONA_COMMANDS:
            if persona_name not in file_names:
                missing.append(persona_name)
        assert not missing, f"Missing persona agents: {missing}"

    def test_persona_metadata_correct(self):
        """Verify persona metadata matches expected values."""
        files = get_command_files()
        errors = []
        for path in files:
            if path.name not in self.PERSONA_COMMANDS:
                continue
            content = path.read_text()
            expected = self.PERSONA_COMMANDS[path.name]

            # Check model_hint
            meta_hint = re.search(r'^model_hint:\s*"([^"]+)"', content, re.MULTILINE)
            if meta_hint and meta_hint.group(1) != expected["model"]:
                errors.append(
                    f"{path.name}: model_hint={meta_hint.group(1)}, expected {expected['model']}"
                )

            # Check category
            meta_cat = re.search(r'^category:\s*"([^"]+)"', content, re.MULTILINE)
            if meta_cat and meta_cat.group(1) != expected["category"]:
                errors.append(
                    f"{path.name}: category={meta_cat.group(1)}, expected {expected['category']}"
                )

            # Check difficulty
            meta_diff = re.search(r'^difficulty:\s*"([^"]+)"', content, re.MULTILINE)
            if meta_diff and meta_diff.group(1) != expected["difficulty"]:
                errors.append(
                    f"{path.name}: difficulty={meta_diff.group(1)}, expected {expected['difficulty']}"
                )

        assert not errors, f"Persona metadata mismatches:\n" + "\n".join(f"  {e}" for e in errors)

    def test_persona_agents_have_decision_framework(self):
        """Ensure persona agents have structured decision/review framework."""
        files = get_command_files()
        missing_framework = []
        for path in files:
            if path.name not in self.PERSONA_COMMANDS:
                continue
            content = path.read_text().lower()

            # Personas must have either: "decision", "framework", "review", or "criteria"
            if not any(keyword in content for keyword in ["decision", "framework", "review criteria", "red flags"]):
                missing_framework.append(path.name)

        assert not missing_framework, f"Persona agents missing decision framework: {missing_framework}"

    def test_multi_perspective_reviews_exist(self):
        """Ensure multi-perspective review commands exist (Phase 2)."""
        multi_reviews = {"pb-review-backend.md", "pb-review-frontend.md", "pb-review-infrastructure.md"}
        files = get_command_files()
        file_names = {f.name for f in files}
        missing = multi_reviews - file_names
        assert not missing, f"Missing multi-perspective reviews: {missing}"

    def test_persona_no_hardcoded_security_flaws(self):
        """Check persona agents for common security anti-patterns."""
        # Specifically validates pb-linus-agent.md for password hashing security
        files = get_command_files()
        security_issues = []
        for path in files:
            if path.name == "pb-linus-agent.md":
                content = path.read_text()
                # Should not have hardcoded salt in password examples
                if "b'salt'" in content:
                    security_issues.append(f"{path.name}: Contains hardcoded salt in password example")
                # Should use bcrypt, not pbkdf2 with hardcoded salt
                if re.search(r"pbkdf2_hmac.*b'salt'", content):
                    security_issues.append(f"{path.name}: Uses pbkdf2 with hardcoded salt")

        assert not security_issues, f"Security issues in persona agents:\n" + "\n".join(
            f"  {issue}" for issue in security_issues
        )
