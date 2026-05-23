# OpsSpec Operation JSON Examples (All Params Per Operation)

This document lists JSON examples for each supported non-draw operation in `nlp_server/opsspec/specs/`.

Notes:
- Every operation MUST include `meta.inputs` (empty list `[]` is allowed).
- Cross-node scalar references MUST use `"ref:n<digits>"` strings (example: `"ref:n1"`).
- `filter` supports three modes: membership (`include`/`exclude`), comparison (`operator`+`value`), and group-only (`group` only).

## Common Fields (All Ops)

```json
{
  "op": "OP_NAME",
  "id": "n1",
  "chartId": "optional-chart-id",
  "meta": {
    "nodeId": "n1",
    "inputs": ["n0"],
    "sentenceIndex": 1,
    "view": {
      "split": "vertical",
      "align": "x",
      "highlight": true,
      "reference_line": true,
      "note": "optional note"
    },
    "source": "optional freeform source string"
  }
}
```

## retrieveValue

Default forward (x → y): `target`이 x축 카테고리 라벨, 매칭되는 y 값을 반환.

```json
{
  "op": "retrieveValue",
  "id": "n1",
  "chartId": "chart-1",
  "meta": { "nodeId": "n1", "inputs": [], "sentenceIndex": 1 },
  "field": "Revenue_Million_Euros",
  "target": ["2016/17", "2017/18"],
  "group": "Broadcasting"
}
```

Reverse lookup (y → x): `targetAxis: "y"`이면 `target`을 numeric y값으로 보고, 그 값을 가진 x 카테고리를 찾음.

```json
{
  "op": "retrieveValue",
  "id": "n1",
  "chartId": "chart-1",
  "meta": { "nodeId": "n1", "inputs": [], "sentenceIndex": 1 },
  "field": "Revenue_Million_Euros",
  "target": 150,
  "targetAxis": "y",
  "group": "Broadcasting"
}
```

## filter (membership mode)

```json
{
  "op": "filter",
  "id": "n1",
  "chartId": "chart-1",
  "meta": { "nodeId": "n1", "inputs": [], "sentenceIndex": 1 },
  "field": "Season",
  "include": ["2016/17", "2017/18"],
  "exclude": ["2015/16"],
  "group": "Broadcasting"
}
```

## filter (membership on non-primary categorical field)

```json
{
  "op": "filter",
  "id": "n1b",
  "chartId": "chart-1",
  "meta": { "nodeId": "n1b", "inputs": [], "sentenceIndex": 1 },
  "field": "Frequency",
  "include": ["Occasionally (less than once a month)"]
}
```

## filter (comparison mode)

```json
{
  "op": "filter",
  "id": "n2",
  "chartId": "chart-1",
  "meta": { "nodeId": "n2", "inputs": ["n1"], "sentenceIndex": 2 },
  "field": "Revenue_Million_Euros",
  "operator": ">",
  "value": "ref:n1",
  "group": "Broadcasting"
}
```

## filter (between row-order interval)

```json
{
  "op": "filter",
  "id": "n2b",
  "chartId": "chart-1",
  "meta": { "nodeId": "n2b", "inputs": [], "sentenceIndex": 1 },
  "field": "Year",
  "operator": "between",
  "value": ["2009", "2014"]
}
```

## filter (multi-group OR)

```json
{
  "op": "filter",
  "id": "n3",
  "chartId": "chart-1",
  "meta": { "nodeId": "n3", "inputs": [], "sentenceIndex": 2 },
  "field": "Season",
  "include": ["2016/17", "2017/18"],
  "group": ["Broadcasting", "Commercial"]
}
```

## filter (comparison mode + multi-group OR)

```json
{
  "op": "filter",
  "id": "n4",
  "chartId": "chart-1",
  "meta": { "nodeId": "n4", "inputs": ["n1"], "sentenceIndex": 2 },
  "field": "Revenue_Million_Euros",
  "operator": ">",
  "value": "ref:n1",
  "group": ["Broadcasting", "Commercial"]
}
```

## filter (group-only series restriction)

