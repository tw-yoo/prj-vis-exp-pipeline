from __future__ import annotations

import math
from typing import Any, Dict, Iterable, List, Set

from opsspec.runtime.executor import OpsSpecExecutor
from opsspec.core.models import ChartContext
from opsspec.specs.filter import FilterOp
from opsspec.specs.aggregate import RetrieveValueOp
from opsspec.specs.union import OperationSpec

from .chart_type import ChartKind, derive_chart_kind
from .models import (
    DrawBandOp,
    DrawBandSpec,
    DrawBandStyle,
    DrawClearOp,
    DrawGroupFilterSpec,
    DrawGroupedFilterGroupsOp,
    DrawHighlightOp,
    DrawLineConnectBySpec,
    DrawLineConnectEndpoint,
    DrawLineConnectPanelScalarSpec,
    DrawLineConnectSpec,
    DrawLineHorizontalFromYSpec,
    DrawLineHorizontalSpec,
    DrawLinePanelScalarConnectSpec,
    DrawLinePanelScalarEndpoint,
    DrawLineOp,
    DrawLinePairSpec,
    DrawLineStyle,
    DrawMeta,
    DrawOpsGroupMap,
    DrawScalarPanelDelta,
    DrawScalarPanelOp,
    DrawScalarPanelSpec,
    DrawScalarPanelStyle,
    DrawScalarPanelValue,
    DrawSelect,
    DrawSumOp,
    DrawSumSpec,
    DrawStackedFilterGroupsOp,
    DrawStyle,
    DrawTextNormalizedPosition,
    DrawTextOp,
    DrawTextSpec,
    DrawTextStyle,
    dump_draw_groups,
)

HIGHLIGHT_OPS: Set[str] = {
    "retrieveValue",
    "filter",
    "findExtremum",
    "nth",
    "setOp",
    "lagDiff",
    "compare",
    "pairDiff",
}
SCALAR_LINE_OPS: Set[str] = {"average", "diff", "count", "compare", "compareBool", "add", "scale", "findExtremum"}
SCALAR_TEXT_OPS: Set[str] = {"average", "diff", "count", "compare", "compareBool", "add", "scale", "sum", "findExtremum"}
SUM_OPS: Set[str] = {"sum"}
RANGE_BAND_OPS: Set[str] = {"determineRange"}
CONNECT_OPS: Set[str] = {"compare", "diff"}
LINE_ANCHORED_TEXT_OPS: Set[str] = {"average", "diff", "compare", "findExtremum"}
TEXT_ABOVE_LINE_GAP_NORM = 0.03125


def _ordered_groups(group_names: Iterable[str]) -> List[str]:
    names = [name for name in set(group_names) if isinstance(name, str)]
    ordered: List[str] = []
    if "ops" in names:
        ordered.append("ops")
    ordered.extend(
        sorted(
            [name for name in names if name.startswith("ops") and name[3:].isdigit()],
            key=lambda item: int(item[3:]),
        )
    )
    ordered.extend(sorted([name for name in names if name not in ordered]))
    return ordered


def _build_meta(op: OperationSpec) -> DrawMeta:
    node_id = op.meta.nodeId if op.meta else None
    sentence_index = op.meta.sentenceIndex if op.meta else None
    inputs = list(op.meta.inputs if op.meta else [])
    return DrawMeta(nodeId=node_id, sentenceIndex=sentence_index, inputs=inputs)


def _node_sort_key(node_id: str) -> tuple[int, str]:
    if isinstance(node_id, str) and node_id.startswith("n") and node_id[1:].isdigit():
        return (int(node_id[1:]), node_id)
    return (10**9, str(node_id))


def _unique_targets(result_rows: List[Any]) -> List[str]:
    out: List[str] = []
    seen: Set[str] = set()
    for row in result_rows:
        target = getattr(row, "target", None)
        if target is None:
            continue
        text = str(target).strip()
        if not text or text.startswith("__"):
            continue
        if text in seen:
            continue
        seen.add(text)
        out.append(text)
    return out


