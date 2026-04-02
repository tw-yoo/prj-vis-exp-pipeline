"""Baseline: Text-to-Image Description module (sequential per-step).

Generates N image generation prompts — one per explanation sentence — via
sequential LLM calls. Each step receives the previous step's image_prompt
as context, so prompts accumulate visually (each is self-contained and
cumulative).

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

class TextToImageStepOutput(BaseModel):
    image_prompt: str = ""
    visual_elements: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)


# ── Final API response schema ─────────────────────────────────────────────────

class ImageStep(BaseModel):
    sentenceIndex: int
    sentence: str
    image_prompt: str
    visual_elements: List[str] = Field(default_factory=list)


class TextToImageOutput(BaseModel):
    """Response: one image_prompt per sentence (each self-contained & cumulative)."""
    steps: List[ImageStep] = Field(default_factory=list)
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
    previous_image_prompt: str,
    chart_context: Dict[str, JsonValue],
    roles_summary: Dict[str, JsonValue],
    vega_lite_spec: Dict[str, Any],
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
        previous_image_prompt=previous_image_prompt or "(none — this is the first step)",
        chart_context_json=json.dumps(chart_context, ensure_ascii=True, indent=2),
        roles_summary_json=json.dumps(roles_summary, ensure_ascii=True, indent=2),
        vega_lite_spec_json=json.dumps(vega_lite_spec, ensure_ascii=True, indent=2),
        rows_preview_json=json.dumps(rows_preview, ensure_ascii=True, indent=2),
    )


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# ── Main entry point ──────────────────────────────────────────────────────────

def run_baseline_text_to_image(
    *,
    llm: StructuredLLMClient,
    step_prompt_template: str,
    prompt_path: str,
    question: str,
    explanation: str,
    explanation_sentences: List[str],
    chart_context: Dict[str, JsonValue],
    roles_summary: Dict[str, JsonValue],
    vega_lite_spec: Dict[str, Any],
    rows_preview: List[Dict[str, JsonValue]],
    include_debug_prompts: bool = False,
) -> Dict[str, Any]:
    """Run sequential text-to-image generation: N LLM calls, one per sentence.

    Each call receives the previous step's image_prompt so that each new
    prompt is self-contained and cumulative (includes all prior annotations).

    Returns dict with:
      steps:    list of {sentenceIndex, sentence, image_prompt, visual_elements}
      warnings: list of warning strings
    """
    system_prompt = (
        "You are a visual explanation designer. "
        "Generate a self-contained image generation prompt for the current "
        "explanation step, carrying forward all prior visual annotations. "
        "Return strict JSON only."
    )

    total = len(explanation_sentences)
    previous_image_prompt: str = ""
    steps: List[Dict[str, Any]] = []
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
            previous_image_prompt=previous_image_prompt,
            chart_context=chart_context,
            roles_summary=roles_summary,
            vega_lite_spec=vega_lite_spec,
            rows_preview=rows_preview,
        )

        logger.debug(
            "[text_to_image] step %d/%d | sentence=%r",
            idx, total, sentence[:60],
        )

        parsed = llm.complete(
            response_model=TextToImageStepOutput,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            task_name=f"baseline_text_to_image_step{idx}",
        )

        image_prompt = parsed.get("image_prompt") or ""
        previous_image_prompt = image_prompt  # pass to next step as context

        steps.append({
            "sentenceIndex": idx,
            "sentence": sentence,
            "image_prompt": image_prompt,
            "visual_elements": parsed.get("visual_elements") or [],
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
        "steps": steps,
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
