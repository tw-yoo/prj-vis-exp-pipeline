Task: Step-Compose (Recursive Grammar Pipeline, MVP).

You will be given:
- A fixed current operation task selected by the pipeline
- A set of remaining operation tasks S(O) extracted from the explanation
- A set of available executed nodes (nodeId + result summaries)
- Chart context and rows preview

Your job:
Propose exactly ONE operation spec (op_spec) for the fixed current task
using the currently available nodes and the base chart (C0).
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
  "op_spec": {
    "op": "string",
    "...": "OperationSpec-like top-level fields (NO id/meta/chartId)"
  },
  "inputs": ["n<digits>", "..."],
  "warnings": ["string"]
}

Critical rules:
1) Task selection:
   - DO NOT pick/select a taskId in your output.
   - The pipeline already selected the current task.
   - op_spec.op MUST match current_task.op.
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
   - Each op may have at most ONE "data parent" input (the prior node whose row result becomes this op's dataset). Prefer scalar refs ("ref:nX") for additional scalar dependencies.
   - Prefer ops that consume already-produced intermediates and move one step closer to final output intent.
5) Series restriction:
   - Do NOT filter on series_field directly.
   - Restrict series via op_spec.group / op_spec.groupA / op_spec.groupB when needed.
   - For FilterOp, op_spec.group may be a string or list of strings. A list means OR semantics.
   - IMPORTANT: For average/count/findExtremum/sort/retrieveValue/lagDiff/nth, group MUST be a single series value string.
   - Never use chunk-layer tokens ("ops", "ops2", ...) as group values.
   - Never put dimension subsets (e.g., years like ["2010","2013"]) into group.
5a) retrieveValue direction:
   - retrieveValue supports BOTH forward (x→y) and reverse (y→x) lookup via `targetAxis`.
   - Default (omitted or "x"): forward — `target` is an x-axis category label, returns y values.
   - `targetAxis: "y"`: reverse — `target` MUST be a numeric value of the measure (y), returns matching x category row(s).
   - Emit `targetAxis: "y"` ONLY when the explanation explicitly says things like "which year had value X" / "어느 카테고리가 60을 기록" / "find the country with rating 60". The numeric target MUST appear in the explanation.
   - For multi-measure charts, also include `field` so the y value is interpreted against the correct measure.

6) Filter MUST choose a mode:
   - For op="filter", you MUST set EITHER:
     - membership mode: include and/or exclude
     - comparison mode: operator AND value (both)
     - group-only mode: group only (series restriction)
   - In membership mode, field may be any categorical field (except series_field).
   - For row-order interval phrases like "from year A to year B", use comparison mode:
     operator="between", value=[A,B] (inclusive slice from first A to first B after A).
   - Never output a field-only filter. It will be rejected by validation.
