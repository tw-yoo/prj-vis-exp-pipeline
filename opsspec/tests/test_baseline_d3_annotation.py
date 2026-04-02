from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from opsspec.modules.module_baseline_d3_annotation import D3AnnotationStepValidationError, run_baseline_d3_annotation
from opsspec.runtime.context_builder import build_chart_context
from opsspec.runtime.vegalite_to_d3 import convert_vegalite_to_d3


def _assert_js_parses(testcase: unittest.TestCase, code: str) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "annotated.mjs"
        path.write_text(code, encoding="utf-8")
        subprocess.run(["node", "--check", str(path)], check=True, capture_output=True, text=True)


def _insert_annotation(code: str, js_line: str) -> str:
    marker = "// ANNOTATION_LAYER_START"
    replacement = marker + "\n  " + js_line
    return code.replace(marker, replacement, 1)


class _FakeLLM:
    def __init__(self, responses: list[dict]) -> None:
        self.responses = responses
        self.calls = 0

    def complete(self, *, response_model, system_prompt, user_prompt, task_name):  # type: ignore[no-untyped-def]
        _ = (response_model, system_prompt, user_prompt, task_name)
        response = self.responses[self.calls]
        self.calls += 1
        return response


class BaselineD3AnnotationTest(unittest.TestCase):
    def test_validator_allows_whitespace_only_changes_outside_marker(self) -> None:
        spec = {
            "mark": "bar",
            "encoding": {
                "x": {"field": "year", "type": "nominal"},
                "y": {"field": "value", "type": "quantitative"},
            },
        }
        rows = [{"year": "2019", "value": 10}, {"year": "2020", "value": 14}]
        chart_context, _warnings, rows_preview = build_chart_context(spec, rows)
        base_chart = convert_vegalite_to_d3(vega_lite_spec=spec, data_rows=rows, chart_context=chart_context)

        reformatted = base_chart["d3_code"].replace("const width = config.width;", "const width = config.width;\n")
        reformatted = _insert_annotation(
            reformatted,
            "annotationLayer.append('line').attr('x1', 0).attr('x2', 100).attr('y1', yScale(12)).attr('y2', yScale(12)).attr('stroke', '#e45756');",
        )
        llm = _FakeLLM(
            [
                {
                    "annotated_d3_code": reformatted,
                    "annotations_added": ["average reference line"],
                    "computed_values": {"average": 12},
                    "warnings": [],
                }
            ]
        )

        result = run_baseline_d3_annotation(
            llm=llm,  # type: ignore[arg-type]
            step_prompt_template="Current code:\n$accumulated_d3_code\n",
            prompt_path="prompts/baseline_d3_annotation_step.md",
            question="How many years are above average?",
            explanation="Find the average.",
            explanation_sentences=["Find the average."],
            chart_context=chart_context.model_dump(mode="json"),
            rows_preview=rows_preview,
            base_chart=base_chart,
            include_debug_prompts=False,
        )

        self.assertEqual(len(result["step_specs"]), 1)
        self.assertEqual(result["step_specs"][0]["computed_values"], {"average": 12})

    def test_sequential_annotation_retries_and_accumulates(self) -> None:
        spec = {
            "mark": "bar",
            "encoding": {
                "x": {"field": "year", "type": "nominal"},
                "y": {"field": "value", "type": "quantitative"},
            },
        }
        rows = [{"year": "2019", "value": 10}, {"year": "2020", "value": 14}]
        chart_context, _warnings, rows_preview = build_chart_context(spec, rows)
        base_chart = convert_vegalite_to_d3(vega_lite_spec=spec, data_rows=rows, chart_context=chart_context)

        invalid_code = "function broken() {}"
        step1_code = _insert_annotation(
            base_chart["d3_code"],
            "annotationLayer.append('line').attr('x1', 0).attr('x2', 100).attr('y1', yScale(12)).attr('y2', yScale(12)).attr('stroke', '#e45756');",
        )
        step2_code = _insert_annotation(
            step1_code,
            "annotationLayer.append('text').attr('x', 8).attr('y', yScale(12) - 8).text('Average: 12');",
        )

        llm = _FakeLLM(
            [
                {
                    "annotated_d3_code": invalid_code,
                    "annotations_added": [],
                    "computed_values": {},
                    "warnings": [],
                },
                {
                    "annotated_d3_code": step1_code,
                    "annotations_added": ["average reference line"],
                    "computed_values": {"average": 12},
                    "warnings": [],
                },
                {
                    "annotated_d3_code": step2_code,
                    "annotations_added": ["average label"],
                    "computed_values": {"average": 12},
                    "warnings": ["label may overlap on very small charts"],
                },
            ]
        )

        result = run_baseline_d3_annotation(
            llm=llm,  # type: ignore[arg-type]
            step_prompt_template=(
                "Step $sentence_index/$total_sentences\n"
                "Current sentence: $current_sentence\n"
                "Current code:\n$accumulated_d3_code\n"
                "Feedback:\n$validation_feedback\n"
            ),
            prompt_path="prompts/baseline_d3_annotation_step.md",
            question="How many years are above average?",
            explanation="Find the average. Highlight the average.",
            explanation_sentences=["Find the average.", "Highlight the average."],
            chart_context=chart_context.model_dump(mode="json"),
            rows_preview=rows_preview,
            base_chart=base_chart,
            include_debug_prompts=True,
        )

        self.assertEqual(llm.calls, 3)
        self.assertEqual(len(result["step_specs"]), 2)
        self.assertEqual(result["step_specs"][0]["computed_values"], {"average": 12})
        self.assertEqual(result["step_specs"][1]["annotations_added"], ["average label"])
        self.assertEqual(result["warnings"], ["label may overlap on very small charts"])
        self.assertIn("annotationLayer.append('line')", result["step_specs"][1]["annotated_d3_code"])
        self.assertIn("annotationLayer.append('text')", result["step_specs"][1]["annotated_d3_code"])
        self.assertIn("_debug", result)
        _assert_js_parses(self, result["step_specs"][1]["annotated_d3_code"])

    def test_failure_exposes_last_response_and_partial_result(self) -> None:
        spec = {
            "mark": "bar",
            "encoding": {
                "x": {"field": "year", "type": "nominal"},
                "y": {"field": "value", "type": "quantitative"},
            },
        }
        rows = [{"year": "2019", "value": 10}, {"year": "2020", "value": 14}]
        chart_context, _warnings, rows_preview = build_chart_context(spec, rows)
        base_chart = convert_vegalite_to_d3(vega_lite_spec=spec, data_rows=rows, chart_context=chart_context)

        bad_code = base_chart["d3_code"].replace("const width = config.width;", "const width = 999;")
        llm = _FakeLLM(
            [
                {
                    "annotated_d3_code": bad_code,
                    "annotations_added": ["broken change"],
                    "computed_values": {"average": 12},
                    "warnings": [],
                }
            ]
        )

        with self.assertRaises(D3AnnotationStepValidationError) as ctx:
            run_baseline_d3_annotation(
                llm=llm,  # type: ignore[arg-type]
                step_prompt_template="Current code:\n$accumulated_d3_code\n",
                prompt_path="prompts/baseline_d3_annotation_step.md",
                question="How many years are above average?",
                explanation="Find the average.",
                explanation_sentences=["Find the average."],
                chart_context=chart_context.model_dump(mode="json"),
                rows_preview=rows_preview,
                base_chart=base_chart,
                include_debug_prompts=True,
            )

        detail = ctx.exception.to_detail()
        self.assertEqual(detail["step_index"], 1)
        self.assertIn("last_response", detail)
        self.assertEqual(detail["last_response"]["computed_values"], {"average": 12})
        self.assertEqual(detail["partial_result"]["step_specs"], [])
        self.assertIn("steps", ctx.exception.debug_payload or {})


if __name__ == "__main__":
    unittest.main()
