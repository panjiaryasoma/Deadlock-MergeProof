from __future__ import annotations

import argparse
import json
from pathlib import Path

from .models import MergeProofReport
from .validator import validate_report


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a MergeProof JSON report.")
    parser.add_argument("report", type=Path)
    args = parser.parse_args()

    payload = json.loads(args.report.read_text(encoding="utf-8"))
    report = MergeProofReport.model_validate(payload)
    issues = validate_report(report)

    if issues:
        for issue in issues:
            print(f"[FAIL] {issue.code}: {issue.message}")
        return 1

    print("[PASS] report satisfies current deterministic invariants")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
