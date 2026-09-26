# Product Requirements Document — MergeProof v0.1

## 0. Status

- Team: Deadlock
- Product name: MergeProof (working)
- Release target: Hackathon MVP
- Authority: this PRD defines product behavior unless superseded by an explicit addendum.
- Merge authority: human only.

---

## 1. Product summary

MergeProof is a **Bob-native pre-merge evidence workflow**.

It receives:
- current source artifacts,
- repository state,
- tests,
- and a change scope,

then asks IBM Bob to gather evidence across those artifacts and returns a structured report identifying whether the change is aligned, risky, ambiguous, or clean.

The product is not a general bug detector. Its primary question is:

> **Does this change remain consistent with the latest authoritative source artifacts, and is that consistency supported by tests/evidence?**

---

## 2. Primary user journey

1. Maintainer opens a repository in Bob.
2. Maintainer activates `mergeproof` mode / skill.
3. Maintainer points MergeProof at the current change (diff/branch/files).
4. MergeProof identifies authoritative source artifacts.
5. MergeProof extracts/normalizes atomic requirements.
6. Focused analysis maps requirements to changed implementation and relevant tests.
7. Findings are emitted with exact evidence anchors.
8. Deterministic validator rejects malformed/unsupported findings.
9. Aggregate advisory is produced:
   - PASS
   - REVIEW_REQUIRED
   - ABSTAIN
10. Human reviewer makes the merge decision.

---

## 3. Personas

### P1 — Maintainer / reviewer
Needs a compact, evidence-backed pre-merge view without re-reading the entire repository.

### P2 — Engineer authoring the change
Needs actionable evidence on exactly which requirement/test boundary may be broken.

### P3 — QA / test engineer
Needs to know which requirement has no corresponding acceptance test or changed boundary.

---

## 4. Functional requirements

### FR-001 — Source registration
The system MUST register every source artifact with:
- unique source ID;
- type;
- path/URI;
- version or commit when available;
- effective date when available;
- authority class;
- supersession relationship;
- scope.

### FR-002 — Source precedence
The system MUST resolve explicit supersession first.
If no explicit supersession exists, deterministic precedence rules apply.
Conflicting high-authority sources MUST produce `ABSTAIN`.

### FR-003 — Requirement extraction
The workflow MUST represent requirements as atomic statements with stable requirement IDs.

### FR-004 — Change scoping
The user MUST be able to provide:
- git diff / branch diff; or
- explicit list of changed files.

### FR-005 — Evidence anchors
Every non-clean finding MUST include:
- source anchor;
- implementation or test anchor;
- a short evidence statement.

### FR-006 — Finding classes
Allowed finding classes:
- `CONFIRMED_ISSUE`
- `POTENTIAL_RISK`
- `SPEC_AMBIGUITY`
- `NO_ISSUE`

No other class is valid in MVP.

### FR-007 — Finding types
MVP MUST support:
- `REQUIREMENT_IMPLEMENTATION_MISMATCH`
- `API_CONTRACT_DRIFT`
- `BOUNDARY_CONDITION_DRIFT`
- `ENUM_OR_SCHEMA_DRIFT`
- `MISSING_ACCEPTANCE_TEST`
- `SOURCE_CONFLICT`
- `STALE_SOURCE`
- `UNSUPPORTED_BEST_PRACTICE_CLAIM`
- `HARMLESS_REFACTOR`

### FR-008 — Severity rubric
Severity MUST be derived from deterministic rules using:
- requirement criticality;
- scope of impact;
- backward compatibility;
- availability of mitigating tests;
- evidence strength.

Bob MAY propose severity evidence, but the final severity field MUST conform to the rubric.

### FR-009 — Abstention
The system MUST output `ABSTAIN` when:
- authoritative sources conflict;
- source authority cannot be determined;
- evidence anchors are missing;
- requirement wording is materially ambiguous.

### FR-010 — Human authority
The system MUST NOT:
- merge;
- approve;
- reject;
- push;
- commit;
- edit source code as part of the verification workflow.

### FR-011 — Read-only default
The MergeProof Bob mode MUST default to read-only analysis tools where possible.

### FR-012 — Subagent decomposition
Independent tasks MAY be delegated to focused Bob subagents, e.g.:
- source/requirements pass;
- implementation pass;
- test coverage pass.

Subagent results MUST be summarized back into the main evidence report.

### FR-013 — Machine-readable report
The workflow MUST output a report conforming to the frozen finding/report schema.

