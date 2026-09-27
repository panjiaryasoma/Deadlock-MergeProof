---
name: severity-impact
description: Describe impact and apply only frozen MergeProof severity values from explicit project rules; never invent or emit out-of-schema severity labels.
---

# Severity & Impact

First describe impact factually.

Then resolve severity from the active deterministic project rules.

## Required sources

Use:

`docs/03_EVALUATION_AND_DOMAIN_RULES/domain_rules_v1.0.yaml`

Use:

`docs/05_PREPRODUCTION/01_CONTRACTS_ACTIVE/FEATURE_SCHEMA_FINAL.yaml`

for legal report values.

## Resolution order

1. Apply any established `rules[].then.severity` mapping in
   `domain_rules_v1.0.yaml`.
2. If no exact rule applies, use the severity rubric in that same file.
3. If neither path resolves severity deterministically, do not guess.

This keeps ambiguity/source-conflict and unsupported-best-practice severity
resolution inside one active rule source rather than scattering it across skills
or hidden acceptance fixtures.

Allowed report values:
- `CRITICAL`
- `HIGH`
- `MEDIUM`
- `LOW`
- `NONE`

Never emit `UNSPECIFIED_BY_PROJECT`.

If available frozen rules do not deterministically map a finding to a legal severity:
- describe impact factually;
- mark severity resolution as unresolved analysis state;
- send that state to self-audit / conflict-abstention;
- do not guess a severity.

Impact and severity are not synonyms.
