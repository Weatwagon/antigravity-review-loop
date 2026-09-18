#!/usr/bin/env python3
"""
Unit tests for scorecard.py
"""

import unittest
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from scorecard import (
    extract_pm_score,
    extract_dr_score,
    evaluate_gate,
    render_markdown_scorecard,
    extract_ponytail_findings,
)


class TestScorecard(unittest.TestCase):

    def test_extract_pm_score_various_formats(self):
        sample1 = "Overall assessment: OVERALL_SCORE: 8.5/10. Ready for implementation."
        self.assertEqual(extract_pm_score(sample1), 8.5)

        sample2 = "Final Score: 9/10"
        self.assertEqual(extract_pm_score(sample2), 9.0)

        sample3 = "I rate this plan 7/10 because fallbacks are missing."
        self.assertEqual(extract_pm_score(sample3), 7.0)

        sample4 = "OVERALL_SCORE: 10"
        self.assertEqual(extract_pm_score(sample4), 10.0)

    def test_extract_dr_score_various_formats(self):
        sample1 = "Review summary: PERCENTAGE_COMPLETE: 92%. All unit tests passed."
        self.assertEqual(extract_dr_score(sample1), 92.0)

        sample2 = "Completion: 85%"
        self.assertEqual(extract_dr_score(sample2), 85.0)

        sample3 = "95% complete with all deliverables verified."
        self.assertEqual(extract_dr_score(sample3), 95.0)

    def test_evaluate_gate_pm_passed(self):
        res = evaluate_gate(
            phase="pm",
            score=8.0,
            gate_threshold=8.0,
            iteration=1,
            max_retries=4,
        )
        self.assertTrue(res["passed"])
        self.assertFalse(res["can_retry"])
        self.assertEqual(res["status"], "PASSED")

    def test_evaluate_gate_pm_retry(self):
        res = evaluate_gate(
            phase="pm",
            score=6.0,
            gate_threshold=8.0,
            iteration=2,
            max_retries=4,
        )
        self.assertFalse(res["passed"])
        self.assertTrue(res["can_retry"])
        self.assertEqual(res["retries_left"], 2)
        self.assertEqual(res["status"], "RETRY")

    def test_evaluate_gate_exhausted(self):
        res = evaluate_gate(
            phase="pm",
            score=6.0,
            gate_threshold=8.0,
            iteration=4,
            max_retries=4,
        )
        self.assertFalse(res["passed"])
        self.assertFalse(res["can_retry"])
        self.assertTrue(res["exhausted"])
        self.assertEqual(res["status"], "EXHAUSTED")

    def test_render_scorecard_markdown(self):
        eval_res = evaluate_gate(
            phase="dr",
            score=95.0,
            gate_threshold=90.0,
            iteration=1,
            max_retries=3,
        )
        md = render_markdown_scorecard(eval_res, notes="All 15 tests passed.")
        self.assertIn("DR Review Gate Scorecard", md)
        self.assertIn("95%", md)
        self.assertIn("PASSED", md)
        self.assertIn("All 15 tests passed.", md)

    def test_extract_ponytail_findings(self):
        sample = """
        #### Ponytail Simplicity & Anti-Bloat Audit
        - yagni: Speculative CacheManager class with only one caller. Remove and inline.
        - stdlib: Hand-rolled string padding function. Use str.rjust().
        - shrink: Reduce 80-line parser into 15-line regex lookup.
        """
        findings = extract_ponytail_findings(sample)
        self.assertEqual(len(findings), 3)
        self.assertTrue(any("yagni:" in f for f in findings))
        self.assertTrue(any("stdlib:" in f for f in findings))
        self.assertTrue(any("shrink:" in f for f in findings))


if __name__ == "__main__":
    unittest.main()
