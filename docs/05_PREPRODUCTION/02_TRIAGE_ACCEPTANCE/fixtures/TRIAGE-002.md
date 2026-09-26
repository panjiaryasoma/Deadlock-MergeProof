# TRIAGE-002 — API required field drift

## Given
Active contract marks email required; implementation accepts missing email.

## Expected
- finding_class: `CONFIRMED_ISSUE`
- finding_type: `API_CONTRACT_DRIFT`
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
