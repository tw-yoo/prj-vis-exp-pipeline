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
    "mention": "short quote/summary of the meaningful chunk that mentions this operation",
    "paramsHint": { "paramName": "scalar|list-of-scalars" }
  }],
  "warnings": ["string"]
}

Rules:
- First segment the explanation into meaningful reasoning chunks.
  - A chunk may be shorter than a sentence, equal to a sentence, or span multiple sentences.
  - Segment by coherent visual/computational intent, not grammar alone.
  - sentenceIndex is a legacy field name; use it to encode chunk order.
- Chunking policy:
  - One sentence may split into multiple chunks if it contains multiple distinct visual/computational acts.
  - Multiple adjacent sentences may merge into one chunk if together they express one coherent act.
  - Rhetorical bridge, restatement, transition, confirmation, or interpretation-only text should not become standalone tasks.
  - Absorb such non-substantive text into the nearest substantive chunk mention.
- Sparse operation extraction:
  - Treat the explanation as a set of text spans with possible visual/computational intent.
  - Create tasks only for spans that actually describe an operation-bearing act.
  - It is acceptable for explanatory, rhetorical, or interpretive spans to have no task.
  - Never use task count to mirror sentence count or chunk count.
- Only extract operations that are explicitly mentioned in the explanation.
  - Do NOT invent extra steps just because an op exists in allowed_ops.
  - Do NOT add operations that are logically implied but not stated —
    Step-Compose handles intermediate steps at compose-time.
  - "clearly implied" means: the current chunk directly describes the action or result for this op.
    It does NOT mean: "this op will eventually be needed to reach the final answer."
- CRITICAL: Do NOT anticipate future operations based on semantic inference across chunks.
  - Do NOT add a task to chunk N just because it logically prepares for an operation in chunk N+1.
  - Example (WRONG):
    Chunk 1: "retrieve value of 2016 and 2017"
    → LLM infers: "these two values will be diffed later, so I should add a diff task here"
    → Output: [retrieveValue(2016), retrieveValue(2017), diff(...)] ✗
  - Example (RIGHT):
    Chunk 1: "retrieve value of 2016 and 2017" (only retrieve is mentioned)
    → Output: [retrieveValue(2016), retrieveValue(2017)] (no diff)
    Chunk 3: "get the difference of the retrieved values"
    → Output: [diff(...)] (diff goes here, where it is explicitly mentioned)
  - Rationale: Step-Compose will compose operations across chunk boundaries. Inventory must not pre-compose.
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
  - include prerequisite steps (filter/aggregate/diff) needed to derive the final intended artifact.
  - avoid redundant branches that do not contribute to the final artifact.
- sentenceIndex MUST be the 1-based order of the meaningful chunk that explicitly names or describes this task's action.
  - Assign a task to the chunk whose verb/action directly corresponds to this op
    (e.g., "retrieve" → retrieveValue, "difference" → diff, "filter" → filter).
  - Do NOT assign a task to a chunk just because it provides input data for the task.
  - The fact that chunk 1 produces values that a later op will consume
    does NOT mean that later op belongs in sentenceIndex=1.
    If an op is only mentioned in chunk 3, it gets sentenceIndex=3.
- mention should quote or briefly summarize the full meaningful chunk, not just one sentence fragment.
- paramsHint must be FLAT (no nested objects). Keep it minimal.
- Role tokens allowed in paramsHint values:
  - "@primary_dimension", "@primary_measure", "@series_field"
- Series restriction:
  - Never represent series selection as a filter on the series field.
  - paramsHint.group is ONLY for series restriction on substantive ops.
  - Use paramsHint.group="<series value>" on single-group ops such as average/count/findExtremum/sort/retrieveValue/lagDiff/nth.
  - Use paramsHint.group=["A","B"] only for FilterOp series restriction; a list means OR semantics across listed series values.
  - Never use paramsHint.group to encode primary-dimension subsets such as years/categories/labels.
  - If the explanation names a subset of primary-dimension values, emit a filter task with include/exclude/between instead.