```json
{
  "op": "filter",
  "id": "n5",
  "chartId": "chart-1",
  "meta": { "nodeId": "n5", "inputs": [], "sentenceIndex": 1 },
  "group": ["Philippines", "Thailand"]
}
```

## findExtremum

```json
{
  "op": "findExtremum",
  "id": "n3",
  "chartId": "chart-1",
  "meta": { "nodeId": "n3", "inputs": ["n2"], "sentenceIndex": 2 },
  "field": "Revenue_Million_Euros",
  "group": "Broadcasting",
  "which": "max"
}
```

## findExtremum (second highest)

```json
{
  "op": "findExtremum",
  "id": "n3b",
  "chartId": "chart-1",
  "meta": { "nodeId": "n3b", "inputs": ["n2"], "sentenceIndex": 2 },
  "field": "Revenue_Million_Euros",
  "which": "max",
  "rank": 2
}
```

## findExtremum (second lowest)

```json
{
  "op": "findExtremum",
  "id": "n3c",
  "chartId": "chart-1",
  "meta": { "nodeId": "n3c", "inputs": ["n2"], "sentenceIndex": 2 },
  "field": "Revenue_Million_Euros",
  "which": "min",
  "rank": 2
}
```

## compare

```json
{
  "op": "compare",
  "id": "n5",
  "chartId": "chart-1",
  "meta": { "nodeId": "n5", "inputs": ["n1", "n3"], "sentenceIndex": 3 },
  "field": "Revenue_Million_Euros",
  "targetA": "2016/17",
  "targetB": "2017/18",
  "group": "Broadcasting",
  "groupA": "Broadcasting",
  "groupB": "Commercial",
  "aggregate": "avg",
  "which": "max"
}
```

## compareBool

```json
{
  "op": "compareBool",
  "id": "n6",
  "chartId": "chart-1",
  "meta": { "nodeId": "n6", "inputs": ["n1", "n3"], "sentenceIndex": 3 },
  "field": "Revenue_Million_Euros",
  "targetA": "ref:n1",
  "targetB": "ref:n3",
  "group": "Broadcasting",
  "groupA": "Broadcasting",
  "groupB": "Commercial",
  "aggregate": "avg",
  "operator": ">"
}
```

## sort

```json
{
  "op": "sort",
  "id": "n7",
  "chartId": "chart-1",
  "meta": { "nodeId": "n7", "inputs": ["n2"], "sentenceIndex": 2 },
  "field": "Revenue_Million_Euros",
  "group": "Broadcasting",
  "order": "desc",
  "orderField": "Revenue_Million_Euros"
}
```

## sum

```json
{
  "op": "sum",
  "id": "n8",
  "chartId": "chart-1",
  "meta": { "nodeId": "n8", "inputs": ["n2"], "sentenceIndex": 2 },
  "field": "Revenue_Million_Euros",
  "group": "Broadcasting"
}
```

Notes:
- `sum` is allowed only for bar charts.
- `group` can be `"A"` or `["A","B"]`.
- For stacked bar, `group` omitted or multi-group means sum all values.

## average

```json
{
  "op": "average",
  "id": "n9",
  "chartId": "chart-1",
  "meta": { "nodeId": "n9", "inputs": ["n2"], "sentenceIndex": 2 },
  "field": "Revenue_Million_Euros",
  "group": "Broadcasting"
}
```

## diff

```json
{
  "op": "diff",
  "id": "n10",
  "chartId": "chart-1",
  "meta": { "nodeId": "n10", "inputs": ["n1", "n3"], "sentenceIndex": 4 },
  "field": "Revenue_Million_Euros",
  "targetA": "ref:n1",
  "targetB": "ref:n3",
  "group": "Broadcasting",
  "groupA": "Broadcasting",
  "groupB": "Commercial",
  "aggregate": "avg",
  "signed": true,
  "mode": "ratio",
  "percent": true,
  "scale": 100,
  "precision": 2,
  "targetName": "gap"
}
```

## lagDiff

```json
{
  "op": "lagDiff",
  "id": "n11",
  "chartId": "chart-1",
  "meta": { "nodeId": "n11", "inputs": [], "sentenceIndex": 1 },
  "field": "Audience_Millions",
  "group": "All",
  "order": "asc",
  "absolute": true
}
```

