from __future__ import annotations

import json
from dataclasses import dataclass
from textwrap import dedent
from typing import Any, Dict, List, Optional

from ..core.models import ChartContext


ANNOTATION_START_MARKER = "// ANNOTATION_LAYER_START"
ANNOTATION_END_MARKER = "// ANNOTATION_LAYER_END"

_BAR_DEFAULT_FILL = "#69b3a2"
_LINE_DEFAULT_STROKE = "#4f46e5"
_GROUPED_BAR_PALETTE = [
    "#4e79a7",
    "#f28e2b",
    "#e15759",
    "#76b7b2",
    "#59a14f",
    "#edc948",
    "#b07aa1",
    "#ff9da7",
    "#9c755f",
    "#bab0ab",
]
_MULTI_LINE_PALETTE = [
    "#60a5fa",
    "#fb7185",
    "#f59e0b",
    "#10b981",
    "#c084fc",
    "#f472b6",
    "#22d3ee",
    "#a3e635",
    "#f97316",
]
_UNSUPPORTED_TOP_LEVEL_KEYS = ("facet", "concat", "hconcat", "vconcat", "repeat", "params", "selection")
_UNSUPPORTED_CHANNEL_KEYS = ("aggregate", "bin", "timeUnit")


class VegaLiteToD3Error(ValueError):
    """Raised when a Vega-Lite spec falls outside the deterministic converter subset."""


@dataclass(frozen=True)
class _ResolvedChannel:
    field: str
    type: str
    title: Optional[str]
    sort: Any = None


@dataclass(frozen=True)
class _ResolvedView:
    mark: str
    mark_def: Dict[str, Any]
    encoding: Dict[str, Dict[str, Any]]


def _stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)


def _as_record(value: Any) -> Dict[str, Any]:
    if isinstance(value, dict):
        return value
    return {}


def _normalize_mark(raw_mark: Any) -> str:
    if isinstance(raw_mark, str):
        return raw_mark.strip().lower()
    if isinstance(raw_mark, dict):
        raw_type = raw_mark.get("type")
        if isinstance(raw_type, str):
            return raw_type.strip().lower()
    return ""


