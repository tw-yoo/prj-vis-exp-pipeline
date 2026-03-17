from __future__ import annotations

from typing import Any, Dict, List, Literal, Set

from .artifacts import extract_scalar_ref_deps
from ..specs.union import OperationSpec

NodeResultKind = Literal["source-backed", "source-aggregate", "synthetic-result"]


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


def _node_sort_key(value: Any) -> tuple[int, str]:
    text = str(value or "")
    if text.startswith("n") and text[1:].isdigit():
        return (int(text[1:]), text)
    return (10**9, text)


def _op_node_id(op: OperationSpec) -> str:
    node_id = getattr(op.meta, "nodeId", None) if op.meta else None
    if isinstance(node_id, str) and node_id:
        return node_id
    if isinstance(op.id, str) and op.id:
        return op.id
    return str(op.op or "op")


def _collect_sentence_groups(ops_spec: Dict[str, List[OperationSpec]]) -> Dict[int, List[str]]:
    sentence_to_groups: Dict[int, List[str]] = {}
    ordered_groups = _ordered_group_names(list(ops_spec.keys()))
    for group_name in ordered_groups:
        sentence_index = _infer_sentence_index_for_group(group_name, ops_spec.get(group_name, []))
        sentence_to_groups.setdefault(sentence_index, []).append(group_name)
    return sentence_to_groups


def _scalar_dep_ids(op: OperationSpec) -> List[str]:
    dumped = op.model_dump(by_alias=True, exclude_none=True)
    dumped.pop("meta", None)
    deps = extract_scalar_ref_deps(dumped)
    return sorted(list(deps), key=_node_sort_key)


def _direct_input_ids(op: OperationSpec) -> List[str]:
    inputs = list((op.meta.inputs or []) if op.meta else [])
    return sorted([str(value) for value in inputs if isinstance(value, str) and value], key=_node_sort_key)


def _selector_has_ref(value: Any) -> bool:
    if isinstance(value, str):
        return value.startswith("ref:")
    if isinstance(value, list):
        return any(_selector_has_ref(entry) for entry in value)
    if hasattr(value, "model_dump"):
        return _selector_has_ref(value.model_dump(exclude_none=True))
    if isinstance(value, dict):
        category = value.get("category") or value.get("target")
        selector_id = value.get("id")
        selector_ref = isinstance(selector_id, str) and (
            selector_id.startswith("ref:") or (
                selector_id.startswith("n") and selector_id[1:].isdigit()
            )
        )
        return _selector_has_ref(category) or selector_ref
    return False


def _classify_node_result_kind(
    op: OperationSpec,
    *,
    node_kinds: Dict[str, NodeResultKind],
) -> NodeResultKind:
    op_name = str(op.op or "").strip()
    inputs = _direct_input_ids(op)

    if op_name in {"average", "sum", "count", "determineRange"}:
        return "source-aggregate" if not inputs else "synthetic-result"

    if op_name in {"diff", "add", "scale", "compareBool", "pairDiff", "lagDiff"}:
        return "synthetic-result"

    if op_name == "compare":
        input_kinds = [node_kinds.get(node_id, "synthetic-result") for node_id in inputs]
        if input_kinds and any(kind != "source-backed" for kind in input_kinds):
            return "synthetic-result"

    return "source-backed"


def _build_node_kind_map(ops_spec: Dict[str, List[OperationSpec]]) -> Dict[str, NodeResultKind]:
    node_kinds: Dict[str, NodeResultKind] = {}
    ordered_groups = _ordered_group_names(list(ops_spec.keys()))
    ordered_ops: List[OperationSpec] = []
    for group_name in ordered_groups:
        ordered_ops.extend(ops_spec.get(group_name, []))
    ordered_ops.sort(key=lambda op: _node_sort_key(_op_node_id(op)))

    for op in ordered_ops:
        node_id = _op_node_id(op)
        kind = _classify_node_result_kind(op, node_kinds=node_kinds)
        node_kinds[node_id] = kind
        if isinstance(op.id, str) and op.id:
            node_kinds[op.id] = kind
    return node_kinds


