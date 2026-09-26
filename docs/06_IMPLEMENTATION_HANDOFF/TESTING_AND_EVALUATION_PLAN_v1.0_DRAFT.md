# Testing & Evaluation Plan

## Test layers

### T1 — deterministic unit tests
- source precedence;
- supersession;
- enum validation;
- evidence completeness;
- advisory aggregation.

### T2 — schema negative tests
- unknown finding class;
- missing anchor;
- invalid severity combination;
- forbidden fake probability field.

### T3 — frozen triage acceptance
TRIAGE-001..008.

### T4 — seeded evaluation corpus
EVAL cases.

### T5 — demo smoke
One end-to-end Bob run producing a valid report.

## Metrics

Report only observed values.

Required final table:
- confirmed finding precision;
- seeded defect recall;
- clean false-positive rate;
- source-anchor validity;
- critical misses;
- abstention correctness.

## No vanity metrics
Do not claim "X% productivity improvement" without a timed baseline.
