# MergeProof

**Team:** Deadlock  
**Status:** IBM Bob 2.0 Hackathon MVP

MergeProof is a Bob-native pre-merge evidence workflow. It checks whether a proposed
software change still aligns with active requirements, contracts, acceptance criteria,
implementation, and tests.

Final advisories:
- `PASS`
- `REVIEW_REQUIRED`
- `ABSTAIN`

Human reviewers retain merge authority.

## Layout

```text
.
├── .bob/
│   ├── custom_modes.yaml
│   ├── rules-mergeproof/
│   └── skills/
├── src/mergeproof/
├── tests/
├── eval/
├── demo/
├── reports/
├── schemas/
├── scripts/
└── docs/
```

## Local verification

```bash
uv sync --locked --dev
uv run pytest -q
uv run ruff check src tests scripts demo
```

## Seeded demo

The Block 3 demo lives under `demo/` and contains:
- one active submission-deadline requirement;
- the current implementation;
- a small runnable test suite;
- an explicit changed-file scope.

Run the sample application:

```bash
uv run python -m demo.app
```

Run the application tests directly:

```bash
uv run python -m unittest discover -s demo/tests -t . -v
```

### Isolated Bob run

Measured Bob analysis must not expose evaluator ground truth. Build a restricted
workspace first:

```bash
uv run python scripts/prepare_demo_workspace.py
```

Then open `build/demo-workspace` in Bob rather than the repository root. The generated
workspace contains the Bob configuration, demo artifacts, domain rules, and canonical
report contract, while evaluation expectations and frozen acceptance fixtures remain
outside the analysis-visible tree.

## Verification mode

The `MergeProof` Bob mode is intentionally read-only.

Expected permissions:
- Read
- Skill
- Subagent

Intentionally absent:
- Edit
- Execute
- MCP

Do not broaden verification permissions merely to make a demo convenient.