def _resolve_scalar(result_rows: List[Any]) -> float | None:
    for row in reversed(result_rows):
        value = getattr(row, "value", None)
        if isinstance(value, bool) or value is None:
            continue
        try:
            numeric = float(value)
        except Exception:
            continue
        if math.isfinite(numeric):
            return numeric
    return None


def _group_filter_action(chart_kind: ChartKind) -> str | None:
    if chart_kind == "stacked_bar":
        return "stacked-filter-groups"
    if chart_kind == "grouped_bar":
        return "grouped-filter-groups"
    return None


def _normalize_orientation(raw: Any) -> str | None:
    if not isinstance(raw, str):
        return None
    token = raw.strip().lower()
    if token not in {"horizontal", "vertical"}:
        return None
    return token


def _scalar_axis_bounds(chart_context: ChartContext, field: str | None) -> tuple[float, float] | None:
    candidates: List[str] = []
    if isinstance(field, str) and field.strip():
        candidates.append(field.strip())
    if isinstance(chart_context.primary_measure, str) and chart_context.primary_measure.strip():
        candidates.append(chart_context.primary_measure.strip())
    for key in candidates:
        stats = chart_context.numeric_stats.get(key)
        if stats is None:
            continue
        lo = float(stats.min)
        hi = float(stats.max)
        if not math.isfinite(lo) or not math.isfinite(hi):
            continue
        if lo == hi:
            hi = lo + 1.0
        domain_lo = min(lo, 0.0)
        domain_hi = max(hi, 0.0)
        if domain_hi <= domain_lo:
            domain_hi = domain_lo + 1.0
        return domain_lo, domain_hi
    return None


def _normalized_scalar_y(chart_context: ChartContext, field: str | None, value: float) -> float | None:
    if not math.isfinite(value):
        return None
    bounds = _scalar_axis_bounds(chart_context, field)
    if bounds is None:
        return None
    lo, hi = bounds
    if hi <= lo:
        return 0.5
    ratio = (value - lo) / (hi - lo)
    ratio = max(0.0, min(1.0, ratio))
    # draw.text normalized y uses bottom=0, top=1.
    return ratio


def _resolve_range_band(result_rows: List[Any]) -> DrawBandSpec | None:
    min_row = None
    max_row = None
    for row in result_rows:
        target = str(getattr(row, "target", "") or "")
        if target == "__min__":
            min_row = row
        elif target == "__max__":
            max_row = row
    if min_row is None or max_row is None:
        return None

    min_name = getattr(min_row, "name", None)
    max_name = getattr(max_row, "name", None)
    if isinstance(min_name, str) and isinstance(max_name, str) and min_name and max_name:
        return DrawBandSpec(
            axis="x",
            range=[min_name, max_name],
            label="range",
            style=DrawBandStyle(fill="rgba(59,130,246,0.16)", stroke="#3b82f6", strokeWidth=1.5, opacity=1.0),
        )

    min_value = _resolve_scalar([min_row])
    max_value = _resolve_scalar([max_row])
    if min_value is None or max_value is None:
        return None
    lo = min(min_value, max_value)
    hi = max(min_value, max_value)
    return DrawBandSpec(
        axis="y",
        range=[float(lo), float(hi)],
        label="range",
        style=DrawBandStyle(fill="rgba(59,130,246,0.14)", stroke="#3b82f6", strokeWidth=1.5, opacity=1.0),
    )


def _normalize_selector_values(raw: Any) -> List[str]:
    if raw is None:
        return []
    if isinstance(raw, (str, int, float)):
        return [str(raw)]
    if isinstance(raw, dict):
        for key in ("target", "category", "id"):
            value = raw.get(key)
            if value is not None:
                return [str(value)]
        return []
    if isinstance(raw, list):
        out: List[str] = []
        for item in raw:
            out.extend(_normalize_selector_values(item))
        return out
    return []


