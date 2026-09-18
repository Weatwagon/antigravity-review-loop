#!/usr/bin/env python3
"""
test_negative_cases.py - Adversarial negative edge case tests for Review Loop.
"""

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from gate_parser import parse_gate_string
from scorecard import (
    extract_pm_score,
    extract_dr_score,
    evaluate_gate,
    extract_ponytail_findings,
    render_markdown_scorecard,
)


class TestNegativeAndAdversarialCases(unittest.TestCase):

    def test_negative_gate_values_clamped(self):
        """Negative numbers should be clamped to minimum valid bounds (PM: 1, DR: 1)"""
        res = parse_gate_string("PM -5--2 DR -20%--1")
        self.assertGreaterEqual(res["pm_gate"], 1)
        self.assertGreaterEqual(res["pm_max_retries"], 0)
        self.assertGreaterEqual(res["dr_gate"], 1)
        self.assertGreaterEqual(res["dr_max_retries"], 0)

    def test_excessive_gate_values_clamped(self):
        """Values exceeding maximum bounds should be clamped (PM <= 10, DR <= 100, retries <= 10)"""
        res = parse_gate_string("PM 999-50 DR 500%-80")
        self.assertEqual(res["pm_gate"], 10)
        self.assertEqual(res["pm_max_retries"], 10)
        self.assertEqual(res["dr_gate"], 100)
        self.assertEqual(res["dr_max_retries"], 10)

    def test_corrupt_or_garbage_strings(self):
        """Random gibberish should fallback safely to default configuration"""
        res = parse_gate_string("!@#$%^&*()_+ arbitrary text without gate numbers")
        self.assertEqual(res["pm_gate"], 8)
        self.assertEqual(res["pm_max_retries"], 4)
        self.assertEqual(res["dr_gate"], 90)
        self.assertEqual(res["dr_max_retries"], 3)

    def test_pm_score_missing_or_corrupt(self):
        """Text without valid score should return None"""
        self.assertIsNone(extract_pm_score("No score was provided in this text."))
        self.assertIsNone(extract_pm_score("Score was invalid: OVERALL_SCORE: 15/10"))  # > 10
        self.assertIsNone(extract_pm_score("Score: -5/10"))  # < 0

    def test_dr_score_missing_or_corrupt(self):
        """Text without valid completion percentage should return None"""
        self.assertIsNone(extract_dr_score("No completion was recorded."))
        self.assertIsNone(extract_dr_score("PERCENTAGE_COMPLETE: 250%"))  # > 100
        self.assertIsNone(extract_dr_score("PERCENTAGE_COMPLETE: -15%"))  # < 0

    def test_ponytail_extraction_adversarial_variants(self):
        """Ponytail finding extractor handles backticks, mixed casing, and messy bullets"""
        sample = """
        * `yagni:` extra abstraction layer with 1 caller
        - YAGNI: redundant singleton registry
        * `stdlib:` hand-rolled date formatter
        - Shrink: 200 lines down to 10
        Random text line that mentions yagni in prose should not match.
        """
        findings = extract_ponytail_findings(sample)
        self.assertEqual(len(findings), 4)

    def test_scorecard_rendering_empty_notes_and_boundary_iterations(self):
        """Scorecard renders cleanly without crashing on empty notes and 0 retries left"""
        eval_res = evaluate_gate(
            phase="pm",
            score=7.0,
            gate_threshold=8.0,
            iteration=4,
            max_retries=4,
        )
        md = render_markdown_scorecard(eval_res, notes="")
        self.assertIn("EXHAUSTED", md)
        self.assertIn("7/10", md)


if __name__ == "__main__":
    unittest.main()
