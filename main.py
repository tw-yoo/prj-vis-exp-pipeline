from contextlib import asynccontextmanager
import csv
from datetime import datetime
import json
import logging
import os
import time
from pathlib import Path
import traceback
from threading import Lock
import uuid
from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import (
    AnnotateChartImageRequest,
    AnnotateChartImageResponse,
    CanonicalizeOpsSpecRequest,
    CanonicalizeOpsSpecResponse,
    CompileOpsPlanRequest,
    CompileOpsPlanResponse,
    GenerateD3AnnotationBaselineResponse,
    GenerateAnswerRequest,
    GenerateAnswerResponse,
    GenerateGrammarRequest,
    GenerateGrammarRequestBodyRequest,
    RunModuleTraceRequest,
    RunModuleTraceResponse,
    RunPythonPlanRequest,
    RunPythonPlanResponse,
)
from draw_plan import build_draw_ops_spec, export_draw_plan_to_public, validate_draw_groups_payload
from opsspec.runtime.scheduler import schedule_ops_spec
from opsspec.runtime.executor import OpsSpecExecutor
from opsspec.runtime.execution_plan import build_sentence_execution_plan
from opsspec.runtime.visual_execution_plan import build_visual_execution_plan
from opsspec.modules.pipeline import OpsSpecPipeline, _build_retry_feedback
from opsspec.modules.module_baseline_single_shot import run_baseline_single_shot
from opsspec.modules.module_baseline_d3_annotation import D3AnnotationStepValidationError, run_baseline_d3_annotation
from opsspec.modules.module_baseline_text_to_image import run_baseline_text_to_image
from opsspec.modules.module_baseline_vegalite_annotation import run_baseline_vegalite_annotation
from opsspec.modules.module_chart_annotator import annotate_chart_steps
from opsspec.modules.module_inventory import split_explanation_sentences
from opsspec.modules.prompt_examples import (
    build_single_shot_few_shot_examples,
    build_text_to_image_few_shot_examples,
    build_vegalite_annotation_few_shot_examples,
    tune_few_shot_budget,
)
from opsspec.runtime.op_registry import build_ops_contract_for_prompt
from opsspec.core.llm import StructuredLLMClient
from opsspec.modules.answer_pipeline import (
    ChartAnswerPipeline,
    _load_csv_file,
    _load_json_file,
    _project_root,
    _resolve_path_under_root,
)
from opsspec.runtime.python_scenario_loader import PythonScenarioLoadError, load_python_scenario_request
from opsspec.runtime.ui_schema import build_op_registry_ui_schema
from opsspec.runtime.context_builder import build_chart_context
from opsspec.runtime.canonicalize import canonicalize_ops_spec_groups
from opsspec.runtime.chartqa_loader import load_chartqa_case
from opsspec.runtime.vegalite_to_d3 import convert_vegalite_to_d3
from opsspec.runtime.baseline_repair import autorepair_ops_groups, build_repair_feedback
from opsspec.validation.endpoint_validators import validate_and_parse_ops_spec_groups, validate_refs_against_node_ids
from opsspec.core.utils import prune_nulls

logger = logging.getLogger(__name__)
trace_logger = logging.getLogger("pipeline_trace")
_GRAMMAR_RESULT_FIELDS = ["chart_id", "model", "question", "explanation", "vega_lite_spec", "spec"]
_grammar_result_lock = Lock()


def _error_reports_dir() -> Path:
    return Path(__file__).resolve().parents[1] / "data" / "expert_prompt_reports"


def _grammar_result_csv_path() -> Path:
    return Path(__file__).resolve().parent / "grammar_result.csv"


def _chart_id_from_vega_spec(vega_lite_spec: Dict[str, Any]) -> str:
    data = vega_lite_spec.get("data") if isinstance(vega_lite_spec, dict) else None
    url = data.get("url") if isinstance(data, dict) else None
    if not isinstance(url, str) or not url.strip():
        return ""
    return Path(url.strip()).stem


