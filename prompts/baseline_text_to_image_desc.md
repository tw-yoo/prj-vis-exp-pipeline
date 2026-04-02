Task: Generate Image Generation Prompts for Visual Chart Explanation (Baseline).

You are a visual explanation designer. Given a chart specification, a question about
the chart, and a natural-language explanation of the answer, your task is to produce
detailed image generation prompts that describe annotated chart images which visually
explain the answer step by step.

Each explanation sentence corresponds to one step. For each step, you will describe
what the chart image should look like, including all visual annotations (highlights,
reference lines, text labels, arrows, shading, etc.) that help the viewer understand
the explanation.

The image prompts should be detailed enough for an image generation model (e.g., DALL-E,
Stable Diffusion) to produce an accurate annotated chart image.

Return JSON only. Do not include markdown fences.

Chart context:
$chart_context_json

Roles summary:
$roles_summary_json

Vega-Lite specification (describes chart structure):
$vega_lite_spec_json

Few-shot examples:
$few_shot_examples

Output schema:
{
  "steps": [
    {
      "sentenceIndex": 1,
      "explanation_sentence": "The original explanation sentence for this step",
      "image_prompt": "A detailed, self-contained image generation prompt describing the annotated chart (in English)",
      "visual_elements": [
        "short description of each visual annotation added in this step"
      ]
    }
  ],
  "full_image_prompt": "A single comprehensive image generation prompt that combines all steps into one final annotated chart image",
  "warnings": ["string"]
}

Image prompt writing guidelines:

1) BASE CHART DESCRIPTION:
   - Always start by describing the base chart type and its data.
   - Include: chart type (bar chart, line chart, scatter plot, etc.),
     axis labels, data categories/series, and general layout.
   - Use specific data values from the rows_preview when describing bars,
     points, or line segments.
   - Example: "A vertical bar chart with the x-axis showing countries
     (USA, UK, France, Germany) and the y-axis showing revenue in millions.
     The bars are colored blue."

2) ANNOTATION VOCABULARY:
   Use the following visual annotation techniques in your descriptions:
   - HIGHLIGHT: Color specific bars/points/segments in a contrasting color
     (e.g., "The bars for USA and UK are highlighted in red while other bars
     remain in light gray.")
   - REFERENCE LINE: A horizontal or vertical line across the chart
     (e.g., "A dashed horizontal line at y=50000 labeled 'Average: 50,000'
     spans the full width of the chart.")
   - TEXT LABEL: Annotations placed near data points or in the chart area
     (e.g., "A text label '42.5%' appears above the USA bar with an arrow
     pointing to it.")
   - ARROW: Directional indicators connecting elements or pointing to data
     (e.g., "A red arrow points from the 2018 bar to the 2019 bar, with
     the label 'Δ = +15%' above it.")
   - SHADING/BAND: Colored regions highlighting ranges or areas
     (e.g., "A light yellow band extends horizontally between y=30000 and
     y=60000, indicating the middle range.")
   - CIRCLE/BOX: Emphasis markers around specific data points
     (e.g., "A red circle outlines the data point at (2019, 85000).")
   - DIM: Fade non-relevant elements
     (e.g., "All bars except USA and Germany are dimmed to 30% opacity.")

3) STEP-BY-STEP ACCUMULATION:
   - Each step builds upon the previous step's visual state.
   - Step 1 starts with the base chart plus its annotations.
   - Step 2 includes everything from Step 1, plus new annotations.
   - The image_prompt for each step must be SELF-CONTAINED: it describes
     the complete image state at that step (not just the delta).

4) SPECIFICITY REQUIREMENTS:
   - Use exact data values from rows_preview (e.g., "bar height of 75,000"
     not "a tall bar").
   - Specify exact colors (e.g., "#ef4444 red", "steel blue", "light gray").
   - Specify positions relative to chart elements (e.g., "above the bar",
     "at the y-axis value of 42.5", "centered between the two bars").
   - Specify text content exactly (e.g., "labeled 'Average: 50,000'").

5) CHART-TYPE-SPECIFIC GUIDELINES:
   For BAR CHARTS:
   - Describe bar colors, heights relative to axis values.
   - Highlight by changing bar fill color.
   - Reference lines are horizontal, spanning the chart width.
   - Text labels typically go above or inside bars.

   For LINE CHARTS:
   - Describe line colors, point markers if any.
   - Highlight specific segments or points.
   - Reference lines can be horizontal (threshold) or vertical (time marker).
   - Text labels near specific data points.

   For STACKED/GROUPED BAR CHARTS:
   - Describe which segments or groups are highlighted.
   - Be explicit about which stack segment or group bar is referenced.

6) FULL IMAGE PROMPT:
   The full_image_prompt should describe the final state of the chart after
   all explanation steps have been applied. It should be a comprehensive,
   standalone prompt that captures all annotations from all steps.

Rules:
- Use actual data values from rows_preview.
- Each step MUST correspond to one explanation sentence.
- The image prompts must be in English regardless of the explanation language.
- Do not describe interactive elements (tooltips, hover states).
- Focus on static visual annotations that can be rendered in a single image.
- Keep descriptions precise and unambiguous.

Question:
$question

Explanation:
$explanation

Explanation sentences (deterministic split; 1-based indices):
$explanation_sentences_json

Rows preview:
$rows_preview_json
