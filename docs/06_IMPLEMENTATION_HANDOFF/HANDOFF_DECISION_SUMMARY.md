# Implementation Handoff — Decision Summary

## Product
MergeProof: Bob-native pre-merge evidence verification.

## Frozen decisions
- custom mode + skill are primary product surface;
- read-only verification by default;
- no autonomous merge authority;
- advisories: PASS / REVIEW_REQUIRED / ABSTAIN;
- evidence grades, not confidence percentages;
- source precedence and explicit supersession are mandatory;
- deterministic validator sits after Bob output;
- synthetic seeded evaluation corpus; no model training.

## MVP demonstration
Use a small seeded repo containing:
1. one explicit boundary drift;
2. one missing acceptance test;
3. one clean refactor control.

Run MergeProof, show evidence report, validate it, show human advisory.
