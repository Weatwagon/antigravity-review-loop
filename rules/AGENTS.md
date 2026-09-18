# Review Loop & Quality Gate Instructions

When the user asks for a goal using `/reviewLoop`, `/review-loop`, `start /reviewLoop`, or requests a gated review process with PM and Dev reviews:

1. **Automatic Antigravity Goal Initialization**:
   - Invoking `/reviewLoop` or `/review-loop` automatically activates **Antigravity Autonomous Goal Mode**. The user **does NOT need to run `/goal` separately**.
   - The agent must adopt an autonomous, run-to-completion posture: it will not stop for turn-by-turn prompts, executing end-to-end through both review gates.

2. **Step 0: Formalize & Declare the Active Goal Contract**:
   - Immediately output a formalized Goal Summary:
     - **Objective & Scope**
     - **Deliverables Checklist**
     - **Success Metrics & Fallbacks**
     - **Configured Review Gates** (e.g. PM Gate: 8/10 [4 retries], Dev Gate: 90% [3 retries])

3. **Phase 1: Plan Generation & PM-Ready Specification**:
   - Draft a comprehensive, implementation-ready plan covering architecture, security, user safety, UI/UX, feasibility, and fallbacks.
   - Enforce Ponytail simplicity: eliminate speculative abstractions (`yagni:`) before writing code.

4. **Gate 1: Cranky Senior PM Review Subagent**:
   - Spawn/invoke the review subagent acting as a **cranky, picky senior project manager**.
   - Grade the plan from 1 to 10 across the standard rubrics.
   - If `Score < PM Gate`, iterate and address every critique up to the specified retry limit.
   - Only advance to implementation once `Score >= PM Gate` (or retries exhausted).

5. **Phase 2: Implementation & Verification**:
   - Write clean, minimal code using standard libraries and native features first.
   - Write and run adversarial automated test suites covering negative cases and boundary failures.
   - Stay strictly within workspace boundaries.

6. **Gate 2: Senior Dev & Ponytail Anti-Bloat Reviewer Subagent**:
   - Spawn/invoke the reviewer subagent acting as an **unforgiving senior staff engineer & QA reviewer**.
   - **🎯 Heaviest Weight (40%) — User Request Fidelity & End-to-End Lineage:** Trace `[Original User Prompt] ──> [Architecture Plan] ──> [Code Implementation] ──> [Delivered & Verified Result]`. If ANY requirement or constraint from the user's ask was dropped, forgotten, or quietly substituted, immediately dock 25–40% and reject the gate.
   - **Ponytail Simplicity Audit (20%):** Audit diffs for `yagni:` (speculative code), `stdlib:` (reinvented wheels), and `shrink:` (bloat) based on [Dietrich Gebert's Ponytail](https://github.com/DietrichGebert/ponytail). Dock 5–10% per finding.
   - **Hard-to-Meet Criteria:** Require proof of negative failure tests, zero-leak sanitization, idempotency, and cross-platform portability.
   - If `Completion < DR Gate`, fix defects, restore missing requirements, and re-test up to the specified retry limit.
   - Conclude and seal the goal with `<!-- GOAL_COMPLETE -->` once `Completion >= DR Gate`.

