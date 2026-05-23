from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

from ..core.types import JsonValue
from ..specs.union import OperationSpec, parse_operation_spec


@dataclass(frozen=True)
class FewShotBundle:
    text: str
    ids: List[str]


@dataclass(frozen=True)
class FewShotBudget:
    inventory_max_examples: int
    inventory_max_chars: int
    step_max_examples: int
    step_max_chars: int
    step_steps_per_example: int


@dataclass(frozen=True)
class _ExampleRecord:
    ex_id: str
    question: str
    explanation: str
    chart_context: Dict[str, Any]
    spec: Dict[str, List[OperationSpec]]
    op_names: Set[str]
    mark: str
    is_stacked: bool
    has_series: bool
    family: str


_KEYWORD_TO_OPS: Dict[str, Tuple[str, ...]] = {
    "average": ("average",),
    "mean": ("average",),
    "sum": ("sum", "add"),
    "add": ("add",),
    "total": ("sum", "add"),
    "count": ("count",),
    "how many": ("count",),
    "difference": ("diff", "pairDiff", "lagDiff"),
    "diff": ("diff", "pairDiff", "lagDiff"),
    "change": ("diff", "lagDiff"),
    "compare": ("compareBool", "diffByValue"),
    "bigger": ("compareBool",),
    "greater": ("compareBool", "filter"),
    "above": ("filter",),
    "below": ("filter",),
    "filter": ("filter",),
    "between": ("filter",),
    "from": ("filter",),
    "highest": ("findExtremum",),
    "lowest": ("findExtremum",),
    "second": ("findExtremum", "nth"),
    "retrieve": ("retrieveValue",),
    "value of": ("retrieveValue",),
    "double": ("scale",),
    "pair": ("pairDiff",),
    "lag": ("lagDiff",),
    # "intersection"/"union" are no longer mapped to a dedicated op; chained filters
    # (or a single filter with combined include list) express the same outcome.
    "common to both": ("filter",),
    "in both": ("filter",),
    "shared between": ("filter",),
    "appear in both": ("filter",),
    "either a or b": ("filter",),
    "intersection of": ("filter",),
    # Expanded-field patterns (diff.percent / mode / aggregate)
    "ratio": ("diff",),
    "times as": ("diff",),
    "fold": ("diff", "scale"),
    "percent change": ("diff",),
    "percentage change": ("diff",),
    "% change": ("diff",),
    "% increase": ("diff",),
    "% decrease": ("diff",),
    "share of": ("diff",),
    "fraction of": ("diff",),
    "percent of total": ("diff",),
    # nth.from / orderField patterns
    "leftmost": ("nth",),
    "rightmost": ("nth",),
    "from the left": ("nth",),
    "from the right": ("nth",),
    # sort.orderField patterns
    "sorted by": ("sort",),
    "in order of": ("sort",),
    "ordered by": ("sort",),
    "chronological": ("sort", "lagDiff"),
    # lagDiff chronological phrases
    "year-over-year": ("lagDiff",),
    "yoy": ("lagDiff",),
    "month-over-month": ("lagDiff",),
    "previous period": ("lagDiff",),
    "previous year": ("lagDiff",),
    # pairDiff.absolute / diff signed=false
    "absolute difference": ("diff", "pairDiff"),
    "magnitude of": ("diff", "pairDiff"),
}


def _examples_csv_path() -> Path:
    return Path(__file__).resolve().parents[2] / "example.csv"


def _group_sort_key(name: str) -> Tuple[int, int, str]:
    if name == "ops":
        return (0, 0, name)
    m = re.fullmatch(r"ops(\d+)", name)
    if m:
        return (0, int(m.group(1)), name)
    return (1, 9999, name)


def _node_sort_key(node: Dict[str, Any]) -> Tuple[int, str]:
    node_id = str((node.get("meta") or {}).get("nodeId") or node.get("id") or "")
    m = re.fullmatch(r"n(\d+)", node_id)
    if m:
        return (int(m.group(1)), node_id)
    return (9999, node_id)


