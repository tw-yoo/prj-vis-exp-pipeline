"""Utility: build request body for POST /annotate_chart_image.

Usage:
    from opsspec.modules.module_annotation_request_builder import build_annotate_chart_request

    body = build_annotate_chart_request(
        chart_id="0egdxqun1m2n9k4z",
        question="How many years are above the average?",
        explanation="1. Find average\\n2. filter which countries are above the average",
        image_path="path/to/chart.png",
        server_url="http://localhost:3000",
    )
    # → POST /annotate_chart_image with body

Pipeline:
  1. load_chartqa_case(chart_id)           → vega_lite_spec, data_rows
  2. image_path → base64 PNG
  3. POST /generate_vegalite_annotation_baseline  → step_specs[].computed_values
  4. computed_values  →  AnnotationItem list  (heuristic mapper)
  5. vega_lite_spec + data_rows  →  chart_area (pixel bounds + data range)
  6. assemble final request body dict

The lower-level `build_annotate_request_from_baseline` is also exported for
callers that already have the baseline result and want to skip the HTTP call.
"""
from __future__ import annotations

import base64
import json
import logging
import re
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from ..runtime.context_builder import build_chart_context
from ..tests.comparators import load_chartqa_case

logger = logging.getLogger(__name__)

# ── Vega-Lite default rendering geometry ──────────────────────────────────────
# When vl-convert renders a Vega-Lite spec without explicit dimensions,
# these defaults are used.  Override via chart_area_overrides.
_VL_DEFAULT_WIDTH = 200        # plot area width  (px)
_VL_DEFAULT_HEIGHT = 200       # plot area height (px)
_VL_PAD_LEFT = 50              # y-axis labels
_VL_PAD_TOP = 20               # title / top margin
_VL_PAD_RIGHT = 20             # right margin
_VL_PAD_BOTTOM = 40            # x-axis labels


# ── Image loading ─────────────────────────────────────────────────────────────

def _load_image_base64(image_path: str | Path) -> str:
    """Read a PNG from disk and return a base64-encoded string."""
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Chart image not found: {path}")
    raw = path.read_bytes()
    return base64.b64encode(raw).decode("utf-8")


# ── Chart area inference ──────────────────────────────────────────────────────

