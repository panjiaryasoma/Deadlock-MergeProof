---
name: test-acceptance-audit
description: Verify whether tests cover acceptance boundaries implied by applicable requirements and changed behavior without treating test existence as proof of correctness.
---

# Test & Acceptance Audit

Check:
- equality boundaries
- negative/error cases
- required vs optional semantics
- enum/schema changes
- defaults
- nullability
- backward compatibility
- explicit regression cases

Passing tests prove tested behavior, not requirement correctness.

Only call `MISSING_ACCEPTANCE_TEST` when an applicable requirement or
acceptance criterion defines behavior that lacks test evidence.
