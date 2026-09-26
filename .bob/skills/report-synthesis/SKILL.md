---
name: report-synthesis
description: Produce the final MergeProof report by carrying forward the latest reconciled advisory state without recomputing PASS, REVIEW_REQUIRED, or ABSTAIN.
---

# Report Synthesis

Do not synthesize until verification, preliminary abstention analysis,
self-audit, and any required reconciliation pass are complete.

## Advisory ownership

`report-synthesis` is **not** an advisory decision engine.

It must:
- identify the latest advisory state produced by `conflict-abstention`;
- use the reconciliation advisory when a reconciliation pass exists;
- otherwise use the preliminary advisory;
- never recompute or override that advisory.

If no valid advisory state from `conflict-abstention` exists, do not invent one.
Report the workflow state as incomplete.

## Canonical report contract

The frozen active implementation contract is:

`docs/05_PREPRODUCTION/01_CONTRACTS_ACTIVE/FEATURE_SCHEMA_FINAL.yaml`

Do not define or maintain a parallel report schema inside this skill.
Detailed executable schema validation belongs to production Block 2.

## Human-readable output order

1. Scope
2. Source inventory
3. Authority resolution
4. Requirement trace
5. Observed implementation
6. Test evidence
7. Findings
8. Preliminary advisory
9. Self-audit corrections
10. Reconciliation result, if any
11. Unresolved questions
12. Final advisory

## Final advisory

Copy exactly one latest advisory state:
- `PASS`
- `REVIEW_REQUIRED`
- `ABSTAIN`

Never claim:
- merged;
- approved;
- rejected;
- human authorization.

The final advisory remains decision support only.
