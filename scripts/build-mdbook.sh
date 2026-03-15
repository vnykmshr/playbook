#!/usr/bin/env bash
# Build the mdbook reference site.
# Copies source files to mdbook-src/, strips YAML frontmatter, runs mdbook build.
# Source files are never modified.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/mdbook-src"
OUT="$ROOT/mdbook-out"

echo "Preparing mdbook source..."

# Clean previous build
rm -rf "$SRC" "$OUT"
mkdir -p "$SRC"

# Copy docs and commands into mdbook source
cp -r "$ROOT/docs" "$SRC/docs"
cp -r "$ROOT/commands" "$SRC/commands"

# Copy mdbook config files
cp "$ROOT/mdbook/book.toml" "$SRC/book.toml"
cp "$ROOT/mdbook/SUMMARY.md" "$SRC/SUMMARY.md"
cp "$ROOT/mdbook/intro.md" "$SRC/intro.md"
cp -r "$ROOT/mdbook/theme" "$SRC/theme" 2>/dev/null || true
cp "$ROOT/mdbook/mermaid.min.js" "$SRC/" 2>/dev/null || true
cp "$ROOT/mdbook/mermaid-init.js" "$SRC/" 2>/dev/null || true

# Strip YAML frontmatter from all .md files in commands/
echo "Stripping YAML frontmatter..."
find "$SRC/commands" -name '*.md' | while read -r f; do
  python3 -c "
import sys
with open('$f') as fh:
    lines = fh.readlines()
if lines and lines[0].strip() == '---':
    # Find closing ---
    for i in range(1, len(lines)):
        if lines[i].strip() == '---':
            lines = lines[i+1:]
            break
with open('$f', 'w') as fh:
    fh.writelines(lines)
"
done

# Build
echo "Building mdbook..."
cd "$SRC"
mdbook build --dest-dir "$OUT"

echo "Done. Output in mdbook-out/"
echo "Files: $(find "$OUT" -name '*.html' | wc -l | tr -d ' ') HTML pages"
