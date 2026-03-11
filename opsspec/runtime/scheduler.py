from __future__ import annotations

from copy import deepcopy
from typing import Dict, List, Set

from opsspec.specs.base import OpsMetaView
from opsspec.specs.union import OperationSpec


def _node_sort_key(node_id: str) -> tuple[int, str]:
    if isinstance(node_id, str) and node_id.startswith("n") and node_id[1:].isdigit():
        return (int(node_id[1:]), node_id)
    return (10**9, str(node_id))


def _collect_edges(groups: Dict[str, List[OperationSpec]]) -> Dict[str, Set[str]]:
    edges: Dict[str, Set[str]] = {}
    for ops in groups.values():
        for op in ops:
            if not op.meta or not op.meta.nodeId:
                continue
            node = op.meta.nodeId
            parents = set(op.meta.inputs or [])
            edges[node] = parents
    return edges


def _topo_phases(edges: Dict[str, Set[str]]) -> Dict[str, int]:
    phase: Dict[str, int] = {}
    remaining = {node: set(parents) for node, parents in edges.items()}
    while remaining:
        roots = [n for n, parents in remaining.items() if not parents]
        if not roots:
            # cycle safety: assign rest to next phase and break
            for n in remaining.keys():
                phase[n] = max(phase.values() or [0]) + 1
            break
        current_phase = max(phase.values() or [0]) + 1
        for r in roots:
            phase[r] = current_phase
            remaining.pop(r, None)
        for parents in remaining.values():
            parents.difference_update(roots)
    return phase


def _parallel_groups(edges: Dict[str, Set[str]], phases: Dict[str, int]) -> Dict[int, List[str]]:
    per_phase: Dict[int, List[str]] = {}
    for node, ph in phases.items():
        per_phase.setdefault(ph, []).append(node)
    return per_phase


def _index_nodes(groups: Dict[str, List[OperationSpec]]) -> Dict[str, OperationSpec]:
    node_map: Dict[str, OperationSpec] = {}
    for ops in groups.values():
        for op in ops:
            if not op.meta or not op.meta.nodeId:
                continue
            node_map[op.meta.nodeId] = op
    return node_map


def _ancestor_closure(start: str, edges: Dict[str, Set[str]]) -> Set[str]:
    visited: Set[str] = set()
    stack: List[str] = [start]
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        for parent in sorted(edges.get(node, set()), key=_node_sort_key):
            if parent not in visited:
                stack.append(parent)
    return visited


def _merge_view(op: OperationSpec, **updates: object) -> None:
    if not op.meta:
        return
    view = op.meta.view or OpsMetaView()
    view_dict = view.model_dump() if hasattr(view, "model_dump") else dict(view)
    for key, value in updates.items():
        if value is None:
            continue
        view_dict[key] = value
    op.meta.view = OpsMetaView(**view_dict)


def _annotate_fork_join_splits(
    groups: Dict[str, List[OperationSpec]],
    *,
    edges: Dict[str, Set[str]],
    phases: Dict[str, int],
) -> None:
    node_map = _index_nodes(groups)
    assigned_nodes: Set[str] = set()
    join_nodes = sorted(
        [node for node, parents in edges.items() if len(parents) == 2],
        key=lambda node: (phases.get(node, 10**9), _node_sort_key(node)),
    )

    for join_node in join_nodes:
        parents = sorted(edges.get(join_node, set()), key=_node_sort_key)
        if len(parents) != 2:
            continue

        branch_sets: List[Set[str]] = []
        valid = True
        for parent in parents:
            branch = _ancestor_closure(parent, edges)
            if not branch:
                valid = False
                break
            if branch & assigned_nodes:
                valid = False
                break
            branch_sets.append(branch)

        if not valid or len(branch_sets) != 2:
            continue
        if branch_sets[0] & branch_sets[1]:
            continue

        split_group = f"sg_{join_node}"
        panel_ids = ("left", "right")
        for panel_id, branch in zip(panel_ids, branch_sets):
            for node_id in sorted(branch, key=_node_sort_key):
                op = node_map.get(node_id)
                if op is None:
                    continue
                _merge_view(
                    op,
                    split="horizontal",
                    splitGroup=split_group,
                    panelId=panel_id,
                    parallelGroup=split_group,
                )
                assigned_nodes.add(node_id)

        join_op = node_map.get(join_node)
        if join_op is not None:
            _merge_view(
                join_op,
                split="horizontal",
                splitGroup=split_group,
                joinBarrier=True,
            )


def schedule_ops_spec(groups: Dict[str, List[OperationSpec]]) -> Dict[str, List[OperationSpec]]:
    scheduled = deepcopy(groups)
    edges = _collect_edges(scheduled)
    phases = _topo_phases(edges)
    per_phase = _parallel_groups(edges, phases)

    # detect join nodes (multiple parents)
    join_nodes: Set[str] = {n for n, parents in edges.items() if len(parents) >= 2}
    # pick a deterministic parallel group id per phase
    for ph, nodes in per_phase.items():
        if len(nodes) <= 1:
            continue
        gid = f"p{ph}"
        for n in nodes:
            for ops in scheduled.values():
                for op in ops:
                    if op.meta and op.meta.nodeId == n:
                        view = op.meta.view or OpsMetaView()
                        view_dict = view.model_dump() if hasattr(view, "model_dump") else dict(view)
                        if not view_dict.get("parallelGroup"):
                            view_dict["parallelGroup"] = gid
                        op.meta.view = OpsMetaView(**view_dict)

    _annotate_fork_join_splits(scheduled, edges=edges, phases=phases)

    # annotate phase + split hints around joins
    for ops in scheduled.values():
        for op in ops:
            if not op.meta or not op.meta.nodeId:
                continue
            node = op.meta.nodeId
            ph = phases.get(node)
            view = op.meta.view or OpsMetaView()
            view_dict = view.model_dump() if hasattr(view, "model_dump") else dict(view)
            if ph is not None:
                view_dict["phase"] = ph
            # mark parents of join for split hint
            if node in join_nodes and not view_dict.get("joinBarrier"):
                for parent in edges.get(node, []):
                    for ops2 in scheduled.values():
                        for op2 in ops2:
                            if op2.meta and op2.meta.nodeId == parent:
                                v = op2.meta.view or OpsMetaView()
                                vd = v.model_dump() if hasattr(v, "model_dump") else dict(v)
                                if not vd.get("split"):
                                    vd["split"] = "horizontal"
                                op2.meta.view = OpsMetaView(**vd)
            op.meta.view = OpsMetaView(**view_dict)
    return scheduled
