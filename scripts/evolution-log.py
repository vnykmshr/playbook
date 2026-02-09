#!/usr/bin/env python3
"""
Structured Evolution Log Management

Maintains machine-readable evolution audit trail.
Replaces narrative todos/evolution-log.md with structured JSON.

This enables:
- Pattern detection (what typically changes?)
- Impact analysis (do changes help or hurt?)
- Regression detection (did a previous evolution fix work?)
- Future automation (predict what needs evolution)

Usage:
    # Record a new evolution
    python3 scripts/evolution-log.py --record-cycle "Q1 2026" \
      --trigger "quarterly" \
      --capability-changes "Sonnet 4.6 30% faster"

    # Record a command change within current cycle
    python3 scripts/evolution-log.py --record-change pb-start \
      --field model_hint \
      --before sonnet \
      --after opus \
      --rationale "Architecture decisions now within Sonnet 4.6 capability"

    # View evolution history
    python3 scripts/evolution-log.py --show

    # Analyze patterns
    python3 scripts/evolution-log.py --analyze
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from collections import defaultdict


class EvolutionLog:
    """Manage structured evolution audit trail."""

    def __init__(self):
        self.log_file = Path("todos/evolution-audit.json")
        self._load_log()

    def _load_log(self):
        """Load existing log."""
        if self.log_file.exists():
            with open(self.log_file) as f:
                self.log = json.load(f) or {"cycles": [], "version": "1.0"}
        else:
            self.log = {"cycles": [], "version": "1.0"}

    def _save_log(self):
        """Save log."""
        self.log_file.parent.mkdir(exist_ok=True)
        with open(self.log_file, 'w') as f:
            json.dump(self.log, f, indent=2)

    def record_cycle(self, cycle_name: str, trigger: str, capability_changes: str) -> dict:
        """Record a new evolution cycle."""
        cycle = {
            "cycle": cycle_name,
            "started_at": datetime.now().isoformat(),
            "trigger": trigger,  # "quarterly", "version_upgrade", "user_feedback", "manual"
            "capability_changes": capability_changes,
            "changes": [],
            "status": "in_progress",  # "in_progress", "completed", "reverted"
            "snapshot_id": None,
            "pr_number": None,
        }

        self.log["cycles"].append(cycle)
        self._save_log()

        print(f"✅ Evolution cycle recorded: {cycle_name}\n")
        return cycle

    def record_change(self, cycle_name: str, command: str, field: str,
                     before: str, after: str, rationale: str) -> bool:
        """Record a change within current cycle."""
        # Find the cycle
        cycle = None
        for c in self.log["cycles"]:
            if c["cycle"] == cycle_name and c["status"] == "in_progress":
                cycle = c
                break

        if not cycle:
            print(f"❌ No active cycle: {cycle_name}\n")
            return False

        # Record the change
        change = {
            "command": command,
            "field": field,
            "before": before,
            "after": after,
            "rationale": rationale,
            "recorded_at": datetime.now().isoformat(),
        }

        cycle["changes"].append(change)
        self._save_log()

        print(f"✅ Change recorded: {command}.{field}: {before} → {after}\n")
        return True

    def set_cycle_snapshot(self, cycle_name: str, snapshot_id: str) -> bool:
        """Link cycle to snapshot."""
        for c in self.log["cycles"]:
            if c["cycle"] == cycle_name:
                c["snapshot_id"] = snapshot_id
                self._save_log()
                print(f"✅ Snapshot linked: {snapshot_id}\n")
                return True

        print(f"❌ Cycle not found: {cycle_name}\n")
        return False

    def complete_cycle(self, cycle_name: str, pr_number: int = None) -> bool:
        """Mark cycle as complete."""
        for c in self.log["cycles"]:
            if c["cycle"] == cycle_name:
                c["status"] = "completed"
                c["completed_at"] = datetime.now().isoformat()
                if pr_number:
                    c["pr_number"] = pr_number
                self._save_log()
                print(f"✅ Evolution cycle completed: {cycle_name}\n")
                return True

        print(f"❌ Cycle not found: {cycle_name}\n")
        return False

    def revert_cycle(self, cycle_name: str, reason: str) -> bool:
        """Mark cycle as reverted (if it broke something)."""
        for c in self.log["cycles"]:
            if c["cycle"] == cycle_name:
                c["status"] = "reverted"
                c["reverted_at"] = datetime.now().isoformat()
                c["revert_reason"] = reason
                self._save_log()
                print(f"⚠️  Evolution cycle reverted: {cycle_name}\n")
                print(f"   Reason: {reason}\n")
                return True

        print(f"❌ Cycle not found: {cycle_name}\n")
        return False

    def show_history(self):
        """Display evolution history."""
        if not self.log["cycles"]:
            print("No evolution cycles recorded.\n")
            return

        print("\n📜 Evolution History\n")
        print("=" * 80)

        for cycle in reversed(self.log["cycles"]):
            print(f"\n{cycle['cycle']}")
            print(f"  Status: {cycle['status']}")
            print(f"  Started: {cycle['started_at']}")
            print(f"  Trigger: {cycle['trigger']}")
            print(f"  Capabilities: {cycle['capability_changes']}")
            print(f"  Changes: {len(cycle['changes'])} command(s)")
            if cycle.get('snapshot_id'):
                print(f"  Snapshot: {cycle['snapshot_id']}")
            if cycle.get('pr_number'):
                print(f"  PR: #{cycle['pr_number']}")

            if cycle["changes"]:
                print(f"\n  Changes:")
                for change in cycle["changes"]:
                    print(f"    • {change['command']}.{change['field']}: "
                          f"{change['before']} → {change['after']}")
                    print(f"      {change['rationale']}")

        print("\n" + "=" * 80 + "\n")

    def analyze_patterns(self):
        """Analyze patterns in evolution history."""
        if not self.log["cycles"]:
            print("No evolution cycles to analyze.\n")
            return

        print("\n🔬 Evolution Pattern Analysis\n")
        print("=" * 80)

        # Count changes by field
        field_changes = defaultdict(int)
        field_transitions = defaultdict(lambda: defaultdict(int))

        for cycle in self.log["cycles"]:
            for change in cycle["changes"]:
                field = change["field"]
                before = change["before"]
                after = change["after"]

                field_changes[field] += 1
                field_transitions[field][(before, after)] += 1

        print("\nMost Frequently Changed Fields:")
        for field, count in sorted(field_changes.items(), key=lambda x: -x[1])[:5]:
            print(f"  {field}: {count} changes")

        print("\nCommon Transitions:")
        for field, transitions in field_transitions.items():
            print(f"\n  {field}:")
            for (before, after), count in sorted(
                transitions.items(),
                key=lambda x: -x[1]
            )[:3]:
                print(f"    {before} → {after}: {count} times")

        # Analyze by cycle trigger
        print("\nEvolution by Trigger Type:")
        triggers = defaultdict(int)
        for cycle in self.log["cycles"]:
            triggers[cycle["trigger"]] += 1

        for trigger, count in sorted(triggers.items()):
            print(f"  {trigger}: {count} cycle(s)")

        print("\n" + "=" * 80 + "\n")

    def export_timeline(self, output_file: str = "todos/evolution-timeline.json"):
        """Export timeline for visualization."""
        timeline = []

        for cycle in self.log["cycles"]:
            timeline.append({
                "cycle": cycle["cycle"],
                "date": cycle["started_at"],
                "changes": len(cycle["changes"]),
                "status": cycle["status"],
            })

        with open(output_file, 'w') as f:
            json.dump(timeline, f, indent=2)

        print(f"✅ Timeline exported to: {output_file}\n")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Evolution Log Manager"
    )
    parser.add_argument(
        "--record-cycle",
        type=str,
        help="Record a new evolution cycle"
    )
    parser.add_argument(
        "--trigger",
        type=str,
        choices=["quarterly", "version_upgrade", "user_feedback", "manual"],
        default="manual",
        help="What triggered this evolution"
    )
    parser.add_argument(
        "--capability-changes",
        type=str,
        help="Description of Claude capability changes"
    )
    parser.add_argument(
        "--record-change",
        type=str,
        metavar="COMMAND",
        help="Record a change within current cycle"
    )
    parser.add_argument(
        "--field",
        type=str,
        help="Field that changed"
    )
    parser.add_argument(
        "--before",
        type=str,
        help="Value before"
    )
    parser.add_argument(
        "--after",
        type=str,
        help="Value after"
    )
    parser.add_argument(
        "--rationale",
        type=str,
        help="Why this change was made"
    )
    parser.add_argument(
        "--cycle",
        type=str,
        help="Cycle name (for recording changes)"
    )
    parser.add_argument(
        "--snapshot",
        type=str,
        help="Link snapshot ID to cycle"
    )
    parser.add_argument(
        "--complete",
        type=str,
        metavar="CYCLE",
        help="Mark cycle as complete"
    )
    parser.add_argument(
        "--pr",
        type=int,
        help="PR number (with --complete)"
    )
    parser.add_argument(
        "--revert",
        type=str,
        metavar="CYCLE",
        help="Mark cycle as reverted"
    )
    parser.add_argument(
        "--reason",
        type=str,
        help="Revert reason"
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Show evolution history"
    )
    parser.add_argument(
        "--analyze",
        action="store_true",
        help="Analyze evolution patterns"
    )

    args = parser.parse_args()

    log = EvolutionLog()

    if args.record_cycle:
        log.record_cycle(
            args.record_cycle,
            args.trigger,
            args.capability_changes or ""
        )
        sys.exit(0)

    elif args.record_change:
        if not (args.cycle and args.field and args.before and args.after and args.rationale):
            print("❌ Missing required arguments for recording change.\n")
            parser.print_help()
            sys.exit(1)
        log.record_change(
            args.cycle,
            args.record_change,
            args.field,
            args.before,
            args.after,
            args.rationale
        )
        sys.exit(0)

    elif args.snapshot:
        log.set_cycle_snapshot(args.cycle, args.snapshot)
        sys.exit(0)

    elif args.complete:
        log.complete_cycle(args.complete, args.pr)
        sys.exit(0)

    elif args.revert:
        log.revert_cycle(args.revert, args.reason or "No reason provided")
        sys.exit(0)

    elif args.show:
        log.show_history()
        sys.exit(0)

    elif args.analyze:
        log.analyze_patterns()
        sys.exit(0)

    else:
        log.show_history()
        sys.exit(0)


if __name__ == "__main__":
    main()
