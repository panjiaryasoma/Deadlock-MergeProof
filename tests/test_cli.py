import json
from pathlib import Path

from mergeproof.cli import main


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
        "findings": [
            {
                "finding_id": "F-001",
                "finding_class": "CONFIRMED_ISSUE",
                "finding_type": "BOUNDARY_CONDITION_DRIFT",
                "title": "Deadline drift",
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
                "rationale": "Boundary differs.",
            }
        ],
        "generated_at": "2026-09-27T02:00:00+07:00",
    }


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_cli_returns_zero_for_valid_report(tmp_path: Path, capsys) -> None:
    path = tmp_path / "report.json"
    _write_json(path, _valid_payload())

    assert main([str(path)]) == 0
    assert "[PASS]" in capsys.readouterr().out


def test_cli_returns_one_for_semantic_invalid_report(tmp_path: Path, capsys) -> None:
    payload = _valid_payload()
    payload["findings"][0]["repo_anchors"] = []
    path = tmp_path / "report.json"
    _write_json(path, payload)

    assert main([str(path)]) == 1
    assert "FINDING_WITHOUT_REPOSITORY_ANCHOR" in capsys.readouterr().out


def test_cli_returns_one_for_structural_invalid_report(tmp_path: Path, capsys) -> None:
    payload = _valid_payload()
    payload["findings"][0]["severity"] = "SEVERE"
    path = tmp_path / "report.json"
    _write_json(path, payload)

    assert main([str(path)]) == 1
    assert "STRUCTURAL_VALIDATION_ERROR" in capsys.readouterr().out


def test_cli_returns_two_for_malformed_json(tmp_path: Path, capsys) -> None:
    path = tmp_path / "report.json"
    path.write_text("{not json", encoding="utf-8")

    assert main([str(path)]) == 2
    assert "[ERROR] JSON" in capsys.readouterr().err


def test_cli_returns_two_for_missing_file(tmp_path: Path, capsys) -> None:
    path = tmp_path / "missing.json"

    assert main([str(path)]) == 2
    assert "[ERROR] INPUT" in capsys.readouterr().err
