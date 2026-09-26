# Workflow Map

```text
scope
  |
  v
source-authority
  |
  v
requirement-trace
  |
  +-------------------+
  |                   |
  v                   v
implementation     test-acceptance
observation        audit
  |                   |
  +---------+---------+
            |
            v
 evidence-classification
            |
            v
 severity-impact
            |
            v
 conflict-abstention
 (preliminary advisory)
            |
            v
        self-audit
            |
            v
   material correction
   or new uncertainty?
        /         \
      YES          NO
       |            |
       v            |
 conflict-abstention|
  (reconciliation)  |
       |            |
       +------+-----+
              |
              v
      report-synthesis
              |
              v
      final advisory
```

## Architectural invariant

`conflict-abstention` is the only component allowed to decide whether unresolved
uncertainty requires `ABSTAIN`.

`self-audit` may force a reconciliation pass by changing material evidence.

`report-synthesis` must use the latest advisory state and must not recompute it.
