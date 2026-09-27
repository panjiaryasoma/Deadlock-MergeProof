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

Before handing a finding to report synthesis, ensure its class, type, evidence grade,
severity, and anchors use only values and fields present in the canonical report contract.
