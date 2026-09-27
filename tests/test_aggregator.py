from mergeproof.aggregator import aggregate_advisory
from mergeproof.enums import (
    Advisory,
    EvidenceGrade,
    FindingClass,
    FindingType,
    Severity,
    SourceState,
    SourceType,
)
from mergeproof.models import Anchor, Finding, Source


def _anchor() -> Anchor:
    return Anchor(artifact="src/example.py", locator="line 10")


def test_clean_case_passes() -> None:
    findings = [
        Finding(
            finding_id="F-001",
            finding_class=FindingClass.NO_ISSUE,
            finding_type=FindingType.HARMLESS_REFACTOR,
            title="Clean refactor",
            evidence_grade=EvidenceGrade.DIRECT,
            severity=Severity.NONE,
            repo_anchors=[_anchor()],
            rationale="No behavioral contract change.",
        )
    ]
    assert aggregate_advisory(findings, []) is Advisory.PASS


def test_confirmed_issue_requires_review() -> None:
    findings = [
        Finding(
            finding_id="F-001",
            finding_class=FindingClass.CONFIRMED_ISSUE,
            finding_type=FindingType.BOUNDARY_CONDITION_DRIFT,
            title="Boundary drift",
            evidence_grade=EvidenceGrade.DIRECT,
            severity=Severity.HIGH,
            repo_anchors=[_anchor()],
            source_anchors=[Anchor(artifact="docs/PRD.md", locator="REQ-001")],
            rationale="Boundary differs from requirement.",
        )
    ]
    assert aggregate_advisory(findings, []) is Advisory.REVIEW_REQUIRED


def test_conflicting_source_abstains() -> None:
    sources = [
        Source(
            source_id="SRC-001",
            source_type=SourceType.PRD,
            location="docs/PRD.md",
            authority="product_contract",
            state=SourceState.CONFLICTING,
            scope=["submission_deadline"],
        )
    ]
    assert aggregate_advisory([], sources) is Advisory.ABSTAIN
