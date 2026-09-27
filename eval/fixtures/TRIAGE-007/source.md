# Source artifacts

## SRC-TRIAGE-007-PRD

- Source ID: `SRC-TRIAGE-007-PRD`
- Source type: `PRD`
- State: `ACTIVE`
- Authority: `product_contract`
- Scope: `eval/fixtures/TRIAGE-007/implementation.py`

### REQ-TRIAGE-007

- Criticality: `LOW`
- Statement: The handler reads the optional `name` field and returns a greeting.
- Note: This project source does not require runtime schema validation.

## SRC-TRIAGE-007-EXT

- Source ID: `SRC-TRIAGE-007-EXT`
- Source type: `EXTERNAL_GUIDANCE`
- State: `ACTIVE`
- Authority: `external_guidance`
- Scope: `eval/fixtures/TRIAGE-007/implementation.py`

### Guidance

External guidance recommends validating untrusted request payloads against an explicit runtime schema.
