from __future__ import annotations

from collections import Counter
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

    source_id_counts = Counter(source.source_id for source in report.sources)
    for source_id, count in source_id_counts.items():
        if count > 1:
            issues.append(
                ValidationIssue(
                    "DUPLICATE_SOURCE_ID",
                    f"{source_id} appears {count} times; source_id values must be unique.",
                )
            )

    known_source_ids = set(source_id_counts)
    for requirement in report.requirements:
        if requirement.source_id not in known_source_ids:
            issues.append(
                ValidationIssue(
                    "UNKNOWN_REQUIREMENT_SOURCE_ID",
                    f"{requirement.requirement_id} references unknown source_id "
                    f"{requirement.source_id!r}.",
                )
            )

    for finding in report.findings:
        if not finding.repo_anchors:
            issues.append(
                ValidationIssue(
                    "FINDING_WITHOUT_REPOSITORY_ANCHOR",
                    f"{finding.finding_id} must include at least one repository anchor.",
                )
            )

        requires_source_anchor = (
            finding.finding_class
            in {
                FindingClass.CONFIRMED_ISSUE,
                FindingClass.SPEC_AMBIGUITY,
            }
            or finding.finding_type
            in {
                FindingType.SOURCE_CONFLICT,
                FindingType.UNSUPPORTED_BEST_PRACTICE_CLAIM,
            }
        )
        if requires_source_anchor and not finding.source_anchors:
            issues.append(
                ValidationIssue(
                    "FINDING_WITHOUT_REQUIRED_SOURCE_ANCHOR",
                    f"{finding.finding_id} must include at least one source anchor "
                    "for this finding class/type.",
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
