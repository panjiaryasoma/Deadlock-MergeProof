# Evaluation Corpus Strategy

## Decision

**No model training dataset will be created for the MVP.**

MergeProof uses IBM Bob as the reasoning environment. The dataset exists solely to evaluate the workflow.

## Corpus composition

### A. Seeded synthetic cases — primary
Small repositories/artifacts with one controlled mutation per case:
- boundary operator;
- required/optional field;
- enum value;
- HTTP status;
- default value;
- negation;
- missing test;
- source conflict;
- stale source;
- harmless refactor.

### B. Clean controls
Cases with no behavior drift.

### C. Ambiguity controls
Cases where the correct behavior is `ABSTAIN`.

### D. Real-world references
Used for problem framing and mutation design only. Do not copy proprietary code.

## Why synthetic-first

Ground truth is explicit.
The mutation is known.
False positives are measurable.
The demo can be reproduced locally.
No licensing or secret-data problem is introduced 30 hours before deadline, which would be a remarkably human thing to do.
