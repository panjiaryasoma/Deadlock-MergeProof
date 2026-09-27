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


def _prepare(case_id: str, output_root: Path) -> Path:
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
    return output_root / case_id


def _workspace_case(workspace: Path, case_id: str) -> dict:
    return _load_yaml(workspace / "eval" / "fixtures" / case_id / "case.yaml")


def _workspace_registry(workspace: Path, case_id: str) -> list[dict]:
    case = _workspace_case(workspace, case_id)
    registry = _load_yaml(workspace / case["source_registry"])
    sources = registry["sources"]
    assert isinstance(sources, list)
    return sources


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

        paths = [
            *case["source_files"],
            *case["changed_files"],
            case["application_entrypoint"],
            case["source_registry"],
        ]
        if "change_evidence" in case:
            paths.append(case["change_evidence"])

        for raw_path in paths:
            assert (REPO_ROOT / raw_path).is_file(), raw_path

        visible_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in root.rglob("*")
            if path.is_file()
            and path.suffix in {".md", ".patch", ".py", ".yaml", ".yml", ".txt"}
        )
        for key in ("finding_class", "finding_type", "advisory"):
            assert expected[key] not in visible_text


def test_source_registries_match_case_files_and_visible_metadata() -> None:
    for case_id in CASE_IDS:
        root = REPO_ROOT / "eval" / "fixtures" / case_id
        case = _load_yaml(root / "case.yaml")
        registry = _load_yaml(REPO_ROOT / case["source_registry"])
        sources = registry["sources"]

        assert [source["location"] for source in sources] == case["source_files"]
        assert len({source["source_id"] for source in sources}) == len(sources)

        for source in sources:
            source_text = (REPO_ROOT / source["location"]).read_text(encoding="utf-8")
            for field in ("source_id", "source_type", "state", "authority"):
                assert str(source[field]) in source_text
            for scope_path in source["scope"]:
                assert scope_path in source_text
            for superseded_id in source.get("supersedes") or []:
                assert superseded_id in source_text


def test_triage_006_uses_equal_precedence_conflicting_sources() -> None:
    root = REPO_ROOT / "eval" / "fixtures" / "TRIAGE-006"
    case = _load_yaml(root / "case.yaml")
    sources = _load_yaml(REPO_ROOT / case["source_registry"])["sources"]

    assert [source["source_type"] for source in sources] == ["ADR", "ADR"]
    assert [source["state"] for source in sources] == ["ACTIVE", "ACTIVE"]
    assert sources[0]["scope"] == sources[1]["scope"]
    assert all(source["supersedes"] is None for source in sources)

    correction = (
        REPO_ROOT
        / "docs/05_PREPRODUCTION/02_TRIAGE_ACCEPTANCE/"
        "FIXTURE_CONSISTENCY_CORRECTIONS.md"
    ).read_text(encoding="utf-8")
    assert "before measured Block 5 IBM Bob runs" in correction
    assert "No frozen TRIAGE expected tuple changed" in correction


def test_domain_rules_resolve_ambiguity_and_best_practice_severity() -> None:
    rules = _load_yaml(
        REPO_ROOT / "docs/03_EVALUATION_AND_DOMAIN_RULES/domain_rules_v1.0.yaml"
    )["rules"]
    by_id = {rule["id"]: rule for rule in rules}

    assert by_id["DR-011"]["then"]["severity"] == "NONE"
    assert by_id["DR-012"]["then"]["severity"] == "MEDIUM"


def test_triage_003_has_explicit_change_evidence() -> None:
    root = REPO_ROOT / "eval" / "fixtures" / "TRIAGE-003"
    case = _load_yaml(root / "case.yaml")
    patch = (REPO_ROOT / case["change_evidence"]).read_text(encoding="utf-8")

    assert "-def _normalize" in patch
    assert "+def _canonicalize" in patch


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
        assert context["source_registry"]
        assert context["bob_mode_version"] == "1.0.0"
        assert context["skill_version"] == "1.0.2"
        assert context["report_schema_version"] == "1.0"
        assert (workspace / context["source_registry"]).is_file()

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
    case = _workspace_case(workspace, case_id)
    sources = _workspace_registry(workspace, case_id)
    repo_artifact = case["changed_files"][0]

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
                        "locator": "line 1",
                    }
                ],
                "source_anchors": [
                    {
                        "artifact": source["location"],
                        "locator": "line 1",
                    }
                    for source in sources
                ],
                "rationale": "Used only to verify the deterministic Block 5 evaluator.",
            }
        ],
        "generated_at": context["timestamp"],
    }
    return MergeProofReport.model_validate(payload)


