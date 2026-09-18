#!/usr/bin/env python3
"""
Unit tests for gate_parser.py
"""

import unittest
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from gate_parser import parse_gate_string


class TestGateParser(unittest.TestCase):

    def test_exact_user_prompt_syntax(self):
        """User example: 'start /reviewLoop PM 8-4 DR 90%-3'"""
        res = parse_gate_string("start /reviewLoop PM 8-4 DR 90%-3")
        self.assertEqual(res["pm_gate"], 8)
        self.assertEqual(res["pm_max_retries"], 4)
        self.assertEqual(res["dr_gate"], 90)
        self.assertEqual(res["dr_max_retries"], 3)

    def test_hyphenated_slash_command(self):
        """Standard invocation: '/review-loop PM 8-4 DR 90%-3'"""
        res = parse_gate_string("/review-loop PM 8-4 DR 90%-3")
        self.assertEqual(res["pm_gate"], 8)
        self.assertEqual(res["pm_max_retries"], 4)
        self.assertEqual(res["dr_gate"], 90)
        self.assertEqual(res["dr_max_retries"], 3)

    def test_standalone_args_without_command(self):
        """Invocation: 'PM 8-4 DR 90-3'"""
        res = parse_gate_string("PM 8-4 DR 90-3")
        self.assertEqual(res["pm_gate"], 8)
        self.assertEqual(res["pm_max_retries"], 4)
        self.assertEqual(res["dr_gate"], 90)
        self.assertEqual(res["dr_max_retries"], 3)

    def test_defaults_when_empty(self):
        """Invocation with no args should return defaults (PM 8-4, DR 90-3)"""
        res = parse_gate_string("")
        self.assertEqual(res["pm_gate"], 8)
        self.assertEqual(res["pm_max_retries"], 4)
        self.assertEqual(res["dr_gate"], 90)
        self.assertEqual(res["dr_max_retries"], 3)
        self.assertEqual(res["preset"], "default")

    def test_defaults_when_only_thresholds_given(self):
        """Invocation: 'PM 8 DR 90%' without retry numbers should default PM retries to 4 and DR retries to 3"""
        res = parse_gate_string("PM 8 DR 90%")
        self.assertEqual(res["pm_gate"], 8)
        self.assertEqual(res["pm_max_retries"], 4)
        self.assertEqual(res["dr_gate"], 90)
        self.assertEqual(res["dr_max_retries"], 3)

    def test_positional_shorthand(self):
        """Invocation: '8-4 90-3' or '8-4 90%-3'"""
        res = parse_gate_string("8-4 90-3")
        self.assertEqual(res["pm_gate"], 8)
        self.assertEqual(res["pm_max_retries"], 4)
        self.assertEqual(res["dr_gate"], 90)
        self.assertEqual(res["dr_max_retries"], 3)

    def test_preset_strict(self):
        """Preset: '--preset strict' should set PM 9-5, DR 95-5"""
        res = parse_gate_string("/review-loop --preset strict")
        self.assertEqual(res["pm_gate"], 9)
        self.assertEqual(res["pm_max_retries"], 5)
        self.assertEqual(res["dr_gate"], 95)
        self.assertEqual(res["dr_max_retries"], 5)
        self.assertEqual(res["preset"], "strict")

    def test_preset_turbo(self):
        """Preset: '--preset turbo' should set PM 7-2, DR 80-2"""
        res = parse_gate_string("/review-loop --preset turbo")
        self.assertEqual(res["pm_gate"], 7)
        self.assertEqual(res["pm_max_retries"], 2)
        self.assertEqual(res["dr_gate"], 80)
        self.assertEqual(res["dr_max_retries"], 2)
        self.assertEqual(res["preset"], "turbo")

    def test_flag_style_arguments(self):
        """Invocation: '--pm 9 --pm-retries 3 --dr 95 --dr-retries 2'"""
        res = parse_gate_string("--pm 9 --pm-retries 3 --dr 95 --dr-retries 2")
        self.assertEqual(res["pm_gate"], 9)
        self.assertEqual(res["pm_max_retries"], 3)
        self.assertEqual(res["dr_gate"], 95)
        self.assertEqual(res["dr_max_retries"], 2)

    def test_clamping_bounds(self):
        """Values should be clamped within logical bounds"""
        res = parse_gate_string("PM 15-20 DR 150%-20")
        self.assertEqual(res["pm_gate"], 10)  # Max 10
        self.assertEqual(res["pm_max_retries"], 10)  # Max 10
        self.assertEqual(res["dr_gate"], 100)  # Max 100%
        self.assertEqual(res["dr_max_retries"], 10)


if __name__ == "__main__":
    unittest.main()
