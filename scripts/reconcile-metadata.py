#!/usr/bin/env python3
"""
Reconcile metadata model_hint with body Resource Hint.

Scans all command files for body Resource Hint: and updates metadata
model_hint to match (body is authoritative from v2.8.0 audit).

Usage:
    python3 scripts/reconcile-metadata.py --check   # Show conflicts
    python3 scripts/reconcile-metadata.py --fix     # Fix conflicts
"""

import re
import sys
from pathlib import Path


def extract_resource_hint(content: str) -> str | None:
    """Extract Resource Hint model from body.

    Looking for patterns like:
    **Resource Hint:** sonnet — Description
    **Resource Hint:** opus — Description
    **Resource Hint:** haiku — Description
    """
    match = re.search(r'\*\*Resource Hint:\*\*\s+(sonnet|opus|haiku)', content)
    if match:
        return match.group(1)
    return None


def extract_frontmatter(content: str) -> tuple[dict, str]:
    """Extract YAML front-matter and return (metadata dict, rest of content)."""
    if not content.startswith("---"):
        return {}, content

    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not match:
        return {}, content

    yaml_content = match.group(1)
    rest = content[match.end():]

    metadata = {}
    for line in yaml_content.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        if ':' not in line:
            continue

        key, _, value = line.partition(':')
        key = key.strip()
        value = value.strip()
        metadata[key] = value

    return metadata, rest


def update_metadata_model_hint(content: str, new_model_hint: str) -> str:
    """Update model_hint in YAML front-matter."""
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not match:
        return content

    yaml_content = match.group(1)
    rest = content[match.end():]

    # Update the model_hint line
    new_yaml = re.sub(
        r'model_hint:\s*"[^"]*"',
        f'model_hint: "{new_model_hint}"',
        yaml_content
    )

    return f"---\n{new_yaml}\n---\n{rest}"


def main():
    import sys

    action = sys.argv[1] if len(sys.argv) > 1 else "--check"

    root = Path(__file__).parent.parent
    commands_dir = root / "commands"

    conflicts = []

    for filepath in sorted(commands_dir.glob("**/pb-*.md")):
        with open(filepath) as f:
            content = f.read()

        # Extract resource hint from body
        body_hint = extract_resource_hint(content)

        # Extract metadata model_hint
        metadata, _ = extract_frontmatter(content)
        meta_hint = metadata.get('model_hint', '').strip('"')

        # Check for conflict
        if body_hint and meta_hint and body_hint != meta_hint:
            conflicts.append({
                'file': filepath.name,
                'path': filepath,
                'body_hint': body_hint,
                'meta_hint': meta_hint
            })

    if action == "--check":
        if conflicts:
            print(f"\n🔴 Found {len(conflicts)} conflicts (body vs metadata):\n")
            for item in conflicts:
                print(f"  {item['file']}")
                print(f"    Body says: {item['body_hint']}")
                print(f"    Meta says: {item['meta_hint']}")
                print()
        else:
            print("\n✅ No conflicts found. Metadata is consistent with body Resource Hints.\n")
        return

    if action == "--fix":
        if not conflicts:
            print("\n✅ No conflicts to fix.\n")
            return

        print(f"\n🔧 Fixing {len(conflicts)} conflicts...\n")

        for item in conflicts:
            filepath = item['path']
            new_model = item['body_hint']

            with open(filepath) as f:
                content = f.read()

            # Update the metadata
            updated_content = update_metadata_model_hint(content, new_model)

            with open(filepath, 'w') as f:
                f.write(updated_content)

            print(f"  ✅ {item['file']}: {item['meta_hint']} → {new_model}")

        print(f"\n✅ Fixed {len(conflicts)} conflicts.\n")
        return

    print("Usage: python3 scripts/reconcile-metadata.py --check|--fix")
    sys.exit(1)


if __name__ == "__main__":
    main()
