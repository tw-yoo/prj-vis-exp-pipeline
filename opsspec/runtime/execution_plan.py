from __future__ import annotations

from typing import Any, Dict, List

from ..specs.union import OperationSpec


def _group_to_sentence_index(group_name: str) -> int:
    if group_name == "ops":
        return 1
    if group_name.startswith("ops") and group_name[3:].isdigit():
        value = int(group_name[3:])
        return value if value >= 2 else 1
    return 1


def _ordered_group_names(group_names: List[str]) -> List[str]:
    unique: List[str] = []
    seen: set[str] = set()
    for name in group_names:
        if not isinstance(name, str):
            continue
        if name in seen:
            continue
        seen.add(name)
        unique.append(name)
    ordered: List[str] = []
    if "ops" in unique:
        ordered.append("ops")
    ordered.extend(
        sorted(
            [name for name in unique if name.startswith("ops") and name[3:].isdigit()],
            key=lambda name: int(name[3:]),
        )
    )
    ordered.extend(sorted([name for name in unique if name not in ordered]))
    return ordered


def _join_policy_for_op(op_name: str | None) -> str | None:
    if not isinstance(op_name, str) or not op_name:
        return None
    token = op_name.strip()
    if token in {"diff", "compare", "count"}:
        return "keep-split"
    if token == "sum":
        return "merge"
    return "merge"


def _infer_sentence_index_for_group(group_name: str, group_ops: List[OperationSpec]) -> int:
    indices: List[int] = []
    for op in group_ops:
        meta = op.meta if op else None
        sentence_index = getattr(meta, "sentenceIndex", None) if meta else None
        if isinstance(sentence_index, int) and sentence_index >= 1:
            indices.append(int(sentence_index))
    if not indices:
        return _group_to_sentence_index(group_name)
    return min(indices)


def build_sentence_execution_plan(
    *,
    ops_spec: Dict[str, List[OperationSpec]],
    draw_plan_groups: Dict[str, List[Dict[str, Any]]] | None = None,
) -> Dict[str, Any]:
    sentence_to_groups: Dict[int, List[str]] = {}
    ordered_groups = _ordered_group_names(list(ops_spec.keys()))
    for group_name in ordered_groups:
        sentence_index = _infer_sentence_index_for_group(group_name, ops_spec.get(group_name, []))
        sentence_to_groups.setdefault(sentence_index, []).append(group_name)

    draw_groups = draw_plan_groups or {}
    steps: List[Dict[str, Any]] = []
    active_split_groups: set[str] = set()
    for sentence_index in sorted(sentence_to_groups.keys()):
        group_names = sentence_to_groups.get(sentence_index, [])
        split_groups: List[str] = []
        panel_ids: List[str] = []
        join_op_name: str | None = None
        join_policy: str | None = None

        for group_name in group_names:
            for op in ops_spec.get(group_name, []):
                view = op.meta.view if op.meta else None
                if view and isinstance(view.splitGroup, str) and view.splitGroup:
                    split_groups.append(str(view.splitGroup))
                if view and isinstance(view.panelId, str) and view.panelId:
                    panel_ids.append(str(view.panelId))
                if view and view.joinBarrier and join_op_name is None:
                    join_op_name = str(op.op)
                    join_policy = _join_policy_for_op(join_op_name)

        split_group_value: str | None = None
        if split_groups:
            split_group_value = sorted(list(set(split_groups)))[0]

        split_lifecycle: str | None = None
        if split_group_value:
            if join_policy == "merge":
                split_lifecycle = "merge"
                active_split_groups.discard(split_group_value)
            elif split_group_value in active_split_groups:
                split_lifecycle = "keep"
            else:
                split_lifecycle = "enter"
                active_split_groups.add(split_group_value)

        draw_group_names = [name for name in group_names if isinstance(draw_groups.get(name), list)]
        step: Dict[str, Any] = {
            "id": f"s{sentence_index}",
            "sentenceIndex": int(sentence_index),
            "groupNames": group_names,
            "drawGroupNames": draw_group_names,
            "parallel": True,
        }
        if split_group_value:
            step["splitGroup"] = split_group_value
        if split_lifecycle:
            step["splitLifecycle"] = split_lifecycle
        if panel_ids:
            step["panelIds"] = sorted(list(set(panel_ids)))
        if join_op_name:
            step["joinOp"] = join_op_name
        if join_policy:
            step["joinPolicy"] = join_policy
        steps.append(step)

    return {
        "mode": "sentence-step",
        "steps": steps,
    }
