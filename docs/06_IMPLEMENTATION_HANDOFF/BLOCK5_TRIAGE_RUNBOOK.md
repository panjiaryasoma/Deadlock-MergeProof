# Block 5 TRIAGE Acceptance Runbook

Block 5 uses TRIAGE-001 through TRIAGE-008 with the documented consistency
corrections.

The final measured series uses MergeProof skill version `1.0.1`.
The earlier TRIAGE-001 run under skill `1.0.0` is diagnostic-only and is documented in
`BLOCK5_MEASUREMENT_RESTART_v1.0.1.md`.

## 1. Prepare all isolated workspaces

After pulling the latest repo, regenerate all workspaces once:

```bash
git pull
uv sync --locked --dev
uv run python scripts/prepare_triage_workspace.py --all
```

Verify each generated `MERGEPROOF_RUN_CONTEXT.yaml` records:

```yaml
skill_version: "1.0.1"
```

This creates `build/triage/TRIAGE-001` through `TRIAGE-008`.

Each workspace contains only the MergeProof Bob configuration, selected analysis
fixture, canonical source registry, optional change evidence, active contracts, and
per-run provenance. Evaluator ground truth is not copied.

## 2. Execute IBM Bob once per case

For each case:

1. Open only `build/triage/<CASE_ID>` in IBM Bob.
2. Activate the `MergeProof` mode.
3. Invoke the `mergeproof` skill.
4. Capture the successful final response exactly as emitted.
5. The response must be raw JSON: first non-whitespace character `{`, last
   non-whitespace character `}`, no prose and no code fence.
6. Save it outside Bob verification mode as `reports/triage/<CASE_ID>.json`.

Do not inspect `eval/expected/<CASE_ID>.yaml` while producing the Bob response.

## 3. Evaluate one case

```bash
uv run python scripts/evaluate_triage_report.py \
  --case TRIAGE-001 \
  --report reports/triage/TRIAGE-001.json
```

The evaluator checks Block 2 validity, run provenance, exact source governance,
expected advisory and finding tuple, anchor roles/locators, conflict evidence, and
artifact existence.

## 4. Evaluate all eight

```bash
uv run python scripts/run_triage_acceptance.py
```

Final Block 5 acceptance requires:

```text
passed=8 failed=0 pending=0 total=8
```

GitHub Actions verifies the corpus, preparation tooling, and deterministic evaluator.
It does not execute IBM Bob.
