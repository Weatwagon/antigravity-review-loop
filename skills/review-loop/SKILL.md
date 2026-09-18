---
name: review-loop
description: >-
  Executes a rigorous two-tier gated review engineering loop: State goal & metrics ->
  Plan -> Gate 1: Cranky Senior PM Review (1-10) -> Implement & Test -> Gate 2: Senior Dev
  Review (0-100%). Automatically initializes and summarizes the active Antigravity Goal
  contract so you don't need to invoke /goal separately. Use whenever the user invokes
  /reviewLoop, /review-loop, /gate-loop, or asks for a gated development loop with PM and dev review gates.
argument-hint: "[PM <gate>-<retries>] [DR <gate>%-<retries>] | [--preset strict|turbo|default]"
license: MIT
---

# Review Loop: Two-Tier Gated Engineering Workflow

The **Review Loop** skill enforces an autonomous, iterative quality-control protocol designed to guarantee that solutions are thoroughly architected before implementation and rigorously verified before completion.

> [!TIP]
> **Built-In Antigravity Goal Mode:**  
> Invoking `/reviewLoop` or `/review-loop` automatically initializes Antigravity Autonomous Goal mode. You do **not** need to call `/goal` separately! The agent automatically summarizes the Goal Contract, adopts an autonomous run-to-completion posture through both review gates, and concludes with `<!-- GOAL_COMPLETE -->`.

---

## 🎯 When to Use This Skill

Activate this skill when the user:
- Types `/reviewLoop`, `/review-loop`, `start /reviewLoop`, or `/gate-loop`
- Specifies a review gate format like `PM 8-4 DR 90%-3` or `PM 9-5 DR 95%-5`
- Asks for a goal using the pattern: *"State goal -> plan -> PM review -> implement -> senior dev review"*

---

## ⚙️ Gate Configuration & Syntax

The user can configure target gate thresholds and retry limits flexibly:

| Invocation Syntax | PM Gate (Plan Review) | DR Gate (Dev Review) | Description |
| :--- | :---: | :---: | :--- |
| `start /reviewLoop PM 8-4 DR 90%-3` | Score $\ge 8/10$ (Max 4 retries) | Completion $\ge 90\%$ (Max 3 retries) | Standard user format |
| `/review-loop` | Score $\ge 8/10$ (Max 4 retries) | Completion $\ge 90\%$ (Max 3 retries) | Default configuration |
| `/review-loop --preset strict` | Score $\ge 9/10$ (Max 5 retries) | Completion $\ge 95\%$ (Max 5 retries) | Ultra-high assurance |
| `/review-loop --preset turbo` | Score $\ge 7/10$ (Max 2 retries) | Completion $\ge 80\%$ (Max 2 retries) | Fast iterative mode |
| `/review-loop 8-4 90-3` | Score $\ge 8/10$ (Max 4 retries) | Completion $\ge 90\%$ (Max 3 retries) | Positional shorthand |

### Parameter Parser
To parse user arguments quickly and reliably, run the bundled parser:
```bash
python .agents/plugins/review-loop/skills/review-loop/scripts/gate_parser.py "<user_args>"
```

---

## 🔁 Workflow Execution Protocol

```mermaid
graph TD
    A["User Prompt: Goal + Deliverables + Criteria"] --> B["Step 0: Summarize & Declare Active Goal Contract"]
    B --> C["Step 1: Draft PM-Ready Architecture Plan"]
    C --> D["Step 2: Gate 1 - Cranky Senior PM Review"]
    D --> E{"Score >= PM Gate?"}
    E -- "No (Score < Gate & Retries Left)" --> F["Refine Plan & Address Critiques"]
    F --> D
    E -- "Yes (Score >= Gate)" --> G["Step 3: Implementation & Local Verification"]
    G --> H["Step 4: Gate 2 - Senior Dev Review & QA"]
    H --> I{"Completion >= DR Gate?"}
    I -- "No (Completion < Gate & Retries Left)" --> J["Fix Defects & Add Regression Tests"]
    J --> H
    I -- "Yes (Completion >= Gate)" --> K["Step 5: Goal Complete Marker & Final Scorecard"]
```

---

### Step 0: Summarize & Declare the Active Goal Contract
Immediately output a structured **Goal Declaration** in chat to anchor the session:
- **Goal Statement:** Clear 1–2 sentence declaration of the target objective.
- **Deliverables Checklist:** Concrete, numbered deliverables.
- **Success Criteria & Fallbacks:** Explicit acceptance metrics and fallback guarantees.
- **Configured Review Gates:** Target PM score + retries, and target Dev Review completion % + retries.
- **Autonomous Posture:** Inform the user that execution is running autonomously end-to-end.

