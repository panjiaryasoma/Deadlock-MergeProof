# Block 4 IBM Bob E2E Runbook

This run is the final runtime evidence for Block 4. GitHub Actions cannot replace
it because CI does not execute IBM Bob.

## Prepare

From the repository root:

```bash
git pull
uv sync --locked --dev
uv run python scripts/prepare_demo_workspace.py
```

Open `build/demo-workspace` in IBM Bob.

## Execute

1. Activate the `MergeProof` custom mode.
2. Invoke the `mergeproof` skill.
3. Follow `demo/BOB_RUN.md`.
4. Capture Bob's complete final JSON response exactly as emitted.

Do not expose evaluator fixtures or expected-output files to the Bob workspace.

## Validate outside verification mode

Save the captured JSON as:

`reports/block4-bob-report.json`

Then run:

```bash
uv run mergeproof reports/block4-bob-report.json
```

Block 4 runtime ACC requires:
- Bob completes the isolated workflow;
- final output is one JSON object;
- deterministic validator exits `0`;
- report run ID, commit SHA, changed files, and generated timestamp match the run context;
- no autonomous merge/approve/reject action occurs.

Only after deterministic validation should evaluator-side expected results be compared.
