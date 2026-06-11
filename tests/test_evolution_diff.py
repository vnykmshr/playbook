"""Regression test for evolution-diff.py report header."""
import re
from datetime import datetime


def test_generated_field_is_timestamp(tmp_path, load_script):
    """#12: the report's Generated field must be a timestamp, not the basename of
    the current working directory (Path('').absolute().name)."""
    ed = load_script("evolution-diff.py")
    out = tmp_path / "report.md"

    ed.EvolutionDiff().generate_markdown_report({}, str(out))

    content = out.read_text()
    m = re.search(r'^\*\*Generated:\*\* (.+)$', content, re.MULTILINE)
    assert m, content
    # Must parse as an ISO timestamp; a cwd basename would raise here.
    datetime.fromisoformat(m.group(1).strip())
