# Submission Deadline Requirements

## Source metadata

- Source ID: `SRC-PRD-001`
- Source type: `PRD`
- State: `ACTIVE`
- Authority: `product_contract`
- Scope: `src/deadline.py`

## REQ-DEADLINE-001

Criticality: `HIGH`

A submission is expired when `evaluated_at >= submission_deadline`.

The equality boundary is part of the requirement: evaluating exactly at the submission deadline is expired.