def _infer_chart_area(
    vega_lite_spec: Dict[str, Any],
    data_rows: List[Dict[str, Any]],
    chart_context: Any,
    *,
    overrides: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Infer pixel chart_area from a Vega-Lite spec + data.

    Assumes vl-convert default rendering:
      - plot area (x, y, width, height) = spec width/height + standard padding
      - y range = [0, max(measure) * 1.1]  (bar charts start at 0)
      - x_categories = ordered unique values of the primary dimension
    """
    spec_width = int(vega_lite_spec.get("width") or _VL_DEFAULT_WIDTH)
    spec_height = int(vega_lite_spec.get("height") or _VL_DEFAULT_HEIGHT)

    # y data range
    measure = chart_context.primary_measure
    y_values: List[float] = []
    for row in data_rows:
        raw = row.get(measure)
        if raw is not None:
            try:
                y_values.append(float(raw))
            except (ValueError, TypeError):
                pass
    y_min = 0.0
    y_max = (max(y_values) * 1.1) if y_values else 100.0

    # x categories (keep original order from data)
    dimension = chart_context.primary_dimension
    seen: Dict[str, None] = {}
    for row in data_rows:
        v = row.get(dimension)
        if v is not None:
            seen[str(v)] = None
    x_categories = list(seen.keys())

    area: Dict[str, Any] = {
        "x": _VL_PAD_LEFT,
        "y": _VL_PAD_TOP,
        "width": spec_width,
        "height": spec_height,
        "y_min": y_min,
        "y_max": round(y_max, 4),
        "x_categories": x_categories,
    }

    if overrides:
        area.update(overrides)

    return area


# ── computed_values → AnnotationItem list ─────────────────────────────────────

def _fmt_key(key: str) -> str:
    """Convert snake_case / camelCase key to a readable label."""
    # insert space before uppercase (camelCase) then replace underscores
    s = re.sub(r"([a-z])([A-Z])", r"\1 \2", key)
    return s.replace("_", " ").title()


def _is_numeric(val: Any) -> bool:
    return isinstance(val, (int, float)) and not isinstance(val, bool)


def _looks_like_category_list(
    val: Any, x_categories: List[str]
) -> bool:
    """Return True if val is a list of strings that overlap with x_categories."""
    if not isinstance(val, list) or not val:
        return False
    if not all(isinstance(v, (str, int, float)) for v in val):
        return False
    cat_set = set(x_categories)
    return any(str(v) in cat_set for v in val)


def _map_computed_values_to_annotations(
    computed_values: Dict[str, Any],
    x_categories: List[str],
    colors: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    """Heuristically map LLM-produced computed_values to AnnotationItem dicts.

    Heuristics:
      numeric value          → reference_line (+ text label if key is "average" etc.)
      list of strings/nums
        ∩ x_categories ≠ ∅  → highlight_bar  (keep matched categories)
      dict {lower, upper}   → band
      int count-like key     → ignored (not a visual element on its own)
    """
    if colors is None:
        colors = ["#e45756", "#4c78a8", "#f58518", "#54a24b"]

    annotations: List[Dict[str, Any]] = []
    color_idx = 0

    # Collect reference lines first (so they're drawn before bars)
    for key, val in computed_values.items():
        if not _is_numeric(val):
            continue
        key_lower = key.lower()
        # Skip pure count values — they don't map to a y-axis position
        if any(w in key_lower for w in ("count", "num_", "number", "n_", "total")):
            continue
        color = colors[color_idx % len(colors)]
        color_idx += 1
        label = f"{_fmt_key(key)}: {val}"
        annotations.append({
            "type": "reference_line",
            "value": float(val),
            "label": label,
            "color": color,
        })

    # Then highlight_bar / band
    for key, val in computed_values.items():
        if isinstance(val, dict):
            lower = val.get("lower") or val.get("y_lower") or val.get("min")
            upper = val.get("upper") or val.get("y_upper") or val.get("max")
            if lower is not None and upper is not None:
                color = colors[color_idx % len(colors)]
                color_idx += 1
                annotations.append({
                    "type": "band",
                    "y_lower": float(lower),
                    "y_upper": float(upper),
                    "color": color,
                    "opacity": 0.15,
                })

        elif _looks_like_category_list(val, x_categories):
            matched = [str(v) for v in val if str(v) in set(x_categories)]
            if matched:
                annotations.append({
                    "type": "highlight_bar",
                    "categories": matched,
                    "highlight_color": "#e45756",
                    "dim_color": "#d3d3d3",
                    "dim_opacity": 0.55,
                })

    return annotations


# ── HTTP helper ───────────────────────────────────────────────────────────────

def _post_json(url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Simple urllib POST → JSON (no extra deps)."""
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"POST {url} failed: HTTP {exc.code}  {body[:300]}"
        ) from exc


# ── Low-level builder (takes baseline result directly) ───────────────────────