def _merge_operand_kinds(kinds: List[NodeResultKind]) -> NodeResultKind | None:
    if not kinds:
        return None
    if "synthetic-result" in kinds:
        return "synthetic-result"
    if "source-aggregate" in kinds:
        return "source-aggregate"
    return "source-backed"


def _selector_operand_kind(value: Any, *, node_kinds: Dict[str, NodeResultKind]) -> NodeResultKind | None:
    if value is None:
        return None
    if isinstance(value, str):
        if value.startswith("ref:"):
            return node_kinds.get(value[len("ref:") :], "synthetic-result")
        return "source-backed"
    if isinstance(value, list):
        merged = [
            kind
            for entry in value
            for kind in [_selector_operand_kind(entry, node_kinds=node_kinds)]
            if kind is not None
        ]
        return _merge_operand_kinds(merged)
    if hasattr(value, "model_dump"):
        return _selector_operand_kind(value.model_dump(exclude_none=True), node_kinds=node_kinds)
    if isinstance(value, dict):
        selector_id = value.get("id")
        if isinstance(selector_id, str):
            if selector_id.startswith("ref:"):
                return node_kinds.get(selector_id[len("ref:") :], "synthetic-result")
            if selector_id.startswith("n") and selector_id[1:].isdigit():
                return node_kinds.get(selector_id, "synthetic-result")
        category = value.get("category") or value.get("target")
        if isinstance(category, str) and category.startswith("ref:"):
            return node_kinds.get(category[len("ref:") :], "synthetic-result")
        return "source-backed"
    return None


def _prefilter_substeps(op: OperationSpec, *, group_name: str) -> List[Dict[str, Any]]:
    node_id = _op_node_id(op)
    out: List[Dict[str, Any]] = []

    group = getattr(op, "group", None)
    if isinstance(group, str) and group.strip():
        out.append(
            {
                "id": f"{node_id}_prefilter_group",
                "kind": "prefilter",
                "groupName": group_name,
                "nodeId": node_id,
                "opName": str(op.op),
                "label": f"filter group {group.strip()}",
                "visible": True,
                "scope": {"groups": [group.strip()], "role": "shared"},
            }
        )

    group_a = getattr(op, "groupA", None)
    if isinstance(group_a, str) and group_a.strip():
        out.append(
            {
                "id": f"{node_id}_prefilter_left",
                "kind": "prefilter",
                "groupName": group_name,
                "nodeId": node_id,
                "opName": str(op.op),
                "label": f"filter left operand {group_a.strip()}",
                "visible": True,
                "scope": {"groups": [group_a.strip()], "role": "left"},
            }
        )

    group_b = getattr(op, "groupB", None)
    if isinstance(group_b, str) and group_b.strip():
        out.append(
            {
                "id": f"{node_id}_prefilter_right",
                "kind": "prefilter",
                "groupName": group_name,
                "nodeId": node_id,
                "opName": str(op.op),
                "label": f"filter right operand {group_b.strip()}",
                "visible": True,
                "scope": {"groups": [group_b.strip()], "role": "right"},
            }
        )

    return out


def _materialization_template(op: OperationSpec, *, node_kinds: Dict[str, NodeResultKind]) -> str | None:
    op_name = str(op.op or "").strip()
    scalar_deps = _scalar_dep_ids(op)
    inputs = _direct_input_ids(op)
    scalar_count = len(scalar_deps)
    input_count = len(inputs)

    if op_name in {"average", "sum", "count"} and input_count >= 1:
        return "operand-only-chart"
    if op_name in {"diff", "compare", "compareBool", "add"}:
        left_kind = _selector_operand_kind(getattr(op, "targetA", None), node_kinds=node_kinds)
        right_kind = _selector_operand_kind(getattr(op, "targetB", None), node_kinds=node_kinds)
        kinds = [kind for kind in [left_kind, right_kind] if kind is not None]
        if kinds and "synthetic-result" in kinds:
            synthetic_count = sum(1 for kind in kinds if kind == "synthetic-result")
            return "two-value-chart" if synthetic_count >= 2 else "mixed-operands-chart"
        return None
    if op_name == "scale":
        target_kind = _selector_operand_kind(getattr(op, "target", None), node_kinds=node_kinds)
        return "scalar-reference-chart" if target_kind == "synthetic-result" else None
    if scalar_count >= 1 and input_count >= 1:
        return "mixed-operands-chart"
    if any(_prefilter_substeps(op, group_name="")):
        return "filtered-operands-chart"
    return None


