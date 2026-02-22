#!/usr/bin/env python3
"""
Evolution Execution Validation

Tests that evolved playbooks still execute correctly with current Claude.
This prevents metadata changes from breaking actual playbook logic.

Run after evolution cycle to validate:
1. Evolved playbooks parse correctly
2. Resource hints match execution requirements
3. Related commands still exist and are reachable
4. Metadata changes don't introduce contradictions

Usage:
    pytest tests/test_evolution_execution.py -v
    pytest tests/test_evolution_execution.py::TestEvolutionImpact -v
"""

import re
from pathlib import Path

import pytest

COMMANDS_DIR = Path(__file__).parent.parent / "commands"


def extract_resource_hint(content: str) -> str | None:
    """Extract model from body Resource Hint line."""
    match = re.search(r'\*\*Resource Hint:\*\*\s+(sonnet|opus|haiku)', content)
    return match.group(1) if match else None


def extract_metadata_field(content: str, field: str) -> str | None:
    """Extract a field from YAML front-matter."""
    pattern = rf'^{field}:\s*"?([^"\n]+)"?'
    match = re.search(pattern, content, re.MULTILINE)
    return match.group(1) if match else None


def extract_related_commands(content: str) -> list[str]:
    """Extract command references from the Related Commands section only."""
    in_section = False
    refs = []
    for line in content.splitlines():
        if line.strip().startswith("## Related Commands"):
            in_section = True
            continue
        if in_section:
            if line.startswith("## ") or line.strip() == "---":
                break
            matches = re.findall(r'/pb-[\w-]+', line)
            refs.extend(matches)
    return sorted(set(refs))


def get_all_command_files():
    """Get all command files."""
    return sorted(COMMANDS_DIR.glob("**/pb-*.md"))


def command_exists(name: str) -> bool:
    """Check if a command file exists."""
    for f in get_all_command_files():
        if extract_metadata_field(f.read_text(), "name") == name:
            return True
    return False


class TestEvolutionMetadataImpact:
    """Test that metadata evolution doesn't break playbooks."""

    def test_evolved_resource_hints_are_valid(self):
        """After evolution, Resource Hint in body should match metadata model_hint."""
        files = get_all_command_files()
        mismatches = []

        for filepath in files:
            content = filepath.read_text()
            body_hint = extract_resource_hint(content)
            meta_hint = extract_metadata_field(content, "model_hint")

            if body_hint and meta_hint and body_hint != meta_hint:
                mismatches.append(
                    f"{filepath.name}: body={body_hint}, meta={meta_hint}"
                )

        assert not mismatches, (
            f"Resource Hint mismatches (would break routing):\n"
            + "\n".join(f"  {m}" for m in mismatches)
        )

    def test_related_commands_exist(self):
        """All related_commands references should point to existing commands."""
        # Template files use placeholder references like /pb-related-1
        template_files = {"pb-new-playbook.md"}
        files = get_all_command_files()
        broken_refs = []

        for filepath in files:
            if filepath.name in template_files:
                continue
            content = filepath.read_text()
            related = extract_related_commands(content)

            for ref in related:
                # Convert /pb-something to pb-something
                cmd_name = ref.lstrip("/")
                if not command_exists(cmd_name):
                    broken_refs.append(f"{filepath.name}: {ref} not found")

        assert not broken_refs, (
            f"Broken related command references (would 404):\n"
            + "\n".join(f"  {r}" for r in broken_refs)
        )

    def test_model_hints_match_task_complexity(self):
        """Model hints should make sense for task complexity (heuristic check).

        This is a soft check (warnings, not errors) because some assignments
        may be intentional even if they seem mismatched.
        """
        files = get_all_command_files()
        potential_mismatches = []

        for filepath in files:
            content = filepath.read_text()
            name = extract_metadata_field(content, "name")
            model = extract_metadata_field(content, "model_hint")
            category = extract_metadata_field(content, "category")

            # Heuristic: review/security commands should not be haiku
            if "review" in name or "security" in name:
                if model == "haiku":
                    potential_mismatches.append(
                        f"{name}: {model} for {category} (review/security typically needs depth)"
                    )

            # Heuristic: utilities should prefer haiku
            if category == "utilities" and "setup" not in name:
                if model == "opus":
                    potential_mismatches.append(
                        f"{name}: {model} for {category} (utilities typically don't need opus)"
                    )

        if potential_mismatches:
            pytest.warns(
                UserWarning,
                match="Potential model hint mismatches",
            )
            # Log but don't fail (these may be intentional)
            for msg in potential_mismatches:
                print(f"  ⚠️  {msg}")


