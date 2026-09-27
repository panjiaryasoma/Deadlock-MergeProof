from __future__ import annotations

import json
import shlex
import subprocess
import sys
from pathlib import Path

import yaml

from mergeproof.models import MergeProofReport
from mergeproof.triage_acceptance import TriageExpectation, evaluate_triage_report

REPO_ROOT = Path(__file__).resolve().parents[1]
CASE_IDS = tuple(f"TRIAGE-{index:03d}" for index in range(1, 9))


def _load_yaml(path: Path) -> dict:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def _suite_rows() -> dict[str, tuple[str, str, str, str]]:
    suite = (
        REPO_ROOT
        / "docs/05_PREPRODUCTION/02_TRIAGE_ACCEPTANCE/TRIAGE_EVALUATION_SUITE.md"
    ).read_text(encoding="utf-8")
    rows: dict[str, tuple[str, str, str, str]] = {}
    for line in suite.splitlines():
        if not line.startswith("| TRIAGE-"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        rows[cells[0]] = (cells[2], cells[3], cells[4], cells[5])
    return rows


def test_machine_expected_matches_frozen_suite() -> None:
    rows = _suite_rows()
    assert tuple(rows) == CASE_IDS

    for case_id in CASE_IDS:
        payload = _load_yaml(REPO_ROOT / "eval" / "expected" / f"{case_id}.yaml")
        expected = payload["expected"]
        assert (
            expected["finding_class"],
            expected["finding_type"],
            expected["severity"],
            expected["advisory"],
        ) == rows[case_id]


def test_fixture_paths_exist_and_do_not_embed_expected_labels() -> None:
    for case_id in CASE_IDS:
        root = REPO_ROOT / "eval" / "fixtures" / case_id
        case = _load_yaml(root / "case.yaml")
        expected = _load_yaml(REPO_ROOT / "eval" / "expected" / f"{case_id}.yaml")[
            "expected"
        ]

        for raw_path in (
            *case["source_files"],
            *case["changed_files"],
            case["application_entrypoint"],
        ):
            assert (REPO_ROOT / raw_path).is_file(), raw_path

        visible_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in root.rglob("*")
            if path.is_file() and path.suffix in {".md", ".py", ".yaml", ".yml", ".txt"}
        )
        for key in ("finding_class", "finding_type", "advisory"):
            assert expected[key] not in visible_text


def test_all_fixture_test_commands_are_runnable_and_green() -> None:
    for case_id in CASE_IDS:
        case = _load_yaml(
            REPO_ROOT / "eval" / "fixtures" / case_id / "case.yaml"
        )
        command = shlex.split(case["test_command"])
        if command[0] == "python":
            command[0] = sys.executable

        result = subprocess.run(
            command,
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, (
            f"{case_id}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )


def test_prepare_all_triage_workspaces_hides_ground_truth(tmp_path: Path) -> None:
    output_root = tmp_path / "triage"
    result = subprocess.run(
        [
            sys.executable,
            "scripts/prepare_triage_workspace.py",
            "--all",
            "--output-root",
            str(output_root),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr

    for case_id in CASE_IDS:
        workspace = output_root / case_id
        context = _load_yaml(workspace / "MERGEPROOF_RUN_CONTEXT.yaml")

        assert context["case_id"] == case_id
        assert context["run_id"].startswith(f"mergeproof-{case_id.lower()}-")
        assert context["changed_files"]
        assert context["source_ids"]
        assert context["bob_mode_version"] == "1.0.0"
        assert context["skill_version"] == "1.0.0"
        assert context["report_schema_version"] == "1.0"

        assert not (workspace / "eval" / "expected").exists()
        assert not (
            workspace
            / "docs/05_PREPRODUCTION/02_TRIAGE_ACCEPTANCE"
        ).exists()

        fixture_root = workspace / "eval" / "fixtures"
        assert sorted(path.name for path in fixture_root.iterdir()) == [case_id]


def _synthetic_report(
    case_id: str,
    workspace: Path,
    expectation: TriageExpectation,
    context: dict,
) -> MergeProofReport:
    case = _load_yaml(workspace / "eval" / "fixtures" / case_id / "case.yaml")
    source_artifact = case["source_files"][0]
    repo_artifact = case["changed_files"][0]

    sources = [
        {
            "source_id": source_id,
            "source_type": "PRD",
            "location": source_artifact,
            "authority": "fixture",
            "state": "ACTIVE",
            "scope": list(case["changed_files"]),
        }
        for source_id in context["source_ids"]
    ]

    payload = {
        "report_version": context["report_schema_version"],
        "run_id": context["run_id"],
        "advisory": expectation.advisory.value,
        "repository": {
            "commit_sha": context["repository_commit_sha"],
            "changed_files": context["changed_files"],
        },
        "sources": sources,
        "findings": [
            {
                "finding_id": f"{case_id}-F-001",
                "finding_class": expectation.finding_class.value,
                "finding_type": expectation.finding_type.value,
                "title": "Synthetic evaluator self-test",
                "evidence_grade": "DIRECT",
                "severity": expectation.severity.value,
                "repo_anchors": [
                    {
                        "artifact": repo_artifact,
                        "locator": "synthetic evaluator self-test",
                    }
                ],
                "source_anchors": [
                    {
                        "artifact": source_artifact,
                        "locator": "synthetic evaluator self-test",
                    }
                ],
                "rationale": "Used only to verify the deterministic Block 5 evaluator.",
            }
        ],
        "generated_at": context["timestamp"],
    }
    return MergeProofReport.model_validate(payload)


def test_triage_evaluator_accepts_all_frozen_expected_tuples(tmp_path: Path) -> None:
    output_root = tmp_path / "triage"
    result = subprocess.run(
        [
            sys.executable,
            "scripts/prepare_triage_workspace.py",
            "--all",
            "--output-root",
            str(output_root),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr

    for case_id in CASE_IDS:
        workspace = output_root / case_id
        context = _load_yaml(workspace / "MERGEPROOF_RUN_CONTEXT.yaml")
        expected_payload = _load_yaml(
            REPO_ROOT / "eval" / "expected" / f"{case_id}.yaml"
        )
        expectation = TriageExpectation.from_mapping(expected_payload)
        report = _synthetic_report(case_id, workspace, expectation, context)

        assert evaluate_triage_report(
            report,
            expectation,
            context,
            workspace,
        ) == []


def test_triage_evaluator_rejects_wrong_advisory(tmp_path: Path) -> None:
    case_id = "TRIAGE-001"
    output_root = tmp_path / "triage"
    result = subprocess.run(
        [
            sys.executable,
            "scripts/prepare_triage_workspace.py",
            "--case",
            case_id,
            "--output-root",
            str(output_root),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr

    workspace = output_root / case_id
    context = _load_yaml(workspace / "MERGEPROOF_RUN_CONTEXT.yaml")
    expectation = TriageExpectation.from_mapping(
        _load_yaml(REPO_ROOT / "eval" / "expected" / f"{case_id}.yaml")
    )
    report = _synthetic_report(case_id, workspace, expectation, context)
    payload = json.loads(report.model_dump_json())
    payload["advisory"] = "PASS"
    wrong = MergeProofReport.model_validate(payload)

    codes = {
        issue.code
        for issue in evaluate_triage_report(
            wrong,
            expectation,
            context,
            workspace,
        )
    }
    assert "ADVISORY_MISMATCH" in codes
