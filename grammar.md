# 파이프라인 개선 계획: VIS 학회 수준으로 끌어올리기

## Context

현재 파이프라인은 question + explanation → OpsSpec grammar를 생성하는 3-module LLM 파이프라인이다.
**핵심 문제**: Module 2(Ground)가 단순 토큰 치환(46줄)으로, 연구 기여가 없다. Module 이름들이 기술적이고 개념적 역할이 드러나지 않는다. 모듈 간 경계가 모호하다.

**참고 논문에서 가져온 핵심 인사이트**:
- **(1) Chart QA**: 6-step Visual→Non-Visual 변환이 핵심 기여. 각 단계가 명확한 이름/역할/I-O를 가짐. Word2vec + dependency parsing으로 다층 해석.
- **(2) DataDive/ClaimVis**: Multi-strategy resolution (Direct → Semantic → SQL → QA fallback). "LLM은 생성에, symbolic method는 그라운딩에" 원칙.
- **(3) DiaryPlay**: 모듈마다 Design Goal(DG1-3)에 명시적 연결. Problem→Solution→Justification 패턴.

---

## 1. 모듈 재명명

| 현재 | 제안 | 약칭 | 도전 과제 |
|------|------|------|-----------|
| Module 1: Decompose | **Explanation Decomposition** | Decompose | 다문장 자연어 설명을 구조화된 연산 계획으로 분해하는 방법 |
| Module 2: Ground | **Chart-Grounded Resolution** | Resolve | 추상적 계획 참조를 실제 차트 데이터 요소에 안정적으로 대응시키는 방법 |
| Module 3: Compile | **Grammar Specification** | Specify | 검증된 계획을 실행 가능한 OpsSpec 문법으로 합성하는 방법 |

**명명 근거**:
- **Decompose**: Paper 1의 "Visual→Non-Visual Conversion"처럼, NL 설명 → 연산 DAG 변환을 수행. 기존 이름이 적절.
- **Resolve**: Paper 2(DataDive)의 "Locate Context in Data"에 대응. "Ground"는 단순 치환 느낌이지만, "Resolve"는 다중 전략 해결(ambiguity resolution)을 함축.
- **Specify**: Paper 1의 "Explanation Generation"처럼, 최종 형식 명세 생성을 담당. "Compile"은 기계적이지만, "Specify"는 문법 사양 생성이라는 목적을 드러냄.

---

## 2. Module 2 (Resolve) 대폭 강화 — 가장 큰 변경

### 현재 문제
- 코드 46줄, 프롬프트 53줄. LLM에게 토큰 치환만 요청.
- 검증(validation) 없음, 재시도(retry) 없음, 다중 전략 없음.
- VIS 논문에서 별도 모듈로 정당화하기 어려움.

### 개선 후 4-step 서브프로세스

Paper 1의 6-step 접근법과 ClaimVis의 multi-strategy resolution에서 영감.

```
PlanTree (추상적 참조)
    ↓
  Step 1: Deterministic Token Resolution (LLM 불필요)
    @primary_measure → chart_context.primary_measure
    @primary_dimension → chart_context.primary_dimension
    @series_field → chart_context.series_field
    ↓
  Step 2: Value Resolution — Multi-Strategy (LLM 불필요)
    params 내 값 참조 (target, include/exclude 등)에 대해:
    전략 1: Exact match (categorical_values 도메인 직접 비교)
    전략 2: Case-insensitive match
    전략 3: Fuzzy match (문자열 유사도 기반, ClaimVis의 rapidfuzz 참고)
    ↓
  Step 3: LLM-Assisted Disambiguation (남은 모호성만 LLM 처리)
    Step 1-2로 해결 안 된 참조만 LLM에게 전달
    series 값 vs dimension 값 판단 등 의미적 판단 필요한 부분
    ↓
  Step 4: Domain Validation (LLM 불필요)
    해결된 모든 값이 실제 데이터 도메인에 존재하는지 검증
    필드 타입 일치 확인 (numeric field에 aggregate, categorical field에 filter)
    ref:nX 참조 유효성 검증
```

### 연구적 의의
- **DataDive 원칙 적용**: "LLM은 생성(diversity)에, deterministic method는 그라운딩(precision)에"
- **Paper 1 참고**: 6-step 각각이 명확한 역할을 가지듯, 4-step 각각이 다른 해결 전략 담당
- **Ablation 가능**: Step 1-2만 (deterministic) vs Step 1-3 (+ LLM) vs Full pipeline 비교 가능

