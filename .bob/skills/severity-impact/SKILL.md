---
name: severity-impact
description: Describe impact and apply only frozen MergeProof severity values from explicit project rules; never invent or emit out-of-schema severity labels.
---

# Severity & Impact

First describe impact factually.

Then resolve severity from available frozen project rules.

## Required source in isolated/demo workspace

Use:

`docs/03_EVALUATION_AND_DOMAIN_RULES/domain_rules_v1.0.yaml`

Use:

`docs/05_PREPRODUCTION/01_CONTRACTS_ACTIVE/FEATURE_SCHEMA_FINAL.yaml`

for legal report values.

When running in the full repository, frozen triage fixtures may be used as additional
acceptance evidence, but they are not required for severity resolution when the domain
rules already map the finding deterministically.

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
