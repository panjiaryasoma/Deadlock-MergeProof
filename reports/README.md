# Reports

Generated reports are local runtime artifacts.

The MergeProof Bob mode is read-only. Persisting a conversational report must be
a separate explicitly authorized write step.

For Block 5, store captured IBM Bob reports locally as:

```text
reports/triage/TRIAGE-001.json
...
reports/triage/TRIAGE-008.json
```

Then run `uv run python scripts/run_triage_acceptance.py`.