def _compact_value(value: Any) -> Any:
    if isinstance(value, list):
        if len(value) <= 4:
            return [_compact_value(v) for v in value]
        return [_compact_value(v) for v in value[:4]] + ["..."]
    if isinstance(value, dict):
        out: Dict[str, Any] = {}
        for k, v in value.items():
            if k in {"id", "meta", "chartId"}:
                continue
            out[k] = _compact_value(v)
        return out
    return value


def _infer_intent_ops(question: str, explanation: str) -> Set[str]:
    text = f"{question} {explanation}".lower()
    found: Set[str] = set()
    for keyword, ops in _KEYWORD_TO_OPS.items():
        if keyword in text:
            found.update(ops)
    return found


def _flatten_nodes(spec: Dict[str, List[OperationSpec]]) -> List[Dict[str, Any]]:
    nodes: List[Dict[str, Any]] = []
    for group_name in sorted(spec.keys(), key=_group_sort_key):
        for op in spec.get(group_name, []):
            node = op.model_dump(mode="json", exclude_none=True)
            node["_group"] = group_name
            nodes.append(node)
    nodes.sort(key=_node_sort_key)
    return nodes


def _example_score(
    *,
    example: _ExampleRecord,
    target_mark: str,
    target_is_stacked: bool,
    target_has_series: bool,
    target_ops: Set[str],
) -> int:
    score = 0
    if example.mark == target_mark:
        score += 4
    if example.is_stacked == target_is_stacked:
        score += 2
    if example.has_series == target_has_series:
        score += 1
    score += 3 * len(example.op_names.intersection(target_ops))
    return score


def _chart_family_from_context(chart_context: Dict[str, Any]) -> str:
    mark = str(chart_context.get("mark") or "unknown")
    is_stacked = bool(chart_context.get("is_stacked"))
    has_series = bool(chart_context.get("series_field"))
    if mark == "bar":
        if is_stacked:
            return "bar_stacked"
        if has_series:
            return "bar_grouped_or_multiseries"
        return "bar_simple"
    if mark == "line":
        return "line_multi" if has_series else "line_simple"
    return f"{mark}_generic"


def tune_few_shot_budget(
    *,
    question: str,
    explanation: str,
    chart_context: Dict[str, JsonValue],
) -> FewShotBudget:
    family = _chart_family_from_context(chart_context)
    target_ops = _infer_intent_ops(question, explanation)
    complexity = len(target_ops)

    # 정확도 우선: family별 기본 예산.
    if family == "bar_simple":
        budget = FewShotBudget(5, 9000, 4, 8500, 4)
    elif family == "bar_stacked":
        budget = FewShotBudget(6, 9800, 5, 9300, 5)
    elif family == "bar_grouped_or_multiseries":
        budget = FewShotBudget(6, 9800, 5, 9300, 5)
    elif family == "line_simple":
        budget = FewShotBudget(5, 9000, 4, 8500, 4)
    elif family == "line_multi":
        budget = FewShotBudget(6, 9800, 5, 9300, 5)
    else:
        budget = FewShotBudget(4, 8200, 3, 7800, 3)

    # 다양성 강화: 연산 의도 복잡도가 높으면 예시/길이 소폭 확장.
    if complexity >= 4:
        budget = FewShotBudget(
            inventory_max_examples=min(8, budget.inventory_max_examples + 1),
            inventory_max_chars=min(12000, budget.inventory_max_chars + 1200),
            step_max_examples=min(7, budget.step_max_examples + 1),
            step_max_chars=min(12000, budget.step_max_chars + 1200),
            step_steps_per_example=min(6, budget.step_steps_per_example + 1),
        )
    if {"pairDiff", "lagDiff"}.intersection(target_ops):
        budget = FewShotBudget(
            inventory_max_examples=min(8, budget.inventory_max_examples + 1),
            inventory_max_chars=min(12000, budget.inventory_max_chars + 1000),
            step_max_examples=min(7, budget.step_max_examples + 1),
            step_max_chars=min(12000, budget.step_max_chars + 1000),
            step_steps_per_example=min(6, budget.step_steps_per_example + 1),
        )
    return budget


