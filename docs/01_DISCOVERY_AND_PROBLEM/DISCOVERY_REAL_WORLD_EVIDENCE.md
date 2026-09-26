# Discovery — Real-World Evidence

## Purpose

This file tests whether the problem is real outside our own workflow. It deliberately separates:
- direct incidents,
- established engineering practices,
- research evidence,
- product/vendor evidence.

It does **not** claim that MergeProof would have prevented every incident below. The incidents are used to identify failure patterns, not to perform retroactive marketing.

---

## Case 1 — CrowdStrike Channel File 291 (2024)

**Observed pattern:** interface/input expectation mismatch + validation/test gap.

CrowdStrike's RCA describes a mismatch around a 21st input parameter and explains that the mismatch evaded multiple validation and testing layers. The failure later contributed to an out-of-bounds read and Windows crashes.

**What this supports**
- a change can satisfy existing tests while still violating an interface expectation;
- exact boundary/field-count tests matter;
- validation systems themselves need contract checks.

**What it does NOT prove**
- that an LLM reviewer would have caught the defect;
- that a pre-merge tool alone is sufficient for deployment safety.

Source:
https://www.crowdstrike.com/wp-content/uploads/2024/08/Channel-File-291-Incident-Root-Cause-Analysis-08.06.2024.pdf

---

## Case 2 — Knight Capital (2012)

**Observed pattern:** inconsistent deployment/change control + dormant behavior unexpectedly reactivated.

The SEC described an incorrect deployment in which new code was not consistently deployed and a defective legacy function was triggered. The event generated millions of orders and losses above $460M.

**What this supports**
- implementation/change state must be checked against intended deployment state;
- "the code exists" and "the intended system is deployed consistently" are different claims;
- review gates need explicit evidence, not assumption.

**What it does NOT prove**
- that MergeProof's MVP should solve deployment orchestration. That remains out of scope.

Source:
https://www.sec.gov/newsroom/press-releases/2013-222

---

## Case 3 — API drift as an explicit engineering problem

Swagger Contract Testing documents "API drift" as divergence between an API implementation and its specification, noting risks such as broken integrations, inaccurate documentation, and unintended breaking changes.

**What this supports**
- spec/implementation drift is a named, operationally relevant problem;
- verifying implementation against contract is a valid developer workflow category.

Source:
https://support.smartbear.com/swagger/contract-testing/docs/en/drift.html

---

## Case 4 — Contract testing exists because shared expectations break

Pact defines contract tests around shared consumer/provider expectations and explains provider contract verification as checking whether actual behavior conforms to a documented contract.

**What this supports**
- "shared expectation vs implementation" is testable;
- a good solution should generate or point to concrete tests, not only prose findings.

Source:
https://docs.pact.io/

---

## Case 5 — Stripe treats API compatibility as a first-class contract problem

Stripe's engineering documentation gives concrete examples of changing field names/types breaking dependent code and describes API review/versioning practices designed to prevent accidental compatibility breaks.

**What this supports**
- field names, types, and semantics are contract artifacts;
- seemingly local changes can have remote consumer impact;
- explicit review of API changes is valuable.

Sources:
https://stripe.com/blog/api-versioning
https://docs.stripe.com/api/versioning

---

## Case 6 — Code review is broader than syntax

Google's engineering practices describe code review as a quality process that examines design, functionality, complexity, and other properties.

**What this supports**
- pre-merge review is a legitimate workflow boundary;
- MergeProof should complement, not replace, human review.

Source:
https://google.github.io/eng-practices/review/

---

## Case 7 — Traceability helps maintenance, but maintaining links is costly

A systematic mapping study covering 63 studies reports that traceability supports maintenance/evolution activities, especially change management, while establishing/maintaining traceability links is itself a significant cost.

**What this supports**
- automating *recovery* or *checking* of trace links is useful;
- the product must avoid turning traceability into another manual bureaucracy.

Source:
https://arxiv.org/abs/2108.02133

---

## Case 8 — Requirement quality affects automated traceability

A 2026 empirical study reports that requirement-quality defects can materially affect automated traceability-link recovery and that different approaches respond differently.

**What this supports**
- source quality must be represented explicitly;
- ambiguous/poor source material should trigger `ABSTAIN`, not hallucinated certainty.

Source:
https://arxiv.org/abs/2606.11834

---

## Case 9 — Trace links are often missing or broken

A 2025 study of release artifacts reports missing and broken traceability links and evaluates LLM-assisted recovery approaches.

**What this supports**
- repository artifacts frequently lack perfect links;
- a system should support evidence recovery but still distinguish recovered links from explicit links.

Source:
https://arxiv.org/abs/2511.18187

---

## Case 10 — Runtime validation cannot be replaced by static types

OWASP guidance recommends validating input type/format/range and rejecting unexpected content.

**What this supports**
- a source requirement about runtime validation needs executable evidence;
- TypeScript compile-time typing alone does not prove runtime request validation.

Source:
https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html

---

# Discovery synthesis

The evidence supports a narrow opportunity:

> **A reviewer needs a fast, inspectable way to trace authoritative requirements/contracts into changed implementation and tests, while explicitly handling stale sources, weak evidence, and ambiguity.**

The evidence does **not** justify:
- autonomous merge authority;
- universal bug detection;
- replacing contract tests/security scanners;
- claiming every software incident is caused by "spec drift."

## Decision

**PROBLEM: ACCEPTED FOR MVP**

Reason: the problem is externally supported, maps directly to the hackathon's code-review/testing workflow, and can be evaluated with controlled seeded cases inside the remaining timebox.
