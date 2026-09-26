# Finding Contract

Every material finding should contain:
- finding class
- source evidence
- repository evidence
- test evidence when relevant
- evidence grade
- severity
- impact
- uncertainty
- human check required

Severity must conform to the frozen report contract:
- `CRITICAL`
- `HIGH`
- `MEDIUM`
- `LOW`
- `NONE`

Do not emit `UNSPECIFIED_BY_PROJECT`.

For frozen material ambiguity and source-conflict cases represented as
`SPEC_AMBIGUITY`, severity is `NONE`.