def _evaluation_codes(
    report: MergeProofReport,
    expectation: TriageExpectation,
    context: dict,
    workspace: Path,
) -> set[str]:
    return {
        issue.code
        for issue in evaluate_triage_report(
            report,
            expectation,
            context,
            workspace,
        )
    }


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
        expectation = TriageExpectation.from_mapping(
            _load_yaml(REPO_ROOT / "eval" / "expected" / f"{case_id}.yaml")
        )
        report = _synthetic_report(case_id, workspace, expectation, context)

        assert evaluate_triage_report(
            report,
            expectation,
            context,
            workspace,
        ) == []


def test_triage_evaluator_rejects_wrong_advisory(tmp_path: Path) -> None:
    case_id = "TRIAGE-001"
    workspace = _prepare(case_id, tmp_path / "triage")
    context = _load_yaml(workspace / "MERGEPROOF_RUN_CONTEXT.yaml")
    expectation = TriageExpectation.from_mapping(
        _load_yaml(REPO_ROOT / "eval" / "expected" / f"{case_id}.yaml")
    )
    report = _synthetic_report(case_id, workspace, expectation, context)
    payload = json.loads(report.model_dump_json())
    payload["advisory"] = "PASS"
    wrong = MergeProofReport.model_validate(payload)

    assert "ADVISORY_MISMATCH" in _evaluation_codes(
        wrong,
        expectation,
        context,
        workspace,
    )


def test_triage_evaluator_rejects_source_metadata_drift(tmp_path: Path) -> None:
    case_id = "TRIAGE-008"
    workspace = _prepare(case_id, tmp_path / "triage")
    context = _load_yaml(workspace / "MERGEPROOF_RUN_CONTEXT.yaml")
    expectation = TriageExpectation.from_mapping(
        _load_yaml(REPO_ROOT / "eval" / "expected" / f"{case_id}.yaml")
    )
    report = _synthetic_report(case_id, workspace, expectation, context)
    payload = json.loads(report.model_dump_json())
    payload["sources"][0]["state"] = "ACTIVE"
    wrong = MergeProofReport.model_validate(payload)

    assert "SOURCE_METADATA_MISMATCH" in _evaluation_codes(
        wrong,
        expectation,
        context,
        workspace,
    )


def test_triage_evaluator_validates_anchor_roles_and_locators(tmp_path: Path) -> None:
    case_id = "TRIAGE-001"
    workspace = _prepare(case_id, tmp_path / "triage")
    context = _load_yaml(workspace / "MERGEPROOF_RUN_CONTEXT.yaml")
    expectation = TriageExpectation.from_mapping(
        _load_yaml(REPO_ROOT / "eval" / "expected" / f"{case_id}.yaml")
    )
    report = _synthetic_report(case_id, workspace, expectation, context)

    wrong_role_payload = json.loads(report.model_dump_json())
    wrong_role_payload["findings"][0]["source_anchors"][0] = {
        "artifact": context["changed_files"][0],
        "locator": "line 1",
    }
    wrong_role = MergeProofReport.model_validate(wrong_role_payload)
    assert "SOURCE_ANCHOR_NOT_REGISTERED" in _evaluation_codes(
        wrong_role,
        expectation,
        context,
        workspace,
    )

    bad_locator_payload = json.loads(report.model_dump_json())
    bad_locator_payload["findings"][0]["source_anchors"][0]["locator"] = "banana"
    bad_locator = MergeProofReport.model_validate(bad_locator_payload)
    assert "ANCHOR_LOCATOR_UNRESOLVED" in _evaluation_codes(
        bad_locator,
        expectation,
        context,
        workspace,
    )


