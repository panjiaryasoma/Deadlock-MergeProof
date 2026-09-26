---
name: self-audit
description: Critically re-check MergeProof's draft findings, challenge assumptions, downgrade unsupported claims, and emit explicit correction state before final reconciliation.
---

# Self-Audit

Treat every earlier conclusion as provisional.

For each material prior claim classify:
- `CONFIRMED`
- `PARTIALLY_SUPPORTED`
- `UNSUPPORTED`
- `NEEDS_RUNTIME_TEST`

## Challenge questions

- Did I confuse ACTIVE with AUTHORITATIVE?
- Did I assume document precedence?
- Did I mix observed behavior with expected behavior?
- Did I turn best practice into a requirement?
- Did I invent severity?
- Did I silently choose a product decision?
- Did I group runtime cases that behave differently?
- Did I miss extra-field, null, boundary, or negation cases?
- Did I rely on framework behavior that was not actually verified?
- Did I recommend a fix before proving a violation?

## Correction behavior

If an earlier claim is wrong:
- explicitly retract it;
- state the corrected claim;
- identify the evidence that changed the conclusion.

## Required reconciliation output

Always emit:

```text
material_correction: true | false
new_uncertainty: true | false
claims_changed:
  - <claim id or concise identifier>
```

Set `material_correction: true` when a correction changes evidence,
classification, impact, requirement interpretation, or another fact that could
affect the advisory.

Set `new_uncertainty: true` when self-audit introduces or reveals unresolved
authority, ambiguity, missing evidence, NEEDS_RUNTIME_TEST, or an unspecified
product decision that could affect the advisory.

## Authority boundary

Self-audit does **not** decide:
- PASS
- REVIEW_REQUIRED
- ABSTAIN

If `material_correction` or `new_uncertainty` is true, send the corrected state
back to `conflict-abstention` for reconciliation.

Do not hide revisions.
