import pytest
from pydantic import ValidationError

from mergeproof.models import MergeProofReport
from mergeproof.validator import validate_report


def _payload() -> dict:
    return {
        "report_version": "1.0",
        "run_id": "acceptance-001",
        "advisory": "REVIEW_REQUIRED",
        "repository": {
            "commit_sha": "abc123",
            "changed_files": ["src/example.py"],
        },
        "sources": [
            {
                "source_id": "SRC-001",
                "source_type": "PRD",
                "location": "docs/PRD.md",
                "authority": "product_contract",
                "state": "ACTIVE",
                "scope": ["submission_deadline"],
            }
        ],
        "findings": [
            {
                "finding_id": "F-001",
                "finding_class": "CONFIRMED_ISSUE",
                "finding_type": "BOUNDARY_CONDITION_DRIFT",
                "title": "Boundary drift",
                "evidence_grade": "DIRECT",
                "severity": "HIGH",
                "repo_anchors": [
                    {
                        "artifact": "src/example.py",
                        "locator": "line 10",
                    }
                ],
                "source_anchors": [
                    {
                        "artifact": "docs/PRD.md",
                        "locator": "REQ-001",
                    }
                ],
                "rationale": "Boundary differs from requirement.",
            }
        ],
        "generated_at": "2026-09-27T02:00:00+07:00",
    }


def test_acceptance_valid_example_passes() -> None:
    report = MergeProofReport.model_validate(_payload())

    assert validate_report(report) == []


def test_acceptance_confirmed_issue_without_anchors_fails() -> None:
    payload = _payload()
    payload["findings"][0]["repo_anchors"] = []
    payload["findings"][0]["source_anchors"] = []

    report = MergeProofReport.model_validate(payload)
    codes = {issue.code for issue in validate_report(report)}

    assert "FINDING_WITHOUT_REPOSITORY_ANCHOR" in codes
    assert "NON_CLEAN_WITHOUT_SOURCE_ANCHOR" in codes


def test_acceptance_invalid_enum_fails() -> None:
    payload = _payload()
    payload["findings"][0]["finding_class"] = "BUG"

    with pytest.raises(ValidationError):
        MergeProofReport.model_validate(payload)


def test_acceptance_no_issue_with_high_severity_fails() -> None:
    payload = _payload()
    payload["findings"][0].update(
        {
            "finding_class": "NO_ISSUE",
            "finding_type": "HARMLESS_REFACTOR",
            "severity": "HIGH",
            "source_anchors": [],
        }
    )

    report = MergeProofReport.model_validate(payload)
    codes = {issue.code for issue in validate_report(report)}

    assert "NO_ISSUE_WITH_NON_NONE_SEVERITY" in codes
