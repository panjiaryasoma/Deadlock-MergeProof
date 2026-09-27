from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .enums import Advisory, FindingClass, FindingType, Severity
from .models import MergeProofReport, Source
from .validator import validate_report

LINE_LOCATOR = re.compile(
    r"^(?:line|lines|l)\s*(\d+)(?:\s*[-:]\s*(\d+))?$",
    re.IGNORECASE,
)
LOCATOR_TOKEN = re.compile(r"[A-Za-z_][A-Za-z0-9_-]{2,}")
GENERIC_LOCATOR_TOKENS = {
    "class",
    "function",
    "implementation",
    "line",
    "lines",
    "requirement",
    "section",
    "source",
    "symbol",
    "test",
    "tests",
}


@dataclass(frozen=True)
class TriageExpectation:
    case_id: str
    finding_class: FindingClass
    finding_type: FindingType
    severity: Severity
    advisory: Advisory

    @classmethod
    def from_mapping(cls, payload: dict[str, Any]) -> TriageExpectation:
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


def _workspace_yaml(workspace: Path, artifact: str) -> dict[str, Any] | None:
    path = _workspace_file(workspace, artifact)
    if path is None:
        return None
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError):
        return None
    return payload if isinstance(payload, dict) else None


def _registered_sources(
    workspace: Path,
    run_context: dict[str, Any],
) -> list[dict[str, Any]] | None:
    case_payload = _workspace_yaml(workspace, str(run_context.get("case_descriptor", "")))
    if case_payload is None:
        return None

    registry_path = case_payload.get("source_registry")
    if not isinstance(registry_path, str):
        return None

    registry = _workspace_yaml(workspace, registry_path)
    if registry is None:
        return None

    sources = registry.get("sources")
    if not isinstance(sources, list) or not sources:
        return None
    if not all(isinstance(source, dict) for source in sources):
        return None
    return sources


def _source_snapshot(source: Source) -> dict[str, Any]:
    return {
        "source_id": source.source_id,
        "source_type": source.source_type.value,
        "location": source.location,
        "authority": source.authority,
        "state": source.state.value,
        "scope": source.scope,
        "supersedes": source.supersedes,
    }


