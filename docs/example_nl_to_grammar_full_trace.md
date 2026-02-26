# 예시 1개로 보는 전체 변환 추적: 자연어 → PlanTree → GroundedPlanTree → OpsSpec(Grammar)

이 문서는 **실제 repo 차트/데이터**를 기준으로, 입력이 모듈/스텝을 지날 때마다 어떤 형태로 바뀌는지 “스냅샷”으로 보여줍니다.

## 관련 코드(동작 원리 확인용)

- Pipeline orchestrator + debug 번들: `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/modules/pipeline.py`
- Context builder: `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/runtime/context_builder.py`
- Module 1 (Decompose): `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/modules/module_decompose.py`
- Module 2 (Resolve): `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/modules/module_resolve.py`
  - Step 4 validation: `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/validation/resolve_validators.py`
- Module 3 (Specify): `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/modules/module_specify.py`
- Canonicalize: `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/runtime/canonicalize.py`
- Prompts:
  - `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/prompts/opsspec_decompose.md`
  - `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/prompts/opsspec_resolve.md`
  - `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/prompts/opsspec_specify.md`
  - shared rules: `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/prompts/opsspec_shared_rules.md`

---

## 0) 예시 차트(실제 repo 데이터)

아래 문서에서 이미 사용 중인 stacked bar 차트 예시를 그대로 사용합니다:

- Vega-Lite spec(참고): `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/data/test/spec/bar_stacked_ver.json`
- Data CSV(참고): `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/data/test/data/bar_stacked_ver.csv`

차트 인코딩(요약):

- `primary_dimension`: `month`
- `primary_measure`: `count`
- `series_field`: `weather`

예시 `weather` 도메인:
`drizzle, fog, rain, snow, sun`

---

## 1) 시작 형태: 자연어(Question + Explanation)

> (이 단계의 “아웃풋 형태”는 사람이 쓴 자연어 텍스트입니다.)

Question (NL):
- Which months have above-average `count` in both rain and sun?

Explanation (NL):
1) Compute the average of count for rain and for sun across all months.
2) Filter months where each is above its own average.
3) Take the intersection of the two month sets.

---

## 2) Step 0 — Context Builder 출력(결정론적)

입력:
- `vega_lite_spec` + `data_rows`

출력:
- `ChartContext` (Pydantic model; LLM grounding 안정화를 위한 컨텍스트)

핵심 필드만 요약하면:

```json
{
  "primary_dimension": "month",
  "primary_measure": "count",
  "series_field": "weather",
  "fields": ["month", "weather", "count"],
  "measure_fields": ["count"],
  "dimension_fields": ["month", "weather"],
  "categorical_values": {
    "month": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
    "weather": ["drizzle", "fog", "rain", "snow", "sun"]
  }
}
```

> 실제 `ChartContext`는 `field_types`, `numeric_stats`, `mark`, `is_stacked`, `encoding_summary` 등도 포함합니다.

---

## 3) Module 1 — Decompose 출력: PlanTree(추상 계획)

입력:
- 자연어 `question`, `explanation` + `ChartContext` 요약

출력:
- `plan_tree`

참고(디버깅/분석용):
- 파이프라인은 `question` 텍스트로부터 `goal_type`을 **결정론적으로 추정**해 trace/debug에만 기록합니다.
  - 코드: `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/validation/plan_validators.py` (`infer_goal_type`)

### 3-A) Module 1에서 `@...` 토큰으로 표현 가능한 것과 사용 규칙

Module 1의 PlanTree는 아직 “chart context에 완전히 grounding 되기 전”이라,
차트 필드명을 직접 적기 어려운 경우 아래 **역할 토큰(role token)** 을 쓸 수 있습니다.

허용되는 `@token` 목록(정확히 이 3개만):
- `@primary_measure`
- `@primary_dimension`
- `@series_field`

코드에서 이 목록이 나타나는 위치:
- 잔류 토큰 검사(Resolve 이후 남아 있으면 hard error):  
  `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/validation/resolve_validators.py` (`_ROLE_TOKENS`)
- 토큰 치환 규칙(Resolve Step 1; 결정론적 치환):  
  `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/modules/module_resolve.py` (`_resolve_role_tokens`)

언제/어떻게 쓰는가(실제 파이프라인 규칙):
- **Module 1(Decompose)**: `plan_tree.nodes[*].params`의 “필드명을 기대하는 자리”에만 `@token`을 사용합니다.
  - 대표적으로 `params.field`, `params.orderField` 등
- **Module 2(Resolve) Step 1**: `@token` 문자열은 chart_context의 구체 필드명으로 치환됩니다.
- **Module 2(Resolve) Step 4 validation**: 치환 후에도 `@token`이 남아 있으면 hard error입니다.

주의:
- `@series_field`는 chart_context에 `series_field=None`이면 치환 불가하므로, 그 경우에는 Module 2에서 경고/실패가 날 수 있습니다.
- `group`, `include/exclude` 같은 “값(value)” 자리에는 `@token`을 쓰지 않습니다(도메인 매칭이 깨짐).

