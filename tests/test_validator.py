from mergeproof.models import MergeProofReport
from mergeproof.validator import validate_report


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


def _report(payload: dict | None = None) -> MergeProofReport:
    return MergeProofReport.model_validate(payload or _valid_payload())


def _codes(report: MergeProofReport) -> list[str]:
    return [issue.code for issue in validate_report(report)]


def test_valid_canonical_report_has_no_semantic_issues() -> None:
    assert validate_report(_report()) == []


def test_confirmed_issue_rejects_weak_evidence() -> None:
    payload = _valid_payload()
    payload["findings"][0]["evidence_grade"] = "INFERRED"

    assert "CONFIRMED_WITH_WEAK_EVIDENCE" in _codes(_report(payload))


def test_confirmed_issue_requires_source_anchor() -> None:
    payload = _valid_payload()
    payload["findings"][0]["source_anchors"] = []

    assert "FINDING_WITHOUT_REQUIRED_SOURCE_ANCHOR" in _codes(_report(payload))


def test_spec_ambiguity_requires_source_anchor() -> None:
    payload = _valid_payload()
    payload["findings"][0].update(
        {
            "finding_class": "SPEC_AMBIGUITY",
            "finding_type": "SOURCE_CONFLICT",
            "severity": "NONE",
            "source_anchors": [],
        }
    )

    assert "FINDING_WITHOUT_REQUIRED_SOURCE_ANCHOR" in _codes(_report(payload))


def test_best_practice_risk_requires_source_anchor() -> None:
    payload = _valid_payload()
    payload["findings"][0].update(
        {
            "finding_class": "POTENTIAL_RISK",
            "finding_type": "UNSUPPORTED_BEST_PRACTICE_CLAIM",
            "severity": "MEDIUM",
            "source_anchors": [],
        }
    )

    assert "FINDING_WITHOUT_REQUIRED_SOURCE_ANCHOR" in _codes(_report(payload))


def test_other_potential_risk_is_not_blanket_source_anchor_rejected() -> None:
    payload = _valid_payload()
    payload["findings"][0].update(
        {
            "finding_class": "POTENTIAL_RISK",
            "finding_type": "API_CONTRACT_DRIFT",
            "evidence_grade": "INFERRED",
            "severity": "LOW",
            "source_anchors": [],
        }
    )

    assert "FINDING_WITHOUT_REQUIRED_SOURCE_ANCHOR" not in _codes(_report(payload))


def test_every_finding_requires_repository_anchor() -> None:
    payload = _valid_payload()
    payload["findings"][0]["repo_anchors"] = []

    assert "FINDING_WITHOUT_REPOSITORY_ANCHOR" in _codes(_report(payload))


def test_no_issue_requires_none_severity() -> None:
    payload = _valid_payload()
    payload["findings"][0].update(
        {
            "finding_class": "NO_ISSUE",
            "finding_type": "HARMLESS_REFACTOR",
            "severity": "HIGH",
            "source_anchors": [],
        }
    )

    assert "NO_ISSUE_WITH_NON_NONE_SEVERITY" in _codes(_report(payload))


def test_best_practice_claim_cannot_be_confirmed_issue() -> None:
    payload = _valid_payload()
    payload["findings"][0]["finding_type"] = "UNSUPPORTED_BEST_PRACTICE_CLAIM"

    assert "CONFIRMED_BEST_PRACTICE_CLAIM" in _codes(_report(payload))


def test_duplicate_source_ids_are_rejected() -> None:
    payload = _valid_payload()
    duplicate = dict(payload["sources"][0])
    payload["sources"].append(duplicate)

    assert "DUPLICATE_SOURCE_ID" in _codes(_report(payload))


def test_requirement_source_id_must_reference_registered_source() -> None:
    payload = _valid_payload()
    payload["requirements"][0]["source_id"] = "SRC-GAIB"

    assert "UNKNOWN_REQUIREMENT_SOURCE_ID" in _codes(_report(payload))


def test_valid_source_ids_and_requirement_references_pass() -> None:
    assert "DUPLICATE_SOURCE_ID" not in _codes(_report())
    assert "UNKNOWN_REQUIREMENT_SOURCE_ID" not in _codes(_report())


def test_forbidden_probability_fields_are_found_recursively() -> None:
    payload = _valid_payload()
    payload["metadata"] = {
        "llm_confidence_percent": 91,
        "nested": {"probability_correct": 0.91},
    }

    issues = validate_report(_report(payload))
    forbidden_messages = [issue.message for issue in issues if issue.code == "FORBIDDEN_FIELD"]

    assert len(forbidden_messages) == 2
    assert "$.metadata.llm_confidence_percent" in forbidden_messages[0]
    assert "$.metadata.nested.probability_correct" in forbidden_messages[1]


def test_unknown_harmless_extension_is_not_rejected() -> None:
    payload = _valid_payload()
    payload["metadata"] = {
        "confidence_label": "direct",
        "producer": "bob",
    }
    payload["findings"][0]["extension"] = {"review_hint": "boundary"}

    assert validate_report(_report(payload)) == []


def test_validator_collects_all_observable_issues() -> None:
    payload = _valid_payload()
    payload["findings"][0].update(
        {
            "evidence_grade": "INFERRED",
            "source_anchors": [],
            "repo_anchors": [],
            "finding_type": "UNSUPPORTED_BEST_PRACTICE_CLAIM",
        }
    )
    payload["probability_correct"] = 0.75

    codes = _codes(_report(payload))

    assert codes.count("FINDING_WITHOUT_REPOSITORY_ANCHOR") == 1
    assert codes.count("FINDING_WITHOUT_REQUIRED_SOURCE_ANCHOR") == 1
    assert codes.count("CONFIRMED_WITH_WEAK_EVIDENCE") == 1
    assert codes.count("CONFIRMED_BEST_PRACTICE_CLAIM") == 1
    assert codes.count("FORBIDDEN_FIELD") == 1
    assert len(codes) == 5
