# Scripts

Deterministic Block 2 tooling.

Validate a report through the single CLI implementation:

```bash
uv run mergeproof reports/example.json
```

Equivalent thin wrapper:

```bash
uv run python scripts/validate_report.py reports/example.json
```

Exit codes:
- `0`: valid report;
- `1`: structurally or semantically invalid report;
- `2`: invocation, input, or JSON parse failure.

Regenerate the checked-in JSON Schema artifact:

```bash
uv run python scripts/generate_schema.py
```
