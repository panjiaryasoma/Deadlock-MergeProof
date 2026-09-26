# Integration 001

Purpose: prove the complete path from source registration to final advisory.

Scenario:
- source says `>=`;
- implementation uses `>`;
- equality boundary test is absent.

Expected:
1. source resolved as active;
2. requirement extracted;
3. implementation operator mismatch detected;
4. missing equality test detected;
5. two findings produced;
6. final advisory `REVIEW_REQUIRED`;
7. report passes deterministic validator.
