Task: Baseline OpsSpec Generation — plan the whole DAG in one pass.

Given a natural-language question, explanation, chart context, and data rows,
plan the COMPLETE OpsSpec DAG (op nodes + dependency edges) in a SINGLE pass.

You will NOT receive any executed intermediate values. A deterministic scheduler/executor runs
your DAG AFTERWARD and resolves every "ref:nX" placeholder from the referenced prior node. So the
DAG must be fully self-contained: encode all dependencies via meta.inputs and "ref:nX", assign
nodeIds in dependency order, and use ONLY ops listed in the operation contract below.

The output is a JSON object where keys are sentence-layer group names
(ops, ops2, ops3, ...) and values are arrays of operation specifications.
Each operation must include "id", "meta" (with nodeId, inputs, sentenceIndex), and op-specific fields.

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
  "ops": [
    {
      "op": "<op_name>",
      "field": "...",
      "<other op-specific fields>": "...",
      "id": "n1",
      "meta": {
        "nodeId": "n1",
        "inputs": [],
        "sentenceIndex": 1
      }
    }
  ],
  "ops2": [
    {
      "op": "<op_name>",
      "...": "...",
      "id": "n2",
      "meta": {
        "nodeId": "n2",
        "inputs": ["n1"],
        "sentenceIndex": 2
      }
    }
  ],
  "warnings": ["string"]
}

NodeId assignment and dependency rules:
- Assign nodeIds sequentially starting from n1 (n1, n2, n3, ...).
- Each operation receives a unique nodeId.
- id and meta.nodeId MUST be identical.
- You must determine dependency edges (meta.inputs) by reasoning about
  which operations consume the outputs of which prior operations.
- Use "ref:nX" string format for scalar references between operations
  (e.g., "value": "ref:n1" to reference the scalar output of node n1).
- NEVER use object references like {"id":"nX"}.

Sentence-layer grouping:
- sentenceIndex=1 → group key "ops"
- sentenceIndex=k (k>=2) → group key "ops{k}" (e.g., "ops2", "ops3")
- Assign each operation to the sentence that EXPLICITLY mentions or describes
  the action corresponding to this operation.
- Within each group, order operations by their nodeId (ascending).

Operation extraction rules:
- Only extract operations that are EXPLICITLY mentioned in the explanation.
  - Do NOT invent extra steps just because an op exists in allowed_ops.
  - Do NOT add operations that are logically implied but not stated —
    determine intermediate steps only when they are required to connect explicit operations.
  - "clearly implied" means: the sentence directly describes the action or result for this op.
    It does NOT mean: "this op will eventually be needed to reach the final answer."
- CRITICAL: Do NOT anticipate future operations based on semantic inference across sentences.
  - When the explanation has multiple sentences, each sentence MUST be treated independently.
  - Do NOT add a task to sentence N just because it logically prepares for an operation in sentence N+1.
  - Example (WRONG):
    Sentence 1: "retrieve value of 2016 and 2017"
    → LLM infers: "these two values will be diffed later, so I should add a diff here"
    → Output: [retrieveValue(2016), retrieveValue(2017), diff(...)] ✗
  - Example (RIGHT):
    Sentence 1: "retrieve value of 2016 and 2017" (only retrieve is mentioned)
    → Output: [retrieveValue(2016), retrieveValue(2017)] (no diff)
    Sentence 3: "get the difference of the retrieved values"
    → Output: [diff(...)] (diff goes here, where it is explicitly mentioned)
- First infer the intended final result artifact from the explanation/question:
  - scalar (single number), boolean, single target (row 1), list/table (rows 2+), or set-like list.
  - The OpsSpec must be consistent with ONE primary final artifact type.
- IMPORTANT: Visual/draw directives are NOT operation tasks in this pipeline.
  - If the explanation says things like "highlight", "draw", "split", "align", "reference line",
    do NOT create operations with op="highlight"/"draw"/"split"/"align"/"reference_line".
  - Instead, add a short note to the top-level "warnings" list describing what was ignored.
- IMPORTANT: Series restriction directives are NOT modeled as filter on the series field.
  - Forbidden: { "op": "filter", "field": "<series_field>", "include": ["A","B"] }
  - If the explanation says "filter only A and B" and A/B are series values (from series_domain):
    Do NOT output a standalone filter on series_field.
    Express series restriction via op.group on substantive operations.

