# Source Governance

`ACTIVE` is a lifecycle state.

`AUTHORITATIVE` is a governance property.

Never equate the two.

Resolve source authority in this order:

1. explicit supersession metadata;
2. explicit repository-defined governance or precedence;
3. explicit source scope/applicability;
4. otherwise preserve the conflict as unresolved.

Do not invent precedence from:
- filename;
- document type;
- recency alone;
- prose quality;
- formality;
- engineering preference.

Unresolved applicable source conflict must be handed to
`conflict-abstention`.
