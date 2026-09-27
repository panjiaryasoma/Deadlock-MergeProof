---
name: implementation-observation
description: Determine what changed implementation actually does, including edge cases, without mixing observation with expected behavior or remediation advice.
---

# Implementation Observation

Inspect only the requested changed-file scope unless a directly referenced dependency
is required to understand behavior.

If the case descriptor provides `change_evidence`, inspect that artifact before
classifying the kind of change. Use it to distinguish a refactor from a behavioral
change; do not infer a rename or prior implementation state that is not evidenced.

Describe:
- control flow;
- validation behavior;
- runtime transformations;
- error behavior;
- state mutation;
- API responses;
- boundary behavior.

For every material observation provide a repository anchor with:
- workspace-root-relative artifact path;
- stable locator such as function/class/symbol and line when visible;
- short excerpt only when needed.

Do not:
- call behavior wrong before comparing it to authority;
- assign severity;
- recommend a fix;
- convert best practice into expected behavior.

Mark unverified runtime/framework claims as `NEEDS_RUNTIME_TEST`.
