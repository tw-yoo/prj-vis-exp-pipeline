from typing import Any, List, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

from opsspec.core.models import ChartContext as OpsChartContext, RecursivePipelineTrace
from opsspec.specs.union import OperationSpec


class GenerateGrammarRequest(BaseModel):
    question: str = Field(..., min_length=1)
    explanation: str = Field(..., min_length=1)
    vega_lite_spec: dict = Field(..., description="Vega-Lite spec JSON")
    data_rows: list[dict] = Field(..., description="Raw data rows (<500 lines assumed)")
    debug: bool = True
    llm_backend: Literal["openai", "ollama"] | None = None
    openai_model: str | None = Field(None, description="OpenAI model override (e.g. 'gpt-5.2-mini'). Falls back to OPENAI_MODEL env or server default.")
    ollama_model: str | None = Field(None, description="Ollama model override (e.g. 'deepseek-r1:32b').")

    model_config = ConfigDict(extra="forbid")


class GenerateGrammarRequestBodyRequest(BaseModel):
    question: str = Field(..., min_length=1)
    explanation: str = Field(..., min_length=1)
    chart_id: str = Field(..., min_length=1, description="ChartQA chart id / Vega-Lite spec id")
    debug: bool = True
    llm_backend: Literal["openai", "ollama"] | None = None
    openai_model: str | None = Field(None, description="OpenAI model override.")
    ollama_model: str | None = Field(None, description="Ollama model override (e.g. deepseek-r1:32b).")

    model_config = ConfigDict(extra="forbid")


class GenerateGrammarResponse(BaseModel):
    ops_spec: dict[str, list[OperationSpec]] = Field(default_factory=dict)
    chart_context: OpsChartContext
    text_chunks: dict[str, str] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
    trace: RecursivePipelineTrace | None = None
    visual_execution_plan: dict = Field(default_factory=dict)

    model_config = ConfigDict(extra="forbid")


class D3BaseChart(BaseModel):
    chart_family: Literal["bar_simple", "bar_grouped", "bar_stacked", "line_simple", "line_multi"]
    d3_code: str = Field(..., min_length=1)
    converter_summary: dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(extra="forbid")


class D3AnnotationStepSpec(BaseModel):
    sentenceIndex: int = Field(..., ge=1)
    sentence: str = Field(..., min_length=1)
    annotated_d3_code: str = Field(..., min_length=1)
    annotations_added: list[str] = Field(default_factory=list)
    computed_values: dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(extra="forbid")


class GenerateD3AnnotationBaselineResponse(BaseModel):
    base_chart: D3BaseChart
    step_specs: list[D3AnnotationStepSpec] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)

    model_config = ConfigDict(extra="forbid")


class ExecutionPlanStep(BaseModel):
    id: str = Field(..., min_length=1)
    sentenceIndex: int = Field(..., ge=1)
    groupNames: list[str] = Field(default_factory=list)
    drawGroupNames: list[str] = Field(default_factory=list)
    splitGroup: str | None = None
    splitLifecycle: Literal["enter", "keep", "merge"] | None = None
    panelIds: list[str] = Field(default_factory=list)
    joinOp: str | None = None
    joinPolicy: Literal["keep-split", "merge"] | None = None
    parallel: bool = True

    model_config = ConfigDict(extra="forbid")


class ExecutionPlan(BaseModel):
    mode: Literal["sentence-step"] = "sentence-step"
    steps: list[ExecutionPlanStep] = Field(default_factory=list)

    model_config = ConfigDict(extra="forbid")


class RunPythonPlanRequest(BaseModel):
    scenario_path: str = Field(..., min_length=1)
    debug: bool = False

    model_config = ConfigDict(extra="forbid")


class RunPythonPlanResponse(BaseModel):
    scenario_path: str = Field(..., min_length=1)
    vega_lite_spec: dict = Field(default_factory=dict)
    draw_plan: dict[str, list[dict]] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)

    model_config = ConfigDict(extra="forbid")


class CompileOpsPlanRequest(BaseModel):
    vega_lite_spec: dict = Field(..., description="Vega-Lite spec JSON")
    data_rows: list[dict] = Field(..., description="Raw data rows")
    ops_spec: dict[str, list[dict]] = Field(default_factory=dict, description="OpsSpec group map (raw dict ops)")

    model_config = ConfigDict(extra="forbid")


class CompileOpsPlanResponse(BaseModel):
    ops_spec: dict[str, list[dict]] = Field(default_factory=dict)
    draw_plan: dict[str, list[dict]] = Field(default_factory=dict)
    execution_plan: ExecutionPlan = Field(default_factory=ExecutionPlan)
    visual_execution_plan: dict = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)

    model_config = ConfigDict(extra="forbid")


class CanonicalizeOpsSpecRequest(BaseModel):
    question: str = Field(..., min_length=1)
    explanation: str = Field(..., min_length=1)
    vega_lite_spec: dict = Field(..., description="Vega-Lite spec JSON")
    data_rows: list[dict] = Field(..., description="Raw data rows (<500 lines assumed)")
    ops_spec: dict[str, list[dict]] = Field(default_factory=dict, description="OpsSpec group map (raw dict ops)")

    model_config = ConfigDict(extra="forbid")


class CanonicalizeOpsSpecResponse(BaseModel):
    ops_spec: dict[str, list[dict]] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
    chart_context: OpsChartContext

    model_config = ConfigDict(extra="forbid")


