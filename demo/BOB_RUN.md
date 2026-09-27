# MergeProof Bob Run

Open the generated demo workspace in IBM Bob.

1. Activate the `MergeProof` mode.
2. Invoke the `mergeproof` skill.
3. Read `MERGEPROOF_RUN_CONTEXT.yaml`.
4. Verify the context contains `run_id`, `repository_commit_sha`,
   `changed_files`, `source_ids`, `bob_mode_version`, `skill_version`,
   `timestamp`, and `report_schema_version`.
5. Read the case descriptor referenced by that context.
6. Resolve source authority before asserting expected behavior.
7. Inspect only the requested changed-file scope and directly relevant evidence.
8. Use focused read-only subagents only when they reduce evidence ambiguity.
9. Return exactly one JSON object matching
   `schemas/mergeproof_report.schema.json`.

Do not read files outside the opened workspace.
Do not write or modify repository files.
Do not invent missing product requirements or report metadata.
