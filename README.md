# Google Antigravity Review Loop (`/review-loop`)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Antigravity Compatible](https://img.shields.io/badge/Antigravity-2.0%20%7C%20CLI-brightgreen.svg)](https://antigravity.google)
[![Anti-Bloat Powered](https://img.shields.io/badge/Ponytail-Anti--Bloat%20Audit-orange.svg)](#the-ponytail-anti-bloat-audit)

A robust, two-tier gated engineering workflow for **Google Antigravity** that ensures features are rigorously planned before implementation and ruthlessly verified against bloat and edge cases before completion.

![Review Loop Overview](assets/review_loop_overview.jpg)

---

## 🎯 The Problem Solved

AI coding assistants often fall into two traps:
1. **The Rushed Plan Trap:** Jumping straight into coding with incomplete specs, missing fallbacks, and hand-waved security assumptions.
2. **The Rubber-Stamp Dev Review Trap:** Automated dev reviews often pass happily (100% complete!) even when the resulting code is over-engineered, full of speculative abstractions (`yagni`), reinvents standard libraries, or leaves failure modes completely untested.

**Review Loop** introduces an autonomous, adversarial dual-gate engineering loop:
- **Gate 1 (Plan Stage):** Reviewed by a **Cranky, Picky Senior Project Manager** who rejects hand-waving, checks blast radius, and demands explicit fallbacks.
- **Gate 2 (Implementation Stage):** Audited by an uncompromising **Senior Staff Dev & QA Architect** armed with the **Ponytail Complexity Ladder** (docking scores for speculative abstractions, bloat, or missing negative failure tests).

---

## 🏛️ Architecture & Workflow

Invoking `/review-loop` automatically initializes Antigravity's **Autonomous Goal Mode**—the agent outputs an active Goal Contract and runs continuously to completion without pausing for turn-by-turn prompts.

```mermaid
graph TD
    A["User Request: Goal + Criteria + Deliverables"] --> B["Step 0: Formalize Active Goal Contract"]
    B --> C["Step 1: Draft PM-Ready Architecture Plan"]
    C --> D["Gate 1: Cranky Senior PM Review (1-10)"]
    D --> E{"Score >= PM Gate?"}
    E -- "No (Score < Gate & Retries Left)" --> F["Refine Plan & Address Critiques"]
    F --> D
    E -- "Yes (Score >= Gate)" --> G["Step 2: Implementation & Negative Tests"]
    G --> H["Gate 2: Senior Dev & Ponytail Anti-Bloat Review"]
    H --> I{"Completion >= DR Gate?"}
    I -- "No (Completion < Gate & Retries Left)" --> J["Eliminate Bloat, Fix Defects & Re-Test"]
    J --> H
    I -- "Yes (Completion >= Gate)" --> K["Step 3: Goal Complete Seal & Final Scorecard"]
```

---

## 🚀 Quick Install

### Windows (PowerShell)
Run the automated installer to deploy globally (`~/.gemini/config/plugins/review-loop`):
```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1
```
*(To install only in the current workspace `.agents/plugins/review-loop`, pass `-Scope Workspace`)*

### macOS / Linux (Bash)
Run the shell installer:
```bash
chmod +x install.sh
./install.sh
```

---

## 💻 How to Use

### 1. Invocations

Trigger the review loop directly in chat with your task requirements:

- **Custom Gates & Retries (Recommended):**
  ```text
  start /reviewLoop PM 8-4 DR 90%-3
  ```
  *(Requires PM score $\ge 8/10$ with up to 4 retries, Dev completion $\ge 90\%$ with up to 3 retries)*

- **Zero-Config Default (PM 8-4, DR 90%-3):**
  ```text
  /review-loop
  ```

- **Predefined Presets:**
  ```text
  /review-loop --preset strict    # PM 9-5, DR 95%-5 (Ultra-high assurance)
  /review-loop --preset turbo     # PM 7-2, DR 80%-2 (Rapid iterative cycle)
  /review-loop --preset default   # PM 8-4, DR 90%-3
  ```

- **Positional Shorthand:**
  ```text
  /review-loop 8-4 90-3
  ```

---

## 🔍 The Two Quality Gates

### Gate 1: Cranky Picky Senior PM Review (Plan Stage)
Evaluates the initial technical plan across 6 core dimensions:
1. **Scope & Deliverable Precision (20%):** Are deliverables clearly itemized with unambiguous acceptance criteria?
2. **Feasibility & Ponytail Simplicity (20%):** Is this the shortest, cleanest architecture? Are standard libraries used first?
3. **Security, Permissions & Blast Radius (15%):** Are protected files respected and local user paths sanitized?
4. **User Safety & Error Handling (15%):** Are boundary inputs and crash scenarios mitigated?
5. **UI/UX & Developer Ergonomics (15%):** Is the interface or CLI intuitive and foot-gun proof?
6. **Fallback & Contingency Strategy (15%):** Is there an automated fallback if primary dependencies fail?

![PM Gate Scorecard](assets/pm_gate_scorecard.jpg)

---

### Gate 2: Senior Dev & Ponytail Anti-Bloat Review (Implementation Stage)
Evaluates code diffs, automated test execution, and structural simplicity.

![Dev Gate Scorecard](assets/dev_gate_scorecard.jpg)

#### The Ponytail Anti-Bloat Audit
The reviewer actively scans for over-engineering and applies deductions:
- `yagni:` Premature abstraction, single-use interface, or speculative configuration. **(-5% to -10% per finding)**
- `stdlib:` Hand-rolled wheel where the standard library already provides a solution. **(-5% per finding)**
- `shrink:` 200 lines of boilerplate where 40 lines of idiomatic code would suffice. **(-5% per finding)**
- `delete:` Dead code, unused imports, or orphaned scaffolding.

#### Hard-to-Meet Adversarial Criteria
To achieve $\ge 90\%$ completion, the solution must pass these checkpoints:
1. **Adversarial Negative Testing:** Proof that invalid inputs, missing parameters, and boundary limits fail safely.
2. **Zero-Leak Sanitization:** Complete elimination of personal identifiers, local machine directories, or private tokens.
3. **Idempotency:** Installers, setup scripts, and commands must run repeatedly with clean, identical states.
4. **Cross-Platform Portability:** Operates smoothly across Windows PowerShell, macOS, and Linux without brittle path assumptions.

---

## 🧪 Automated Testing

Run the full automated test suite:
```bash
# Unit tests: parser, scorecard, and adversarial edge cases
python -m unittest discover -s skills/review-loop/tests -p "test_*.py" -v

# Sanitization audit: ensures zero personal/machine leaks
python tests/test_sanitization.py
```

---

## 📁 Repository Structure

```text
antigravity-review-loop/
├── plugin.json                       # Plugin manifest & Antigravity registration
├── LICENSE                           # MIT License
├── README.md                         # Documentation & How-To Guide
├── install.ps1                       # Windows installer script
├── install.sh                        # macOS & Linux installer script
├── assets/                           # Screenshots and architecture diagrams
│   ├── review_loop_overview.jpg
│   ├── pm_gate_scorecard.jpg
│   └── dev_gate_scorecard.jpg
├── rules/
│   └── AGENTS.md                     # Antigravity agent instructions & autonomous goal hooks
├── skills/
│   └── review-loop/
│       ├── SKILL.md                  # Detailed skill manual & slash command hints
│       ├── scripts/
│       │   ├── gate_parser.py        # CLI argument & preset parser
│       │   └── scorecard.py          # Scorecard evaluator & markdown renderer
│       ├── references/
│       │   ├── pm_persona.md         # Cranky Senior PM prompt & rubric
│       │   ├── dev_persona.md        # Senior Dev & Ponytail reviewer prompt & rubric
│       │   └── plan_template.md      # PM-ready architecture plan template
│       └── tests/
│           ├── test_gate_parser.py   # Unit tests for argument parsing
│           ├── test_scorecard.py     # Unit tests for scoring & Ponytail extraction
│           └── test_negative_cases.py# Adversarial boundary & negative tests
└── tests/
    └── test_sanitization.py          # Leak detection scanner
```

---

## 📜 License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.