### 코드 변경

#### 파일 생성/수정

| 파일 | 작업 | 설명 |
|------|------|------|
| `opsspec/module_resolve.py` (신규) | 생성 | module_ground.py 대체. ~150줄. 4-step 서브프로세스 구현 |
| `opsspec/resolve_validators.py` (신규) | 생성 | ~100줄. Domain validation 로직 |
| `prompts/opsspec_resolve.md` (신규) | 생성 | Step 3 LLM 프롬프트. 기존 ground.md 대비 더 구조화 |
| `opsspec/module_ground.py` | 삭제 | module_resolve.py로 대체 |
| `prompts/opsspec_ground.md` | 삭제 | opsspec_resolve.md로 대체 |

#### `module_resolve.py` 핵심 구조

```python
def run_resolve_module(
    *,
    llm: StructuredLLMClient,
    prompt_template: str,
    shared_rules: str,
    plan_tree: Dict[str, JsonValue],
    chart_context: ChartContext,       # ← Pydantic 모델 직접 전달 (dict 아님)
    rows_preview: List[Dict[str, JsonValue]],
    validation_feedback: Optional[List[str]] = None,
) -> Dict[str, Any]:
    # Step 1: Deterministic token resolution
    pre_resolved, step1_warnings = _resolve_role_tokens(plan_tree, chart_context)

    # Step 2: Multi-strategy value resolution
    pre_resolved, step2_warnings = _resolve_values(pre_resolved, chart_context)

    # Step 3: LLM-assisted disambiguation (남은 미해결 참조만)
    has_unresolved = _has_unresolved_references(pre_resolved, chart_context)
    if has_unresolved:
        resolved = _llm_disambiguate(llm, prompt_template, shared_rules,
                                     pre_resolved, chart_context, rows_preview,
                                     validation_feedback)
    else:
        resolved = pre_resolved  # LLM 호출 스킵 (결정론적 해결 완료)

    # Step 4: Domain validation
    validated, step4_warnings, errors = validate_grounded_plan(resolved, chart_context)
    if errors:
        raise ValueError("Resolve validation failed:\n- " + "\n- ".join(errors))

    return {
        "grounded_plan_tree": validated,
        "warnings": step1_warnings + step2_warnings + step4_warnings,
    }
```

#### `resolve_validators.py` 핵심 검증 규칙

```python
def validate_grounded_plan(
    plan_tree: Dict, chart_context: ChartContext
) -> Tuple[Dict, List[str], List[str]]:
    """
    검증 항목:
    1. 모든 @token이 해결됨 (미해결 잔류 없음)
    2. field 값이 chart_context.fields에 존재
    3. include/exclude 값이 categorical_values 도메인에 존재
    4. aggregate op의 field가 numeric (measure_fields에 존재)
    5. group 값이 series 도메인에 존재 (series_field가 있을 때)
    6. ref:nX 참조가 유효한 nodeId를 가리킴
    """
```

#### Pipeline에 Module 2 Retry 추가

```python
# pipeline.py 내 Module 2 호출부
max_resolve_attempts = 3
resolve_feedback: List[str] = []

for attempt in range(1, max_resolve_attempts + 1):
    try:
        resolve_payload = run_resolve_module(
            ...,
            validation_feedback=resolve_feedback,
        )
        # Step 4의 validation이 이미 run_resolve_module 내에서 수행됨
        break
    except (ValueError, RuntimeError) as exc:
        resolve_feedback = [line.strip() for line in str(exc).splitlines() if line.strip()]
        if attempt == max_resolve_attempts:
            raise RuntimeError("resolve failed after retries: " + ...) from exc
```

---

## 3. Module 1 (Decompose) 개선 — 중간 규모 변경

### 현재 강점
- Intent classification(내부), few-shot examples, plan_validators, retry loop

### 개선 사항

#### 3-1. 프롬프트 구조화: "분석 → 생성" 분리

현재 프롬프트는 goal-driven planning을 "do NOT output these steps"로 숨기고 있음.
→ 명시적 2-phase 프롬프트로 개선:

```markdown
# Phase 1: Intent Analysis (internal reasoning)
1) goal_type 판별: LIST_TARGETS / RETURN_SCALARS / COMPARE_SCALARS / FIND_EXTREMUM / SET_INTERSECTION
2) explanation 각 문장의 역할 판별: intermediate / final

# Phase 2: Plan Generation (실제 출력)
위 분석에 기반해 minimal plan tree 생성
```

