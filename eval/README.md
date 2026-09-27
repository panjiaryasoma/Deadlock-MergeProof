# Evaluation

The frozen eight-case TRIAGE corpus lives in:

- `eval/fixtures/TRIAGE-001` through `TRIAGE-008` for analysis-visible artifacts;
- `eval/expected/TRIAGE-001.yaml` through `TRIAGE-008.yaml` for evaluator-only ground truth.

Expected outputs are copied from the frozen preproduction TRIAGE suite and are never
placed in the IBM Bob analysis workspace.

Prepare isolated workspaces with:

```bash
uv run python scripts/prepare_triage_workspace.py --all
```

Do not tune Bob prompts or skills against evaluator-side expected outputs after a run.
