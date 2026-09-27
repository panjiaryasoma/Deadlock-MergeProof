---
name: source-authority
description: Inventory project sources and resolve lifecycle state, supersession, scope, and authority without inventing precedence.
---

# Source Authority

For each relevant source capture the canonical source facts:

- `source_id`
- `source_type`
- workspace-root-relative `location`
- declared `authority` string
- declared lifecycle `state`
- declared `scope`
- version/date, supersession, and content hash when present

Resolution order:

1. explicit supersession;
2. repository-defined governance;
3. source scope/applicability;
4. unresolved if still conflicting.

Never choose a source merely because it is newer, an ADR, machine-readable,
or more formal unless project governance explicitly says so.

## Important separation

The report field `source.authority` preserves the repository-declared authority
value exactly, for example `product_contract`.

Internal authority resolution may classify a source as:
- AUTHORITATIVE;
- NON_AUTHORITATIVE;
- UNRESOLVED.

That internal resolution state is analysis metadata only. Do not replace the
canonical report's project-specific `authority` string with those labels.
