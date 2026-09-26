# Source Schema

## Purpose

Source quality is part of the product. MergeProof must know *what* it is reading before deciding *what it means*.

## Required fields

```yaml
source_id: SRC-PROJECT-001
source_type: PRD
location: docs/PRD.md
version: "1.2"
effective_at: "2026-09-25"
authority: product_contract
state: ACTIVE
supersedes:
  - SRC-PROJECT-000
scope:
  - submission_deadline
content_hash: "sha256:..."
```

## `source_type`

- `MACHINE_READABLE_CONTRACT`
- `CHANGE_ACCEPTANCE_CRITERIA`
- `ADR`
- `PRD`
- `REPOSITORY_DOCUMENTATION`
- `ISSUE_OR_PR_TEXT`
- `EXTERNAL_GUIDANCE`

## `state`

- `ACTIVE`
- `SUPERSEDED`
- `CONFLICTING`
- `UNKNOWN`

## Authority rules

Authority is **project-specific**. A file is not authoritative merely because it has "PRD" in the filename.

Explicit supersession wins.

When project metadata is absent, the fallback precedence in `domain_rules_v1.0.yaml` is used only as a conservative heuristic.

## Evidence anchor format

```yaml
artifact: docs/PRD.md
locator: "REQ-DL-004 / lines 88-95"
excerpt: "evaluated_at >= submission_deadline ..."
commit_sha: "optional"
```

## Important distinction

External guidance (OWASP, Google, vendor docs) can justify a `POTENTIAL_RISK`.

It cannot silently manufacture a project requirement and then accuse the implementation of violating it.
