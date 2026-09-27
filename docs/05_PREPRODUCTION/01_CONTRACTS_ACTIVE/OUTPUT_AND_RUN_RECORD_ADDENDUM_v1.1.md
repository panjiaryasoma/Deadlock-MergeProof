# Output & Run Record Addendum — MergeProof v1.1

## Status

- Status: ACTIVE
- Effective scope: Hackathon MVP from Block 4 onward
- Authority: explicit addendum under the supersession clause in SIMPLE_PRD.md
- Supersedes: SIMPLE_PRD FR-014 and BASELINE_CONTRACT output sequencing only as described below

## Output-stage sequencing

For Blocks 4 through 6, the IBM Bob verification workflow MUST emit exactly one
machine-readable report conforming to the frozen report schema.

The Bob verification response MUST NOT append a Markdown summary. The report is
validated first by the deterministic Block 2 validator.

FR-014 remains an MVP release requirement. In Block 7, a Markdown summary MUST be
derived from the deterministically accepted report. That summary MUST contain the
same conclusion set and MUST NOT introduce additional findings, severities,
advisories, or hidden evidence.

This addendum does not change FR-013, the allowed advisory values, evidence rules,
or human merge authority.

## FR-016 reproducibility record

MERGEPROOF_RUN_CONTEXT.yaml is the authoritative per-run reproducibility record
for the seeded measured workflow.

It MUST record:
- run_id
- repository_commit_sha
- changed_files
- source_ids
- bob_mode_version
- skill_version
- timestamp
- report_schema_version

It also records workspace-local paths to the case descriptor, report schema,
domain rules, and this addendum.

The canonical report keeps its frozen fields. FR-016 does not require inventing
new report fields when the run context already records the metadata
deterministically.

## Fail-closed behavior

Canonical report synthesis is attempted only when every required provenance value
is grounded.

If run-context provenance is incomplete, the orchestrator MUST stop before
report-synthesis and surface a workflow setup error. It MUST NOT fabricate a
schema-valid report or invent an INCOMPLETE advisory.
