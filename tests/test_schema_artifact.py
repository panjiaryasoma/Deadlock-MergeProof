import json
from pathlib import Path

from mergeproof.models import MergeProofReport

SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schemas" / "mergeproof_report.schema.json"


def test_checked_in_json_schema_matches_runtime_model() -> None:
    checked_in = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    assert checked_in == MergeProofReport.model_json_schema()