def _parse_spec(spec_json: str) -> Dict[str, List[OperationSpec]]:
    payload = json.loads(spec_json)
    if not isinstance(payload, dict):
        raise ValueError("spec_json must be an object")

    out: Dict[str, List[OperationSpec]] = {}
    for group_name, raw_ops in payload.items():
        if not isinstance(group_name, str) or not isinstance(raw_ops, list):
            raise ValueError("spec_json group format is invalid")
        parsed_ops: List[OperationSpec] = []
        for raw_op in raw_ops:
            if not isinstance(raw_op, dict):
                raise ValueError("operation item must be an object")
            parsed_ops.append(parse_operation_spec(raw_op))
        out[group_name] = parsed_ops
    return out


@lru_cache(maxsize=1)
def _load_examples() -> List[_ExampleRecord]:
    csv_path = _examples_csv_path()
    if not csv_path.exists():
        return []

    out: List[_ExampleRecord] = []
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not isinstance(row, dict):
                continue
            ex_id = str(row.get("id") or "").strip()
            if not ex_id:
                continue

            try:
                chart_context = json.loads(str(row.get("chart_context_json") or "{}"))
                spec = _parse_spec(str(row.get("spec_json") or "{}"))
            except Exception:
                continue

            if not isinstance(chart_context, dict):
                continue

            op_names: Set[str] = set()
            for ops in spec.values():
                for op in ops:
                    op_names.add(str(op.op))

            out.append(
                _ExampleRecord(
                    ex_id=ex_id,
                    question=str(row.get("question") or "").strip(),
                    explanation=str(row.get("explanation") or "").strip(),
                    chart_context=chart_context,
                    spec=spec,
                    op_names=op_names,
                    mark=str(chart_context.get("mark") or "unknown"),
                    is_stacked=bool(chart_context.get("is_stacked")),
                    has_series=bool(chart_context.get("series_field")),
                    family=_chart_family_from_context(chart_context),
                )
            )
    return out


def _pick_examples(
    *,
    question: str,
    explanation: str,
    chart_context: Dict[str, JsonValue],
    max_examples: int,
) -> List[_ExampleRecord]:
    examples = _load_examples()
    if not examples:
        return []

    target_ops = _infer_intent_ops(question, explanation)
    target_mark = str(chart_context.get("mark") or "unknown")
    target_is_stacked = bool(chart_context.get("is_stacked"))
    target_has_series = bool(chart_context.get("series_field"))
    target_family = _chart_family_from_context(chart_context)

    ranked = sorted(
        examples,
        key=lambda ex: (
            1 if ex.family == target_family else 0,
            _example_score(
                example=ex,
                target_mark=target_mark,
                target_is_stacked=target_is_stacked,
                target_has_series=target_has_series,
                target_ops=target_ops,
            ),
            ex.ex_id,
        ),
        reverse=True,
    )

    selected: List[_ExampleRecord] = []
    covered_ops: Set[str] = set()
    while ranked and len(selected) < max_examples:
        best_idx = 0
        best_value = -10**9
        for idx, ex in enumerate(ranked):
            base = _example_score(
                example=ex,
                target_mark=target_mark,
                target_is_stacked=target_is_stacked,
                target_has_series=target_has_series,
                target_ops=target_ops,
            )
            family_bonus = 4 if ex.family == target_family else 0
            diversity_bonus = 2 * len(ex.op_names - covered_ops)
            value = base + family_bonus + diversity_bonus
            if value > best_value:
                best_value = value
                best_idx = idx
        chosen = ranked.pop(best_idx)
        selected.append(chosen)
        covered_ops.update(chosen.op_names)
    return selected


def _chunk_text(explanation: str, sentence_index: int) -> str:
    text = str(explanation or "").strip()
    # The stored example corpus is sentence-oriented; reuse it as a rough proxy
    # for the legacy sentenceIndex field, which now represents chunk order.
    lines = [x.strip() for x in re.split(r"\n+", text) if x.strip()]
    if 1 <= sentence_index <= len(lines):
        return lines[sentence_index - 1]
    return text


