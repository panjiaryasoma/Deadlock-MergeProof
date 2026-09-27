---
name: evidence-classification
description: Convert candidate observations into disciplined MergeProof findings using evidence grades and strict separation of violations, risks, ambiguity, and clean cases.
---

# Evidence Classification

Allowed finding classes:
- `CONFIRMED_ISSUE`
- `POTENTIAL_RISK`
- `SPEC_AMBIGUITY`
- `NO_ISSUE`

Use `CONFIRMED_ISSUE` only when all are present:
- applicable authoritative expected behavior;
- DIRECT or CORROBORATED source evidence;
- DIRECT or CORROBORATED repository/test evidence;
- demonstrated mismatch.

Use `POTENTIAL_RISK` for a plausible concern not established as a local requirement violation.

Use `SPEC_AMBIGUITY` when expected behavior cannot be resolved reliably.

Use `NO_ISSUE` when evidence supports alignment or harmlessness within evaluated scope.

## Finding-type selection

Read `finding_type_selection` from
`docs/03_EVALUATION_AND_DOMAIN_RULES/domain_rules_v1.0.yaml`.

Apply `MOST_SPECIFIC_SUPPORTED_TYPE_WINS`.

In particular:
- exact inclusion/exclusion, equality, deadline, or comparison-operator drift is
  `BOUNDARY_CONDITION_DRIFT`, not the generic
  `REQUIREMENT_IMPLEMENTATION_MISMATCH`;
- missing explicit acceptance coverage is `MISSING_ACCEPTANCE_TEST`;
- API request/response contract drift is `API_CONTRACT_DRIFT`;
- enum/type/nullability/schema drift is `ENUM_OR_SCHEMA_DRIFT`;
- unresolved authoritative-source disagreement is `SOURCE_CONFLICT`;
- explicit supersession/stale-source reasoning is `STALE_SOURCE`. If a relevant
  superseded source and its active superseding source are both present,
  `STALE_SOURCE` takes precedence over `HARMLESS_REFACTOR`;
- external-guidance-only concerns are `UNSUPPORTED_BEST_PRACTICE_CLAIM`;
- `HARMLESS_REFACTOR` is allowed only when explicit change evidence supports an
  internal behavior-preserving refactor. Do not use it merely because current
  implementation and tests align with the active requirement.

Use `REQUIREMENT_IMPLEMENTATION_MISMATCH` only as the generic fallback when no
more-specific supported type applies.

Do not collapse two independently supported issues into one finding merely because
they share the same requirement. For example, a boundary implementation drift and a
missing boundary test may be separate findings.

Before handing a finding to report synthesis, ensure its class, type, evidence grade,
severity, and anchors use only values and fields present in the canonical report contract.
