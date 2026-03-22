"""test_grammar.py 정답 spec 검증 + /generate_grammar 출력 비교 pytest 테스트.

실행 방법:
    # 구조 검증 + 직렬화 (LLM 호출 없음, 빠름)
    pytest opsspec/tests/test_grammar_eval.py -v -m "not integration"

    # API 비교 (LLM 호출, 느림)
    pytest opsspec/tests/test_grammar_eval.py -v -m integration
"""
from __future__ import annotations

import uuid
from typing import Any, Dict

import pytest

from opsspec.tests import test_grammar
from opsspec.tests.eval_utils import (
    SpecCompareResult,
    compare_spec_groups,
    load_scenario,
    serialize_spec_dict,
    validate_spec_dict,
)

# ────────────────────────────────────────────────────────────────────────────
# 모든 spec_ 변수 수집
# ────────────────────────────────────────────────────────────────────────────

ALL_SPECS: Dict[str, Any] = {
    name: val
    for name, val in vars(test_grammar).items()
    if name.startswith("spec_") and isinstance(val, dict)
}

# ────────────────────────────────────────────────────────────────────────────
# (1) 구조 검증 테스트
# ────────────────────────────────────────────────────────────────────────────


@pytest.mark.parametrize("spec_name,spec_dict", list(ALL_SPECS.items()))
def test_validate_spec(spec_name: str, spec_dict: dict) -> None:
    """각 ground truth spec이 구조적으로 올바른지 검증한다.

    검증 항목:
    - 그룹 키 순서/갭 없는지 (ops, ops2, ops3, ...)
    - id == meta.nodeId 일치
    - nodeId 중복 없음
    - meta.inputs가 앞선 nodeId만 참조
    - ref:nX 참조가 유효한 nodeId를 가리키는지
    - op별 필수 필드 존재 (NthOp.n, PairDiffOp.by/groupA/groupB 등)
    """
    errors = validate_spec_dict(spec_dict)
    assert not errors, f"[{spec_name}] 구조 검증 오류:\n" + "\n".join(errors)


# ────────────────────────────────────────────────────────────────────────────
# (2) 직렬화 가능성 테스트
# ────────────────────────────────────────────────────────────────────────────


@pytest.mark.parametrize("spec_name,spec_dict", list(ALL_SPECS.items()))
def test_serialize_spec(spec_name: str, spec_dict: dict) -> None:
    """각 ground truth spec이 JSON 직렬화 가능한지 확인한다."""
    serialized = serialize_spec_dict(spec_dict)

    assert serialized, f"[{spec_name}] 직렬화 결과가 비어 있음"
    assert all(
        isinstance(v, list) for v in serialized.values()
    ), f"[{spec_name}] 모든 그룹 값이 list여야 함"
    assert all(
        isinstance(op, dict)
        for ops in serialized.values()
        for op in ops
    ), f"[{spec_name}] 모든 op가 dict여야 함"

    # 각 op에 'op' 필드(type discriminator)가 있는지
    for group_key, ops in serialized.items():
        for i, op in enumerate(ops):
            assert "op" in op, f"[{spec_name}] {group_key}[{i}]: 'op' 필드 없음"


# ────────────────────────────────────────────────────────────────────────────
# (3) API 출력 vs 정답 비교 테스트 (integration, LLM 호출)
# ────────────────────────────────────────────────────────────────────────────


@pytest.mark.integration
@pytest.mark.parametrize("spec_name,spec_dict", list(ALL_SPECS.items()))
def test_grammar_matches_ground_truth(spec_name: str, spec_dict: dict) -> None:
    """pipeline 출력이 ground truth spec과 일치하는지 검증한다.

    scenario 파일(data/expert/.../{chart_id}.py)이 없으면 skip.
    """
    chart_id = spec_name.removeprefix("spec_")
    scenario = load_scenario(chart_id)

    if scenario is None:
        pytest.skip(f"scenario 파일 없음: chart_id={chart_id}")

    # pipeline 직접 호출 (HTTP 서버 불필요)
    from opsspec.modules.pipeline import OpsSpecPipeline

    pipeline = OpsSpecPipeline()
    result = pipeline.generate(
        question=scenario["question"],
        explanation=scenario["explanation"],
        vega_lite_spec=scenario["vega_lite_spec"],
        data_rows=scenario["data_rows"],
        request_id=f"test_{chart_id}_{uuid.uuid4().hex[:8]}",
        debug=False,
    )

    # ground truth 직렬화
    gt_serialized = serialize_spec_dict(spec_dict)

    # pipeline 출력 직렬화 (ops 그룹만, draw_plan 등 제외)
    pred_groups: Dict[str, Any] = {
        group_key: [op.model_dump(by_alias=True, exclude_none=True) for op in ops]
        for group_key, ops in result.ops_spec.items()
    }

    cmp: SpecCompareResult = compare_spec_groups(gt_serialized, pred_groups)

    assert cmp.all_match, (
        f"[{spec_name}] grammar 불일치:\n{cmp.report()}"
    )
