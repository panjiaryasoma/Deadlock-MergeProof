# Severity Rule

Do not invent severity.

The frozen MergeProof report contract allows only:
- `CRITICAL`
- `HIGH`
- `MEDIUM`
- `LOW`
- `NONE`

The primary deterministic severity source is:

`docs/03_EVALUATION_AND_DOMAIN_RULES/domain_rules_v1.0.yaml`

The canonical legal values are frozen in:

`docs/05_PREPRODUCTION/01_CONTRACTS_ACTIVE/FEATURE_SCHEMA_FINAL.yaml`

Full-repository acceptance fixtures may corroborate a mapping when available, but
verification must not depend on fixture files that are intentionally absent from an
isolated evaluation workspace.

Never emit `UNSPECIFIED_BY_PROJECT` or another out-of-schema value.

If available frozen rules do not deterministically resolve severity, do not guess.
Surface the unresolved severity state to self-audit and conflict-abstention.

Impact and severity are not synonyms.
