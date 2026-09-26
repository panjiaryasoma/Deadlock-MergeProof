# Calibration & Uncertainty

## No fake confidence percentages

MergeProof does not output "93% confident."

LLM probabilities are not available or calibrated for this task.

## Evidence-grade model

- `DIRECT` — explicit requirement + explicit implementation/test evidence.
- `CORROBORATED` — multiple independent anchors support the same conclusion.
- `INFERRED` — plausible but requires human confirmation.
- `INSUFFICIENT` — evidence missing or contradictory.

## Behavior

`CONFIRMED_ISSUE` requires DIRECT or CORROBORATED.

INFERRED can only produce `POTENTIAL_RISK` or `SPEC_AMBIGUITY`.

INSUFFICIENT must not produce a confirmed issue.
