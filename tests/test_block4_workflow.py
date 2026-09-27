from __future__ import annotations

import subprocess
import sys
from datetime import datetime
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def test_orchestrator_implements_block4_sequence() -> None:
    skill = _read(".bob/skills/mergeproof/SKILL.md")

    required_markers = (
        "MERGEPROOF_RUN_CONTEXT.yaml",
        "source-authority",
        "requirement-trace",
        "implementation-observation",
        "test-acceptance-audit",
        "Optionally delegate",
        "evidence-classification",
        "report-synthesis",
        "exactly one JSON object",
        "schemas/mergeproof_report.schema.json",
    )

    for marker in required_markers:
        assert marker in skill


def test_report_synthesis_is_schema_only() -> None:
    synthesis = _read(".bob/skills/report-synthesis/SKILL.md")

    assert "Return exactly one JSON object" in synthesis
    assert "repository.commit_sha" in synthesis
    assert "repository.changed_files" in synthesis
    assert "Preserve project-specific `source.authority` strings exactly" in synthesis
    assert "Human-readable output order" not in synthesis


def test_source_authority_separates_project_value_from_resolution_state() -> None:
    skill = _read(".bob/skills/source-authority/SKILL.md")

    assert "preserves the repository-declared authority" in skill
    assert "analysis metadata only" in skill
    assert "Do not replace" in skill


def test_isolated_severity_workflow_does_not_require_hidden_triage_fixtures() -> None:
    skill = _read(".bob/skills/severity-impact/SKILL.md")
    rule = _read(".bob/rules-mergeproof/05-severity.md")

    assert "not required for severity resolution" in skill
    assert "must not depend on fixture files" in rule


def test_demo_run_context_is_grounded_and_workspace_local(tmp_path: Path) -> None:
    output = tmp_path / "demo-workspace"
    result = subprocess.run(
        [
            sys.executable,
            "scripts/prepare_demo_workspace.py",
            "--output",
            str(output),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr

    context = yaml.safe_load(
        (output / "MERGEPROOF_RUN_CONTEXT.yaml").read_text(encoding="utf-8")
    )
    expected_sha = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()

    assert context["repository_commit_sha"] == expected_sha
    assert context["run_id"].startswith(f"mergeproof-{expected_sha[:12]}-")
    assert context["changed_files"] == [
        "demo/src/deadline.py",
        "demo/tests/test_deadline.py",
    ]
    assert context["source_ids"] == ["SRC-PRD-001"]
    assert context["bob_mode_version"] == "1.0.0"
    assert context["skill_version"] == "1.0.1"
    assert context["report_schema_version"] == "1.0"
    assert datetime.fromisoformat(context["timestamp"].replace("Z", "+00:00"))
    assert context["case_descriptor"] == "demo/case.yaml"
    assert (output / context["case_descriptor"]).is_file()
    assert (output / context["report_schema"]).is_file()
    assert (output / context["domain_rules"]).is_file()
    assert (output / context["output_contract_addendum"]).is_file()
    assert (output / ".bob/manifest.yaml").is_file()


def test_demo_bob_prompt_does_not_reveal_expected_outcome() -> None:
    prompt = _read("demo/BOB_RUN.md")

    forbidden = (
        "BOUNDARY_CONDITION_DRIFT",
        "MISSING_ACCEPTANCE_TEST",
        "REVIEW_REQUIRED",
        "CONFIRMED_ISSUE",
    )
    for token in forbidden:
        assert token not in prompt


def test_active_output_addendum_resolves_json_summary_stage_conflict() -> None:
    addendum = _read(
        "docs/05_PREPRODUCTION/01_CONTRACTS_ACTIVE/"
        "OUTPUT_AND_RUN_RECORD_ADDENDUM_v1.1.md"
    )

    assert "Blocks 4 through 6" in addendum
    assert "FR-014 remains an MVP release requirement" in addendum
    assert "Block 7" in addendum
    assert "MUST NOT introduce additional findings" in addendum


def test_report_synthesis_uses_grounded_run_context_fields() -> None:
    synthesis = _read(".bob/skills/report-synthesis/SKILL.md")

    for field in (
        "run_id",
        "repository_commit_sha",
        "changed_files",
        "source_ids",
        "bob_mode_version",
        "skill_version",
        "timestamp",
        "report_schema_version",
    ):
        assert field in synthesis

    assert "workflow setup error" in synthesis
