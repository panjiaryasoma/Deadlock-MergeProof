# Evaluation & Domain Rules — Second Brain

## Read order

1. `domain_rules_v1.0.yaml`
2. `SOURCE_SCHEMA.md`
3. `feature_schema_v1.0.yaml`
4. `evaluation_spec_v1.0.yaml`
5. `evaluation_matrix_v1.0.csv`
6. `feature_traceability_v1.0.csv`
7. `SOURCE_EVALUATION_SUITE_001-030.md`
8. `validation_report.txt`

## Canonical principle

MergeProof is not trying to predict "bad code."

It is trying to produce **defensible evidence about alignment**.

Therefore:

```text
weak source
    |
    v
weak/ambiguous claim
    |
    v
ABSTAIN or POTENTIAL_RISK
```

Never:

```text
weak source
    |
    v
confident HIGH severity requirement violation
```

## Source vs evidence vs authority

- **Source** = where a statement came from.
- **Evidence** = concrete support for a finding.
- **Authority** = whether that source is allowed to define expected behavior.
- **Scope** = whether the source applies to this change.

All four must survive validation.

## Bob-specific role

Bob is used for:
- repository/document understanding;
- candidate trace recovery;
- focused subagent exploration;
- finding synthesis.

Deterministic files/rules are used for:
- enum validity;
- source precedence invariants;
- evidence completeness;
- advisory aggregation constraints.

That split is intentional.
