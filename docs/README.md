# MergeProof Preproduction Pack

**Team:** Deadlock  
**Working product name:** MergeProof *(provisional; naming is intentionally non-blocking)*  
**Prepared:** 2026-09-26  
**Hackathon context:** IBM Bob 2.0 Hackathon  
**Core workflow:** Code Review + Testing, with maintenance/release support as secondary context.

## One-line product definition

MergeProof is a **Bob-native pre-merge evidence workflow** that checks whether a proposed code change still aligns with the repository's requirements, contracts, acceptance criteria, and tests, then returns a structured evidence report for **human merge review**.

## Why Bob-native instead of "yet another AI dashboard"

The MVP is designed around Bob capabilities that are actually shareable with a repository:

- project-level custom mode;
- reusable skill and supporting files;
- read-only / controlled tool permissions;
- repository context via AGENTS.md;
- focused subagents for independent evidence gathering;
- deterministic report/schema validation outside the LLM.

The product is therefore a developer workflow package first. A web dashboard is explicitly **not required for MVP**.

## Canonical MVP flow

```text
Change / PR diff
    +
Current source artifacts
(PRD, contract, acceptance criteria, ADRs)
    +
Repository + tests
        |
        v
Bob: MergeProof custom mode
  |- source/provenance pass
  |- requirements extraction
  |- implementation alignment
  |- test/acceptance coverage
  |- focused subagent checks
        |
        v
Structured findings
  CONFIRMED_ISSUE
  POTENTIAL_RISK
  SPEC_AMBIGUITY
  NO_ISSUE
        |
        v
Deterministic schema/rule validation
        |
        v
PASS / REVIEW_REQUIRED / ABSTAIN
        |
        v
HUMAN decides merge
```

## Non-negotiable boundary

MergeProof **never merges, blocks, edits, or approves a PR on its own**. It provides evidence and an advisory verdict only.

## Folder map

1. `01_DISCOVERY_AND_PROBLEM` — problem framing, real-world evidence, and discovery review.
2. `02_PRODUCT_REQUIREMENTS` — PRD and alignment review.
3. `03_EVALUATION_AND_DOMAIN_RULES` — rules, schemas, matrix, source-evidence tests, validation.
4. `04_DATA_STRATEGY` — evaluation corpus strategy. **No ML training dataset is required for MVP.**
5. `05_PREPRODUCTION` — frozen contracts, triage fixtures, integration fixture, closure audit.
6. `06_IMPLEMENTATION_HANDOFF` — exact production order, cut-scope, test/eval plan, readiness gate.

## Current gate

**PREPRODUCTION DESIGN: READY FOR IMPLEMENTATION, WITH RUNTIME VALIDATION PENDING.**

The design is internally consistent. The first implementation task must validate that the project-level Bob custom mode and skill load correctly in the installed Bob version before any optional UI work.
