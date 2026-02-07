#!/usr/bin/env python3
"""
Convention validation tests for playbook command files.

Verifies all command files follow audit conventions established in v2.8.0:
- Resource Hint present with valid model tier
- When to Use section present (or recognized variant)
- Related Commands count within limits
- Expected command count
"""

from pathlib import Path

import pytest

COMMANDS_DIR = Path(__file__).parent.parent / "commands"
EXPECTED_COUNT = 84

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