def test_source_conflict_requires_both_active_sides(tmp_path: Path) -> None:
    case_id = "TRIAGE-006"
    workspace = _prepare(case_id, tmp_path / "triage")
    context = _load_yaml(workspace / "MERGEPROOF_RUN_CONTEXT.yaml")
    expectation = TriageExpectation.from_mapping(
        _load_yaml(REPO_ROOT / "eval" / "expected" / f"{case_id}.yaml")
    )
    report = _synthetic_report(case_id, workspace, expectation, context)
    payload = json.loads(report.model_dump_json())
    payload["findings"][0]["source_anchors"] = payload["findings"][0]["source_anchors"][:1]
    incomplete = MergeProofReport.model_validate(payload)

    assert "SOURCE_CONFLICT_EVIDENCE_INCOMPLETE" in _evaluation_codes(
        incomplete,
        expectation,
        context,
        workspace,
    )


def test_stale_source_and_best_practice_require_both_evidence_roles(
    tmp_path: Path,
) -> None:
    for case_id, code in (
        ("TRIAGE-007", "BEST_PRACTICE_EVIDENCE_INCOMPLETE"),
        ("TRIAGE-008", "STALE_SOURCE_EVIDENCE_INCOMPLETE"),
    ):
        workspace = _prepare(case_id, tmp_path / case_id)
        context = _load_yaml(workspace / "MERGEPROOF_RUN_CONTEXT.yaml")
        expectation = TriageExpectation.from_mapping(
            _load_yaml(REPO_ROOT / "eval" / "expected" / f"{case_id}.yaml")
        )
        report = _synthetic_report(case_id, workspace, expectation, context)
        payload = json.loads(report.model_dump_json())
        payload["findings"][0]["source_anchors"] = payload["findings"][0][
            "source_anchors"
        ][:1]
        incomplete = MergeProofReport.model_validate(payload)

        assert code in _evaluation_codes(
            incomplete,
            expectation,
            context,
            workspace,
        )


def test_change_evidence_is_allowed_as_relevant_repo_anchor(tmp_path: Path) -> None:
    case_id = "TRIAGE-003"
    workspace = _prepare(case_id, tmp_path / "triage")
    context = _load_yaml(workspace / "MERGEPROOF_RUN_CONTEXT.yaml")
    expectation = TriageExpectation.from_mapping(
        _load_yaml(REPO_ROOT / "eval" / "expected" / f"{case_id}.yaml")
    )
    report = _synthetic_report(case_id, workspace, expectation, context)
    payload = json.loads(report.model_dump_json())
    case = _workspace_case(workspace, case_id)
    payload["findings"][0]["repo_anchors"] = [
        {
            "artifact": case["change_evidence"],
            "locator": "line 1",
        }
    ]
    anchored = MergeProofReport.model_validate(payload)
    codes = _evaluation_codes(anchored, expectation, context, workspace)

    assert "REPO_ANCHOR_OUTSIDE_EVALUATED_SCOPE" not in codes
    assert "ANCHOR_LOCATOR_UNRESOLVED" not in codes


def test_finding_type_policy_prefers_specific_boundary_drift() -> None:
    rules = _load_yaml(
        REPO_ROOT / "docs/03_EVALUATION_AND_DOMAIN_RULES/domain_rules_v1.0.yaml"
    )
    policy = rules["finding_type_selection"]

    assert policy["policy"] == "MOST_SPECIFIC_SUPPORTED_TYPE_WINS"
    assert policy["precedence"].index("BOUNDARY_CONDITION_DRIFT") < policy[
        "precedence"
    ].index("REQUIREMENT_IMPLEMENTATION_MISMATCH")
    assert "comparison operators differ" in " ".join(
        policy["rules"]["BOUNDARY_CONDITION_DRIFT"]["when"]
    )
    assert "no more specific finding type above applies" in " ".join(
        policy["rules"]["REQUIREMENT_IMPLEMENTATION_MISMATCH"]["when"]
    )


def test_successful_report_transport_is_raw_json_only() -> None:
    synthesis = (
        REPO_ROOT / ".bob/skills/report-synthesis/SKILL.md"
    ).read_text(encoding="utf-8")
    orchestrator = (
        REPO_ROOT / ".bob/skills/mergeproof/SKILL.md"
    ).read_text(encoding="utf-8")

    for text in (synthesis, orchestrator):
        assert "start with" in text.lower()
        assert "end with" in text.lower()
        assert "code fence" in text.lower()

    assert "introductory sentence" in synthesis