#### 3-2. goal_type은 출력 스키마에서 제거하고 trace/debug에만 결정론적으로 기록

```python
class DecomposeOutput(BaseModel):
    plan_tree: PlanTree
    warnings: List[str]
```

이를 통해:
- Module 1 출력이 단순해짐(PlanTree만)
- goal_type taxonomy 논쟁을 output contract에서 분리(리뷰 리스크 감소)
- Debug/trace에서는 question 기반 `goal_type`을 결정론적으로 추정해 기록 가능

#### 코드 변경

| 파일 | 변경 |
|------|------|
| `opsspec/module_decompose.py` | DecomposeOutput에서 goal_type 제거 (plan_tree만) |
| `prompts/opsspec_decompose.md` | output schema에서 goal_type 제거 |
| `opsspec/validation/plan_validators.py` | question 기반 goal_type deterministic 추정 추가 |
| `opsspec/pipeline.py` | 추정 goal_type을 trace/debug에만 기록 |

---

## 4. Module 3 (Specify) 개선 — 소규모 변경

### 현재 강점
- op_contract 시스템, schema validation, retry loop

### 개선 사항

#### 4-1. 파일 리네이밍
- `module_compile.py` → `module_specify.py`
- `opsspec_compile.md` → `opsspec_specify.md`

#### 4-2. 시스템 프롬프트 개선

현재: "You are module-3 (compile). Compile grounded plan tree to final OpsSpec group map."
→ 개선: "You are the Grammar Specification module. Synthesize the grounded plan into a precise, executable OpsSpec grammar. Each plan node must produce exactly one OperationSpec."

#### 4-3. Cross-module 피드백 경로 추가

Module 3 실패 시 에러 원인 분석:
- **schema 문제** (Module 3 자체 retry로 해결) → 기존 로직 유지
- **grounding 문제** (잘못된 field/value) → Module 2 재실행 트리거

```python
# pipeline.py 내
try:
    specify_result = _run_specify_with_retry(...)
except RuntimeError as exc:
    if _is_grounding_error(exc):
        # Module 2 재실행 후 Module 3 재시도
        resolve_feedback.extend(_extract_grounding_errors(exc))
        resolve_payload = run_resolve_module(..., validation_feedback=resolve_feedback)
        specify_result = _run_specify_with_retry(...)
    else:
        raise
```

#### 코드 변경

| 파일 | 변경 |
|------|------|
| `opsspec/module_compile.py` → `opsspec/module_specify.py` | 리네이밍 + 시스템 프롬프트 개선 |
| `prompts/opsspec_compile.md` → `prompts/opsspec_specify.md` | 리네이밍 |
| `opsspec/pipeline.py` | import 경로 업데이트 + cross-module 피드백 |

---

## 5. Pipeline 수준 개선

### 5-1. Debug 번들 강화

각 모듈의 서브스텝을 명시적으로 기록:

```
00_request.json
01_context.json
02_module1_decompose.json       ← goal_type 포함
03_module2_resolve_step1.json   ← deterministic token resolution 결과
03_module2_resolve_step2.json   ← value resolution 결과 (어떤 전략으로 해결됐는지)
03_module2_resolve_step3.json   ← LLM disambiguation 결과 (호출 여부 포함)
03_module2_resolve_final.json   ← validation 후 최종 결과
04_module3_specify.json
05_final_grammar.json
06_tree_ops_spec.dot
```

### 5-2. Retry 정책 통일

| Module | 현재 | 개선 후 |
|--------|------|---------|
| Decompose | 3회 | 3회 (유지) |
| Resolve | **없음** | **3회 (추가)** |
| Specify | 3회 | 3회 (유지) |

### 5-3. 전체 파이프라인 흐름도 (개선 후)

```
Question + Explanation + Vega-Lite + Data
    ↓
[Context Builder] (deterministic)
    ↓ ChartContext
[Module 1: Decompose] (LLM + retry ×3)
    ↓ PlanTree + goal_type
[Module 2: Resolve]
  ├ Step 1: Token Resolution (deterministic)
  ├ Step 2: Value Resolution (deterministic, multi-strategy)
  ├ Step 3: LLM Disambiguation (조건부 LLM 호출)
  ├ Step 4: Domain Validation (deterministic)
  └ retry ×3
    ↓ GroundedPlanTree
[Module 3: Specify] (LLM + retry ×3)
    ↓ OpsSpec groups
[Canonicalize] (deterministic)
    ↓
Final OpsSpec
```

