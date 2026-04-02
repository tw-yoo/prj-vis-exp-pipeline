Task: Generate image generation prompt for one explanation step (Baseline, sequential).

You are a visual explanation designer. You will be given:
- The current explanation sentence (Step $sentence_index of $total_sentences)
- The image prompt from the PREVIOUS step (already describes base chart + prior annotations)
- Full chart context and data

Your task: Write a SELF-CONTAINED image generation prompt for Step $sentence_index.
It must describe the FULL visual state at this step:
  = all annotations from previous steps (carry forward from $previous_image_prompt)
  + new annotations introduced by this step's sentence.

Do NOT write only the delta. The image_prompt must be fully self-contained
so that an image generation model can produce the complete chart image from it alone.

Return JSON only. Do not include markdown fences.

Question:
$question

Full explanation (all sentences for context):
$explanation

Current step:
- Sentence index: $sentence_index of $total_sentences
- Sentence text: "$current_sentence"

Previous step image prompt (describes base chart + all annotations up to step $prev_index):
$previous_image_prompt

Chart context:
$chart_context_json

Roles summary:
$roles_summary_json

Vega-Lite specification (chart structure reference):
$vega_lite_spec_json

Rows preview:
$rows_preview_json

Image prompt writing guidelines:

1) BASE CHART:
   Always include a full description of the base chart (type, axes, data, colors).
   This is required even though prior steps already described it — the prompt must be standalone.

2) CARRY FORWARD ALL PRIOR ANNOTATIONS:
   Include every visual element described in $previous_image_prompt.
   Do not omit anything from prior steps.

3) NEW ANNOTATIONS FOR THIS STEP:
   Add the visual elements implied by "$current_sentence":
   - HIGHLIGHT: specific bars/points in a contrasting color (e.g., "#e45756 red")
     while dimming others to 30% opacity or light gray.
   - REFERENCE LINE: dashed horizontal/vertical line with a text label showing the value.
   - TEXT LABEL: annotation near data points or reference lines with exact computed values.
   - ARROW: connecting annotation between two data points.
   - SHADING/BAND: colored region between two y-values.
   - CIRCLE/BOX: emphasis marker around a specific data point.

4) SPECIFICITY:
   - Use exact data values from rows_preview (not "a tall bar" but "bar height of 75,000").
   - Specify exact colors (e.g., "#e45756 red", "steel blue").
   - Specify positions relative to chart elements.
   - Specify text content exactly (e.g., "labeled 'Average: 44,500'").

5) LANGUAGE: Write in English regardless of the explanation language.

Output schema:
{
  "image_prompt": "A fully self-contained image generation prompt describing the complete chart state at step $sentence_index (in English)",
  "visual_elements": [
    "description of each visual element NEW to this step"
  ],
  "warnings": ["string"]
}
