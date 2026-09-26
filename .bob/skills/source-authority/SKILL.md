---
name: source-authority
description: Inventory project sources and resolve lifecycle state, supersession, scope, and authority without inventing precedence.
---

# Source Authority

For each relevant source capture:
- path
- source type
- declared state
- scope
- version/date if present
- supersession links
- repository-defined authority metadata

Resolution:
1. explicit supersession
2. repository-defined governance
3. scope applicability
4. unresolved if still conflicting

Never choose a source merely because it is newer, an ADR, machine-readable,
or more formal unless project governance explicitly says so.

Output authority:
- `AUTHORITATIVE`
- `NON_AUTHORITATIVE`
- `UNRESOLVED`