class GenerateAnswerRequest(BaseModel):
    question: str = Field(..., min_length=1)
    vega_lite_spec_path: str = Field(..., min_length=1, description="Path to a Vega-Lite spec JSON file")
    data_csv_path: str = Field(..., min_length=1, description="Path to a CSV file containing chart data")
    llm: Literal["chatgpt", "gemini"] = Field(
        "chatgpt",
        description="LLM backend to use for the answer. Optional; defaults to chatgpt.",
    )
    debug: bool = False

    model_config = ConfigDict(extra="forbid")


class GenerateAnswerResponse(BaseModel):
    plan: list[str] = Field(default_factory=list)
    answer: str
    explanation: str
    warnings: list[str] = Field(default_factory=list)
    request_id: str = Field(..., min_length=1)

    model_config = ConfigDict(extra="forbid")


class RunModuleTraceRequest(BaseModel):
    question: str = Field(..., min_length=1)
    explanation: str = Field(..., min_length=1)
    vega_lite_spec_path: str = Field(..., min_length=1)
    data_csv_path: str = Field(..., min_length=1)

    model_config = ConfigDict(extra="forbid")


class RunModuleTraceResponse(BaseModel):
    inventory: dict = Field(default_factory=dict)
    steps: list[dict] = Field(default_factory=list)
    ops_spec: dict = Field(default_factory=dict)
    trace: dict = Field(default_factory=dict)
    chart_context: dict = Field(default_factory=dict)

    model_config = ConfigDict(extra="forbid")


# ── PIL Chart Annotator ────────────────────────────────────────────────────────

class ChartAreaSpec(BaseModel):
    """Pixel-space bounding box of the chart's plot area + axis ranges."""
    x: int = Field(..., description="Left edge of the plot area in pixels")
    y: int = Field(..., description="Top edge of the plot area in pixels")
    width: int = Field(..., description="Width of the plot area in pixels")
    height: int = Field(..., description="Height of the plot area in pixels")
    y_min: float = Field(0.0, description="Minimum data value on the y-axis")
    y_max: float = Field(100.0, description="Maximum data value on the y-axis")
    x_categories: List[str] = Field(
        default_factory=list,
        description="Ordered list of x-axis category labels (left to right)",
    )

    model_config = ConfigDict(extra="forbid")


class AnnotationItem(BaseModel):
    """A single visual annotation to draw on the chart image.

    Supported types:
      reference_line  — dashed horizontal line at a y data value
      text_label      — text string near a data point or at explicit pixel pos
      band            — shaded region between two y data values
      highlight_bar   — dim all bars except the specified categories
      circle          — emphasis circle around a data point
    """
    type: Literal["reference_line", "text_label", "band", "highlight_bar", "circle"]
    # reference_line / circle / text_label (y position in data coords)
    value: Optional[float] = Field(None, description="Y data value (reference_line, circle)")
    y_value: Optional[float] = Field(None, description="Alias for value (text_label anchor)")
    # text_label
    label: Optional[str] = Field(None, description="Text to display (text_label, reference_line)")
    x_category: Optional[str] = Field(None, description="X category to anchor label/circle")
    x_px: Optional[int] = Field(None, description="Explicit pixel x (overrides x_category)")
    y_px: Optional[int] = Field(None, description="Explicit pixel y (overrides y_value)")
    dx: int = Field(5, description="Horizontal offset for text_label")
    dy: int = Field(-12, description="Vertical offset for text_label")
    # band
    y_lower: Optional[float] = Field(None, description="Lower y bound for band")
    y_upper: Optional[float] = Field(None, description="Upper y bound for band")
    opacity: float = Field(0.15, description="Opacity for band")
    # highlight_bar
    categories: List[str] = Field(default_factory=list, description="Categories to highlight")
    highlight_color: str = Field("#e45756", description="Highlight bar color")
    dim_color: str = Field("#d3d3d3", description="Color for dimmed bars")
    dim_opacity: float = Field(0.55, description="Opacity of dim overlay (0–1)")
    # circle
    radius: int = Field(14, description="Circle radius in pixels")
    # shared
    color: str = Field("#e45756", description="Line/text/outline color (#RRGGBB)")
    line_width: int = Field(2, description="Line width in pixels")

    model_config = ConfigDict(extra="forbid")


class AnnotationStep(BaseModel):
    """One explanation step with its list of annotations."""
    sentence: str = Field("", description="Explanation sentence for this step")
    annotations: List[AnnotationItem] = Field(
        default_factory=list,
        description="Annotations to draw for this step (cumulative with prior steps)",
    )

    model_config = ConfigDict(extra="forbid")


class AnnotateChartImageRequest(BaseModel):
    """Request: annotate a chart image with PIL-drawn visual elements."""
    image_base64: str = Field(
        ...,
        description="Base64-encoded PNG of the base chart image",
    )
    chart_area: ChartAreaSpec = Field(
        ...,
        description="Plot area bounding box and axis ranges",
    )
    steps: List[AnnotationStep] = Field(
        ...,
        min_length=1,
        description="Ordered list of annotation steps (one per explanation sentence)",
    )
    return_each_step: bool = Field(
        True,
        description="If True, return an annotated image per step; if False, return only the final image",
    )

    model_config = ConfigDict(extra="forbid")


class AnnotatedStepResult(BaseModel):
    sentenceIndex: int
    sentence: str
    image_base64: str = Field(..., description="Base64-encoded annotated PNG")

    model_config = ConfigDict(extra="forbid")


class AnnotateChartImageResponse(BaseModel):
    steps: List[AnnotatedStepResult] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)

    model_config = ConfigDict(extra="forbid")
