from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import patch

from opsspec.core.models import ChartContext
from opsspec.modules.pipeline import OpsSpecPipeline


class RecursivePipelineTest(unittest.TestCase):
    def setUp(self) -> None:
        self.prompts_dir = Path(__file__).resolve().parents[2] / "prompts"
        self.context = ChartContext(
            fields=["season", "category", "Revenue_Million_Euros"],
            dimension_fields=["season", "category"],
            measure_fields=["Revenue_Million_Euros"],
            primary_dimension="season",
            primary_measure="Revenue_Million_Euros",
            series_field="category",
            categorical_values={"category": ["Broadcasting", "Commercial"]},
        )
        self.rows = [
            {"season": "2016/17", "category": "Broadcasting", "Revenue_Million_Euros": 220.0},
            {"season": "2017/18", "category": "Broadcasting", "Revenue_Million_Euros": 190.0},
            {"season": "2016/17", "category": "Commercial", "Revenue_Million_Euros": 300.0},
            {"season": "2017/18", "category": "Commercial", "Revenue_Million_Euros": 260.0},
        ]
        self.rows_preview = self.rows[:2]

    def _pipeline(self) -> OpsSpecPipeline:
        return OpsSpecPipeline(
            ollama_model="test",
            ollama_base_url="http://localhost:11434/v1",
            ollama_api_key="test",
            prompts_dir=self.prompts_dir,
        )

    def test_recursive_chain_with_scalar_ref(self) -> None:
        inventory_payload = {
            "tasks": [
                {
                    "taskId": "o1",
                    "op": "average",
                    "sentenceIndex": 1,
                    "mention": "average revenue for Broadcasting",
                    "paramsHint": {"field": "@primary_measure", "group": "Broadcasting"},
                },
                {
                    "taskId": "o2",
                    "op": "filter",
                    "sentenceIndex": 2,
                    "mention": "revenue greater than that average (Broadcasting)",
                    "paramsHint": {"field": "@primary_measure", "operator": ">", "value": "ref:n1", "group": "Broadcasting"},
                },
                {
                    "taskId": "o3",
                    "op": "findExtremum",
                    "sentenceIndex": 2,
                    "mention": "pick the maximum season",
                    "paramsHint": {"which": "max", "field": "@primary_measure"},
                },
            ],
            "warnings": [],
        }
        step_payloads = [
            {"pickTaskId": "o1", "op_spec": {"op": "average", "field": "@primary_measure", "group": "Broadcasting"}, "inputs": []},
            {
                "pickTaskId": "o2",
                "op_spec": {
                    "op": "filter",
                    "field": "@primary_measure",
                    "operator": ">",
                    "value": "ref:n1",
                    "group": "Broadcasting",
                },
                "inputs": [],
            },
            {"pickTaskId": "o3", "op_spec": {"op": "findExtremum", "which": "max", "field": "@primary_measure"}, "inputs": ["n2"]},
        ]

        with (
            patch("opsspec.modules.pipeline.build_chart_context", return_value=(self.context, [], self.rows_preview)),
            patch("opsspec.modules.pipeline.run_inventory_module", return_value=inventory_payload),
            patch("opsspec.modules.pipeline.run_step_compose_module", side_effect=step_payloads),
            patch("opsspec.modules.pipeline.build_draw_ops_spec", return_value={}),
            patch("opsspec.modules.pipeline.export_draw_plan_to_public", return_value=Path("/tmp/draw_plan.json")),
            patch("opsspec.modules.pipeline._persist_debug_bundle", return_value=Path("/tmp/debug_bundle")),
        ):
            pipeline = self._pipeline()
            result = pipeline.generate(
                question="q",
                explanation="e",
                vega_lite_spec={},
                data_rows=self.rows,
                request_id="req",
                debug=False,
            )

        self.assertIn("ops", result.ops_spec)
        self.assertIn("ops2", result.ops_spec)
        self.assertEqual(len(result.ops_spec["ops"]), 1)
        self.assertEqual(len(result.ops_spec["ops2"]), 2)

        op1 = result.ops_spec["ops"][0]
        op2 = result.ops_spec["ops2"][0]
        op3 = result.ops_spec["ops2"][1]

        self.assertEqual(op1.meta.nodeId, "n1")
        self.assertEqual(op2.meta.nodeId, "n2")
        self.assertEqual(op3.meta.nodeId, "n3")

        self.assertEqual(op1.id, "n1")
        self.assertEqual(op2.id, "n2")
        self.assertEqual(op3.id, "n3")

        self.assertEqual(op1.meta.inputs, [])
        self.assertEqual(op2.meta.inputs, ["n1"])
        self.assertEqual(op3.meta.inputs, ["n2"])

        op2_dump = op2.model_dump(by_alias=True, exclude_none=True)
        self.assertEqual(op2_dump.get("value"), "ref:n1")
        self.assertNotIsInstance(op2_dump.get("value"), dict)

        self.assertEqual(op1.meta.sentenceIndex, 1)
        self.assertEqual(op2.meta.sentenceIndex, 2)
        self.assertEqual(op3.meta.sentenceIndex, 2)
        self.assertTrue(str(op1.meta.source).startswith("recursive_step=1;"))
        self.assertTrue(str(op2.meta.source).startswith("recursive_step=2;"))
        self.assertTrue(str(op3.meta.source).startswith("recursive_step=3;"))

    def test_find_extremum_with_rank_is_parsed_and_executed(self) -> None:
        inventory_payload = {
            "tasks": [
                {
                    "taskId": "o1",
                    "op": "findExtremum",
                    "sentenceIndex": 1,
                    "mention": "find second highest",
                    "paramsHint": {"which": "max", "rank": 2, "field": "@primary_measure"},
                }
            ],
            "warnings": [],
        }
        step_payloads = [
            {
                "pickTaskId": "o1",
                "op_spec": {"op": "findExtremum", "which": "max", "rank": 2, "field": "@primary_measure"},
                "inputs": [],
            }
        ]

        with (
            patch("opsspec.modules.pipeline.build_chart_context", return_value=(self.context, [], self.rows_preview)),
            patch("opsspec.modules.pipeline.run_inventory_module", return_value=inventory_payload),
            patch("opsspec.modules.pipeline.run_step_compose_module", side_effect=step_payloads),
            patch("opsspec.modules.pipeline.build_draw_ops_spec", return_value={}),
            patch("opsspec.modules.pipeline.export_draw_plan_to_public", return_value=Path("/tmp/draw_plan.json")),
            patch("opsspec.modules.pipeline._persist_debug_bundle", return_value=Path("/tmp/debug_bundle")),
        ):
            pipeline = self._pipeline()
            result = pipeline.generate(
                question="q",
                explanation="e",
                vega_lite_spec={},
                data_rows=self.rows,
                request_id="req",
                debug=False,
            )

        self.assertIn("ops", result.ops_spec)
        self.assertEqual(len(result.ops_spec["ops"]), 1)
        op = result.ops_spec["ops"][0]
        self.assertEqual(op.op, "findExtremum")
        self.assertEqual(op.rank, 2)

    def test_setop_requires_two_inputs(self) -> None:
        inventory_payload = {
            "tasks": [
                {
                    "taskId": "o1",
                    "op": "filter",
                    "sentenceIndex": 1,
                    "mention": "Broadcasting in 2016/17",
                    "paramsHint": {"field": "@primary_dimension", "include": ["2016/17"], "group": "Broadcasting"},
                },
                {
                    "taskId": "o2",
                    "op": "filter",
                    "sentenceIndex": 1,
                    "mention": "Commercial in 2016/17",
                    "paramsHint": {"field": "@primary_dimension", "include": ["2016/17"], "group": "Commercial"},
                },
                {
                    "taskId": "o3",
                    "op": "setOp",
                    "sentenceIndex": 2,
                    "mention": "intersection of those seasons",
                    "paramsHint": {"fn": "intersection"},
                },
            ],
            "warnings": [],
        }
        step_payloads = [
            {
                "pickTaskId": "o1",
                "op_spec": {"op": "filter", "field": "@primary_dimension", "include": ["2016/17"], "group": "Broadcasting"},
                "inputs": [],
            },
            {
                "pickTaskId": "o2",
                "op_spec": {"op": "filter", "field": "@primary_dimension", "include": ["2016/17"], "group": "Commercial"},
                "inputs": [],
            },
            {
                "pickTaskId": "o3",
                "op_spec": {"op": "setOp", "fn": "intersection"},
                "inputs": ["n1", "n2"],
            },
        ]

        with (
            patch("opsspec.modules.pipeline.build_chart_context", return_value=(self.context, [], self.rows_preview)),
            patch("opsspec.modules.pipeline.run_inventory_module", return_value=inventory_payload),
            patch("opsspec.modules.pipeline.run_step_compose_module", side_effect=step_payloads),
            patch("opsspec.modules.pipeline.build_draw_ops_spec", return_value={}),
            patch("opsspec.modules.pipeline.export_draw_plan_to_public", return_value=Path("/tmp/draw_plan.json")),
            patch("opsspec.modules.pipeline._persist_debug_bundle", return_value=Path("/tmp/debug_bundle")),
        ):
            pipeline = self._pipeline()
            result = pipeline.generate(
                question="q",
                explanation="e",
                vega_lite_spec={},
                data_rows=self.rows,
                request_id="req",
                debug=False,
            )

        self.assertIn("ops", result.ops_spec)
        self.assertIn("ops2", result.ops_spec)
        self.assertEqual(len(result.ops_spec["ops"]), 2)
        self.assertEqual(len(result.ops_spec["ops2"]), 1)

        set_op = result.ops_spec["ops2"][0]
        self.assertEqual(set_op.op, "setOp")
        self.assertEqual(set_op.meta.nodeId, "n3")
        self.assertEqual(set(set_op.meta.inputs or []), {"n1", "n2"})

    def test_step_compose_strict_retry(self) -> None:
        inventory_payload = {
            "tasks": [
                {
                    "taskId": "o1",
                    "op": "average",
                    "sentenceIndex": 1,
                    "mention": "average revenue",
                    "paramsHint": {"field": "@primary_measure"},
                }
            ],
            "warnings": [],
        }
        invalid = {"pickTaskId": "o1", "op_spec": {"op": "average", "id": "oops"}, "inputs": []}
        valid = {"pickTaskId": "o1", "op_spec": {"op": "average", "field": "@primary_measure"}, "inputs": []}

        with (
            patch("opsspec.modules.pipeline.build_chart_context", return_value=(self.context, [], self.rows_preview)),
            patch("opsspec.modules.pipeline.run_inventory_module", return_value=inventory_payload),
            patch("opsspec.modules.pipeline.run_step_compose_module", side_effect=[invalid, valid]) as step_compose,
            patch("opsspec.modules.pipeline.build_draw_ops_spec", return_value={}),
            patch("opsspec.modules.pipeline.export_draw_plan_to_public", return_value=Path("/tmp/draw_plan.json")),
            patch("opsspec.modules.pipeline._persist_debug_bundle", return_value=Path("/tmp/debug_bundle")),
        ):
            pipeline = self._pipeline()
            result = pipeline.generate(
                question="q",
                explanation="e",
                vega_lite_spec={},
                data_rows=self.rows,
                request_id="req",
                debug=False,
            )

        self.assertEqual(step_compose.call_count, 2)
        self.assertIn("ops", result.ops_spec)
        self.assertEqual(len(result.ops_spec["ops"]), 1)
        self.assertEqual(result.ops_spec["ops"][0].meta.nodeId, "n1")
        self.assertTrue(any("step 1 attempt 1" in w for w in result.warnings))

    def test_filter_group_list_is_grounded_and_executed(self) -> None:
        inventory_payload = {
            "tasks": [
                {
                    "taskId": "o1",
                    "op": "filter",
                    "sentenceIndex": 1,
                    "mention": "keep 2016/17 for broadcasting and commercial",
                    "paramsHint": {"field": "@primary_dimension", "include": ["2016/17"], "group": ["broadcasting", "commercial"]},
                }
            ],
            "warnings": [],
        }
        step_payloads = [
            {
                "pickTaskId": "o1",
                "op_spec": {"op": "filter", "field": "@primary_dimension", "include": ["2016/17"], "group": ["broadcasting", "commercial"]},
                "inputs": [],
            }
        ]

        with (
            patch("opsspec.modules.pipeline.build_chart_context", return_value=(self.context, [], self.rows_preview)),
            patch("opsspec.modules.pipeline.run_inventory_module", return_value=inventory_payload),
            patch("opsspec.modules.pipeline.run_step_compose_module", side_effect=step_payloads),
            patch("opsspec.modules.pipeline.build_draw_ops_spec", return_value={}),
            patch("opsspec.modules.pipeline.export_draw_plan_to_public", return_value=Path("/tmp/draw_plan.json")),
            patch("opsspec.modules.pipeline._persist_debug_bundle", return_value=Path("/tmp/debug_bundle")),
        ):
            pipeline = self._pipeline()
            result = pipeline.generate(
                question="q",
                explanation="e",
                vega_lite_spec={},
                data_rows=self.rows,
                request_id="req",
                debug=False,
            )

        self.assertIn("ops", result.ops_spec)
        self.assertEqual(len(result.ops_spec["ops"]), 1)
        op = result.ops_spec["ops"][0]
        self.assertEqual(op.group, ["Broadcasting", "Commercial"])

    def test_filter_between_is_parsed_and_executed(self) -> None:
        context = ChartContext(
            fields=["Year", "Population growth compared to previous year"],
            dimension_fields=["Year"],
            measure_fields=["Population growth compared to previous year"],
            primary_dimension="Year",
            primary_measure="Population growth compared to previous year",
            series_field=None,
            categorical_values={"Year": ["2009", "2010", "2011", "2012", "2013", "2014", "2015"]},
            field_types={"Year": "categorical", "Population growth compared to previous year": "numeric"},
            mark="bar",
            is_stacked=False,
        )
        rows = [
            {"Year": "2009", "Population growth compared to previous year": 2.76},
            {"Year": "2010", "Population growth compared to previous year": 2.76},
            {"Year": "2011", "Population growth compared to previous year": 2.76},
            {"Year": "2012", "Population growth compared to previous year": 2.76},
            {"Year": "2013", "Population growth compared to previous year": 2.76},
            {"Year": "2014", "Population growth compared to previous year": 2.75},
            {"Year": "2015", "Population growth compared to previous year": 2.73},
        ]
        inventory_payload = {
            "tasks": [
                {
                    "taskId": "o1",
                    "op": "filter",
                    "sentenceIndex": 1,
                    "mention": "from 2009 to 2014",
                    "paramsHint": {"field": "Year", "operator": "between", "value": ["2009", "2014"]},
                }
            ],
            "warnings": [],
        }
        step_payloads = [
            {
                "pickTaskId": "o1",
                "op_spec": {"op": "filter", "field": "Year", "operator": "between", "value": ["2009", "2014"]},
                "inputs": [],
            }
        ]

        with (
            patch("opsspec.modules.pipeline.build_chart_context", return_value=(context, [], rows[:2])),
            patch("opsspec.modules.pipeline.run_inventory_module", return_value=inventory_payload),
            patch("opsspec.modules.pipeline.run_step_compose_module", side_effect=step_payloads),
            patch("opsspec.modules.pipeline.build_draw_ops_spec", return_value={}),
            patch("opsspec.modules.pipeline.export_draw_plan_to_public", return_value=Path("/tmp/draw_plan.json")),
            patch("opsspec.modules.pipeline._persist_debug_bundle", return_value=Path("/tmp/debug_bundle")),
        ):
            pipeline = self._pipeline()
            result = pipeline.generate(
                question="q",
                explanation="e",
                vega_lite_spec={},
                data_rows=rows,
                request_id="req",
                debug=False,
            )

        self.assertIn("ops", result.ops_spec)
        self.assertEqual(len(result.ops_spec["ops"]), 1)
        op = result.ops_spec["ops"][0]
        self.assertEqual(op.op, "filter")
        self.assertEqual(op.operator, "between")

    def test_add_step_is_parsed_and_emitted(self) -> None:
        inventory_payload = {
            "tasks": [
                {
                    "taskId": "o1",
                    "op": "average",
                    "sentenceIndex": 1,
                    "mention": "average for broadcasting",
                    "paramsHint": {"field": "@primary_measure", "group": "Broadcasting"},
                },
                {
                    "taskId": "o2",
                    "op": "average",
                    "sentenceIndex": 1,
                    "mention": "average for commercial",
                    "paramsHint": {"field": "@primary_measure", "group": "Commercial"},
                },
                {
                    "taskId": "o3",
                    "op": "add",
                    "sentenceIndex": 2,
                    "mention": "add those two averages",
                    "paramsHint": {"targetA": "ref:n1", "targetB": "ref:n2"},
                },
            ],
            "warnings": [],
        }
        step_payloads = [
            {"pickTaskId": "o1", "op_spec": {"op": "average", "field": "@primary_measure", "group": "Broadcasting"}, "inputs": []},
            {"pickTaskId": "o2", "op_spec": {"op": "average", "field": "@primary_measure", "group": "Commercial"}, "inputs": []},
            {"pickTaskId": "o3", "op_spec": {"op": "add", "targetA": "ref:n1", "targetB": "ref:n2"}, "inputs": ["n1", "n2"]},
        ]

        with (
            patch("opsspec.modules.pipeline.build_chart_context", return_value=(self.context, [], self.rows_preview)),
            patch("opsspec.modules.pipeline.run_inventory_module", return_value=inventory_payload),
            patch("opsspec.modules.pipeline.run_step_compose_module", side_effect=step_payloads),
            patch("opsspec.modules.pipeline.build_draw_ops_spec", return_value={}),
            patch("opsspec.modules.pipeline.export_draw_plan_to_public", return_value=Path("/tmp/draw_plan.json")),
            patch("opsspec.modules.pipeline._persist_debug_bundle", return_value=Path("/tmp/debug_bundle")),
        ):
            pipeline = self._pipeline()
            result = pipeline.generate(
                question="q",
                explanation="e",
                vega_lite_spec={},
                data_rows=self.rows,
                request_id="req",
                debug=False,
            )

        self.assertIn("ops2", result.ops_spec)
        self.assertEqual(result.ops_spec["ops2"][-1].op, "add")

    def test_pairdiff_step_is_parsed_and_emitted(self) -> None:
        inventory_payload = {
            "tasks": [
                {
                    "taskId": "o1",
                    "op": "pairDiff",
                    "sentenceIndex": 1,
                    "mention": "compute per-season difference between broadcasting and commercial",
                    "paramsHint": {
                        "by": "@primary_dimension",
                        "field": "@primary_measure",
                        "groupA": "Broadcasting",
                        "groupB": "Commercial",
                    },
                }
            ],
            "warnings": [],
        }
        step_payloads = [
            {
                "pickTaskId": "o1",
                "op_spec": {
                    "op": "pairDiff",
                    "by": "@primary_dimension",
                    "field": "@primary_measure",
                    "groupA": "Broadcasting",
                    "groupB": "Commercial",
                },
                "inputs": [],
            }
        ]

        with (
            patch("opsspec.modules.pipeline.build_chart_context", return_value=(self.context, [], self.rows_preview)),
            patch("opsspec.modules.pipeline.run_inventory_module", return_value=inventory_payload),
            patch("opsspec.modules.pipeline.run_step_compose_module", side_effect=step_payloads),
            patch("opsspec.modules.pipeline.build_draw_ops_spec", return_value={}),
            patch("opsspec.modules.pipeline.export_draw_plan_to_public", return_value=Path("/tmp/draw_plan.json")),
            patch("opsspec.modules.pipeline._persist_debug_bundle", return_value=Path("/tmp/debug_bundle")),
        ):
            pipeline = self._pipeline()
            result = pipeline.generate(
                question="q",
                explanation="e",
                vega_lite_spec={},
                data_rows=self.rows,
                request_id="req",
                debug=False,
            )

        self.assertIn("ops", result.ops_spec)
        self.assertEqual(len(result.ops_spec["ops"]), 1)
        op = result.ops_spec["ops"][0]
        self.assertEqual(op.op, "pairDiff")
        self.assertEqual(op.by, "season")

    def test_pairdiff_grouped_bar_with_explicit_series_field(self) -> None:
        grouped_context = ChartContext(
            fields=["City", "Year", "Population in millions"],
            dimension_fields=["City", "Year"],
            measure_fields=["Population in millions"],
            primary_dimension="City",
            primary_measure="Population in millions",
            series_field="Year",
            categorical_values={"City": ["Tokyo", "Delhi"], "Year": ["2010", "2025"]},
            mark="bar",
            is_stacked=False,
        )
        grouped_rows = [
            {"City": "Tokyo", "Year": "2025", "Population in millions": 37.1},
            {"City": "Tokyo", "Year": "2010", "Population in millions": 36.7},
            {"City": "Delhi", "Year": "2025", "Population in millions": 28.6},
            {"City": "Delhi", "Year": "2010", "Population in millions": 22.2},
        ]
        inventory_payload = {
            "tasks": [
                {
                    "taskId": "o1",
                    "op": "pairDiff",
                    "sentenceIndex": 1,
                    "mention": "city-wise 2025 minus 2010",
                    "paramsHint": {
                        "by": "City",
                        "seriesField": "Year",
                        "field": "Population in millions",
                        "groupA": "2025",
                        "groupB": "2010",
                    },
                }
            ],
            "warnings": [],
        }
        step_payloads = [
            {
                "pickTaskId": "o1",
                "op_spec": {
                    "op": "pairDiff",
                    "by": "City",
                    "seriesField": "Year",
                    "field": "Population in millions",
                    "groupA": "2025",
                    "groupB": "2010",
                },
                "inputs": [],
            }
        ]

        with (
            patch("opsspec.modules.pipeline.build_chart_context", return_value=(grouped_context, [], grouped_rows[:2])),
            patch("opsspec.modules.pipeline.run_inventory_module", return_value=inventory_payload),
            patch("opsspec.modules.pipeline.run_step_compose_module", side_effect=step_payloads),
            patch("opsspec.modules.pipeline.build_draw_ops_spec", return_value={}),
            patch("opsspec.modules.pipeline.export_draw_plan_to_public", return_value=Path("/tmp/draw_plan.json")),
            patch("opsspec.modules.pipeline._persist_debug_bundle", return_value=Path("/tmp/debug_bundle")),
        ):
            pipeline = self._pipeline()
            result = pipeline.generate(
                question="q",
                explanation="e",
                vega_lite_spec={},
                data_rows=grouped_rows,
                request_id="req",
                debug=False,
            )

        self.assertIn("ops", result.ops_spec)
        self.assertEqual(len(result.ops_spec["ops"]), 1)
        op = result.ops_spec["ops"][0]
        self.assertEqual(op.op, "pairDiff")
        self.assertEqual(op.by, "City")
        self.assertEqual(op.seriesField, "Year")

    def test_filter_membership_on_non_primary_categorical_field(self) -> None:
        grouped_context = ChartContext(
            fields=["Frequency", "Race/Ethnicity", "Share of respondents"],
            dimension_fields=["Frequency", "Race/Ethnicity"],
            measure_fields=["Share of respondents"],
            primary_dimension="Race/Ethnicity",
            primary_measure="Share of respondents",
            series_field="Race/Ethnicity",
            categorical_values={
                "Frequency": [
                    "Frequently (one or more times per month)",
                    "Occasionally (less than once a month)",
                    "Infrequently (once a year or less)",
                ],
                "Race/Ethnicity": ["White", "Hispanic"],
            },
            mark="bar",
            is_stacked=False,
        )
        grouped_rows = [
            {
                "Frequency": "Frequently (one or more times per month)",
                "Race/Ethnicity": "White",
                "Share of respondents": 0.12,
            },
            {
                "Frequency": "Occasionally (less than once a month)",
                "Race/Ethnicity": "White",
                "Share of respondents": 0.40,
            },
            {
                "Frequency": "Occasionally (less than once a month)",
                "Race/Ethnicity": "Hispanic",
                "Share of respondents": 0.43,
            },
        ]
        inventory_payload = {
            "tasks": [
                {
                    "taskId": "o1",
                    "op": "filter",
                    "sentenceIndex": 1,
                    "mention": "keep occasionally frequency",
                    "paramsHint": {"field": "Frequency", "include": ["Occasionally (less than once a month)"]},
                }
            ],
            "warnings": [],
        }
        step_payloads = [
            {
                "pickTaskId": "o1",
                "op_spec": {"op": "filter", "field": "Frequency", "include": ["Occasionally (less than once a month)"]},
                "inputs": [],
            }
        ]

        with (
            patch("opsspec.modules.pipeline.build_chart_context", return_value=(grouped_context, [], grouped_rows[:2])),
            patch("opsspec.modules.pipeline.run_inventory_module", return_value=inventory_payload),
            patch("opsspec.modules.pipeline.run_step_compose_module", side_effect=step_payloads),
            patch("opsspec.modules.pipeline.build_draw_ops_spec", return_value={}),
            patch("opsspec.modules.pipeline.export_draw_plan_to_public", return_value=Path("/tmp/draw_plan.json")),
            patch("opsspec.modules.pipeline._persist_debug_bundle", return_value=Path("/tmp/debug_bundle")),
        ):
            pipeline = self._pipeline()
            result = pipeline.generate(
                question="q",
                explanation="e",
                vega_lite_spec={},
                data_rows=grouped_rows,
                request_id="req",
                debug=False,
            )

        self.assertIn("ops", result.ops_spec)
        self.assertEqual(len(result.ops_spec["ops"]), 1)
        op = result.ops_spec["ops"][0]
        self.assertEqual(op.op, "filter")
        self.assertEqual(op.field, "Frequency")

    def test_filter_group_only_step_is_allowed(self) -> None:
        inventory_payload = {
            "tasks": [
                {
                    "taskId": "o1",
                    "op": "filter",
                    "sentenceIndex": 1,
                    "mention": "keep only broadcasting and commercial series",
                    "paramsHint": {"group": ["broadcasting", "commercial"]},
                }
            ],
            "warnings": [],
        }
        step_payloads = [
            {
                "pickTaskId": "o1",
                "op_spec": {"op": "filter", "group": ["broadcasting", "commercial"]},
                "inputs": [],
            }
        ]

        with (
            patch("opsspec.modules.pipeline.build_chart_context", return_value=(self.context, [], self.rows_preview)),
            patch("opsspec.modules.pipeline.run_inventory_module", return_value=inventory_payload),
            patch("opsspec.modules.pipeline.run_step_compose_module", side_effect=step_payloads),
            patch("opsspec.modules.pipeline.build_draw_ops_spec", return_value={}),
            patch("opsspec.modules.pipeline.export_draw_plan_to_public", return_value=Path("/tmp/draw_plan.json")),
            patch("opsspec.modules.pipeline._persist_debug_bundle", return_value=Path("/tmp/debug_bundle")),
        ):
            pipeline = self._pipeline()
            result = pipeline.generate(
                question="q",
                explanation="e",
                vega_lite_spec={},
                data_rows=self.rows,
                request_id="req",
                debug=False,
            )

        self.assertIn("ops", result.ops_spec)
        self.assertEqual(len(result.ops_spec["ops"]), 1)
        op = result.ops_spec["ops"][0]
        self.assertEqual(op.op, "filter")
        self.assertEqual(op.group, ["Broadcasting", "Commercial"])
