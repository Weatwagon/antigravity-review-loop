#!/usr/bin/env python3
"""
gate_parser.py - Parse configuration arguments for the Review Loop skill.

Supported formats:
  - Standard user invocation:
      "start /reviewLoop PM 8-4 DR 90%-3"
      "/review-loop PM 8-4 DR 90%-3"
      "PM 8-4 DR 90%-3"
  - Shorthand variations:
      "PM:8-4, DR:90-3"
      "8-4 90-3"
      "PM 8 DR 90%" (uses default retries: 4)
  - Presets:
      "/review-loop --preset strict"  (PM 9-5, DR 95%-5)
      "/review-loop --preset turbo"   (PM 7-2, DR 80%-2)
      "/review-loop --preset default" (PM 8-4, DR 90%-3)
  - Empty string / no args:
      Defaults to PM 8-4, DR 90%-3
"""

import sys
import re
import json
import argparse
from typing import Dict, Any, Optional

PRESETS = {
    "default": {
        "pm_gate": 8,
        "pm_max_retries": 4,
        "dr_gate": 90,
        "dr_max_retries": 3,
    },
    "strict": {
        "pm_gate": 9,
        "pm_max_retries": 5,
        "dr_gate": 95,
        "dr_max_retries": 5,
    },
    "turbo": {
        "pm_gate": 7,
        "pm_max_retries": 2,
        "dr_gate": 80,
        "dr_max_retries": 2,
    },
    "relaxed": {
        "pm_gate": 7,
        "pm_max_retries": 3,
        "dr_gate": 80,
        "dr_max_retries": 3,
    },
}

DEFAULT_CONFIG = PRESETS["default"].copy()


def parse_gate_string(text: str) -> Dict[str, Any]:
    """
    Parse an arbitrary user invocation string into validated gate parameters.
    """
    raw_input = text.strip() if text else ""
    config = DEFAULT_CONFIG.copy()
    preset_detected = None

    if not raw_input:
        return {
            **config,
            "preset": "default",
            "raw_input": raw_input,
        }

    # Clean leading command triggers
    clean = re.sub(
        r"^(?:start\s+)?(?:/(?:reviewLoop|review-loop|gate-loop|dual-gate))\s*",
        "",
        raw_input,
        flags=re.IGNORECASE,
    ).strip()

    # Check for explicit preset flags: --preset strict / preset: turbo
    preset_match = re.search(
        r"(?:--preset\s+|preset[:=\s]+)(\w+)", clean, flags=re.IGNORECASE
    )
    if preset_match:
        name = preset_match.group(1).lower()
        if name in PRESETS:
            config = PRESETS[name].copy()
            preset_detected = name
            # Remove preset part to allow further overrides
            clean = re.sub(
                r"(?:--preset\s+|preset[:=\s]+)\w+", "", clean, flags=re.IGNORECASE
            ).strip()

    # Check for CLI flags: --pm, --pm-retries, --dr, --dr-retries
    pm_flag = re.search(r"--pm[:=\s]+(\d+)", clean, flags=re.IGNORECASE)
    if pm_flag:
        config["pm_gate"] = int(pm_flag.group(1))

    pm_retries_flag = re.search(
        r"--pm-retries[:=\s]+(\d+)", clean, flags=re.IGNORECASE
    )
    if pm_retries_flag:
        config["pm_max_retries"] = int(pm_retries_flag.group(1))

    dr_flag = re.search(r"--dr[:=\s]+(\d+)%?", clean, flags=re.IGNORECASE)
    if dr_flag:
        config["dr_gate"] = int(dr_flag.group(1))

    dr_retries_flag = re.search(
        r"--dr-retries[:=\s]+(\d+)", clean, flags=re.IGNORECASE
    )
    if dr_retries_flag:
        config["dr_max_retries"] = int(dr_retries_flag.group(1))

    # Check for PM pattern: PM[:=\s]*(\d+)(?:[-/:](\d+))?
    pm_match = re.search(
        r"\bPM[:=\s]*(\d+)(?:[-/:x](\d+))?\b", clean, flags=re.IGNORECASE
    )
    if pm_match:
        config["pm_gate"] = int(pm_match.group(1))
        if pm_match.group(2) is not None:
            config["pm_max_retries"] = int(pm_match.group(2))

    # Check for DR pattern: DR[:=\s]*(\d+)%?(?:[-/:x](\d+))?
    dr_match = re.search(
        r"\bDR[:=\s]*(\d+)%?(?:[-/:x](\d+))?\b", clean, flags=re.IGNORECASE
    )
    if dr_match:
        config["dr_gate"] = int(dr_match.group(1))
        if dr_match.group(2) is not None:
            config["dr_max_retries"] = int(dr_match.group(2))

    # Check for positional shorthand e.g. "8-4 90-3" or "8-4 90%-3"
    if not pm_match and not dr_match and not pm_flag and not dr_flag:
        pos_match = re.search(
            r"^\s*(\d+)(?:[-/:x](\d+))?\s+(\d+)%?(?:[-/:x](\d+))?\s*$", clean
        )
        if pos_match:
            config["pm_gate"] = int(pos_match.group(1))
            if pos_match.group(2):
                config["pm_max_retries"] = int(pos_match.group(2))
            config["dr_gate"] = int(pos_match.group(3))
            if pos_match.group(4):
                config["dr_max_retries"] = int(pos_match.group(4))

    # Validate bounds
    config["pm_gate"] = max(1, min(10, config["pm_gate"]))
    config["pm_max_retries"] = max(0, min(10, config["pm_max_retries"]))
    config["dr_gate"] = max(1, min(100, config["dr_gate"]))
    config["dr_max_retries"] = max(0, min(10, config["dr_max_retries"]))

    return {
        "pm_gate": config["pm_gate"],
        "pm_max_retries": config["pm_max_retries"],
        "dr_gate": config["dr_gate"],
        "dr_max_retries": config["dr_max_retries"],
        "preset": preset_detected or "custom",
        "raw_input": raw_input,
    }


def format_summary(config: Dict[str, Any]) -> str:
    """Return a human-readable summary of the gate configuration."""
    return (
        f"Review Loop Configuration:\n"
        f"  - Gate 1 (PM Review): Target Score >= {config['pm_gate']}/10 (Max Retries: {config['pm_max_retries']})\n"
        f"  - Gate 2 (Dev Review): Target Completion >= {config['dr_gate']}% (Max Retries: {config['dr_max_retries']})\n"
        f"  - Preset: {config['preset']}"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Parse Review Loop gate arguments."
    )
    parser.add_argument(
        "query",
        nargs="*",
        help="Argument string (e.g. 'PM 8-4 DR 90%-3', 'start /reviewLoop PM 8-4 DR 90%-3')",
    )
    parser.add_argument(
        "--json", action="store_true", default=True, help="Output JSON"
    )
    parser.add_argument(
        "--human", action="store_true", help="Output human-readable format"
    )

    args = parser.parse_args()
    input_str = " ".join(args.query)
    result = parse_gate_string(input_str)

    if args.human:
        print(format_summary(result))
    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