- Subset-based aggregate pattern:
  - When an aggregate/ranking op applies to a subset of primary-dimension values, inventory must emit:
    1. a subset-selection task (typically filter on @primary_dimension or another categorical field)
    2. a substantive op that consumes that subset later (average/count/findExtremum/sort/etc.)
  - Do NOT encode the subset directly inside paramsHint.group for those ops.
- Filter task must choose a mode:
  - If you output a task with op="filter", paramsHint MUST include EITHER:
    - membership mode: include and/or exclude
    - comparison mode: operator AND value (both)
    - group-only mode: group only (series restriction)
  - In membership mode, paramsHint.field may be any categorical field (except series_field).
  - If the explanation only says "filter only A and B" and A/B are series values (from series_domain),
    do NOT create a group-only filter task; attach the series restriction to other substantive tasks via paramsHint.group.
- DATA RESOLUTION RULE: When a task requires selecting a specific subset of data items
  (e.g., "top N", "highest N", "lowest N", "bottom N", "most recent N", "largest N",
  "smallest N", or any phrase asking to pick N specific items by value ranking):
  1. Check if you can determine the actual values from rows_preview.
  2. If YES: use op="filter" with paramsHint.include=[<specific_values_from_rows_preview>].
     - Read rows_preview, sort mentally by the relevant measure field,
       and extract the N dimension values directly.
  3. If NO (e.g., the subset depends on an intermediate computed result not yet available):
     - Fall back to dynamic ops (sort, nth, findExtremum).
  Principle: rows_preview is provided so you can resolve data-dependent selections AT INVENTORY TIME.
  Always prefer resolving to concrete values over deferring to runtime sorting.
  Example:
    rows_preview: [{Year:"2018", prod:100}, {Year:"2019", prod:95}, {Year:"2017", prod:80}, ...]
    explanation: "find the top 2 years by production"
    → filter(field="Year", include=["2018", "2019"])  ← resolved from rows_preview
    NOT: sort(desc) + nth(1,2)
  Example:
    explanation: "compute the average for 2010, 2013, and 2017"
    → filter(field="@primary_dimension", include=["2010", "2013", "2017"])
    → average(field="@primary_measure")
    NOT: average(field="@primary_measure", group=["2010", "2013", "2017"])
- CHUNK-LEVEL COMPLETENESS:
  The final substantive chunk(s) should collectively support the final answer to the QUESTION.
  Read the QUESTION to understand the answer structure, but do not invent tasks for chunks that do not explicitly introduce an operation.

- MULTI-OP GENERATION PER CHUNK:
  A single meaningful chunk may require MULTIPLE ops to be extracted.
  - Example:
    explanation: "Filter for the revenue of Thailand and the Philippines"
    question: "in which years did Thailand's revenue exceed Philippines?"
    → This chunk requires TWO ops:
      1) filter(field="Country", include=["Thailand", "Philippines"])  ← the explicit "filter"
      2) pairDiff(...) ← implicit pairwise comparison to prepare for later question answering
      So taskIds: o1 (filter), o2 (pairDiff) with sentenceIndex=1 for both.
    → Do NOT create filter-only (no pairDiff) just because the chunk only mentions "filter".
    → The question context ("Thailand exceeded Philippines") reveals that pairDiff is needed.

- PAIRDIFF GROUPORDER SEMANTICS:
  For pairDiff(groupA, groupB):
  - Read the QUESTION to understand which direction the comparison should go.
  - groupA should be the SUBJECT being asked about (numerator in the division).
  - groupB should be the BASELINE/COMPARISON target (denominator).
  - Example:
    question: "in which years did Thailand's revenue exceed that of Philippines?"
    → groupA="Thailand" (the subject being analyzed)
    → groupB="Philippines" (the baseline it is compared against)
    → signed=true (so positive result = Thailand > Philippines)
  - Counter-example (WRONG):
    question: "in which years did Thailand's revenue exceed Philippines?"
    → groupA="Philippines", groupB="Thailand"  ← WRONG: reversed
    → This would make positive results mean Philippines > Thailand, contradicting the question.

Question:
$question

Explanation:
$explanation

Chart context:
$chart_context_json

Rows preview:
$rows_preview_json