7) Op-specific reminders (extended-field semantics):
   - For op="findExtremum", use rank for k-th extremum (e.g., second highest -> which="max", rank=2).
   - For op="compareBool":
     - MUST include operator (e.g., ">", "<=", "==").
     - For slice-aggregate comparisons (e.g., "is the average of A higher than the average of B"), set groupA/groupB + aggregate ("sum"|"avg"|"min"|"max") and use field as the measure being aggregated. targetA/targetB are optional in this mode.
   - For op="add", you MUST include targetA and targetB (each should be scalar ref like "ref:nX" or numeric literal).
   - For op="diff": MUST include targetA and targetB (both must be scalar refs "ref:nX" or dimension labels).
     inputs MUST contain exactly 2 nodeIds matching the referenced nodes when scalar refs are used.
     Extended fields:
     - percent=true → percentage change (targetA - targetB) / targetB * 100. Use for "% increase", "% decrease", "percent change".
     - mode="ratio" → returns targetA / targetB (multiplied by scale; default scale is 1.0, or 100 when percent=true). Use for "ratio of A to B", "N times".
     - aggregate ("sum"|"avg"|"min"|"max"|"percentage_of_total") → applies when targetA/targetB resolve to multi-row slices: each slice is aggregated by this method before the diff. "percentage_of_total" returns targetA as a share of the total.
     - groupA/groupB → series slices when targetA/targetB are dimension labels and the chart has a series field. Otherwise use a single `group`.
     - precision → rounds final scalar; scale → multiplies final scalar by that factor.
   - For op="diffByValue": MUST include either `value` (numeric literal) or `targetValue` ("ref:nX")
     — exactly one of the two — defining the scalar reference V every chart row is compared against.
   - For op="nth":
     - n is REQUIRED (integer or list of integers).
     - from="left"|"right" picks direction; "right" for positional-from-end phrases like "2nd from the right" or "the most recent two".
     - orderField (alternate sort key dimension) defines the ordering; combine with order="asc"|"desc" when explicit. If absent, nth assumes the upstream node is already sorted.
     - field/group are optional narrowing parameters.
   - For op="sort":
     - field is the measure column being compared (defaults to primary_measure when omitted).
     - orderField is an alternate sort key, typically a dimension (e.g., "Year"). Use orderField when the explanation says "sort by Year/Date/Category" (not by the measure). If both are given, orderField wins for ordering.
     - order="asc"|"desc" defaults to "asc" when omitted.
   - For op="pairDiff":
     - MUST include by, groupA, and groupB.
     - For grouped/stacked comparisons where groupA/groupB come from a non-default field, include seriesField.
     - absolute=true returns abs(groupA - groupB) per key (default keeps sign).
     - precision rounds each per-key delta.
   - For op="lagDiff":
     - absolute=true returns absolute magnitudes of adjacent-period differences. Use for "absolute year-over-year change", "size of period-to-period swings".
     - order="asc"|"desc" controls the ordering used to define adjacency.
   - For op="sum", use it only for bar charts (simple/stacked); group may be string or list. sum is row aggregation, not scalar addition. Check chart_context.mark: when it is "line" (simple/multiple) the contract rejects sum — to total exactly two specific points on a line chart use scalar `add` over their values instead.
   - For op="scale":
     - target MUST be a scalar ref ("ref:nX") or a numeric literal.
     - factor MUST be a numeric multiplier (e.g., 2.0 for "doubled", 0.5 for "halved", 100 for "to percent").
     - scale is scalar-only; do not use it on row-list results.
   - For op="range":
     - Computes max − min of the working slice as a single scalar.
     - field defaults to primary_measure; group restricts to one series before computing the spread.
     - Use this instead of findExtremum(max)+findExtremum(min)+diff when the intent is "spread / variation / range".
   - For op="rollingWindow":
     - window is a required positive integer (e.g., window=3 for a 3-year window).
     - aggregate is one of "sum"|"avg"|"min"|"max" (default "avg"). Pick "avg" for "moving average", "sum" for "consecutive N-year total", and so on.
     - orderField is the sliding axis (typically the x-axis dimension such as "Year" / "Date"); omit only when natural data order is correct.
     - field defaults to primary_measure; group restricts to one series first.
     - Result is a row list of (N − window + 1) windows; chain with findExtremum/nth to pick the best/worst window.
   - For op="monotonicRun":
     - direction is "increasing" or "decreasing" (default "increasing").
     - mode = "longest" (default; returns the longest qualifying run as a row list), "firstBreak" (single row marking where the first run starts), or "all" (every qualifying run flattened).
     - strict defaults to true (every step must be strictly inc/dec).
     - minLength filters out runs shorter than the count (default 2). Use minLength=3 for "more than 2 years" / "≥ 3 consecutive".
     - orderField defines the scan axis (typically the x-axis dimension); field is the measure compared between adjacent rows.
     - Pick mode="firstBreak" only when the question asks for the starting point of a trend; otherwise mode="longest" matches "longest period of decrease/increase".
