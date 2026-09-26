# Label Policy

## Ground-truth labels

Each seeded case is labeled before Bob sees it.

Allowed case labels:
- `TRUE_DRIFT`
- `TRUE_MISSING_TEST`
- `CLEAN`
- `AMBIGUOUS`
- `SOURCE_CONFLICT`
- `RISK_NOT_REQUIREMENT`

## Mapping

| Ground truth | Expected class |
|---|---|
| TRUE_DRIFT | CONFIRMED_ISSUE |
| TRUE_MISSING_TEST | CONFIRMED_ISSUE |
| CLEAN | NO_ISSUE |
| AMBIGUOUS | SPEC_AMBIGUITY |
| SOURCE_CONFLICT | SPEC_AMBIGUITY |
| RISK_NOT_REQUIREMENT | POTENTIAL_RISK |

## Labeling rule

Never derive the expected label from Bob's output. Ground truth is fixed in fixture metadata first.
