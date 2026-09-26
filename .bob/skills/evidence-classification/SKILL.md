---
name: evidence-classification
description: Convert candidate observations into disciplined MergeProof findings using evidence grades and strict separation of violations, risks, ambiguity, and clean cases.
---

# Evidence Classification

Allowed:
- `CONFIRMED_ISSUE`
- `POTENTIAL_RISK`
- `SPEC_AMBIGUITY`
- `NO_ISSUE`

Confirmed issue requires:
- applicable authoritative expected behavior
- direct/corroborated source evidence
- direct/corroborated repo/test evidence
- demonstrated mismatch

Potential risk: concern is plausible but not established as local requirement.

Spec ambiguity: expected behavior cannot be resolved reliably.

No issue: evidence supports alignment or harmless change.
