from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from opsspec.runtime.context_builder import build_chart_context
from opsspec.runtime.vegalite_to_d3 import VegaLiteToD3Error, convert_vegalite_to_d3


def _assert_js_parses(testcase: unittest.TestCase, code: str) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "chart.mjs"
        path.write_text(code, encoding="utf-8")
        subprocess.run(["node", "--check", str(path)], check=True, capture_output=True, text=True)


class VegaLiteToD3Test(unittest.TestCase):
    def _convert(self, spec: dict, rows: list[dict]) -> dict:
        chart_context, _warnings, _preview = build_chart_context(spec, rows)
        return convert_vegalite_to_d3(vega_lite_spec=spec, data_rows=rows, chart_context=chart_context)

    def test_simple_bar_conversion_is_reproducible(self) -> None:
        spec = {
            "mark": "bar",
            "width": 420,
            "height": 280,
            "encoding": {
                "x": {"field": "year", "type": "nominal", "title": "Year"},
                "y": {"field": "value", "type": "quantitative", "title": "Value"},
            },
        }
        rows = [{"year": "2019", "value": 10}, {"year": "2020", "value": 14}]
        first = self._convert(spec, rows)
        second = self._convert(spec, rows)

        self.assertEqual(first["chart_family"], "bar_simple")
        self.assertEqual(first["d3_code"], second["d3_code"])
        self.assertIn("function renderAnnotatedChart(container, dataOverride)", first["d3_code"])
        self.assertIn("const annotationLayer =", first["d3_code"])
        self.assertIn("// ANNOTATION_LAYER_START", first["d3_code"])
        _assert_js_parses(self, first["d3_code"])

    def test_grouped_bar_conversion(self) -> None:
        spec = {
            "mark": "bar",
            "encoding": {
                "x": {"field": "year", "type": "nominal"},
                "xOffset": {"field": "series", "type": "nominal"},
                "y": {"field": "value", "type": "quantitative"},
                "color": {"field": "series", "type": "nominal"},
            },
        }
        rows = [
            {"year": "2019", "series": "A", "value": 10},
            {"year": "2019", "series": "B", "value": 12},
        ]
        result = self._convert(spec, rows)
        self.assertEqual(result["chart_family"], "bar_grouped")
        self.assertIn("const innerScale =", result["d3_code"])
        self.assertIn("const colorScale =", result["d3_code"])
        _assert_js_parses(self, result["d3_code"])

    def test_stacked_bar_conversion(self) -> None:
        spec = {
            "mark": "bar",
            "encoding": {
                "x": {"field": "year", "type": "nominal"},
                "y": {"field": "value", "type": "quantitative"},
                "color": {"field": "series", "type": "nominal"},
            },
        }
        rows = [
            {"year": "2019", "series": "A", "value": 10},
            {"year": "2019", "series": "B", "value": 12},
        ]
        result = self._convert(spec, rows)
        self.assertEqual(result["chart_family"], "bar_stacked")
        self.assertIn("const stackedSeries =", result["d3_code"])
        _assert_js_parses(self, result["d3_code"])

    def test_line_simple_and_multi_conversion(self) -> None:
        simple_spec = {
            "mark": {"type": "line", "stroke": "#2563eb"},
            "encoding": {
                "x": {"field": "year", "type": "quantitative"},
                "y": {"field": "value", "type": "quantitative"},
            },
        }
        simple_rows = [{"year": 2019, "value": 10}, {"year": 2020, "value": 16}]
        simple_result = self._convert(simple_spec, simple_rows)
        self.assertEqual(simple_result["chart_family"], "line_simple")
        self.assertIn("const lineGenerator =", simple_result["d3_code"])
        _assert_js_parses(self, simple_result["d3_code"])

        multi_spec = {
            "mark": "line",
            "encoding": {
                "x": {"field": "date", "type": "temporal"},
                "y": {"field": "value", "type": "quantitative"},
                "color": {"field": "series", "type": "nominal"},
            },
        }
        multi_rows = [
            {"date": "2020-01-01", "series": "A", "value": 10},
            {"date": "2020-01-01", "series": "B", "value": 14},
        ]
        multi_result = self._convert(multi_spec, multi_rows)
        self.assertEqual(multi_result["chart_family"], "line_multi")
        self.assertIn("const groupedRows = d3.group", multi_result["d3_code"])
        _assert_js_parses(self, multi_result["d3_code"])

    def test_unsupported_spec_fails_fast(self) -> None:
        spec = {
            "mark": "bar",
            "facet": {"field": "group", "type": "nominal"},
            "encoding": {
                "x": {"field": "year", "type": "nominal"},
                "y": {"field": "value", "type": "quantitative"},
            },
        }
        rows = [{"year": "2019", "value": 10, "group": "G1"}]
        with self.assertRaises(VegaLiteToD3Error):
            self._convert(spec, rows)


if __name__ == "__main__":
    unittest.main()
