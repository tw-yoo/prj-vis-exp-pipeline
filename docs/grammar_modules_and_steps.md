# 실제 Grammar 파이프라인 문서 (Modules + Steps)

이 문서는 `nlp_server`의 **현재 구현 상태** 기준으로, 자연어 입력이 어떤 모듈/스텝을 거쳐 최종 OpsSpec(=grammar)로 변환되는지 설명합니다. (수정 “계획” 문서가 아닙니다.)

## 0) 엔드포인트 계약 (Public API)

- Endpoint: `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/main.py`
  - `POST /generate_grammar`: `question + explanation + vega_lite_spec + data_rows (+ debug)` → `{<opsSpec group map>}`

파이프라인 오케스트레이션(모듈 호출/재시도/디버그 번들 저장):
- `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/modules/pipeline.py`

---

## 1) 핵심 데이터 구조(중간 표현)

### 1-1) ChartContext (결정론적 컨텍스트)

- 정의: `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/core/models.py`
  - `primary_dimension`, `primary_measure`, `series_field`
  - `categorical_values[field]` (도메인 목록)
  - `field_types`, `measure_fields`, `dimension_fields`, `numeric_stats`, `mark`, `is_stacked`, ...

생성 로직:
- `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/runtime/context_builder.py`

### 1-2) PlanTree / GroundedPlanTree (모듈 1→2 출력)

- 정의: `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/core/models.py`

노드(PlanNode)의 핵심 필드:
- `nodeId`: 반드시 `n<digits>` 형태 (예: `n1`)
- `op`: 연산 이름(legacy op)
- `group`: 문장 레이어 그룹만 허용
  - `sentenceIndex=1 → "ops"`
  - `sentenceIndex=k → "ops{k}" (k>=2)`
- `params`: **flat key-value** (중첩 객체 금지)
- `inputs`: 이전 노드 `nodeId` 의존성
- `sentenceIndex`: 1-based 문장 인덱스

### 1-3) OpsSpec group map (모듈 3 출력)

- 모델/파서:
  - OperationSpec Union: `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/specs/union.py`
  - Base meta 필드: `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/specs/base.py`

OpsSpec의 공통 핵심 규칙:
- 각 op는 `meta.nodeId`, `meta.inputs`, `meta.sentenceIndex`를 통해 DAG 연결이 복원 가능해야 함
- cross-node scalar reference는 `"ref:nX"` **문자열만** 허용 (객체 `{ "id": "nX" }` 금지)

---

## 2) 전체 파이프라인(실제 실행 순서)

구현 entrypoint:
- `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/modules/pipeline.py` (`OpsSpecPipeline.generate`)

큰 흐름:
1. Step 0: Context Builder (deterministic)
2. Module 1: Decompose (LLM + strict retry ×3)
3. Module 2: Resolve (4-step + strict retry ×3)
4. Module 3: Specify (LLM + strict retry ×3 + cross-module feedback)
5. Canonicalize (deterministic)
6. (옵션) Draw plan 생성 + export
7. `/generate_grammar` 응답은 opsSpec groups map을 그대로 반환 (최소 응답)

---

## 3) Step 0 — Context Builder

코드:
- `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/runtime/context_builder.py`

입력:
- `vega_lite_spec`
- `data_rows` (현재 코드에서는 rows preview도 함께 생성)

출력:
- `ChartContext`
- `context_warnings`
- `rows_preview`

설명:
- Vega-Lite encoding의 `type`(nominal/quantitative/temporal 등)을 강한 힌트로 사용해 field type을 안정화합니다.
- categorical 도메인 목록/measure 후보/mark/stacked 여부 등을 구성해 이후 LLM 모듈이 안정적으로 생성하도록 돕습니다.

---

## 4) Module 1 — Decompose (Explanation Decomposition)

코드:
- `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/modules/module_decompose.py`

프롬프트:
- `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/prompts/opsspec_decompose.md`
- shared rules: `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/prompts/opsspec_shared_rules.md`

입력(요약):
- `question`, `explanation`
- `chart_context_json`, `roles_summary`, `series_domain`, `measure_fields`, `rows_preview`
- 이전 실패의 `validation_feedback` (strict retry 시)

출력:
- `plan_tree`

참고(디버깅/분석용):
- 파이프라인은 `question` 텍스트로부터 `goal_type`을 결정론적으로 추정해 trace/debug에만 기록합니다.
  - 코드: `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/validation/plan_validators.py` (`infer_goal_type`)

모듈 내 핵심 스텝(구현 기준):
1) explanation 문장 분리(결정론적 split) → `sentenceIndex`를 위한 기반 구성  
   - 구현: `_split_explanation_sentences` in `module_decompose.py`
2) LLM이 문장 레이어 그룹(`ops/ops2/...`)과 의존성(`inputs`)을 가진 PlanTree를 생성
3) 파이프라인에서 PlanTree를 엄격 검증 + 실패 시 feedback을 넣어 재시도(최대 3회)
   - 구조 검증: `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/validation/plan_validators.py`
   - 호출부: `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/modules/pipeline.py`

중요 규칙(실제 스키마 관점):
- `group`은 문장 레이어 그룹만 허용(`ops`, `ops2`, `ops3`, ...)
- `params`는 flat만 허용(중첩 JSON 금지)
- role token은 `@primary_dimension/@primary_measure/@series_field`만 사용 가능(문자열로만)
- series 제한은 `filter(field=@series_field, include/exclude=...)`로 표현하지 않습니다. 반드시 `params.group="<series value>"`로 제한합니다.

