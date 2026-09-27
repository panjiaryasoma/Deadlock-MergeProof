from __future__ import annotations

import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

from demo.src.deadline import is_submission_expired

REPO_ROOT = Path(__file__).resolve().parents[1]
DEMO_ROOT = REPO_ROOT / "demo"


def test_seeded_boundary_behavior_is_present_for_evaluator() -> None:
    deadline = datetime(2026, 9, 27, 12, 0, tzinfo=UTC)

    assert is_submission_expired(deadline, deadline) is False


def test_demo_visible_tree_does_not_contain_expected_labels() -> None:
    forbidden = {
        "CONFIRMED_ISSUE",
        "BOUNDARY_CONDITION_DRIFT",
        "MISSING_ACCEPTANCE_TEST",
        "REVIEW_REQUIRED",
    }

    text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in DEMO_ROOT.rglob("*")
        if path.is_file() and path.suffix in {".md", ".py", ".yaml", ".yml", ".txt"}
    )

    for token in forbidden:
        assert token not in text


def test_demo_tests_are_runnable() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            "demo/tests",
            "-t",
            ".",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr


def test_demo_app_is_runnable() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "demo.app"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "status=OPEN" in result.stdout
    assert "status=EXPIRED" in result.stdout


def test_isolated_workspace_excludes_ground_truth(tmp_path: Path) -> None:
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
    assert (output / ".bob").is_dir()
    assert (output / "demo/docs/submission_requirements.md").is_file()
    assert (
        output
        / "docs/05_PREPRODUCTION/01_CONTRACTS_ACTIVE/FEATURE_SCHEMA_FINAL.yaml"
    ).is_file()
    assert not (output / "eval").exists()
    assert not (output / "docs/05_PREPRODUCTION/02_TRIAGE_ACCEPTANCE").exists()
    assert not (output / "docs/05_PREPRODUCTION/03_INTEGRATION_001").exists()