def _format_inventory_example_output(spec: Dict[str, List[OperationSpec]], explanation: str) -> str:
    nodes = _flatten_nodes(spec)
    tasks: List[Dict[str, Any]] = []
    for idx, node in enumerate(nodes, start=1):
        meta = node.get("meta") or {}
        sentence_index = meta.get("sentenceIndex")
        mention = _chunk_text(explanation, sentence_index if isinstance(sentence_index, int) else 1)
        params_hint: Dict[str, Any] = {}
        for key, value in node.items():
            if key in {"op", "id", "meta", "chartId", "_group"} or value is None:
                continue
            params_hint[key] = _compact_value(value)
        tasks.append(
            {
                "taskId": f"o{idx}",
                "op": node.get("op"),
                "sentenceIndex": sentence_index,
                "mention": mention,
                "paramsHint": params_hint,
            }
        )
    payload = {"tasks": tasks, "warnings": []}
    return json.dumps(payload, ensure_ascii=False, indent=2)


def _format_step_compose_example_output(spec: Dict[str, List[OperationSpec]], max_steps: int) -> str:
    nodes = _flatten_nodes(spec)
    examples: List[Dict[str, Any]] = []
    available_ids: List[str] = []
    for idx, node in enumerate(nodes[:max_steps], start=1):
        meta = node.get("meta") or {}
        op_spec = {
            k: _compact_value(v)
            for k, v in node.items()
            if k not in {"id", "meta", "chartId", "_group"}
        }
        item = {
            "currentTask": {
                "taskId": f"o{idx}",
                "op": str(node.get("op") or ""),
                "sentenceIndex": int(meta.get("sentenceIndex") or 1),
            },
            "availableNodeIds": list(available_ids),
            "output": {
                "op_spec": op_spec,
                "inputs": list(meta.get("inputs") or []),
                "warnings": [],
            },
        }
        examples.append(item)
        node_id = str(meta.get("nodeId") or node.get("id") or "")
        if node_id:
            available_ids.append(node_id)
    return json.dumps(examples, ensure_ascii=False, indent=2)


def _context_summary(ctx: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "mark": ctx.get("mark"),
        "is_stacked": ctx.get("is_stacked"),
        "primary_dimension": ctx.get("primary_dimension"),
        "primary_measure": ctx.get("primary_measure"),
        "series_field": ctx.get("series_field"),
    }


