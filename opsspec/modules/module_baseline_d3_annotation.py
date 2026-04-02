"""Baseline: D3 annotation module (sequential per-step).

The baseline first receives a deterministic D3 scaffold converted from Vega-Lite.
Then it asks the LLM to modify only the annotation marker region for each
explanation sentence, returning cumulative D3 code per step.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
from string import Template
from typing import Any, Dict, List, Tuple

from pydantic import BaseModel, Field

from ..core.llm import StructuredLLMClient
from ..core.types import JsonValue
from ..runtime.vegalite_to_d3 import ANNOTATION_END_MARKER, ANNOTATION_START_MARKER

_BANNED_PATTERNS: Tuple[str, ...] = ("eval(", "Function(", "document.", "window.")


class D3AnnotationStepOutput(BaseModel):
    annotated_d3_code: str = ""
    annotations_added: List[str] = Field(default_factory=list)
    computed_values: Dict[str, Any] = Field(default_factory=dict)
    warnings: List[str] = Field(default_factory=list)


class D3AnnotationStepValidationError(RuntimeError):
    def __init__(
        self,
        *,
        step_index: int,
        sentence: str,
        validation_feedback: List[str],
        last_parsed: Dict[str, Any] | None,
        partial_result: Dict[str, Any],
        debug_payload: Dict[str, Any] | None,
    ) -> None:
        message = f"D3 annotation step {step_index} failed validation: {validation_feedback[-1] if validation_feedback else 'unknown error'}"
        super().__init__(message)
        self.step_index = step_index
        self.sentence = sentence
        self.validation_feedback = list(validation_feedback)
        self.last_parsed = dict(last_parsed or {})
        self.partial_result = partial_result
        self.debug_payload = debug_payload

    def to_detail(self) -> Dict[str, Any]:
        return {
            "message": str(self),
            "step_index": self.step_index,
            "sentence": self.sentence,
            "validation_feedback": self.validation_feedback,
            "last_response": self.last_parsed,
            "partial_result": self.partial_result,
        }


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _render_step_prompt(
    *,
    step_template: str,
    question: str,
    explanation: str,
    current_sentence: str,
    sentence_index: int,
    total_sentences: int,
    base_d3_code: str,
    accumulated_d3_code: str,
    converter_summary: Dict[str, Any],
    chart_context: Dict[str, JsonValue],
    rows_preview: List[Dict[str, JsonValue]],
    validation_feedback: List[str],
) -> str:
    prev_index = sentence_index - 1
    feedback_block = "\n".join(f"- {item}" for item in validation_feedback) if validation_feedback else "(none)"
    return Template(step_template).safe_substitute(
        question=question,
        explanation=explanation,
        current_sentence=current_sentence,
        sentence_index=sentence_index,
        total_sentences=total_sentences,
        prev_index=prev_index,
        base_d3_code=base_d3_code,
        accumulated_d3_code=accumulated_d3_code,
        converter_summary_json=json.dumps(converter_summary, ensure_ascii=True, indent=2),
        chart_context_json=json.dumps(chart_context, ensure_ascii=True, indent=2),
        rows_preview_json=json.dumps(rows_preview, ensure_ascii=True, indent=2),
        validation_feedback=feedback_block,
        annotation_start_marker=ANNOTATION_START_MARKER,
        annotation_end_marker=ANNOTATION_END_MARKER,
    )


def _extract_annotation_segments(code: str) -> Tuple[str, str, str]:
    start_index = code.find(ANNOTATION_START_MARKER)
    end_index = code.find(ANNOTATION_END_MARKER)
    if start_index < 0 or end_index < 0 or end_index <= start_index:
        raise ValueError("Missing required annotation markers.")
    prefix = code[: start_index + len(ANNOTATION_START_MARKER)]
    middle = code[start_index + len(ANNOTATION_START_MARKER) : end_index]
    suffix = code[end_index:]
    return prefix, middle, suffix


def _normalize_outside_marker(text: str) -> str:
    return re.sub(r"\s+", "", text)


def validate_annotated_d3_code(*, previous_code: str, candidate_code: str) -> None:
    stripped = candidate_code.strip()
    if not stripped:
        raise ValueError("annotated_d3_code is empty.")
    if "function renderAnnotatedChart(container, dataOverride)" not in candidate_code:
        raise ValueError("The required renderAnnotatedChart(container, dataOverride) function is missing.")

    required_anchors = (
        "const data =",
        "const svg =",
        "const chartLayer =",
        "const annotationLayer =",
        "const xScale =",
        "const yScale =",
    )
    for anchor in required_anchors:
        if anchor not in candidate_code:
            raise ValueError(f"Missing required anchor: {anchor}")

    for banned in _BANNED_PATTERNS:
        if banned in candidate_code:
            raise ValueError(f"Disallowed JavaScript pattern found: {banned}")

    prev_prefix, _prev_middle, prev_suffix = _extract_annotation_segments(previous_code)
    cand_prefix, _cand_middle, cand_suffix = _extract_annotation_segments(candidate_code)
    if (
        _normalize_outside_marker(cand_prefix) != _normalize_outside_marker(prev_prefix)
        or _normalize_outside_marker(cand_suffix) != _normalize_outside_marker(prev_suffix)
    ):
        raise ValueError(
            "Only minimal formatting changes are allowed outside the annotation block; keep all base chart statements unchanged."
        )


def run_baseline_d3_annotation(
    *,
    llm: StructuredLLMClient,
    step_prompt_template: str,
    prompt_path: str,
    question: str,
    explanation: str,
    explanation_sentences: List[str],
    chart_context: Dict[str, JsonValue],
    rows_preview: List[Dict[str, JsonValue]],
    base_chart: Dict[str, Any],
    include_debug_prompts: bool = False,
) -> Dict[str, Any]:
    system_prompt = (
        "You are a D3 annotation expert. "
        "Return strict JSON only. Keep the deterministic base chart code unchanged "
        "outside the annotation marker block."
    )

    total = len(explanation_sentences)
    accumulated_d3_code = str(base_chart.get("d3_code") or "")
    converter_summary = dict(base_chart.get("converter_summary") or {})
    step_specs: List[Dict[str, Any]] = []
    all_warnings: List[str] = []
    debug_steps: List[Dict[str, Any]] = []
    max_retries = int(os.getenv("RECURSIVE_MAX_RETRIES", "3") or "3")

    for idx, sentence in enumerate(explanation_sentences, start=1):
        validation_feedback: List[str] = []
        parsed: Dict[str, Any] | None = None
        last_error: Exception | None = None
        final_prompt = ""

        for attempt in range(1, max_retries + 1):
            user_prompt = _render_step_prompt(
                step_template=step_prompt_template,
                question=question,
                explanation=explanation,
                current_sentence=sentence,
                sentence_index=idx,
                total_sentences=total,
                base_d3_code=str(base_chart.get("d3_code") or ""),
                accumulated_d3_code=accumulated_d3_code,
                converter_summary=converter_summary,
                chart_context=chart_context,
                rows_preview=rows_preview,
                validation_feedback=validation_feedback,
            )
            final_prompt = user_prompt

            try:
                parsed = llm.complete(
                    response_model=D3AnnotationStepOutput,
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    task_name=f"baseline_d3_annotation_step{idx}_attempt{attempt}",
                )
                candidate_code = str(parsed.get("annotated_d3_code") or "")
                validate_annotated_d3_code(previous_code=accumulated_d3_code, candidate_code=candidate_code)
                accumulated_d3_code = candidate_code
                last_error = None
                break
            except Exception as exc:
                last_error = exc
                validation_feedback.append(str(exc))

        if parsed is None or last_error is not None:
            failure_debug = {
                "step": idx,
                "user_prompt": final_prompt,
                "parsed": parsed or {},
                "validation_feedback": validation_feedback,
                "failed": True,
            }
            if include_debug_prompts:
                debug_steps.append(failure_debug)
            partial_result: Dict[str, Any] = {
                "base_chart": base_chart,
                "step_specs": step_specs,
                "warnings": all_warnings,
            }
            debug_payload = None
            if include_debug_prompts:
                debug_payload = {
                    "system_prompt": system_prompt,
                    "prompt_path": prompt_path,
                    "prompt_sha256": _sha256_text(step_prompt_template),
                    "steps": debug_steps,
                }
            raise D3AnnotationStepValidationError(
                step_index=idx,
                sentence=sentence,
                validation_feedback=validation_feedback,
                last_parsed=parsed,
                partial_result=partial_result,
                debug_payload=debug_payload,
            ) from last_error

        step_specs.append(
            {
                "sentenceIndex": idx,
                "sentence": sentence,
                "annotated_d3_code": accumulated_d3_code,
                "annotations_added": parsed.get("annotations_added") or [],
                "computed_values": parsed.get("computed_values") or {},
            }
        )
        all_warnings.extend(parsed.get("warnings") or [])

        if include_debug_prompts:
            debug_steps.append(
                {
                    "step": idx,
                    "user_prompt": final_prompt,
                    "parsed": parsed,
                    "validation_feedback": validation_feedback,
                }
            )

    result: Dict[str, Any] = {
        "base_chart": base_chart,
        "step_specs": step_specs,
        "warnings": all_warnings,
    }
    if include_debug_prompts:
        result["_debug"] = {
            "system_prompt": system_prompt,
            "prompt_path": prompt_path,
            "prompt_sha256": _sha256_text(step_prompt_template),
            "steps": debug_steps,
        }
    return result
