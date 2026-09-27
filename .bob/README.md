# MergeProof Bob Configuration

Mode: `MergeProof`

Tool groups:
- `read`
- `skill`
- `subagent`

No edit/execute/MCP tools are exposed.

Project skills:
- mergeproof
- source-authority
- requirement-trace
- implementation-observation
- test-acceptance-audit
- evidence-classification
- severity-impact
- conflict-abstention
- self-audit
- report-synthesis

## Evidence workflow

The orchestrator consumes explicit run context and case scope, resolves source authority,
extracts requirements, inspects changed implementation and tests, optionally delegates
independent read-only exploration, reconciles findings, and emits exactly one canonical
JSON report.

The final report contract is `schemas/mergeproof_report.schema.json`.