def _stable_json(value: Any) -> str:
    return json.dumps(prune_nulls(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _read_cached_grammar_spec(
    *,
    chart_id: str,
    model: str,
    question: str,
    explanation: str,
    vega_lite_spec: Dict[str, Any],
) -> Dict[str, Any] | None:
    path = _grammar_result_csv_path()
    if not path.exists():
        return None

    vega_lite_spec_text = _stable_json(vega_lite_spec)
    with _grammar_result_lock:
        try:
            with path.open("r", encoding="utf-8", newline="") as fp:
                reader = csv.DictReader(fp)
                for row in reader:
                    cached_vega_lite_spec = row.get("vega_lite_spec")
                    if cached_vega_lite_spec is not None and cached_vega_lite_spec != vega_lite_spec_text:
                        continue
                    if (
                        row.get("chart_id") == chart_id
                        and row.get("model") == model
                        and row.get("question") == question
                        and row.get("explanation") == explanation
                    ):
                        spec_text = row.get("spec") or ""
                        if not spec_text.strip():
                            continue
                        spec = json.loads(spec_text)
                        if isinstance(spec, dict):
                            return spec
        except Exception as exc:
            logger.warning("Failed to read grammar_result cache at %s: %s", path, exc)
    return None


def _append_grammar_result(
    *,
    chart_id: str,
    model: str,
    question: str,
    explanation: str,
    vega_lite_spec: Dict[str, Any],
    spec: Dict[str, Any],
) -> None:
    path = _grammar_result_csv_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    row = {
        "chart_id": chart_id,
        "model": model,
        "question": question,
        "explanation": explanation,
        "vega_lite_spec": _stable_json(vega_lite_spec),
        "spec": _stable_json(spec),
    }

    with _grammar_result_lock:
        write_header = not path.exists() or path.stat().st_size == 0
        with path.open("a", encoding="utf-8", newline="") as fp:
            writer = csv.DictWriter(fp, fieldnames=_GRAMMAR_RESULT_FIELDS)
            if write_header:
                writer.writeheader()
            writer.writerow(row)


def _grammar_cache_ops_groups(spec: Dict[str, Any]) -> Dict[str, Any]:
    return {
        key: value
        for key, value in (spec or {}).items()
        if isinstance(key, str) and (key == "ops" or (key.startswith("ops") and key[3:].isdigit()))
    }


def _grammar_cache_text_chunks(spec: Dict[str, Any]) -> Dict[str, str]:
    raw = (spec or {}).get("text_chunks")
    if not isinstance(raw, dict):
        return {}
    return {str(key): str(value) for key, value in raw.items() if isinstance(key, str) and isinstance(value, str)}


def _build_generate_grammar_response_payload(
    *,
    ops_spec: Dict[str, List[Any]],
    text_chunks: Dict[str, str] | None = None,
) -> Dict[str, Any]:
    # /generate_grammar는 grammar(=OpsSpec) + 문장 단위 텍스트만 반환한다.
    # draw_plan / execution_plan / visual_execution_plan 컴파일은 /compile_ops_plan 책임.
    groups_dump = {
        group_name: [op.model_dump(by_alias=True, exclude_none=True) for op in ops]
        for group_name, ops in ops_spec.items()
    }

    response_payload: Dict[str, Any] = dict(groups_dump)
    response_payload["text_chunks"] = text_chunks or {}
    return prune_nulls(response_payload)


def _parse_cached_ops_spec(
    *,
    spec: Dict[str, Any],
    vega_lite_spec: Dict[str, Any],
    data_rows: List[Dict[str, Any]],
) -> tuple[Dict[str, List[Any]], Any, List[str]]:
    chart_context, context_warnings, _rows_preview = build_chart_context(vega_lite_spec, data_rows)
    groups, parse_warnings, errors = validate_and_parse_ops_spec_groups(
        _grammar_cache_ops_groups(spec),
        chart_context,
    )
    errors.extend(validate_refs_against_node_ids(groups))
    if errors:
        raise ValueError("Cached grammar spec validation failed:\n- " + "\n- ".join(errors))
    scheduled_groups = schedule_ops_spec(groups)
    return scheduled_groups, chart_context, list(context_warnings) + parse_warnings


def _safe_line(value: str, *, max_len: int = 500) -> str:
    normalized = " ".join(value.split())
    if len(normalized) <= max_len:
        return normalized
    return normalized[: max_len - 3] + "..."


def _extract_encoding_fields(spec: Dict[str, Any]) -> List[str]:
    encoding = spec.get("encoding")
    if not isinstance(encoding, dict):
        return []
    fields: List[str] = []
    for channel_spec in encoding.values():
        if not isinstance(channel_spec, dict):
            continue
        field = channel_spec.get("field")
        if isinstance(field, str) and field and field not in fields:
            fields.append(field)
    return fields


def _write_error_report(
    *,
    endpoint: str,
    request_id: str,
    elapsed_ms: float,
    error: Exception,
    request_summary: Dict[str, Any],
) -> Path | None:
    try:
        out_dir = _error_reports_dir()
        out_dir.mkdir(parents=True, exist_ok=True)

        now = datetime.now()
        stamp = now.strftime("%Y%m%d_%H%M%S")
        file_name = f"{endpoint.strip('/').replace('/', '_')}_error_{stamp}_{request_id}.txt"
        path = out_dir / file_name

        lines: List[str] = [
            "# NLP Server Error Report",
            f"generated_at: {now.strftime('%Y-%m-%d %H:%M:%S %z')}",
            f"endpoint: {endpoint}",
            f"request_id: {request_id}",
            f"elapsed_ms: {elapsed_ms:.1f}",
            f"error_type: {type(error).__name__}",
            f"error_message: {_safe_line(str(error), max_len=1000)}",
            "",
            "## Request Summary",
        ]

        for key, value in request_summary.items():
            if isinstance(value, str):
                lines.append(f"{key}: {_safe_line(value, max_len=1000)}")
            else:
                lines.append(f"{key}: {value}")

        lines.extend(
            [
                "",
                "## Traceback",
                traceback.format_exc().rstrip(),
                "",
            ]
        )
        path.write_text("\n".join(lines), encoding="utf-8")
        return path
    except Exception:
        logger.exception(
            "Failed to write error report | endpoint=%s request_id=%s",
            endpoint,
            request_id,
        )
        return None


def configure_trace_logger(log_path: str) -> None:
    path = Path(log_path)
    if not path.is_absolute():
        path = Path.cwd() / path
    path.parent.mkdir(parents=True, exist_ok=True)

    for handler in list(trace_logger.handlers):
        trace_logger.removeHandler(handler)
        handler.close()

    file_handler = logging.FileHandler(path, mode="w", encoding="utf-8")
    file_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    trace_logger.addHandler(file_handler)
    trace_logger.setLevel(logging.INFO)
    trace_logger.propagate = False

    trace_logger.info("==== pipeline trace log initialized ====")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ollama_model = os.getenv("OLLAMA_MODEL", "deepseek-r1:14b")
    ollama_model = os.getenv("OLLAMA_MODEL", "qwen2.5:14b")
    ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://192.168.0.131:11434")
    ollama_api_key = os.getenv("OLLAMA_API_KEY", "ollama")
    trace_log_path = os.getenv("TRACE_LOG_PATH", "logs/pipeline_trace.log")

    configure_trace_logger(trace_log_path)
    trace_logger.info(
        "startup config | model=%s base_url=%s",
        ollama_model,
        ollama_base_url,
    )

    grammar_pipeline = OpsSpecPipeline(
        ollama_model=ollama_model,
        ollama_base_url=ollama_base_url,
        ollama_api_key=ollama_api_key,
        prompts_dir=Path(__file__).parent / "prompts",
    )
    answer_pipeline = ChartAnswerPipeline(
        ollama_model=ollama_model,
        ollama_base_url=ollama_base_url,
        ollama_api_key=ollama_api_key,
        prompts_dir=Path(__file__).parent / "prompts",
    )

    try:
        grammar_pipeline.load()
        answer_pipeline.load()
    except Exception:
        logger.exception("Failed to initialize NLP models during startup.")
        raise

    app.state.grammar_pipeline = grammar_pipeline
    app.state.answer_pipeline = answer_pipeline
    yield


app = FastAPI(
    title="Neuro-Symbolic Semantic Parser",
    version="1.0.0",
    lifespan=lifespan,
)

default_origins = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:5174,http://127.0.0.1:5174"
cors_origins = [
    origin.strip()
    for origin in os.getenv("CORS_ALLOW_ORIGINS", default_origins).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/op_registry")
async def op_registry():
    # UI-facing schema for specTest: op-specific parameter contract + ref rules.
    return prune_nulls(build_op_registry_ui_schema())


@app.post("/generate_grammar_request_body", response_model=GenerateGrammarRequest)
async def generate_grammar_request_body(request: GenerateGrammarRequestBodyRequest):
    request_id = uuid.uuid4().hex[:12]
    q_preview = " ".join(request.question.split())[:120]
    logger.info(
        '[/generate_grammar_request_body] request received | request_id=%s chart_id=%s question="%s"',
        request_id,
        request.chart_id,
        q_preview,
    )

    try:
        vega_lite_spec, data_rows = load_chartqa_case(request.chart_id)
    except FileNotFoundError as exc:
        logger.error(
            "[/generate_grammar_request_body] ChartQA file not found | request_id=%s chart_id=%s error=%s",
            request_id,
            request.chart_id,
            exc,
        )
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        logger.error(
            "[/generate_grammar_request_body] invalid ChartQA lookup | request_id=%s chart_id=%s error=%s",
            request_id,
            request.chart_id,
            exc,
        )
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return GenerateGrammarRequest(
        question=request.question,
        explanation=request.explanation,
        vega_lite_spec=vega_lite_spec,
        data_rows=data_rows,
        debug=bool(request.debug),
        llm_backend=request.llm_backend,
        openai_model=request.openai_model,
    )


@app.post("/canonicalize_opsspec", response_model=CanonicalizeOpsSpecResponse)
async def canonicalize_opsspec(request: CanonicalizeOpsSpecRequest):
    request_id = uuid.uuid4().hex[:12]
    started_at = time.perf_counter()
    q_preview = " ".join(request.question.split())[:120]
    logger.info('[/canonicalize_opsspec] request received | request_id=%s question="%s"', request_id, q_preview)

    trace_logger.info(
        "[request:%s] canonicalize_in | rows=%d groups=%d",
        request_id,
        len(request.data_rows),
        len(request.ops_spec or {}),
    )

    try:
        chart_context, ctx_warnings, _rows_preview = build_chart_context(
            request.vega_lite_spec,
            request.data_rows,
        )

        raw_groups = request.ops_spec or {}
        if not isinstance(raw_groups, dict):
            raise ValueError('ops_spec must be an object like {"ops":[...],"ops2":[...]}')

        groups, parse_warnings, errors = validate_and_parse_ops_spec_groups(raw_groups, chart_context)
        warnings: List[str] = list(ctx_warnings) + parse_warnings

        # "ops" 그룹이 없으면 빈 값으로 보장 (안정적인 UI 흐름)
        groups.setdefault("ops", [])

        # ref/inputs 가 실존하는 nodeId를 가리키는지 교차 검증
        errors.extend(validate_refs_against_node_ids(groups))

        if errors:
            raise ValueError("Validation failed:\n- " + "\n- ".join(errors))

        canonical_groups, canon_warnings = canonicalize_ops_spec_groups(groups, chart_context=chart_context)
        warnings.extend(canon_warnings)

        ops_dump = {
            group_name: [op.model_dump(by_alias=True, exclude_none=True) for op in ops]
            for group_name, ops in canonical_groups.items()
        }
        response = CanonicalizeOpsSpecResponse(
            ops_spec=prune_nulls(ops_dump),
            warnings=warnings,
            chart_context=chart_context,
        )

        elapsed_ms = (time.perf_counter() - started_at) * 1000
        logger.info(
            "[/canonicalize_opsspec] request completed | request_id=%s groups=%d warnings=%d elapsed_ms=%.1f",
            request_id,
            len(ops_dump),
            len(warnings),
            elapsed_ms,
        )
        trace_logger.info("[request:%s] canonicalize_out | elapsed_ms=%.1f", request_id, elapsed_ms)
        return prune_nulls(response.model_dump())
    except Exception as exc:
        elapsed_ms = (time.perf_counter() - started_at) * 1000
        logger.error(
            "[/canonicalize_opsspec] error | request_id=%s elapsed_ms=%.1f error=%s",
            request_id,
            elapsed_ms,
            exc,
        )
        report_path = _write_error_report(
            endpoint="/canonicalize_opsspec",
            request_id=request_id,
            elapsed_ms=elapsed_ms,
            error=exc,
            request_summary={
                "question_preview": q_preview,
                "explanation_preview": _safe_line(request.explanation, max_len=500),
                "data_rows_count": len(request.data_rows),
                "ops_groups_count": len(request.ops_spec or {}),
            },
        )
        if report_path is not None:
            logger.error(
                "[/canonicalize_opsspec] error report saved | request_id=%s path=%s",
                request_id,
                report_path,
            )
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/generate_grammar")
async def generate_grammar(request: GenerateGrammarRequest):
    pipeline: OpsSpecPipeline = getattr(app.state, "grammar_pipeline", None)
    if pipeline is None:
        raise HTTPException(status_code=500, detail="Grammar pipeline is not initialized.")

    request_id = uuid.uuid4().hex[:12]
    started_at = time.perf_counter()
    q_preview = " ".join(request.question.split())[:120]
    logger.info('[/generate_grammar] request received | request_id=%s question="%s"', request_id, q_preview)

    trace_logger.info(
        "[request:%s] grammar_endpoint_in | rows=%d debug=%s",
        request_id,
        len(request.data_rows),
        bool(request.debug),
    )

    try:
        chart_id = _chart_id_from_vega_spec(request.vega_lite_spec)
        model_name = pipeline.model_name_for_request(request.llm_backend, request.openai_model)
        cached_spec = _read_cached_grammar_spec(
            chart_id=chart_id,
            model=model_name,
            question=request.question,
            explanation=request.explanation,
            vega_lite_spec=request.vega_lite_spec,
        )
        if cached_spec is not None:
            cached_groups, cached_chart_context, cache_warnings = _parse_cached_ops_spec(
                spec=cached_spec,
                vega_lite_spec=request.vega_lite_spec,
                data_rows=request.data_rows,
            )
            elapsed_ms = (time.perf_counter() - started_at) * 1000
            logger.info(
                "[/generate_grammar] cache hit | request_id=%s chart_id=%s model=%s groups=%d warnings=%d elapsed_ms=%.1f",
                request_id,
                chart_id,
                model_name,
                len(cached_groups),
                len(cache_warnings),
                elapsed_ms,
            )
            trace_logger.info("[request:%s] grammar_cache_hit | elapsed_ms=%.1f", request_id, elapsed_ms)
            return _build_generate_grammar_response_payload(
                ops_spec=cached_groups,
                text_chunks=_grammar_cache_text_chunks(cached_spec),
            )

        result = pipeline.generate(
            question=request.question,
            explanation=request.explanation,
            vega_lite_spec=request.vega_lite_spec,
            data_rows=request.data_rows,
            request_id=request_id,
            debug=bool(request.debug),
            llm_backend=request.llm_backend,
            openai_model=request.openai_model,
        )
        elapsed_ms = (time.perf_counter() - started_at) * 1000
        logger.info(
            "[/generate_grammar] request completed | request_id=%s groups=%d warnings=%d elapsed_ms=%.1f",
            request_id,
            len(result.ops_spec),
            len(result.warnings),
            elapsed_ms,
        )
        trace_logger.info("[request:%s] grammar_endpoint_out | elapsed_ms=%.1f", request_id, elapsed_ms)
        # Return both logical ops groups and executable draw_plan for the web client.
        groups_dump = {
            group_name: [op.model_dump(by_alias=True, exclude_none=True) for op in ops]
            for group_name, ops in result.ops_spec.items()
        }
        response_payload = _build_generate_grammar_response_payload(
            ops_spec=result.ops_spec,
            text_chunks=result.text_chunks,
        )
        _append_grammar_result(
            chart_id=chart_id,
            model=model_name,
            question=request.question,
            explanation=request.explanation,
            vega_lite_spec=request.vega_lite_spec,
            spec={**groups_dump, "text_chunks": result.text_chunks},
        )
        return response_payload
    except RuntimeError as exc:
        elapsed_ms = (time.perf_counter() - started_at) * 1000
        logger.error(
            "[/generate_grammar] runtime error | request_id=%s elapsed_ms=%.1f error=%s",
            request_id,
            elapsed_ms,
            exc,
        )
        report_path = _write_error_report(
            endpoint="/generate_grammar",
            request_id=request_id,
            elapsed_ms=elapsed_ms,
            error=exc,
            request_summary={
                "question_preview": q_preview,
                "explanation_preview": _safe_line(request.explanation, max_len=500),
                "data_rows_count": len(request.data_rows),
                "vega_mark": request.vega_lite_spec.get("mark"),
                "vega_encoding_fields": _extract_encoding_fields(request.vega_lite_spec),
                "debug": bool(request.debug),
            },
        )
        if report_path is not None:
            logger.error("[/generate_grammar] error report saved | request_id=%s path=%s", request_id, report_path)
        trace_logger.error("[request:%s] grammar_runtime_error | elapsed_ms=%.1f error=%s", request_id, elapsed_ms, exc)
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        elapsed_ms = (time.perf_counter() - started_at) * 1000
        logger.error(
            "[/generate_grammar] unhandled error | request_id=%s elapsed_ms=%.1f error=%s",
            request_id,
            elapsed_ms,
            exc,
        )
        report_path = _write_error_report(
            endpoint="/generate_grammar",
            request_id=request_id,
            elapsed_ms=elapsed_ms,
            error=exc,
            request_summary={
                "question_preview": q_preview,
                "explanation_preview": _safe_line(request.explanation, max_len=500),
                "data_rows_count": len(request.data_rows),
                "vega_mark": request.vega_lite_spec.get("mark"),
                "vega_encoding_fields": _extract_encoding_fields(request.vega_lite_spec),
                "debug": bool(request.debug),
            },
        )
        if report_path is not None:
            logger.error("[/generate_grammar] error report saved | request_id=%s path=%s", request_id, report_path)
        trace_logger.error("[request:%s] grammar_unhandled_error | elapsed_ms=%.1f error=%s", request_id, elapsed_ms, exc)
        logger.exception("Failed to generate grammar.")
        raise HTTPException(status_code=500, detail=f"Failed to parse text: {exc}") from exc


@app.post("/compile_ops_plan", response_model=CompileOpsPlanResponse)
async def compile_ops_plan(request: CompileOpsPlanRequest):
    request_id = uuid.uuid4().hex[:12]
    started_at = time.perf_counter()
    logger.info(
        "[/compile_ops_plan] request received | request_id=%s groups=%d rows=%d",
        request_id,
        len(request.ops_spec or {}),
        len(request.data_rows),
    )

    try:
        chart_context, ctx_warnings, _ = build_chart_context(request.vega_lite_spec, request.data_rows)
        raw_groups = request.ops_spec or {}
        if not isinstance(raw_groups, dict):
            raise ValueError('ops_spec must be an object like {"ops":[...],"ops2":[...]}')

        groups, parse_warnings, parse_errors = validate_and_parse_ops_spec_groups(raw_groups, chart_context)
        groups.setdefault("ops", [])
        parse_errors.extend(validate_refs_against_node_ids(groups))
        if parse_errors:
            raise ValueError("Validation failed:\n- " + "\n- ".join(parse_errors))

        canonical_groups, canonical_warnings = canonicalize_ops_spec_groups(groups, chart_context=chart_context)
        scheduled_groups = schedule_ops_spec(canonical_groups)

        draw_plan_dump = validate_draw_groups_payload(
            build_draw_ops_spec(
                ops_spec=scheduled_groups,
                chart_context=chart_context,
                data_rows=request.data_rows,
                vega_lite_spec=request.vega_lite_spec,
            )
        )
        execution_plan_dump = build_sentence_execution_plan(
            ops_spec=scheduled_groups,
            draw_plan_groups=draw_plan_dump,
        )
        visual_execution_plan_dump = build_visual_execution_plan(ops_spec=scheduled_groups)
        ops_dump = {
            group_name: [op.model_dump(by_alias=True, exclude_none=True) for op in ops]
            for group_name, ops in scheduled_groups.items()
        }
        warnings = list(ctx_warnings) + list(parse_warnings) + list(canonical_warnings)

        elapsed_ms = (time.perf_counter() - started_at) * 1000
        logger.info(
            "[/compile_ops_plan] request completed | request_id=%s groups=%d draw_groups=%d steps=%d warnings=%d elapsed_ms=%.1f",
            request_id,
            len(ops_dump),
            len(draw_plan_dump),
            len(execution_plan_dump.get("steps") or []),
            len(warnings),
            elapsed_ms,
        )

        payload = CompileOpsPlanResponse(
            ops_spec=ops_dump,
            draw_plan=draw_plan_dump,
            execution_plan=execution_plan_dump,
            visual_execution_plan=visual_execution_plan_dump,
            warnings=warnings,
        )
        return prune_nulls(payload.model_dump())
    except Exception as exc:
        elapsed_ms = (time.perf_counter() - started_at) * 1000
        logger.error(
            "[/compile_ops_plan] error | request_id=%s elapsed_ms=%.1f error=%s",
            request_id,
            elapsed_ms,
            exc,
        )
        report_path = _write_error_report(
            endpoint="/compile_ops_plan",
            request_id=request_id,
            elapsed_ms=elapsed_ms,
            error=exc,
            request_summary={
                "ops_groups_count": len(request.ops_spec or {}),
                "data_rows_count": len(request.data_rows),
                "vega_mark": request.vega_lite_spec.get("mark"),
                "vega_encoding_fields": _extract_encoding_fields(request.vega_lite_spec),
            },
        )
        if report_path is not None:
            logger.error("[/compile_ops_plan] error report saved | request_id=%s path=%s", request_id, report_path)
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/answer_question", response_model=GenerateAnswerResponse)
async def answer_question(request: GenerateAnswerRequest):
    pipeline: ChartAnswerPipeline = getattr(app.state, "answer_pipeline", None)
    if pipeline is None:
        raise HTTPException(status_code=500, detail="Answer pipeline is not initialized.")

    request_id = uuid.uuid4().hex[:12]
    started_at = time.perf_counter()
    q_preview = " ".join(request.question.split())[:120]
    logger.info('[/answer_question] request received | request_id=%s question="%s"', request_id, q_preview)

    trace_logger.info(
        "[request:%s] answer_endpoint_in | spec_path=%s csv_path=%s debug=%s",
        request_id,
        request.vega_lite_spec_path,
        request.data_csv_path,
        bool(request.debug),
    )

    try:
        payload = pipeline.answer_from_paths(
            question=request.question,
            vega_lite_spec_path=request.vega_lite_spec_path,
            data_csv_path=request.data_csv_path,
            llm_choice=request.llm,
            request_id=request_id,
            debug=bool(request.debug),
        )
        elapsed_ms = (time.perf_counter() - started_at) * 1000
        logger.info(
            "[/answer_question] request completed | request_id=%s warnings=%d elapsed_ms=%.1f",
            request_id,
            len(payload.get("warnings") or []),
            elapsed_ms,
        )
        trace_logger.info("[request:%s] answer_endpoint_out | elapsed_ms=%.1f", request_id, elapsed_ms)

        return {
            "plan": payload.get("plan") or [],
            "answer": payload.get("answer") or "",
            "explanation": payload.get("explanation") or "",
            "warnings": payload.get("warnings") or [],
            "request_id": request_id,
        }
    except RuntimeError as exc:
        elapsed_ms = (time.perf_counter() - started_at) * 1000
        logger.error(
            "[/answer_question] runtime error | request_id=%s elapsed_ms=%.1f error=%s",
            request_id,
            elapsed_ms,
            exc,
        )
        report_path = _write_error_report(
            endpoint="/answer_question",
            request_id=request_id,
            elapsed_ms=elapsed_ms,
            error=exc,
            request_summary={
                "question_preview": q_preview,
                "vega_lite_spec_path": request.vega_lite_spec_path,
                "data_csv_path": request.data_csv_path,
                "llm": request.llm,
                "debug": bool(request.debug),
            },
        )
        if report_path is not None:
            logger.error("[/answer_question] error report saved | request_id=%s path=%s", request_id, report_path)
        trace_logger.error("[request:%s] answer_runtime_error | elapsed_ms=%.1f error=%s", request_id, elapsed_ms, exc)
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        elapsed_ms = (time.perf_counter() - started_at) * 1000
        logger.error(
            "[/answer_question] unhandled error | request_id=%s elapsed_ms=%.1f error=%s",
            request_id,
            elapsed_ms,
            exc,
        )
        report_path = _write_error_report(
            endpoint="/answer_question",
            request_id=request_id,
            elapsed_ms=elapsed_ms,
            error=exc,
            request_summary={
                "question_preview": q_preview,
                "vega_lite_spec_path": request.vega_lite_spec_path,
                "data_csv_path": request.data_csv_path,
                "llm": request.llm,
                "debug": bool(request.debug),
            },
        )
        if report_path is not None:
            logger.error("[/answer_question] error report saved | request_id=%s path=%s", request_id, report_path)
        trace_logger.error("[request:%s] answer_unhandled_error | elapsed_ms=%.1f error=%s", request_id, elapsed_ms, exc)
        raise HTTPException(status_code=500, detail=f"Failed to answer question: {exc}") from exc


@app.post("/run_module_trace", response_model=RunModuleTraceResponse)
async def run_module_trace(request: RunModuleTraceRequest):
    pipeline: OpsSpecPipeline = getattr(app.state, "grammar_pipeline", None)
    if pipeline is None:
        raise HTTPException(status_code=500, detail="Grammar pipeline is not initialized.")

    try:
        root = _project_root().resolve()
        spec_path = _resolve_path_under_root(request.vega_lite_spec_path, root=root)
        data_path = _resolve_path_under_root(request.data_csv_path, root=root)
        spec = _load_json_file(spec_path)
        _, rows = _load_csv_file(data_path)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    request_id = uuid.uuid4().hex[:12]
    result = pipeline.generate(
        question=request.question,
        explanation=request.explanation,
        vega_lite_spec=spec,
        data_rows=rows,
        request_id=request_id,
        debug=True,
    )

    trace = result.trace.model_dump(mode="json") if result.trace else {}
    inventory = trace.get("inventory", {}) if isinstance(trace, dict) else {}
    steps = trace.get("steps", []) if isinstance(trace, dict) else []
    ops_spec = {
        group: [op.model_dump(by_alias=True, exclude_none=True) for op in ops]
        for group, ops in result.ops_spec.items()
    }
    return {
        "inventory": inventory,
        "steps": steps,
        "ops_spec": ops_spec,
        "trace": trace,
        "chart_context": result.chart_context.model_dump(mode="json"),
    }


@app.post("/run_python_plan", response_model=RunPythonPlanResponse)
async def run_python_plan(request: RunPythonPlanRequest):
    pipeline: OpsSpecPipeline = getattr(app.state, "grammar_pipeline", None)
    if pipeline is None:
        raise HTTPException(status_code=500, detail="Grammar pipeline is not initialized.")

    request_id = uuid.uuid4().hex[:12]
    started_at = time.perf_counter()
    scenario_preview = _safe_line(request.scenario_path, max_len=180)
    logger.info('[/run_python_plan] request received | request_id=%s scenario="%s"', request_id, scenario_preview)

    trace_logger.info(
        "[request:%s] python_plan_endpoint_in | scenario_path=%s debug=%s",
        request_id,
        request.scenario_path,
        bool(request.debug),
    )

    try:
        scenario_request, normalized_path = load_python_scenario_request(request.scenario_path)
        debug_flag = bool(request.debug or scenario_request.debug)

        grammar_result = pipeline.generate(
            question=scenario_request.question,
            explanation=scenario_request.explanation,
            vega_lite_spec=scenario_request.vega_lite_spec,
            data_rows=scenario_request.data_rows,
            request_id=request_id,
            debug=debug_flag,
        )

        draw_plan = build_draw_ops_spec(
            ops_spec=grammar_result.ops_spec,
            chart_context=grammar_result.chart_context,
            data_rows=scenario_request.data_rows,
            vega_lite_spec=scenario_request.vega_lite_spec,
        )
        draw_plan_path = export_draw_plan_to_public(draw_plan, request_id=request_id)

        elapsed_ms = (time.perf_counter() - started_at) * 1000
        logger.info(
            "[/run_python_plan] request completed | request_id=%s scenario=%s groups=%d draw_groups=%d elapsed_ms=%.1f",
            request_id,
            normalized_path,
            len(grammar_result.ops_spec),
            len(draw_plan),
            elapsed_ms,
        )
        trace_logger.info(
            "[request:%s] python_plan_endpoint_out | elapsed_ms=%.1f draw_plan_path=%s",
            request_id,
            elapsed_ms,
            str(draw_plan_path),
        )
        response_payload = RunPythonPlanResponse(
            scenario_path=normalized_path,
            vega_lite_spec=scenario_request.vega_lite_spec,
            draw_plan=draw_plan,
            warnings=list(grammar_result.warnings),
        )
        return prune_nulls(response_payload.model_dump())
    except PythonScenarioLoadError as exc:
        elapsed_ms = (time.perf_counter() - started_at) * 1000
        logger.error(
            "[/run_python_plan] scenario load error | request_id=%s elapsed_ms=%.1f error=%s",
            request_id,
            elapsed_ms,
            exc,
        )
        report_path = _write_error_report(
            endpoint="/run_python_plan",
            request_id=request_id,
            elapsed_ms=elapsed_ms,
            error=exc,
            request_summary={
                "scenario_path": request.scenario_path,
                "debug": bool(request.debug),
                "failure_stage": "scenario_load",
            },
        )
        if report_path is not None:
            logger.error("[/run_python_plan] error report saved | request_id=%s path=%s", request_id, report_path)
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        elapsed_ms = (time.perf_counter() - started_at) * 1000
        logger.error(
            "[/run_python_plan] runtime error | request_id=%s elapsed_ms=%.1f error=%s",
            request_id,
            elapsed_ms,
            exc,
        )
        report_path = _write_error_report(
            endpoint="/run_python_plan",
            request_id=request_id,
            elapsed_ms=elapsed_ms,
            error=exc,
            request_summary={
                "scenario_path": request.scenario_path,
                "debug": bool(request.debug),
            },
        )
        if report_path is not None:
            logger.error("[/run_python_plan] error report saved | request_id=%s path=%s", request_id, report_path)
        trace_logger.error("[request:%s] python_plan_runtime_error | elapsed_ms=%.1f error=%s", request_id, elapsed_ms, exc)
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        elapsed_ms = (time.perf_counter() - started_at) * 1000
        logger.error(
            "[/run_python_plan] unhandled error | request_id=%s elapsed_ms=%.1f error=%s",
            request_id,
            elapsed_ms,
            exc,
        )
        report_path = _write_error_report(
            endpoint="/run_python_plan",
            request_id=request_id,
            elapsed_ms=elapsed_ms,
            error=exc,
            request_summary={
                "scenario_path": request.scenario_path,
                "debug": bool(request.debug),
            },
        )
        if report_path is not None:
            logger.error("[/run_python_plan] error report saved | request_id=%s path=%s", request_id, report_path)
        trace_logger.error("[request:%s] python_plan_unhandled_error | elapsed_ms=%.1f error=%s", request_id, elapsed_ms, exc)
        raise HTTPException(status_code=500, detail=f"Failed to run python plan: {exc}") from exc


def _get_baseline_llm(app_instance: FastAPI) -> StructuredLLMClient:
    """Get or create a shared LLM client for baseline endpoints."""
    llm = getattr(app_instance.state, "_baseline_llm", None)
    if llm is None:
        pipeline: OpsSpecPipeline = getattr(app_instance.state, "grammar_pipeline", None)
        if pipeline is None:
            raise HTTPException(status_code=500, detail="Grammar pipeline is not initialized.")
        llm = pipeline.llm
        app_instance.state._baseline_llm = llm
    return llm


def _load_baseline_prompt(name: str) -> str:
    path = Path(__file__).parent / "prompts" / name
    if not path.exists():
        raise HTTPException(status_code=500, detail=f"Prompt file not found: {name}")
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        raise HTTPException(status_code=500, detail=f"Prompt file is empty: {name}")
    return text


def _build_common_context(request: GenerateGrammarRequest):
    """Build chart context, roles summary, and other common variables used by all baselines."""
    chart_context, context_warnings, rows_preview = build_chart_context(
        request.vega_lite_spec, request.data_rows
    )
    roles_summary = {
        "primary_measure": chart_context.primary_measure,
        "primary_dimension": chart_context.primary_dimension,
        "series_field": chart_context.series_field,
    }
    series_domain: List[Any] = []
    if chart_context.series_field:
        series_domain = list(chart_context.categorical_values.get(chart_context.series_field, []))
    measure_fields = list(chart_context.measure_fields)
    explanation_sentences = split_explanation_sentences(request.explanation)
    return chart_context, context_warnings, rows_preview, roles_summary, series_domain, measure_fields, explanation_sentences


def _d3_annotation_debug_root() -> Path:
    return Path(__file__).resolve().parent / "opsspec" / "debug_d3_annotation"


def _create_d3_annotation_debug_dir() -> Path:
    base = _d3_annotation_debug_root()
    base.mkdir(parents=True, exist_ok=True)
    stem = datetime.now().strftime("%m%d%H%M")
    candidate = base / stem
    if not candidate.exists():
        candidate.mkdir(parents=True, exist_ok=False)
        return candidate
    suffix = 1
    while True:
        alt = base / f"{stem}_{suffix:02d}"
        if not alt.exists():
            alt.mkdir(parents=True, exist_ok=False)
            return alt
        suffix += 1


def _write_debug_json(path: Path, payload: Dict[str, Any]) -> None:
    path.write_text(json.dumps(prune_nulls(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _persist_d3_annotation_debug_bundle(
    *,
    debug_dir: Path,
    request: GenerateGrammarRequest,
    request_id: str,
    chart_context: Dict[str, Any] | None,
    context_warnings: List[str] | None,
    rows_preview: List[Dict[str, Any]] | None,
    base_chart: Dict[str, Any] | None,
    result_debug: Dict[str, Any] | None,
    final_result: Dict[str, Any] | None,
    error: Exception | None,
) -> None:
    _write_debug_json(
        debug_dir / "00_request.json",
        {
            "request_id": request_id,
            "question": request.question,
            "explanation": request.explanation,
            "vega_lite_spec": request.vega_lite_spec,
            "data_rows_count": len(request.data_rows),
            "debug": bool(request.debug),
        },
    )

    if chart_context is not None:
        _write_debug_json(
            debug_dir / "01_context.json",
            {
                "chart_context": chart_context,
                "context_warnings": context_warnings or [],
                "rows_preview": rows_preview or [],
            },
        )

    if base_chart is not None:
        _write_debug_json(
            debug_dir / "02_base_d3.json",
            {
                "chart_family": base_chart.get("chart_family"),
                "d3_code": base_chart.get("d3_code"),
            },
        )
        _write_debug_json(
            debug_dir / "03_converter_summary.json",
            base_chart.get("converter_summary") or {},
        )

    if result_debug is not None:
        steps = result_debug.get("steps") or []
        for step in steps:
            step_index = int(step.get("step") or 0)
            prompt_prefix = 4 + ((step_index - 1) * 2)
            _write_debug_json(
                debug_dir / f"{prompt_prefix:02d}_step_{step_index:02d}_prompt.json",
                {
                    "system_prompt": result_debug.get("system_prompt"),
                    "prompt_path": result_debug.get("prompt_path"),
                    "prompt_sha256": result_debug.get("prompt_sha256"),
                    "user_prompt": step.get("user_prompt"),
                    "validation_feedback": step.get("validation_feedback") or [],
                },
            )
            _write_debug_json(
                debug_dir / f"{prompt_prefix + 1:02d}_step_{step_index:02d}_response.json",
                {
                    "parsed": step.get("parsed") or {},
                },
            )

    if final_result is not None:
        _write_debug_json(
            debug_dir / "90_final_d3.json",
            {
                "base_chart": final_result.get("base_chart") or {},
                "step_specs": final_result.get("step_specs") or [],
                "warnings": final_result.get("warnings") or [],
            },
        )

    if error is not None:
        _write_debug_json(
            debug_dir / "99_error.json",
            {
                "error_type": type(error).__name__,
                "error": str(error),
            },
        )


@app.post("/generate_grammar_baseline")
async def generate_grammar_baseline(request: GenerateGrammarRequest):
    """Baseline (B2, plan-then-execute / LLMCompiler-style).

    한 번의 LLM 호출로 전체 OpsSpec DAG(op 노드 + 의존성 edge)를 계획한 뒤,
    제안 시스템과 *동일한* 결정론적 validator/scheduler/executor 로 실행한다.
    실행/검증 실패 시 strict-retry(전체 plan 재생성)로 교정한다.

    /generate_grammar(recursive)와의 차이:
    - recursive: op 하나하나를 별도 LLM 호출로 compose하며, step 사이에 실제 실행값을 다음 입력으로 전달.
    - baseline:  계획 단계에서 실행 중간값을 전혀 보지 않고 전체 DAG를 한 번에 생성 → 이후 결정론적 실행.
    planner에는 recursive와 동일한 op contract(allowed ops + 필드/의미 규칙)를 주입하므로,
    두 시스템의 차이는 "op 지식"이 아니라 "분해/grounding 전략"뿐이다.
    """
    llm = _get_baseline_llm(app)
    request_id = uuid.uuid4().hex[:12]
    started_at = time.perf_counter()
    q_preview = " ".join(request.question.split())[:120]
    logger.info('[/generate_grammar_baseline] request received | request_id=%s question="%s"', request_id, q_preview)

    try:
        prompt_template = _load_baseline_prompt("baseline_single_shot_opsspec.md")
        shared_rules_path = Path(__file__).parent / "prompts" / "opsspec_shared_rules.md"
        shared_rules = shared_rules_path.read_text(encoding="utf-8") if shared_rules_path.exists() else ""

        (
            chart_context, context_warnings, rows_preview,
            roles_summary, series_domain, measure_fields, explanation_sentences,
        ) = _build_common_context(request)

        # planner 에 주입하는 op 계약 — recursive pipeline과 동일 (baseline도 op을 똑같이 안다).
        ops_contract = build_ops_contract_for_prompt(chart_context=chart_context)
        budget = tune_few_shot_budget(
            question=request.question,
            explanation=request.explanation,
            chart_context=chart_context.model_dump(mode="json"),
        )
        few_shot = build_single_shot_few_shot_examples(
            question=request.question,
            explanation=request.explanation,
            chart_context=chart_context.model_dump(mode="json"),
            max_examples=budget.inventory_max_examples,
            max_chars=budget.inventory_max_chars,
        )

        max_retries = int(os.getenv("RECURSIVE_MAX_RETRIES", "3") or "3")
        validation_feedback: List[str] = []
        scheduled_groups: Dict[str, List[Any]] | None = None
        warnings: List[str] = list(context_warnings)

        for attempt in range(1, max_retries + 1):
            # ── Planner (LLM 1회): 전체 DAG 계획 ──────────────────────────────
            result = run_baseline_single_shot(
                llm=llm,
                prompt_template=prompt_template,
                prompt_path="prompts/baseline_single_shot_opsspec.md",
                shared_rules=shared_rules,
                shared_rules_path="prompts/opsspec_shared_rules.md",
                question=request.question,
                explanation=request.explanation,
                explanation_sentences=explanation_sentences,
                chart_context=chart_context.model_dump(mode="json"),
                roles_summary=roles_summary,
                series_domain=series_domain,
                measure_fields=measure_fields,
                rows_preview=rows_preview,
                ops_contract=ops_contract,
                validation_feedback=validation_feedback,
                few_shot_examples=few_shot.text,
                include_debug_prompts=bool(request.debug),
            )
            result.pop("_debug", None)
            llm_warnings = result.get("warnings") if isinstance(result.get("warnings"), list) else []

            # planner 출력에서 ops 그룹(ops, ops2, ...)만 추출.
            raw_groups = {
                key: value
                for key, value in result.items()
                if isinstance(key, str) and (key == "ops" or (key.startswith("ops") and key[3:].isdigit()))
            }
            # ── Stage 1: 결정론적 구조 복구 (LLM 없음) ──────────────────────────
            #    group↔sentenceIndex 불일치 등 cosmetic 오류를 검증 전에 미리 교정.
            #    스케줄러/실행기는 meta.inputs/nodeId만 보므로 실행 의미는 불변.
            raw_groups, repair_notes = autorepair_ops_groups(raw_groups)
            if repair_notes:
                warnings.extend(repair_notes)
            try:
                # ── Validate (schema + op contract + ref/node 교차검증) ──────
                groups, parse_warnings, errors = validate_and_parse_ops_spec_groups(raw_groups, chart_context)
                groups.setdefault("ops", [])
                errors.extend(validate_refs_against_node_ids(groups))
                if errors:
                    raise ValueError("Validation failed:\n- " + "\n- ".join(errors))
                # ── Task Fetching Unit + Executor (결정론): schedule 후 실제 실행으로 runnability 확인 ──
                #    executor가 nodeId 순으로 ref:nX placeholder를 해소하며 전체 DAG를 실행.
                scheduled = schedule_ops_spec(groups)
                OpsSpecExecutor(chart_context).execute(rows=request.data_rows, ops_spec=scheduled)
                scheduled_groups = scheduled
                warnings.extend(parse_warnings)
                warnings.extend(str(w) for w in llm_warnings)
                break
            except Exception as exc:
                # ── Stage 2: informed repair ─────────────────────────────────
                #    blind replan 대신, 다음 planner 콜에 자기 직전 spec + 정확한 에러 +
                #    "패치만" 지시를 주입한다(structured retry feedback 확장).
                validation_feedback = build_repair_feedback(
                    raw_groups, _build_retry_feedback(attempt, max_retries, exc)
                )
                logger.warning(
                    "[/generate_grammar_baseline] retry | request_id=%s attempt=%d/%d error=%s",
                    request_id, attempt, max_retries, exc,
                )
                if attempt == max_retries:
                    raise RuntimeError(
                        f"baseline plan-then-execute failed after {max_retries} attempts: {exc}"
                    ) from exc

        assert scheduled_groups is not None
        elapsed_ms = (time.perf_counter() - started_at) * 1000
        logger.info(
            "[/generate_grammar_baseline] completed | request_id=%s groups=%d warnings=%d elapsed_ms=%.1f",
            request_id, len(scheduled_groups), len(warnings), elapsed_ms,
        )
        # /generate_grammar와 동일한 응답 형태(ops group map). baseline은 inventory가 없어 text_chunks는 비움.
        payload = _build_generate_grammar_response_payload(ops_spec=scheduled_groups, text_chunks={})
        payload["warnings"] = warnings
        return payload

    except Exception as exc:
        elapsed_ms = (time.perf_counter() - started_at) * 1000
        logger.error(
            "[/generate_grammar_baseline] error | request_id=%s elapsed_ms=%.1f error=%s",
            request_id, elapsed_ms, exc,
        )
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/generate_visual_desc_baseline")
async def generate_visual_desc_baseline(request: GenerateGrammarRequest):
    """Baseline: Generate image generation prompts for visual chart explanation.

    Returns one image_prompt per explanation sentence via sequential LLM calls.
    Each prompt is self-contained and cumulative (includes all prior annotations).
    Response: { steps: [{sentenceIndex, sentence, image_prompt, visual_elements}], warnings }
    """
    llm = _get_baseline_llm(app)
    request_id = uuid.uuid4().hex[:12]
    started_at = time.perf_counter()
    q_preview = " ".join(request.question.split())[:120]
    logger.info('[/visual_desc_baseline] request received | request_id=%s question="%s"', request_id, q_preview)

    try:
        step_prompt_template = _load_baseline_prompt("baseline_text_to_image_step.md")

        (
            chart_context, context_warnings, rows_preview,
            roles_summary, series_domain, measure_fields, explanation_sentences,
        ) = _build_common_context(request)

        result = run_baseline_text_to_image(
            llm=llm,
            step_prompt_template=step_prompt_template,
            prompt_path="prompts/baseline_text_to_image_step.md",
            question=request.question,
            explanation=request.explanation,
            explanation_sentences=explanation_sentences,
            chart_context=chart_context.model_dump(mode="json"),
            roles_summary=roles_summary,
            vega_lite_spec=request.vega_lite_spec,
            rows_preview=rows_preview,
            include_debug_prompts=bool(request.debug),
        )

        elapsed_ms = (time.perf_counter() - started_at) * 1000
        logger.info(
            "[/visual_desc_baseline] completed | request_id=%s steps=%d elapsed_ms=%.1f",
            request_id, len(result.get("steps", [])), elapsed_ms,
        )

        result.pop("_debug", None)
        return prune_nulls(result)

    except Exception as exc:
        elapsed_ms = (time.perf_counter() - started_at) * 1000
        logger.error(
            "[/visual_desc_baseline] error | request_id=%s elapsed_ms=%.1f error=%s",
            request_id, elapsed_ms, exc,
        )
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/generate_vegalite_annotation_baseline")
async def generate_vegalite_annotation_baseline(request: GenerateGrammarRequest):
    """Baseline: Generate annotated Vega-Lite specifications (one per sentence).

    Returns N annotated specs via sequential LLM calls. Each spec is
    cumulative: it carries forward all annotations from previous steps.
    Response: { step_specs: [{sentenceIndex, sentence, annotated_spec, layers_added, computed_values}], warnings }
    """
    llm = _get_baseline_llm(app)
    request_id = uuid.uuid4().hex[:12]
    started_at = time.perf_counter()
    q_preview = " ".join(request.question.split())[:120]
    logger.info('[/vegalite_annotation_baseline] request received | request_id=%s question="%s"', request_id, q_preview)

    try:
        step_prompt_template = _load_baseline_prompt("baseline_vegalite_annotation_step.md")

        (
            chart_context, context_warnings, rows_preview,
            roles_summary, series_domain, measure_fields, explanation_sentences,
        ) = _build_common_context(request)

        result = run_baseline_vegalite_annotation(
            llm=llm,
            step_prompt_template=step_prompt_template,
            prompt_path="prompts/baseline_vegalite_annotation_step.md",
            question=request.question,
            explanation=request.explanation,
            explanation_sentences=explanation_sentences,
            chart_context=chart_context.model_dump(mode="json"),
            roles_summary=roles_summary,
            series_domain=series_domain,
            measure_fields=measure_fields,
            vega_lite_spec=request.vega_lite_spec,
            rows_preview=rows_preview,
            include_debug_prompts=bool(request.debug),
        )

        elapsed_ms = (time.perf_counter() - started_at) * 1000
        logger.info(
            "[/vegalite_annotation_baseline] completed | request_id=%s steps=%d elapsed_ms=%.1f",
            request_id, len(result.get("step_specs", [])), elapsed_ms,
        )

        result.pop("_debug", None)
        return prune_nulls(result)

    except Exception as exc:
        elapsed_ms = (time.perf_counter() - started_at) * 1000
        logger.error(
            "[/vegalite_annotation_baseline] error | request_id=%s elapsed_ms=%.1f error=%s",
            request_id, elapsed_ms, exc,
        )
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/generate_d3_annotation_baseline", response_model=GenerateD3AnnotationBaselineResponse)
async def generate_d3_annotation_baseline(request: GenerateGrammarRequest):
    """Baseline: convert Vega-Lite to deterministic D3, then annotate the D3 code step by step."""
    llm = _get_baseline_llm(app)
    request_id = uuid.uuid4().hex[:12]
    started_at = time.perf_counter()
    q_preview = " ".join(request.question.split())[:120]
    logger.info('[/d3_annotation_baseline] request received | request_id=%s question="%s"', request_id, q_preview)

    debug_dir: Path | None = _create_d3_annotation_debug_dir() if request.debug else None
    chart_context_payload: Dict[str, Any] | None = None
    context_warnings: List[str] | None = None
    rows_preview: List[Dict[str, Any]] | None = None
    base_chart: Dict[str, Any] | None = None
    result_debug: Dict[str, Any] | None = None
    final_result: Dict[str, Any] | None = None

    try:
        step_prompt_template = _load_baseline_prompt("baseline_d3_annotation_step.md")

        (
            chart_context, context_warnings, rows_preview,
            _roles_summary, _series_domain, _measure_fields, explanation_sentences,
        ) = _build_common_context(request)
        chart_context_payload = chart_context.model_dump(mode="json")

        base_chart = convert_vegalite_to_d3(
            vega_lite_spec=request.vega_lite_spec,
            data_rows=request.data_rows,
            chart_context=chart_context,
        )

        result = run_baseline_d3_annotation(
            llm=llm,
            step_prompt_template=step_prompt_template,
            prompt_path="prompts/baseline_d3_annotation_step.md",
            question=request.question,
            explanation=request.explanation,
            explanation_sentences=explanation_sentences,
            chart_context=chart_context_payload,
            rows_preview=rows_preview,
            base_chart=base_chart,
            include_debug_prompts=bool(request.debug),
        )
        final_result = dict(result)
        result_debug = result.pop("_debug", None)

        if debug_dir is not None:
            _persist_d3_annotation_debug_bundle(
                debug_dir=debug_dir,
                request=request,
                request_id=request_id,
                chart_context=chart_context_payload,
                context_warnings=context_warnings,
                rows_preview=rows_preview,
                base_chart=base_chart,
                result_debug=result_debug,
                final_result=final_result,
                error=None,
            )

        elapsed_ms = (time.perf_counter() - started_at) * 1000
        logger.info(
            "[/d3_annotation_baseline] completed | request_id=%s steps=%d elapsed_ms=%.1f",
            request_id, len(result.get("step_specs", [])), elapsed_ms,
        )
        return prune_nulls(result)

    except Exception as exc:
        elapsed_ms = (time.perf_counter() - started_at) * 1000
        if isinstance(exc, D3AnnotationStepValidationError):
            result_debug = exc.debug_payload
            final_result = exc.partial_result
        if debug_dir is not None:
            _persist_d3_annotation_debug_bundle(
                debug_dir=debug_dir,
                request=request,
                request_id=request_id,
                chart_context=chart_context_payload,
                context_warnings=context_warnings,
                rows_preview=rows_preview,
                base_chart=base_chart,
                result_debug=result_debug,
                final_result=final_result,
                error=exc,
            )
        logger.error(
            "[/d3_annotation_baseline] error | request_id=%s elapsed_ms=%.1f error=%s",
            request_id, elapsed_ms, exc,
        )
        if isinstance(exc, D3AnnotationStepValidationError):
            raise HTTPException(status_code=500, detail=exc.to_detail()) from exc
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/annotate_chart_image", response_model=AnnotateChartImageResponse)
async def annotate_chart_image(request: AnnotateChartImageRequest):
    """Programmatically draw annotations on a chart image using PIL/Pillow.

    Accepts a base64-encoded PNG of a chart and a list of annotation steps
    (one per explanation sentence). Returns one annotated PNG per step
    (or only the final combined image if return_each_step=False).

    Each step's annotations are cumulative: step 2 shows step 1 + step 2 elements.

    Supported annotation types per step:
      reference_line  — dashed horizontal line at a y data value
      text_label      — text string near a data point
      band            — shaded horizontal region between two y values
      highlight_bar   — dim all bars except the specified categories
      circle          — emphasis circle around a data point

    chart_area must describe the plot area in pixel coordinates:
      x, y            — top-left corner of the plot area
      width, height   — dimensions of the plot area
      y_min, y_max    — data range of the y-axis
      x_categories    — ordered category labels for the x-axis (bar charts)
    """
    request_id = uuid.uuid4().hex[:12]
    started_at = time.perf_counter()
    logger.info(
        "[/annotate_chart_image] request received | request_id=%s steps=%d return_each=%s",
        request_id, len(request.steps), request.return_each_step,
    )

    try:
        steps_payload = [
            {
                "sentence": s.sentence,
                "annotations": [
                    a.model_dump(exclude_none=True) for a in s.annotations
                ],
            }
            for s in request.steps
        ]

        result = annotate_chart_steps(
            image_base64=request.image_base64,
            chart_area=request.chart_area.model_dump(),
            steps=steps_payload,
            return_each_step=request.return_each_step,
        )

        elapsed_ms = (time.perf_counter() - started_at) * 1000
        logger.info(
            "[/annotate_chart_image] completed | request_id=%s output_steps=%d warnings=%d elapsed_ms=%.1f",
            request_id,
            len(result.get("steps", [])),
            len(result.get("warnings", [])),
            elapsed_ms,
        )

        return {
            "steps": result.get("steps", []),
            "warnings": result.get("warnings", []),
        }

    except Exception as exc:
        elapsed_ms = (time.perf_counter() - started_at) * 1000
        logger.error(
            "[/annotate_chart_image] error | request_id=%s elapsed_ms=%.1f error=%s",
            request_id, elapsed_ms, exc,
        )
        raise HTTPException(status_code=500, detail=str(exc)) from exc


if __name__ == "__main__":
    try:
        import uvicorn  # type: ignore
    except Exception as exc:  # pragma: no cover
        raise RuntimeError(
            "uvicorn is required to run the server via `python main.py`. "
            "Install uvicorn or run via your existing server runner."
        ) from exc

    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)
