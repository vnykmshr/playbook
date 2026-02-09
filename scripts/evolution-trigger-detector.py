#!/usr/bin/env python3
"""
Evolution Trigger Detection

Automatically detects when evolution is needed based on multiple signals:
1. Time since last evolution (staleness)
2. Command metadata staleness (last_reviewed dates)
3. Claude version changes
4. User feedback signals

This is a reporting tool, not automatic action. Always requires human approval.

Usage:
    python3 scripts/evolution-trigger-detector.py --check

    python3 scripts/evolution-trigger-detector.py --report > evolution-triggers.md
"""

import json
import re
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict


class EvolutionTriggerDetector:
    """Detect signals that evolution is needed."""

    def __init__(self):
        self.commands_dir = Path("commands")
        self.log_file = Path("todos/evolution-audit.json")
        self.triggers = []

    def check_time_since_last_evolution(self, threshold_days: int = 90) -> dict | None:
        """Check if enough time has passed since last evolution."""
        if not self.log_file.exists():
            return {
                "type": "first_evolution",
                "severity": "info",
                "message": "No evolution cycles recorded yet. This is the first!",
            }

        with open(self.log_file) as f:
            log = json.load(f)

        if not log.get("cycles"):
            return {
                "type": "no_history",
                "severity": "info",
                "message": "Evolution log is empty.",
            }

        last_cycle = log["cycles"][-1]
        last_date = datetime.fromisoformat(last_cycle["started_at"])
        days_since = (datetime.now() - last_date).days

        if days_since >= threshold_days:
            return {
                "type": "calendar_trigger",
                "severity": "high",
                "days_since_last": days_since,
                "message": f"It's been {days_since} days since last evolution (threshold: {threshold_days} days)",
                "recommendation": f"Schedule evolution now (last was {last_cycle['cycle']})",
            }

        return None

    def check_command_staleness(self, threshold_days: int = 180) -> dict | None:
        """Check if commands have stale last_reviewed dates."""
        stale_commands = []
        cutoff_date = (datetime.now() - timedelta(days=threshold_days)).date()

        for filepath in sorted(self.commands_dir.glob("**/pb-*.md")):
            with open(filepath) as f:
                content = f.read()

            # Extract last_reviewed date
            match = re.search(r'^last_reviewed:\s*"([^"]+)"', content, re.MULTILINE)
            if match:
                try:
                    reviewed_date = datetime.fromisoformat(match.group(1)).date()
                    if reviewed_date <= cutoff_date:
                        days_stale = (datetime.now().date() - reviewed_date).days
                        stale_commands.append({
                            "command": filepath.stem,
                            "last_reviewed": str(reviewed_date),
                            "days_stale": days_stale,
                        })
                except ValueError:
                    pass

        if len(stale_commands) > len(self.get_all_commands()) * 0.25:  # > 25%
            return {
                "type": "staleness_trigger",
                "severity": "medium",
                "stale_count": len(stale_commands),
                "total_commands": len(self.get_all_commands()),
                "message": f"{len(stale_commands)} commands have stale reviews (>{threshold_days} days old)",
                "recommendation": f"Evolution cycle would update {len(stale_commands)} commands",
                "stale_commands": stale_commands[:10],  # Show top 10
            }

        return None

    def check_claude_version_change(self) -> dict | None:
        """Check if Claude version has changed significantly.

        Note: This requires manual input since we can't query version directly.
        """
        # Placeholder: In real implementation, check against saved version
        # For now, check CLAUDE.md or CHANGELOG for version hints
        changelog_path = Path("CHANGELOG.md")

        if changelog_path.exists():
            with open(changelog_path) as f:
                content = f.read()

            # Look for recent Claude version mentions
            claude_versions = re.findall(r'Claude (\d+\.\d+)', content)
            if claude_versions and len(claude_versions) >= 2:
                latest = claude_versions[0]
                if latest != claude_versions[1]:
                    return {
                        "type": "version_upgrade",
                        "severity": "high",
                        "new_version": latest,
                        "message": f"Claude version upgraded to {latest}",
                        "recommendation": "Run evolution to optimize for new capabilities",
                    }

        return None

    def check_git_log_for_user_feedback(self) -> dict | None:
        """Look for feedback signals in recent git history.

        Searches for commit messages or issue comments mentioning playbook gaps.
        """
        # Placeholder: In real implementation, parse issues/PRs via GitHub API
        # For now, just check if there are recent TODOs
        todos_dir = Path("todos")

        if todos_dir.exists():
            # Check for playbook-related TODOs
            feedback_files = list(todos_dir.glob("*feedback*"))
            if feedback_files:
                feedback_count = sum(1 for f in feedback_files if f.stat().st_size > 0)
                if feedback_count > 0:
                    return {
                        "type": "user_feedback",
                        "severity": "medium",
                        "feedback_items": feedback_count,
                        "message": f"Found {feedback_count} items of user feedback",
                        "recommendation": "Review feedback in evolution cycle",
                    }

        return None

    def get_all_commands(self):
        """Get list of all commands."""
        return list(self.commands_dir.glob("**/pb-*.md"))

    def run_detection(self) -> list[dict]:
        """Run all trigger detection checks."""
        triggers = []

        # Check 1: Time since last evolution
        time_trigger = self.check_time_since_last_evolution()
        if time_trigger:
            triggers.append(time_trigger)

        # Check 2: Command staleness
        staleness_trigger = self.check_command_staleness()
        if staleness_trigger:
            triggers.append(staleness_trigger)

        # Check 3: Claude version change
        version_trigger = self.check_claude_version_change()
        if version_trigger:
            triggers.append(version_trigger)

        # Check 4: User feedback
        feedback_trigger = self.check_git_log_for_user_feedback()
        if feedback_trigger:
            triggers.append(feedback_trigger)

        return triggers

    def print_check_summary(self, triggers: list[dict]):
        """Print human-readable summary."""
        if not triggers:
            print("✅ No evolution triggers detected.\n")
            print("   System is healthy. Continue normal operations.\n")
            return

        print(f"\n⚠️  Evolution Triggers Detected: {len(triggers)}\n")

        for i, trigger in enumerate(triggers, 1):
            severity = trigger["severity"]
            trigger_type = trigger["type"]
            message = trigger["message"]

            severity_icon = {
                "high": "🔴",
                "medium": "🟡",
                "info": "ℹ️ ",
            }.get(severity, "❓")

            print(f"{i}. {severity_icon} [{severity.upper()}] {trigger_type}")
            print(f"   {message}")
            if "recommendation" in trigger:
                print(f"   → {trigger['recommendation']}")
            print()

    def generate_markdown_report(self, triggers: list[dict], output_file: str = "todos/evolution-triggers.md") -> None:
        """Generate markdown report of triggers."""
        with open(output_file, 'w') as f:
            f.write("# Evolution Triggers Report\n\n")
            f.write(f"**Generated:** {datetime.now().isoformat()}\n\n")

            if not triggers:
                f.write("✅ No evolution triggers detected.\n\n")
                return

            f.write(f"## Summary\n\n")
            f.write(f"Found {len(triggers)} trigger(s) for evolution:\n\n")

            for trigger in triggers:
                severity = trigger["severity"]
                trigger_type = trigger["type"]
                message = trigger["message"]

                f.write(f"### {trigger_type} ({severity})\n\n")
                f.write(f"{message}\n\n")

                if "recommendation" in trigger:
                    f.write(f"**Recommendation:** {trigger['recommendation']}\n\n")

                if "stale_commands" in trigger:
                    f.write("**Stale commands (sample):**\n\n")
                    for cmd in trigger["stale_commands"]:
                        f.write(f"- `{cmd['command']}`: last reviewed {cmd['days_stale']} days ago\n")
                    f.write("\n")

            f.write("## Recommendation\n\n")
            f.write("Consider scheduling an evolution cycle to address these triggers.\n\n")
            f.write("Run: `python3 scripts/evolution-snapshot.py --create 'Before evolution'`\n\n")
            f.write("Then: Follow the Evolution Operational Guide in `docs/evolution-operational-guide.md`\n")

        print(f"✅ Report generated: {output_file}\n")


def main():
    import sys
    import argparse

    parser = argparse.ArgumentParser(
        description="Evolution Trigger Detection"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check for triggers (console output)"
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Generate markdown report"
    )

    args = parser.parse_args()

    detector = EvolutionTriggerDetector()
    triggers = detector.run_detection()

    if args.check or (not args.report):
        detector.print_check_summary(triggers)

    if args.report:
        detector.generate_markdown_report(triggers)


if __name__ == "__main__":
    main()
