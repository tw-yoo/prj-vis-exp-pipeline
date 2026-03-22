"""test_grammar.py 정답 spec 검증/직렬화/비교 유틸리티."""
from __future__ import annotations

import copy
import importlib.util
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from opsspec.specs.base import BaseOpFields

# ────────────────────────────────────────────────────────────────────────────
# Internal helpers
# ────────────────────────────────────────────────────────────────────────────

_VALID_GROUP_NAMES = re.compile(r"^ops(\d+)?$")
_REF_PATTERN = re.compile(r"^ref:(n\d+)$")

# op별 필수 필드 정의
_OP_REQUIRED_FIELDS: Dict[str, List[str]] = {
    "nth": ["n"],
    "pairDiff": ["by", "groupA", "groupB"],
    "add": ["targetA", "targetB"],
    "scale": ["target", "factor"],
    "setOp": ["fn"],
    "compareBool": ["operator"],
}

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


def _collect_ref_ids(value: Any) -> List[str]:
    """value 내 모든 ref:nX 패턴의 nodeId를 수집한다."""
    results: List[str] = []
    if isinstance(value, str):
        m = _REF_PATTERN.match(value)
        if m:
            results.append(m.group(1))
    elif isinstance(value, list):
        for item in value:
            results.extend(_collect_ref_ids(item))
    elif isinstance(value, dict):
        for v in value.values():
            results.extend(_collect_ref_ids(v))
    return results


def _op_to_dict(op: BaseOpFields) -> Dict[str, Any]:
    return op.model_dump(by_alias=True, exclude_none=True)


def _expected_group_key(index: int) -> str:
    """sentenceIndex 1 → 'ops', 2 → 'ops2', ..."""
    return "ops" if index == 1 else f"ops{index}"


# ────────────────────────────────────────────────────────────────────────────
# (1) validate_spec_dict
# ────────────────────────────────────────────────────────────────────────────

def validate_spec_dict(spec_dict: dict) -> List[str]:
    """정답 spec dict의 구조적 유효성을 검사한다.

    Returns:
        오류 메시지 리스트. 빈 리스트 = valid.
    """
    errors: List[str] = []

    # 1. 그룹 키 검증 ─ ops, ops2, ops3, ... 순서대로 gap 없이
    keys = list(spec_dict.keys())
    invalid_keys = [k for k in keys if not _VALID_GROUP_NAMES.match(k)]
    if invalid_keys:
        errors.append(f"올바르지 않은 그룹 키: {invalid_keys}")

    # 숫자 정렬: ops=1, ops2=2, ...
    def _key_order(k: str) -> int:
        return 1 if k == "ops" else int(k[3:])

    valid_keys = [k for k in keys if _VALID_GROUP_NAMES.match(k)]
    sorted_indices = sorted(_key_order(k) for k in valid_keys)
    expected_indices = list(range(1, len(sorted_indices) + 1))
    if sorted_indices != expected_indices:
        errors.append(
            f"그룹 키 순서/갭 오류: 있는 인덱스={sorted_indices}, 기대={expected_indices}"
        )

    # 2. op 순서대로 순회 (groups 순서 유지)
    seen_node_ids: List[str] = []  # 앞서 정의된 nodeId 목록 (순서 중요)
    seen_node_id_set: set = set()

    for group_key in sorted(valid_keys, key=_key_order):
        ops = spec_dict.get(group_key, [])
        if not isinstance(ops, list):
            errors.append(f"{group_key}: list가 아님 (type={type(ops).__name__})")
            continue

        for i, op in enumerate(ops):
            prefix = f"{group_key}[{i}]"

            # 2a. BaseOpFields 인스턴스 확인
            if not isinstance(op, BaseOpFields):
                errors.append(f"{prefix}: BaseOpFields 인스턴스가 아님 (type={type(op).__name__})")
                continue

            op_type = op.op
            node_id = op.meta.nodeId if op.meta else None
            op_id = op.id

            # 2b. id == meta.nodeId 일치
            if op_id and node_id and op_id != node_id:
                errors.append(f"{prefix}({op_type}): id='{op_id}'와 meta.nodeId='{node_id}' 불일치")

            # 2c. nodeId 존재 여부
            if not node_id:
                errors.append(f"{prefix}({op_type}): meta.nodeId 없음")
            else:
                # 2d. nodeId 중복
                if node_id in seen_node_id_set:
                    errors.append(f"{prefix}({op_type}): nodeId '{node_id}' 중복")
                else:
                    seen_node_id_set.add(node_id)
                    seen_node_ids.append(node_id)

            # 2e. meta.inputs가 앞서 정의된 nodeId만 참조하는지
            inputs: List[str] = op.meta.inputs if op.meta else []
            for inp in inputs:
                if inp not in seen_node_id_set or inp == node_id:
                    errors.append(
                        f"{prefix}({op_type}): meta.inputs의 '{inp}'가 앞서 정의된 nodeId가 아님"
                    )

            # 2f. 필드 내 ref:nX 참조가 유효한지
            op_dict = _op_to_dict(op)
            for fname, fval in op_dict.items():
                if fname in ("op", "id", "meta", "chartId"):
                    continue
                ref_ids = _collect_ref_ids(fval)
                for ref_id in ref_ids:
                    if ref_id not in seen_node_id_set:
                        errors.append(
                            f"{prefix}({op_type}).{fname}: 'ref:{ref_id}'가 정의되지 않은 nodeId를 참조"
                        )

            # 2g. op별 필수 필드
            required = _OP_REQUIRED_FIELDS.get(op_type, [])
            for req_field in required:
                val = getattr(op, req_field, None)
                if val is None:
                    errors.append(f"{prefix}({op_type}): 필수 필드 '{req_field}' 없음")

    return errors


# ────────────────────────────────────────────────────────────────────────────
# (2) serialize_spec_dict
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


# ────────────────────────────────────────────────────────────────────────────
# (3) strip_pipeline_fields
# ────────────────────────────────────────────────────────────────────────────

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


# ────────────────────────────────────────────────────────────────────────────
# (4) compare_op_dicts
# ────────────────────────────────────────────────────────────────────────────

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


# ────────────────────────────────────────────────────────────────────────────
# (5) SpecCompareResult + compare_spec_groups
# ────────────────────────────────────────────────────────────────────────────

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


# ────────────────────────────────────────────────────────────────────────────
# (6) load_scenario
# ────────────────────────────────────────────────────────────────────────────

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
