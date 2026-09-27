# Block 5 TRIAGE Acceptance Runbook

Block 5 uses TRIAGE-001 through TRIAGE-008 with the pre-measurement consistency
corrections documented in
`docs/05_PREPRODUCTION/02_TRIAGE_ACCEPTANCE/FIXTURE_CONSISTENCY_CORRECTIONS.md`.

## 1. Prepare all isolated workspaces

```bash
git pull
uv sync --locked --dev
uv run python scripts/prepare_triage_workspace.py --all
```

This creates:

```text
build/triage/TRIAGE-001
...
build/triage/TRIAGE-008
```

Each workspace contains only:
- MergeProof Bob configuration;
- the selected analysis fixture;
- its canonical source registry;
- optional change evidence when the scenario requires it;
- active domain/schema/output contracts;
- per-run provenance.

Evaluator ground truth under `eval/expected/` is not copied.

## 2. Execute IBM Bob once per case

For each case:

1. Open `build/triage/<CASE_ID>` in IBM Bob.
2. Activate the `MergeProof` mode.
3. Invoke the `mergeproof` skill.
4. Capture the final JSON exactly as emitted.
5. Save it outside Bob verification mode as `reports/triage/<CASE_ID>.json`.

Do not inspect `eval/expected/<CASE_ID>.yaml` until that case's Bob response has
already been captured.

## 3. Evaluate one case

```bash
uv run python scripts/evaluate_triage_report.py \
  --case TRIAGE-001 \
  --report reports/triage/TRIAGE-001.json
```

The evaluator checks:
- Block 2 structural and semantic validity;
- run provenance;
- exact registered source-ID set;
- source type/state/authority/scope/supersession/location against the source registry;
- expected advisory;
- frozen expected finding class/type/severity tuple;
- source anchors point to registered source locations;
- repository anchors stay in evaluated changed-file scope;
- anchor locators resolve against their artifacts;
- source-conflict findings cite both active sides;
- cited artifacts exist inside the isolated workspace.

## 4. Evaluate all eight

After all reports are captured:

```bash
uv run python scripts/run_triage_acceptance.py
```

Block 5 final acceptance requires:

```text
passed=8 failed=0 pending=0 total=8
```

GitHub Actions verifies the corpus, preparation tooling, and deterministic evaluator.
It does not execute IBM Bob, so CI success alone is not an 8/8 TRIAGE result.
