---
name: conflict-abstention
description: Serve as the single advisory decision point for unresolved source conflicts, ambiguous requirements, missing authority, insufficient evidence, or invented product decisions.
---

# Conflict & Abstention

This skill is the **single owner of ABSTAIN decisions**.

It may run:
1. once before self-audit to produce a preliminary advisory state;
2. again after self-audit when material corrections or new uncertainty exist.

Focused skills and self-audit may emit uncertainty, but they do not decide ABSTAIN.

## ABSTAIN triggers

Return `ABSTAIN` when any material condition remains unresolved:

- applicable authoritative sources conflict;
- authority hierarchy is unresolved;
- source scope is unclear;
- requirement wording is materially ambiguous;
- evidence needed for a reliable conclusion is missing;
- deciding would require inventing a product decision.

## Non-ABSTAIN handling

Not every uncertainty token automatically means ABSTAIN.

Evaluate whether the unresolved condition is material to the advisory.

Examples:
- a non-material runtime uncertainty outside evaluated scope may remain disclosed
  without forcing ABSTAIN;
- a severity-contract gap is not itself proof of a requirement violation; preserve
  it as unresolved state and do not invent an out-of-schema severity;
- an unsupported finding removed by self-audit does not force ABSTAIN unless its
  removal reveals a new material evidence gap.

## Reconciliation pass

When re-run after `self-audit`:
- consume corrected findings and uncertainty state;
- discard stale preliminary conclusions that depended on retracted claims;
- recompute the advisory from the corrected evidence;
- label the result as the **latest advisory state**.

## Required output

State:
1. pass type: `PRELIMINARY` or `RECONCILIATION`;
2. material unresolved conditions;
3. why each condition does or does not cross the ABSTAIN threshold;
4. latest advisory state:
   - `PASS`
   - `REVIEW_REQUIRED`
   - `ABSTAIN`

Do not make the human merge decision.
