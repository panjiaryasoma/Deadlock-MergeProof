from mergeproof.aggregator import aggregate_advisory
from mergeproof.enums import Advisory, EvidenceGrade, FindingClass, SourceAuthority, SourceState
from mergeproof.models import Finding, SourceRecord


def test_clean_case_passes() -> None:
    findings = [
        Finding(
            finding_id="F-001",
            finding_class=FindingClass.NO_ISSUE,
            evidence_grade=EvidenceGrade.DIRECT,
        )
    ]
    assert aggregate_advisory(findings, []) is Advisory.PASS


def test_conflicting_source_abstains() -> None:
    sources = [
        SourceRecord(
            source_id="SRC-001",
            path="docs/spec.md",
            state=SourceState.CONFLICTING,
            authority=SourceAuthority.UNRESOLVED,
        )
    ]
    assert aggregate_advisory([], sources) is Advisory.ABSTAIN
