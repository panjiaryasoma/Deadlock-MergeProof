---
name: requirement-trace
description: Extract atomic requirements and trace them to changed implementation and tests while preserving exact operators, negation, schema semantics, and boundaries.
---

# Requirement Trace

Preserve exact semantics:

- `<`, `<=`, `>`, `>=`, `==`
- MUST / MUST NOT
- required / optional
- enum values
- nullability
- defaults
- HTTP status codes
- field names/types
- deadlines and boundaries

For each applicable requirement capture:
- requirement ID;
- source ID;
- exact statement;
- declared scope;
- declared criticality;
- ambiguity only when supported by source evidence;
- exact source anchor;
- candidate implementation anchors;
- candidate test anchors.

Do not synthesize missing requirement metadata.
Do not infer undocumented business requirements.
