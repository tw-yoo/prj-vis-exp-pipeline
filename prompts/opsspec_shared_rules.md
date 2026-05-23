Shared rules (apply to ALL modules):

1) NodeId format:
- A nodeId MUST be a string matching: n<digits> (examples: "n1", "n2", "n10").

2) Scalar references (CRITICAL):
- When a field needs to refer to the scalar output of a previous node, use a STRING reference:
  - "ref:n<digits>" (example: "ref:n1")
- NEVER use an object reference like: { "id": "n1" } anywhere.

3) Prefer stable, simple JSON:
- Prefer scalar values and lists of scalars.
- Avoid nested objects unless absolutely necessary.

4) Strict JSON only:
- Output must be valid JSON.
- Do not output null keys.
- Do not output unknown keys.

5) Step-Compose output restrictions:
- In Step-Compose output, NEVER include: "id", "meta", "chartId".
- The pipeline assigns id/meta deterministically.

6) Meaningful-chunk grouping:
- Group names represent ordered reasoning chunks, not grammatical sentences and not series branches.
- sentenceIndex is a legacy public-schema field name; interpret it as chunk order, not sentence order.
- The pipeline maps:
  - chunkIndex=1 -> group "ops"
  - chunkIndex=k (k>=2) -> group "ops{k}" (examples: "ops2", "ops3", "ops10")
- Do NOT use a "last" group.
- Operation extraction is sparse: a text span without operation-bearing intent can have no task.
- Absorb rhetorical bridge / transition / interpretation-only text into the nearest substantive chunk mention when it helps preserve context.

7) Series restriction (CRITICAL):
- Do NOT restrict series values via a filter on the series field.
  - Forbidden (OpsSpec): { "op": "filter", "field": "<series_field>", "include": ["A","B"] }
- Instead, restrict series via op_spec.group / op_spec.groupA / op_spec.groupB:
  - Example: { "op": "average", "field": "@primary_measure", "group": "A" }
  - FilterOp also allows multi-series restriction via list:
    { "op": "filter", "field": "<categorical_field>", "include": ["2016"], "group": ["A","B"] }
  - For FilterOp, group list uses OR semantics (match any listed group).
  - FilterOp also allows group-only mode for series restriction:
    { "op": "filter", "group": ["A","B"] }
  - FilterOp comparison mode also allows row-order interval slicing:
    { "op": "filter", "field": "<categorical_field>", "operator": "between", "value": ["2009","2014"] }
    This means inclusive slice from first "2009" to first "2014" after it.
  - FilterOp may include optional "xKindHint" to describe the x-axis semantic kind:
    "temporal", "quantitative", "ordinal", "nominal", or "unknown".
    Prefer chart_context / Vega-Lite x encoding when available. Use "temporal" for date/year/month/quarter/time axes,
    "quantitative" when x position is a numeric magnitude, "ordinal" for rank/stage/order axes, and "nominal" for countries/products/names.
    Examples:
    { "op": "filter", "field": "Year", "operator": "between", "value": ["2008","2011"], "xKindHint": "temporal" }
    { "op": "filter", "field": "country", "include": ["USA","KOR"], "xKindHint": "nominal" }
  - For pairwise differences, prefer op="pairDiff" with by/groupA/groupB.
  - If groupA/groupB are values of a non-default field, set pairDiff.seriesField explicitly.

8) Chart-specific operation availability:
- Always follow the Operation contract's allowed_ops for the current chart.
- For chart_family="bar_simple" or chart_family="line_simple", NEVER create op="pairDiff".
- pairDiff is allowed only when the chart has a series field, such as grouped bar, stacked bar, or multi-series line.

9) SumOp rule:
- op="sum" is allowed only for bar charts (simple/stacked).
- SumOp.group may be a string or list of strings.
- In stacked bar, group=None or multi-group means sum all values.
- SumOp is row aggregation only (not scalar arithmetic).

10) AddOp rule:
- Use op="add" to add two scalar values.
- targetA/targetB must be scalar refs ("ref:nX") or numeric literals.

11) DiffByValue rule:
- Use op="diffByValue" to compute per-row deviation from a single scalar reference V (= row.value − V for every row in the working slice).
- Specify V either as `value` (numeric literal) or `targetValue` ("ref:nX" pointing to a prior scalar node) — EXACTLY one of the two. meta.inputs fallback is NOT allowed; targetValue must be explicit when V comes from a prior node.
- Default `signed=true` returns row.value − V (signed delta). Set `signed=false` only when the explanation says "absolute distance / magnitude".
- Result is a row list (one delta per input row), not a scalar.
- Distinguish from `diff` (compares two specific targetA/targetB scalars) and `lagDiff` (compares adjacent rows in a sequence): diffByValue compares EVERY row against ONE reference V.

12) ScaleOp rule:
- Use op="scale" for scalar arithmetic (constant multiplication): result = target × factor.
- target must be a scalar ref ("ref:nX") or numeric literal; factor is a numeric multiplier.
- Common factor values: 2 (doubled), 0.5 (halved / midpoint pattern), 100 (to percent), 0.01 (to fraction).
- For the "midpoint of A and B (= (A + B) / 2)" pattern, emit `add(A, B)` first then `scale(target=ref:n_add, factor=0.5)`. Do NOT use `diff(mode=ratio)` for arithmetic midpoint.
- scale is scalar arithmetic only (not row aggregation; use rollingWindow/average for sliding/mean).

13) Derived-pattern ops (range / rollingWindow / monotonicRun):
- "spread" / "variation" / "max minus min" / "range between highest and lowest"
    → prefer op="range" over the verbose chain findExtremum(max)+findExtremum(min)+diff.
- "3-year average" / "N-consecutive-year window" / "moving average / sum / min / max"
    → prefer op="rollingWindow" with window=N and aggregate one of "sum|avg|min|max"
    (default "avg"). Use orderField for the sliding axis (typically the x-axis dimension).
- "longest period of decrease / increase" / "continuous run of decreasing/increasing"
    → op="monotonicRun" with direction set and mode="longest" (default).
- "year when X starts to decrease/increase" / "first break point"
    → op="monotonicRun" with direction set and mode="firstBreak".
- "all stretches of N or more consecutive increases/decreases"
    → op="monotonicRun" with mode="all" and minLength=N.
- For range/rollingWindow/monotonicRun, group is a single-series restriction when given.

14) Final artifact consistency:
- For each request, produce one primary final artifact type (scalar, boolean, or row-list).
- Intermediate artifacts may differ, but each intermediate node should contribute to deriving that final artifact.
- Avoid dangling branches that do not feed into any later node.
