# Block 5 Measurement Restart — Skill v1.0.1

## Status

A first TRIAGE-001 IBM Bob run was captured under skill version `1.0.0`.

That run correctly detected the deadline boundary mismatch and missing acceptance
coverage, but it exposed two general workflow-contract gaps:

1. finding-type selection did not explicitly require the most-specific supported
   taxonomy value, so a boundary drift could be emitted as the generic
   `REQUIREMENT_IMPLEMENTATION_MISMATCH`;
2. successful report transport said "JSON only" but did not mechanically prohibit
   introductory prose and Markdown code fences.

The run is retained as diagnostic evidence but is not part of the final 8-case
measurement series.

## Correction

Skill version `1.0.1`:
- adds a general `MOST_SPECIFIC_SUPPORTED_TYPE_WINS` taxonomy policy to the
  active domain rules;
- makes `REQUIREMENT_IMPLEMENTATION_MISMATCH` the fallback finding type;
- strengthens the final response transport contract to raw JSON only.

No frozen TRIAGE expected tuple was changed.

## Measurement reset

After pulling this correction, regenerate all TRIAGE workspaces. The final Block 5
measurement series begins only with workspaces whose
`MERGEPROOF_RUN_CONTEXT.yaml` records:

`skill_version: "1.0.1"`

Do not mix reports from skill v1.0.0 and v1.0.1 in the aggregate result.
