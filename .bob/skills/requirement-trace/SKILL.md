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

For each requirement return:
- requirement ID if available
- source anchor
- exact expectation
- scope
- ambiguity status
- candidate implementation anchors
- candidate test anchors

Do not infer undocumented business requirements.
