# Depth-3 End-to-End Example (Input -> Decompose -> Resolve -> Specify -> Final Grammar)

This is a concrete, fully-specified depth-3 scenario that uses the stacked bar chart:
- Spec: `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/data/test/spec/bar_stacked_ver.json`
- Data: `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/data/test/data/bar_stacked_ver.csv`

Scenario goal:
- Find months where **both** `rain` and `sun` are above their own averages.

Depth definition:
- Depth = max number of nodes along dependency edges (`inputs` in plan trees, `meta.inputs` in opsSpec).

## 0) API Input JSON (POST /generate_grammar)

```json
{
  "question": "Which months have above-average count in both rain and sun?",
  "explanation": "Compute the average of count for rain and for sun across all months. Filter months where each is above its own average. Take the intersection of the two month sets.",
  "vega_lite_spec": {
    "$schema": "https://vega.github.io/schema/vega-lite/v3.0.0-rc4.json",
    "encoding": {
      "x": { "field": "month", "type": "nominal", "sort": null },
      "color": { "field": "weather", "type": "nominal" },
      "y": { "field": "count", "type": "quantitative" }
    },
    "data": { "url": "data/test/data/bar_stacked_ver.csv" },
    "mark": "bar"
  },
  "data_rows": [
    { "month": 1, "weather": "drizzle", "count": 10 },
    { "month": 1, "weather": "fog", "count": 38 },
    { "month": 1, "weather": "rain", "count": 35 },
    { "month": 1, "weather": "snow", "count": 8 },
    { "month": 1, "weather": "sun", "count": 33 },
    { "month": 2, "weather": "drizzle", "count": 4 },
    { "month": 2, "weather": "fog", "count": 36 },
    { "month": 2, "weather": "rain", "count": 40 },
    { "month": 2, "weather": "snow", "count": 3 },
    { "month": 2, "weather": "sun", "count": 30 },
    { "month": 3, "weather": "drizzle", "count": 3 },
    { "month": 3, "weather": "fog", "count": 36 },
    { "month": 3, "weather": "rain", "count": 37 },
    { "month": 3, "weather": "snow", "count": 6 },
    { "month": 3, "weather": "sun", "count": 42 },
    { "month": 4, "weather": "drizzle", "count": 4 },
    { "month": 4, "weather": "fog", "count": 34 },
    { "month": 4, "weather": "rain", "count": 20 },
    { "month": 4, "weather": "snow", "count": 1 },
    { "month": 4, "weather": "sun", "count": 61 },
    { "month": 5, "weather": "drizzle", "count": 1 },
    { "month": 5, "weather": "fog", "count": 25 },
    { "month": 5, "weather": "rain", "count": 16 },
    { "month": 5, "weather": "sun", "count": 82 },
    { "month": 6, "weather": "drizzle", "count": 2 },
    { "month": 6, "weather": "fog", "count": 14 },
    { "month": 6, "weather": "rain", "count": 19 },
    { "month": 6, "weather": "sun", "count": 85 },
    { "month": 7, "weather": "drizzle", "count": 8 },
    { "month": 7, "weather": "fog", "count": 13 },
    { "month": 7, "weather": "rain", "count": 14 },
    { "month": 7, "weather": "sun", "count": 89 },
    { "month": 8, "weather": "drizzle", "count": 8 },
    { "month": 8, "weather": "fog", "count": 16 },
    { "month": 8, "weather": "rain", "count": 6 },
    { "month": 8, "weather": "sun", "count": 94 },
    { "month": 9, "weather": "drizzle", "count": 5 },
    { "month": 9, "weather": "fog", "count": 40 },
    { "month": 9, "weather": "rain", "count": 4 },
    { "month": 9, "weather": "sun", "count": 71 },
    { "month": 10, "weather": "drizzle", "count": 4 },
    { "month": 10, "weather": "fog", "count": 55 },
    { "month": 10, "weather": "rain", "count": 20 },
    { "month": 10, "weather": "sun", "count": 45 },
    { "month": 11, "weather": "drizzle", "count": 3 },
    { "month": 11, "weather": "fog", "count": 50 },
    { "month": 11, "weather": "rain", "count": 25 },
    { "month": 11, "weather": "sun", "count": 42 },
    { "month": 12, "weather": "drizzle", "count": 2 },
    { "month": 12, "weather": "fog", "count": 54 },
    { "month": 12, "weather": "rain", "count": 23 },
    { "month": 12, "weather": "snow", "count": 5 },
    { "month": 12, "weather": "sun", "count": 40 }
  ],
  "debug": true
}
```

## 1) Module 1 Output (Decompose → plan_tree + goal_type)

