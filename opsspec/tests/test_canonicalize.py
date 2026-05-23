from __future__ import annotations

import unittest

from opsspec.runtime.canonicalize import canonicalize_ops_spec_groups
from opsspec.core.models import ChartContext
from opsspec.specs.aggregate import AverageOp
from opsspec.specs.base import OpsMeta
from opsspec.specs.filter import FilterOp


class CanonicalizeTest(unittest.TestCase):
    def test_assigns_node_id_and_id_for_chained_ops(self) -> None:
        context = ChartContext(
            fields=["season", "category", "Revenue_Million_Euros"],
            dimension_fields=["season"],
            measure_fields=["Revenue_Million_Euros"],
            primary_dimension="season",
            primary_measure="Revenue_Million_Euros",
            series_field="category",
            categorical_values={"category": ["Broadcasting", "Commercial"]},
        )
        # Chained filters (replacement for the removed setOp pattern): the second
        # filter consumes the first via meta.inputs, expressing intersection of
        # the two include lists.
        groups = {
            "ops": [
                FilterOp(
                    op="filter",
                    field="season",
                    include=["2016/17", "2017/18"],
                    meta=OpsMeta(nodeId="n1"),
                ),
            ],
            "ops2": [
                FilterOp(
                    op="filter",
                    field="season",
                    include=["2017/18"],
                    meta=OpsMeta(nodeId="n2", inputs=["n1"]),
                ),
            ],
            "ops3": [
                AverageOp(
                    op="average",
                    field="Revenue_Million_Euros",
                    meta=OpsMeta(nodeId="n3", inputs=["n2"]),
                ),
            ],
        }
        normalized, warnings = canonicalize_ops_spec_groups(groups, chart_context=context)
        self.assertTrue(normalized["ops"][0].id)
        self.assertTrue(normalized["ops"][0].meta and normalized["ops"][0].meta.nodeId)
        self.assertEqual(normalized["ops2"][0].meta.inputs, ["n1"])
        self.assertEqual(normalized["ops3"][0].meta.inputs, ["n2"])
        self.assertIsNotNone(warnings)


if __name__ == "__main__":
    unittest.main()
