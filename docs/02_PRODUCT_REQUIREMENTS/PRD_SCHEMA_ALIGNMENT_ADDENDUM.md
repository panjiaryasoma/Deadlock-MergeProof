# PRD ↔ Schema Alignment Addendum

## Purpose

This addendum prevents the PRD, feature schema, report contract, and evaluation fixtures from drifting apart before implementation even begins. That would be impressively on-brand, but useless.

## Canonical enum alignment

| Concept | Canonical values |
|---|---|
| Finding class | CONFIRMED_ISSUE, POTENTIAL_RISK, SPEC_AMBIGUITY, NO_ISSUE |
| Advisory | PASS, REVIEW_REQUIRED, ABSTAIN |
| Evidence grade | DIRECT, CORROBORATED, INFERRED, INSUFFICIENT |
| Severity | CRITICAL, HIGH, MEDIUM, LOW, NONE |
| Source state | ACTIVE, SUPERSEDED, CONFLICTING, UNKNOWN |
| Finding status | OPEN, DISMISSED_BY_RULE, NEEDS_HUMAN_REVIEW |

## Invariants

1. `CONFIRMED_ISSUE` cannot use `INSUFFICIENT` evidence.
2. `NO_ISSUE` must use severity `NONE`.
3. `SPEC_AMBIGUITY` forces aggregate advisory `ABSTAIN` unless the ambiguity is explicitly outside changed scope.
4. `SOURCE_CONFLICT` between authoritative in-scope sources forces `ABSTAIN`.
5. A `POTENTIAL_RISK` may produce `REVIEW_REQUIRED`, but it cannot claim requirement violation.
6. A best-practice recommendation with no source requirement is never `CONFIRMED_ISSUE`.
7. `PASS` requires no unresolved confirmed issue, no in-scope source conflict, and no unresolved material ambiguity.
8. All findings require at least one repository anchor; non-clean findings additionally require one source/test anchor appropriate to the finding type.

## Source-of-truth order

Explicit supersession metadata overrides generic precedence.

Fallback precedence:
1. active machine-readable contract / schema for its declared scope;
2. active acceptance criteria specifically tied to the change;
3. explicit ADR / decision record with effective date;
4. active PRD requirement;
5. current repository documentation;
6. issue/PR prose;
7. external best-practice material.

External guidance can establish risk context but cannot silently become a project requirement.

## Change control

Any implementation that needs a new enum, finding type, advisory, or required field MUST first update:
- `feature_schema_v1.0.yaml`;
- `domain_rules_v1.0.yaml`;
- traceability CSV;
- affected evaluation fixtures.

No ad-hoc schema mutation during coding.
