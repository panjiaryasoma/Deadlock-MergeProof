---
name: report-synthesis
description: Produce the final canonical MergeProof JSON report by carrying forward the latest advisory state without recomputing it.
---

# Report Synthesis

This skill has a strict precondition.

Do not invoke it unless evidence collection, classification, preliminary
advisory, self-audit, any required reconciliation, and run-provenance validation
are complete.

`MERGEPROOF_RUN_CONTEXT.yaml` must contain:
- `run_id`
- `repository_commit_sha`
- `changed_files`
- `source_ids`
- `bob_mode_version`
- `skill_version`
- `timestamp`
- `report_schema_version`

If any are absent, the orchestrator reports a workflow setup error before this
skill runs.

## Advisory ownership

Use the latest advisory state produced by `conflict-abstention`.
Use reconciliation output when one exists.
Never recompute or override the advisory.

## Canonical contract

Read the executable shape from:
`schemas/mergeproof_report.schema.json`

The design authority remains:
`docs/05_PREPRODUCTION/01_CONTRACTS_ACTIVE/FEATURE_SCHEMA_FINAL.yaml`

## Field provenance

Populate:
- `report_version`: run-context `report_schema_version`;
- `run_id`: run-context `run_id`;
- `advisory`: latest conflict-abstention state;
- `repository.commit_sha`: run-context `repository_commit_sha`;
- `repository.changed_files`: run-context `changed_files`;
- `sources`: inspected registered source facts;
- `requirements`: traced documented requirements when included;
- `findings`: classified evidence with canonical anchors;
- `generated_at`: run-context `timestamp`;
- `human_override`: omit unless an actual human override is supplied.

Preserve project-specific `source.authority` strings exactly.
Use workspace-root-relative artifact paths in anchors.

## Final response transport contract

The successful final response is raw JSON and nothing else.

Mechanical requirements:
- the first non-whitespace character MUST be `{`;
- the last non-whitespace character MUST be `}`;
- do not emit an introductory sentence;
- do not emit a closing sentence;
- do not wrap the object in ```json` or any Markdown code fence;
- do not emit Markdown headings, bullets, workflow notes, self-audit notes,
  source-resolution scratch state, or merge/approve/reject language.

Return exactly one JSON object matching the canonical schema.

If a required report value cannot be grounded, do not invent it. This skill must
not be invoked; the orchestrator reports a workflow setup error before final
output synthesis.
