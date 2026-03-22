"""test_grammar.py 정답 spec과 /generate_grammar 출력 비교."""
from __future__ import annotations

import copy
import importlib.util
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from opsspec.specs.base import BaseOpFields

# ────────────────────────────────────────────────────────────────────────────
# Configuration (코드로 on/off)
# ────────────────────────────────────────────────────────────────────────────

# True: 비교 활성화, False: 스킵
COMPARISON_ENABLED = True

# ────────────────────────────────────────────────────────────────────────────
# Internal helpers
# ────────────────────────────────────────────────────────────────────────────

_VALID_GROUP_NAMES = re.compile(r"^ops(\d+)?$")
_REF_PATTERN = re.compile(r"^ref:(n\d+)$")

# 의미 비교 대상 필드 (pipeline이 자동 추가하는 id/meta.source/meta.view/chartId 제외)
_SEMANTIC_FIELDS = {
    "op",
    "field",
    "group",
    "operator",
    "value",
    "targetA",
    "targetB",
    "which",
    "rank",
    "include",
    "exclude",
    "by",
    "groupA",
    "groupB",
    "seriesField",
    "signed",
    "percent",
    "factor",
    "target",
    "fn",
    "n",
    "order",
    "orderField",
    "absolute",
    "aggregate",
    "precision",
    "mode",
    "scale",
    "targetName",
    "from",
}

_META_SEMANTIC_FIELDS = {"inputs", "sentenceIndex"}


# ────────────────────────────────────────────────────────────────────────────
# Public functions
# ────────────────────────────────────────────────────────────────────────────

def serialize_spec_dict(spec_dict: dict) -> Dict[str, List[Dict[str, Any]]]:
    """정답 spec dict를 JSON 직렬화 가능한 dict로 변환한다.

    각 op는 .model_dump(by_alias=True, exclude_none=True)로 직렬화된다.

    Returns:
        {"ops": [{"op": "average", "id": "n1", ...}], "ops2": [...], ...}
    """
    result: Dict[str, List[Dict[str, Any]]] = {}
    for key, ops in spec_dict.items():
        if not isinstance(ops, list):
            continue
        serialized_ops = []
        for op in ops:
            if isinstance(op, BaseOpFields):
                serialized_ops.append(op.model_dump(by_alias=True, exclude_none=True))
            elif isinstance(op, dict):
                serialized_ops.append(op)
        result[key] = serialized_ops
    return result


def strip_pipeline_fields(op_dict: Dict[str, Any]) -> Dict[str, Any]:
    """API 출력 op dict에서 pipeline이 자동 추가한 필드를 제거한다.

    제거 대상: chartId, meta.source, meta.view

    Returns:
        정리된 op dict (원본 수정 없이 새 dict 반환)
    """
    result = copy.deepcopy(op_dict)
    result.pop("chartId", None)
    meta = result.get("meta")
    if isinstance(meta, dict):
        meta.pop("source", None)
        meta.pop("view", None)
    return result


def compare_op_dicts(gt: Dict[str, Any], pred: Dict[str, Any]) -> Dict[str, Any]:
    """두 op dict를 의미 필드만 비교한다.

    Args:
        gt: 정답 op dict (serialize_spec_dict 결과)
        pred: 예측 op dict (strip_pipeline_fields 적용 후)

    Returns:
        {"match": bool, "mismatches": [{"field": str, "expected": any, "got": any}]}
    """
    mismatches: List[Dict[str, Any]] = []

    # 최상위 의미 필드 비교
    all_fields = _SEMANTIC_FIELDS | set(gt.keys()) | set(pred.keys())
    for fname in all_fields:
        if fname not in _SEMANTIC_FIELDS:
            continue
        gt_val = gt.get(fname)
        pred_val = pred.get(fname)
        if gt_val != pred_val:
            mismatches.append({"field": fname, "expected": gt_val, "got": pred_val})

    # meta 내부 의미 필드 비교
    gt_meta = gt.get("meta", {}) or {}
    pred_meta = pred.get("meta", {}) or {}
    for mfield in _META_SEMANTIC_FIELDS:
        gt_val = gt_meta.get(mfield)
        pred_val = pred_meta.get(mfield)
        if gt_val != pred_val:
            mismatches.append({"field": f"meta.{mfield}", "expected": gt_val, "got": pred_val})

    return {"match": len(mismatches) == 0, "mismatches": mismatches}


