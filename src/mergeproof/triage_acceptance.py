from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .enums import Advisory, FindingClass, FindingType, Severity
from .models import MergeProofReport
from .validator import validate_report


@dataclass(frozen=True)
class TriageExpectation:
    case_id: str
    finding_class: FindingClass
    finding_type: FindingType
    severity: Severity
    advisory: Advisory

    @classmethod
    def from_mapping(cls, payload: dict[str, Any]) -> "TriageExpectation":
        expected = payload["expected"]
        return cls(
            case_id=str(payload["case_id"]),
            finding_class=FindingClass(expected["finding_class"]),
            finding_type=FindingType(expected["finding_type"]),
            severity=Severity(expected["severity"]),
            advisory=Advisory(expected["advisory"]),
        )


@dataclass(frozen=True)
class AcceptanceIssue:
    code: str
    message: str


def _workspace_file(workspace: Path, artifact: str) -> Path | None:
    artifact_path = Path(artifact)
    if artifact_path.is_absolute():
        return None

    root = workspace.resolve()
    candidate = (root / artifact_path).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        return None
    return candidate if candidate.is_file() else None


def evaluate_triage_report(
    report: MergeProofReport,
    expectation: TriageExpectation,
    run_context: dict[str, Any],
    workspace: Path,
) -> list[AcceptanceIssue]:
    issues: list[AcceptanceIssue] = []

    for semantic_issue in validate_report(report):
        issues.append(
            AcceptanceIssue(
                f"SEMANTIC_{semantic_issue.code}",
                semantic_issue.message,
            )
        )

    provenance_pairs = (
        ("report_version", report.report_version, run_context.get("report_schema_version")),
        ("run_id", report.run_id, run_context.get("run_id")),
        (
            "repository.commit_sha",
            report.repository.commit_sha,
            run_context.get("repository_commit_sha"),
        ),
        (
            "repository.changed_files",
            report.repository.changed_files,
            run_context.get("changed_files"),
        ),
        ("generated_at", report.generated_at, run_context.get("timestamp")),
    )
    for field_name, actual, expected in provenance_pairs:
        if actual != expected:
            issues.append(
                AcceptanceIssue(
                    "RUN_PROVENANCE_MISMATCH",
                    f"{field_name}={actual!r} does not match run context {expected!r}.",
                )
            )

    report_source_ids = {source.source_id for source in report.sources}
    context_source_ids = set(run_context.get("source_ids", []))
    if report_source_ids != context_source_ids:
        issues.append(
            AcceptanceIssue(
                "SOURCE_SET_MISMATCH",
                f"report source IDs {sorted(report_source_ids)!r} do not match "
                f"run context {sorted(context_source_ids)!r}.",
            )
        )

    if report.advisory is not expectation.advisory:
        issues.append(
            AcceptanceIssue(
                "ADVISORY_MISMATCH",
                f"{expectation.case_id} expected {expectation.advisory.value}, "
                f"got {report.advisory.value}.",
            )
        )

    matching = [
        finding
        for finding in report.findings
        if finding.finding_class is expectation.finding_class
        and finding.finding_type is expectation.finding_type
        and finding.severity is expectation.severity
    ]
    if not matching:
        issues.append(
            AcceptanceIssue(
                "EXPECTED_FINDING_MISSING",
                f"{expectation.case_id} requires "
                f"{expectation.finding_class.value}/"
                f"{expectation.finding_type.value}/"
                f"{expectation.severity.value}.",
            )
        )
    elif not any(finding.source_anchors for finding in matching):
        issues.append(
            AcceptanceIssue(
                "EXPECTED_FINDING_WITHOUT_SOURCE_ANCHOR",
                f"{expectation.case_id} expected finding must cite source evidence.",
            )
        )

    for source in report.sources:
        if _workspace_file(workspace, source.location) is None:
            issues.append(
                AcceptanceIssue(
                    "SOURCE_LOCATION_MISSING",
                    f"Source {source.source_id} points to missing workspace artifact "
                    f"{source.location!r}.",
                )
            )

    for finding in report.findings:
        for anchor in (
            *finding.repo_anchors,
            *finding.source_anchors,
            *finding.test_anchors,
        ):
            if _workspace_file(workspace, anchor.artifact) is None:
                issues.append(
                    AcceptanceIssue(
                        "ANCHOR_ARTIFACT_MISSING",
                        f"{finding.finding_id} anchor points to missing workspace artifact "
                        f"{anchor.artifact!r}.",
                    )
                )

    return issues
