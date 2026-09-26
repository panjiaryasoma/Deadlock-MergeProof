# TRIAGE-004 — Material ambiguity

## Given
Requirement says 'respond quickly' with no measurable bound; implementation changed timeout.

## Expected
- finding_class: `SPEC_AMBIGUITY`
- finding_type: `REQUIREMENT_IMPLEMENTATION_MISMATCH`
- severity: `NONE`
- advisory: `ABSTAIN`

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