### FR-014 — Human-readable summary
The workflow MUST output a Markdown summary containing:
- overall advisory;
- confirmed issues;
- potential risks;
- ambiguities;
- clean/verified items;
- sources inspected;
- tests inspected;
- unresolved questions.

### FR-015 — Deterministic validator
A local script MUST validate:
- report schema;
- allowed enums;
- evidence completeness;
- source IDs;
- impossible combinations.

### FR-016 — Reproducibility record
Each run MUST record:
- repository commit SHA if available;
- changed-file scope;
- source IDs;
- Bob mode/skill version;
- timestamp;
- report schema version.

---

## 5. Non-functional requirements

### NFR-001 — Explainability
A reviewer must be able to inspect the evidence without relying on hidden chain-of-thought.

### NFR-002 — Fail closed on ambiguity
Ambiguity becomes `ABSTAIN`, not confident prose.

### NFR-003 — No fake probability
MVP MUST NOT output fabricated numerical "confidence %" from the LLM.
Confidence is represented by evidence grade:
- DIRECT
- CORROBORATED
- INFERRED
- INSUFFICIENT

### NFR-004 — Minimal dependency surface
The deterministic validator should prefer Python standard library or a very small declared dependency set.

### NFR-005 — Repository portability
The workflow configuration MUST live inside the repository and be version-controllable.

### NFR-006 — Demo time
A complete demonstration on the seeded sample repository should finish within 5 minutes.

---

## 6. Bob-native architecture

```text
.bob/custom_modes.yaml
        |
        v
mergeproof custom mode
        |
        +--> .bob/rules-mergeproof/*
        |
        +--> .bob/skills/mergeproof/SKILL.md
                    |
                    +--> evidence checklist
                    +--> severity rubric
                    +--> report template
                    +--> validator script reference
        |
        v
focused Bob analysis/subagents
        |
        v
reports/mergeproof-report.json
        |
        v
scripts/validate_report.py
        |
        +--> PASS / INVALID REPORT
        |
        v
reports/mergeproof-summary.md
```

---

## 7. MVP user stories

### US-001
As a reviewer, I want to see requirement-to-code mismatches so I can focus review attention.

Done when:
- mismatch cites exact requirement;
- mismatch cites exact code location;
- validator accepts the finding structure.

### US-002
As a reviewer, I want missing boundary tests identified without generic lint noise.

Done when:
- relevant requirement/code boundary is shown;
- exact missing scenario is described;
- no finding is raised when the requirement is silent and the claim is only stylistic.

### US-003
As a reviewer, I want stale/conflicting source artifacts called out before conclusions are drawn.

Done when:
- conflict is explicit;
- aggregate advisory is ABSTAIN;
- no source is silently selected by the LLM.

### US-004
As a maintainer, I want clean refactors to pass without false alarms.

Done when:
- clean fixture yields PASS;
- no unsupported high-severity finding appears.

### US-005
As a team, we want the workflow versioned with the repo.

Done when:
- mode/skill/rules are project-local;
- run metadata includes versions.

---

## 8. Evaluation targets

Hard acceptance:
- 8/8 triage fixtures meet expected advisory.
- 100% confirmed issues contain valid evidence anchors.
- 0 autonomous merge/approval actions.
- 0 unsupported finding classes.
- 0 source conflicts silently resolved.

Target metrics for broader evaluation:
- confirmed-finding precision >= 0.90;
- seeded-defect recall >= 0.85;
- clean-case pass rate >= 0.90;
- critical miss rate = 0 on frozen critical fixtures;
- unsupported-finding rate <= 0.05;
- source-anchor validity >= 0.95.

Time-reduction is measured but not used as a hard gate unless a manual baseline has actually been collected.

---

## 9. Explicit non-goals

- replace human review;
- replace SAST/security tools;
- replace Pact/OpenAPI contract tests;
- guarantee absence of bugs;
- infer business requirements that were never documented;
- auto-fix production code in MVP;
- integrate with GitHub API in MVP.

---

## 10. Demo story

The seeded demo contains a requirement:

> A submission is expired when `evaluated_at >= submission_deadline`.

The implementation intentionally uses:

```python
evaluated_at > submission_deadline
```

and the tests omit equality.

MergeProof must:
1. identify the source requirement;
2. identify the operator drift;
3. identify the missing equality test;
4. classify it as confirmed boundary-condition drift;
5. produce `REVIEW_REQUIRED`;
6. show exact evidence;
7. leave the final merge decision to the human reviewer.

---

## 11. MVP release gate

Do not add UI or GitHub integration until:
- custom mode loads;
- skill loads;
- first end-to-end report validates;
- TRIAGE-001 through TRIAGE-008 pass.
