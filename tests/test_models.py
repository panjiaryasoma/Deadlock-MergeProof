import pytest
from pydantic import ValidationError

from mergeproof.enums import (
    Advisory,
    EvidenceGrade,
    FindingClass,
    FindingType,
    RequirementAmbiguity,
    RequirementCriticality,
    Severity,
    SourceState,
    SourceType,
)
from mergeproof.models import MergeProofReport


def _valid_payload() -> dict:
    return {
        "report_version": "1.0",
        "run_id": "run-001",
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
        "requirements": [
            {
                "requirement_id": "REQ-001",
                "source_id": "SRC-001",
                "statement": "evaluated_at >= submission_deadline",
                "scope": ["submission_deadline"],
                "criticality": "HIGH",
            }
        ],
        "findings": [
            {
                "finding_id": "F-001",
                "finding_class": "CONFIRMED_ISSUE",
                "finding_type": "BOUNDARY_CONDITION_DRIFT",
                "title": "Deadline equality boundary drift",
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
                "rationale": "Implementation excludes the equality case required by the source.",
            }
        ],
        "generated_at": "2026-09-27T02:00:00+07:00",
    }


def test_canonical_payload_maps_to_typed_models() -> None:
    report = MergeProofReport.model_validate(_valid_payload())

    assert report.advisory is Advisory.REVIEW_REQUIRED
    assert report.sources[0].source_type is SourceType.PRD
    assert report.sources[0].state is SourceState.ACTIVE
    assert report.requirements[0].criticality is RequirementCriticality.HIGH
    assert report.findings[0].finding_class is FindingClass.CONFIRMED_ISSUE
    assert report.findings[0].finding_type is FindingType.BOUNDARY_CONDITION_DRIFT
    assert report.findings[0].evidence_grade is EvidenceGrade.DIRECT
    assert report.findings[0].severity is Severity.HIGH


def test_missing_ambiguity_remains_unset_on_serialization() -> None:
    report = MergeProofReport.model_validate(_valid_payload())

    requirement = report.requirements[0]
    dumped_requirement = requirement.model_dump(mode="json", exclude_unset=True)

    assert requirement.ambiguity is None
    assert "ambiguity" not in requirement.model_fields_set
    assert "ambiguity" not in dumped_requirement


def test_explicit_ambiguity_enum_is_preserved() -> None:
    payload = _valid_payload()
    payload["requirements"][0]["ambiguity"] = "MATERIAL"

    report = MergeProofReport.model_validate(payload)
    requirement = report.requirements[0]

    assert requirement.ambiguity is RequirementAmbiguity.MATERIAL
    assert requirement.model_dump(mode="json", exclude_unset=True)["ambiguity"] == "MATERIAL"


def test_explicit_null_ambiguity_is_rejected() -> None:
    payload = _valid_payload()
    payload["requirements"][0]["ambiguity"] = None

    with pytest.raises(ValidationError, match="ambiguity may be omitted but must not be null"):
        MergeProofReport.model_validate(payload)


def test_optional_report_fields_may_be_omitted() -> None:
    payload = _valid_payload()
    payload.pop("requirements")

    report = MergeProofReport.model_validate(payload)

    assert report.requirements == []
    assert report.human_override is None


def test_exclude_unset_does_not_synthesize_omitted_optional_fields() -> None:
    report = MergeProofReport.model_validate(_valid_payload())
    dumped = report.model_dump(mode="json", exclude_unset=True)

    requirement = dumped["requirements"][0]
    finding = dumped["findings"][0]

    assert "ambiguity" not in requirement
    assert "requirement_ids" not in finding
    assert "test_anchors" not in finding
    assert "human_override" not in dumped
    assert "source_anchors" in finding


def test_unknown_fields_are_preserved_at_nested_levels() -> None:
    payload = _valid_payload()
    payload["report_extension"] = {"producer": "bob"}
    payload["repository"]["repository_extension"] = "kept"
    payload["sources"][0]["source_extension"] = {"origin": "fixture"}
    payload["requirements"][0]["requirement_extension"] = True
    payload["findings"][0]["finding_extension"] = 7
    payload["findings"][0]["repo_anchors"][0]["anchor_extension"] = "kept"

    report = MergeProofReport.model_validate(payload)
    dumped = report.model_dump(mode="json")

    assert dumped["report_extension"] == {"producer": "bob"}
    assert dumped["repository"]["repository_extension"] == "kept"
    assert dumped["sources"][0]["source_extension"] == {"origin": "fixture"}
    assert dumped["requirements"][0]["requirement_extension"] is True
    assert dumped["findings"][0]["finding_extension"] == 7
    assert dumped["findings"][0]["repo_anchors"][0]["anchor_extension"] == "kept"


def test_missing_required_report_field_is_rejected() -> None:
    payload = _valid_payload()
    payload.pop("repository")

    with pytest.raises(ValidationError):
        MergeProofReport.model_validate(payload)


def test_invalid_canonical_enum_is_rejected() -> None:
    payload = _valid_payload()
    payload["findings"][0]["severity"] = "UNSPECIFIED_BY_PROJECT"

    with pytest.raises(ValidationError):
        MergeProofReport.model_validate(payload)


def test_old_report_shape_cannot_replace_required_canonical_fields() -> None:
    payload = _valid_payload()
    payload.pop("repository")
    payload["scope"] = {"changed_files": ["src/example.py"]}

    with pytest.raises(ValidationError):
        MergeProofReport.model_validate(payload)