def _merge_layer_encoding(spec: Dict[str, Any], layer: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    merged: Dict[str, Dict[str, Any]] = {}
    top_encoding = _as_record(spec.get("encoding"))
    layer_encoding = _as_record(layer.get("encoding"))
    for source in (top_encoding, layer_encoding):
        for channel, raw in source.items():
            if isinstance(channel, str) and isinstance(raw, dict):
                merged[channel] = dict(raw)
    return merged


def _resolve_view(spec: Dict[str, Any]) -> _ResolvedView:
    top_mark = _normalize_mark(spec.get("mark"))
    top_mark_def = _as_record(spec.get("mark"))
    if top_mark in {"bar", "line"}:
        return _ResolvedView(
            mark=top_mark,
            mark_def=top_mark_def,
            encoding={k: dict(v) for k, v in _as_record(spec.get("encoding")).items() if isinstance(v, dict)},
        )

    layers = spec.get("layer")
    if not isinstance(layers, list) or not layers:
        raise VegaLiteToD3Error("Unsupported Vega-Lite spec: expected a bar or line mark.")

    supported_layers: List[Dict[str, Any]] = []
    supported_marks: List[str] = []
    for layer in layers:
        if not isinstance(layer, dict):
            continue
        layer_mark = _normalize_mark(layer.get("mark"))
        if layer_mark in {"bar", "line"}:
            supported_layers.append(layer)
            supported_marks.append(layer_mark)
        elif layer_mark not in {"", "point"}:
            raise VegaLiteToD3Error(f"Unsupported layered mark for deterministic D3 conversion: {layer_mark}")

    if not supported_layers:
        raise VegaLiteToD3Error("Unsupported Vega-Lite layered spec: no bar or line layer found.")
    if len(set(supported_marks)) > 1:
        raise VegaLiteToD3Error("Unsupported Vega-Lite layered spec: mixed primary marks are not supported.")

    primary_layer = supported_layers[0]
    return _ResolvedView(
        mark=supported_marks[0],
        mark_def=_as_record(primary_layer.get("mark")),
        encoding=_merge_layer_encoding(spec, primary_layer),
    )


def _extract_title(channel: Dict[str, Any], fallback: str) -> str:
    raw_title = channel.get("title")
    if isinstance(raw_title, str) and raw_title.strip():
        return raw_title.strip()
    axis = _as_record(channel.get("axis"))
    axis_title = axis.get("title")
    if isinstance(axis_title, str) and axis_title.strip():
        return axis_title.strip()
    return fallback


def _resolve_channel(name: str, raw: Dict[str, Any]) -> _ResolvedChannel:
    field = raw.get("field")
    if not isinstance(field, str) or not field.strip():
        raise VegaLiteToD3Error(f"Unsupported Vega-Lite spec: channel '{name}' must define a field.")

    for key in _UNSUPPORTED_CHANNEL_KEYS:
        if key in raw:
            raise VegaLiteToD3Error(f"Unsupported Vega-Lite spec: channel '{name}' uses unsupported key '{key}'.")

    raw_type = raw.get("type")
    channel_type = raw_type.strip().lower() if isinstance(raw_type, str) and raw_type.strip() else ""
    if not channel_type:
        channel_type = "quantitative" if name == "y" else "nominal"

    return _ResolvedChannel(
        field=field.strip(),
        type=channel_type,
        title=_extract_title(raw, field.strip()),
        sort=raw.get("sort"),
    )


def _normalize_dimension(value: Any, *, fallback: int) -> int:
    if isinstance(value, (int, float)) and int(value) > 0:
        return int(value)
    return fallback


def _resolve_sort_spec(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, str) and value in {"ascending", "descending"}:
        return value
    if isinstance(value, list) and all(isinstance(item, (str, int, float)) for item in value):
        return list(value)
    if isinstance(value, dict):
        field = value.get("field")
        op = value.get("op", "sum")
        order = value.get("order", "ascending")
        if isinstance(field, str) and isinstance(op, str) and isinstance(order, str) and order in {"ascending", "descending"}:
            return {"field": field, "op": op, "order": order}
    raise VegaLiteToD3Error("Unsupported Vega-Lite sort specification for deterministic D3 conversion.")


def _extract_mark_style(spec: Dict[str, Any], mark_def: Dict[str, Any], *, fallback_fill: str, fallback_stroke: str) -> Dict[str, Any]:
    config_mark = _as_record(_as_record(spec.get("config")).get("mark"))
    fill = mark_def.get("fill") if isinstance(mark_def.get("fill"), str) else None
    color = mark_def.get("color") if isinstance(mark_def.get("color"), str) else None
    stroke = mark_def.get("stroke") if isinstance(mark_def.get("stroke"), str) else None
    config_color = config_mark.get("color") if isinstance(config_mark.get("color"), str) else None
    stroke_width = mark_def.get("strokeWidth") if isinstance(mark_def.get("strokeWidth"), (int, float)) else None

    return {
        "fill": fill or color or config_color or fallback_fill,
        "stroke": stroke or color or config_color or fallback_stroke,
        "strokeWidth": float(stroke_width if stroke_width is not None else 2),
    }


def _resolve_color_domain(data_rows: List[Dict[str, Any]], field: str) -> List[str]:
    seen: Dict[str, None] = {}
    for row in data_rows:
        raw = row.get(field)
        if raw is None:
            continue
        token = str(raw)
        if token not in seen:
            seen[token] = None
    return list(seen.keys())


def _resolve_color_range(spec: Dict[str, Any], *, family: str) -> List[str]:
    color_channel = _as_record(_as_record(spec.get("encoding")).get("color"))
    channel_scale = _as_record(color_channel.get("scale"))
    if isinstance(channel_scale.get("range"), list):
        colors = [str(entry).strip() for entry in channel_scale["range"] if isinstance(entry, str) and str(entry).strip()]
        if colors:
            return colors

    config_range = _as_record(_as_record(spec.get("config")).get("range"))
    if isinstance(config_range.get("category"), list):
        colors = [str(entry).strip() for entry in config_range["category"] if isinstance(entry, str) and str(entry).strip()]
        if colors:
            return colors

    return list(_MULTI_LINE_PALETTE if family == "line_multi" else _GROUPED_BAR_PALETTE)


def _validate_supported_spec(spec: Dict[str, Any], view: _ResolvedView, chart_context: ChartContext) -> None:
    for key in _UNSUPPORTED_TOP_LEVEL_KEYS:
        if key in spec:
            raise VegaLiteToD3Error(f"Unsupported Vega-Lite spec: top-level key '{key}' is not supported.")

    if "transform" in spec:
        raise VegaLiteToD3Error("Unsupported Vega-Lite spec: top-level transform is not supported.")

    layers = spec.get("layer")
    if isinstance(layers, list):
        for index, layer in enumerate(layers):
            if isinstance(layer, dict) and "transform" in layer:
                raise VegaLiteToD3Error(f"Unsupported Vega-Lite spec: layer[{index}] transform is not supported.")

    x_raw = view.encoding.get("x")
    y_raw = view.encoding.get("y")
    if not x_raw or not y_raw:
        raise VegaLiteToD3Error("Unsupported Vega-Lite spec: x and y encodings are required.")

    x_channel = _resolve_channel("x", x_raw)
    y_channel = _resolve_channel("y", y_raw)

    if view.mark == "bar":
        if x_channel.type not in {"nominal", "ordinal", "temporal"}:
            raise VegaLiteToD3Error("Unsupported Vega-Lite bar spec: x must be categorical/temporal.")
        if y_channel.type != "quantitative":
            raise VegaLiteToD3Error("Unsupported Vega-Lite bar spec: y must be quantitative.")

    if view.mark == "line":
        if x_channel.type not in {"nominal", "ordinal", "temporal", "quantitative"}:
            raise VegaLiteToD3Error("Unsupported Vega-Lite line spec: x must be nominal/ordinal/temporal/quantitative.")
        if y_channel.type != "quantitative":
            raise VegaLiteToD3Error("Unsupported Vega-Lite line spec: y must be quantitative.")

    color_raw = view.encoding.get("color")
    if color_raw:
        color_channel = _resolve_channel("color", color_raw)
        if chart_context.field_types.get(color_channel.field) not in {"categorical", None}:
            raise VegaLiteToD3Error("Unsupported Vega-Lite spec: color field must be categorical for D3 conversion.")


def _resolve_chart_family(mark: str, chart_context: ChartContext) -> str:
    if mark == "bar":
        if chart_context.series_field:
            return "bar_stacked" if chart_context.is_stacked else "bar_grouped"
        return "bar_simple"
    if mark == "line":
        return "line_multi" if chart_context.series_field else "line_simple"
    raise VegaLiteToD3Error(f"Unsupported Vega-Lite mark for D3 conversion: {mark}")


def _shared_js_helpers() -> str:
    return dedent(
        """
        function normalizeTemporalValue(rawValue) {
          if (rawValue instanceof Date) return rawValue;
          if (typeof rawValue === 'number') {
            if (rawValue > 1e10) return new Date(rawValue);
            if (rawValue > 3000) return new Date(rawValue * 1000);
            return new Date(Date.UTC(rawValue, 0, 1));
          }
          return new Date(String(rawValue));
        }

        function resolveCategoricalDomain(rows, field, sortSpec, sortField) {
          const fallback = [];
          rows.forEach((row) => {
            const rawValue = row[field];
            if (rawValue == null) return;
            const token = String(rawValue);
            if (!fallback.includes(token)) fallback.push(token);
          });
          if (!sortSpec) return fallback;

          if (Array.isArray(sortSpec)) {
            const specified = sortSpec.map((item) => String(item));
            const seen = new Set(specified);
            fallback.forEach((item) => {
              if (!seen.has(item)) specified.push(item);
            });
            return specified;
          }

          if (sortSpec === 'ascending') return fallback.slice().sort((a, b) => a.localeCompare(b, undefined, { numeric: true, sensitivity: 'base' }));
          if (sortSpec === 'descending') return fallback.slice().sort((a, b) => b.localeCompare(a, undefined, { numeric: true, sensitivity: 'base' }));

          if (typeof sortSpec === 'object' && sortSpec.field) {
            const op = typeof sortSpec.op === 'string' ? sortSpec.op.toLowerCase() : 'sum';
            const direction = sortSpec.order === 'descending' ? -1 : 1;
            const groups = new Map();
            rows.forEach((row) => {
              const key = String(row[field]);
              if (!groups.has(key)) groups.set(key, []);
              groups.get(key).push(Number(row[sortSpec.field]));
            });
            const score = (values) => {
              const numeric = values.filter((value) => Number.isFinite(value));
              if (!numeric.length) return 0;
              if (op === 'mean' || op === 'average' || op === 'avg') return d3.mean(numeric) ?? 0;
              if (op === 'min') return d3.min(numeric) ?? 0;
              if (op === 'max') return d3.max(numeric) ?? 0;
              if (op === 'count' || op === 'valid') return numeric.length;
              return d3.sum(numeric);
            };
            return fallback
              .slice()
              .sort((left, right) => {
                const delta = (score(groups.get(left) ?? []) - score(groups.get(right) ?? [])) * direction;
                if (delta !== 0) return delta;
                return left.localeCompare(right, undefined, { numeric: true, sensitivity: 'base' });
              });
          }

          return fallback;
        }

        function resolveNumericDomain(values, { includeZero = false, padRatio = 0.05 } = {}) {
          const numeric = values.filter((value) => Number.isFinite(value));
          if (!numeric.length) return [0, 1];
          let minValue = d3.min(numeric) ?? 0;
          let maxValue = d3.max(numeric) ?? 1;
          if (includeZero) {
            minValue = Math.min(minValue, 0);
            maxValue = Math.max(maxValue, 0);
          }
          if (minValue === maxValue) {
            const pad = minValue === 0 ? 1 : Math.abs(minValue) * Math.max(padRatio, 0.1);
            return [minValue - pad, maxValue + pad];
          }
          const span = maxValue - minValue;
          const pad = span * padRatio;
          return [minValue - pad, maxValue + pad];
        }
        """
    ).strip()


def _annotation_block() -> str:
    return dedent(
        f"""
          {ANNOTATION_START_MARKER}
          // Add annotation marks to annotationLayer only.
          // Preserve every statement outside this marker block.
          {ANNOTATION_END_MARKER}
        """
    ).strip()


def _render_function_code(config: Dict[str, Any], data_rows: List[Dict[str, Any]]) -> str:
    config_json = _stable_json(config)
    data_json = _stable_json(data_rows)
    family = config["chart_family"]
    annotation_block = _annotation_block()

    if family == "bar_simple":
        family_code = dedent(
            f"""
            function renderAnnotatedChart(container, dataOverride) {{
              const config = {config_json};
              const data = Array.isArray(dataOverride) ? dataOverride : {data_json};
              const width = config.width;
              const height = config.height;
              const margin = config.margin;
              const innerWidth = width - margin.left - margin.right;
              const innerHeight = height - margin.top - margin.bottom;
              const root = d3.select(container);
              root.selectAll('*').remove();
              const svg = root
                .append('svg')
                .attr('viewBox', `0 0 ${{width}} ${{height}}`)
                .attr('width', width)
                .attr('height', height);
              const chartLayer = svg.append('g').attr('transform', `translate(${{margin.left}},${{margin.top}})`);
              const annotationLayer = svg.append('g').attr('transform', `translate(${{margin.left}},${{margin.top}})`).attr('data-layer', 'annotation');
              const rows = data
                .map((row) => ({{
                  ...row,
                  [config.x.field]: row[config.x.field] == null ? null : String(row[config.x.field]),
                  [config.y.field]: Number(row[config.y.field]),
                }}))
                .filter((row) => row[config.x.field] != null && Number.isFinite(row[config.y.field]));
              const xDomain = resolveCategoricalDomain(rows, config.x.field, config.x.sort, config.y.field);
              const xScale = d3.scaleBand().domain(xDomain).range([0, innerWidth]).paddingInner(0.18).paddingOuter(0.08);
              const yDomain = resolveNumericDomain(rows.map((row) => row[config.y.field]), {{ includeZero: true, padRatio: 0.0 }});
              const yScale = d3.scaleLinear().domain(yDomain).nice().range([innerHeight, 0]);
              const colorScale = null;

              chartLayer.append('g').attr('transform', `translate(0,${{innerHeight}})`).call(d3.axisBottom(xScale));
              chartLayer.append('g').call(d3.axisLeft(yScale).ticks(5));
              chartLayer
                .append('text')
                .attr('x', innerWidth / 2)
                .attr('y', innerHeight + margin.bottom - 12)
                .attr('text-anchor', 'middle')
                .text(config.x.title);
              chartLayer
                .append('text')
                .attr('transform', 'rotate(-90)')
                .attr('x', -innerHeight / 2)
                .attr('y', -margin.left + 16)
                .attr('text-anchor', 'middle')
                .text(config.y.title);

              chartLayer
                .selectAll('rect.base-bar')
                .data(rows)
                .join('rect')
                .attr('class', 'base-bar')
                .attr('x', (row) => xScale(row[config.x.field]) ?? 0)
                .attr('y', (row) => (row[config.y.field] >= 0 ? yScale(row[config.y.field]) : yScale(0)))
                .attr('width', xScale.bandwidth())
                .attr('height', (row) => Math.abs(yScale(row[config.y.field]) - yScale(0)))
                .attr('fill', config.markStyle.fill);

              {annotation_block}

              return {{
                svg: svg.node(),
                chartLayer: chartLayer.node(),
                annotationLayer: annotationLayer.node(),
                xScale,
                yScale,
                colorScale,
                data,
              }};
            }}
            """
        ).strip()
    elif family == "bar_grouped":
        family_code = dedent(
            f"""
            function renderAnnotatedChart(container, dataOverride) {{
              const config = {config_json};
              const data = Array.isArray(dataOverride) ? dataOverride : {data_json};
              const width = config.width;
              const height = config.height;
              const margin = config.margin;
              const innerWidth = width - margin.left - margin.right;
              const innerHeight = height - margin.top - margin.bottom;
              const root = d3.select(container);
              root.selectAll('*').remove();
              const svg = root
                .append('svg')
                .attr('viewBox', `0 0 ${{width}} ${{height}}`)
                .attr('width', width)
                .attr('height', height);
              const chartLayer = svg.append('g').attr('transform', `translate(${{margin.left}},${{margin.top}})`);
              const annotationLayer = svg.append('g').attr('transform', `translate(${{margin.left}},${{margin.top}})`).attr('data-layer', 'annotation');
              const rows = data
                .map((row) => ({{
                  ...row,
                  [config.x.field]: row[config.x.field] == null ? null : String(row[config.x.field]),
                  [config.y.field]: Number(row[config.y.field]),
                  [config.color.field]: row[config.color.field] == null ? null : String(row[config.color.field]),
                }}))
                .filter((row) => row[config.x.field] != null && row[config.color.field] != null && Number.isFinite(row[config.y.field]));

              const xDomain = resolveCategoricalDomain(rows, config.x.field, config.x.sort, config.y.field);
              const seriesDomain = config.color.domain;
              const aggregatedRows = [];
              xDomain.forEach((category) => {{
                seriesDomain.forEach((series) => {{
                  const matching = rows.filter((row) => row[config.x.field] === category && row[config.color.field] === series);
                  aggregatedRows.push({{
                    category,
                    series,
                    value: d3.sum(matching, (row) => row[config.y.field]) || 0,
                  }});
                }});
              }});

              const xScale = d3.scaleBand().domain(xDomain).range([0, innerWidth]).paddingInner(0.18).paddingOuter(0.08);
              const innerScale = d3.scaleBand().domain(seriesDomain).range([0, Math.max(xScale.bandwidth(), 1)]).padding(0.08);
              const yDomain = resolveNumericDomain(aggregatedRows.map((row) => row.value), {{ includeZero: true, padRatio: 0.0 }});
              const yScale = d3.scaleLinear().domain(yDomain).nice().range([innerHeight, 0]);
              const colorScale = d3.scaleOrdinal(config.color.range).domain(seriesDomain);

              chartLayer.append('g').attr('transform', `translate(0,${{innerHeight}})`).call(d3.axisBottom(xScale));
              chartLayer.append('g').call(d3.axisLeft(yScale).ticks(5));
              chartLayer
                .append('text')
                .attr('x', innerWidth / 2)
                .attr('y', innerHeight + margin.bottom - 12)
                .attr('text-anchor', 'middle')
                .text(config.x.title);
              chartLayer
                .append('text')
                .attr('transform', 'rotate(-90)')
                .attr('x', -innerHeight / 2)
                .attr('y', -margin.left + 16)
                .attr('text-anchor', 'middle')
                .text(config.y.title);

              chartLayer
                .selectAll('rect.base-bar')
                .data(aggregatedRows)
                .join('rect')
                .attr('class', 'base-bar')
                .attr('x', (row) => (xScale(row.category) ?? 0) + (innerScale(row.series) ?? 0))
                .attr('y', (row) => (row.value >= 0 ? yScale(row.value) : yScale(0)))
                .attr('width', innerScale.bandwidth())
                .attr('height', (row) => Math.abs(yScale(row.value) - yScale(0)))
                .attr('fill', (row) => colorScale(row.series));

              {annotation_block}

              return {{
                svg: svg.node(),
                chartLayer: chartLayer.node(),
                annotationLayer: annotationLayer.node(),
                xScale,
                yScale,
                colorScale,
                data,
              }};
            }}
            """
        ).strip()
    elif family == "bar_stacked":
        family_code = dedent(
            f"""
            function renderAnnotatedChart(container, dataOverride) {{
              const config = {config_json};
              const data = Array.isArray(dataOverride) ? dataOverride : {data_json};
              const width = config.width;
              const height = config.height;
              const margin = config.margin;
              const innerWidth = width - margin.left - margin.right;
              const innerHeight = height - margin.top - margin.bottom;
              const root = d3.select(container);
              root.selectAll('*').remove();
              const svg = root
                .append('svg')
                .attr('viewBox', `0 0 ${{width}} ${{height}}`)
                .attr('width', width)
                .attr('height', height);
              const chartLayer = svg.append('g').attr('transform', `translate(${{margin.left}},${{margin.top}})`);
              const annotationLayer = svg.append('g').attr('transform', `translate(${{margin.left}},${{margin.top}})`).attr('data-layer', 'annotation');
              const rows = data
                .map((row) => ({{
                  ...row,
                  [config.x.field]: row[config.x.field] == null ? null : String(row[config.x.field]),
                  [config.y.field]: Number(row[config.y.field]),
                  [config.color.field]: row[config.color.field] == null ? null : String(row[config.color.field]),
                }}))
                .filter((row) => row[config.x.field] != null && row[config.color.field] != null && Number.isFinite(row[config.y.field]));

              const xDomain = resolveCategoricalDomain(rows, config.x.field, config.x.sort, config.y.field);
              const seriesDomain = config.color.domain;
              const stackedInput = xDomain.map((category) => {{
                const record = {{ category }};
                seriesDomain.forEach((series) => {{
                  record[series] = d3.sum(
                    rows.filter((row) => row[config.x.field] === category && row[config.color.field] === series),
                    (row) => row[config.y.field],
                  ) || 0;
                }});
                return record;
              }});

              const stackedSeries = d3.stack().keys(seriesDomain)(stackedInput);
              const yExtent = [
                d3.min(stackedSeries, (series) => d3.min(series, (segment) => segment[0])) ?? 0,
                d3.max(stackedSeries, (series) => d3.max(series, (segment) => segment[1])) ?? 0,
              ];
              const xScale = d3.scaleBand().domain(xDomain).range([0, innerWidth]).paddingInner(0.18).paddingOuter(0.08);
              const yScale = d3.scaleLinear().domain([Math.min(0, yExtent[0]), Math.max(0, yExtent[1])]).nice().range([innerHeight, 0]);
              const colorScale = d3.scaleOrdinal(config.color.range).domain(seriesDomain);

              chartLayer.append('g').attr('transform', `translate(0,${{innerHeight}})`).call(d3.axisBottom(xScale));
              chartLayer.append('g').call(d3.axisLeft(yScale).ticks(5));
              chartLayer
                .append('text')
                .attr('x', innerWidth / 2)
                .attr('y', innerHeight + margin.bottom - 12)
                .attr('text-anchor', 'middle')
                .text(config.x.title);
              chartLayer
                .append('text')
                .attr('transform', 'rotate(-90)')
                .attr('x', -innerHeight / 2)
                .attr('y', -margin.left + 16)
                .attr('text-anchor', 'middle')
                .text(config.y.title);

              chartLayer
                .selectAll('g.series-layer')
                .data(stackedSeries)
                .join('g')
                .attr('class', 'series-layer')
                .attr('fill', (series) => colorScale(series.key))
                .selectAll('rect.base-bar')
                .data((series) => series.map((segment) => ({{
                  key: series.key,
                  category: segment.data.category,
                  y0: segment[0],
                  y1: segment[1],
                }})))
                .join('rect')
                .attr('class', 'base-bar')
                .attr('x', (segment) => xScale(segment.category) ?? 0)
                .attr('y', (segment) => yScale(segment.y1))
                .attr('width', xScale.bandwidth())
                .attr('height', (segment) => Math.abs(yScale(segment.y0) - yScale(segment.y1)));

              {annotation_block}

              return {{
                svg: svg.node(),
                chartLayer: chartLayer.node(),
                annotationLayer: annotationLayer.node(),
                xScale,
                yScale,
                colorScale,
                data,
              }};
            }}
            """
        ).strip()
    elif family == "line_simple":
        family_code = dedent(
            f"""
            function renderAnnotatedChart(container, dataOverride) {{
              const config = {config_json};
              const data = Array.isArray(dataOverride) ? dataOverride : {data_json};
              const width = config.width;
              const height = config.height;
              const margin = config.margin;
              const innerWidth = width - margin.left - margin.right;
              const innerHeight = height - margin.top - margin.bottom;
              const root = d3.select(container);
              root.selectAll('*').remove();
              const svg = root
                .append('svg')
                .attr('viewBox', `0 0 ${{width}} ${{height}}`)
                .attr('width', width)
                .attr('height', height);
              const chartLayer = svg.append('g').attr('transform', `translate(${{margin.left}},${{margin.top}})`);
              const annotationLayer = svg.append('g').attr('transform', `translate(${{margin.left}},${{margin.top}})`).attr('data-layer', 'annotation');
              const rows = data
                .map((row) => {{
                  const nextRow = {{ ...row, [config.y.field]: Number(row[config.y.field]) }};
                  if (config.x.type === 'temporal') {{
                    nextRow[config.x.field] = normalizeTemporalValue(row[config.x.field]);
                  }} else if (config.x.type === 'quantitative') {{
                    nextRow[config.x.field] = Number(row[config.x.field]);
                  }} else {{
                    nextRow[config.x.field] = row[config.x.field] == null ? null : String(row[config.x.field]);
                  }}
                  return nextRow;
                }})
                .filter((row) => row[config.x.field] != null && Number.isFinite(row[config.y.field]));

              const orderedRows = (() => {{
                if (config.x.type === 'temporal' || config.x.type === 'quantitative') {{
                  return rows.slice().sort((left, right) => {{
                    const leftValue = left[config.x.field];
                    const rightValue = right[config.x.field];
                    return leftValue < rightValue ? -1 : leftValue > rightValue ? 1 : 0;
                  }});
                }}
                const categoricalDomain = resolveCategoricalDomain(rows, config.x.field, config.x.sort, config.y.field);
                const order = new Map(categoricalDomain.map((value, index) => [String(value), index]));
                return rows.slice().sort((left, right) => (order.get(String(left[config.x.field])) ?? 0) - (order.get(String(right[config.x.field])) ?? 0));
              }})();

              const xScale = (() => {{
                if (config.x.type === 'temporal') {{
                  return d3.scaleTime().domain(d3.extent(orderedRows, (row) => row[config.x.field])).range([0, innerWidth]);
                }}
                if (config.x.type === 'quantitative') {{
                  return d3.scaleLinear().domain(d3.extent(orderedRows, (row) => row[config.x.field])).nice().range([0, innerWidth]);
                }}
                const domain = resolveCategoricalDomain(orderedRows, config.x.field, config.x.sort, config.y.field);
                return d3.scalePoint().domain(domain).range([0, innerWidth]).padding(0.5);
              }})();
              const yScale = d3.scaleLinear().domain(resolveNumericDomain(orderedRows.map((row) => row[config.y.field]), {{ includeZero: false, padRatio: 0.05 }})).nice().range([innerHeight, 0]);
              const colorScale = null;
              const lineGenerator = d3
                .line()
                .x((row) => xScale(row[config.x.field]) ?? 0)
                .y((row) => yScale(row[config.y.field]));

              chartLayer
                .append('g')
                .attr('transform', `translate(0,${{innerHeight}})`)
                .call(config.x.type === 'temporal' || config.x.type === 'quantitative' ? d3.axisBottom(xScale).ticks(5) : d3.axisBottom(xScale));
              chartLayer.append('g').call(d3.axisLeft(yScale).ticks(5));
              chartLayer
                .append('text')
                .attr('x', innerWidth / 2)
                .attr('y', innerHeight + margin.bottom - 12)
                .attr('text-anchor', 'middle')
                .text(config.x.title);
              chartLayer
                .append('text')
                .attr('transform', 'rotate(-90)')
                .attr('x', -innerHeight / 2)
                .attr('y', -margin.left + 16)
                .attr('text-anchor', 'middle')
                .text(config.y.title);

              chartLayer
                .append('path')
                .datum(orderedRows)
                .attr('class', 'base-line')
                .attr('fill', 'none')
                .attr('stroke', config.markStyle.stroke)
                .attr('stroke-width', config.markStyle.strokeWidth)
                .attr('d', lineGenerator);

              chartLayer
                .selectAll('circle.base-point')
                .data(orderedRows)
                .join('circle')
                .attr('class', 'base-point')
                .attr('cx', (row) => xScale(row[config.x.field]) ?? 0)
                .attr('cy', (row) => yScale(row[config.y.field]))
                .attr('r', 4)
                .attr('fill', config.markStyle.stroke);

              {annotation_block}

              return {{
                svg: svg.node(),
                chartLayer: chartLayer.node(),
                annotationLayer: annotationLayer.node(),
                xScale,
                yScale,
                colorScale,
                data,
              }};
            }}
            """
        ).strip()
    elif family == "line_multi":
        family_code = dedent(
            f"""
            function renderAnnotatedChart(container, dataOverride) {{
              const config = {config_json};
              const data = Array.isArray(dataOverride) ? dataOverride : {data_json};
              const width = config.width;
              const height = config.height;
              const margin = config.margin;
              const innerWidth = width - margin.left - margin.right;
              const innerHeight = height - margin.top - margin.bottom;
              const root = d3.select(container);
              root.selectAll('*').remove();
              const svg = root
                .append('svg')
                .attr('viewBox', `0 0 ${{width}} ${{height}}`)
                .attr('width', width)
                .attr('height', height);
              const chartLayer = svg.append('g').attr('transform', `translate(${{margin.left}},${{margin.top}})`);
              const annotationLayer = svg.append('g').attr('transform', `translate(${{margin.left}},${{margin.top}})`).attr('data-layer', 'annotation');
              const rows = data
                .map((row) => {{
                  const nextRow = {{
                    ...row,
                    [config.y.field]: Number(row[config.y.field]),
                    [config.color.field]: row[config.color.field] == null ? null : String(row[config.color.field]),
                  }};
                  if (config.x.type === 'temporal') {{
                    nextRow[config.x.field] = normalizeTemporalValue(row[config.x.field]);
                  }} else if (config.x.type === 'quantitative') {{
                    nextRow[config.x.field] = Number(row[config.x.field]);
                  }} else {{
                    nextRow[config.x.field] = row[config.x.field] == null ? null : String(row[config.x.field]);
                  }}
                  return nextRow;
                }})
                .filter((row) => row[config.x.field] != null && row[config.color.field] != null && Number.isFinite(row[config.y.field]));

              const seriesDomain = config.color.domain;
              const orderedRows = (() => {{
                if (config.x.type === 'temporal' || config.x.type === 'quantitative') {{
                  return rows.slice().sort((left, right) => {{
                    const leftValue = left[config.x.field];
                    const rightValue = right[config.x.field];
                    return leftValue < rightValue ? -1 : leftValue > rightValue ? 1 : 0;
                  }});
                }}
                const categoricalDomain = resolveCategoricalDomain(rows, config.x.field, config.x.sort, config.y.field);
                const order = new Map(categoricalDomain.map((value, index) => [String(value), index]));
                return rows.slice().sort((left, right) => (order.get(String(left[config.x.field])) ?? 0) - (order.get(String(right[config.x.field])) ?? 0));
              }})();

              const xScale = (() => {{
                if (config.x.type === 'temporal') {{
                  return d3.scaleTime().domain(d3.extent(orderedRows, (row) => row[config.x.field])).range([0, innerWidth]);
                }}
                if (config.x.type === 'quantitative') {{
                  return d3.scaleLinear().domain(d3.extent(orderedRows, (row) => row[config.x.field])).nice().range([0, innerWidth]);
                }}
                const domain = resolveCategoricalDomain(orderedRows, config.x.field, config.x.sort, config.y.field);
                return d3.scalePoint().domain(domain).range([0, innerWidth]).padding(0.5);
              }})();
              const yScale = d3.scaleLinear().domain(resolveNumericDomain(orderedRows.map((row) => row[config.y.field]), {{ includeZero: false, padRatio: 0.05 }})).nice().range([innerHeight, 0]);
              const colorScale = d3.scaleOrdinal(config.color.range).domain(seriesDomain);
              const groupedRows = d3.group(orderedRows, (row) => row[config.color.field]);
              const lineGenerator = d3
                .line()
                .x((row) => xScale(row[config.x.field]) ?? 0)
                .y((row) => yScale(row[config.y.field]));

              chartLayer
                .append('g')
                .attr('transform', `translate(0,${{innerHeight}})`)
                .call(config.x.type === 'temporal' || config.x.type === 'quantitative' ? d3.axisBottom(xScale).ticks(5) : d3.axisBottom(xScale));
              chartLayer.append('g').call(d3.axisLeft(yScale).ticks(5));
              chartLayer
                .append('text')
                .attr('x', innerWidth / 2)
                .attr('y', innerHeight + margin.bottom - 12)
                .attr('text-anchor', 'middle')
                .text(config.x.title);
              chartLayer
                .append('text')
                .attr('transform', 'rotate(-90)')
                .attr('x', -innerHeight / 2)
                .attr('y', -margin.left + 16)
                .attr('text-anchor', 'middle')
                .text(config.y.title);

              chartLayer
                .selectAll('path.base-line')
                .data(seriesDomain.map((series) => ({{ series, rows: groupedRows.get(series) ?? [] }})))
                .join('path')
                .attr('class', 'base-line')
                .attr('fill', 'none')
                .attr('stroke', (series) => colorScale(series.series))
                .attr('stroke-width', config.markStyle.strokeWidth)
                .attr('d', (series) => lineGenerator(series.rows));

              chartLayer
                .selectAll('circle.base-point')
                .data(orderedRows)
                .join('circle')
                .attr('class', 'base-point')
                .attr('cx', (row) => xScale(row[config.x.field]) ?? 0)
                .attr('cy', (row) => yScale(row[config.y.field]))
                .attr('r', 4)
                .attr('fill', (row) => colorScale(row[config.color.field]));

              {annotation_block}

              return {{
                svg: svg.node(),
                chartLayer: chartLayer.node(),
                annotationLayer: annotationLayer.node(),
                xScale,
                yScale,
                colorScale,
                data,
              }};
            }}
            """
        ).strip()
    else:
        raise VegaLiteToD3Error(f"Unsupported chart family for D3 conversion: {family}")

    return _shared_js_helpers() + "\n\n" + family_code + "\n"


def convert_vegalite_to_d3(
    *,
    vega_lite_spec: Dict[str, Any],
    data_rows: List[Dict[str, Any]],
    chart_context: ChartContext,
) -> Dict[str, Any]:
    if not isinstance(vega_lite_spec, dict):
        raise VegaLiteToD3Error("vega_lite_spec must be an object.")
    if not isinstance(data_rows, list) or not data_rows:
        raise VegaLiteToD3Error("data_rows must contain at least one row.")

    view = _resolve_view(vega_lite_spec)
    _validate_supported_spec(vega_lite_spec, view, chart_context)

    x_channel = _resolve_channel("x", view.encoding["x"])
    y_channel = _resolve_channel("y", view.encoding["y"])
    chart_family = _resolve_chart_family(view.mark, chart_context)
    color_channel = _resolve_channel("color", view.encoding["color"]) if isinstance(view.encoding.get("color"), dict) else None

    if chart_family in {"bar_grouped", "bar_stacked", "line_multi"} and color_channel is None:
        raise VegaLiteToD3Error(f"Unsupported Vega-Lite spec: {chart_family} requires a categorical color channel.")
    if chart_family in {"bar_simple", "line_simple"} and color_channel is not None:
        raise VegaLiteToD3Error(f"Unsupported Vega-Lite spec: unexpected color channel for {chart_family}.")

    color_domain = _resolve_color_domain(data_rows, color_channel.field) if color_channel else []
    color_range = _resolve_color_range(vega_lite_spec, family=chart_family) if color_channel else []

    config: Dict[str, Any] = {
        "chart_family": chart_family,
        "width": _normalize_dimension(vega_lite_spec.get("width"), fallback=640),
        "height": _normalize_dimension(vega_lite_spec.get("height"), fallback=360),
        "margin": {"top": 32, "right": 24, "bottom": 56, "left": 64},
        "mark": view.mark,
        "markStyle": _extract_mark_style(
            vega_lite_spec,
            view.mark_def,
            fallback_fill=_BAR_DEFAULT_FILL,
            fallback_stroke=_LINE_DEFAULT_STROKE,
        ),
        "x": {
            "field": x_channel.field,
            "type": x_channel.type,
            "title": x_channel.title or x_channel.field,
            "sort": _resolve_sort_spec(x_channel.sort),
        },
        "y": {
            "field": y_channel.field,
            "type": y_channel.type,
            "title": y_channel.title or y_channel.field,
        },
        "color": (
            {
                "field": color_channel.field,
                "type": color_channel.type,
                "title": color_channel.title or color_channel.field,
                "domain": color_domain,
                "range": color_range,
            }
            if color_channel
            else None
        ),
    }

    converter_summary = {
        "chart_family": chart_family,
        "mark": view.mark,
        "dimensions": {"width": config["width"], "height": config["height"], "margin": config["margin"]},
        "fields": {
            "x": config["x"],
            "y": config["y"],
            "color": config["color"],
        },
        "row_count": len(data_rows),
        "supported_vl_properties": [
            "mark",
            "encoding.x",
            "encoding.y",
            "encoding.color",
            "width",
            "height",
            "axis.title",
            "encoding.sort",
            "mark.color/fill/stroke",
        ],
        "rejected_vl_properties": list(_UNSUPPORTED_TOP_LEVEL_KEYS) + ["transform", "encoding.aggregate", "encoding.bin", "encoding.timeUnit"],
        "annotation_contract": {
            "function_name": "renderAnnotatedChart",
            "allowed_region": "between annotation markers only",
            "markers": {"start": ANNOTATION_START_MARKER, "end": ANNOTATION_END_MARKER},
            "anchors": ["const data", "const svg", "const chartLayer", "const annotationLayer", "const xScale", "const yScale"],
        },
    }

    d3_code = _render_function_code(config, data_rows)
    return {
        "chart_family": chart_family,
        "d3_code": d3_code,
        "converter_summary": converter_summary,
    }
