---
name: report-synthesis
description: Produce the final canonical MergeProof JSON report by carrying forward the latest advisory state without recomputing it.
---

# Report Synthesis

Do not synthesize until evidence collection, classification, preliminary advisory,
self-audit, and any required reconciliation are complete.

## Advisory ownership

`report-synthesis` is not an advisory decision engine.

It must:
- use the latest advisory state produced by `conflict-abstention`;
- use reconciliation output when a reconciliation pass exists;
- otherwise use the preliminary advisory;
- never recompute or override the advisory.

## Canonical contract

Read the executable report shape from:

`schemas/mergeproof_report.schema.json`

The frozen design authority is:

`docs/05_PREPRODUCTION/01_CONTRACTS_ACTIVE/FEATURE_SCHEMA_FINAL.yaml`

Do not define a parallel report schema in this skill.

## Field provenance

Populate report fields only from grounded workflow evidence:

- `report_version`: frozen contract version;
- `run_id`: nonempty run identifier grounded in current run context;
- `advisory`: latest conflict-abstention state;
- `repository.commit_sha`: `MERGEPROOF_RUN_CONTEXT.yaml`;
- `repository.changed_files`: case descriptor;
- `sources`: registered source facts;
- `requirements`: traced documented requirements when included;
- `findings`: classified evidence with canonical anchors;
- `generated_at`: actual run timestamp;
- `human_override`: omit unless an actual human override is supplied.

Preserve project-specific `source.authority` strings exactly.
Use workspace-root-relative artifact paths in anchors.

## Final response contract

Return exactly one JSON object matching the canonical schema.

Do not prepend or append:
- Markdown explanation;
- workflow notes;
- self-audit notes;
- source-resolution scratch state;
- unresolved-question prose outside canonical fields;
- merge/approve/reject language.

If a required report value cannot be grounded, do not invent it.
Stop report synthesis and state that the workflow is incomplete.