def build_annotate_request_from_baseline(
    *,
    image_path: str | Path,
    baseline_result: Dict[str, Any],
    vega_lite_spec: Dict[str, Any],
    data_rows: List[Dict[str, Any]],
    return_each_step: bool = True,
    chart_area_overrides: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Build /annotate_chart_image body from an already-computed baseline result.

    Args:
        image_path:        Path to the base chart PNG.
        baseline_result:   Response from POST /generate_vegalite_annotation_baseline.
                           Expected shape: { step_specs: [{sentenceIndex, sentence,
                           annotated_spec, layers_added, computed_values}], warnings }
        vega_lite_spec:    Original Vega-Lite spec (used for chart_area inference).
        data_rows:         CSV data rows as list of dicts.
        return_each_step:  If True, return one image per step.
        chart_area_overrides: Partial dict to override inferred chart_area fields.

    Returns:
        dict ready to POST to /annotate_chart_image
    """
    chart_context, _warnings, _preview = build_chart_context(vega_lite_spec, data_rows)

    image_base64 = _load_image_base64(image_path)

    chart_area = _infer_chart_area(
        vega_lite_spec, data_rows, chart_context, overrides=chart_area_overrides
    )

    step_specs: List[Dict[str, Any]] = baseline_result.get("step_specs") or []
    steps: List[Dict[str, Any]] = []

    for step in step_specs:
        computed_values = step.get("computed_values") or {}
        annotations = _map_computed_values_to_annotations(
            computed_values, chart_area["x_categories"]
        )
        steps.append({
            "sentence": step.get("sentence", ""),
            "annotations": annotations,
        })

    return {
        "image_base64": image_base64,
        "chart_area": chart_area,
        "steps": steps,
        "return_each_step": return_each_step,
    }


# ── High-level builder (full pipeline) ───────────────────────────────────────

def build_annotate_chart_request(
    chart_id: str,
    question: str,
    explanation: str,
    image_path: str | Path,
    *,
    server_url: str = "http://localhost:3000",
    return_each_step: bool = True,
    chart_area_overrides: Optional[Dict[str, Any]] = None,
    debug: bool = False,
) -> Dict[str, Any]:
    """Build request body for POST /annotate_chart_image.

    This is the single entry point for the full pipeline:
      chart_id + question + explanation + image_path
        → calls /generate_vegalite_annotation_baseline
        → assembles /annotate_chart_image request body

    Args:
        chart_id:             ChartQA chart identifier (e.g. "0egdxqun1m2n9k4z").
        question:             Chart question string.
        explanation:          Step-by-step explanation string.
        image_path:           Path to the rendered chart PNG.
        server_url:           Base URL of the running nlp_server.
        return_each_step:     Whether to request one image per step.
        chart_area_overrides: Override specific chart_area fields (e.g. {"x": 55}).
        debug:                Pass debug=True to the baseline API call.

    Returns:
        dict ready to POST to /annotate_chart_image.
        Also includes "_meta" key with intermediate info (stripped before posting).

    Raises:
        FileNotFoundError: if chart_id files or image_path are not found.
        RuntimeError:      if the baseline API call fails.

    Example::

        body = build_annotate_chart_request(
            chart_id="0egdxqun1m2n9k4z",
            question="How many years are above the average?",
            explanation="1. Find average\\n2. filter which countries are above the average",
            image_path="ChartQA/used_for_study/bar/simple/0egdxqun1m2n9k4z.png",
        )
        # strip internal metadata before posting
        clean = {k: v for k, v in body.items() if not k.startswith("_")}
        # → POST /annotate_chart_image with clean
    """
    # ── Step 1: load chart data ───────────────────────────────────────────────
    logger.info("[build_annotate_request] loading ChartQA data | chart_id=%s", chart_id)
    vega_lite_spec, data_rows = load_chartqa_case(chart_id)

    # ── Step 2: call baseline annotation API ─────────────────────────────────
    baseline_url = f"{server_url.rstrip('/')}/generate_vegalite_annotation_baseline"
    logger.info("[build_annotate_request] calling baseline API | url=%s", baseline_url)
    baseline_payload: Dict[str, Any] = {
        "question": question,
        "explanation": explanation,
        "vega_lite_spec": vega_lite_spec,
        "data_rows": data_rows,
        "debug": debug,
    }
    baseline_result = _post_json(baseline_url, baseline_payload)
    logger.info(
        "[build_annotate_request] baseline done | steps=%d warnings=%d",
        len(baseline_result.get("step_specs") or []),
        len(baseline_result.get("warnings") or []),
    )

    # ── Step 3: assemble PIL annotation request body ──────────────────────────
    body = build_annotate_request_from_baseline(
        image_path=image_path,
        baseline_result=baseline_result,
        vega_lite_spec=vega_lite_spec,
        data_rows=data_rows,
        return_each_step=return_each_step,
        chart_area_overrides=chart_area_overrides,
    )

    # Attach metadata for debugging (caller strips before posting)
    body["_meta"] = {
        "chart_id": chart_id,
        "question": question,
        "baseline_warnings": baseline_result.get("warnings") or [],
        "step_summaries": [
            {
                "sentenceIndex": s.get("sentenceIndex"),
                "sentence": s.get("sentence"),
                "computed_values": s.get("computed_values"),
                "layers_added": s.get("layers_added"),
            }
            for s in (baseline_result.get("step_specs") or [])
        ],
    }

    return body