### 3-B) Module 1에서 `params.fn`에 들어갈 수 있는 값과 코드 위치

Module 1의 `setOp` 노드는 집합 연산을 나타내며, 이때 `params.fn`으로 연산 종류를 지정합니다.

허용되는 `fn` 값:
- `intersection`
- `union`

코드에서 이 목록이 나타나는 위치:
- PlanTree 검증(Decompose strict validator; Module 1 산출물에서 즉시 검사):  
  `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/validation/plan_validators.py`
  - `setOp`는 `params.fn` 필수 + `inputs` 최소 2개 요구
- 최종 OpsSpec 스키마(Union 모델 중 setOp):  
  `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/specs/set_op.py` (`fn: Literal["intersection","union"]`)
- op contract(LLM prompt에 주입되는 required 필드):  
  `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/runtime/op_registry.py`

### Module 1 output (예시 JSON)

```json
{
  "plan_tree": {
    "nodes": [
      {
        "nodeId": "n1",
        "op": "average",
        "group": "ops",
        "params": { "field": "@primary_measure", "group": "Rain" },
        "inputs": [],
        "sentenceIndex": 1
      },
      {
        "nodeId": "n2",
        "op": "average",
        "group": "ops",
        "params": { "field": "@primary_measure", "group": "Sun" },
        "inputs": [],
        "sentenceIndex": 1
      },
      {
        "nodeId": "n3",
        "op": "filter",
        "group": "ops2",
        "params": { "field": "@primary_measure", "operator": ">", "value": "ref:n1", "group": "Rain" },
        "inputs": ["n1"],
        "sentenceIndex": 2
      },
      {
        "nodeId": "n4",
        "op": "filter",
        "group": "ops2",
        "params": { "field": "@primary_measure", "operator": ">", "value": "ref:n2", "group": "Sun" },
        "inputs": ["n2"],
        "sentenceIndex": 2
      },
      {
        "nodeId": "n5",
        "op": "setOp",
        "group": "ops3",
        "params": { "fn": "intersection" },
        "inputs": ["n3", "n4"],
        "sentenceIndex": 3
      }
    ],
    "warnings": []
  },
  "warnings": []
}
```

포인트:
- 아직 `@primary_measure` token이 남아있습니다(Resolve가 처리).
- `group` 값은 사람이 쓴 casing(예: `"Rain"`)일 수 있습니다(Resolve Step 2가 정규화).
- `group`은 “문장 레이어 그룹명(ops/ops2/ops3/...)”이고,
  `params.group`는 “series 값(weather)” 제한을 의미합니다.

---

## 4) Module 2 — Resolve: PlanTree → GroundedPlanTree (4-step)

Resolve는 **가능한 한 결정론적으로** token/value를 chart_context에 맞춰 확정합니다.

### Step 2-1) Token resolution (결정론적)

`@primary_measure` → `count` 로 치환합니다.

Before:

```json
{ "field": "@primary_measure", "operator": ">", "value": "ref:n1", "group": "Rain" }
```

After Step 1:

```json
{ "field": "count", "operator": ">", "value": "ref:n1", "group": "Rain" }
```

### Step 2-2) Value resolution (결정론적, multi-strategy)

`params.group`는 `series_field=weather` 도메인에서 매칭됩니다.

- `"Rain"` → `"rain"` (case-insensitive match)
- `"Sun"` → `"sun"` (case-insensitive match)

After Step 2 (일부 노드 params 예시):

```json
{ "field": "count", "group": "rain" }
```

```json
{ "field": "count", "operator": ">", "value": "ref:n2", "group": "sun" }
```

### Step 2-3) LLM disambiguation (조건부)

Step 1-2 이후에도 “도메인에 없는 값”이 남아 의미 판단이 필요할 때만 LLM을 호출합니다.

이 예시에서는 Step 2까지로 전부 해결되므로:
- `llm_called = false` (호출 스킵)

### Step 2-4) Domain validation (결정론적)

검증 예:
- 미해결 `@token` 잔류 여부
- 존재하지 않는 `field` 사용 여부
- `ref:nX`가 실제 nodeId를 가리키는지
- `inputs`가 모두 유효한 nodeId인지

### Module 2 output: grounded_plan_tree (예시 JSON)

