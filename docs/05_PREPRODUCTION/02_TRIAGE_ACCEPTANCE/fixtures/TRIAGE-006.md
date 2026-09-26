# TRIAGE-006 — Conflicting active sources

## Given
PRD says <=; active ADR says <; no supersession metadata.

## Expected
- finding_class: `SPEC_AMBIGUITY`
- finding_type: `SOURCE_CONFLICT`
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
