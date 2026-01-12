#!/usr/bin/env python3
"""
Shared utilities for playbook scripts.

Consolidates common patterns: logging, metadata loading, constants, validation.
"""

import json
import logging
import re
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Set


def setup_logger(logger_name: str, verbose: bool = False) -> logging.Logger:
    """Setup standard logger for playbook scripts."""
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def load_metadata(metadata_file: Path) -> Optional[Dict[str, Any]]:
    """Load metadata from JSON file with consistent error handling."""
    if not metadata_file.exists():
        logging.error(f"Metadata file not found: {metadata_file}")
        return None

    try:
        with open(metadata_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON in metadata file: {e}")
        return None
    except Exception as e:
        logging.error(f"Error loading metadata: {e}")
        return None


def load_json(json_file: Path) -> Optional[Dict[str, Any]]:
    """Load any JSON file with standard error handling."""
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"File not found: {json_file}")
        return None
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON: {e}")
        return None


def is_skill_file(content: str) -> bool:
    """Check if file is a skill file (AI prompt template)."""
    skill_indicators = [
        r"^You are\s",
        r"^You will\s",
        r"^Lets\s",
        r"^You should\s",
    ]
    first_line = content.split("\n")[0].strip()
    return any(re.match(indicator, first_line) for indicator in skill_indicators)


def normalize_tier(tier: Any) -> str:
    """Normalize tier to single string value."""
    if isinstance(tier, list):
        return tier[0] if tier else "M"
    return tier or "M"


def get_tier_time_minutes(tier: Any) -> int:
    """Get estimated time in minutes for a tier."""
    tier_str = normalize_tier(tier)
    times = {"XS": 5, "S": 10, "M": 25, "L": 45}
    return times.get(str(tier_str), 15)


def get_tier_time_string(tier: Any) -> str:
    """Get estimated time as formatted string for a tier."""
    minutes = get_tier_time_minutes(tier)
    if minutes < 30:
        return f"{minutes} min"
    elif minutes < 120:
        hours = minutes // 60
        return f"{hours}h" if hours > 1 else f"{hours}h"
    else:
        hours = minutes // 60
        return f"{hours}+ hours"


def validate_command_reference(
    reference: str, valid_commands: Set[str]
) -> Optional[str]:
    """Validate a command reference. Returns error message or None if valid."""
    cmd_name = reference.lstrip("/")
    if cmd_name not in valid_commands:
        return f"Referenced command /{cmd_name} not found"
    return None


# Constants for validation
VALID_TIERS = {"XS", "S", "M", "L"}
VALID_FREQUENCIES = {
    "daily",
    "weekly",
    "start-of-feature",
    "per-iteration",
    "per-pr",
    "pre-release",
    "on-incident",
    "one-time",
    "as-needed",
}
VALID_CATEGORIES = {
    "core",
    "development",
    "planning",
    "reviews",
    "release",
    "deployment",
    "repo",
    "people",
    "templates",
}

TIER_PRIORITY = {"XS": 5, "S": 4, "M": 3, "L": 2}
TIER_TIME_MINUTES = {"XS": 5, "S": 10, "M": 25, "L": 45}