@dataclass
class SpecCompareResult:
    op_match_count: int
    total_ops: int
    group_match_count: int
    total_groups: int
    details: List[Dict[str, Any]] = field(default_factory=list)

    @property
    def op_accuracy(self) -> float:
        return self.op_match_count / self.total_ops if self.total_ops else 1.0

    @property
    def all_match(self) -> bool:
        return self.op_match_count == self.total_ops

    def report(self) -> str:
        lines = [
            f"op 일치: {self.op_match_count}/{self.total_ops} ({self.op_accuracy:.1%})",
            f"group 일치: {self.group_match_count}/{self.total_groups}",
        ]
        for detail in self.details:
            group = detail["group"]
            gt_count = detail["gt_op_count"]
            pred_count = detail["pred_op_count"]
            if gt_count != pred_count:
                lines.append(f"  {group}: op 개수 불일치 (정답={gt_count}, 예측={pred_count})")
            for op_detail in detail.get("ops", []):
                if not op_detail["match"]:
                    idx = op_detail["index"]
                    lines.append(f"  {group}[{idx}]: 불일치")
                    for mm in op_detail["mismatches"]:
                        lines.append(
                            f"    .{mm['field']}: 기대={mm['expected']!r} / 실제={mm['got']!r}"
                        )
        return "\n".join(lines)


def compare_spec_groups(
    gt: Dict[str, Any],
    pred: Dict[str, Any],
) -> SpecCompareResult:
    """직렬화된 두 spec dict를 그룹별, op별로 비교한다.

    pred의 각 op에는 strip_pipeline_fields가 적용된다.

    Args:
        gt: serialize_spec_dict(ground_truth_spec_dict) 결과
        pred: API 출력의 ops 그룹 dict (draw_plan 등 제외하고 넘길 것)
    """
    if not COMPARISON_ENABLED:
        return SpecCompareResult(
            op_match_count=0, total_ops=0, group_match_count=0, total_groups=0
        )

    # ops 그룹 키만 추출 (draw_plan, execution_plan 등 제외)
    gt_groups = {k: v for k, v in gt.items() if _VALID_GROUP_NAMES.match(k)}
    pred_groups = {k: v for k, v in pred.items() if _VALID_GROUP_NAMES.match(k)}

    all_group_keys = sorted(
        set(gt_groups) | set(pred_groups),
        key=lambda k: 1 if k == "ops" else int(k[3:]),
    )

    op_match_count = 0
    total_ops = 0
    group_match_count = 0
    details: List[Dict[str, Any]] = []

    for group_key in all_group_keys:
        gt_ops: List[Dict[str, Any]] = gt_groups.get(group_key, [])
        pred_ops_raw: List[Dict[str, Any]] = pred_groups.get(group_key, [])
        pred_ops = [strip_pipeline_fields(op) for op in pred_ops_raw]

        gt_count = len(gt_ops)
        pred_count = len(pred_ops)
        total_ops += gt_count

        group_detail: Dict[str, Any] = {
            "group": group_key,
            "gt_op_count": gt_count,
            "pred_op_count": pred_count,
            "ops": [],
        }

        min_len = min(gt_count, pred_count)
        group_all_match = gt_count == pred_count

        for i in range(min_len):
            cmp = compare_op_dicts(gt_ops[i], pred_ops[i])
            group_detail["ops"].append({"index": i, **cmp})
            if cmp["match"]:
                op_match_count += 1
            else:
                group_all_match = False

        details.append(group_detail)
        if group_all_match:
            group_match_count += 1

    return SpecCompareResult(
        op_match_count=op_match_count,
        total_ops=total_ops,
        group_match_count=group_match_count,
        total_groups=len(all_group_keys),
        details=details,
    )


def load_scenario(chart_id: str) -> Optional[Dict[str, Any]]:
    """data/expert/ 하위에서 {chart_id}.py를 찾아 REQUEST dict를 반환한다.

    여러 서브디렉토리가 있으면 가장 처음 발견된 파일을 반환한다.
    파일이 없으면 None을 반환한다.
    """
    # nlp_server 루트 기준으로 data/expert/ 탐색
    root = Path(__file__).parent.parent.parent
    expert_dir = root / "data" / "expert"

    if not expert_dir.exists():
        return None

    for py_file in sorted(expert_dir.rglob(f"{chart_id}.py")):
        spec = importlib.util.spec_from_file_location(f"_scenario_{chart_id}", py_file)
        if spec is None or spec.loader is None:
            continue
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)  # type: ignore[arg-type]
        except Exception:
            continue
        request = getattr(module, "REQUEST", None)
        if isinstance(request, dict):
            return request

    return None
