---
name: mergeproof
description: Orchestrate a conservative read-only pre-merge verification across source authority, requirements, implementation, tests, evidence, reconciliation, and final advisory.
---

# MergeProof Orchestrator

Use this skill for the complete MergeProof workflow.

## Workflow

1. Define change scope.
2. Resolve relevant sources with `source-authority`.
3. Trace applicable requirements with `requirement-trace`.
4. Observe actual code behavior with `implementation-observation`.
5. Inspect relevant tests with `test-acceptance-audit`.
6. Classify candidate findings with `evidence-classification`.
7. Apply project severity rules through `severity-impact`.
8. Run `conflict-abstention` to produce the **preliminary advisory state**.
9. Run `self-audit` to challenge all material claims and emit:
   - `material_correction`
   - `new_uncertainty`
   - `claims_changed`
10. Reconciliation gate:
   - if `material_correction == true` or `new_uncertainty == true`,
     run `conflict-abstention` again using the corrected evidence;
   - otherwise preserve the preliminary advisory state.
11. Run `report-synthesis` using the **latest conflict-abstention advisory state**.

## Ownership rules

Focused skills emit evidence, classifications, uncertainty, or verification state.
They do not decide ABSTAIN.

`conflict-abstention` is the **single owner** of ABSTAIN decisions.
It may run more than once.

`self-audit` may invalidate or revise prior claims, but it does not decide the final advisory.

`report-synthesis` does not calculate PASS / REVIEW_REQUIRED / ABSTAIN.
It only carries forward the latest advisory state produced by `conflict-abstention`.

## Mandatory principles

- ACTIVE != AUTHORITATIVE.
- observed behavior != expected behavior.
- best practice != project requirement.
- AI finding != verified finding.
- impact != severity.
- unresolved material conflict => evaluated by `conflict-abstention`.
- human reviewer owns merge authority.

## Output

Return:
1. Scope
2. Source inventory
3. Authority resolution
4. Requirement trace
5. Observed implementation
6. Test evidence
7. Findings
8. Preliminary advisory state
9. Self-audit corrections
10. Reconciliation result
11. Unresolved questions
12. Final advisory

Do not write files.
