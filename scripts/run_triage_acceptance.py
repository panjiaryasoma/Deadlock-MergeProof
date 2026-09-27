from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CASE_IDS = tuple(f"TRIAGE-{index:03d}" for index in range(1, 9))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run frozen TRIAGE acceptance across eight captured Bob reports."
    )
    parser.add_argument(
        "--reports-dir",
        type=Path,
        default=REPO_ROOT / "reports" / "triage",
    )
    parser.add_argument(
        "--workspaces-dir",
        type=Path,
        default=REPO_ROOT / "build" / "triage",
    )
    args = parser.parse_args()

    passed = 0
    failed = 0
    pending = 0

    for case_id in CASE_IDS:
        report = args.reports_dir / f"{case_id}.json"
        workspace = args.workspaces_dir / case_id

        if not report.is_file() or not workspace.is_dir():
            print(f"[PENDING] {case_id}: report/workspace missing")
            pending += 1
            continue

        result = subprocess.run(
            [
                sys.executable,
                "scripts/evaluate_triage_report.py",
                "--case",
                case_id,
                "--report",
                str(report),
                "--workspace",
                str(workspace),
            ],
            cwd=REPO_ROOT,
            check=False,
        )
        if result.returncode == 0:
            passed += 1
        else:
            failed += 1

    print(
        f"TRIAGE summary: passed={passed} failed={failed} pending={pending} total=8"
    )
    return 0 if passed == 8 and failed == 0 and pending == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
