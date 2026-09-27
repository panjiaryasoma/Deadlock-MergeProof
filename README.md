# MergeProof

**Team:** Deadlock  
**Hackathon:** IBM Bob 2.0  
**Status:** MVP  
**MergeProof skill:** `v1.0.3`

MergeProof is a **Bob-native, read-only pre-merge verification workflow** for checking
whether a proposed software change is still supported by the repository's actual
requirements, contracts, acceptance criteria, implementation, and tests.

Instead of asking an AI reviewer to "find bugs" in the abstract, MergeProof forces the
review through an evidence pipeline:

```text
source authority
    ↓
requirement trace
    ↓
implementation observation
    ↓
test / acceptance audit
    ↓
evidence classification
    ↓
severity + abstention
    ↓
canonical JSON report
```

The final advisory is one of:

- `PASS`
- `REVIEW_REQUIRED`
- `ABSTAIN`

**A human reviewer always retains merge authority.** MergeProof never merges, approves,
rejects, pushes, or edits production code.

## Why MergeProof

Pre-merge AI review becomes unreliable when requirements disagree, old documentation is
still present, tests miss a boundary, or generic best-practice advice is mistaken for a
project requirement.

MergeProof is designed around those failure modes.

It explicitly separates:

- authoritative vs. merely active sources;
- current vs. superseded requirements;
- documented behavior vs. observed implementation;
- project requirements vs. external best practice;
- confirmed issues vs. potential risks vs. ambiguity;
- review evidence vs. the final human merge decision.

When the evidence cannot support a reliable conclusion, MergeProof is expected to
`ABSTAIN` rather than invent a product decision.

## Bob-native workflow

The repository includes a dedicated IBM Bob mode and composable skills under `.bob/`.

The MergeProof mode is intentionally **read-only**.

Expected permissions:

- Read
- Skill
- Subagent

Intentionally absent:

- Edit
- Execute
- MCP

The workflow uses focused skills for source authority, requirement tracing,
implementation observation, test auditing, evidence classification, severity,
conflict/abstention, self-audit, and final report synthesis.

Successful verification output is a **single canonical JSON object** conforming to:

```text
schemas/mergeproof_report.schema.json
```

No autonomous merge decision is encoded in the report.

## Evidence model

Finding classes:

```text
CONFIRMED_ISSUE
POTENTIAL_RISK
SPEC_AMBIGUITY
NO_ISSUE
```

Evidence grades:

```text
DIRECT
CORROBORATED
INFERRED
INSUFFICIENT
```

Examples of supported finding types include:

```text
BOUNDARY_CONDITION_DRIFT
API_CONTRACT_DRIFT
MISSING_ACCEPTANCE_TEST
SOURCE_CONFLICT
STALE_SOURCE
UNSUPPORTED_BEST_PRACTICE_CLAIM
HARMLESS_REFACTOR
REQUIREMENT_IMPLEMENTATION_MISMATCH
```

Severity and advisory decisions are constrained by deterministic project rules in:

```text
docs/03_EVALUATION_AND_DOMAIN_RULES/domain_rules_v1.0.yaml
```

The advisory precedence is:

```text
ABSTAIN > REVIEW_REQUIRED > PASS
```

## Frozen TRIAGE evaluation suite

MergeProof ships with eight frozen acceptance scenarios.

| ID | Scenario | Expected result |
| --- | --- | --- |
| TRIAGE-001 | Deadline equality drift | `CONFIRMED_ISSUE / BOUNDARY_CONDITION_DRIFT / HIGH / REVIEW_REQUIRED` |
| TRIAGE-002 | API required-field drift | `CONFIRMED_ISSUE / API_CONTRACT_DRIFT / HIGH / REVIEW_REQUIRED` |
| TRIAGE-003 | Clean internal refactor | `NO_ISSUE / HARMLESS_REFACTOR / NONE / PASS` |
| TRIAGE-004 | Material requirement ambiguity | `SPEC_AMBIGUITY / REQUIREMENT_IMPLEMENTATION_MISMATCH / NONE / ABSTAIN` |
| TRIAGE-005 | Missing acceptance test | `CONFIRMED_ISSUE / MISSING_ACCEPTANCE_TEST / MEDIUM / REVIEW_REQUIRED` |
| TRIAGE-006 | Conflicting active sources | `SPEC_AMBIGUITY / SOURCE_CONFLICT / NONE / ABSTAIN` |
| TRIAGE-007 | External best-practice-only concern | `POTENTIAL_RISK / UNSUPPORTED_BEST_PRACTICE_CLAIM / MEDIUM / REVIEW_REQUIRED` |
| TRIAGE-008 | Superseded requirement | `NO_ISSUE / STALE_SOURCE / NONE / PASS` |

The evaluator ground truth is intentionally excluded from isolated Bob workspaces.

## Quick start

Requirements:

- Python 3.12+
- `uv`

Install and verify:

```bash
uv sync --locked --dev
uv run pytest -q
uv run ruff check src tests scripts demo
```

Run the CLI:

```bash
uv run mergeproof --help
```

## Seeded demo

The demo under `demo/` contains:

- an active submission-deadline requirement;
- a scoped implementation;
- a runnable test suite;
- an explicit changed-file set.

Run it:

```bash
uv run python -m demo.app
uv run python -m unittest discover -s demo/tests -t . -v
```

Prepare an isolated Bob workspace:

```bash
uv run python scripts/prepare_demo_workspace.py
```

Then open:

```text
build/demo-workspace
```

in IBM Bob instead of opening the repository root.

## TRIAGE reproduction

Prepare all isolated evaluation workspaces:

```bash
uv run python scripts/prepare_triage_workspace.py --all
```

Or prepare one case:

```bash
uv run python scripts/prepare_triage_workspace.py --case TRIAGE-004
```

Open the generated case directory in Bob, select the **MergeProof** mode, then use:

```text
Use the mergeproof orchestrator skill. Perform the verification workflow for the current isolated workspace using MERGEPROOF_RUN_CONTEXT.yaml and return exactly the canonical JSON report.
```

Validate a captured report deterministically:

```bash
uv run python scripts/evaluate_triage_report.py \
  --case TRIAGE-004 \
  --report reports/triage/TRIAGE-004.json
```

Run the aggregate acceptance harness:

```bash
uv run python scripts/run_triage_acceptance.py
```

## Repository layout

```text
.
├── .bob/
│   ├── custom_modes.yaml
│   ├── rules-mergeproof/
│   └── skills/
├── demo/                         # seeded demonstration case
├── docs/                         # contracts, rules, evaluation design
├── eval/
│   ├── fixtures/                 # TRIAGE input cases
│   └── expected/                 # frozen evaluator ground truth
├── reports/
│   ├── diagnostic/               # preserved failed/diagnostic runs
│   └── triage/                   # accepted captured Bob reports
├── schemas/                      # canonical JSON schema
├── scripts/                      # workspace + evaluation tooling
├── src/mergeproof/               # models, validation, CLI, evaluator
└── tests/                        # deterministic regression tests
```

## Design boundaries

MergeProof deliberately does **not**:

- infer product decisions that are absent from repository evidence;
- promote external best practice into a local requirement;
- hide unresolved source conflicts;
- invent numeric confidence scores;
- autonomously approve, reject, or merge changes.

Its job is narrower: produce a traceable evidence report that makes the human review
decision easier to defend.
