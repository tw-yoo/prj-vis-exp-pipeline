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
            llm_backend="ollama",
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
        self.assertEqual(response.llm_backend, "ollama")

    def test_grammar_result_cache_round_trips_spec_by_request_key(self) -> None:
        spec = {
            "ops": [{"op": "findExtremum", "field": "Value"}],
            "text_chunks": {"ops": "Find the highest bar."},
        }
        vega_lite_spec = {"mark": "bar", "encoding": {"x": {"field": "Year"}}}

        with TemporaryDirectory() as tmp:
            cache_path = Path(tmp) / "grammar_result.csv"
            with patch.object(main, "_grammar_result_csv_path", return_value=cache_path):
                main._append_grammar_result(
                    chart_id="case_abc",
                    model="deepseek-r1:32b",
                    question="Which year is highest?",
                    explanation="Find the highest bar.",
                    vega_lite_spec=vega_lite_spec,
                    spec=spec,
                )
                cached = main._read_cached_grammar_spec(
                    chart_id="case_abc",
                    model="deepseek-r1:32b",
                    question="Which year is highest?",
                    explanation="Find the highest bar.",
                    vega_lite_spec=vega_lite_spec,
                )
                miss = main._read_cached_grammar_spec(
                    chart_id="case_abc",
                    model="different-model",
                    question="Which year is highest?",
                    explanation="Find the highest bar.",
                    vega_lite_spec=vega_lite_spec,
                )
                spec_miss = main._read_cached_grammar_spec(
                    chart_id="case_abc",
                    model="deepseek-r1:32b",
                    question="Which year is highest?",
                    explanation="Find the highest bar.",
                    vega_lite_spec={"mark": "line", "encoding": {"x": {"field": "Year"}}},
                )

        self.assertEqual(cached, spec)
        self.assertIsNone(miss)
        self.assertIsNone(spec_miss)

    def test_cached_ops_spec_parsing_ignores_text_chunks(self) -> None:
        spec = {
            "ops": [
                {
                    "op": "findExtremum",
                    "id": "n1",
                    "meta": {"nodeId": "n1", "inputs": [], "sentenceIndex": 1},
                    "field": "Value",
                    "which": "max",
                }
            ],
            "text_chunks": {"ops": "Find the highest bar."},
        }
        vega_lite_spec = {
            "mark": "bar",
            "encoding": {
                "x": {"field": "Year", "type": "nominal"},
                "y": {"field": "Value", "type": "quantitative"},
            },
        }
        rows = [{"Year": "2020", "Value": 10}, {"Year": "2021", "Value": 12}]

        groups, _chart_context, _warnings = main._parse_cached_ops_spec(
            spec=spec,
            vega_lite_spec=vega_lite_spec,
            data_rows=rows,
        )

        self.assertEqual(list(groups.keys()), ["ops"])
        self.assertEqual(groups["ops"][0].op, "findExtremum")
        self.assertEqual(main._grammar_cache_text_chunks(spec), {"ops": "Find the highest bar."})

    def test_chart_id_from_vega_spec_uses_data_url_stem(self) -> None:
        chart_id = main._chart_id_from_vega_spec(
            {"data": {"url": "ChartQA/data/csv/bar/stacked/10t8o5vhethzeod1.csv"}}
        )

        self.assertEqual(chart_id, "10t8o5vhethzeod1")

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
