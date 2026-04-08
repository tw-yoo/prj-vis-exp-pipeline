from __future__ import annotations

import asyncio
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import main
from models import GenerateGrammarRequestBodyRequest
from opsspec.runtime.chartqa_loader import load_chartqa_case


class GenerateGrammarRequestBodyTest(unittest.TestCase):
    def test_chartqa_loader_reads_spec_and_rows(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            spec_dir = root / "ChartQA" / "data" / "vlSpec" / "bar" / "simple"
            csv_dir = root / "ChartQA" / "data" / "csv" / "bar" / "simple"
            spec_dir.mkdir(parents=True, exist_ok=True)
            csv_dir.mkdir(parents=True, exist_ok=True)

            chart_id = "case_123"
            (spec_dir / f"{chart_id}.json").write_text(
                '{"mark":"bar","encoding":{"x":{"field":"Year","type":"nominal"},"y":{"field":"Value","type":"quantitative"}}}',
                encoding="utf-8",
            )
            (csv_dir / f"{chart_id}.csv").write_text(
                "Year,Value\n2020,10\n2021,12\n",
                encoding="utf-8",
            )

            spec, rows = load_chartqa_case(chart_id, root=root)

        self.assertEqual(spec["mark"], "bar")
        self.assertEqual(rows, [{"Year": "2020", "Value": "10"}, {"Year": "2021", "Value": "12"}])

    def test_endpoint_returns_generate_grammar_payload(self) -> None:
        request = GenerateGrammarRequestBodyRequest(
            question="Which year is highest?",
            explanation="Find the highest bar.",
            chart_id="case_abc",
            debug=False,
        )

        fake_spec = {
            "mark": "bar",
            "encoding": {
                "x": {"field": "Year", "type": "nominal"},
                "y": {"field": "Value", "type": "quantitative"},
            },
        }
        fake_rows = [{"Year": "2020", "Value": "10"}, {"Year": "2021", "Value": "12"}]

        with patch.object(main, "load_chartqa_case", return_value=(fake_spec, fake_rows)):
            response = asyncio.run(main.generate_grammar_request_body(request))

        self.assertEqual(response.question, "Which year is highest?")
        self.assertEqual(response.explanation, "Find the highest bar.")
        self.assertEqual(response.vega_lite_spec, fake_spec)
        self.assertEqual(response.data_rows, fake_rows)
        self.assertFalse(response.debug)

    def test_endpoint_returns_404_for_missing_chart_id(self) -> None:
        request = GenerateGrammarRequestBodyRequest(
            question="Which year is highest?",
            explanation="Find the highest bar.",
            chart_id="missing_case",
        )

        with patch.object(main, "load_chartqa_case", side_effect=FileNotFoundError("missing")):
            with self.assertRaises(main.HTTPException) as ctx:
                asyncio.run(main.generate_grammar_request_body(request))

        self.assertEqual(ctx.exception.status_code, 404)
        self.assertEqual(ctx.exception.detail, "missing")


if __name__ == "__main__":
    unittest.main()
