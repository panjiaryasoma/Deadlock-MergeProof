from mergeproof.enums import (
    Advisory,
    EvidenceGrade,
    FindingClass,
    SourceAuthority,
    SourceState,
)
from mergeproof.models import EvidenceAnchor, Finding, MergeProofReport, Scope, SourceRecord
from mergeproof.validator import validate_report


def test_valid_confirmed_issue() -> None:
    report = MergeProofReport(
        report_version="0.1",
        run_id="test-001",
        advisory=Advisory.REVIEW_REQUIRED,
        scope=Scope(changed_files=["src/example.py"]),
        sources=[
            SourceRecord(
                source_id="SRC-001",
                path="docs/spec.md",
                state=SourceState.ACTIVE,
                authority=SourceAuthority.AUTHORITATIVE,
            )
        ],
        findings=[
            Finding(
                finding_id="F-001",
                finding_class=FindingClass.CONFIRMED_ISSUE,
                evidence_grade=EvidenceGrade.DIRECT,
                source_evidence=[EvidenceAnchor(artifact="docs/spec.md", locator="REQ-001")],
                repository_evidence=[EvidenceAnchor(artifact="src/example.py", locator="line 10")],
            )
        ],
    )
    assert validate_report(report) == []


def test_confirmed_without_evidence_is_rejected() -> None:
    report = MergeProofReport(
        report_version="0.1",
        run_id="test-002",
        advisory=Advisory.REVIEW_REQUIRED,
        scope=Scope(),
        findings=[
            Finding(
                finding_id="F-001",
                finding_class=FindingClass.CONFIRMED_ISSUE,
                evidence_grade=EvidenceGrade.INFERRED,
            )
        ],
    )
    codes = {issue.code for issue in validate_report(report)}
    assert "CONFIRMED_WITH_WEAK_EVIDENCE" in codes
    assert "CONFIRMED_WITHOUT_SOURCE_EVIDENCE" in codes
    assert "CONFIRMED_WITHOUT_REPOSITORY_EVIDENCE" in codes


def test_unresolved_authority_requires_abstain() -> None:
    report = MergeProofReport(
        report_version="0.1",
        run_id="test-003",
        advisory=Advisory.PASS,
        scope=Scope(),
        sources=[
            SourceRecord(
                source_id="SRC-001",
                path="docs/spec.md",
                state=SourceState.ACTIVE,
                authority=SourceAuthority.UNRESOLVED,
            )
        ],
    )
    codes = {issue.code for issue in validate_report(report)}
    assert "UNRESOLVED_AUTHORITY_WITHOUT_ABSTAIN" in codes