def _locator_resolves(path: Path, locator: str) -> bool:
    locator = locator.strip()
    if len(locator) < 3:
        return False

    text = path.read_text(encoding="utf-8")
    line_match = LINE_LOCATOR.fullmatch(locator)
    if line_match is not None:
        start = int(line_match.group(1))
        end = int(line_match.group(2) or start)
        line_count = len(text.splitlines())
        return 1 <= start <= end <= line_count

    if locator.casefold() in text.casefold():
        return True

    tokens = [
        token
        for token in LOCATOR_TOKEN.findall(locator)
        if token.casefold() not in GENERIC_LOCATOR_TOKENS
    ]
    lowered = text.casefold()
    return any(token.casefold() in lowered for token in tokens)


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

    case_payload = _workspace_yaml(
        workspace,
        str(run_context.get("case_descriptor", "")),
    )
    registered = _registered_sources(workspace, run_context)
    if case_payload is None or registered is None:
        issues.append(
            AcceptanceIssue(
                "SOURCE_REGISTRY_INVALID",
                "Case source registry is missing or malformed inside the workspace.",
            )
        )
        return issues

    expected_by_id = {str(source["source_id"]): source for source in registered}
    report_source_ids = {source.source_id for source in report.sources}
    context_source_ids = set(run_context.get("source_ids", []))
    registry_source_ids = set(expected_by_id)

    if report_source_ids != context_source_ids or report_source_ids != registry_source_ids:
        issues.append(
            AcceptanceIssue(
                "SOURCE_SET_MISMATCH",
                f"report={sorted(report_source_ids)!r}, "
                f"context={sorted(context_source_ids)!r}, "
                f"registry={sorted(registry_source_ids)!r}.",
            )
        )

    for source in report.sources:
        expected_source = expected_by_id.get(source.source_id)
        if expected_source is None:
            continue
        expected_snapshot = {
            "source_id": str(expected_source["source_id"]),
            "source_type": str(expected_source["source_type"]),
            "location": str(expected_source["location"]),
            "authority": str(expected_source["authority"]),
            "state": str(expected_source["state"]),
            "scope": list(expected_source["scope"]),
            "supersedes": expected_source.get("supersedes"),
        }
        actual_snapshot = _source_snapshot(source)
        if actual_snapshot != expected_snapshot:
            issues.append(
                AcceptanceIssue(
                    "SOURCE_METADATA_MISMATCH",
                    f"{source.source_id} metadata does not match the frozen source registry.",
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

    registered_locations = {
        str(source["location"])
        for source in registered
    }
    active_locations = {
        str(source["location"])
        for source in registered
        if str(source["state"]) == "ACTIVE"
    }
    relevant_repo_locations = set(run_context.get("changed_files", []))
    change_evidence = case_payload.get("change_evidence")
    if isinstance(change_evidence, str):
        relevant_repo_locations.add(change_evidence)

    superseded_locations = {
        str(source["location"])
        for source in registered
        if str(source["state"]) == "SUPERSEDED"
    }
    superseded_ids = {
        str(source["source_id"])
        for source in registered
        if str(source["state"]) == "SUPERSEDED"
    }
    superseding_locations = {
        str(source["location"])
        for source in registered
        if any(
            superseded_id in (source.get("supersedes") or [])
            for superseded_id in superseded_ids
        )
    }
    external_locations = {
        str(source["location"])
        for source in registered
        if str(source["source_type"]) == "EXTERNAL_GUIDANCE"
    }
    project_locations = {
        str(source["location"])
        for source in registered
        if str(source["source_type"]) != "EXTERNAL_GUIDANCE"
        and str(source["state"]) == "ACTIVE"
    }

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
        for anchor in finding.repo_anchors:
            if anchor.artifact not in relevant_repo_locations:
                issues.append(
                    AcceptanceIssue(
                        "REPO_ANCHOR_OUTSIDE_EVALUATED_SCOPE",
                        f"{finding.finding_id} repository anchor {anchor.artifact!r} "
                        "is not in the evaluated changed/relevant artifact scope.",
                    )
                )

        for anchor in finding.source_anchors:
            if anchor.artifact not in registered_locations:
                issues.append(
                    AcceptanceIssue(
                        "SOURCE_ANCHOR_NOT_REGISTERED",
                        f"{finding.finding_id} source anchor {anchor.artifact!r} "
                        "does not point to a registered source location.",
                    )
                )

        anchored_sources = {
            anchor.artifact
            for anchor in finding.source_anchors
            if anchor.artifact in registered_locations
        }

        if finding.finding_type is FindingType.SOURCE_CONFLICT:
            if len(active_locations) < 2 or not active_locations.issubset(anchored_sources):
                issues.append(
                    AcceptanceIssue(
                        "SOURCE_CONFLICT_EVIDENCE_INCOMPLETE",
                        f"{finding.finding_id} must cite both active sides of the "
                        "registered source conflict.",
                    )
                )

        if finding.finding_type is FindingType.STALE_SOURCE:
            required_stale_evidence = superseded_locations | superseding_locations
            if (
                not superseded_locations
                or not superseding_locations
                or not required_stale_evidence.issubset(anchored_sources)
            ):
                issues.append(
                    AcceptanceIssue(
                        "STALE_SOURCE_EVIDENCE_INCOMPLETE",
                        f"{finding.finding_id} must cite the superseded source and "
                        "the active source that explicitly supersedes it.",
                    )
                )

        if finding.finding_type is FindingType.UNSUPPORTED_BEST_PRACTICE_CLAIM:
            if (
                not (anchored_sources & external_locations)
                or not (anchored_sources & project_locations)
            ):
                issues.append(
                    AcceptanceIssue(
                        "BEST_PRACTICE_EVIDENCE_INCOMPLETE",
                        f"{finding.finding_id} must cite both project evidence and "
                        "the external-guidance source.",
                    )
                )

        for anchor in (
            *finding.repo_anchors,
            *finding.source_anchors,
            *finding.test_anchors,
        ):
            artifact = _workspace_file(workspace, anchor.artifact)
            if artifact is None:
                issues.append(
                    AcceptanceIssue(
                        "ANCHOR_ARTIFACT_MISSING",
                        f"{finding.finding_id} anchor points to missing workspace artifact "
                        f"{anchor.artifact!r}.",
                    )
                )
                continue
            if not _locator_resolves(artifact, anchor.locator):
                issues.append(
                    AcceptanceIssue(
                        "ANCHOR_LOCATOR_UNRESOLVED",
                        f"{finding.finding_id} locator {anchor.locator!r} does not "
                        f"resolve against {anchor.artifact!r}.",
                    )
                )

    return issues
