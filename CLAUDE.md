# nlp_server 역할/계약 문서 (For Other AI Agents)

이 문서는 다른 AI Agent에게 `nlp_server`가 프로젝트에서 어떤 역할을 하는지, 어떤 입력을 받아 무엇을 출력하는지, 그리고 내부 파이프라인이 어떻게 구성되어 있는지를 **구체적으로** 설명하기 위한 문서입니다.

## 0) AI Agent 개발 명령 (연구용 최소 구현 원칙)

아래는 이 repo에서 `nlp_server`를 수정/확장하는 AI Agent에게 주는 **명령**입니다.

1. 최소한의 기능을 만들 것.
   - 이 코드는 연구를 위한 코드이므로 “기능 확장”을 전제로 과도한 설계를 하지 말 것.
   - 목표는 빠르게 가설을 검증할 수 있는 **MVP 파이프라인**을 유지하는 것.
2. 코드의 재사용성을 고려할 것.
   - 규칙/계약/프롬프트는 중복 작성하지 말고 한 곳에서 관리할 것(예: shared rules).
3. 코드의 가독성을 고려할 것.
   - 작은 함수, 명확한 타입, 명확한 파일 경계를 유지할 것.
4. 응답은 한국어로 할 것.

연구용 코드 품질을 위해 추가로 필요한 명령:
1. 재현 가능성(Reproducibility)을 최우선으로 할 것.
   - LLM 호출은 `temperature=0` 유지.
   - 출력은 스키마 검증 + canonicalize로 **결정적(deterministic)** 형태로 정규화.
   - `OPENAI_MODEL`, 프롬프트 파일 버전(파일 경로/내용), 입력 JSON을 debug 번들에 남겨 추적 가능하게 할 것.
2. 일반화 가능성(Generalizability)을 최우선으로 할 것.
   - 특정 데이터셋/특정 질문 패턴에만 맞춘 하드코딩을 피할 것.
   - 규칙 추가가 필요하면 “한 케이스 예외 처리” 대신, contract/validator 레벨에서 일관 규칙으로 추가할 것.
3. 변경 범위를 최소화하고, 실패는 빠르게 드러나게 할 것.
   - 스키마/validator 위반은 조용히 무시하지 말고 실패(또는 strict retry)시키며, debug 번들에 원인 기록.
4. 의존성 추가는 신중하게 할 것.
   - 가능한 표준 라이브러리로 해결하고(예: DOT 렌더는 graphviz CLI), 필수일 때만 의존성을 추가.

## 1) nlp_server의 핵심 역할 (한 줄 정의)

`nlp_server`는 **(question + explanation) 자연어 텍스트**와 **Vega-Lite spec + data rows**를 입력으로 받아, 최종적으로 **OpsSpec(=grammar)** 를 생성해서 반환하는 서버입니다.

- 출력 OpsSpec은 “legacy operation set(비-드로우)” 기반이며, 복합 질문을 **tree/DAG 구조**로 표현하기 위해 각 op에 `meta.nodeId` / `meta.inputs`를 포함합니다.
- 최종 출력은 웹/TS가 쉽게 소비할 수 있도록 현재 **최소 응답**으로 내려갑니다:
  - `{"ops1": { "ops": [...], "ops2": [...], "last": [...] }}`

## 2) nlp_server가 “하는 일” / “하지 않는 일”

### 하는 일
1. **차트 컨텍스트 구성**
   - Vega-Lite encoding + data rows로부터
     - `primary_dimension`, `primary_measure`, `series_field`
     - categorical domain(값 목록), numeric stats
     - chart mark / stacked 여부
   - 를 구성해서 LLM grounding의 안정성을 높임.

2. **3-Module LLM 파이프라인 실행**
   - Module 1: Explanation Decomposition — NL 설명 → PlanTree + goal_type
   - Module 2: Chart-Grounded Resolution — 4-step 서브프로세스(토큰/값 해결 + LLM 보조 + 검증)
   - Module 3: Grammar Specification — GroundedPlanTree → 최종 OpsSpec groups

3. **엄격 검증 + 재시도**
   - LLM이 잘못된 JSON/스키마/의미 규칙을 출력하면, validation feedback을 넣어 **strict retry** 수행.

4. **Canonicalization(유니크성 강화)**
   - 브랜치 그룹명 정규화(ops/ops2/... 재명명)
   - 그래프 기반 `nodeId` 재부여 + `"ref:nX"` rewrite
   - 의미적으로 동치인 표현을 단일화(validator 규칙)

5. **디버깅 번들 저장 + 트리 시각화**
   - 각 요청마다 `nlp_server/debug/MMddhhmm/`에 단계별 JSON을 저장
   - final OpsSpec을 DOT(+가능하면 SVG/PNG)로 렌더링해서 저장

### 하지 않는 일
1. **실제 시각화 렌더링 엔진 구현**
   - Python은 draw plan(JSON) 생성까지 담당하고, 실제 렌더링은 TS Workbench가 담당.
2. **차트 데이터의 대규모 truncation/cap**
   - 현재 가정: `data_rows < 500`.

