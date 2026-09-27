---
name: mergeproof
description: Orchestrate a conservative read-only pre-merge verification from explicit scope and source artifacts to a canonical evidence report.
---

# MergeProof Orchestrator

Use this skill for the complete MergeProof evidence workflow.

## Inputs

For the seeded/demo workflow:

1. Read `MERGEPROOF_RUN_CONTEXT.yaml` when present.
2. Read the case descriptor named by `case_descriptor`.
3. Treat all paths in the case descriptor as workspace-root-relative.
4. Use `source_files` as the candidate source inventory.
5. Use `changed_files` as the exact requested change scope.

Do not inspect files outside the opened workspace.
Do not use evaluator or expected-output material even if it is mentioned elsewhere.

## Evidence workflow

1. Resolve relevant source lifecycle, scope, supersession, and authority with `source-authority`.
2. Extract applicable atomic requirements with `requirement-trace`.
3. Inspect changed implementation with `implementation-observation`.
4. Inspect relevant tests with `test-acceptance-audit`.
5. Optionally delegate independent read-only exploration to focused subagents.
   Delegation must not broaden scope or transfer advisory ownership.
6. Classify candidate findings with `evidence-classification`.
7. Apply deterministic project severity rules with `severity-impact`.
8. Run `conflict-abstention` for the preliminary advisory state.
9. Run `self-audit`.
10. If self-audit reports a material correction or new uncertainty, run
    `conflict-abstention` again using corrected evidence.
11. Run `report-synthesis` using the latest advisory state.

## Evidence boundaries

Keep these separate throughout the workflow:

- documented expected behavior;
- observed implementation behavior;
- observed test coverage;
- source authority resolution;
- engineering opinion;
- unresolved uncertainty.

A passing test is evidence about tested behavior, not proof that the requirement is correct.

## Ownership rules

Focused skills produce evidence and classifications.
They do not decide ABSTAIN.

`conflict-abstention` is the single owner of the advisory decision.

`self-audit` may retract or revise claims, but does not choose the advisory.

`report-synthesis` carries forward the latest advisory and never recomputes it.

## Final output

The final user-visible output of this skill is exactly one JSON object conforming to:

`schemas/mergeproof_report.schema.json`

The frozen design authority remains:

`docs/05_PREPRODUCTION/01_CONTRACTS_ACTIVE/FEATURE_SCHEMA_FINAL.yaml`

Do not add analysis-only scratch fields to the final report.
Do not emit a Markdown summary before or after the JSON report.

Populate:
- `repository.commit_sha` from `MERGEPROOF_RUN_CONTEXT.yaml`;
- `repository.changed_files` from the case descriptor;
- source fields from inspected source metadata;
- requirements only from documented source text;
- finding anchors using workspace-root-relative artifact paths;
- `generated_at` as the actual run timestamp.

Never invent a required report value merely to satisfy the schema.

Do not write files.
