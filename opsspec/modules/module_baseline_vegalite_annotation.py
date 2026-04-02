"""Baseline: Vega-Lite Annotation module (sequential per-step).

Generates N annotated Vega-Lite specs — one per explanation sentence — via
sequential LLM calls. Each step receives the accumulated spec from the
previous step as context, so annotations build up correctly.

Used as a baseline for the Explanation Generator evaluation.
"""
from __future__ import annotations

import hashlib
import json
import logging
from string import Template
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from ..core.llm import StructuredLLMClient
from ..core.types import JsonValue

logger = logging.getLogger(__name__)


# ── Per-step LLM output schema ────────────────────────────────────────────────

class VegaLiteStepOutput(BaseModel):
    annotated_spec: Dict[str, Any] = Field(default_factory=dict)
    layers_added: List[str] = Field(default_factory=list)
    computed_values: Dict[str, Any] = Field(default_factory=dict)
    warnings: List[str] = Field(default_factory=list)


# ── Final API response schema ─────────────────────────────────────────────────

class VegaLiteStepSpec(BaseModel):
    sentenceIndex: int
    sentence: str
    annotated_spec: Dict[str, Any] = Field(default_factory=dict)
    layers_added: List[str] = Field(default_factory=list)
    computed_values: Dict[str, Any] = Field(default_factory=dict)


class VegaLiteAnnotationOutput(BaseModel):
    """Response: one annotated spec per sentence (cumulative)."""
    step_specs: List[VegaLiteStepSpec] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)


# ── Prompt rendering ──────────────────────────────────────────────────────────

def _render_step_prompt(
    *,
    step_template: str,
    question: str,
    explanation: str,
    current_sentence: str,
    sentence_index: int,
    total_sentences: int,
    accumulated_spec: Dict[str, Any],
    chart_context: Dict[str, JsonValue],
    roles_summary: Dict[str, JsonValue],
    series_domain: List[JsonValue],
    measure_fields: List[str],
    rows_preview: List[Dict[str, JsonValue]],
) -> str:
    prev_index = sentence_index - 1
    return Template(step_template).safe_substitute(
        question=question,
        explanation=explanation,
        current_sentence=current_sentence,
        sentence_index=sentence_index,
        total_sentences=total_sentences,
        prev_index=prev_index,
        accumulated_spec_json=json.dumps(accumulated_spec, ensure_ascii=True, indent=2),
        roles_summary_json=json.dumps(roles_summary, ensure_ascii=True, indent=2),
        series_domain_json=json.dumps(series_domain, ensure_ascii=True, indent=2),
        measure_fields_json=json.dumps(measure_fields, ensure_ascii=True, indent=2),
        chart_context_json=json.dumps(chart_context, ensure_ascii=True, indent=2),
        rows_preview_json=json.dumps(rows_preview, ensure_ascii=True, indent=2),
    )


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# ── Main entry point ──────────────────────────────────────────────────────────

def run_baseline_vegalite_annotation(
    *,
    llm: StructuredLLMClient,
    step_prompt_template: str,
    prompt_path: str,
    question: str,
    explanation: str,
    explanation_sentences: List[str],
    chart_context: Dict[str, JsonValue],
    roles_summary: Dict[str, JsonValue],
    series_domain: List[JsonValue],
    measure_fields: List[str],
    vega_lite_spec: Dict[str, Any],
    rows_preview: List[Dict[str, JsonValue]],
    include_debug_prompts: bool = False,
) -> Dict[str, Any]:
    """Run sequential Vega-Lite annotation: N LLM calls, one per sentence.

    Each call receives the accumulated spec from previous steps so that
    annotations build up correctly.

    Returns dict with:
      step_specs: list of {sentenceIndex, sentence, annotated_spec, layers_added, computed_values}
      warnings:   list of warning strings
    """
    system_prompt = (
        "You are a Vega-Lite annotation expert. "
        "Add annotation layers to the accumulated Vega-Lite specification "
        "for the current explanation step only. Return strict JSON only."
    )

    total = len(explanation_sentences)
    accumulated_spec: Dict[str, Any] = dict(vega_lite_spec)
    step_specs: List[Dict[str, Any]] = []
    all_warnings: List[str] = []
    debug_steps: List[Dict[str, Any]] = []

    for idx, sentence in enumerate(explanation_sentences, start=1):
        user_prompt = _render_step_prompt(
            step_template=step_prompt_template,
            question=question,
            explanation=explanation,
            current_sentence=sentence,
            sentence_index=idx,
            total_sentences=total,
            accumulated_spec=accumulated_spec,
            chart_context=chart_context,
            roles_summary=roles_summary,
            series_domain=series_domain,
            measure_fields=measure_fields,
            rows_preview=rows_preview,
        )

        logger.debug(
            "[vegalite_annotation] step %d/%d | sentence=%r",
            idx, total, sentence[:60],
        )

        parsed = llm.complete(
            response_model=VegaLiteStepOutput,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            task_name=f"baseline_vegalite_annotation_step{idx}",
        )

        new_spec = parsed.get("annotated_spec") or {}
        if new_spec:
            accumulated_spec = new_spec

        step_specs.append({
            "sentenceIndex": idx,
            "sentence": sentence,
            "annotated_spec": accumulated_spec,
            "layers_added": parsed.get("layers_added") or [],
            "computed_values": parsed.get("computed_values") or {},
        })

        step_warnings = parsed.get("warnings") or []
        all_warnings.extend(step_warnings)

        if include_debug_prompts:
            debug_steps.append({
                "step": idx,
                "user_prompt": user_prompt,
                "parsed": parsed,
            })

    result: Dict[str, Any] = {
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