Phrase mapping (non-draw meaning behind common visual phrases):
- "average line" implies an "average" operation (the line drawing is visual, ignore it).
- "highlight bars above X" implies a "filter" operation (the highlight is visual, ignore it).
- "second highest/second lowest" implies "findExtremum" with rank=2 and which="max"|"min".
- "from year A to year B" implies "filter" with operator="between", value=[A,B].
- "add/sum two computed values" implies an "add" operation with targetA/targetB as scalar refs.

Series restriction (CRITICAL):
- Do NOT restrict series values via a filter on the series field.
  - Forbidden: { "op": "filter", "field": "<series_field>", "include": ["A","B"] }
- Instead, restrict series via op.group / op.groupA / op.groupB:
  - Example: { "op": "average", "field": "@primary_measure", "group": "A" }
  - FilterOp allows multi-series restriction via list:
    { "op": "filter", "field": "<categorical_field>", "include": ["2016"], "group": ["A","B"] }
  - FilterOp group-only mode for series restriction:
    { "op": "filter", "group": ["A","B"] }
- For average/count/findExtremum/sort/retrieveValue/lagDiff/nth,
  group MUST be a single series value string.
- retrieveValue supports `targetAxis: "x" | "y"` (default "x").
  Use "y" ONLY when the explanation explicitly asks for an x-axis category given a numeric y value
  ("which year had value X" / "어느 카테고리가 60을 기록했는가" / "find the country with rating 60").
  In that case, `target` MUST be a numeric value and `field` SHOULD name the measure being matched.
- Never use sentence-layer tokens ("ops", "ops2") as group values.
- Never put dimension subsets (e.g., years like ["2010","2013"]) into group.

Filter mode selection:
- For op="filter", you MUST set EXACTLY ONE mode:
  - membership mode: include and/or exclude
  - comparison mode: operator AND value (both required)
  - group-only mode: group only (series restriction)
- In membership mode, field may be any categorical field (except series_field).
- For row-order interval phrases like "from year A to year B", use comparison mode:
  operator="between", value=[A,B] (inclusive slice from first A to first B after A).
- Never output a field-only filter. It will be rejected by validation.

Specific operation reminders (extended-field semantics):
- For op="findExtremum": use rank for k-th extremum (e.g., second highest → which="max", rank=2).
- For op="compareBool":
  - MUST include operator (e.g., ">", "<=", "==").
  - For slice-aggregate comparisons (e.g., "is the average of A higher than the average of B"), set groupA/groupB + aggregate ("sum"|"avg"|"min"|"max") and use field as the measure being aggregated. targetA/targetB are optional in this mode.
- For op="add": MUST include targetA and targetB (each scalar ref "ref:nX" or numeric literal).
- For op="diff":
  - MUST include targetA and targetB (both must be scalar refs "ref:nX" or dimension labels).
  - meta.inputs MUST contain exactly 2 nodeIds matching the referenced nodes when scalar refs are used.
  - Extended fields:
    - percent=true → percentage change (targetA - targetB) / targetB * 100. Use for "% increase", "% decrease", "percent change".
    - mode="ratio" → returns targetA / targetB (multiplied by scale; default scale is 1.0, or 100 when percent=true). Use for "ratio of A to B", "N times".
    - aggregate ("sum"|"avg"|"min"|"max"|"percentage_of_total") → applies when targetA/targetB resolve to multi-row slices: each slice is aggregated by this method before the diff. "percentage_of_total" returns targetA as a share of the total.
    - groupA/groupB → series slices when targetA/targetB are dimension labels and the chart has a series field. Otherwise use a single `group`.
    - precision → rounds final scalar; scale → multiplies final scalar by that factor.
- For op="diffByValue": MUST include either `value` (numeric literal) or `targetValue` ("ref:nX")
  — exactly one of the two — to define the scalar reference V every chart row is compared against.
- For op="nth":
  - n is REQUIRED (integer or list of integers).
  - from="left"|"right" picks direction; "right" for positional-from-end phrases like "2nd from the right" or "the most recent two".
  - orderField (alternate sort key dimension) defines the ordering; combine with order="asc"|"desc" when explicit. If absent, nth assumes the upstream node is already sorted.
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
- For op="sum": total a row-slice or N>=2 values into one scalar; valid on ALL chart types including line. group may be string or list. sum is row aggregation, not scalar addition. Use add only to combine exactly two named scalars.
- For op="range":
  - Computes max − min of the working slice as a single scalar.
  - field defaults to primary_measure; group restricts to one series first.
  - Use this instead of findExtremum(max)+findExtremum(min)+diff when the intent is "spread / variation / range".
