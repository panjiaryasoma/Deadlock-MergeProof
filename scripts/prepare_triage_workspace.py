from __future__ import annotations

import argparse
import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "build" / "triage"
MARKER = ".mergeproof-triage-workspace"
RUN_CONTEXT = "MERGEPROOF_RUN_CONTEXT.yaml"
CASE_IDS = tuple(f"TRIAGE-{index:03d}" for index in range(1, 9))
BOB_MANIFEST = Path(".bob/manifest.yaml")
FEATURE_SCHEMA = Path(
    "docs/05_PREPRODUCTION/01_CONTRACTS_ACTIVE/FEATURE_SCHEMA_FINAL.yaml"
)
OUTPUT_ADDENDUM = Path(
    "docs/05_PREPRODUCTION/01_CONTRACTS_ACTIVE/"
    "OUTPUT_AND_RUN_RECORD_ADDENDUM_v1.1.md"
)

COMMON_PATHS = (
    Path(".bob"),
    Path("docs/03_EVALUATION_AND_DOMAIN_RULES/domain_rules_v1.0.yaml"),
    FEATURE_SCHEMA,
    OUTPUT_ADDENDUM,
    Path("schemas/mergeproof_report.schema.json"),
)

SOURCE_KEYS = {
    "source_id",
    "source_type",
    "location",
    "authority",
    "state",
    "scope",
    "supersedes",
}


def _git_head() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    sha = result.stdout.strip()
    if result.returncode != 0 or not sha:
        raise RuntimeError("Unable to resolve repository commit SHA.")
    return sha


def _load_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load((REPO_ROOT / path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError(f"Expected mapping in {path}.")
    return payload


def _case_root(case_id: str) -> Path:
    return Path("eval") / "fixtures" / case_id


def _case_descriptor(case_id: str) -> Path:
    return _case_root(case_id) / "case.yaml"


def _validate_under_case_root(case_id: str, raw_path: str) -> Path:
    root = _case_root(case_id)
    relative = Path(raw_path)
    try:
        relative.relative_to(root)
    except ValueError as exc:
        raise RuntimeError(
            f"{case_id} path escapes its fixture root: {raw_path}"
        ) from exc
    if not (REPO_ROOT / relative).is_file():
        raise RuntimeError(f"{case_id} references missing file: {raw_path}")
    return relative


def _source_registry(case_id: str, case: dict[str, Any]) -> list[dict[str, Any]]:
    registry_path = _validate_under_case_root(case_id, str(case["source_registry"]))
    registry = _load_yaml(registry_path)
    sources = registry.get("sources")
    if not isinstance(sources, list) or not sources:
        raise RuntimeError(f"{registry_path} must contain a non-empty sources list.")

    source_ids: list[str] = []
    locations: list[str] = []
    for source in sources:
        if not isinstance(source, dict) or not SOURCE_KEYS.issubset(source):
            raise RuntimeError(f"{registry_path} contains an incomplete source record.")
        source_id = str(source["source_id"])
        if source_id in source_ids:
            raise RuntimeError(f"{registry_path} duplicates source_id {source_id}.")
        source_ids.append(source_id)
        location = str(source["location"])
        _validate_under_case_root(case_id, location)
        locations.append(location)

    if locations != list(case["source_files"]):
        raise RuntimeError(
            f"{case_id} source_registry locations must exactly match source_files."
        )
    return sources


def _validate_case_paths(case_id: str, case: dict[str, Any]) -> list[dict[str, Any]]:
    candidates = [
        *case["source_files"],
        *case["changed_files"],
        case["application_entrypoint"],
        case["source_registry"],
    ]
    if "change_evidence" in case:
        candidates.append(case["change_evidence"])

    for raw_path in candidates:
        _validate_under_case_root(case_id, str(raw_path))

    return _source_registry(case_id, case)


def _copy(source: Path, output: Path) -> None:
    src = REPO_ROOT / source
    dst = output / source
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.is_dir():
        shutil.copytree(src, dst)
    else:
        shutil.copy2(src, dst)


def _reset(output: Path, output_root: Path, case_id: str) -> None:
    if not output.exists():
        return

    expected_output = (output_root / case_id).resolve()
    if output.resolve() != expected_output:
        raise RuntimeError(
            f"Refusing to replace unexpected workspace path: {output}."
        )

    marker = output / MARKER
    if not marker.is_file():
        allowed_partial_entries = {
            ".bob",
            "docs",
            "eval",
            "schemas",
            RUN_CONTEXT,
        }
        actual_entries = {entry.name for entry in output.iterdir()}
        unexpected_entries = sorted(actual_entries - allowed_partial_entries)
        if unexpected_entries:
            raise RuntimeError(
                f"Refusing to recover {output}: generated-workspace marker is missing "
                f"and unexpected entries exist: {unexpected_entries!r}."
            )

    try:
        shutil.rmtree(output)
    except PermissionError as exc:
        raise RuntimeError(
            f"Unable to replace {output}: Windows is still using a file in this "
            "workspace. Close the IBM Bob/VS Code window that has this TRIAGE "
            "folder open, then rerun the preparation command."
        ) from exc


def _prepare(case_id: str, output_root: Path) -> Path:
    descriptor = _case_descriptor(case_id)
    case = _load_yaml(descriptor)
    if case.get("case_id") != case_id:
        raise RuntimeError(f"{descriptor} case_id does not match {case_id}.")
    sources = _validate_case_paths(case_id, case)

    manifest = _load_yaml(BOB_MANIFEST)
    feature_schema = _load_yaml(FEATURE_SCHEMA)
    commit_sha = _git_head()
    timestamp = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    output = (output_root / case_id).resolve()
    _reset(output, output_root, case_id)
    output.mkdir(parents=True, exist_ok=True)
    (output / MARKER).write_text(
        "generated by prepare_triage_workspace.py\n",
        encoding="utf-8",
    )

    for path in COMMON_PATHS:
        _copy(path, output)
    _copy(_case_root(case_id), output)

    context = {
        "workspace_version": "1.1",
        "run_id": f"mergeproof-{case_id.lower()}-{commit_sha[:12]}-"
        f"{timestamp.replace(':', '')}",
        "case_id": case_id,
        "repository_commit_sha": commit_sha,
        "changed_files": list(case["changed_files"]),
        "source_ids": [str(source["source_id"]) for source in sources],
        "bob_mode_version": str(manifest["bob_mode"]["version"]),
        "skill_version": str(manifest["skill"]["version"]),
        "timestamp": timestamp,
        "report_schema_version": str(feature_schema["version"]),
        "case_descriptor": descriptor.as_posix(),
        "source_registry": str(case["source_registry"]),
        "report_schema": "schemas/mergeproof_report.schema.json",
        "domain_rules": "docs/03_EVALUATION_AND_DOMAIN_RULES/domain_rules_v1.0.yaml",
        "output_contract_addendum": OUTPUT_ADDENDUM.as_posix(),
    }
    (output / RUN_CONTEXT).write_text(
        yaml.safe_dump(context, sort_keys=False),
        encoding="utf-8",
    )
    return output


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Prepare isolated IBM Bob workspaces for frozen TRIAGE cases."
    )
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--case", choices=CASE_IDS)
    target.add_argument("--all", action="store_true")
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    args = parser.parse_args()

    cases = CASE_IDS if args.all else (args.case,)
    for case_id in cases:
        output = _prepare(case_id, args.output_root)
        print(f"[PASS] {case_id}: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
