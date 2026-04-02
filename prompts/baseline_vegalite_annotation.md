Task: Generate Annotated Vega-Lite Specification for Visual Chart Explanation (Baseline).

You are a Vega-Lite expert. Given a Vega-Lite chart specification, a question about
the chart, and a natural-language explanation of the answer, your task is to produce
a modified Vega-Lite specification that adds annotation layers to visually explain
the answer.

The output must be a valid Vega-Lite JSON specification that extends the original
chart with annotation layers (reference lines, text marks, highlights, bands, etc.).

Return JSON only. Do not include markdown fences.

Roles summary:
$roles_summary_json

Series domain (values for series_field; empty list if unknown):
$series_domain_json

Measure fields (numeric candidates):
$measure_fields_json

Few-shot examples:
$few_shot_examples

Vega-Lite Annotation Techniques Reference:

1) LAYER COMPOSITION:
   The primary pattern for adding annotations is Vega-Lite's "layer" composition.
   Wrap the original spec as the first layer, then append annotation layers.

   Structure:
   {
     "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
     "width": <original_width>,
     "height": <original_height>,
     "data": <original_data>,
     "layer": [
       <original_chart_as_first_layer>,
       <annotation_layer_1>,
       <annotation_layer_2>,
       ...
     ]
   }

   If the original spec already uses "layer", append to the existing layers array.
   If the original spec uses a single "mark", convert it to a layer structure first.

2) REFERENCE LINES (rule mark):
   For horizontal reference lines (e.g., average, threshold):
   {
     "mark": {"type": "rule", "strokeDash": [4, 4], "strokeWidth": 1.5},
     "encoding": {
       "y": {"datum": <numeric_value>},
       "color": {"value": "#e45756"}
     },
     "description": "Reference line for average value"
   }

   For vertical reference lines:
   {
     "mark": {"type": "rule", "strokeDash": [4, 4]},
     "encoding": {
       "x": {"datum": "<category_value>"}
     }
   }

3) TEXT ANNOTATIONS (text mark):
   For labels near data points or reference lines:
   {
     "mark": {
       "type": "text",
       "align": "left",
       "dx": 5,
       "dy": -10,
       "fontSize": 12,
       "fontWeight": "bold"
     },
     "encoding": {
       "x": {"datum": "<x_value>"},
       "y": {"datum": <y_value>},
       "text": {"value": "Average: 50,000"},
       "color": {"value": "#e45756"}
     },
     "description": "Text label showing average value"
   }

4) HIGHLIGHTING (conditional encoding):
   To highlight specific bars/points in a contrasting color:
   Modify the original layer's color encoding with a condition:
   {
     "mark": "<original_mark>",
     "encoding": {
       ...original_encoding...,
       "color": {
         "condition": {
           "test": "datum['<field>'] == '<value1>' || datum['<field>'] == '<value2>'",
           "value": "#e45756"
         },
         "value": "#d3d3d3"
       },
       "opacity": {
         "condition": {
           "test": "datum['<field>'] == '<value1>' || datum['<field>'] == '<value2>'",
           "value": 1
         },
         "value": 0.3
       }
     }
   }

5) BANDS/REGIONS (rect mark):
   For shaded regions (e.g., value ranges):
   {
     "mark": {"type": "rect", "opacity": 0.15},
     "encoding": {
       "y": {"datum": <lower_value>},
       "y2": {"datum": <upper_value>},
       "color": {"value": "#4c78a8"}
     },
     "description": "Band showing data range"
   }

6) CONNECTING LINES (rule mark between points):
   For comparison arrows or difference indicators:
   {
     "mark": {"type": "rule", "strokeWidth": 2},
     "encoding": {
       "x": {"datum": "<category_A>"},
       "x2": {"datum": "<category_B>"},
       "y": {"datum": <y_value>},
       "color": {"value": "#e45756"}
     },
     "description": "Connecting line for comparison"
   }

7) POINT EMPHASIS (point/circle mark):
   To emphasize specific data points:
   {
     "mark": {"type": "point", "size": 200, "filled": true, "strokeWidth": 2},
     "encoding": {
       "x": {"datum": "<x_value>"},
       "y": {"datum": <y_value>},
       "color": {"value": "#e45756"}
     }
   }

8) COMPUTED VALUES VIA TRANSFORMS:
   For calculated annotations (e.g., average line computed from data):
   {
     "mark": "rule",
     "transform": [
       {"aggregate": [{"op": "mean", "field": "<measure_field>", "as": "avg_val"}]}
     ],
     "encoding": {
       "y": {"field": "avg_val", "type": "quantitative"}
     }
   }

   Alternatively, for simpler cases, embed the pre-computed literal value directly
   using "datum" encoding (preferred when you can compute the value from rows_preview).

Output schema:
{
  "annotated_spec": {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "...": "complete Vega-Lite specification with annotation layers"
  },
  "annotation_summary": [
    {
      "sentenceIndex": 1,
      "layers_added": [
        "description of each annotation layer added for this sentence"
      ],
      "computed_values": {
        "key": "value (e.g., average: 42.5, diff: 15.2)"
      }
    }
  ],
  "warnings": ["string"]
}

Rules:

1) PRESERVE THE ORIGINAL CHART:
   - The original chart marks, encoding, and data MUST be preserved.
   - Only ADD annotation layers; never remove or modify existing layers.
   - If the original spec has a single mark (not layered), convert it to
     a layer structure with the original spec as the first layer.

2) VALID VEGA-LITE:
   - The output annotated_spec MUST be valid Vega-Lite v5 JSON.
   - All encoding references must use fields that exist in the data.
   - Numeric values must be actual numbers, not strings.
   - Use "datum" for literal values, "field" for data-bound values.

3) SENTENCE-TO-LAYER MAPPING:
   - Each explanation sentence should produce one or more annotation layers.
   - Add a "description" property to each annotation layer indicating which
     sentence it corresponds to and what it visualizes.
   - Format: "Step {sentenceIndex}: {purpose}"

4) DATA-GROUNDED ANNOTATIONS:
   - Compute actual values from rows_preview for annotations.
   - For averages: calculate the mean from the data.
   - For differences: calculate the actual difference.
   - For extrema: identify the actual min/max values.
   - Use "datum" encoding with computed literal values (preferred over transforms
     for accuracy and simplicity).

5) COLOR CONSISTENCY:
   - Use a consistent annotation color scheme:
     - Primary highlight: "#e45756" (red)
     - Secondary highlight: "#4c78a8" (blue)
     - Reference lines: "#e45756" with strokeDash [4,4]
     - Text labels: same color as the element they describe
     - Dimmed elements: opacity 0.3 or color "#d3d3d3"

6) TEXT READABILITY:
   - Position text labels to avoid overlapping chart elements.
   - Use appropriate font sizes (11-14px).
   - Include computed values in text labels where relevant.
   - Align text relative to reference elements (left/right/center).

7) ANNOTATION SUMMARY:
   - The annotation_summary array describes what was added for each sentence.
   - Include any computed values (averages, sums, differences) used in annotations.
   - This serves as a traceability record.

Question:
$question

Explanation:
$explanation

Explanation sentences (deterministic split; 1-based indices):
$explanation_sentences_json

Original Vega-Lite specification:
$vega_lite_spec_json

Chart context:
$chart_context_json

Rows preview:
$rows_preview_json
