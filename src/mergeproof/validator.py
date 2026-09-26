from __future__ import annotations

from dataclasses import dataclass

from .enums import Advisory, EvidenceGrade, FindingClass, SourceAuthority, SourceState
from .models import MergeProofReport


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    message: str


def validate_report(report: MergeProofReport) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for finding in report.findings:
        if finding.finding_class is FindingClass.CONFIRMED_ISSUE:
            if finding.evidence_grade not in {
                EvidenceGrade.DIRECT,
                EvidenceGrade.CORROBORATED,
            }:
                issues.append(
                    ValidationIssue(
                        "CONFIRMED_WITH_WEAK_EVIDENCE",
                        f"{finding.finding_id} lacks direct/corroborated evidence.",
                    )
                )
            if not finding.source_evidence:
                issues.append(
                    ValidationIssue(
                        "CONFIRMED_WITHOUT_SOURCE_EVIDENCE",
                        f"{finding.finding_id} has no source evidence.",
                    )
                )
            if not finding.repository_evidence:
                issues.append(
                    ValidationIssue(
                        "CONFIRMED_WITHOUT_REPOSITORY_EVIDENCE",
                        f"{finding.finding_id} has no repository evidence.",
                    )
                )

    unresolved_authority = any(
        source.state is SourceState.CONFLICTING
        or source.authority is SourceAuthority.UNRESOLVED
        for source in report.sources
    )

    if unresolved_authority and report.advisory is not Advisory.ABSTAIN:
        issues.append(
            ValidationIssue(
                "UNRESOLVED_AUTHORITY_WITHOUT_ABSTAIN",
                "Unresolved/conflicting authority requires ABSTAIN.",
            )
        )

    if report.unresolved_questions and report.advisory is Advisory.PASS:
        issues.append(
            ValidationIssue(
                "PASS_WITH_UNRESOLVED_QUESTIONS",
                "PASS is invalid while material unresolved questions remain.",
            )
        )

    return issues
