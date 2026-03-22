Task: Inventory (Recursive Grammar Pipeline, MVP).

Given a natural-language question + explanation and chart context,
extract the minimal set of operation tasks explicitly mentioned in the explanation.

Return JSON only. Do not include markdown fences.

Shared rules:
$shared_rules

High-priority context:
Roles summary:
$roles_summary_json

Series domain (values for series_field; empty list if unknown):
$series_domain_json

Measure fields (numeric candidates):
$measure_fields_json

Operation contract (allowed ops + required/optional/forbidden fields + semantic rules):
$ops_contract_json

Validation feedback from previous failed attempts:
$validation_feedback_json

Few-shot examples (reference patterns; adapt field/group values to current chart context):
$few_shot_examples

Output schema:
{
  "tasks": [{
    "taskId": "o1|o2|o3|... (MUST be unique, MUST match o<digits>)",
    "op": "string (MUST be in allowed_ops)",
    "sentenceIndex": 1,
    "mention": "short quote/summary of the part of explanation that mentions this operation",
    "paramsHint": { "paramName": "scalar|list-of-scalars" }
  }],
  "warnings": ["string"]
}

Rules:
- Only extract operations that are explicitly mentioned in the explanation.
  - Do NOT invent extra steps just because an op exists in allowed_ops.
  - Do NOT add operations that are logically implied but not stated —
    Step-Compose handles intermediate steps at compose-time.
  - "clearly implied" means: the sentence directly describes the action or result for this op.
    It does NOT mean: "this op will eventually be needed to reach the final answer."
- First infer the intended final result artifact from the explanation/question:
  - scalar (single number), boolean, single target(row 1), list/table(rows 2+), or set-like list.
  - Inventory must be consistent with ONE primary final artifact type.
  - If multiple artifact types are mentioned, treat non-final ones as intermediate steps and keep one final output intent.
- IMPORTANT: Visual/draw directives are NOT operation tasks in this pipeline.
  - If the explanation says things like "highlight", "draw", "split", "align", "reference line",
    do NOT create tasks with op="highlight"/"draw"/"split"/"align"/"reference_line".
  - Instead, add a short note to the top-level "warnings" list describing what was ignored.
  - This endpoint generates non-draw OpsSpec only.
- IMPORTANT: Series restriction directives are NOT modeled as filter tasks on the series field.
  - Forbidden inventory task:
    - { "op": "filter", "paramsHint": { "field": "@series_field", "include": ["A","B"] } }
    - { "op": "filter", "paramsHint": { "field": "<series_field>", "include": ["A","B"] } }
  - If the explanation says "filter only A and B" and A/B are series values (from series_domain):
    - Do NOT output a standalone filter task.
    - Add a warning.
    - Later steps should express series restriction via op_spec.group on substantive operations.
- Phrase mapping (non-draw meaning behind common visual phrases):
  - "average line" implies an "average" operation task (the *line drawing* itself is visual and should be in warnings).
  - "highlight bars above X" implies a "filter" operation task (the *highlight* itself is visual and should be in warnings).
  - "second highest/second lowest" implies a "findExtremum" task with paramsHint.rank=2 and which="max|min".
  - "from year A to year B" implies a "filter" task with paramsHint.operator="between", paramsHint.value=[A,B].
  - "add/sum two computed values" implies an "add" operation task with paramsHint.targetA/targetB (usually refs at compose-time).
- If the same op name appears in different parts of the explanation with different intent/arguments,
  create separate tasks with different taskIds.
- Build tasks as a minimal executable plan:
  - include prerequisite steps (filter/aggregate/compare) needed to derive the final intended artifact.
  - avoid redundant branches that do not contribute to the final artifact.
- sentenceIndex MUST be the 1-based index of the sentence that explicitly names or describes this task's action.
  - Assign a task to the sentence whose verb/action directly corresponds to this op
    (e.g., "retrieve" → retrieveValue, "difference" → diff, "filter" → filter).
  - Do NOT assign a task to a sentence just because it provides input data for the task.
  - The fact that sentence 1 produces values that a later op will consume
    does NOT mean that later op belongs in sentenceIndex=1.
    If an op is only mentioned in sentence 3, it gets sentenceIndex=3.
- paramsHint must be FLAT (no nested objects). Keep it minimal.
- Role tokens allowed in paramsHint values:
  - "@primary_dimension", "@primary_measure", "@series_field"
- Series restriction:
  - Never represent series selection as a filter on the series field.
  - Use paramsHint.group="<series value>" or paramsHint.group=["A","B"] instead.
  - When paramsHint.group is a list for FilterOp, it means OR semantics across listed series values.
- Filter task must choose a mode:
  - If you output a task with op="filter", paramsHint MUST include EITHER:
    - membership mode: include and/or exclude
    - comparison mode: operator AND value (both)
    - group-only mode: group only (series restriction)
  - In membership mode, paramsHint.field may be any categorical field (except series_field).
  - If the explanation only says "filter only A and B" and A/B are series values (from series_domain),
    do NOT create a group-only filter task; attach the series restriction to other substantive tasks via paramsHint.group.

Question:
$question

Explanation:
$explanation

Explanation sentences (deterministic split; 1-based indices):
$explanation_sentences_json

Chart context:
$chart_context_json

Rows preview:
$rows_preview_json
