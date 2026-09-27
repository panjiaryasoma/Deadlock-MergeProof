# Block 5 Measurement Restart — Skill v1.0.2

## Status

A TRIAGE-001 diagnostic run under skill version `1.0.1` confirmed that the
taxonomy correction worked:

- `BOUNDARY_CONDITION_DRIFT` was selected for the operator/equality drift;
- `MISSING_ACCEPTANCE_TEST` was emitted separately;
- severity and advisory matched the frozen expectations.

However, Bob still narrated intermediate workflow stages before the final JSON,
violating the raw-JSON transport contract.

The v1.0.1 run is retained as diagnostic evidence and is not part of the final
8-case measurement series.

## Correction

Skill version `1.0.2` moves the successful-output transport constraint to the
MergeProof custom-mode instruction and a dedicated project rule, in addition to
the existing orchestrator/report-synthesis instructions.

The correction is general:
- intermediate reasoning remains internal;
- no stage headings or progress narration are user-visible;
- successful output is exactly one raw JSON object;
- no Markdown code fence;
- no prose before or after the object.

No TRIAGE fixture, expected tuple, source-governance rule, severity mapping, or
advisory rule changed.

## Measurement reset

Regenerate all TRIAGE workspaces after pulling this correction.

The final Block 5 series begins only with workspaces whose run context records:

`skill_version: "1.0.2"`

Do not mix v1.0.0, v1.0.1, and v1.0.2 reports in the final aggregate result.
