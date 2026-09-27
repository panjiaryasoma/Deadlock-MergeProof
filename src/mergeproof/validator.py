from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from .enums import EvidenceGrade, FindingClass, FindingType, Severity
from .models import MergeProofReport

FORBIDDEN_FIELDS = frozenset({"llm_confidence_percent", "probability_correct"})


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    message: str


def _iter_forbidden_fields(value: Any, path: str = "$") -> list[tuple[str, str]]:
    matches: list[tuple[str, str]] = []

    if isinstance(value, Mapping):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if key in FORBIDDEN_FIELDS:
                matches.append((key, child_path))
            matches.extend(_iter_forbidden_fields(child, child_path))
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for index, child in enumerate(value):
            matches.extend(_iter_forbidden_fields(child, f"{path}[{index}]"))

    return matches


def validate_report(report: MergeProofReport) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for finding in report.findings:
        if not finding.repo_anchors:
            issues.append(
                ValidationIssue(
                    "FINDING_WITHOUT_REPOSITORY_ANCHOR",
                    f"{finding.finding_id} must include at least one repository anchor.",
                )
            )

        if finding.finding_class is FindingClass.CONFIRMED_ISSUE:
            if finding.evidence_grade not in {
                EvidenceGrade.DIRECT,
                EvidenceGrade.CORROBORATED,
            }:
                issues.append(
                    ValidationIssue(
                        "CONFIRMED_WITH_WEAK_EVIDENCE",
                        f"{finding.finding_id} must use DIRECT or CORROBORATED evidence.",
                    )
                )
            if not finding.source_anchors:
                issues.append(
                    ValidationIssue(
                        "CONFIRMED_WITHOUT_SOURCE_ANCHOR",
                        f"{finding.finding_id} must include at least one source anchor.",
                    )
                )

        if finding.finding_class is FindingClass.NO_ISSUE and finding.severity is not Severity.NONE:
            issues.append(
                ValidationIssue(
                    "NO_ISSUE_WITH_NON_NONE_SEVERITY",
                    f"{finding.finding_id} must use severity NONE when finding_class is NO_ISSUE.",
                )
            )

        if (
            finding.finding_type is FindingType.UNSUPPORTED_BEST_PRACTICE_CLAIM
            and finding.finding_class is FindingClass.CONFIRMED_ISSUE
        ):
            issues.append(
                ValidationIssue(
                    "CONFIRMED_BEST_PRACTICE_CLAIM",
                    f"{finding.finding_id} cannot classify an unsupported best-practice claim "
                    "as CONFIRMED_ISSUE.",
                )
            )

    payload = report.model_dump(mode="python", exclude_unset=True)
    for field_name, path in _iter_forbidden_fields(payload):
        issues.append(
            ValidationIssue(
                "FORBIDDEN_FIELD",
                f"{path} uses forbidden field {field_name!r}.",
            )
        )

    return issues
