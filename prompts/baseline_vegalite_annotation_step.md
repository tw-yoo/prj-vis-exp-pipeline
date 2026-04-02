Task: Add Vega-Lite annotation for one explanation step (Baseline, sequential).

You are a Vega-Lite expert. You will be given:
- The current explanation sentence (Step $sentence_index of $total_sentences)
- The accumulated Vega-Lite spec from all previous steps (already contains prior annotations)
- Full chart context and data

Your task: Add annotation layers for THIS STEP ONLY to the accumulated spec.
Do NOT re-add or re-describe annotations that already exist in $accumulated_spec_json.
The result must be the full accumulated spec (previous layers + new layers for this step).

Return JSON only. Do not include markdown fences.

Question:
$question

Full explanation (all sentences for context):
$explanation

Current step:
- Sentence index: $sentence_index of $total_sentences
- Sentence text: "$current_sentence"

Accumulated Vega-Lite spec (includes all annotations from steps 1 to $prev_index):
$accumulated_spec_json

Roles summary:
$roles_summary_json

Series domain:
$series_domain_json

Measure fields:
$measure_fields_json

Chart context:
$chart_context_json

Rows preview:
$rows_preview_json

Vega-Lite Annotation Techniques Reference:

1) LAYER COMPOSITION:
   If $accumulated_spec_json already uses "layer", append new annotation layers to it.
   If it uses a single "mark", convert to layer first (original mark as first layer).

2) REFERENCE LINES (rule mark):
   { "mark": {"type": "rule", "strokeDash": [4, 4], "strokeWidth": 1.5},
     "encoding": {"y": {"datum": <value>}, "color": {"value": "#e45756"}},
     "description": "Step $sentence_index: <purpose>" }

3) TEXT ANNOTATIONS (text mark):
   { "mark": {"type": "text", "align": "left", "dx": 5, "dy": -10, "fontSize": 12},
     "encoding": {"x": {"datum": "<x_val>"}, "y": {"datum": <y_val>},
                  "text": {"value": "<label>"}, "color": {"value": "#e45756"}},
     "description": "Step $sentence_index: <purpose>" }

4) HIGHLIGHTING (conditional encoding on the original mark layer):
   Modify the base mark layer's color/opacity encoding with condition:
   { "condition": {"test": "datum['<field>'] == '<val>'", "value": "#e45756"}, "value": "#d3d3d3" }

5) BANDS (rect mark):
   { "mark": {"type": "rect", "opacity": 0.15},
     "encoding": {"y": {"datum": <lower>}, "y2": {"datum": <upper>}, "color": {"value": "#4c78a8"}},
     "description": "Step $sentence_index: <purpose>" }

6) COLOR CONSISTENCY:
   - Primary highlight: "#e45756" (red)
   - Secondary: "#4c78a8" (blue)
   - Reference lines: "#e45756" with strokeDash [4,4]
   - Dimmed: opacity 0.3 or color "#d3d3d3"

Rules:
- Add a "description" property to every new layer: "Step $sentence_index: <purpose>"
- Use "datum" encoding with computed literal values from rows_preview (preferred over transforms)
- The output annotated_spec MUST be valid Vega-Lite v5 JSON
- Preserve ALL existing layers from accumulated_spec_json unchanged

Output schema:
{
  "annotated_spec": {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "...": "full accumulated spec including new annotation layers for this step"
  },
  "layers_added": ["short description of each layer added in this step"],
  "computed_values": {"key": <numeric_value>},
  "warnings": ["string"]
}