---

### Step 1: Draft PM-Ready Architecture Plan
Draft an implementation plan following [`references/plan_template.md`](references/plan_template.md):
- Address architecture, dependencies, security boundaries, user ergonomics, edge cases, and fallback strategies.

---

### Step 2: Gate 1 — Cranky Senior PM Review Subagent
1. Spawn or invoke a review subagent (or run an evaluation turn) adopting the persona in [`references/pm_persona.md`](references/pm_persona.md):
   - **Persona**: Uncompromising, experienced Senior Project Manager.
   - **Rubric (1-10)**: Scope Precision, Technical Feasibility, Security & Blast Radius, User Safety & Errors, UI/UX Ergonomics, Fallback Strategy.
2. The subagent returns an `OVERALL_SCORE: X/10` and itemized critiques.
3. Evaluate the result:
   ```bash
   python .agents/plugins/review-loop/skills/review-loop/scripts/scorecard.py --phase pm --score <SCORE> --gate <PM_GATE> --iteration <ITERATION> --max-retries <PM_RETRIES>
   ```
4. **Decision Loop**:
   - **If Score $\ge$ PM Gate**: Pass Gate 1. Proceed immediately to Step 3.
   - **If Score < PM Gate and Retries Remain**: Review critiques, revise the plan line-by-line, increment iteration, and re-submit to Gate 1.
   - **If Retries Exhausted**: Proceed with best-effort implementation, alerting the user to residual risks.

---

### Step 3: Implementation & Local Verification
1. Execute the approved plan:
   - Create or modify the necessary files.
   - Write automated unit and integration tests.
   - Stay strictly within workspace boundaries (respecting Guardian / Approve for Me rules).
2. Run tests to confirm zero syntax errors and green test runs:
   ```bash
   npm test   # or python -m unittest / pytest / cargo test
   ```

---

### Step 4: Gate 2 — Senior Staff Dev & Ponytail Anti-Bloat Review Subagent
1. Spawn or invoke a review subagent adopting the persona in [`references/dev_persona.md`](references/dev_persona.md):
   - **Persona**: Uncompromising Senior Staff Dev & QA Architect armed with the **Ponytail Complexity Ladder**.
   - **Ponytail Simplicity Audit**: Scans diffs for `yagni:` (speculative code), `stdlib:` (reinvented wheels), and `shrink:` (bloat). Docks **5% to 10%** per finding.
   - **Hard-to-Meet Checkpoints**:
     - *Negative Testing Proof:* Requires explicit automated tests for invalid inputs, boundary errors, and failure recovery.
     - *Zero-Leak Sanitization:* Immediate rejection if any local machine paths or personal identifiers leak.
     - *Idempotency & Clean State:* Repeated runs must produce identical, clean results.
     - *Cross-Platform Portability:* Validates Windows PowerShell, Linux, and macOS compatibility.
   - **Rubric (0-100% Complete)**: Deliverables & Correctness (25%), Adversarial Negative Testing (20%), Ponytail Anti-Bloat (25%), Security & Sanitization (15%), Portability & Idempotency (15%).
2. The subagent inspects code diffs and test logs, returning a `PERCENTAGE_COMPLETE: X%`, itemized Ponytail tags, and deficiency list.
3. Evaluate the result:
   ```bash
   python .agents/plugins/review-loop/skills/review-loop/scripts/scorecard.py --phase dr --score <PERCENTAGE> --gate <DR_GATE> --iteration <ITERATION> --max-retries <DR_RETRIES>
   ```
4. **Decision Loop**:
   - **If Percentage $\ge$ DR Gate**: Pass Gate 2. Proceed to Step 5.
   - **If Percentage < DR Gate and Retries Remain**: Fix code defects, eliminate bloat, add missing negative tests, increment iteration, and re-submit to Gate 2.
   - **If Retries Exhausted**: Document completed vs deferred items and flag for user inspection.

---

### Step 5: Final Scorecard & Goal Complete Seal
1. Output the comprehensive final scorecard summarizing:
   - Gate 1 (PM Review): Final score, iterations used, status.
   - Gate 2 (Dev Review): Final completion percentage, test count, status.
   - Verified Deliverables checklist.
2. Output `<!-- GOAL_COMPLETE -->` to signal terminal completion to the Antigravity engine.
