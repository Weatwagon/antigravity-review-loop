# Implementation Plan Template (PM-Ready)

Use this template when authoring the initial plan for Gate 1 (Cranky Senior PM Review). Filling in every section thoroughly ensures a high first-pass score.

```markdown
# [Feature / Goal Title]

## 1. Goal & Deliverables
### Primary Goal
- [Clear 1-2 sentence description of what will be achieved]

### Concrete Deliverables
1. **Deliverable 1:** [Specific artifact, command, UI, or library]
2. **Deliverable 2:** [Specific artifact, command, UI, or library]
3. **Deliverable 3:** [Specific artifact, command, UI, or library]

### In Scope vs Out of Scope
- **In Scope:** [Explicit boundaries]
- **Out of Scope:** [Explicitly excluded items]

---

## 2. Technical Architecture & Feasibility
- **Architecture Overview:** [How the components connect]
- **Dependencies & Prerequisites:** [Required runtimes, libraries, or system capabilities]
- **Minimalism & YAGNI:** [Justification that this is the cleanest, least bloated design]

---

## 3. Security, Permissions & User Safety
- **Workspace Boundaries:** [Files and directories created or modified]
- **Protected Resources:** [Confirmation that no credentials or protected paths are touched]
- **Blast Radius Mitigation:** [Why this change cannot inadvertently break other systems]

---

## 4. Error Handling & Edge Cases
- **Boundary Inputs:** [How empty, malformed, or extreme inputs are handled]
- **Error Reporting:** [How errors are surfaced clearly to the user]

---

## 5. UI/UX & Developer Ergonomics
- **CLI / Chat Syntax:** [Exact command or prompt examples]
- **Feedback & Visual Polish:** [Scorecards, progress indicators, helpful hints]

---

## 6. Fallback Strategy
- **Fallback 1:** [What happens if a primary dependency or command fails]
- **Rollback Plan:** [How to revert if an unrecoverable failure occurs]

---

## 7. Verification & Testing Plan
- **Automated Test Commands:**
  - `python -m unittest ...` or `npm test`
- **Manual Verification Steps:**
  - [Step 1]
  - [Step 2]
```