class TestEvolutionStructuralImpact:
    """Test that evolution doesn't break playbook structure."""

    def test_no_orphaned_metadata_fields(self):
        """Evolved metadata should only use defined fields."""
        # This is a placeholder for future schema validation
        # When we add custom fields, this test will catch them
        pass

    def test_categories_are_valid(self):
        """All commands must have valid categories."""
        valid_categories = {
            "core", "planning", "development", "deployment",
            "reviews", "repo", "people", "templates", "utilities"
        }
        files = get_all_command_files()
        invalid = []

        for filepath in files:
            content = filepath.read_text()
            category = extract_metadata_field(content, "category")
            if category and category not in valid_categories:
                invalid.append(f"{filepath.name}: invalid category '{category}'")

        assert not invalid, f"Invalid categories:\n" + "\n".join(f"  {i}" for i in invalid)

    def test_execution_patterns_are_valid(self):
        """All commands must have valid execution patterns."""
        valid_patterns = {
            "sequential", "parallel", "interactive", "exploratory", "reference",
            "automatic", "interactive-once", "checklist"
        }
        files = get_all_command_files()
        invalid = []

        for filepath in files:
            content = filepath.read_text()
            pattern = extract_metadata_field(content, "execution_pattern")
            if pattern and pattern not in valid_patterns:
                invalid.append(f"{filepath.name}: invalid pattern '{pattern}'")

        assert not invalid, f"Invalid execution patterns:\n" + "\n".join(f"  {i}" for i in invalid)


class TestEvolutionReadiness:
    """Check if playbooks are ready for evolution."""

    def test_playbooks_have_last_reviewed_date(self):
        """All commands should have last_reviewed to detect staleness."""
        files = get_all_command_files()
        missing = []

        for filepath in files:
            content = filepath.read_text()
            last_reviewed = extract_metadata_field(content, "last_reviewed")
            if not last_reviewed:
                missing.append(filepath.name)

        assert not missing, (
            f"Missing last_reviewed dates (can't detect staleness):\n"
            + "\n".join(f"  {m}" for m in missing)
        )

    def test_related_commands_not_excessive(self):
        """Related commands should be limited (prevents link decay)."""
        files = get_all_command_files()
        over_limit = []

        for filepath in files:
            content = filepath.read_text()
            related = extract_related_commands(content)
            # Most commands: ≤5 related. Hub commands: ≤10 (pb-patterns indexes all sub-patterns).
            limit = 10 if "pb-patterns.md" in filepath.name else 5

            if len(related) > limit:
                over_limit.append(f"{filepath.name}: {len(related)} related (limit {limit})")

        assert not over_limit, (
            f"Too many related commands:\n" + "\n".join(f"  {o}" for o in over_limit)
        )


class TestEvolutionDependencies:
    """Ensure evolution won't break command dependencies."""

    def test_bidirectional_command_references_exist(self):
        """If A references B, B should exist."""
        template_files = {"pb-new-playbook.md"}
        files = get_all_command_files()
        broken_dependencies = []

        for filepath in files:
            if filepath.name in template_files:
                continue
            content = filepath.read_text()
            related = extract_related_commands(content)

            for ref in related:
                cmd_name = ref.lstrip("/")
                # Check that the referenced command exists
                if not any(cmd_name == extract_metadata_field(f.read_text(), "name")
                          for f in files):
                    broken_dependencies.append(f"{filepath.name} → {ref}")

        assert not broken_dependencies, (
            f"Broken command dependencies:\n" + "\n".join(f"  {b}" for b in broken_dependencies)
        )

    def test_no_circular_references(self):
        """Detect if command A references B, and B references A (potential issue for learning)."""
        files = get_all_command_files()
        circulars = []

        for filepath in files:
            content = filepath.read_text()
            name = extract_metadata_field(content, "name")
            related = extract_related_commands(content)

            for ref in related:
                cmd_name = ref.lstrip("/")
                # Find the referenced command
                for ref_file in files:
                    ref_name = extract_metadata_field(ref_file.read_text(), "name")
                    if ref_name == cmd_name:
                        # Check if ref_file references back to name
                        ref_content = ref_file.read_text()
                        ref_related = extract_related_commands(ref_content)
                        if f"/pb-{name}" in ref_related and name != cmd_name:
                            circulars.append(f"{name} ↔ {cmd_name} (bidirectional)")

        # Note: Some bidirectional refs are intentional (e.g., pb-preamble ↔ design-rules)
        # So we just log them rather than fail
        if circulars:
            print("\n⚠️  Bidirectional references detected:")
            for c in set(circulars):
                print(f"  {c}")
