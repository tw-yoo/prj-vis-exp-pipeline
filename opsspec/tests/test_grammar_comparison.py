"""test_grammar.py 정답 spec과 /generate_grammar 출력 비교 테스트."""
from __future__ import annotations

import os
import uuid
from pathlib import Path
from typing import Any

import pytest

from opsspec.tests import test_grammar
from opsspec.tests.comparators import (
    SpecCompareResult,
    compare_spec_groups,
    load_scenario,
    serialize_spec_dict,
)

# ────────────────────────────────────────────────────────────────────────────
# 모든 spec_ 변수 수집
# ────────────────────────────────────────────────────────────────────────────

# ────────────────────────────────────────────────────────────────────────────
# LLM 설정 (코드로 직접 지정)
# ────────────────────────────────────────────────────────────────────────────

LLM_BACKEND   = "ollama"                   # "openai" | "ollama"
OLLAMA_MODEL  = "qwen2.5-coder:1.5b"       # ollama 사용 시 모델명
OPENAI_MODEL  = "gpt-4o-mini"              # openai 사용 시 모델명
OLLAMA_BASE_URL = "http://localhost:11434/v1"
OLLAMA_API_KEY  = "ollama"

os.environ["LLM_BACKEND"] = LLM_BACKEND
os.environ["OLLAMA_MODEL"] = OLLAMA_MODEL
os.environ["OPENAI_MODEL"] = OPENAI_MODEL

ALL_SPECS: dict[str, dict] = {
    name: val
    for name, val in vars(test_grammar).items()
    if name.startswith("spec_") and isinstance(val, dict)
}

# ────────────────────────────────────────────────────────────────────────────
# API 출력 vs 정답 비교 테스트 (ground truth 검증)
# ────────────────────────────────────────────────────────────────────────────


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

    pipeline = OpsSpecPipeline(
        ollama_model=OLLAMA_MODEL,
        ollama_base_url=OLLAMA_BASE_URL,
        ollama_api_key=OLLAMA_API_KEY,
        prompts_dir=Path(__file__).parent.parent.parent / "prompts",
    )
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
    pred_groups: dict[str, Any] = {
        group_key: [op.model_dump(by_alias=True, exclude_none=True) for op in ops]
        for group_key, ops in result.ops_spec.items()
    }

    cmp: SpecCompareResult = compare_spec_groups(gt_serialized, pred_groups)

    assert cmp.all_match, (
        f"[{spec_name}] grammar 불일치:\n{cmp.report()}"
    )
