# Implementation Handoff Plan v1.0

## Block 1 — Bob-native shell
Create:
- `.bob/custom_modes.yaml`
- `.bob/rules-mergeproof/`
- `.bob/skills/mergeproof/SKILL.md`

Acceptance:
- custom mode visible in Bob;
- read tools available;
- application-code edit tools unavailable in verification mode;
- skill auto/manual activation works.

## Block 2 — Report contract + validator
Create:
- `schemas/mergeproof_report.schema.json` or equivalent frozen Pydantic/dataclass validation;
- `scripts/validate_report.py`.

Acceptance:
- valid example passes;
- confirmed issue without anchors fails;
- invalid enum fails;
- NO_ISSUE + HIGH severity fails.

## Block 3 — Seeded demo repo
Create minimal domain with:
- active requirement;
- changed implementation;
- test suite;
- one intentional boundary drift.

Acceptance:
- app/tests runnable;
- ground truth hidden from Bob-visible analysis.

## Block 4 — Evidence workflow
Teach skill to:
1. resolve sources;
2. extract requirements;
3. inspect change;
4. inspect tests;
5. optionally delegate focused exploration;
6. emit report only in frozen schema.

## Block 5 — Triage acceptance
Run TRIAGE-001..008.
Do not polish UI before the suite is acceptable.

## Block 6 — Evaluation
Run broader evaluation matrix.
Calculate actual metrics only from observed results.

## Block 7 — Demo polish
Optional:
- static HTML summary;
- concise README;
- diagram.

## Block 8 — Submission
- public GitHub;
- product description;
- <=5 minute presentation;
- Bob usage/session evidence required by event workflow;
- final reproducibility instructions.