def build_inventory_few_shot_examples(
    *,
    question: str,
    explanation: str,
    chart_context: Dict[str, JsonValue],
    max_examples: int = 4,
    max_chars: int = 7000,
) -> FewShotBundle:
    canonical_chunk_examples = [
        "[Inventory Canonical Pattern | merge_adjacent_sentences_into_one_chunk]",
        "Rule: Multiple adjacent sentences may map to one meaningful chunk when they describe one coherent visual/computational act.",
        "ExampleExplanation: \"Find the average revenue for Broadcasting. Use that same average as the benchmark for the comparison.\"",
        "ExpectedOutputJSON:",
        json.dumps(
            {
                "tasks": [
                    {
                        "taskId": "o1",
                        "op": "average",
                        "sentenceIndex": 1,
                        "mention": "Find the average revenue for Broadcasting. Use that same average as the benchmark for the comparison.",
                        "paramsHint": {"field": "@primary_measure", "group": "Broadcasting"},
                    }
                ],
                "warnings": [],
            },
            ensure_ascii=False,
            indent=2,
        ),
        "",
        "[Inventory Canonical Pattern | dimension_subset_then_aggregate]",
        "Rule: If a chunk asks for an aggregate over a subset of primary-dimension values, emit a filter task for the subset and a separate aggregate task.",
        "Rule: paramsHint.group is reserved for series restriction, not for year/category/label subsets.",
        "ExampleExplanation: \"Compute the average for 2010, 2013, and 2017.\"",
        "ExpectedOutputJSON:",
        json.dumps(
            {
                "tasks": [
                    {
                        "taskId": "o1",
                        "op": "filter",
                        "sentenceIndex": 1,
                        "mention": "Compute the average for 2010, 2013, and 2017.",
                        "paramsHint": {"field": "@primary_dimension", "include": ["2010", "2013", "2017"]},
                    },
                    {
                        "taskId": "o2",
                        "op": "average",
                        "sentenceIndex": 1,
                        "mention": "Compute the average for 2010, 2013, and 2017.",
                        "paramsHint": {"field": "@primary_measure"},
                    },
                ],
                "warnings": [],
            },
            ensure_ascii=False,
            indent=2,
        ),
        "",
        "[Inventory Canonical Pattern | split_one_sentence_into_multiple_chunks]",
        "Rule: One sentence may split into multiple chunks when it contains multiple distinct acts.",
        "ExampleExplanation: \"Filter to 2016, then compute the average, then compare the result with 2017.\"",
        "ExpectedOutputJSON:",
        json.dumps(
            {
                "tasks": [
                    {
                        "taskId": "o1",
                        "op": "filter",
                        "sentenceIndex": 1,
                        "mention": "Filter to 2016",
                        "paramsHint": {"field": "@primary_dimension", "include": ["2016"]},
                    },
                    {
                        "taskId": "o2",
                        "op": "average",
                        "sentenceIndex": 2,
                        "mention": "compute the average",
                        "paramsHint": {"field": "@primary_measure"},
                    },
                    {
                        "taskId": "o3",
                        "op": "diffByValue",
                        "sentenceIndex": 3,
                        "mention": "compare the result with 2017",
                        "paramsHint": {"targetValue": "ref:n2"},
                    },
                ],
                "warnings": [],
            },
            ensure_ascii=False,
            indent=2,
        ),
        "",
        "[Inventory Canonical Pattern | absorb_noop_text_into_neighbor_chunk]",
        "Rule: Narrative-only text should not become a standalone task. Absorb it into the nearest substantive chunk mention.",
        "ExampleExplanation: \"Compute the average revenue for Commercial. This confirms the overall trend. Compare it against Broadcasting.\"",
        "ExpectedOutputJSON:",
        json.dumps(
            {
                "tasks": [
                    {
                        "taskId": "o1",
                        "op": "average",
                        "sentenceIndex": 1,
                        "mention": "Compute the average revenue for Commercial. This confirms the overall trend.",
                        "paramsHint": {"field": "@primary_measure", "group": "Commercial"},
                    },
                    {
                        "taskId": "o2",
                        "op": "compareBool",
                        "sentenceIndex": 2,
                        "mention": "Compare it against Broadcasting.",
                        "paramsHint": {"operator": ">"},
                    },
                ],
                "warnings": [],
            },
            ensure_ascii=False,
            indent=2,
        ),
        "",
    ]
    selected = _pick_examples(
        question=question,
        explanation=explanation,
        chart_context=chart_context,
        max_examples=max_examples,
    )
    if not selected:
        return FewShotBundle(text="\n".join(canonical_chunk_examples).strip(), ids=[])

    lines: List[str] = list(canonical_chunk_examples)
    used_ids: List[str] = []
    for idx, ex in enumerate(selected, start=1):
        block = [
            f"[Inventory Example {idx} | id={ex.ex_id}]",
            f"Question: {ex.question}",
            f"Explanation: {ex.explanation}",
            f"ChartContextSummary: {json.dumps(_context_summary(ex.chart_context), ensure_ascii=False)}",
            "ExpectedOutputJSON:",
            _format_inventory_example_output(ex.spec, ex.explanation),
            "",
        ]
        candidate = "\n".join(lines + block).strip()
        if len(candidate) > max_chars and lines:
            break
        lines.extend(block)
        used_ids.append(ex.ex_id)
    return FewShotBundle(text="\n".join(lines).strip(), ids=used_ids)


def _format_single_shot_example_output(spec: Dict[str, List[OperationSpec]]) -> str:
    """Format a complete OpsSpec group map with id/meta for single-shot baseline."""
    result: Dict[str, List[Dict[str, Any]]] = {}
    for group_name in sorted(spec.keys(), key=_group_sort_key):
        ops_list: List[Dict[str, Any]] = []
        for op in spec.get(group_name, []):
            node = op.model_dump(mode="json", exclude_none=True, by_alias=True)
            node.pop("chartId", None)
            node.pop("_group", None)
            ops_list.append(node)
        ops_list.sort(key=_node_sort_key)
        result[group_name] = ops_list
    return json.dumps(result, ensure_ascii=False, indent=2)