---

## 5) Module 2 — Resolve (Chart-Grounded Resolution: 4-step)

코드:
- `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/modules/module_resolve.py`

프롬프트(이 모듈에서 LLM은 Step 3에만 사용):
- `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/prompts/opsspec_resolve.md`

검증 로직(도메인 validation):
- `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/validation/resolve_validators.py`

입력:
- `plan_tree` (Module 1 출력)
- `chart_context` (Pydantic 모델)
- `rows_preview`
- 이전 실패의 `validation_feedback` (strict retry 시)

출력:
- `grounded_plan_tree` (+ warnings)

### Step 2-1) Token resolution (결정론적)

역할 토큰을 실제 필드명으로 치환합니다:
- `@primary_measure` → `chart_context.primary_measure`
- `@primary_dimension` → `chart_context.primary_dimension`
- `@series_field` → `chart_context.series_field` (있을 때만)

구현:
- `_resolve_role_tokens` in `module_resolve.py`

### Step 2-2) Value resolution (결정론적, multi-strategy)

categorical 도메인 매칭을 통해 문자열 값을 정규화합니다.

- `params.group`:
  - `chart_context.series_field`가 있을 때, `categorical_values[series_field]` 도메인에서 매칭
- `params.include/params.exclude`:
  - `params.field`가 categorical 도메인을 가지면, `categorical_values[field]`에서 매칭

매칭 전략:
1) exact
2) case-insensitive
3) fuzzy(`difflib.get_close_matches`, cutoff=0.8)

구현:
- `_resolve_values` + `_resolve_single_value` in `module_resolve.py`

### Step 2-3) LLM disambiguation (조건부)

Step 1-2 이후에도 “도메인에 없는 값”이 남아 의미 판단이 필요하면 LLM을 호출합니다.

호출 조건(요약):
- `group`이 series 도메인에 없거나
- include/exclude 값이 해당 field 도메인에 없는 경우

구현:
- `_has_unresolved_domain_values` + `_llm_disambiguate` in `module_resolve.py`

### Step 2-4) Domain validation (결정론적)

하드 에러(실패) vs 소프트 경고를 구분해 검증합니다.

하드 에러 예:
- 미해결 `@token` 잔류
- 존재하지 않는 `params.field`
- 존재하지 않는 nodeId를 향하는 `ref:nX`
- `inputs`에 알 수 없는 nodeId 포함

구현:
- `validate_grounded_plan` in `resolve_validators.py`

### Resolve 재시도 정책(파이프라인)

Resolve 전체는 실패 시 최대 3회 재시도합니다.
- 호출부: `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/modules/pipeline.py`
- debug 스냅샷: `03_module2_resolve_step1.json`, `03_module2_resolve_step2.json`, `03_module2_resolve_step3_llm.json`, `03_module2_resolve_final.json`

---

## 6) Module 3 — Specify (Grammar Specification)

코드:
- `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/modules/module_specify.py`

프롬프트:
- `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/prompts/opsspec_specify.md`

op contract(LLM에 주입되는 operation별 required/optional/forbidden):
- `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/runtime/op_registry.py` (`build_ops_contract_for_prompt`)

입력:
- `grounded_plan_tree` (Module 2 출력)
- `chart_context_json`
- `ops_contract_json`
- 이전 실패의 `validation_feedback` (strict retry 시)

출력:
- `ops_spec` (group → OperationSpec list)

핵심 규칙(실제 validator 기준):
- grounded plan의 각 node는 **정확히 1개** OperationSpec으로 변환되어야 함(누락/추가 금지)
- `meta.nodeId == nodeId`, `meta.sentenceIndex == sentenceIndex` 유지
- `meta.inputs`에 node.inputs를 반영해야 함

검증/파싱:
- schema 파싱: `parse_operation_spec` in `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/specs/union.py`
- semantic 검증: `validate_operation` in `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/validation/validators.py`
- plan↔spec 1:1 매핑 검증: `_validate_compiled_groups_match_plan` in `pipeline.py`
- group 규칙: `"last"` 그룹은 최종 OpsSpec에서 금지(문장 레이어 `ops/ops2/...`만 허용)

재시도 정책:
- Specify는 실패 시 최대 3회 strict retry
- 또한 “그라운딩 문제”로 보이면(Module 3 semantic error가 field/domain 문제일 때) Module 2를 1회 재실행 후 다시 Specify를 시도하는 cross-module feedback 로직이 있습니다.
  - 구현: `_is_grounding_error` + 관련 retry 흐름 in `pipeline.py`

---

## 7) Canonicalize (결정론적 정규화)

코드:
- `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/runtime/canonicalize.py`

역할:
- group 이름/순서 정규화(필요 시)
- `nodeId` 재부여 + `"ref:nX"` rewrite(필요 시)
- `meta.inputs` 결정적 재작성

---

## 8) Debug 번들(요청별 산출물)

저장 위치:
- `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/debug/<MMddhhmm>/`

대표 파일:
- `00_request.json`
- `01_context.json`
- `02_module1_decompose.json`
- `03_module2_resolve_step1.json`
- `03_module2_resolve_step2.json`
- `03_module2_resolve_step3_llm.json`
- `03_module2_resolve_final.json`
- `04_module3_specify.json`
- `05_final_grammar.json`
- `06_draw_plan.json`
- `07_tree_ops_spec.dot` (+ Graphviz가 있으면 `.svg/.png`)

구현:
- `_persist_debug_bundle` in `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/modules/pipeline.py`
