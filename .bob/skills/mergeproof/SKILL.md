---
name: mergeproof
description: Orchestrate a conservative read-only pre-merge verification from explicit scope and source artifacts to a canonical evidence report.
---

# MergeProof Orchestrator

Use this skill for the complete MergeProof evidence workflow.

## Run provenance gate

Read `MERGEPROOF_RUN_CONTEXT.yaml` first.

Before analysis, require:
- `run_id`
- `repository_commit_sha`
- `changed_files`
- `source_ids`
- `bob_mode_version`
- `skill_version`
- `timestamp`
- `report_schema_version`

Read the case descriptor named by `case_descriptor`.
Treat all case paths as workspace-root-relative.
Use `source_files` as the candidate source inventory, `source_registry` as
canonical source metadata when present, and `changed_files` as the exact
requested change scope. Inspect optional `change_evidence` before claiming a
specific change type such as a refactor.

Read `output_contract_addendum` when present.

If required run provenance is missing, stop before report synthesis and surface
a workflow setup error. Do not fabricate a canonical report.

Do not inspect files outside the opened workspace.
Do not use evaluator or expected-output material.

## Evidence workflow

1. Resolve source lifecycle, scope, supersession, and authority with `source-authority`.
2. Extract applicable atomic requirements with `requirement-trace`.
3. Inspect changed implementation with `implementation-observation`.
4. Inspect relevant tests with `test-acceptance-audit`.
5. Optionally delegate independent read-only exploration to focused subagents.
   Delegation must not broaden scope or transfer advisory ownership.
6. Classify candidate findings with `evidence-classification`, applying the
   active most-specific finding-type policy.
7. Apply deterministic project severity rules with `severity-impact`.
8. Run `conflict-abstention` for the preliminary advisory state.
9. Run `self-audit`.
10. If self-audit reports a material correction or new uncertainty, run
    `conflict-abstention` again using corrected evidence.
11. Run `report-synthesis` using the latest advisory state.

Keep documented expected behavior, observed implementation, observed test
coverage, authority resolution, engineering opinion, and unresolved uncertainty
separate until classification.

## Ownership

Focused skills produce evidence and classifications.
`conflict-abstention` is the single advisory decision point.
`self-audit` may revise claims but does not choose the advisory.
`report-synthesis` carries forward the latest advisory and never recomputes it.

## Successful final output

Return exactly one raw JSON object conforming to
`schemas/mergeproof_report.schema.json`.

The response MUST start with `{` and end with `}`.
Do not add any text before or after it and do not use Markdown code fences.

Populate:
- `report_version` from run-context `report_schema_version`;
- `run_id` from run context;
- `repository.commit_sha` from `repository_commit_sha`;
- `repository.changed_files` from run-context `changed_files`;
- source fields from the registered source metadata;
- requirements only from documented source text;
- anchors with workspace-root-relative artifact paths;
- `generated_at` from run-context `timestamp`.

During Blocks 4 through 6 do not append a Markdown summary. The active output
addendum assigns the FR-014 summary to Block 7 after deterministic validation.

Never invent a required report value merely to satisfy the schema.
Do not write files.
