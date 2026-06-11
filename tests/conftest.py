"""Shared helpers for the scripts/ tooling tests.

Most tooling lives in scripts/ as hyphenated files (e.g. evolution-snapshot.py)
that Python can't import by name. `load_script` loads one by path so a test can
call its functions directly. `make_command` writes a throwaway but schema-valid
pb-*.md (mirroring a real command) so the metadata/convention tools get realistic
input; pass field=value to override a field, field=None to omit it.
"""
import importlib.util
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
# scripts share playbook_utils; make it importable for module-loaded scripts.
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))


def _load_script(filename):
    path = SCRIPTS_DIR / filename
    spec = importlib.util.spec_from_file_location(path.stem.replace("-", "_"), path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def load_script():
    """Load a scripts/ file (hyphenated names allowed) as a module."""
    return _load_script


def _default_fields(name):
    # Verbatim YAML right-hand sides, quoted as the real command files are.
    return {
        "name": f'"{name}"',
        "title": '"Example Command"',
        "category": '"development"',
        "difficulty": '"beginner"',
        "model_hint": '"sonnet"',
        "execution_pattern": '"sequential"',
        "related_commands": "['pb-start']",
        "last_reviewed": '"2026-06-10"',
        "last_evolved": '"2026-06-10"',
        "version": '"1.0.0"',
        "version_notes": '"v1.0.0: initial."',
        "breaking_changes": "[]",
    }


def _make_command(directory, name="pb-example", **overrides):
    fields = _default_fields(name)
    for key, value in overrides.items():
        if value is None:
            fields.pop(key, None)
        else:
            fields[key] = value
    body = ["---"]
    body += [f"{k}: {v}" for k, v in fields.items()]
    body += ["---", "", f"# {name}", ""]
    path = Path(directory) / f"{name}.md"
    path.write_text("\n".join(body) + "\n")
    return path


@pytest.fixture
def make_command():
    """Write a schema-valid pb-*.md into a directory; returns the writer."""
    return _make_command
