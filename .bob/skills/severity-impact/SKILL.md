---
name: severity-impact
description: Describe impact and apply severity only when an explicit project severity rubric exists; otherwise prevent model-invented HIGH/MEDIUM/LOW labels.
---

# Severity & Impact

First describe impact factually.

Then search for an explicit project severity rubric.

If found:
- cite it
- apply it deterministically

If absent:
- severity = `UNSPECIFIED_BY_PROJECT`

Never infer severity from intuition.
