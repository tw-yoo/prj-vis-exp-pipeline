"""test_grammar.py 정답 spec과 /generate_grammar 출력 비교 테스트."""
from __future__ import annotations

import csv
import json
import os
import uuid
from datetime import datetime, timezone
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
# LLM 설정 (코드로 직접 지정)
# ────────────────────────────────────────────────────────────────────────────

LLM_BACKEND = "openai"  # "openai" | "ollama"
OLLAMA_MODEL = "llama3.1:8b"
OPENAI_MODEL = "gpt-5.2"
OLLAMA_BASE_URL = "http://localhost:11434/v1"
OLLAMA_API_KEY = "ollama"

os.environ["LLM_BACKEND"] = LLM_BACKEND
os.environ["OLLAMA_MODEL"] = OLLAMA_MODEL
os.environ["OPENAI_MODEL"] = OPENAI_MODEL

# ────────────────────────────────────────────────────────────────────────────
# CSV 설정 (코드로 직접 지정)
# ────────────────────────────────────────────────────────────────────────────

EVAL_RESULTS_CSV = Path(__file__).parent / "eval_results.csv"

CSV_COLUMNS = [
    "spec_id",        # spec 변수명 (e.g. spec_0o12tngadmjjux2n)
    "backend",        # pipeline.llm.backend
    "model",          # 실제 사용 모델명
    "gt_spec",        # 정답 spec JSON 문자열
    "success",        # True / False
    "pred_output",    # pipeline 출력 JSON 문자열
    "failure_reason", # cmp.report() (성공 시 "")
    "timestamp",      # ISO 8601
]

# ────────────────────────────────────────────────────────────────────────────
# CSV 헬퍼
# ────────────────────────────────────────────────────────────────────────────


def _load_done_keys() -> set[tuple[str, str, str, str]]:
    """CSV에서 이미 실행된 (spec_id, backend, model, gt_spec) 조합 로드."""
    if not EVAL_RESULTS_CSV.exists():
        return set()
    with EVAL_RESULTS_CSV.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return {(r["spec_id"], r["backend"], r["model"], r["gt_spec"]) for r in reader}


def _append_row(row: dict) -> None:
    """결과를 CSV에 한 행 추가 (파일 없으면 헤더 포함해서 생성)."""
    write_header = not EVAL_RESULTS_CSV.exists()
    with EVAL_RESULTS_CSV.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        if write_header:
            writer.writeheader()
        writer.writerow(row)


def _get_model_name(pipeline: Any) -> str:
    """backend에 따라 실제 모델명 반환."""
    if pipeline.llm.backend == "openai_http":
        return os.getenv("OPENAI_MODEL", "unknown")
    return pipeline.llm.ollama_model or "unknown"


# ────────────────────────────────────────────────────────────────────────────
# 모든 spec_ 변수 수집
# ────────────────────────────────────────────────────────────────────────────

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
    이미 동일한 (spec_id, backend, model, gt_spec) 조합이 CSV에 있으면 skip.
    """
    chart_id = spec_name.removeprefix("spec_")
    scenario = load_scenario(chart_id)

    if scenario is None:
        pytest.skip(f"scenario 파일 없음: chart_id={chart_id}")

    # pipeline 초기화 (LLM 호출 없음 — backend/model 정보만 추출)
    from opsspec.modules.pipeline import OpsSpecPipeline

    pipeline = OpsSpecPipeline(
        ollama_model=OLLAMA_MODEL,
        ollama_base_url=OLLAMA_BASE_URL,
        ollama_api_key=OLLAMA_API_KEY,
        prompts_dir=Path(__file__).parent.parent.parent / "prompts",
    )
    backend = pipeline.llm.backend or "unknown"
    model = _get_model_name(pipeline)

    # ground truth 직렬화
    gt_serialized = serialize_spec_dict(spec_dict)
    gt_spec_json = json.dumps(gt_serialized, ensure_ascii=False)

    # 중복 체크 — 이미 실행된 조합이면 skip
    done_keys = _load_done_keys()
    if (spec_name, backend, model, gt_spec_json) in done_keys:
        pytest.skip(f"이미 실행된 조합: spec_id={spec_name}, backend={backend}, model={model}")

    # pipeline 실행
    result = pipeline.generate(
        question=scenario["question"],
        explanation=scenario["explanation"],
        vega_lite_spec=scenario["vega_lite_spec"],
        data_rows=scenario["data_rows"],
        request_id=f"test_{chart_id}_{uuid.uuid4().hex[:8]}",
        debug=True,
    )

    # pipeline 출력 직렬화 (ops 그룹만, draw_plan 등 제외)
    pred_groups: dict[str, Any] = {
        group_key: [op.model_dump(by_alias=True, exclude_none=True) for op in ops]
        for group_key, ops in result.ops_spec.items()
    }

    cmp: SpecCompareResult = compare_spec_groups(gt_serialized, pred_groups)

    # CSV 기록
    _append_row({
        "spec_id":        spec_name,
        "backend":        backend,
        "model":          model,
        "gt_spec":        gt_spec_json,
        "success":        cmp.all_match,
        "pred_output":    json.dumps(pred_groups, ensure_ascii=False),
        "failure_reason": "" if cmp.all_match else cmp.report(),
        "timestamp":      datetime.now(timezone.utc).isoformat(),
    })

    assert cmp.all_match, (
        f"[{spec_name}] grammar 불일치:\n{cmp.report()}"
    )