```json
{
  "grounded_plan_tree": {
    "nodes": [
      {
        "nodeId": "n1",
        "op": "average",
        "group": "ops",
        "params": { "field": "count", "group": "rain" },
        "inputs": [],
        "sentenceIndex": 1
      },
      {
        "nodeId": "n2",
        "op": "average",
        "group": "ops",
        "params": { "field": "count", "group": "sun" },
        "inputs": [],
        "sentenceIndex": 1
      },
      {
        "nodeId": "n3",
        "op": "filter",
        "group": "ops2",
        "params": { "field": "count", "operator": ">", "value": "ref:n1", "group": "rain" },
        "inputs": ["n1"],
        "sentenceIndex": 2
      },
      {
        "nodeId": "n4",
        "op": "filter",
        "group": "ops2",
        "params": { "field": "count", "operator": ">", "value": "ref:n2", "group": "sun" },
        "inputs": ["n2"],
        "sentenceIndex": 2
      },
      {
        "nodeId": "n5",
        "op": "setOp",
        "group": "ops3",
        "params": { "fn": "intersection" },
        "inputs": ["n3", "n4"],
        "sentenceIndex": 3
      }
    ],
    "warnings": []
  },
  "warnings": [],
  "llm_called": false
}
```

---

## 5) Module 3 — Specify 출력: OpsSpec(Grammar) JSON

Specify는 grounded_plan_tree의 각 node를 **정확히 1:1**로 OperationSpec으로 변환합니다.

규칙:
- `meta.nodeId == nodeId`
- `meta.inputs`에 `inputs` 반영
- `meta.sentenceIndex == sentenceIndex`
- cross-node scalar ref는 `"ref:nX"` 문자열만

### Module 3 output: ops_spec (예시 JSON)

```json
{
  "ops_spec": {
    "ops": [
      {
        "op": "average",
        "id": "n1",
        "meta": { "nodeId": "n1", "inputs": [], "sentenceIndex": 1 },
        "field": "count",
        "group": "rain"
      },
      {
        "op": "average",
        "id": "n2",
        "meta": { "nodeId": "n2", "inputs": [], "sentenceIndex": 1 },
        "field": "count",
        "group": "sun"
      }
    ],
    "ops2": [
      {
        "op": "filter",
        "id": "n3",
        "meta": { "nodeId": "n3", "inputs": ["n1"], "sentenceIndex": 2 },
        "field": "count",
        "operator": ">",
        "value": "ref:n1",
        "group": "rain"
      },
      {
        "op": "filter",
        "id": "n4",
        "meta": { "nodeId": "n4", "inputs": ["n2"], "sentenceIndex": 2 },
        "field": "count",
        "operator": ">",
        "value": "ref:n2",
        "group": "sun"
      }
    ],
    "ops3": [
      {
        "op": "setOp",
        "id": "n5",
        "meta": { "nodeId": "n5", "inputs": ["n3", "n4"], "sentenceIndex": 3 },
        "fn": "intersection"
      }
    ]
  },
  "warnings": []
}
```

---

## 6) Canonicalize(결정론적) 이후: 최종 grammar JSON

Canonicalize는 group 이름/순서, nodeId, meta.inputs 등을 결정적으로 정규화합니다.

이 예시는 이미 canonical 형태라고 가정하면, 결과는 동일합니다.

---

## 7) 맨 마지막 형태: `/generate_grammar` 최종 응답(JSON)

`/generate_grammar`는 opsSpec groups map을 그대로 반환합니다. (API 래퍼 키 `ops1` 없음)

```json
{
  "ops": [
    {
      "op": "average",
      "id": "n1",
      "meta": { "nodeId": "n1", "inputs": [], "sentenceIndex": 1 },
      "field": "count",
      "group": "rain"
    },
    {
      "op": "average",
      "id": "n2",
      "meta": { "nodeId": "n2", "inputs": [], "sentenceIndex": 1 },
      "field": "count",
      "group": "sun"
    }
  ],
  "ops2": [
    {
      "op": "filter",
      "id": "n3",
      "meta": { "nodeId": "n3", "inputs": ["n1"], "sentenceIndex": 2 },
      "field": "count",
      "operator": ">",
      "value": "ref:n1",
      "group": "rain"
    },
    {
      "op": "filter",
      "id": "n4",
      "meta": { "nodeId": "n4", "inputs": ["n2"], "sentenceIndex": 2 },
      "field": "count",
      "operator": ">",
      "value": "ref:n2",
      "group": "sun"
    }
  ],
  "ops3": [
    {
      "op": "setOp",
      "id": "n5",
      "meta": { "nodeId": "n5", "inputs": ["n3", "n4"], "sentenceIndex": 3 },
      "fn": "intersection"
    }
  ]
}
```

---

## 8) debug=true일 때: 단계별 스냅샷 파일

요청에 `debug=true`를 넣으면, 파이프라인이 아래처럼 단계별 JSON을 저장합니다:

- 저장 위치: `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/debug/<MMddhhmm>/`
- 대표 파일:
  - `00_request.json`
  - `01_context.json`
  - `02_module1_decompose.json`
  - `03_module2_resolve_step1.json`
  - `03_module2_resolve_step2.json`
  - `03_module2_resolve_step3_llm.json`
  - `03_module2_resolve_final.json`
  - `04_module3_specify.json`
  - `05_final_grammar.json`
  - `07_tree_ops_spec.dot` (+ Graphviz 있으면 `.svg/.png`)
