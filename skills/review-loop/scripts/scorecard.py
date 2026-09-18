#!/usr/bin/env python3
"""
scorecard.py - Score extraction, gate evaluation, and markdown scorecard generation for Review Loop.
"""

import sys
import re
import json
import argparse
from typing import Dict, Any, Optional, Tuple


def extract_pm_score(text: str) -> Optional[float]:
    """Extract PM overall score (1-10) from review markdown."""
    patterns = [
        r"OVERALL_SCORE:\s*(-?\d+(?:\.\d+)?)(?:\s*/\s*10)?",
        r"Score:\s*(-?\d+(?:\.\d+)?)\s*/\s*10",
        r"\b(?:Overall|Final)\s+Score[:=\s]+(-?\d+(?:\.\d+)?)(?:\s*/\s*10)?\b",
        r"(?:^|[^\w-])(-?\d+(?:\.\d+)?)\s*/\s*10\b",
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            val = float(m.group(1))
            if 0 <= val <= 10:
                return val
    return None


def extract_dr_score(text: str) -> Optional[float]:
    """Extract Dev Review percentage complete (0-100%) from review markdown."""
    patterns = [
        r"PERCENTAGE_COMPLETE:\s*(-?\d+(?:\.\d+)?)\s*%?",
        r"\bCompletion[:=\s]*(-?\d+(?:\.\d+)?)\s*%",
        r"(?:^|[^\w-])(-?\d+(?:\.\d+)?)\s*%\s*(?:complete|completion)\b",
        r"(?:^|[^\w-])(-?\d+(?:\.\d+)?)\s*%",
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            val = float(m.group(1))
            if 0 <= val <= 100:
                return val
    return None


def evaluate_gate(
    phase: str,
    score: float,
    gate_threshold: float,
    iteration: int,
    max_retries: int,
) -> Dict[str, Any]:
    """Evaluate whether the score passes the gate threshold or should retry."""
    passed = score >= gate_threshold
    retries_left = max(0, max_retries - iteration)
    can_retry = (not passed) and (iteration < max_retries)
    exhausted = (not passed) and (iteration >= max_retries)

    if passed:
        status = "PASSED"
        status_badge = "[PASS] PASSED"
    elif can_retry:
        status = "RETRY"
        status_badge = "[RETRY] RETRY"
    else:
        status = "EXHAUSTED"
        status_badge = "[WARN] EXHAUSTED"

    return {
        "phase": phase.upper(),
        "score": score,
        "gate_threshold": gate_threshold,
        "iteration": iteration,
        "max_retries": max_retries,
        "retries_left": retries_left,
        "passed": passed,
        "can_retry": can_retry,
        "exhausted": exhausted,
        "status": status,
        "status_badge": status_badge,
    }


def extract_ponytail_findings(text: str) -> list:
    """Extract Ponytail complexity findings (yagni:, stdlib:, shrink:, etc.) from review markdown."""
    findings = []
    for line in text.splitlines():
        clean_line = line.strip()
        if re.search(r"^(?:[-*]\s+)?`?(?:yagni|stdlib|native|shrink|delete):", clean_line, re.IGNORECASE):
            findings.append(clean_line)
    return findings


def render_markdown_scorecard(eval_result: Dict[str, Any], notes: str = "", ponytail_findings: list = None) -> str:
    """Generate a clean GitHub-flavored markdown scorecard for display."""
    phase = eval_result["phase"]
    is_pm = "PM" in phase
    score_str = f"{eval_result['score']:g}/10" if is_pm else f"{eval_result['score']:g}%"
    gate_str = f"{eval_result['gate_threshold']:g}/10" if is_pm else f"{eval_result['gate_threshold']:g}%"
    status_badge = f"**{eval_result['status_badge']}**"

    lines = [
        f"### {phase} Review Gate Scorecard",
        "",
        "| Gate Metric | Target Threshold | Achieved Score | Iteration | Status |",
        "| :--- | :---: | :---: | :---: | :---: |",
        f"| **{phase} Gate** | `{gate_str}` | `{score_str}` | {eval_result['iteration']}/{eval_result['max_retries']} | {status_badge} |",
        "",
    ]

    if eval_result["passed"]:
        next_step = "Proceed to Implementation & Verification" if is_pm else "All Quality Gates Passed! Goal Complete."
        lines.append(f"> [!TIP]\n> **Gate Cleared:** Score meets or exceeds target threshold. {next_step}.")
    elif eval_result["can_retry"]:
        lines.append(
            f"> [!IMPORTANT]\n> **Gate Not Cleared:** Target was `{gate_str}`, achieved `{score_str}`. "
            f"Review critiques, refine deliverables, and retry ({eval_result['retries_left']} attempt(s) remaining)."
        )
    else:
        lines.append(
            f"> [!WARNING]\n> **Max Retries Reached:** Gate retry limit ({eval_result['max_retries']}) exhausted. "
            f"Proceeding with best-effort implementation; manual review advised."
        )

    if ponytail_findings:
        lines.extend(["", "#### Ponytail Anti-Bloat Audit", *[f"- {f}" if not f.startswith(("-", "*")) else f for f in ponytail_findings]])

    if notes.strip():
        lines.extend(["", "#### Review Summary", notes.strip()])

    return "\n".join(lines)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    parser = argparse.ArgumentParser(description="Evaluate review loop scores and render scorecards.")
    parser.add_argument("--phase", choices=["pm", "dr"], required=True, help="Review phase: pm or dr")
    parser.add_argument("--score", type=float, help="Explicit awarded score (1-10 for PM, 0-100 for DR)")
    parser.add_argument("--gate", type=float, required=True, help="Target threshold gate value")
    parser.add_argument("--iteration", type=int, default=1, help="Current review iteration attempt")
    parser.add_argument("--max-retries", type=int, default=4, help="Max allowed review retries")
    parser.add_argument("--file", type=str, help="Path to subagent review markdown file to parse")
    parser.add_argument("--notes", type=str, default="", help="Optional notes or summary")

    args = parser.parse_args()

    ponytail_findings = []
    score = args.score
    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                content = f.read()
            if args.phase == "pm":
                score = extract_pm_score(content)
            else:
                score = extract_dr_score(content)
            ponytail_findings = extract_ponytail_findings(content)
        except Exception as e:
            print(f"Error reading file {args.file}: {e}", file=sys.stderr)
            sys.exit(1)

    if score is None:
        print("Error: Could not determine score from arguments or file content.", file=sys.stderr)
        sys.exit(1)

    result = evaluate_gate(
        phase=args.phase,
        score=score,
        gate_threshold=args.gate,
        iteration=args.iteration,
        max_retries=args.max_retries,
    )

    print(render_markdown_scorecard(result, notes=args.notes, ponytail_findings=ponytail_findings))


if __name__ == "__main__":
    main()
