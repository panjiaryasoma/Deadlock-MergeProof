# Seeded Demo Workspace

This directory is the analysis-visible application fixture for the first MergeProof end-to-end run.
It contains an active product requirement, the current implementation, the relevant tests, and the
explicit changed-file scope. It intentionally does not contain evaluator labels or expected output.

## Run the application

From the repository root:

```bash
uv run python -m demo.app
```

## Run the demo tests

```bash
uv run python -m unittest discover -s demo/tests -t . -v
```

## Prepare the isolated Bob workspace

For a measured Bob run, do not open the repository root. Build the analysis-only workspace and open
that generated directory in Bob instead:

```bash
uv run python scripts/prepare_demo_workspace.py
```

Default output: `build/demo-workspace`.

The generated workspace includes the Bob configuration, the demo fixture, the domain rules, and the
canonical report contract. Evaluation expectations and preproduction acceptance fixtures are not
copied into it.
