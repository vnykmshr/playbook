#!/usr/bin/env python3
"""
Evolution Snapshot & Rollback Management

Creates snapshots before evolution, enables safe rollback if needed.

Usage:
    # Create snapshot before evolution
    python3 scripts/evolution-snapshot.py --create "Snapshot before Q1 evolution"

    # List available snapshots
    python3 scripts/evolution-snapshot.py --list

    # Show snapshot info
    python3 scripts/evolution-snapshot.py --show <snapshot-id>

    # Rollback to snapshot
    python3 scripts/evolution-snapshot.py --rollback <snapshot-id>
"""

import json
import sys
import subprocess
from datetime import datetime
from pathlib import Path


class EvolutionSnapshot:
    """Manage evolution snapshots for safe rollback."""

    def __init__(self):
        self.snapshots_dir = Path("todos/evolution-snapshots")
        self.snapshots_dir.mkdir(exist_ok=True)
        self.snapshots_file = self.snapshots_dir / "snapshots.json"
        self._load_snapshots()

    def _load_snapshots(self):
        """Load existing snapshots metadata."""
        if self.snapshots_file.exists():
            with open(self.snapshots_file) as f:
                self.snapshots = json.load(f) or {}
        else:
            self.snapshots = {}

    def _save_snapshots(self):
        """Save snapshots metadata."""
        with open(self.snapshots_file, 'w') as f:
            json.dump(self.snapshots, f, indent=2)

    def create(self, message: str) -> str:
        """Create a snapshot before evolution.

        Returns: snapshot_id
        """
        # Create git tag (primary backup)
        snapshot_id = f"evolution-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

        print(f"\n📸 Creating snapshot: {snapshot_id}")

        # Get current commit hash
        try:
            commit = subprocess.check_output(
                ["git", "rev-parse", "HEAD"],
                text=True
            ).strip()
        except subprocess.CalledProcessError as e:
            print(f"❌ Error getting commit hash: {e}")
            return None

        # Create git tag
        try:
            subprocess.run(
                ["git", "tag", "-a", snapshot_id, "-m", f"Evolution snapshot: {message}"],
                check=True
            )
            print(f"  ✅ Git tag created: {snapshot_id}")
        except subprocess.CalledProcessError as e:
            print(f"  ❌ Failed to create git tag: {e}")
            return None

        # Record metadata
        self.snapshots[snapshot_id] = {
            "created_at": datetime.now().isoformat(),
            "message": message,
            "commit": commit,
            "branch": subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                text=True
            ).strip(),
            "status": "active",
        }
        self._save_snapshots()

        print(f"  ✅ Metadata saved\n")
        return snapshot_id

    def list_snapshots(self):
        """List all available snapshots."""
        if not self.snapshots:
            print("No snapshots found.\n")
            return

        print("\n📋 Available Evolution Snapshots:\n")
        for snapshot_id, metadata in sorted(self.snapshots.items(), reverse=True):
            print(f"  {snapshot_id}")
            print(f"    Message: {metadata['message']}")
            print(f"    Created: {metadata['created_at']}")
            print(f"    Commit: {metadata['commit'][:8]}")
            print(f"    Branch: {metadata['branch']}")
            print(f"    Status: {metadata['status']}")
            print()

    def show(self, snapshot_id: str):
        """Show details of a specific snapshot."""
        if snapshot_id not in self.snapshots:
            print(f"❌ Snapshot not found: {snapshot_id}\n")
            return

        metadata = self.snapshots[snapshot_id]
        print(f"\n📸 Snapshot Details: {snapshot_id}\n")
        print(f"  Message: {metadata['message']}")
        print(f"  Created: {metadata['created_at']}")
        print(f"  Commit: {metadata['commit']}")
        print(f"  Branch: {metadata['branch']}")
        print(f"  Status: {metadata['status']}")
        print()

        # Show git tag info
        try:
            tag_info = subprocess.check_output(
                ["git", "show", snapshot_id],
                text=True,
                stderr=subprocess.DEVNULL
            ).split('\n')[:10]
            print("  Git tag info:")
            for line in tag_info:
                if line:
                    print(f"    {line}")
        except subprocess.CalledProcessError:
            pass

        print()

    def rollback(self, snapshot_id: str, force: bool = False) -> bool:
        """Rollback to a snapshot.

        Returns: success (bool)
        """
        if snapshot_id not in self.snapshots:
            print(f"❌ Snapshot not found: {snapshot_id}\n")
            return False

        metadata = self.snapshots[snapshot_id]
        commit = metadata['commit']

        print(f"\n⚠️  Rollback Warning:")
        print(f"   You are about to rollback to:")
        print(f"   Snapshot: {snapshot_id}")
        print(f"   Message: {metadata['message']}")
        print(f"   Commit: {commit}")
        print(f"\n   This will:")
        print(f"   1. Reset working tree to this commit")
        print(f"   2. Discard all evolution changes since then")
        print(f"   3. Create a rollback commit")
        print()

        if not force:
            response = input("   Proceed with rollback? (yes/no): ").strip().lower()
            if response != "yes":
                print("   ❌ Rollback cancelled.\n")
                return False

        # Check working tree is clean
        try:
            status = subprocess.check_output(
                ["git", "status", "--porcelain"],
                text=True
            ).strip()
            if status:
                print("❌ Working tree is dirty. Commit or stash changes first.\n")
                return False
        except subprocess.CalledProcessError as e:
            print(f"❌ Error checking git status: {e}\n")
            return False

        # Perform rollback
        print(f"\n🔄 Rolling back...")
        try:
            subprocess.run(
                ["git", "reset", "--hard", commit],
                check=True
            )
            print(f"   ✅ Reset to commit {commit[:8]}")

            # Create rollback marker
            rollback_message = f"rollback: restored from snapshot {snapshot_id}\n\nOriginal message: {metadata['message']}"
            subprocess.run(
                ["git", "commit", "--allow-empty", "-m", rollback_message],
                check=True
            )
            print(f"   ✅ Rollback commit created")

            # Update snapshot status
            metadata['status'] = 'used'
            self._save_snapshots()
            print(f"   ✅ Snapshot marked as used\n")
            return True

        except subprocess.CalledProcessError as e:
            print(f"   ❌ Rollback failed: {e}\n")
            return False

    def cleanup_old_snapshots(self, keep: int = 5):
        """Remove old snapshots (keep N most recent)."""
        if len(self.snapshots) <= keep:
            print(f"Only {len(self.snapshots)} snapshots. Keeping all.\n")
            return

        # Sort by creation date
        sorted_snapshots = sorted(
            self.snapshots.items(),
            key=lambda x: x[1]['created_at'],
            reverse=True
        )

        to_delete = sorted_snapshots[keep:]
        print(f"\n🗑️  Cleaning up old snapshots (keeping {keep} most recent)\n")

        for snapshot_id, _ in to_delete:
            print(f"  Deleting: {snapshot_id}")
            try:
                subprocess.run(
                    ["git", "tag", "-d", snapshot_id],
                    check=True
                )
                del self.snapshots[snapshot_id]
            except subprocess.CalledProcessError as e:
                print(f"    ❌ Failed to delete tag: {e}")

        self._save_snapshots()
        print()


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Evolution Snapshot Management"
    )
    parser.add_argument(
        "--create",
        type=str,
        help="Create a snapshot with message"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all snapshots"
    )
    parser.add_argument(
        "--show",
        type=str,
        help="Show snapshot details"
    )
    parser.add_argument(
        "--rollback",
        type=str,
        help="Rollback to snapshot"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force rollback without confirmation"
    )
    parser.add_argument(
        "--cleanup",
        type=int,
        default=5,
        help="Cleanup old snapshots, keep N most recent (default: 5)"
    )

    args = parser.parse_args()

    snapshot = EvolutionSnapshot()

    if args.create:
        snapshot_id = snapshot.create(args.create)
        if snapshot_id:
            print(f"✅ Snapshot created: {snapshot_id}\n")
        sys.exit(0 if snapshot_id else 1)

    elif args.list:
        snapshot.list_snapshots()
        sys.exit(0)

    elif args.show:
        snapshot.show(args.show)
        sys.exit(0)

    elif args.rollback:
        success = snapshot.rollback(args.rollback, force=args.force)
        sys.exit(0 if success else 1)

    else:
        # Default: list snapshots
        snapshot.list_snapshots()
        sys.exit(0)


if __name__ == "__main__":
    main()