def _selector_ref_key(raw: Any) -> str | None:
    values = _normalize_selector_values(raw)
    for value in values:
        if value.startswith("ref:"):
            return value[len("ref:") :]
        if value.startswith("n") and value[1:].isdigit():
            return value
    return None


def _first_finite_scalar(rows: List[Any]) -> float | None:
    for row in rows:
        value = getattr(row, "value", None)
        if value is None:
            continue
        try:
            numeric = float(value)
        except Exception:
            continue
        if math.isfinite(numeric):
            return numeric
    return None


def _scalar_ref_pair(op: OperationSpec, runtime: Dict[str, List[Any]]) -> Dict[str, Any] | None:
    inputs = list(op.meta.inputs if op.meta else [])
    left_ref = _selector_ref_key(getattr(op, "targetA", None))
    right_ref = _selector_ref_key(getattr(op, "targetB", None))
    if left_ref is None and len(inputs) >= 1:
        left_ref = str(inputs[0])
    if right_ref is None and len(inputs) >= 2:
        right_ref = str(inputs[1])
    if not left_ref or not right_ref:
        return None

    left_rows = list(runtime.get(left_ref, []))
    right_rows = list(runtime.get(right_ref, []))
    if not left_rows or not right_rows:
        return None
    left_value = _first_finite_scalar(left_rows)
    right_value = _first_finite_scalar(right_rows)
    if left_value is None or right_value is None:
        return None

    left_label = str(getattr(left_rows[0], "name", "") or f"ref:{left_ref}")
    right_label = str(getattr(right_rows[0], "name", "") or f"ref:{right_ref}")
    left_target = getattr(left_rows[0], "target", None)
    right_target = getattr(right_rows[0], "target", None)
    return {
        "left": {
            "ref": left_ref,
            "label": left_label,
            "value": left_value,
            "target": str(left_target) if left_target is not None else None,
        },
        "right": {
            "ref": right_ref,
            "label": right_label,
            "value": right_value,
            "target": str(right_target) if right_target is not None else None,
        },
    }


def _is_chart_backed_target(target: Any, domain: Set[str]) -> bool:
    if target is None:
        return False
    text = str(target)
    if not text or text.startswith("__"):
        return False
    return text in domain


def _first_selector_target(raw: Any) -> str | None:
    values = _normalize_selector_values(raw)
    return values[0] if values else None


def _resolve_selector_target(raw: Any, runtime: Dict[str, List[Any]]) -> str | None:
    target = _first_selector_target(raw)
    if not target:
        return None
    ref_key: str | None = None
    if target.startswith("ref:"):
        ref_key = target[len("ref:") :]
    elif target.startswith("n") and target[1:].isdigit():
        ref_key = target
    if not ref_key:
        return target
    rows = runtime.get(ref_key, [])
    if not rows:
        return target
    runtime_target = getattr(rows[0], "target", None)
    if runtime_target is None:
        return target
    return str(runtime_target)


def _contiguous_runs(targets: List[str], domain: List[str]) -> List[List[str]]:
    if not targets or not domain:
        return []
    selected = set(targets)
    runs: List[List[str]] = []
    current: List[str] = []
    for label in domain:
        if label in selected:
            current.append(label)
            continue
        if current:
            runs.append(current)
            current = []
    if current:
        runs.append(current)
    return runs


def _series_pair_line_from_compare_like(
    meta: DrawMeta,
    op: OperationSpec,
    color: str,
    runtime: Dict[str, List[Any]],
) -> DrawLineOp | None:
    target_a = _resolve_selector_target(getattr(op, "targetA", None), runtime)
    target_b = _resolve_selector_target(getattr(op, "targetB", None), runtime)
    if not target_a or not target_b:
        return None

    group_a = getattr(op, "groupA", None)
    group_b = getattr(op, "groupB", None)
    style = DrawLineStyle(stroke=color, strokeWidth=2.0, opacity=1.0)

    if isinstance(group_a, str) and isinstance(group_b, str) and group_a and group_b and target_a == target_b:
        return DrawLineOp(
            meta=meta,
            line=DrawLineConnectSpec(
                connectBy=DrawLineConnectBySpec(
                    start=DrawLineConnectEndpoint(target=target_a, series=group_a),
                    end=DrawLineConnectEndpoint(target=target_b, series=group_b),
                ),
                style=style,
            ),
        )

    return DrawLineOp(
        meta=meta,
        line=DrawLineConnectSpec(
            pair=DrawLinePairSpec(x=[target_a, target_b]),
            style=style,
        ),
    )


