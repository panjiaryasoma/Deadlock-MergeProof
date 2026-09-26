# TRIAGE-005 — Missing acceptance test

## Given
Explicit requirement defines 404 for unknown ID; route implements 404 but test absent.

## Expected
- finding_class: `CONFIRMED_ISSUE`
- finding_type: `MISSING_ACCEPTANCE_TEST`
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