## pairDiff

```json
{
  "op": "pairDiff",
  "id": "n12",
  "chartId": "chart-1",
  "meta": { "nodeId": "n12", "inputs": [], "sentenceIndex": 2 },
  "by": "Season",
  "seriesField": "category",
  "field": "Revenue_Million_Euros",
  "groupA": "Broadcasting",
  "groupB": "Commercial",
  "signed": true,
  "absolute": false,
  "precision": 2
}
```

Grouped-bar example (City-wise 2025-2010):

```json
{
  "op": "pairDiff",
  "id": "n13",
  "meta": { "nodeId": "n13", "inputs": [], "sentenceIndex": 2 },
  "by": "City",
  "seriesField": "Year",
  "field": "Population in millions",
  "groupA": "2025",
  "groupB": "2010",
  "signed": true
}
```

## nth

```json
{
  "op": "nth",
  "id": "n13",
  "chartId": "chart-1",
  "meta": { "nodeId": "n13", "inputs": ["n7"], "sentenceIndex": 5 },
  "field": "Revenue_Million_Euros",
  "group": "Broadcasting",
  "order": "desc",
  "orderField": "Revenue_Million_Euros",
  "n": 1,
  "from": "left"
}
```

## count

```json
{
  "op": "count",
  "id": "n14",
  "chartId": "chart-1",
  "meta": { "nodeId": "n14", "inputs": ["n2"], "sentenceIndex": 2 },
  "field": "Revenue_Million_Euros",
  "group": "Broadcasting"
}
```

## scale

```json
{
  "op": "scale",
  "id": "n15",
  "chartId": "chart-1",
  "meta": { "nodeId": "n15", "inputs": ["n9"], "sentenceIndex": 6 },
  "target": "ref:n9",
  "factor": 2.0,
  "field": "Revenue_Million_Euros"
}
```

## add

```json
{
  "op": "add",
  "id": "n16",
  "chartId": "chart-1",
  "meta": { "nodeId": "n16", "inputs": ["n2", "n4"], "sentenceIndex": 3 },
  "targetA": "ref:n2",
  "targetB": "ref:n4",
  "field": "Average weight in metric grams"
}
```

## diffByValue

각 row의 값과 단일 reference scalar `V`의 차이를 계산. `V`는 `value`(literal) 또는 `targetValue`(`"ref:nX"`) 중 정확히 하나로 지정해야 함. `meta.inputs` fallback은 허용되지 않음.

Literal reference (e.g., compare every row to threshold 100):

```json
{
  "op": "diffByValue",
  "id": "n17",
  "chartId": "chart-1",
  "meta": { "nodeId": "n17", "inputs": [], "sentenceIndex": 1 },
  "value": 100,
  "field": "Revenue_Million_Euros",
  "signed": true
}
```

