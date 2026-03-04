from __future__ import annotations

import math
from typing import Any, Dict, Iterable, List, Set

from opsspec.runtime.executor import OpsSpecExecutor
from opsspec.core.models import ChartContext
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
    DrawLineConnectSpec,
    DrawLineHorizontalFromYSpec,
    DrawLineHorizontalSpec,
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
SCALAR_LINE_OPS: Set[str] = {"average", "diff", "count", "compare", "compareBool", "add", "scale"}
SCALAR_TEXT_OPS: Set[str] = {"average", "diff", "count", "compare", "compareBool", "add", "scale", "sum"}
SUM_OPS: Set[str] = {"sum"}
RANGE_BAND_OPS: Set[str] = {"determineRange"}
CONNECT_OPS: Set[str] = {"compare", "diff"}


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


def _scalar_text_op(meta: DrawMeta, op_name: str, scalar: float) -> DrawTextOp:
    if op_name == "compareBool":
        label = "true" if scalar >= 1 else "false"
    elif op_name == "diff":
        label = f"Δ {scalar:.2f}"
    else:
        label = f"{op_name}: {scalar:.2f}"
    return DrawTextOp(
        meta=meta,
        text=DrawTextSpec(
            value=label,
            mode="normalized",
            position=DrawTextNormalizedPosition(x=0.92, y=0.08),
            style=DrawTextStyle(color="#111827", fontSize=12, fontWeight="bold", opacity=1.0),
        ),
    )


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

    for group_name in _ordered_groups(ops_spec.keys()):
        group_ops = ops_spec.get(group_name, [])
        draw_ops = draw_groups.setdefault(group_name, [])
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
            if scoped and group_filter_action:
                if group_filter_action == "stacked-filter-groups":
                    draw_ops.append(
                        DrawStackedFilterGroupsOp(
                            meta=meta,
                            groupFilter=DrawGroupFilterSpec(groups=[str(op_group)]),
                        )
                    )
                else:
                    draw_ops.append(
                        DrawGroupedFilterGroupsOp(
                            meta=meta,
                            groupFilter=DrawGroupFilterSpec(groups=[str(op_group)]),
                        )
                    )

            if op_name in HIGHLIGHT_OPS:
                targets = _unique_targets(result_rows)
                if targets:
                    draw_ops.append(
                        DrawHighlightOp(
                            meta=meta,
                            select=DrawSelect(keys=targets),
                            style=DrawStyle(color="#ef4444", opacity=1.0),
                        )
                    )

            if op_name in RANGE_BAND_OPS:
                band = _resolve_range_band(result_rows)
                if band is not None:
                    draw_ops.append(DrawBandOp(meta=meta, band=band))

            if op_name == "setOp":
                targets = _unique_targets(result_rows)
                if targets:
                    domain = primary_domain if primary_domain else targets
                    runs = _contiguous_runs(targets, domain)
                    for run in runs:
                        if len(run) < 2:
                            continue
                        draw_ops.append(
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
                            )
                        )

            if op_name in SUM_OPS:
                scalar = _resolve_scalar(result_rows)
                if scalar is not None:
                    draw_ops.append(DrawSumOp(meta=meta, sum=DrawSumSpec(value=float(scalar), label="Sum")))

            if op_name in CONNECT_OPS:
                if op_name == "diff":
                    pair = _scalar_ref_pair(op, runtime)
                    if pair is not None:
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
                                )
                            )
                            draw_ops.append(
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
                                )
                            )
                            emitted_scalar_panel_diff = True
                if not emitted_scalar_panel_diff:
                    connector = _series_pair_line_from_compare_like(
                        meta,
                        op,
                        "#0ea5e9" if op_name == "compare" else "#ef4444",
                        runtime,
                    )
                    if connector is not None:
                        draw_ops.append(connector)

            if op_name == "pairDiff":
                draw_ops.extend(_pair_diff_lines(meta, op, result_rows))

            if op_name == "lagDiff":
                for row in result_rows:
                    prev_target = getattr(row, "prevTarget", None)
                    cur_target = getattr(row, "target", None)
                    if prev_target is None or cur_target is None:
                        continue
                    draw_ops.append(
                        DrawLineOp(
                            meta=meta,
                            line=DrawLineConnectSpec(
                                pair=DrawLinePairSpec(x=[str(prev_target), str(cur_target)]),
                                style=DrawLineStyle(stroke="#0ea5e9", strokeWidth=2.0, opacity=0.9),
                            ),
                        )
                    )

            if op_name in SCALAR_LINE_OPS:
                if op_name == "diff" and emitted_scalar_panel_diff:
                    continue
                scalar = _resolve_scalar(result_rows)
                if scalar is not None:
                    draw_ops.append(
                        DrawLineOp(
                            meta=meta,
                            line=DrawLineHorizontalFromYSpec(
                                hline=DrawLineHorizontalSpec(y=float(scalar)),
                                style=DrawLineStyle(stroke="#ef4444", strokeWidth=2.0, opacity=1.0),
                            ),
                        )
                    )

            if op_name in SCALAR_TEXT_OPS:
                if op_name == "diff" and emitted_scalar_panel_diff:
                    continue
                scalar = _resolve_scalar(result_rows)
                if scalar is not None:
                    draw_ops.append(_scalar_text_op(meta, op_name, scalar))

            if scoped and group_filter_action:
                if group_filter_action == "stacked-filter-groups":
                    draw_ops.append(
                        DrawStackedFilterGroupsOp(
                            meta=meta,
                            groupFilter=DrawGroupFilterSpec(reset=True),
                        )
                    )
                else:
                    draw_ops.append(
                        DrawGroupedFilterGroupsOp(
                            meta=meta,
                            groupFilter=DrawGroupFilterSpec(reset=True),
                        )
                    )

    dumped = dump_draw_groups(draw_groups)
    if not dumped:
        return {"ops": []}
    if "ops" not in dumped:
        dumped["ops"] = []
    return dumped