def build_single_shot_few_shot_examples(
    *,
    question: str,
    explanation: str,
    chart_context: Dict[str, JsonValue],
    max_examples: int = 4,
    max_chars: int = 9000,
) -> FewShotBundle:
    """Build few-shot examples for the single-shot OpsSpec baseline.

    Each example shows the complete grouped OpsSpec output (with id, meta).
    """
    selected = _pick_examples(
        question=question,
        explanation=explanation,
        chart_context=chart_context,
        max_examples=max_examples,
    )
    if not selected:
        return FewShotBundle(text="(no few-shot examples available)", ids=[])

    lines: List[str] = []
    used_ids: List[str] = []
    for idx, ex in enumerate(selected, start=1):
        block = [
            f"[SingleShot Example {idx} | id={ex.ex_id}]",
            f"Question: {ex.question}",
            f"Explanation: {ex.explanation}",
            f"ChartContextSummary: {json.dumps(_context_summary(ex.chart_context), ensure_ascii=False)}",
            "ExpectedOpsSpecJSON:",
            _format_single_shot_example_output(ex.spec),
            "",
        ]
        candidate = "\n".join(lines + block).strip()
        if len(candidate) > max_chars and lines:
            break
        lines.extend(block)
        used_ids.append(ex.ex_id)
    return FewShotBundle(text="\n".join(lines).strip(), ids=used_ids)


def _format_text_to_image_example(
    ex: _ExampleRecord,
) -> str:
    """Format an example as a text-to-image description reference."""
    nodes = _flatten_nodes(ex.spec)
    steps: List[Dict[str, Any]] = []
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", ex.explanation) if s.strip()]
    # Group nodes by sentenceIndex
    groups: Dict[int, List[Dict[str, Any]]] = {}
    for node in nodes:
        si = (node.get("meta") or {}).get("sentenceIndex", 1)
        groups.setdefault(si, []).append(node)

    for si in sorted(groups.keys()):
        sent = sentences[si - 1] if si <= len(sentences) else ex.explanation
        elements: List[str] = []
        for node in groups[si]:
            op = node.get("op", "")
            if op in ("filter", "findExtremum", "retrieveValue", "nth"):
                elements.append(f"highlight relevant data elements for {op}")
            elif op in ("average", "sum", "count"):
                elements.append(f"add reference line and text label for {op} result")
            elif op in ("diff", "compare", "compareBool"):
                elements.append(f"add connecting arrow and difference label for {op}")
            else:
                elements.append(f"annotate chart for {op}")
        steps.append({
            "sentenceIndex": si,
            "explanation_sentence": sent,
            "visual_elements": elements,
        })
    return json.dumps(steps, ensure_ascii=False, indent=2)


def build_text_to_image_few_shot_examples(
    *,
    question: str,
    explanation: str,
    chart_context: Dict[str, JsonValue],
    max_examples: int = 3,
    max_chars: int = 7000,
) -> FewShotBundle:
    """Build few-shot examples for the text-to-image baseline."""
    selected = _pick_examples(
        question=question,
        explanation=explanation,
        chart_context=chart_context,
        max_examples=max_examples,
    )
    if not selected:
        return FewShotBundle(text="(no few-shot examples available)", ids=[])

    lines: List[str] = []
    used_ids: List[str] = []
    for idx, ex in enumerate(selected, start=1):
        block = [
            f"[TextToImage Example {idx} | id={ex.ex_id}]",
            f"Question: {ex.question}",
            f"Explanation: {ex.explanation}",
            f"ChartContextSummary: {json.dumps(_context_summary(ex.chart_context), ensure_ascii=False)}",
            "ExpectedSteps:",
            _format_text_to_image_example(ex),
            "",
        ]
        candidate = "\n".join(lines + block).strip()
        if len(candidate) > max_chars and lines:
            break
        lines.extend(block)
        used_ids.append(ex.ex_id)
    return FewShotBundle(text="\n".join(lines).strip(), ids=used_ids)


