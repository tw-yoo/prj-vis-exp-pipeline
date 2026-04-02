from __future__ import annotations

import asyncio
import unittest
from unittest.mock import patch

import main
from models import GenerateGrammarRequest


class D3AnnotationEndpointTest(unittest.TestCase):
    def test_endpoint_returns_expected_shape(self) -> None:
        request = GenerateGrammarRequest(
            question="Which year is highest?",
            explanation="Highlight the highest year.",
            vega_lite_spec={
                "mark": "bar",
                "encoding": {
                    "x": {"field": "year", "type": "nominal"},
                    "y": {"field": "value", "type": "quantitative"},
                },
            },
            data_rows=[{"year": "2019", "value": 10}, {"year": "2020", "value": 14}],
            debug=False,
        )

        def fake_run_baseline_d3_annotation(**kwargs):  # type: ignore[no-untyped-def]
            base_chart = kwargs["base_chart"]
            return {
                "base_chart": base_chart,
                "step_specs": [
                    {
                        "sentenceIndex": 1,
                        "sentence": "Highlight the highest year.",
                        "annotated_d3_code": base_chart["d3_code"],
                        "annotations_added": ["highest bar highlight"],
                        "computed_values": {"highest_value": 14},
                    }
                ],
                "warnings": [],
            }

        with patch.object(main, "_get_baseline_llm", return_value=object()):
            with patch.object(main, "run_baseline_d3_annotation", side_effect=fake_run_baseline_d3_annotation):
                response = asyncio.run(main.generate_d3_annotation_baseline(request))

        self.assertIn("base_chart", response)
        self.assertEqual(response["base_chart"]["chart_family"], "bar_simple")
        self.assertEqual(len(response["step_specs"]), 1)
        self.assertEqual(response["step_specs"][0]["computed_values"], {"highest_value": 14})

    def test_endpoint_returns_structured_failure_detail(self) -> None:
        request = GenerateGrammarRequest(
            question="Which year is highest?",
            explanation="Highlight the highest year.",
            vega_lite_spec={
                "mark": "bar",
                "encoding": {
                    "x": {"field": "year", "type": "nominal"},
                    "y": {"field": "value", "type": "quantitative"},
                },
            },
            data_rows=[{"year": "2019", "value": 10}, {"year": "2020", "value": 14}],
            debug=False,
        )

        error = main.D3AnnotationStepValidationError(
            step_index=1,
            sentence="Highlight the highest year.",
            validation_feedback=["Only minimal formatting changes are allowed outside the annotation block; keep all base chart statements unchanged."],
            last_parsed={
                "annotated_d3_code": "function renderAnnotatedChart(container, dataOverride) {}",
                "annotations_added": ["highest bar highlight"],
                "computed_values": {"highest_value": 14},
                "warnings": [],
            },
            partial_result={"base_chart": {"chart_family": "bar_simple", "d3_code": "x", "converter_summary": {}}, "step_specs": [], "warnings": []},
            debug_payload={"steps": []},
        )

        with patch.object(main, "_get_baseline_llm", return_value=object()):
            with patch.object(main, "run_baseline_d3_annotation", side_effect=error):
                with self.assertRaises(main.HTTPException) as ctx:
                    asyncio.run(main.generate_d3_annotation_baseline(request))

        detail = ctx.exception.detail
        self.assertEqual(detail["step_index"], 1)
        self.assertIn("last_response", detail)
        self.assertEqual(detail["last_response"]["computed_values"], {"highest_value": 14})


if __name__ == "__main__":
    unittest.main()
