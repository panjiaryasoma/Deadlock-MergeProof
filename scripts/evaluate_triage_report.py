from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml
from pydantic import ValidationError

from mergeproof.models import MergeProofReport
from mergeproof.triage_acceptance import TriageExpectation, evaluate_triage_report

REPO_ROOT = Path(__file__).resolve().parents[1]
CASE_IDS = tuple(f"TRIAGE-{index:03d}" for index in range(1, 9))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Evaluate one IBM Bob TRIAGE report against frozen ground truth."
    )
    parser.add_argument("--case", required=True, choices=CASE_IDS)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--workspace", type=Path)
    args = parser.parse_args()

    workspace = args.workspace or REPO_ROOT / "build" / "triage" / args.case
    expected_path = REPO_ROOT / "eval" / "expected" / f"{args.case}.yaml"
    context_path = workspace / "MERGEPROOF_RUN_CONTEXT.yaml"

    try:
        payload = json.loads(args.report.read_text(encoding="utf-8"))
        report = MergeProofReport.model_validate(payload)
        expected_payload = yaml.safe_load(expected_path.read_text(encoding="utf-8"))
        context = yaml.safe_load(context_path.read_text(encoding="utf-8"))
        expectation = TriageExpectation.from_mapping(expected_payload)
    except (OSError, json.JSONDecodeError, ValidationError, KeyError, ValueError) as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 2

    issues = evaluate_triage_report(report, expectation, context, workspace)
    if issues:
        for issue in issues:
            print(f"[FAIL] {issue.code}: {issue.message}")
        return 1

    print(f"[PASS] {args.case}: frozen TRIAGE acceptance satisfied")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
