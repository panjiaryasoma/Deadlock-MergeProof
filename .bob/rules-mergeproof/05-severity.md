# Severity Rule

Do not invent severity.

The frozen MergeProof report contract allows only:
- `CRITICAL`
- `HIGH`
- `MEDIUM`
- `LOW`
- `NONE`

Resolve severity from the frozen MergeProof rules and acceptance artifacts, especially:
- `docs/03_EVALUATION_AND_DOMAIN_RULES/domain_rules_v1.0.yaml`
- `docs/05_PREPRODUCTION/02_TRIAGE_ACCEPTANCE/TRIAGE_EVALUATION_SUITE.md`
- `docs/05_PREPRODUCTION/02_TRIAGE_ACCEPTANCE/fixtures/`

Apply the mapping deterministically.

For frozen ambiguity cases:
- material `SPEC_AMBIGUITY` uses severity `NONE`;
- `SOURCE_CONFLICT` represented as `SPEC_AMBIGUITY` uses severity `NONE`;
- the advisory may still be `ABSTAIN`.

Never emit `UNSPECIFIED_BY_PROJECT` or any other out-of-schema severity value.

If no deterministic severity mapping can be resolved from the frozen project rules,
do not guess. Surface the unresolved severity-contract state for self-audit and
conflict-abstention.

Impact and severity are not synonyms.
