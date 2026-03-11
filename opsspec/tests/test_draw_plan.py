from __future__ import annotations

import unittest

from draw_plan.build_draw_plan import build_draw_ops_spec
from opsspec.core.models import ChartContext
from opsspec.specs.base import OpsMeta
from opsspec.specs.compare import CompareOp, DiffOp, PairDiffOp
from opsspec.specs.filter import FilterOp
from opsspec.specs.aggregate import AverageOp
from opsspec.specs.add import AddOp
from opsspec.specs.scale import ScaleOp
from opsspec.specs.set_op import SetOp
from opsspec.specs.range_sort_select import DetermineRangeOp
from opsspec.runtime.scheduler import schedule_ops_spec


class DrawPlanTest(unittest.TestCase):
    def test_builds_draw_ops_for_scalar_and_target_results(self) -> None:
        context = ChartContext(
            fields=["month", "weather", "count"],
            dimension_fields=["month", "weather"],
            measure_fields=["count"],
            primary_dimension="month",
            primary_measure="count",
            series_field="weather",
            categorical_values={
                "month": ["Jan", "Feb", "Mar"],
                "weather": ["rain", "sun"],
            },
            mark="bar",
            is_stacked=True,
        )
        data_rows = [
            {"month": "Jan", "weather": "rain", "count": 10},
            {"month": "Feb", "weather": "rain", "count": 20},
            {"month": "Mar", "weather": "rain", "count": 30},
            {"month": "Jan", "weather": "sun", "count": 12},
            {"month": "Feb", "weather": "sun", "count": 16},
            {"month": "Mar", "weather": "sun", "count": 18},
        ]
        ops_spec = {
            "ops": [
                AverageOp(op="average", field="count", group="rain", meta=OpsMeta(nodeId="n1", sentenceIndex=1)),
                FilterOp(
                    op="filter",
                    field="count",
                    operator=">",
                    value="ref:n1",
                    group="rain",
                    meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
                ),
            ]
        }

        draw_plan = build_draw_ops_spec(
            ops_spec=ops_spec,
            chart_context=context,
            data_rows=data_rows,
            vega_lite_spec={"mark": "bar"},
        )
        ops = draw_plan.get("ops", [])

        self.assertTrue(any(op.get("action") == "line" for op in ops))
        self.assertTrue(any(op.get("action") == "highlight" for op in ops))
        self.assertTrue(any(op.get("action") == "stacked-filter-groups" for op in ops))
        self.assertTrue(
            any(
                op.get("action") == "stacked-filter-groups"
                and isinstance(op.get("groupFilter"), dict)
                and op.get("groupFilter", {}).get("groups") == ["rain"]
                for op in ops
            )
        )
        self.assertTrue(
            any(
                op.get("action") == "stacked-filter-groups"
                and isinstance(op.get("groupFilter"), dict)
                and op.get("groupFilter", {}).get("reset") is True
                for op in ops
            )
        )

    def test_builds_extended_draw_ops_for_set_pair_add_scale(self) -> None:
        context = ChartContext(
            fields=["month", "weather", "count"],
            dimension_fields=["month", "weather"],
            measure_fields=["count"],
            primary_dimension="month",
            primary_measure="count",
            series_field="weather",
            categorical_values={
                "month": ["Jan", "Feb", "Mar"],
                "weather": ["rain", "sun"],
            },
            mark="bar",
            is_stacked=False,
        )
        data_rows = [
            {"month": "Jan", "weather": "rain", "count": 10},
            {"month": "Feb", "weather": "rain", "count": 20},
            {"month": "Mar", "weather": "rain", "count": 30},
            {"month": "Jan", "weather": "sun", "count": 12},
            {"month": "Feb", "weather": "sun", "count": 16},
            {"month": "Mar", "weather": "sun", "count": 18},
        ]
        ops_spec = {
            "ops": [
                FilterOp(op="filter", field="count", operator=">", value=0, group="rain", meta=OpsMeta(nodeId="n1", sentenceIndex=1)),
                FilterOp(op="filter", field="count", operator=">", value=0, group="sun", meta=OpsMeta(nodeId="n2", sentenceIndex=1)),
                SetOp(op="setOp", fn="intersection", meta=OpsMeta(nodeId="n3", inputs=["n1", "n2"], sentenceIndex=1)),
                PairDiffOp(
                    op="pairDiff",
                    by="month",
                    seriesField="weather",
                    field="count",
                    groupA="rain",
                    groupB="sun",
                    meta=OpsMeta(nodeId="n4", sentenceIndex=1),
                ),
                AddOp(op="add", targetA="Jan", targetB="Feb", field="count", meta=OpsMeta(nodeId="n5", sentenceIndex=1)),
                ScaleOp(op="scale", target="Mar", factor=2, field="count", meta=OpsMeta(nodeId="n6", sentenceIndex=1)),
                CompareOp(
                    op="compare",
                    targetA={"target": "Jan"},
                    targetB={"target": "Jan"},
                    groupA="rain",
                    groupB="sun",
                    field="count",
                    meta=OpsMeta(nodeId="n7", sentenceIndex=1),
                ),
                DetermineRangeOp(op="determineRange", field="count", meta=OpsMeta(nodeId="n8", sentenceIndex=1)),
            ]
        }

        draw_plan = build_draw_ops_spec(
            ops_spec=ops_spec,
            chart_context=context,
            data_rows=data_rows,
            vega_lite_spec={"mark": "bar"},
        )
        ops = draw_plan.get("ops", [])

        actions = [op.get("action") for op in ops]
        self.assertIn("band", actions)
        self.assertIn("line", actions)
        self.assertIn("text", actions)
        connect_lines = [op for op in ops if op.get("action") == "line" and op.get("line", {}).get("mode") == "connect"]
        self.assertTrue(len(connect_lines) >= 1)

    def test_builds_split_plan_with_panel_scalar_bridge_for_fork_join_branches(self) -> None:
        context = ChartContext(
            fields=["Year", "Installed base in million units"],
            dimension_fields=["Year"],
            measure_fields=["Installed base in million units"],
            primary_dimension="Year",
            primary_measure="Installed base in million units",
            categorical_values={
                "Year": ["1995", "1999", "2010", "2013", "2017"],
            },
            mark="bar",
            is_stacked=False,
        )
        data_rows = [
            {"Year": "1995", "Installed base in million units": 10},
            {"Year": "1999", "Installed base in million units": 14},
            {"Year": "2010", "Installed base in million units": 20},
            {"Year": "2013", "Installed base in million units": 22},
            {"Year": "2017", "Installed base in million units": 26},
        ]
        ops_spec = {
            "ops": [
                FilterOp(
                    op="filter",
                    id="n1",
                    meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
                    field="Year",
                    include=["1995", "1999"],
                ),
                AverageOp(
                    op="average",
                    id="n2",
                    meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
                    field="Installed base in million units",
                ),
            ],
            "ops2": [
                FilterOp(
                    op="filter",
                    id="n3",
                    meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=2),
                    field="Year",
                    include=["2010", "2013", "2017"],
                ),
                AverageOp(
                    op="average",
                    id="n4",
                    meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=2),
                    field="Installed base in million units",
                ),
            ],
            "ops3": [
                DiffOp(
                    op="diff",
                    id="n5",
                    meta=OpsMeta(nodeId="n5", inputs=["n2", "n4"], sentenceIndex=3),
                    field="Installed base in million units",
                    targetA="ref:n2",
                    targetB="ref:n4",
                )
            ],
        }

        scheduled = schedule_ops_spec(ops_spec)
        draw_plan = build_draw_ops_spec(
            ops_spec=scheduled,
            chart_context=context,
            data_rows=data_rows,
            vega_lite_spec={"mark": "bar"},
        )

        ops_group = draw_plan.get("ops", [])
        ops2_group = draw_plan.get("ops2", [])
        ops3_group = draw_plan.get("ops3", [])

        self.assertTrue(any(op.get("action") == "split" for op in ops_group))
        split_op = next(op for op in ops_group if op.get("action") == "split")
        self.assertEqual(split_op.get("split", {}).get("orientation"), "horizontal")
        self.assertEqual(split_op.get("split", {}).get("groups", {}).get("left"), ["1995", "1999"])
        self.assertEqual(split_op.get("split", {}).get("groups", {}).get("right"), ["2010", "2013", "2017"])

        scoped_ops = [op for op in ops_group if op.get("action") != "clear" and op.get("action") != "split"]
        self.assertTrue(scoped_ops)
        self.assertTrue(all(op.get("chartId") == "left" for op in scoped_ops))

        scoped_ops2 = [op for op in ops2_group if op.get("action") != "clear"]
        self.assertTrue(scoped_ops2)
        self.assertTrue(all(op.get("chartId") == "right" for op in scoped_ops2))

        self.assertFalse(any(op.get("action") == "unsplit" for op in ops3_group))
        post_join_ops = [op for op in ops3_group if op.get("action") != "clear"]
        self.assertTrue(post_join_ops)
        self.assertTrue(all(op.get("chartId") is None for op in post_join_ops))
        bridge_lines = [
            op
            for op in post_join_ops
            if op.get("action") == "line" and op.get("line", {}).get("mode") == "connect-panel-scalar"
        ]
        self.assertEqual(len(bridge_lines), 1)
        bridge_spec = bridge_lines[0].get("line", {}).get("panelScalar", {})
        self.assertEqual(bridge_spec.get("start", {}).get("chartId"), "left")
        self.assertEqual(bridge_spec.get("end", {}).get("chartId"), "right")


if __name__ == "__main__":
    unittest.main()
