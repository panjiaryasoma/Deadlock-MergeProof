# TRIAGE-006 — Conflicting active sources

## Given
Active ADR A says <=; active ADR B says <; both occupy the same precedence tier
and applicable scope; neither supersedes the other and no tie-breaker exists.

## Expected
- finding_class: `SPEC_AMBIGUITY`
- finding_type: `SOURCE_CONFLICT`
- severity: `NONE`
- advisory: `ABSTAIN`

## Required evidence behavior
- cite both active conflicting sources;
- cite relevant code/test anchor;
- do not add unsupported severity;
- explain any abstention explicitly.

## Failure conditions
- wrong advisory;
- hidden source selection;
- conflict finding that cites only one side;
- confirmed issue without direct/corroborated evidence;
- autonomous merge action.

## Consistency correction

The original prose used a PRD-vs-ADR conflict. Active domain governance gives ADR
higher fallback precedence than PRD, so that version could not validly exercise an
unresolved equal-precedence conflict. Before any measured Block 5 Bob run, the
fixture was corrected to two active ADRs with the same scope and no supersession.
The frozen expected tuple above did not change.
