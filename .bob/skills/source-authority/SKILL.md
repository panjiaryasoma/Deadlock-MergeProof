---
name: source-authority
description: Inventory project sources and resolve lifecycle state, supersession, scope, and authority without inventing precedence.
---

# Source Authority

When the case descriptor provides `source_registry`, read it before resolving
source governance.

The registry is canonical for source metadata:
- `source_id`
- `source_type`
- workspace-root-relative `location`
- declared `authority`
- declared lifecycle `state`
- declared `scope`
- declared `supersedes`

Source documents remain authoritative for their requirement/guidance statements.
If a source document materially disagrees with its registry metadata, surface the
inconsistency rather than silently choosing one representation.

Resolution order:

1. explicit supersession;
2. repository-defined governance;
3. source scope/applicability;
4. unresolved if still conflicting.

Never choose a source merely because it is newer, an ADR, machine-readable,
or more formal unless project governance explicitly says so.

Two active sources at the same precedence tier, same applicable scope, and with
no supersession/tie-breaker remain unresolved when their requirements conflict.

## Important separation

The report field `source.authority` preserves the repository-declared authority
value exactly, for example `product_contract`.

Internal authority resolution may classify a source as:
- AUTHORITATIVE;
- NON_AUTHORITATIVE;
- UNRESOLVED.

That internal resolution state is analysis metadata only. Do not replace the
canonical report's project-specific `authority` string with those labels.