## 3) Public API (FastAPI)

### Health
- `GET /health`

### Grammar(=OpsSpec) 생성
- `POST /generate_grammar`
- 입력: `question`, `explanation`, `vega_lite_spec`, `data_rows`, `debug`
- 출력(최소):
  - `{"ops1": { <opsSpec group map> }}`

관련 코드:
- Endpoint: `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/main.py`
- Request 모델: `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/models.py`

### Python 시나리오 직접 실행
- `POST /run_python_plan`
- 입력:
  - `scenario_path: str` (`data/expert/**.py` 하위 경로만 허용)
  - `debug: bool`
- 시나리오 파일 계약(둘 중 하나):
  - `build_request() -> dict`
  - `REQUEST = {...}`
- dict 필드:
  - `question`, `explanation`, `vega_lite_spec`, `data_rows`, `debug?`
- 출력:
  - `scenario_path`, `vega_lite_spec`, `draw_plan`, `warnings`

### Legacy Lambda 생성 (유지 중)
- `POST /generate_lambda`
- 현재 “새 grammar 파이프라인”과는 별도이며, 레거시 경로로 남겨둔 상태.

## 4) 파이프라인 상세 (3-Module LLM)

실행 orchestrator:
- `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/modules/pipeline.py`

전체 흐름:
```
Question + Explanation + Vega-Lite + Data
    ↓
[Context Builder] (deterministic)
    ↓ ChartContext
[Module 1: Explanation Decomposition] (LLM + retry ×3)
    ↓ PlanTree + goal_type
[Module 2: Chart-Grounded Resolution]
  ├ Step 1: Token Resolution   (deterministic: @token → 구체적 필드명)
  ├ Step 2: Value Resolution   (deterministic: exact → case-insensitive → fuzzy)
  ├ Step 3: LLM Disambiguation (조건부 LLM 호출: 잔여 모호성만)
  ├ Step 4: Domain Validation  (deterministic: 검증)
  └ retry ×3
    ↓ GroundedPlanTree
[Module 3: Grammar Specification] (LLM + retry ×3)
    ↓ OpsSpec groups
[Canonicalize] (deterministic)
    ↓
Final OpsSpec
```

### 4.0 Deterministic Context Builder
- 파일: `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/runtime/context_builder.py`
- 역할:
  - Vega-Lite encoding의 `type`(nominal/quantitative/temporal 등)을 강한 힌트로 사용해 field type/role을 안정화
  - `ChartContext` 생성

### Module 1: Explanation Decomposition (Question+Explanation → PlanTree + goal_type)
- 파일: `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/modules/module_decompose.py`
- 프롬프트: `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/prompts/opsspec_decompose.md`
- 출력: `goal_type` + `plan_tree.nodes[]` (flat params, nodeId=n<digits>, inputs=nodeId only)
- Phase 1: 질문 의도 분류(goal_type: LIST_TARGETS / RETURN_SCALARS / COMPARE_SCALARS / FIND_EXTREMUM / SET_INTERSECTION)
- Phase 2: 최소 plan tree 합성

PlanTree 검증:
- `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/validation/plan_validators.py`
- 과생성 방지, 구조 제약, question intent 정합 검증 포함

### Module 2: Chart-Grounded Resolution (PlanTree → GroundedPlanTree)
- 파일: `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/modules/module_resolve.py`
- 프롬프트(Step 3 LLM): `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/prompts/opsspec_resolve.md`
- 4-step 서브프로세스:
  1. **Token Resolution** (결정론적): @primary_measure/@primary_dimension/@series_field → 구체적 필드명
  2. **Value Resolution** (결정론적, 다중 전략): exact match → case-insensitive → fuzzy(difflib)
  3. **LLM Disambiguation** (조건부): Steps 1-2로 해결 안 된 경우만 LLM 호출
  4. **Domain Validation** (결정론적): 결과 검증
- 그라운딩 검증: `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/validation/resolve_validators.py`

> DataDive 원칙: "LLM은 생성(diversity)에, deterministic method는 그라운딩(precision)에"

### Module 3: Grammar Specification (GroundedPlanTree → OpsSpec Group Map)
- 파일: `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/modules/module_specify.py`
- 프롬프트: `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/prompts/opsspec_specify.md`
- 역할:
  - 최종 operation spec을 op별 모델(Discriminated Union)로 맞춰 출력
  - `ref:nX` 참조 규칙 준수
  - Module 3 실패가 그라운딩 문제이면 Module 2를 1회 재실행하는 cross-module 피드백 포함

Ops contract(LLM에 주입되는 op별 required/optional/forbidden):
- `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/runtime/op_registry.py`

## 5) OpsSpec(=Grammar) 모델 구조

OperationSpec은 “op별 모듈형 명세(Discriminated Union)” 입니다:
- `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/specs/`
- Union: `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/specs/union.py`

공통 필드:
- `op`, `id`, `meta(nodeId, inputs, ...)`, `chartId`

Tree/DAG 연결 필드:
- `meta.nodeId`: 노드 ID
- `meta.inputs`: 부모 노드 nodeId 목록(의존관계 edge)