def _materialize_surface_substep(
    op: OperationSpec, *, group_name: str, node_kinds: Dict[str, NodeResultKind]
) -> Dict[str, Any] | None:
    template = _materialization_template(op, node_kinds=node_kinds)
    if template is None:
        return None
    node_id = _op_node_id(op)
    input_ids = _direct_input_ids(op)
    scalar_ids = _scalar_dep_ids(op)
    source_node_ids = sorted(list({*input_ids, *scalar_ids}), key=_node_sort_key)
    return {
        "id": f"{node_id}_surface",
        "kind": "materialize-surface",
        "groupName": group_name,
        "nodeId": node_id,
        "opName": str(op.op),
        "label": f"materialize {template}",
        "visible": True,
        "surface": {
            "surfaceType": "derived-chart",
            "templateType": template,
            "sourceNodeIds": source_node_ids,
            "syntheticLabels": "semantic",
            "layout": "full-canvas",
        },
    }


def _run_op_substep(
    op: OperationSpec, *, group_name: str, node_kinds: Dict[str, NodeResultKind]
) -> Dict[str, Any]:
    node_id = _op_node_id(op)
    input_ids = _direct_input_ids(op)
    scalar_ids = _scalar_dep_ids(op)
    source_node_ids = sorted(list({*input_ids, *scalar_ids}), key=_node_sort_key)
    template = _materialization_template(op, node_kinds=node_kinds)
    return {
        "id": f"{node_id}_run",
        "kind": "run-op",
        "groupName": group_name,
        "nodeId": node_id,
        "opName": str(op.op),
        "label": f"run {str(op.op)}",
        "visible": True,
        "sourceNodeIds": source_node_ids,
        "surface": {
            "surfaceType": "derived-chart" if template else "source-chart",
            "templateType": template or "source-chart",
            "keepOnComplete": True,
        },
    }


def build_visual_execution_plan(*, ops_spec: Dict[str, List[OperationSpec]]) -> Dict[str, Any]:
    sentence_to_groups = _collect_sentence_groups(ops_spec)
    node_kinds = _build_node_kind_map(ops_spec)
    steps: List[Dict[str, Any]] = []

    for sentence_index in sorted(sentence_to_groups.keys()):
        group_names = sentence_to_groups.get(sentence_index, [])
        substeps: List[Dict[str, Any]] = []

        ordered_ops: List[tuple[str, OperationSpec]] = []
        for group_name in group_names:
            for op in ops_spec.get(group_name, []):
                ordered_ops.append((group_name, op))
        ordered_ops.sort(key=lambda item: _node_sort_key(_op_node_id(item[1])))

        for group_name, op in ordered_ops:
            substeps.extend(_prefilter_substeps(op, group_name=group_name))
            materialize = _materialize_surface_substep(
                op,
                group_name=group_name,
                node_kinds=node_kinds,
            )
            if materialize is not None:
                substeps.append(materialize)
            substeps.append(_run_op_substep(op, group_name=group_name, node_kinds=node_kinds))

        steps.append(
            {
                "id": f"s{sentence_index}",
                "sentenceIndex": int(sentence_index),
                "groupNames": group_names,
                "navigationUnit": "sentence",
                "surfacePolicy": "keep-final-derived-chart",
                "substeps": substeps,
            }
        )

    return {
        "mode": "linear-derived-chart-flow",
        "steps": steps,
        "reusePolicy": "result-only",
    }
