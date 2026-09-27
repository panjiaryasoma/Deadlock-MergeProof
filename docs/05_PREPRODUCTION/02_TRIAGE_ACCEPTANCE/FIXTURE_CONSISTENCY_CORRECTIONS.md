# TRIAGE Fixture Consistency Corrections

These corrections were made on 2026-09-27 before measured Block 5 IBM Bob runs.
They were not derived from observed Bob failures.

## TRIAGE-006 source precedence

Original fixture prose used an active PRD and active ADR with no supersession but
expected unresolved source conflict.

Active domain governance defines ADR above PRD in fallback precedence. That made
the fixture internally inconsistent: a compliant resolver could select the ADR
instead of abstaining.

Correction:
- preserve both conflicting requirement statements;
- preserve the expected tuple
  `SPEC_AMBIGUITY / SOURCE_CONFLICT / NONE / ABSTAIN`;
- model both sources as active ADRs at the same precedence tier and scope;
- keep no supersession or tie-breaker.

## Severity determinism clarification

The active domain rule file now contains explicit deterministic mappings for:
- `SPEC_AMBIGUITY -> severity NONE`;
- best-practice-only `POTENTIAL_RISK + UNSUPPORTED_BEST_PRACTICE_CLAIM -> MEDIUM`.

These mappings consolidate behavior that was previously spread between frozen
acceptance material and skill guidance. They were added before measured TRIAGE
runs so evaluation does not tune rules against Bob outputs.

No frozen TRIAGE expected tuple changed.
