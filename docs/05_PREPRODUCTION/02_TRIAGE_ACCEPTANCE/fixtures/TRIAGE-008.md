# TRIAGE-008 — Superseded requirement

## Given
Old PRD says <=; newer ADR explicitly supersedes it with <; code uses <.

## Expected
- finding_class: `NO_ISSUE`
- finding_type: `STALE_SOURCE`
- severity: `NONE`
- advisory: `PASS`

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