---

## 6. 수정 대상 파일 목록

| 파일 | 작업 |
|------|------|
| `opsspec/module_resolve.py` | **신규 생성** (~150줄) |
| `opsspec/resolve_validators.py` | **신규 생성** (~100줄) |
| `prompts/opsspec_resolve.md` | **신규 생성** (Step 3 LLM 프롬프트) |
| `opsspec/module_ground.py` | **삭제** (module_resolve.py로 대체) |
| `prompts/opsspec_ground.md` | **삭제** (opsspec_resolve.md로 대체) |
| `opsspec/module_compile.py` → `module_specify.py` | **리네이밍** + 시스템 프롬프트 개선 |
| `prompts/opsspec_compile.md` → `opsspec_specify.md` | **리네이밍** |
| `opsspec/module_decompose.py` | DecomposeOutput에 goal_type 추가 |
| `prompts/opsspec_decompose.md` | 2-phase 프롬프트 구조 개선 |
| `opsspec/pipeline.py` | Module 2 retry 추가, import 경로, cross-module 피드백, debug 번들 강화 |
| `opsspec/models.py` | ResolveOutput 모델 추가 (필요시) |
| `CLAUDE.md` | 모듈 이름/역할 업데이트 |

---

## 7. 논문에서의 프레이밍 (DiaryPlay 패턴 참고)

각 모듈을 DiaryPlay처럼 **Design Challenge → Solution → Justification** 패턴으로 작성:

### Module 1: Explanation Decomposition
- **DC1**: 복합적 자연어 설명을 연산 의도로 분해하는 것은, 설명의 암묵적 구조(중간 계산 vs 최종 결과)를 이해해야 함
- **Solution**: Goal-driven planning — 질문 유형(LIST, COMPARE, EXTREMUM 등) 분류 후 설명 문장별 역할 판별
- **Justification**: Paper 1의 compositional question handling + Paper 2의 candidate generation

### Module 2: Chart-Grounded Resolution
- **DC2**: 추상적 계획 참조를 구체적 차트 데이터에 대응시키는 것은, 이름 변형(GDP vs G.D.P.), 암묵적 참조, 시리즈 모호성 등 다양한 불확실성을 처리해야 함
- **Solution**: Multi-strategy resolution — 결정론적 해결 우선, LLM은 모호성 해소에만 사용
- **Justification**: DataDive의 "LLM for generation, symbolic for grounding" 원칙 + ClaimVis의 fuzzy matching

### Module 3: Grammar Specification
- **DC3**: 검증된 계획을 실행 가능한 문법으로 합성하는 것은, 14개 연산 유형의 파라미터 계약(required/optional/forbidden)을 준수해야 함
- **Solution**: Op contract 기반 schema-constrained generation + 계획-문법 일치 검증
- **Justification**: Paper 1의 template-based generation의 한계를 LLM + strict validation으로 극복

---

## 8. Ablation Study 설계

| 실험 조건 | Module 1 | Module 2 | Module 3 | 목적 |
|-----------|----------|----------|----------|------|
| Full pipeline | Decompose | Resolve (4-step) | Specify | 전체 성능 측정 |
| No resolution | Decompose | Skip (토큰만 치환) | Specify | Module 2의 기여 측정 |
| Deterministic only | Decompose | Step 1-2만 | Specify | LLM disambiguation의 기여 |
| Single LLM | 3모듈을 1번의 LLM 호출로 통합 | — | — | 모듈 분리의 기여 측정 |
| No retry | Decompose (1회) | Resolve (1회) | Specify (1회) | Retry 전략의 기여 |

---

## 9. 검증 방법

1. **Import 검증**: `python3 -c "from opsspec.module_resolve import run_resolve_module; ..."`
2. **기존 테스트 실행**: `cd nlp_server && python3 -m pytest opsspec/tests/ -v`
3. **시나리오 테스트**: `/run_python_plan` 엔드포인트로 expert 시나리오 실행, debug 번들 확인
4. **모듈별 단위 테스트 추가**:
   - `test_resolve_tokens.py`: Step 1 결정론적 토큰 해결
   - `test_resolve_values.py`: Step 2 다중 전략 값 해결
   - `test_resolve_validators.py`: Step 4 도메인 검증
5. **Debug 번들 검사**: `debug/MMddhhmm/` 폴더에 03_module2_resolve_*.json 파일 생성 확인