8) Planning quality checklist (must satisfy):
   - Decide whether this step's output is scalar or row-list and ensure it is needed by later steps.
   - If a scalar is needed from prior nodes, use "ref:nX" explicitly.
   - Avoid producing disconnected or unused branches.
   - The selected task already represents one operation-bearing reasoning chunk. Do not add compensating ops for nearby narrative-only text.
   - Keep op choices semantically aligned with intent:
     - row aggregation: sum/average/count
     - scalar arithmetic: add/scale/diff (scalar-ref mode)
     - row selection/ranking: filter/sort/nth/findExtremum
   - MATCH OP TO INPUT SHAPE (contract invariant): the scalar-only ops (add, scale, diff, compareBool) consume scalar refs ("ref:nX"), never a dataset. If the current input node is a ROW-LIST and you need a single number, reduce it with average/sum/count/findExtremum/range; do NOT apply add/scale/diff to a row-list. Use add/diff only to combine exactly two named scalars. (e.g. to total many per-row differences from a prior pairDiff/lagDiff, use sum (bar) — not add; to average a small filtered slice, use average — not scale.)
9) QUESTION-DRIVEN INPUT SELECTION:
   When multiple available nodes could serve as inputs or scalar refs, resolve ambiguity by reading the QUESTION:
   - Ask: "What semantic role does the current step play in answering the question?"
   - Choose inputs/refs that match that semantic role, NOT simply the most recently computed node.
   Example:
     Available: n2=avg_top3, n4=avg_bottom3
     Task: "scale" (double the lowest average)
     Question mentions "lowest three" → target should be "ref:n4" (avg_bottom3), not n2.
   When the current reasoning chunk is ambiguous (e.g., "double the X" without naming X explicitly),
   derive X from the QUESTION before selecting the ref.

10) COMPREHENSIVE INPUTS GATHERING - 필수 규칙 (MUST APPLY):
   For comparison/ranking operations (findExtremum, diff, pairDiff, diffByValue):

   CRITICAL RULE: inputs MUST include ALL available nodes that contribute
   to the semantic meaning of the current task.

   Specific cases (MUST apply):

   - findExtremum: If multiple candidate nodes exist (from different groups/times),
     inputs MUST contain ALL of them.
     Example:
       Available: n1 (Tablets 2017: 173.56), n2 (Mobile PCs 2022: 244.43)
       Task: findExtremum("field", which="max")
       → inputs MUST be ['n1', 'n2'], NOT ['n1'] alone
       → Rationale: "max between two values" requires BOTH values to compare
       → If only n1 is included, the max is not determined between the two candidates

   - diff: MUST include exactly 2 nodes being compared

   - diffByValue: When the reference V comes from a prior node (targetValue="ref:nX"), include that node in inputs

   - pairDiff: Include all relevant input nodes for the pair comparison

   IMPORTANT: The current reasoning chunk may be implicit about all needed inputs.
   Do NOT assume that "find maximum" or "check which is greater" requires only one input.
   Derive from the QUESTION's semantic intent: if the question asks to compare
   MULTIPLE values or entities, then ALL available candidate nodes must be inputs.

Mini pattern (subset average via inputs):
- Wrong:
  {
    "op_spec": { "op": "average", "field": "Installed base in million units", "group": ["2010", "2013", "2017"] },
    "inputs": []
  }
- Correct:
  1) filter subset first (include years) -> node n3
  2) average consumes that filter result
  {
    "op_spec": { "op": "average", "field": "Installed base in million units" },
    "inputs": ["n3"]
  }

Question:
$question

Explanation:
$explanation

Current task (fixed by pipeline):
$current_task_json

Important note:
- current_task.sentenceIndex is a legacy public-schema field name. Treat it as the 1-based order of the current meaningful reasoning chunk, not sentence order.

Remaining tasks S(O):
$remaining_tasks_json

Available executed nodes (you may reference them via nodeId; scalar outputs use "ref:nX"):
$available_nodes_json

Chart context:
$chart_context_json

Rows preview:
$rows_preview_json
