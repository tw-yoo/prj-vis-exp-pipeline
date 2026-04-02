"""Baseline: Single-Shot OpsSpec Generation module.

Generates the complete OpsSpec DAG in a single LLM call (no recursive decomposition).
Used as a baseline to compare against the recursive pipeline.
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


class _SingleShotRawOutput(BaseModel):
    """Flexible schema for single-shot output — ops/ops2/... are dynamic keys."""

    class Config:
        extra = "allow"


def render_single_shot_prompt(
    *,
    prompt_template: str,
    shared_rules: str,
    question: str,
    explanation: str,
    explanation_sentences: List[str],
    chart_context: Dict[str, JsonValue],
    roles_summary: Dict[str, JsonValue],
    series_domain: List[JsonValue],
    measure_fields: List[str],
    rows_preview: List[Dict[str, JsonValue]],
    ops_contract: Dict[str, Any],
    validation_feedback: List[str],
    few_shot_examples: str,
) -> str:
    return Template(prompt_template).safe_substitute(
        shared_rules=shared_rules,
        question=question,
        explanation=explanation,
        explanation_sentences_json=json.dumps(explanation_sentences, ensure_ascii=True, indent=2),
        roles_summary_json=json.dumps(roles_summary, ensure_ascii=True, indent=2),
        series_domain_json=json.dumps(series_domain, ensure_ascii=True, indent=2),
        measure_fields_json=json.dumps(measure_fields, ensure_ascii=True, indent=2),
        chart_context_json=json.dumps(chart_context, ensure_ascii=True, indent=2),
        rows_preview_json=json.dumps(rows_preview, ensure_ascii=True, indent=2),
        ops_contract_json=json.dumps(ops_contract, ensure_ascii=True, indent=2),
        validation_feedback_json=json.dumps(validation_feedback, ensure_ascii=True, indent=2),
        few_shot_examples=few_shot_examples,
    )


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def run_baseline_single_shot(
    *,
    llm: StructuredLLMClient,
    prompt_template: str,
    prompt_path: str,
    shared_rules: str,
    shared_rules_path: str,
    question: str,
    explanation: str,
    explanation_sentences: List[str],
    chart_context: Dict[str, JsonValue],
    roles_summary: Dict[str, JsonValue],
    series_domain: List[JsonValue],
    measure_fields: List[str],
    rows_preview: List[Dict[str, JsonValue]],
    ops_contract: Dict[str, Any],
    validation_feedback: Optional[List[str]] = None,
    few_shot_examples: str = "",
    include_debug_prompts: bool = False,
) -> Dict[str, Any]:
    """Run single-shot OpsSpec generation (one LLM call).

    Returns the raw parsed output dict (ops group map + warnings).
    """
    validation_feedback = validation_feedback or []
    user_prompt = render_single_shot_prompt(
        prompt_template=prompt_template,
        shared_rules=shared_rules,
        question=question,
        explanation=explanation,
        explanation_sentences=explanation_sentences,
        chart_context=chart_context,
        roles_summary=roles_summary,
        series_domain=series_domain,
        measure_fields=measure_fields,
        rows_preview=rows_preview,
        ops_contract=ops_contract,
        validation_feedback=validation_feedback,
        few_shot_examples=few_shot_examples,
    )
    system_prompt = (
        "You are a single-shot OpsSpec generator. "
        "Generate the complete OpsSpec DAG from the question, explanation, and chart context "
        "in one pass. Return strict JSON only."
    )
    parsed = llm.complete(
        response_model=_SingleShotRawOutput,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        task_name="baseline_single_shot_opsspec",
    )
    if include_debug_prompts:
        parsed["_debug"] = {
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "prompt_path": prompt_path,
            "prompt_sha256": _sha256_text(prompt_template),
            "shared_rules_path": shared_rules_path,
            "shared_rules_sha256": _sha256_text(shared_rules),
        }
    return parsed
