# Final Output Transport

Intermediate workflow reasoning is internal.

Do not emit user-visible:
- block/stage headings;
- progress messages;
- "all skills loaded" messages;
- precondition confirmations;
- source-resolution narration;
- requirement-trace narration;
- implementation/test-audit narration;
- classification/severity narration;
- self-audit narration;
- reconciliation narration;
- "proceeding to report synthesis" messages.

For a successful verification run, the entire user-visible response MUST be exactly
one raw JSON object conforming to the canonical MergeProof report schema.

Mechanical contract:
- first non-whitespace character: `{`
- last non-whitespace character: `}`
- no Markdown code fence
- no prose before the object
- no prose after the object

This rule constrains transport only. It does not change evidence, classification,
severity, advisory, or human merge authority.
