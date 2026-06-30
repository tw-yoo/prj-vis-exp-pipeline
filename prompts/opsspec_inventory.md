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
  - "add two computed values" / "add A and B" implies an "add" operation task (usually scalar+scalar addition; Step-Compose fills targetA/targetB via "ref:nX" at compose time).
  - "percent change" / "% increase" / "% decrease" / "increased by X%" implies a "diff" task with paramsHint.percent=true. (Sign direction is decided by Step-Compose from the question; do not pre-assign.)
  - "ratio of A to B" / "A is N times B" / "X-fold" implies a "diff" task with paramsHint.mode="ratio". (Step-Compose fills targetA/targetB or groupA/groupB.)
  - "share of" / "as a fraction of total" / "percent of total" implies a "diff" task with paramsHint.aggregate="percentage_of_total". Prefer this over a manual sum+diff chain when the explanation is "X's share of the total".
  - "absolute difference" / "magnitude of the gap" / "how far apart" implies one of: (a) "diff" task with paramsHint.signed=false for two-target scalar comparison, (b) "pairDiff" task with paramsHint.absolute=true when the comparison is per-key across two series, or (c) "lagDiff" task with paramsHint.absolute=true when computing magnitudes of adjacent-period changes.
  - OPERAND COMPLETENESS for diff/add (binary scalar ops): a "diff" or "add" task ALWAYS consumes exactly TWO operand values, and each operand must be produced by its own node — these ops cannot read a bare category/series label on their own. So when the explanation asks for the difference / sum / ratio between two SPECIFIC NAMED chart values that have not been computed yet (e.g. "the gap between Family and Local community", "Very unlikely in A minus Very unlikely in B", "sales of X plus sales of Y"), emit a "retrieveValue" task for EACH of the two operands FIRST (one per value; use paramsHint.target for the category and paramsHint.group for the series when the value is a specific series point), THEN the "diff"/"add" task. Never emit a lone diff/add whose operands are raw labels with no preceding retrieveValue (or other value-producing) tasks — Step-Compose cannot manufacture the missing operands and the spec is rejected (diff requires exactly two input nodes). EXCEPTION: when the two operands are ALREADY-computed prior results (e.g. two averages, two sums, two extrema from earlier tasks), do NOT add retrieveValue — the diff/add just references those existing nodes.
  - MULTI-ROW SELECTIONS REDUCE WITH sum/average/count, NOT add/diff: an "nth" or "findExtremum" task whose paramsHint.n / paramsHint.rank is a LIST (e.g. n=[2,3,4], "the middle three", "the top two values") returns ONE node holding several rows — NOT one node per position. To total or average those rows into a single value, emit ONE "sum" (or "average"/"count") task over that single node. Example: "the sum of the three median values" → sort → nth(paramsHint.n=[2,3,4]) → sum (one input). Do NOT emit "add"/"diff" referencing ref:n2, ref:n3, ref:n4 as if each position were its own node — only one multi-row node was produced, and add/diff are strictly for combining exactly TWO already-separate named scalars.
  - "leftmost" / "rightmost" / "first from the left/right" / "Nth from the right" implies an "nth" task with paramsHint.from="left" or "right". If the explanation also names a sort dimension ("leftmost when sorted by Year"), include paramsHint.orderField="<that field>".
  - "for each row/year/category, distance from V" / "deviation from the overall average" / "residual from baseline" / "how far each value is from V" implies a "diffByValue" task. paramsHint.value=<numeric literal> when V is a constant; paramsHint.targetValue="ref:nX" when V comes from a prior scalar node (set this at compose time). paramsHint.signed=false only when the explanation explicitly says "absolute distance / magnitude". Distinguish from "diff" (which compares two specific targetA/targetB scalars) and "lagDiff" (which compares adjacent rows in a sequence): diffByValue compares EVERY row against ONE reference V.
  - "doubled" / "tripled" / "halved" / "× N" / "÷ N" / "N times the X" / "convert to percentage" / "the midpoint of A and B (= (a+b)/2)" implies a "scale" task with paramsHint.factor=<numeric>. paramsHint.target should be a scalar ref "ref:nX" pointing to the value being scaled. Common factor values: 2 ("doubled"), 0.5 ("halved" / "average of two = (a+b)×0.5"), 100 ("to percent"), 0.01 ("to fraction"). For the "(a+b)/2" pattern, emit an "add" task first then a "scale" task with factor=0.5; do NOT collapse into one op.
  - "spread" / "variation" / "range between highest and lowest" / "max minus min" implies a "range" task. Prefer this single op over the verbose chain findExtremum(max)+findExtremum(min)+diff when the explanation is purely about the spread of a slice. If the slice is one series, set paramsHint.group=<series>.
  - "3-year average" / "5-year average" / "consecutive N-year window" / "moving average / moving sum" implies a "rollingWindow" task with paramsHint.window=N and paramsHint.aggregate="avg|sum|min|max" (default "avg" when the explanation says "average"). Set paramsHint.orderField to the sliding axis dimension (typically "Year" / "Date"). Chain with findExtremum or nth at compose time when the question asks for the best/worst window.
  - "longest period of decrease/increase" / "longest continuous run of decreasing/increasing" / "decrease period" / "stretch of consecutive declines" implies a "monotonicRun" task with paramsHint.direction="decreasing|increasing" and paramsHint.mode="longest". If the explanation specifies a minimum length ("for more than 2 years", "≥ 3 consecutive"), include paramsHint.minLength accordingly.
  - "year/period when X starts to decrease/increase" / "the point where the trend turns" / "first break in the upward/downward trend" implies a "monotonicRun" task with paramsHint.mode="firstBreak" and paramsHint.direction set to the new trend direction.
  - "every stretch of N consecutive increases/decreases" / "all runs of declines" implies a "monotonicRun" task with paramsHint.mode="all", paramsHint.direction set, and paramsHint.minLength=N when stated.
  - "sorted by X" / "in order of X" / "ordered by date/year/category" (where X is NOT the measure being aggregated) implies a "sort" task with paramsHint.orderField="<X field>". If the explanation says "sort by value/revenue/score" (the measure itself), use paramsHint.field=<measure> instead. The two are different: paramsHint.field is the value column to compare, paramsHint.orderField is an alternate key (typically a dimension) used to sort.
  - "year-over-year change" / "month-over-month" / "compared to the previous period/year" implies a "lagDiff" task with paramsHint.order="asc" (chronological by default). Use paramsHint.order="desc" only when the explanation explicitly reverses the direction.
  - "total of" / "sum of all" / "sum of X" / "add up all" / "add the values of (multiple points/bars)" (dataset row aggregation of N>=2 values or a row-slice, NOT scalar arithmetic) implies a "sum" task. `sum` is valid on ALL chart types including line (line+sum is visualized as line→bar then stacking the bars); group may be a single series or list of series. Choose sum-vs-add by VALUE COUNT, not chart type: use "sum" to total N>=2 points / a slice / many per-row diffs; use "add" only to combine EXACTLY TWO named scalars (two prior computed values, or two specific co-located series values at one x).
  - "how many" / "number of" / "count of" / "tally" / "how many years/months/items satisfy X" implies a "count" task on a prior filtered slice. Emit a prerequisite filter task that captures the condition (e.g., "above the average" → filter(operator=">", value="ref:n_avg")) and a follow-on count task. Do NOT encode the count condition inside the count task itself; count just tallies the rows of its input slice.
  - "is A greater/less/equal to B" / "is X above/below threshold Y" / "did X exceed Y" / "yes/no" terminal comparison implies a "compareBool" task with paramsHint.operator (e.g., ">", "<", "==", ">=", "<="). For scalar-vs-scalar comparison (two prior nodes or one prior node + literal), Step-Compose fills targetA/targetB via "ref:nX" or literal at compose time. Use this when the question is a yes/no question or when the explanation ends with a "since X > Y" / "X is larger than Y, so..." conclusion.
  - "is the average of A greater than the average of B" / "compare the average of group A vs group B" (where A/B are series values) implies a "compareBool" task with paramsHint.aggregate="avg", paramsHint.groupA="A", paramsHint.groupB="B", and paramsHint.operator (e.g., ">"). Other slice-aggregate operators are "sum"/"min"/"max". If A/B are categorical values of a non-series field, emit a prerequisite filter task first instead of using this shortcut.
  - "common to both X and Y" / "appear in both" / "in both A and B" / "shared between" / "intersection of two filter results" implies **two filter tasks** with appropriate sentenceIndex order. The second filter should narrow further on the first filter's result; Step-Compose connects them by putting the first filter's nodeId in the second filter's `inputs` at compose time. The chained filter then runs on the first filter's row result, naturally producing the intersection of the two target sets. **Never emit op="setOp"** — it has been removed from the operation set.
  - "either A or B" / "in A or B" / "union of A and B" (same field, just combine values) implies a **single filter task** with paramsHint.include=[list of A values + B values]. Do not emit two filter tasks for this; do not emit op="setOp".
  - "satisfying A and B" where A and B refer to **different fields** (e.g., "year=2020 AND region=APAC") also implies **two filter tasks chained via Step-Compose inputs**, identical to the same-field intersection pattern. Each filter narrows the dataset on its own field.
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
- Optional paramsHint keys recognized by Step-Compose (FLAT, no nested objects):
  - `percent` (bool — for `diff` task; emit only when explanation explicitly says "percent change" or "%")
  - `mode` (string — only `"ratio"` is meaningful here; the default `"difference"` does not need to be emitted)
  - `aggregate` (string — one of `"sum"`/`"avg"`/`"min"`/`"max"`/`"percentage_of_total"`; applies to `diff` and `compareBool` slice-aggregate forms)
  - `absolute` (bool — for `diff`, `pairDiff`, and `lagDiff` tasks)
  - `from` (string — `"left"` or `"right"`, for `nth` tasks only)
  - `orderField` (string — alternate sort key dimension, for `sort` and `nth` tasks)
  - `order` (string — `"asc"` or `"desc"`, for `sort`/`nth`/`lagDiff` when explicitly directional)
  - `targetAxis` (string — `"x"` (default) or `"y"`, for `retrieveValue` only). Emit `"y"` ONLY when the explanation explicitly asks for an x-axis category given a numeric measure value (reverse lookup), e.g. "어느 해에 65를 기록했나" / "which country had a rating of 60". Otherwise omit (forward `x` is the default).
  - These are HINTS to help Step-Compose pick the right field configuration. Step-Compose may override them based on chart_context and the final-artifact intent. Emit them only when the explanation explicitly suggests them; never invent.
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
- NEVER emit a task with op="setOp". The set-theoretic combination of two filter result sets (intersection or union) is expressed by chaining filters via meta.inputs at Step-Compose time, not by a dedicated op. setOp is no longer in the allowed operation set.
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
