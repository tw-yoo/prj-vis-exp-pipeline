from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


def _project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _find_unique_chartqa_file(base_dir: Path, chart_id: str, suffix: str) -> Path:
    candidates = sorted(base_dir.glob(f"**/{chart_id}{suffix}"))
    if not candidates:
        raise FileNotFoundError(f"ChartQA file not found: chart_id={chart_id}, suffix={suffix}")
    if len(candidates) > 1:
        joined = ", ".join(str(path) for path in candidates[:3])
        if len(candidates) > 3:
            joined += ", ..."
        raise ValueError(
            f"Multiple ChartQA files found for chart_id={chart_id}, suffix={suffix}: {joined}"
        )
    return candidates[0]


def resolve_chartqa_case_paths(chart_id: str, *, root: Path | None = None) -> tuple[Path, Path]:
    normalized_id = str(chart_id).strip()
    if not normalized_id:
        raise ValueError("chart_id is empty.")

    project_root = (root or _project_root()).resolve()
    spec_root = project_root / "ChartQA" / "data" / "vlSpec"
    csv_root = project_root / "ChartQA" / "data" / "csv"

    spec_path = _find_unique_chartqa_file(spec_root, normalized_id, ".json")
    csv_path = _find_unique_chartqa_file(csv_root, normalized_id, ".csv")
    return spec_path, csv_path


def load_chartqa_case(chart_id: str, *, root: Path | None = None) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    spec_path, csv_path = resolve_chartqa_case_paths(chart_id, root=root)

    vega_lite_spec = json.loads(spec_path.read_text(encoding="utf-8"))
    if not isinstance(vega_lite_spec, dict):
        raise ValueError(f"ChartQA Vega-Lite spec must be a JSON object: {spec_path}")

    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        data_rows = list(csv.DictReader(handle))
    return vega_lite_spec, data_rows