def _pair_diff_lines(meta: DrawMeta, op: OperationSpec, result_rows: List[Any]) -> List[DrawLineOp]:
    group_a = getattr(op, "groupA", None)
    group_b = getattr(op, "groupB", None)
    if not isinstance(group_a, str) or not isinstance(group_b, str) or not group_a or not group_b:
        return []
    out: List[DrawLineOp] = []
    for target in _unique_targets(result_rows):
        out.append(
            DrawLineOp(
                meta=meta,
                line=DrawLineConnectSpec(
                    connectBy=DrawLineConnectBySpec(
                        start=DrawLineConnectEndpoint(target=target, series=group_a),
                        end=DrawLineConnectEndpoint(target=target, series=group_b),
                    ),
                    style=DrawLineStyle(stroke="#ef4444", strokeWidth=2.0, opacity=0.95),
                ),
            )
        )
    return out


def _scalar_text_op(
    meta: DrawMeta,
    op_name: str,
    scalar: float,
    line_norm_y: float | None = None,
    label_override: str | None = None,
) -> DrawTextOp:
    if op_name == "compareBool":
        label = "true" if scalar >= 1 else "false"
    elif op_name == "diff":
        label = f"Δ {scalar:.2f}"
    elif isinstance(label_override, str) and label_override.strip():
        label = f"{label_override.strip()}: {scalar:.2f}"
    elif op_name == "findExtremum":
        label = f"extremum: {scalar:.2f}"
    else:
        label = f"{op_name}: {scalar:.2f}"
    text_y = 0.92
    if line_norm_y is not None and math.isfinite(line_norm_y):
        text_y = max(0.04, min(0.98, float(line_norm_y) + TEXT_ABOVE_LINE_GAP_NORM))
    return DrawTextOp(
        meta=meta,
        text=DrawTextSpec(
            value=label,
            mode="normalized",
            position=DrawTextNormalizedPosition(x=0.92, y=text_y),
            style=DrawTextStyle(color="#111827", fontSize=12, fontWeight="bold", opacity=1.0),
        ),
    )


def _merge_inputs(inputs: List[str], extra_inputs: List[str]) -> List[str]:
    merged: List[str] = []
    for value in list(inputs or []) + list(extra_inputs or []):
        if not isinstance(value, str) or not value:
            continue
        if value not in merged:
            merged.append(value)
    return merged


def _with_draw_context(draw_op: Any, *, chart_id: str | None, extra_inputs: List[str]) -> Any:
    update: Dict[str, Any] = {}
    if chart_id is not None:
        update["chartId"] = chart_id
    if extra_inputs:
        meta = draw_op.meta.model_copy(update={"inputs": _merge_inputs(list(draw_op.meta.inputs or []), extra_inputs)})
        update["meta"] = meta
    if not update:
        return draw_op
    return draw_op.model_copy(update=update)


def _collect_edges(ops_spec: Dict[str, List[OperationSpec]]) -> Dict[str, Set[str]]:
    edges: Dict[str, Set[str]] = {}
    for ops in ops_spec.values():
        for op in ops:
            node_id = (op.meta.nodeId if op.meta else None) or op.id
            if not node_id:
                continue
            edges[node_id] = set(op.meta.inputs if op.meta else [])
    return edges


def _index_nodes(ops_spec: Dict[str, List[OperationSpec]]) -> Dict[str, OperationSpec]:
    node_map: Dict[str, OperationSpec] = {}
    for ops in ops_spec.values():
        for op in ops:
            node_id = (op.meta.nodeId if op.meta else None) or op.id
            if node_id:
                node_map[node_id] = op
    return node_map


