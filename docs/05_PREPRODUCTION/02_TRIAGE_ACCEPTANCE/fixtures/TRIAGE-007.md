# TRIAGE-007 — Best-practice only

## Given
No project requirement for runtime schema validator; external OWASP guidance recommends validation.

## Expected
- finding_class: `POTENTIAL_RISK`
- finding_type: `UNSUPPORTED_BEST_PRACTICE_CLAIM`
- severity: `MEDIUM`
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
