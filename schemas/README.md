# Schemas

`mergeproof_report.schema.json` is a generated artifact from
`MergeProofReport.model_json_schema()`.

The design authority remains:

`docs/05_PREPRODUCTION/01_CONTRACTS_ACTIVE/FEATURE_SCHEMA_FINAL.yaml`

The Pydantic runtime model is the executable contract. Do not hand-edit the JSON
Schema artifact. Regenerate it with:

```bash
uv run python scripts/generate_schema.py
```

The test suite fails if the checked-in artifact drifts from the runtime model.
