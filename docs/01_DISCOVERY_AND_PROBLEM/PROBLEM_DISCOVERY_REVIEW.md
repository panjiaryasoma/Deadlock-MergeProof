# Problem & Discovery Review

## Review method

The discovery was challenged against five failure questions:

1. Is the problem externally observable?
2. Is the proposed product solving a narrower problem than "AI code review"?
3. Can success/failure be measured in 48 hours?
4. Does IBM Bob have a first-class role in the workflow?
5. Is the MVP small enough to finish?

## Findings

### P1 — "Generic AI code reviewer" was too broad
**Result:** corrected.

The product is now framed as **source-to-change evidence verification**, not a general quality oracle.

### P2 — Source authority was missing
**Result:** corrected.

The design now includes explicit source provenance, precedence, supersession, conflict detection, and abstention.

### P3 — Severity could become arbitrary LLM opinion
**Result:** corrected.

Severity is rule-bound. Findings without sufficient evidence cannot be promoted to `CONFIRMED_ISSUE`.

### P4 — Autonomous "BLOCK" creates an authority problem
**Result:** corrected.

The aggregate outputs are:
- `PASS`
- `REVIEW_REQUIRED`
- `ABSTAIN`

The system never merges or blocks.

### P5 — A web dashboard would consume time without proving the workflow
**Result:** cut from MVP.

The core artifact is a Bob custom mode + skill + deterministic report validator. A static HTML report is optional only after acceptance tests pass.

## Assumptions still requiring runtime validation

- Bob project-level custom mode loads from `.bob/custom_modes.yaml`.
- Bob skill loads from `.bob/skills/mergeproof/SKILL.md`.
- chosen subagent configuration works under available permissions.
- Bob can consistently cite exact repository locations in the demo project.

## Gate

**DISCOVERY GATE: PASS**

Proceed to PRD with the corrected narrow scope.