def build_draw_ops_spec(
    *,
    ops_spec: Dict[str, List[OperationSpec]],
    chart_context: ChartContext,
    data_rows: List[Dict[str, Any]],
    vega_lite_spec: Dict[str, Any],
) -> Dict[str, List[Dict[str, object]]]:
    """
    Build TS-executable draw ops JSON from Python data-op execution results.

    Output shape is OpsSpecGroupMap-compatible:
    {
      "ops":  [ { op:"draw", ... }, ... ],
      "ops2": [ ... ]
    }
    """
    chart_kind = derive_chart_kind(vega_lite_spec, chart_context)
    group_filter_action = _group_filter_action(chart_kind)

    executor = OpsSpecExecutor(chart_context)
    executor.execute(rows=data_rows, ops_spec=ops_spec)
    runtime = executor.runtime

    draw_groups: DrawOpsGroupMap = {}
    primary_dim = chart_context.primary_dimension
    primary_domain = [str(v) for v in chart_context.categorical_values.get(primary_dim, [])] if primary_dim else []
    primary_domain_set = set(primary_domain)
    scalar_anchors: Dict[str, Dict[str, Any]] = {}

    ordered_groups = _ordered_groups(ops_spec.keys())
    for group_index, group_name in enumerate(ordered_groups):
        group_ops = ops_spec.get(group_name, [])
        draw_ops = draw_groups.setdefault(group_name, [])
        if group_index == 0:
            draw_ops.append(DrawClearOp(meta=DrawMeta(source="python-draw-plan", inputs=[])))

        for op in group_ops:
            op_name = str(op.op)
            node_id = (op.meta.nodeId if op.meta else None) or op.id
            if not node_id:
                continue
            result_rows = runtime.get(node_id, [])
            if not result_rows:
                continue

            meta = _build_meta(op)

            op_group = getattr(op, "group", None)
            scoped = bool(op_group and isinstance(op_group, str) and op_group.strip() and group_filter_action)
            emitted_scalar_panel_diff = False
            emitted_panel_scalar_bridge = False
            if scoped and group_filter_action:
                if group_filter_action == "stacked-filter-groups":
                    draw_ops.append(
                        _with_draw_context(
                            DrawStackedFilterGroupsOp(
                                meta=meta,
                                groupFilter=DrawGroupFilterSpec(groups=[str(op_group)]),
                            ),
                            chart_id=None,
                            extra_inputs=[],
                        )
                    )
                else:
                    draw_ops.append(
                        _with_draw_context(
                            DrawGroupedFilterGroupsOp(
                                meta=meta,
                                groupFilter=DrawGroupFilterSpec(groups=[str(op_group)]),
                            ),
                            chart_id=None,
                            extra_inputs=[],
                        )
                    )

            if op_name in HIGHLIGHT_OPS:
                targets = _unique_targets(result_rows)
                if targets:
                    if op_name == "filter" and scoped:
                        # Group-scoped filter on stacked/grouped charts should preserve chart colors.
                        # Do not inject red highlight for this step.
                        targets = []
                    if op_name == "findExtremum" and scoped:
                        # In scoped stacked/grouped flow, extremum should keep series color semantics.
                        # The extremum cue is provided by line/text, not fill replacement.
                        targets = []
                    if targets:
                        draw_ops.append(
                            _with_draw_context(
                                DrawHighlightOp(
                                    meta=meta,
                                    select=DrawSelect(keys=targets),
                                    style=DrawStyle(color="#ef4444", opacity=1.0),
                                ),
                                chart_id=None,
                                extra_inputs=[],
                            )
                        )

            if op_name in RANGE_BAND_OPS:
                band = _resolve_range_band(result_rows)
                if band is not None:
                    draw_ops.append(
                        _with_draw_context(
                            DrawBandOp(meta=meta, band=band),
                            chart_id=None,
                            extra_inputs=[],
                        )
                    )

            if op_name == "setOp":
                targets = _unique_targets(result_rows)
                if targets:
                    domain = primary_domain if primary_domain else targets
                    runs = _contiguous_runs(targets, domain)
                    for run in runs:
                        if len(run) < 2:
                            continue
                        draw_ops.append(
                            _with_draw_context(
                                DrawBandOp(
                                    meta=meta,
                                    band=DrawBandSpec(
                                        axis="x",
                                        range=[run[0], run[-1]],
                                        label=getattr(op, "fn", "set"),
                                        style=DrawBandStyle(
                                            fill="rgba(59,130,246,0.16)",
                                            stroke="#3b82f6",
                                            strokeWidth=1.5,
                                            opacity=1.0,
                                        ),
                                    ),
                                ),
                                chart_id=None,
                                extra_inputs=[],
                            )
                        )

            if op_name in SUM_OPS:
                scalar = _resolve_scalar(result_rows)
                if scalar is not None:
                    draw_ops.append(
                        _with_draw_context(
                            DrawSumOp(meta=meta, sum=DrawSumSpec(value=float(scalar), label="Sum")),
                            chart_id=None,
                            extra_inputs=[],
                        )
                    )

            if op_name in CONNECT_OPS:
                pair = _scalar_ref_pair(op, runtime)
                if pair is not None:
                    left_anchor = scalar_anchors.get(str(pair["left"]["ref"]))
                    right_anchor = scalar_anchors.get(str(pair["right"]["ref"]))
                    if left_anchor and right_anchor:
                        left_chart_id = left_anchor.get("chart_id")
                        right_chart_id = right_anchor.get("chart_id")
                        if (
                            isinstance(left_chart_id, str)
                            and isinstance(right_chart_id, str)
                            and left_chart_id
                            and right_chart_id
                            and left_chart_id != right_chart_id
                        ):
                            orientation_hint = _normalize_orientation(
                                left_anchor.get("orientation") or right_anchor.get("orientation")
                            )
                            bridge_style = DrawLineStyle(stroke="#ef4444", strokeWidth=2.0, opacity=0.95)
                            draw_ops.append(
                                _with_draw_context(
                                    DrawLineOp(
                                        meta=meta,
                                        line=DrawLineConnectPanelScalarSpec(
                                            panelScalar=DrawLinePanelScalarConnectSpec(
                                                start=DrawLinePanelScalarEndpoint(
                                                    chartId=left_chart_id,
                                                    value=float(left_anchor.get("value")),
                                                    nodeId=str(left_anchor.get("node_id"))
                                                    if left_anchor.get("node_id")
                                                    else None,
                                                ),
                                                end=DrawLinePanelScalarEndpoint(
                                                    chartId=right_chart_id,
                                                    value=float(right_anchor.get("value")),
                                                    nodeId=str(right_anchor.get("node_id"))
                                                    if right_anchor.get("node_id")
                                                    else None,
                                                ),
                                                orientationHint=orientation_hint,
                                            ),
                                            style=bridge_style,
                                        ),
                                    ),
                                    chart_id=None,
                                    extra_inputs=[],
                                )
                            )
                            delta_scalar = _resolve_scalar(result_rows)
                            if delta_scalar is None:
                                delta_scalar = abs(float(pair["left"]["value"]) - float(pair["right"]["value"]))
                            text_y = None
                            left_norm_y = _normalized_scalar_y(
                                chart_context, getattr(op, "field", None), float(left_anchor.get("value"))
                            )
                            right_norm_y = _normalized_scalar_y(
                                chart_context, getattr(op, "field", None), float(right_anchor.get("value"))
                            )
                            if left_norm_y is not None and right_norm_y is not None:
                                # y normalized convention: 0=bottom, 1=top, so "above" means larger y.
                                top_norm = max(float(left_norm_y), float(right_norm_y))
                                text_y = max(0.04, min(0.98, top_norm + TEXT_ABOVE_LINE_GAP_NORM))
                            label = f"Difference: {abs(float(delta_scalar)):.2f}"
                            draw_ops.append(
                                _with_draw_context(
                                    DrawTextOp(
                                        meta=meta,
                                        text=DrawTextSpec(
                                            value=label,
                                            mode="normalized",
                                            position=DrawTextNormalizedPosition(
                                                x=0.5,
                                                y=text_y if text_y is not None else 0.5,
                                            ),
                                            style=DrawTextStyle(
                                                color="#111827",
                                                fontSize=12,
                                                fontWeight="bold",
                                                opacity=1.0,
                                            ),
                                        ),
                                    ),
                                    chart_id=None,
                                    extra_inputs=[],
                                )
                            )
                            emitted_panel_scalar_bridge = True

                    if not emitted_panel_scalar_bridge and op_name == "diff":
                        left_backed = _is_chart_backed_target(pair["left"].get("target"), primary_domain_set)
                        right_backed = _is_chart_backed_target(pair["right"].get("target"), primary_domain_set)
                        if not left_backed and not right_backed:
                            base_node = f"{meta.nodeId or node_id}_scalar_base"
                            diff_node = f"{meta.nodeId or node_id}_scalar_diff"
                            left_abs = abs(float(pair["left"]["value"]))
                            right_abs = abs(float(pair["right"]["value"]))
                            delta_scalar = _resolve_scalar(result_rows)
                            if delta_scalar is None:
                                delta_scalar = abs(left_abs - right_abs)
                            else:
                                delta_scalar = abs(float(delta_scalar))
                            style = DrawScalarPanelStyle(
                                leftFill="#ef4444",
                                rightFill="#ef4444",
                                lineStroke="#ef4444",
                                arrowStroke="#0ea5e9",
                                textColor="#111827",
                                panelFill="#ffffff",
                                panelStroke="#cbd5e1",
                            )
                            draw_ops.append(
                                _with_draw_context(
                                    DrawScalarPanelOp(
                                        meta=DrawMeta(
                                            source=meta.source,
                                            nodeId=base_node,
                                            sentenceIndex=meta.sentenceIndex,
                                            inputs=[],
                                        ),
                                        scalarPanel=DrawScalarPanelSpec(
                                            mode="base",
                                            layout="full-replace",
                                            absolute=True,
                                            left=DrawScalarPanelValue(
                                                label=str(pair["left"]["label"]),
                                                value=left_abs,
                                            ),
                                            right=DrawScalarPanelValue(
                                                label=str(pair["right"]["label"]),
                                                value=right_abs,
                                            ),
                                            style=style,
                                        ),
                                    ),
                                    chart_id=None,
                                    extra_inputs=[],
                                )
                            )
                            draw_ops.append(
                                _with_draw_context(
                                    DrawScalarPanelOp(
                                        meta=DrawMeta(
                                            source=meta.source,
                                            nodeId=diff_node,
                                            sentenceIndex=meta.sentenceIndex,
                                            inputs=[base_node],
                                        ),
                                        scalarPanel=DrawScalarPanelSpec(
                                            mode="diff",
                                            layout="full-replace",
                                            absolute=True,
                                            left=DrawScalarPanelValue(
                                                label=str(pair["left"]["label"]),
                                                value=left_abs,
                                            ),
                                            right=DrawScalarPanelValue(
                                                label=str(pair["right"]["label"]),
                                                value=right_abs,
                                            ),
                                            delta=DrawScalarPanelDelta(label="Δ", value=float(delta_scalar)),
                                            style=style,
                                        ),
                                    ),
                                    chart_id=None,
                                    extra_inputs=[],
                                )
                            )
                            emitted_scalar_panel_diff = True
                if not emitted_scalar_panel_diff and not emitted_panel_scalar_bridge:
                    connector = _series_pair_line_from_compare_like(
                        meta,
                        op,
                        "#ef4444",
                        runtime,
                    )
                    if connector is not None:
                        draw_ops.append(
                            _with_draw_context(
                                connector,
                                chart_id=None,
                                extra_inputs=[],
                            )
                        )

            if op_name == "pairDiff":
                for line_op in _pair_diff_lines(meta, op, result_rows):
                    draw_ops.append(
                        _with_draw_context(
                            line_op,
                            chart_id=None,
                            extra_inputs=[],
                        )
                    )

            if op_name == "lagDiff":
                for row in result_rows:
                    prev_target = getattr(row, "prevTarget", None)
                    cur_target = getattr(row, "target", None)
                    if prev_target is None or cur_target is None:
                        continue
                    draw_ops.append(
                        _with_draw_context(
                            DrawLineOp(
                                meta=meta,
                                line=DrawLineConnectSpec(
                                    pair=DrawLinePairSpec(x=[str(prev_target), str(cur_target)]),
                                    style=DrawLineStyle(stroke="#0ea5e9", strokeWidth=2.0, opacity=0.9),
                                ),
                            ),
                            chart_id=None,
                            extra_inputs=[],
                        )
                    )

            if op_name in SCALAR_LINE_OPS:
                if op_name in {"diff", "compare"} and (emitted_scalar_panel_diff or emitted_panel_scalar_bridge):
                    continue
                scalar = _resolve_scalar(result_rows)
                if scalar is not None:
                    draw_ops.append(
                        _with_draw_context(
                            DrawLineOp(
                                meta=meta,
                                line=DrawLineHorizontalFromYSpec(
                                    hline=DrawLineHorizontalSpec(y=float(scalar)),
                                    style=DrawLineStyle(stroke="#ef4444", strokeWidth=2.0, opacity=1.0),
                                ),
                            ),
                            chart_id=None,
                            extra_inputs=[],
                        )
                    )

            if op_name in SCALAR_TEXT_OPS:
                if op_name in {"diff", "compare"} and (emitted_scalar_panel_diff or emitted_panel_scalar_bridge):
                    continue
                scalar = _resolve_scalar(result_rows)
                if scalar is not None:
                    label_override = None
                    if op_name == "findExtremum":
                        which = getattr(op, "which", None)
                        label_override = "min" if str(which).strip().lower() == "min" else "max"
                    line_norm_y = None
                    if op_name in LINE_ANCHORED_TEXT_OPS:
                        line_norm_y = _normalized_scalar_y(
                            chart_context,
                            getattr(op, "field", None),
                            float(scalar),
                        )
                    draw_ops.append(
                        _with_draw_context(
                            _scalar_text_op(
                                meta,
                                op_name,
                                scalar,
                                line_norm_y=line_norm_y,
                                label_override=label_override,
                            ),
                            chart_id=None,
                            extra_inputs=[],
                        )
                    )
            if op_name in {"average", "count", "add", "scale", "sum", "findExtremum", "retrieveValue"}:
                scalar_value = _resolve_scalar(result_rows)
                if scalar_value is not None:
                    scalar_anchors[str(node_id)] = {
                        "node_id": str(node_id),
                        "chart_id": None,
                        "value": float(scalar_value),
                        "orientation": None,
                    }

            if scoped and group_filter_action and op_name != "filter":
                if group_filter_action == "stacked-filter-groups":
                    draw_ops.append(
                        _with_draw_context(
                            DrawStackedFilterGroupsOp(
                                meta=meta,
                                groupFilter=DrawGroupFilterSpec(reset=True),
                            ),
                            chart_id=None,
                            extra_inputs=[],
                        )
                    )
                else:
                    draw_ops.append(
                        _with_draw_context(
                            DrawGroupedFilterGroupsOp(
                                meta=meta,
                                groupFilter=DrawGroupFilterSpec(reset=True),
                            ),
                            chart_id=None,
                            extra_inputs=[],
                        )
                    )

    dumped = dump_draw_groups(draw_groups)
    if not dumped:
        return {"ops": []}
    if "ops" not in dumped:
        dumped["ops"] = []
    return dumped