def test_prepare_recovers_interrupted_generated_workspace_without_marker(
    tmp_path: Path,
) -> None:
    output_root = tmp_path / "triage"
    partial = output_root / "TRIAGE-001"
    (partial / "docs").mkdir(parents=True)
    (partial / "eval").mkdir()
    (partial / "schemas").mkdir()

    result = subprocess.run(
        [
            sys.executable,
            "scripts/prepare_triage_workspace.py",
            "--case",
            "TRIAGE-001",
            "--output-root",
            str(output_root),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert (partial / ".mergeproof-triage-workspace").is_file()
    assert (partial / "MERGEPROOF_RUN_CONTEXT.yaml").is_file()


def test_prepare_refuses_markerless_workspace_with_unknown_content(
    tmp_path: Path,
) -> None:
    output_root = tmp_path / "triage"
    unsafe = output_root / "TRIAGE-001"
    unsafe.mkdir(parents=True)
    (unsafe / "do-not-delete.txt").write_text("user data\n", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/prepare_triage_workspace.py",
            "--case",
            "TRIAGE-001",
            "--output-root",
            str(output_root),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode != 0
    assert "unexpected entries exist" in result.stderr
    assert (unsafe / "do-not-delete.txt").is_file()


def test_custom_mode_forbids_user_visible_workflow_narration() -> None:
    mode = (
        REPO_ROOT / ".bob/custom_modes.yaml"
    ).read_text(encoding="utf-8")
    rule = (
        REPO_ROOT / ".bob/rules-mergeproof/07-final-output-transport.md"
    ).read_text(encoding="utf-8")

    for text in (mode, rule):
        lowered = text.lower()
        assert "intermediate" in lowered
        assert "raw json" in lowered
        assert "code fence" in lowered

    assert "never narrate stage headings" in mode
    assert "first non-whitespace character" in mode
    assert "progress messages" in rule


def test_triage_evaluator_accepts_bob_colon_line_locators(tmp_path: Path) -> None:
    case_id = "TRIAGE-001"
    workspace = _prepare(case_id, tmp_path / "triage")
    context = _load_yaml(workspace / "MERGEPROOF_RUN_CONTEXT.yaml")
    expectation = TriageExpectation.from_mapping(
        _load_yaml(REPO_ROOT / "eval" / "expected" / f"{case_id}.yaml")
    )
    report = _synthetic_report(case_id, workspace, expectation, context)
    payload = json.loads(report.model_dump_json())

    payload["findings"][0]["source_anchors"][0]["locator"] = "line:14"
    payload["findings"][0]["repo_anchors"][0]["locator"] = "line:7"
    payload["findings"][0]["test_anchors"] = [
        {
            "artifact": "eval/fixtures/TRIAGE-001/tests.py",
            "locator": "line:13-17",
        }
    ]

    bob_style = MergeProofReport.model_validate(payload)
    codes = _evaluation_codes(
        bob_style,
        expectation,
        context,
        workspace,
    )

    assert "ANCHOR_LOCATOR_UNRESOLVED" not in codes


def test_triage_evaluator_accepts_patch_hunk_locator(tmp_path: Path) -> None:
    case_id = "TRIAGE-003"
    workspace = _prepare(case_id, tmp_path / "triage")
    context = _load_yaml(workspace / "MERGEPROOF_RUN_CONTEXT.yaml")
    expectation = TriageExpectation.from_mapping(
        _load_yaml(REPO_ROOT / "eval" / "expected" / f"{case_id}.yaml")
    )
    report = _synthetic_report(case_id, workspace, expectation, context)
    payload = json.loads(report.model_dump_json())
    case = _workspace_case(workspace, case_id)

    payload["findings"][0]["repo_anchors"].append(
        {
            "artifact": case["change_evidence"],
            "locator": "@@",
        }
    )

    bob_style = MergeProofReport.model_validate(payload)
    codes = _evaluation_codes(
        bob_style,
        expectation,
        context,
        workspace,
    )

    assert "ANCHOR_LOCATOR_UNRESOLVED" not in codes
