# Workflow Map

```text
MERGEPROOF_RUN_CONTEXT.yaml
          |
          v
     case descriptor
   / source_files     \
 changed_files        |
          |           |
          +-----+-----+
                |
                v
        source-authority
                |
                v
       requirement-trace
                |
        +-------+-------+
        |               |
        v               v
implementation      test-acceptance
 observation            audit
        |               |
        +-------+-------+
                |
                v
     evidence-classification
                |
                v
        severity-impact
                |
                v
      conflict-abstention
      preliminary advisory
                |
                v
           self-audit
                |
                v
 material correction or
    new uncertainty?
        /         \
      YES          NO
       |            |
       v            |
 conflict-abstention|
   reconciliation   |
       |            |
       +------+-----+
              |
              v
      report-synthesis
              |
              v
 canonical JSON report only
```

## Architectural invariants

- Source authority is resolved before expected behavior is asserted.
- Requirement evidence and observed implementation remain separate until classification.
- Independent read-only exploration may be delegated, but final reconciliation stays in
  the orchestrator.
- `conflict-abstention` is the only advisory decision point.
- `report-synthesis` uses the latest advisory state and emits only the canonical JSON report.
