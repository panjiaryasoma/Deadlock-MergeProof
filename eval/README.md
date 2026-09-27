# Evaluation

The eight-case TRIAGE corpus lives in:

- `eval/fixtures/TRIAGE-001` through `TRIAGE-008` for analysis-visible artifacts;
- `eval/expected/TRIAGE-001.yaml` through `TRIAGE-008.yaml` for evaluator-only ground truth.

Each fixture contains a machine-readable `sources.yaml` registry whose metadata
must match the source records emitted by Bob.

Expected outputs are copied from the preproduction TRIAGE suite and are never placed
in the IBM Bob analysis workspace. The pre-measurement TRIAGE-006 consistency
correction is documented under
`docs/05_PREPRODUCTION/02_TRIAGE_ACCEPTANCE/FIXTURE_CONSISTENCY_CORRECTIONS.md`.

Prepare isolated workspaces with:

```bash
uv run python scripts/prepare_triage_workspace.py --all
```

Do not tune Bob prompts, rules, skills, fixtures, or expected outputs against
measured Bob results.
