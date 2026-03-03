from __future__ import annotations

from copy import deepcopy
from typing import Dict, List, Set

from opsspec.specs.base import OpsMetaView
from opsspec.specs.union import OperationSpec


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
    remaining = dict(edges)
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
                        view_dict.setdefault("parallelGroup", gid)
                        op.meta.view = OpsMetaView(**view_dict)

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
            if node in join_nodes:
                for parent in edges.get(node, []):
                    for ops2 in scheduled.values():
                        for op2 in ops2:
                            if op2.meta and op2.meta.nodeId == parent:
                                v = op2.meta.view or OpsMetaView()
                                vd = v.model_dump() if hasattr(v, "model_dump") else dict(v)
                                vd.setdefault("split", "horizontal")
                                op2.meta.view = OpsMetaView(**vd)
            op.meta.view = OpsMetaView(**view_dict)
    return scheduled
