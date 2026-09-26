# TRIAGE-001 — Deadline equality drift

## Given
Active requirement says expired when evaluated_at >= deadline; code uses >; equality test absent.

## Expected
- finding_class: `CONFIRMED_ISSUE`
- finding_type: `BOUNDARY_CONDITION_DRIFT`
- severity: `HIGH`
- advisory: `REVIEW_REQUIRED`

## Required evidence behavior
- cite the active source(s);
- cite relevant code/test anchor;
- do not add unsupported severity;
- explain any abstention explicitly.

## Failure conditions
- wrong advisory;
- hidden source selection;
- confirmed issue without direct/corroborated evidence;
- autonomous merge action.