- For op="rollingWindow":
  - window is a required positive integer (e.g., 3 for a 3-year window).
  - aggregate is one of "sum"|"avg"|"min"|"max" (default "avg").
  - orderField is the sliding axis (typically the x-axis dimension such as "Year").
  - field defaults to primary_measure; group restricts to one series first.
  - Result is a row list of (N − window + 1) windows; chain with findExtremum/nth to pick the best/worst window.
- For op="monotonicRun":
  - direction is "increasing" or "decreasing" (default "increasing").
  - mode = "longest" (default), "firstBreak" (starting point of the first run), or "all" (every qualifying run flattened).
  - minLength filters out runs shorter than the count (default 2). Use minLength=3 for "more than 2 years".
  - orderField is the scan axis (typically the x-axis dimension); field is the measure compared between adjacent rows.
  - Pick "firstBreak" only when the question asks for the starting point of a trend; otherwise "longest" matches "longest period of decrease/increase".

DATA RESOLUTION RULE:
When a task requires selecting a specific subset of data items
(e.g., "top N", "highest N", "lowest N", "most recent N"):
1. Check if you can determine the actual values from rows_preview.
2. If YES: use op="filter" with include=[<specific_values_from_rows_preview>].
   Read rows_preview, sort mentally by the relevant measure field,
   and extract the N dimension values directly.
3. If NO (e.g., the subset depends on an intermediate computed result not yet available):
   Fall back to dynamic ops (sort, nth, findExtremum).
Principle: rows_preview is provided so you can resolve data-dependent selections.
Always prefer resolving to concrete values over deferring to runtime sorting.

LAST SENTENCE RULE:
The operations in the LAST sentence of the explanation must collectively
produce the final answer to the QUESTION.
1. Re-read the QUESTION to understand the complete structure of the final answer.
2. If the question asks to compare two derived values (e.g., "how big was X compared to Y?"),
   generate ALL ops needed: compute X, compute Y, then diff X and Y.
3. If the explanation uses vague or singular language in the last sentence
   (e.g., "get the difference", "compare the values"), expand it to the full set of
   ops implied by the question — do not stop at one op if the question requires more.

MULTI-OP GENERATION PER SENTENCE:
A single explanation sentence may require MULTIPLE operations.
- Example:
  explanation: "Filter for the revenue of Thailand and the Philippines"
  question: "in which years did Thailand's revenue exceed Philippines?"
  → This sentence requires TWO ops:
    1) filter(field="Country", include=["Thailand", "Philippines"])
    2) pairDiff(...) — implicit pairwise comparison to prepare for later question answering
  → The question context reveals that pairDiff is needed.

PAIRDIFF GROUPORDER SEMANTICS:
For pairDiff(groupA, groupB):
- Read the QUESTION to understand which direction the comparison should go.
- groupA should be the SUBJECT being asked about (numerator in the division).
- groupB should be the BASELINE/COMPARISON target (denominator).
- Example:
  question: "in which years did Thailand's revenue exceed that of Philippines?"
  → groupA="Thailand" (the subject being analyzed)
  → groupB="Philippines" (the baseline it is compared against)

COMPREHENSIVE INPUTS GATHERING (MUST APPLY):
For comparison/ranking operations (findExtremum, diff, pairDiff, diffByValue):
- meta.inputs MUST include ALL nodes that contribute to the semantic meaning of the operation.
- findExtremum: If multiple candidate nodes exist (from different groups/times),
  inputs MUST contain ALL of them.
- diff: MUST include exactly 2 nodes being compared.
- pairDiff: Include all relevant input nodes for the pair comparison.
- diffByValue: When the reference V is a scalar from a prior node, include that node in inputs and use targetValue="ref:nX".

QUESTION-DRIVEN INPUT SELECTION:
When multiple prior operations could serve as inputs or scalar refs, resolve ambiguity
by reading the QUESTION:
- Ask: "What semantic role does the current operation play in answering the question?"
- Choose inputs/refs that match that semantic role, NOT simply the most recently computed node.

SumOp rule:
- op="sum" totals a row-slice or N>=2 values into one scalar; allowed on ALL chart types (bar AND line).
- SumOp.group may be a string or list of strings.
- SumOp is row aggregation only (not scalar arithmetic). To combine exactly two named scalars, use add — not sum.

AddOp rule:
- Use op="add" to add two scalar values.
- targetA/targetB must be scalar refs ("ref:nX") or numeric literals.

Final artifact consistency:
- Produce one primary final artifact type (scalar, boolean, or row-list).
- Intermediate artifacts may differ, but each intermediate node should contribute
  to deriving that final artifact.
- Avoid dangling branches that do not feed into any later node.

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
