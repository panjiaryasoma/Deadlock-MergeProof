from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

from pydantic import ValidationError

from .models import MergeProofReport
from .validator import validate_report


def _format_location(location: tuple[int | str, ...]) -> str:
    return ".".join(str(part) for part in location) or "$"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a MergeProof JSON report.")
    parser.add_argument("report", type=Path)
    args = parser.parse_args(argv)

    try:
        raw = args.report.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        print(f"[ERROR] INPUT: {exc}", file=sys.stderr)
        return 2

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(
            f"[ERROR] JSON: line {exc.lineno}, column {exc.colno}: {exc.msg}",
            file=sys.stderr,
        )
        return 2

    try:
        report = MergeProofReport.model_validate(payload)
    except ValidationError as exc:
        for error in exc.errors(include_url=False):
            location = _format_location(error["loc"])
            print(f"[FAIL] STRUCTURAL_VALIDATION_ERROR at {location}: {error['msg']}")
        return 1

    issues = validate_report(report)
    if issues:
        for issue in issues:
            print(f"[FAIL] {issue.code}: {issue.message}")
        return 1

    print("[PASS] report satisfies the canonical contract and deterministic invariants")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
