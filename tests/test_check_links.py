"""check-links.py reads the built site as the live host serves it, under book.toml's site-url."""
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def check(out: Path, href: str) -> subprocess.CompletedProcess[str]:
    (out / "docs").mkdir(parents=True, exist_ok=True)
    _ = (out / "docs" / "a.html").write_text("<p>a</p>\n")
    _ = (out / "page.html").write_text(f'<p><a href="{href}">a</a></p>\n<pre>&lt;a href="/"&gt;sample&lt;/a&gt;</pre>\n')
    return subprocess.run(
        [sys.executable, str(REPO / "scripts" / "check-links.py"), str(out)], capture_output=True, text=True
    )


def test_a_root_path_outside_the_site_path_is_broken(tmp_path: Path):
    r = check(tmp_path, "/docs/a.html")
    assert r.returncode == 1 and "/docs/a.html" in r.stdout, r.stdout


def test_a_root_path_under_the_site_path_resolves(tmp_path: Path):
    r = check(tmp_path, "/playbook/docs/a.html")
    assert r.returncode == 0, r.stdout


def test_escaped_sample_text_is_not_a_link(tmp_path: Path):
    r = check(tmp_path, "docs/a.html")
    assert r.returncode == 0 and "Checked 1 internal links" in r.stdout, r.stdout
