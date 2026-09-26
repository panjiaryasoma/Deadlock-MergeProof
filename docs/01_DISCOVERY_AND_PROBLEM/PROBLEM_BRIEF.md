# Problem Brief — MergeProof

## 1. Problem

Before merging a change, reviewers often have to answer several different questions manually:

1. What did the current source of truth actually require?
2. Which parts of the implementation changed?
3. Does the implementation still satisfy the requirement or API contract?
4. Are the relevant acceptance and boundary cases represented in tests?
5. Is a flagged issue truly a contract violation, merely a best-practice concern, or just ambiguity in the source material?

These checks are usually fragmented across PR descriptions, PRDs, OpenAPI/schema files, ADRs, issue acceptance criteria, code, and tests.

The core problem is **evidence fragmentation**, not lack of another generic code-review opinion.

## 2. Target user

Primary:
- software engineer reviewing a PR/change;
- tech lead or maintainer responsible for merge approval.

Secondary:
- QA/test engineer;
- API/platform maintainer;
- small teams without dedicated release engineering.

## 3. Job to be done

> Before I merge a change, help me verify that the implementation still matches the latest authoritative requirements/contracts and that the important acceptance boundaries are tested, with evidence I can inspect.

## 4. Current failure modes

- reviewer checks code but never re-opens the requirement;
- requirement changed but an older document is still treated as authoritative;
- API field/type/status semantics drift from the documented contract;
- a boundary operator or negation changes (`<` vs `<=`, `required` vs optional);
- test suite passes but never exercises the changed boundary;
- an AI reviewer reports generic "best practices" as if they were requirements;
- an AI finding contains no exact source/code/test evidence;
- conflicting source artifacts exist and the reviewer is not warned.

## 5. Product hypothesis

A Bob-native workflow can reduce manual cross-checking by:
- reading source documents and repository context;
- decomposing independent evidence checks through focused subagents;
- requiring exact source/code/test anchors;
- applying deterministic domain rules to findings;
- abstaining when the source of truth is ambiguous.

## 6. Why now / hackathon fit

The hackathon asks for a developer workflow improved through IBM Bob. MergeProof uses Bob for:
- document/repository understanding;
- focused multi-step analysis;
- subagent evidence gathering;
- synthesis into a structured review artifact.

The deterministic validation layer exists specifically to stop the LLM from silently upgrading weak evidence into a confident verdict.

## 7. MVP scope

### In scope
- one repository at a time;
- Markdown/YAML/JSON/OpenAPI-like source artifacts;
- Git diff or explicit changed-file scope;
- requirement-to-code/test trace links;
- 4 finding classes;
- evidence strength and source precedence;
- PASS / REVIEW_REQUIRED / ABSTAIN advisory;
- Bob custom mode + skill;
- 8 acceptance fixtures + evaluation corpus;
- machine-readable JSON/YAML report plus Markdown summary.

### Out of scope
- autonomous merge/approval;
- GitHub App installation;
- webhook/polling infrastructure;
- organization-wide knowledge base;
- automatic PR commenting;
- semantic code parsing for every language;
- model training/fine-tuning;
- production security scanner replacement.

## 8. Success criteria

MVP is considered successful if:
1. all 8 frozen triage fixtures return expected advisory behavior;
2. unsupported findings are rejected by report validation;
3. clean/no-op cases do not become false blockers;
4. ambiguous or conflicting source cases abstain;
5. every confirmed finding has at least one source anchor and one code/test anchor;
6. a reviewer can understand *why* a finding exists without reading Bob's hidden reasoning;
7. the workflow can be demonstrated end-to-end in a small repository inside the hackathon timebox.

## 9. Key product boundary

**Evidence before confidence. Human before authority.**

MergeProof may recommend `REVIEW_REQUIRED`; it does not own merge authority.