def build_vegalite_annotation_few_shot_examples(
    *,
    question: str,
    explanation: str,
    chart_context: Dict[str, JsonValue],
    max_examples: int = 3,
    max_chars: int = 7000,
) -> FewShotBundle:
    """Build few-shot examples for the Vega-Lite annotation baseline.

    Since we don't store annotated Vega-Lite specs in example.csv,
    we show the OpsSpec as annotation intent reference.
    """
    selected = _pick_examples(
        question=question,
        explanation=explanation,
        chart_context=chart_context,
        max_examples=max_examples,
    )
    if not selected:
        return FewShotBundle(text="(no few-shot examples available)", ids=[])

    lines: List[str] = []
    used_ids: List[str] = []
    for idx, ex in enumerate(selected, start=1):
        nodes = _flatten_nodes(ex.spec)
        # Build annotation summary from OpsSpec
        summary: List[Dict[str, Any]] = []
        groups: Dict[int, List[str]] = {}
        for node in nodes:
            si = (node.get("meta") or {}).get("sentenceIndex", 1)
            op = node.get("op", "")
            desc = f"{op}"
            field = node.get("field")
            if field:
                desc += f" on {field}"
            groups.setdefault(si, []).append(desc)
        for si in sorted(groups.keys()):
            summary.append({
                "sentenceIndex": si,
                "annotation_intent": groups[si],
            })

        block = [
            f"[VegaLiteAnnotation Example {idx} | id={ex.ex_id}]",
            f"Question: {ex.question}",
            f"Explanation: {ex.explanation}",
            f"ChartContextSummary: {json.dumps(_context_summary(ex.chart_context), ensure_ascii=False)}",
            "AnnotationIntentSummary:",
            json.dumps(summary, ensure_ascii=False, indent=2),
            "",
        ]
        candidate = "\n".join(lines + block).strip()
        if len(candidate) > max_chars and lines:
            break
        lines.extend(block)
        used_ids.append(ex.ex_id)
    return FewShotBundle(text="\n".join(lines).strip(), ids=used_ids)


def build_step_compose_few_shot_examples(
    *,
    question: str,
    explanation: str,
    chart_context: Dict[str, JsonValue],
    max_examples: int = 3,
    steps_per_example: int = 3,
    max_chars: int = 7000,
) -> FewShotBundle:
    canonical_subset_average = [
        "[StepCompose Canonical Pattern | subset_average_via_inputs]",
        "Rule: For dimension subsets (e.g., years), do NOT use op_spec.group on average/count/findExtremum.",
        "Rule: First make a filter node, then consume it via inputs.",
        "ExampleCurrentTask:",
        json.dumps(
            {
                "taskId": "oX",
                "op": "average",
                "sentenceIndex": 2,
                "mention": "average for years 2010, 2013, 2017",
            },
            ensure_ascii=False,
            indent=2,
        ),
        "ExampleOutputJSON:",
        json.dumps(
            {
                "op_spec": {"op": "average", "field": "Installed base in million units"},
                "inputs": ["n3"],
                "warnings": [],
            },
            ensure_ascii=False,
            indent=2,
        ),
        "",
    ]
    selected = _pick_examples(
        question=question,
        explanation=explanation,
        chart_context=chart_context,
        max_examples=max_examples,
    )
    lines: List[str] = list(canonical_subset_average)
    if not selected:
        return FewShotBundle(text="\n".join(lines).strip(), ids=[])

    used_ids: List[str] = []
    for idx, ex in enumerate(selected, start=1):
        block = [
            f"[StepCompose Example {idx} | id={ex.ex_id}]",
            f"Question: {ex.question}",
            f"Explanation: {ex.explanation}",
            f"ChartContextSummary: {json.dumps(_context_summary(ex.chart_context), ensure_ascii=False)}",
            "ExpectedStepOutputsJSON:",
            _format_step_compose_example_output(ex.spec, max_steps=steps_per_example),
            "",
        ]
        candidate = "\n".join(lines + block).strip()
        if len(candidate) > max_chars and lines:
            break
        lines.extend(block)
        used_ids.append(ex.ex_id)
    return FewShotBundle(text="\n".join(lines).strip(), ids=used_ids)