Scalar ref (e.g., each year's deviation from the overall average):

```json
{
  "op": "diffByValue",
  "id": "n18",
  "chartId": "chart-1",
  "meta": { "nodeId": "n18", "inputs": ["n9"], "sentenceIndex": 2 },
  "targetValue": "ref:n9",
  "field": "Revenue_Million_Euros",
  "group": "Broadcasting",
  "signed": false
}
```

Notes:
- `signed: true` (default) → `row.value - V`; `signed: false` → `abs(row.value - V)`.
- 결과는 scalar가 아니라 **row list** (한 행 당 하나의 delta).
- 사용 사례: "for each year, distance from the overall average", "deviation from a baseline".

## range

데이터 슬라이스의 `max − min` spread를 단일 스칼라로 반환. `findExtremum(max) + findExtremum(min) + diff` 체인을 대체.

```json
{
  "op": "range",
  "id": "n19",
  "chartId": "chart-1",
  "meta": { "nodeId": "n19", "inputs": [], "sentenceIndex": 1 },
  "field": "Revenue_Million_Euros"
}
```

Series별 range:

```json
{
  "op": "range",
  "id": "n20",
  "chartId": "chart-1",
  "meta": { "nodeId": "n20", "inputs": [], "sentenceIndex": 1 },
  "field": "Revenue_Million_Euros",
  "group": "Broadcasting"
}
```

Notes:
- `field` 생략 시 `primary_measure` 사용.
- 결과는 단일 DatumValue (`value = max − min`).
- 사용 사례: "spread", "variation", "channel range", "max − min".

## rollingWindow

순서가 있는 시리즈에서 길이 `window`만큼 sliding하며 집계. (N − window + 1)개의 행을 반환.

3-year moving average (기본 aggregate='avg'):

```json
{
  "op": "rollingWindow",
  "id": "n21",
  "chartId": "chart-1",
  "meta": { "nodeId": "n21", "inputs": [], "sentenceIndex": 1 },
  "window": 3,
  "aggregate": "avg",
  "field": "Audience_Millions",
  "orderField": "Year"
}
```

5-consecutive-year total (aggregate='sum'):

```json
{
  "op": "rollingWindow",
  "id": "n22",
  "chartId": "chart-1",
  "meta": { "nodeId": "n22", "inputs": [], "sentenceIndex": 1 },
  "window": 5,
  "aggregate": "sum",
  "field": "Revenue_Million_Euros",
  "orderField": "Year",
  "group": "Broadcasting"
}
```

Chain example: best 3-year window (`rollingWindow → findExtremum`):

```json
{
  "ops": [
    {
      "op": "rollingWindow",
      "id": "n1",
      "meta": { "nodeId": "n1", "inputs": [], "sentenceIndex": 1 },
      "window": 3,
      "aggregate": "avg",
      "field": "Units_Sold",
      "orderField": "Year"
    },
    {
      "op": "findExtremum",
      "id": "n2",
      "meta": { "nodeId": "n2", "inputs": ["n1"], "sentenceIndex": 2 },
      "which": "max",
      "field": "Units_Sold"
    }
  ]
}
```

Notes:
- `window`는 필수 양의 정수.
- `aggregate`: `"sum"|"avg"|"min"|"max"` (기본 `"avg"`).
- `orderField` 생략 시 자연 순서.
- 사용 사례: "3-year average", "moving sum", "consecutive N-window aggregate".

## monotonicRun

순서가 있는 시리즈에서 단조 구간(monotonic run)을 탐색.

Longest decreasing run (기본 `mode='longest'`):

```json
{
  "op": "monotonicRun",
  "id": "n23",
  "chartId": "chart-1",
  "meta": { "nodeId": "n23", "inputs": [], "sentenceIndex": 1 },
  "direction": "decreasing",
  "mode": "longest",
  "field": "Unemployment_Rate",
  "orderField": "Year"
}
```

First-break (a run이 처음 시작되는 시점만 표시 — "year when it starts to decrease"):

```json
{
  "op": "monotonicRun",
  "id": "n24",
  "chartId": "chart-1",
  "meta": { "nodeId": "n24", "inputs": [], "sentenceIndex": 1 },
  "direction": "decreasing",
  "mode": "firstBreak",
  "field": "Mens_Apparel_Share",
  "orderField": "Year"
}
```

All runs (length ≥ minLength) — multiple stretches가 필요한 경우:

```json
{
  "op": "monotonicRun",
  "id": "n25",
  "chartId": "chart-1",
  "meta": { "nodeId": "n25", "inputs": [], "sentenceIndex": 1 },
  "direction": "increasing",
  "mode": "all",
  "minLength": 3,
  "field": "Audience_Millions",
  "orderField": "Year"
}
```

Notes:
- `direction`: `"increasing"|"decreasing"` (기본 `"increasing"`).
- `strict` 기본 `true` — 인접 step이 등호일 때는 run을 끊음.
- `mode`:
  - `"longest"` (기본) → 가장 긴 run의 row list.
  - `"firstBreak"` → 첫 단조 시작 시점의 단일 row.
  - `"all"` → 모든 적격 run을 flatten.
- `minLength` 기본 `2`. ">2 years" 같은 표현은 `minLength: 3`.
- 사용 사례:
  - "longest period of decrease" → `mode: "longest", direction: "decreasing"`
  - "year when X starts to decrease" → `mode: "firstBreak", direction: "decreasing"`
  - "consecutive years of increase ≥ 3" → `mode: "all", direction: "increasing", minLength: 3`