Cross-node scalar reference:
- `"ref:nX"` 문자열로만 표현 (object `{ "id": "nX" }` 금지)

추가 op:
- `setOp` 한 개만 허용 (`fn: intersection|union`)

## 6) 의미 규칙(동치 표현 단일화)

semantic validator:
- `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/validation/validators.py`

핵심 단일화 규칙(요약):
1. series_field를 `filter(field=series_field, include=...)`로 직접 필터링 금지
   - series 제한은 반드시 `op.group="<series value>"`
2. membership filter(include/exclude)는 primary_dimension에서만 허용
3. comparison filter(operator/value)는 numeric measure field에서만 허용

## 7) Canonicalization(유니크성 강화)

canonicalizer:
- `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/runtime/canonicalize.py`

핵심 기능:
1. 브랜치 그룹명 canonicalization (ops/ops2/... 재명명)
2. 그래프 기반 nodeId 재부여 + `"ref:nX"` rewrite
3. 모든 op에 대해 `meta.inputs`를 결정적으로 재작성 (tree/DAG 복원 가능)

## 8) 디버깅 산출물(debug bundle) + 트리 이미지

debug 저장 위치:
- `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/debug/MMddhhmm/`

저장 파일(대표):
- `00_request.json`, `01_context.json`
- `02_module1_decompose.json` — goal_type 포함
- `03_module2_resolve_step1.json` — Token Resolution 결과
- `03_module2_resolve_step2.json` — Value Resolution 결과 (어떤 전략으로 해결됐는지)
- `03_module2_resolve_step3_llm.json` — LLM Disambiguation 호출 여부
- `03_module2_resolve_final.json` — Domain Validation 후 최종 결과
- `04_module3_specify.json`
- `05_final_grammar.json`
- `07_tree_ops_spec.dot` (+ Graphviz 있으면 `.svg`/`.png`)

구현:
- `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/modules/pipeline.py`

## 9) LLM 백엔드 (ChatGPT default)

LLM client:
- `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/core/llm.py`

동작:
- `OPENAI_API_KEY`가 있고 `LLM_BACKEND`를 강제하지 않으면 기본은 OpenAI(ChatGPT) API 사용
- 필요 시 `LLM_BACKEND=ollama`로 로컬 강제 가능
- **백엔드 선택 시 `logger.info`로 선택된 백엔드·모델·base_url을 명시적으로 로깅** (암묵적 fallback 방지)

백엔드 우선순위:
1. `openai_http` — `OPENAI_API_KEY` 있을 때 기본
2. `instructor_openai` — Ollama + instructor 설치 시
3. `ollama_native` — fallback (경고 로그 출력)

## 10) 공유 유틸리티

- `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/core/utils.py`
- `to_float(value)`: 임의 값을 float으로 변환 (변환 불가 시 None)
- `prune_nulls(value)`: None 값을 재귀적으로 제거

> 중복 방지 규칙: `_to_float` / `_prune_nulls` 를 새로 정의하지 말고 반드시 이 모듈에서 import 할 것.

## 11) Resolve 전용 Validator (Module 2 Step 4)

- `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/validation/resolve_validators.py`
- `find_unresolved_tokens(plan_tree)` → `List[str]` (잔류 @token 목록)
- `validate_grounded_plan(plan_tree, chart_context)` → `(plan_tree, warnings, errors)`
  - Hard errors: 미해결 @token, 존재하지 않는 field, 무효 ref:nX
  - Soft warnings: aggregate field가 measure 아님, group이 series domain에 없음, include/exclude가 domain에 없음

> `module_resolve.py`의 Step 4에서 호출. 직접 인라인 작성 금지.

## 12) 엔드포인트 전용 Validator

- `/Users/taewon_1/Desktop/vis-exp/explainable_chart_qa/prj-vis-exp/prj-vis-exp/nlp_server/opsspec/validation/endpoint_validators.py`
- `validate_and_parse_ops_spec_groups(raw_groups, chart_context)` → `(groups, warnings, errors)`
- `validate_refs_against_node_ids(groups)` → `errors`

> `/canonicalize_opsspec` 핸들러의 파싱·검증 로직은 이 모듈에서 관리. main.py에 인라인 추가 금지.

## 12) Canonicalization 사이클 정책

`canonicalize.py`의 그래프 위상 정렬 중 사이클이 감지되면 **조용히 복구하지 않고 `ValueError`를 raise** 합니다.
- 유효한 OpsSpec에서는 사이클이 절대 발생해서는 안 됩니다.
- 발생 시 `meta.inputs` 또는 `ref:nX` 참조의 순환 여부를 확인하세요.

## 13) TS/Web과의 경계

- `nlp_server`는 **OpsSpec(=grammar) 생성 및(옵션) 실행 로직을 Python에서 담당**
- TS/Web은 생성된 OpsSpec을 받아 시각화 및 UI에 연결

현재 `/generate_grammar`는 응답을 최소화해서 `ops1`만 반환하도록 되어 있음.

## 14) 코드 수정
코드 수정을 할 때에는, 관련 .md 문서도 같이 수정해줘.
