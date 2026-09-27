from __future__ import annotations

import json
from pathlib import Path

from mergeproof.models import MergeProofReport

SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schemas" / "mergeproof_report.schema.json"


def render_schema() -> str:
    return json.dumps(MergeProofReport.model_json_schema(), indent=2, sort_keys=True) + "\n"


def main() -> int:
    SCHEMA_PATH.write_text(render_schema(), encoding="utf-8")
    print(f"[PASS] wrote {SCHEMA_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
