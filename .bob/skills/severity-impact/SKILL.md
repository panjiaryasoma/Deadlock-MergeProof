---
name: severity-impact
description: Describe impact and apply only frozen MergeProof severity values from explicit project rules; never invent or emit out-of-schema severity labels.
---

# Severity & Impact

First describe impact factually.

Then resolve severity from the frozen MergeProof severity contract.

## Canonical sources

Use:
- `docs/03_EVALUATION_AND_DOMAIN_RULES/domain_rules_v1.0.yaml`;
- `docs/05_PREPRODUCTION/02_TRIAGE_ACCEPTANCE/TRIAGE_EVALUATION_SUITE.md`;
- the matching fixture under `docs/05_PREPRODUCTION/02_TRIAGE_ACCEPTANCE/fixtures/` when one applies;
- `docs/05_PREPRODUCTION/01_CONTRACTS_ACTIVE/FEATURE_SCHEMA_FINAL.yaml` for legal enum values.

Allowed report values are only:
- `CRITICAL`
- `HIGH`
- `MEDIUM`
- `LOW`
- `NONE`

## Frozen ambiguity mapping

When the finding is a material `SPEC_AMBIGUITY`:
- severity = `NONE`.

When a `SOURCE_CONFLICT` is represented by `SPEC_AMBIGUITY`:
- severity = `NONE`;
- advisory handling remains the responsibility of `conflict-abstention`.

## No invented fallback

Never emit `UNSPECIFIED_BY_PROJECT`.

If the frozen rules do not deterministically map a finding to a legal severity:
- describe impact factually;
- mark the severity contract as unresolved;
- send that unresolved state to self-audit / conflict-abstention;
- do not guess a severity.

Never infer severity from intuition.
