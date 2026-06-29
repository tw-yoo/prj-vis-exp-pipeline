"""Baseline (B2) 2단 구조 복구 헬퍼.

baseline planner는 전체 DAG를 한 번에 내고 all-or-nothing 검증을 받기 때문에,
순수 구조 오류(group↔sentenceIndex 불일치) 하나만으로 spec 전체가 폐기되거나
blind replan으로 같은 실수를 반복한다. 이를 두 단계로 완화한다.

- Stage 1 (autorepair_ops_groups): LLM 없이 결정론적으로 고칠 수 있는 cosmetic 오류만
  교정한다. 현재는 meta.sentenceIndex를 그룹 인덱스에 강제 정렬하는 것뿐이다.
  스케줄러/실행기는 group/sentenceIndex가 아니라 meta.inputs/nodeId(DAG)만 보므로
  이 재스탬프는 실행 의미를 바꾸지 않는다(검증만 통과시킨다).

- Stage 2 (build_repair_feedback): 검증/실행 실패 시 planner를 from-scratch 재생성이 아니라
  "자기 직전 spec + 정확한 에러 + 패치 지시"를 받는 informed repair 콜로 바꾼다.
  recursive step-compose가 스텝마다 받던 피드백 루프를 baseline에 1회 부여하는 것과 같다.
"""
from __future__ import annotations

import json
from copy import deepcopy
from typing import Any, Dict, List, Tuple

from ..validation.endpoint_validators import _group_to_sentence_index


def autorepair_ops_groups(raw_groups: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
    """Stage 1: 결정론적 구조 복구(현재는 sentenceIndex 정렬만).

    각 그룹("ops"=1, "opsN"=N)의 모든 op에 대해 meta.sentenceIndex를 그룹 인덱스로 맞춘다.
    그룹명이 op/opsN 형식이 아니면(인덱스 None) 건드리지 않고 검증기가 처리하도록 둔다.

    Returns:
        repaired: 복구된 raw_groups (깊은 복사본)
        notes:    적용한 교정 내역(경고/로깅용)
    """
    repaired = deepcopy(raw_groups)
    notes: List[str] = []

    for group_name, ops in repaired.items():
        sentence_index = _group_to_sentence_index(group_name)
        if sentence_index is None or not isinstance(ops, list):
            continue
        for i, op in enumerate(ops):
            if not isinstance(op, dict):
                continue
            meta = op.get("meta")
            if not isinstance(meta, dict):
                continue
            current = meta.get("sentenceIndex")
            if isinstance(current, int) and current != sentence_index:
                meta["sentenceIndex"] = sentence_index
                notes.append(
                    f'autorepair: group "{group_name}" ops[{i}] '
                    f"sentenceIndex {current} -> {sentence_index}"
                )

    return repaired, notes


def build_repair_feedback(
    prev_raw_groups: Dict[str, Any],
    base_feedback: List[str],
) -> List[str]:
    """Stage 2: 구조화된 검증 피드백에 "직전 spec + 패치 지시"를 덧붙인다.

    planner는 이 feedback을 보고 from-scratch 재생성 대신, 자기 직전 출력에서
    명시된 에러만 고친 전체 spec을 반환해야 한다.
    """
    feedback = list(base_feedback)
    feedback.append(
        "[Repair mode] The JSON below is YOUR previous attempt. Return the SAME spec "
        "with ONLY the errors listed above fixed. Do not redesign or renumber nodes that "
        "are not implicated by an error; keep every other op, nodeId, and ref identical."
    )
    feedback.append(
        "[Previous attempt spec] " + json.dumps(prev_raw_groups, ensure_ascii=True)
    )
    return feedback
