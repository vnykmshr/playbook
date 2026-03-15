#!/usr/bin/env python3
"""Check internal links in mdbook output.

Verifies that every href pointing to a local file resolves to an
existing file. Run after build-mdbook.sh.

Skips: external links, anchors, example/template links inside code
blocks, the print.html page (concatenates all pages, duplicates issues).

Usage: python3 scripts/check-links.py [mdbook-out/]
"""
import re
import sys
from pathlib import Path

# Links that are examples in command prose, not real references
EXAMPLE_PATTERNS = [
    "/products", "/about", "/", "/api",
    "style.css", "critical.css", "non-critical.css",
    "docs/architecture", "docs/api.html", "docs/contributing",
    "docs/troubleshooting", "docs/advanced-migrations",
    "docs/deployment-automation", "docs/emergency-deploy",
    "docs/kubernetes-deployment", "docs/api-errors",
    ".github/workflows/deploy.yml",
]


def is_example_link(href):
    """Check if a link is an illustrative example, not a real reference."""
    for pattern in EXAMPLE_PATTERNS:
        if pattern in href:
            return True
    return False


def main():
    out_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("mdbook-out")

    if not out_dir.is_dir():
        print(f"Error: {out_dir}/ not found. Run build-mdbook.sh first.")
        sys.exit(1)

    href_re = re.compile(r'href="([^"]+)"')
    skip_prefixes = ("http://", "https://", "mailto:", "javascript:", "#")

    checked = 0
    broken = []

    html_files = sorted(out_dir.rglob("*.html"))

    for html_file in html_files:
        # Skip print.html (concatenation of all pages, duplicates everything)
        if html_file.name == "print.html":
            continue
        # Skip 404.html
        if html_file.name == "404.html":
            continue

        page_dir = html_file.parent
        content = html_file.read_text(errors="ignore")

        for match in href_re.finditer(content):
            href = match.group(1)

            if href.startswith(skip_prefixes):
                continue

            target = href.split("#")[0]
            if not target:
                continue

            if is_example_link(target):
                continue

            checked += 1

            # Handle absolute paths (start with /)
            if target.startswith("/"):
                resolved = (out_dir / target.lstrip("/")).resolve()
            else:
                resolved = (page_dir / target).resolve()

            if not resolved.is_file():
                index_fallback = resolved / "index.html"
                if not index_fallback.is_file():
                    rel_page = html_file.relative_to(out_dir)
                    broken.append((str(rel_page), href))

    page_count = len([f for f in html_files if f.name not in ("print.html", "404.html")])
    print(f"Checked {checked} internal links across {page_count} pages")

    if broken:
        print(f"\n{len(broken)} broken links:\n")
        for page, href in broken:
            print(f"  {page} -> {href}")
        sys.exit(1)
    else:
        print("All internal links valid")


if __name__ == "__main__":
    main()
