Task: Step-Compose (Recursive Grammar Pipeline, MVP).

You will be given:
- A set of remaining operation tasks S(O) extracted from the explanation
- A set of available executed nodes (nodeId + result summaries)
- Chart context and rows preview

Your job:
Pick exactly ONE next task that is executable now, and propose exactly ONE operation spec (op_spec)
that accomplishes that task using the currently available nodes and the base chart (C0).
Always keep global coherence with the intended final artifact type implied by question/explanation
(scalar vs list/table vs boolean). Intermediate nodes are allowed, but the plan must converge to one final artifact.

Return JSON only. Do not include markdown fences.

Shared rules:
$shared_rules

Operation contract (allowed ops + required/optional/forbidden fields + semantic rules):
$ops_contract_json

Validation feedback from previous failed attempts:
$validation_feedback_json

Few-shot examples (reference patterns; adapt field/group values to current chart context):
$few_shot_examples

Output schema:
{
  "pickTaskId": "o<digits>",
  "op_spec": {
    "op": "string",
    "...": "OperationSpec-like top-level fields (NO id/meta/chartId)"
  },
  "inputs": ["n<digits>", "..."],
  "warnings": ["string"]
}

Critical rules:
1) Tie-break for determinism:
   - If multiple tasks are executable, pick the smallest taskId (o1 < o2 < o10 ...).
   - But do not pick a task that makes the remaining plan inconsistent with the final artifact intent.
2) op_spec shape:
   - op_spec MUST include "op".
   - op_spec MUST NOT include: "id", "meta", "chartId".
   - Use ONLY fields allowed by the operation contract for that op.
3) References:
   - If you need a scalar from a previous node, use a STRING reference "ref:nX".
   - NEVER output {"id":"nX"} objects.
4) inputs:
   - inputs can include nodeIds that the operation depends on.
   - Every nodeId in inputs MUST already exist in available nodes.
   - For setOp, inputs MUST contain at least two nodeIds.
   - For non-setOp ops, do NOT use more than one "data parent" input. Prefer scalar refs for scalar dependencies.
   - Prefer ops that consume already-produced intermediates and move one step closer to final output intent.
5) Series restriction:
   - Do NOT filter on series_field directly.
   - Restrict series via op_spec.group / op_spec.groupA / op_spec.groupB when needed.
   - For FilterOp, op_spec.group may be a string or list of strings. A list means OR semantics.
6) Filter MUST choose a mode:
   - For op="filter", you MUST set EITHER:
     - membership mode: include and/or exclude
     - comparison mode: operator AND value (both)
     - group-only mode: group only (series restriction)
   - In membership mode, field may be any categorical field (except series_field).
   - For row-order interval phrases like "from year A to year B", use comparison mode:
     operator="between", value=[A,B] (inclusive slice from first A to first B after A).
   - Never output a field-only filter. It will be rejected by validation.
7) CompareBool / Nth / SetOp reminders:
   - For op="findExtremum", use rank for k-th extremum (e.g., second highest -> which="max", rank=2).
   - For op="compareBool", you MUST include operator (e.g., ">", "<=", "==").
   - For op="add", you MUST include targetA and targetB (each should be scalar ref like "ref:nX" or numeric literal).
   - For op="nth", you MUST include n (integer or list of integers). (n is required.)
   - For op="setOp", you MUST include fn ("intersection" or "union") AND inputs with at least two nodeIds.
   - For op="pairDiff", you MUST include by, groupA, and groupB.
   - For grouped/stacked comparisons where groupA/groupB come from a non-default field, include seriesField.
   - For op="sum", use it only for bar charts; group may be string or list. sum is row aggregation, not scalar addition.
8) Planning quality checklist (must satisfy):
   - Decide whether this step's output is scalar or row-list and ensure it is needed by later steps.
   - If a scalar is needed from prior nodes, use "ref:nX" explicitly.
   - Avoid producing disconnected or unused branches.
   - Keep op choices semantically aligned with intent:
     - row aggregation: sum/average/count
     - scalar arithmetic: add/scale/diff (scalar-ref mode)
     - row selection/ranking: filter/sort/nth/findExtremum

Question:
$question

Explanation:
$explanation

Remaining tasks S(O):
$remaining_tasks_json

Available executed nodes (you may reference them via nodeId; scalar outputs use "ref:nX"):
$available_nodes_json

Chart context:
$chart_context_json

Rows preview:
$rows_preview_json
