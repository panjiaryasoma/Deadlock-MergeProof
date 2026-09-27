---
name: test-acceptance-audit
description: Verify whether tests cover acceptance boundaries implied by applicable requirements and changed behavior without treating test existence as proof of correctness.
---

# Test & Acceptance Audit

Inspect the tests in the requested change scope and directly relevant test files.

Check:
- equality boundaries;
- negative/error cases;
- required vs optional semantics;
- enum/schema changes;
- defaults;
- nullability;
- backward compatibility;
- explicit regression cases.

Passing tests prove tested behavior, not requirement correctness.

Only classify a missing acceptance test when:
1. an applicable requirement or acceptance criterion defines the behavior; and
2. inspected tests do not exercise that behavior.

When test coverage is missing, anchor the inspected test surface that supports the
absence claim. Do not invent a nonexistent test location.
