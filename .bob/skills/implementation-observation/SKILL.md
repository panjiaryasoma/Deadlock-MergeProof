---
name: implementation-observation
description: Determine what the implementation actually does, including edge cases, without mixing observation with expected behavior or remediation advice.
---

# Implementation Observation

Describe:
- control flow
- validation behavior
- runtime transformations
- error behavior
- state mutation
- API responses
- boundary behavior

Cite exact repository locations.

Do not:
- call behavior wrong before comparing to authority
- assign severity
- recommend a fix
- convert best practice into expected behavior

Mark unverified runtime/framework claims as `NEEDS_RUNTIME_TEST`.