`goal_type`은 question 텍스트로부터 pipeline이 **결정론적으로 추정한** coarse label이며, 디버그 번들 및 ablation study에 활용됩니다.
현재 Module 1 출력 스키마에는 `goal_type`을 포함하지 않고, `plan_tree`만 반환합니다.

```json
{
  "plan_tree": {
    "nodes": [
      { "nodeId": "n1", "op": "average", "group": "ops", "params": { "field": "@primary_measure", "group": "rain" }, "inputs": [] },
      { "nodeId": "n2", "op": "filter", "group": "ops", "params": { "field": "@primary_measure", "operator": ">", "value": "ref:n1", "group": "rain" }, "inputs": ["n1"] },
      { "nodeId": "n3", "op": "average", "group": "ops2", "params": { "field": "@primary_measure", "group": "sun" }, "inputs": [] },
      { "nodeId": "n4", "op": "filter", "group": "ops2", "params": { "field": "@primary_measure", "operator": ">", "value": "ref:n3", "group": "sun" }, "inputs": ["n3"] },
      { "nodeId": "n5", "op": "setOp", "group": "last", "params": { "fn": "intersection" }, "inputs": ["n2", "n4"] }
    ],
    "warnings": []
  },
  "warnings": []
}
```

## 2) Module 2 Output (Resolve → grounded_plan_tree)

4-step 서브프로세스(Token Resolution → Value Resolution → LLM Disambiguation → Domain Validation)를 거쳐 `@token`이 구체적 필드명으로 치환됩니다.

```json
{
  "grounded_plan_tree": {
    "nodes": [
      { "nodeId": "n1", "op": "average", "group": "ops", "params": { "field": "count", "group": "rain" }, "inputs": [] },
      { "nodeId": "n2", "op": "filter", "group": "ops", "params": { "field": "count", "operator": ">", "value": "ref:n1", "group": "rain" }, "inputs": ["n1"] },
      { "nodeId": "n3", "op": "average", "group": "ops2", "params": { "field": "count", "group": "sun" }, "inputs": [] },
      { "nodeId": "n4", "op": "filter", "group": "ops2", "params": { "field": "count", "operator": ">", "value": "ref:n3", "group": "sun" }, "inputs": ["n3"] },
      { "nodeId": "n5", "op": "setOp", "group": "last", "params": { "fn": "intersection" }, "inputs": ["n2", "n4"] }
    ],
    "warnings": []
  },
  "warnings": []
}
```

## 3) Module 3 Output (Specify → ops_spec group map)

This is an example specify output that is *semantically correct* but not canonical. The final step will canonicalize:
- branch names (`ops`/`ops2` ordering)
- nodeId numbering (`n1..nK`)
- and rewrite scalar refs (`ref:nX`)

```json
{
  "ops_spec": {
    "ops": [
      { "op": "average", "field": "count", "group": "sun", "id": "n20", "meta": { "nodeId": "n20", "inputs": [] } },
      { "op": "filter", "field": "count", "operator": ">", "value": "ref:n20", "group": "sun", "id": "n21", "meta": { "nodeId": "n21", "inputs": ["n20"] } }
    ],
    "ops2": [
      { "op": "average", "field": "count", "group": "rain", "id": "n10", "meta": { "nodeId": "n10", "inputs": [] } },
      { "op": "filter", "field": "count", "operator": ">", "value": "ref:n10", "group": "rain", "id": "n11", "meta": { "nodeId": "n11", "inputs": ["n10"] } }
    ],
    "last": [
      { "op": "setOp", "fn": "intersection", "id": "n30", "meta": { "nodeId": "n30", "inputs": ["n21", "n11"] } }
    ]
  },
  "warnings": []
}
```

## 4) Final Grammar (API response shape: {\"ops\": [...], \"ops2\": [...], ...})

```json
{
  "ops": [
    { "op": "average", "id": "n1", "meta": { "nodeId": "n1", "inputs": [] }, "field": "count", "group": "rain" },
    { "op": "filter", "id": "n2", "meta": { "nodeId": "n2", "inputs": ["n1"] }, "field": "count", "operator": ">", "value": "ref:n1", "group": "rain" }
  ],
  "ops2": [
    { "op": "average", "id": "n3", "meta": { "nodeId": "n3", "inputs": [] }, "field": "count", "group": "sun" },
    { "op": "filter", "id": "n4", "meta": { "nodeId": "n4", "inputs": ["n3"] }, "field": "count", "operator": ">", "value": "ref:n3", "group": "sun" }
  ],
  "last": [
    { "op": "setOp", "id": "n5", "meta": { "nodeId": "n5", "inputs": ["n2", "n4"] }, "fn": "intersection" }
  ]
}
```
