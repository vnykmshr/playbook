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
    name = path.stem.replace("-", "_")
    cached = sys.modules.get(name)
    if cached is not None:
        # The key is the normalized stem, so foo-bar.py and foo_bar.py collide.
        # Returning whichever loaded first would be a silent wrong answer.
        if getattr(cached, "__file__", None) != str(path):
            raise ImportError(
                f"{name} is already loaded from {getattr(cached, '__file__', '?')}; "
                f"refusing to shadow it with {path}"
            )
        return cached
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    # Register before exec: mock.patch("<name>.attr") resolves through
    # importlib.import_module, which reads sys.modules and never sees a
    # hyphenated file on disk.
    # Consequence: callers now share one module instance instead of getting a
    # freshly executed one. Mutate module-level state through monkeypatch (which
    # unwinds) rather than by assignment, or it leaks into later tests.
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        del sys.modules[name]
        raise
    return module


# Two test modules import these by name at import time rather than calling
# functions by path, and patch attributes on them by string. Registering here
# is what makes that resolve; it replaces the scripts/*_*.py symlinks that
# used to exist purely to give these two an importable spelling.
_load_script("git-signals.py")
_load_script("analyze-playbook-context.py")


@pytest.fixture(scope="session")
def load_script():
    """Load a scripts/ file (hyphenated names allowed) as a module.

    Session-scoped so module-scoped fixtures can consume it; it only hands back
    a stateless loader, so the scope is invisible to callers.
    """
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
