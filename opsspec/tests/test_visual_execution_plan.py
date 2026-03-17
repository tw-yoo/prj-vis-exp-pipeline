from __future__ import annotations

import unittest

from opsspec.runtime.scheduler import schedule_ops_spec
from opsspec.runtime.visual_execution_plan import build_visual_execution_plan
from opsspec.specs.aggregate import AverageOp, RetrieveValueOp
from opsspec.specs.base import OpsMeta
from opsspec.specs.compare import CompareOp, DiffOp
from opsspec.specs.filter import FilterOp
from opsspec.specs.scale import ScaleOp


class VisualExecutionPlanTest(unittest.TestCase):
    def test_builds_operand_only_average_as_only_materialized_surface(self) -> None:
        ops_spec = {
            "ops": [
                RetrieveValueOp(
                    op="retrieveValue",
                    id="n1",
                    meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
                    field="rating",
                    target="USA",
                ),
                RetrieveValueOp(
                    op="retrieveValue",
                    id="n2",
                    meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=1),
                    field="rating",
                    target="JPN",
                ),
                AverageOp(
                    op="average",
                    id="n3",
                    meta=OpsMeta(nodeId="n3", inputs=["n1", "n2"], sentenceIndex=1),
                    field="rating",
                ),
            ],
        }

        plan = build_visual_execution_plan(ops_spec=schedule_ops_spec(ops_spec))

        self.assertEqual(plan.get("mode"), "linear-derived-chart-flow")
        self.assertEqual(plan.get("reusePolicy"), "result-only")
        steps = plan.get("steps") or []
        self.assertEqual(len(steps), 1)
        self.assertEqual(steps[0].get("navigationUnit"), "sentence")
        self.assertEqual(steps[0].get("surfacePolicy"), "keep-final-derived-chart")

        substeps = steps[0].get("substeps") or []
        self.assertEqual(
            [substep.get("kind") for substep in substeps],
            ["run-op", "run-op", "materialize-surface", "run-op"],
        )
        self.assertEqual(substeps[0].get("surface", {}).get("surfaceType"), "source-chart")
        self.assertEqual(substeps[1].get("surface", {}).get("surfaceType"), "source-chart")
        self.assertEqual(substeps[2].get("surface", {}).get("templateType"), "operand-only-chart")
        self.assertEqual(substeps[3].get("surface", {}).get("surfaceType"), "derived-chart")

    def test_exposes_group_prefilter_as_visible_linear_substep(self) -> None:
        ops_spec = {
            "ops": [
                AverageOp(
                    op="average",
                    id="n1",
                    meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
                    field="count",
                    group="rain",
                )
            ]
        }

        plan = build_visual_execution_plan(ops_spec=schedule_ops_spec(ops_spec))
        steps = plan.get("steps") or []
        substeps = steps[0].get("substeps") or []

        self.assertEqual([substep.get("kind") for substep in substeps], ["prefilter", "materialize-surface", "run-op"])
        self.assertEqual(substeps[0].get("scope", {}).get("groups"), ["rain"])
        self.assertEqual(substeps[1].get("surface", {}).get("templateType"), "filtered-operands-chart")
        self.assertEqual(substeps[2].get("opName"), "average")
        self.assertEqual(substeps[2].get("surface", {}).get("surfaceType"), "derived-chart")

    def test_keeps_literal_target_compare_on_source_chart(self) -> None:
        ops_spec = {
            "ops": [
                RetrieveValueOp(
                    op="retrieveValue",
                    id="n1",
                    meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
                    field="rating",
                    target="USA",
                ),
                CompareOp(
                    op="compare",
                    id="n2",
                    meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=1),
                    field="rating",
                    targetA="USA",
                    targetB="JPN",
                ),
            ]
        }

        plan = build_visual_execution_plan(ops_spec=schedule_ops_spec(ops_spec))
        steps = plan.get("steps") or []
        substeps = steps[0].get("substeps") or []

        self.assertEqual([substep.get("kind") for substep in substeps], ["run-op", "run-op"])
        self.assertEqual(substeps[0].get("surface", {}).get("surfaceType"), "source-chart")
        self.assertEqual(substeps[1].get("surface", {}).get("surfaceType"), "source-chart")

    def test_keeps_ref_diff_on_source_chart(self) -> None:
        ops_spec = {
            "ops": [
                RetrieveValueOp(
                    op="retrieveValue",
                    id="n1",
                    meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
                    field="rating",
                    target="USA",
                ),
                RetrieveValueOp(
                    op="retrieveValue",
                    id="n2",
                    meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=1),
                    field="rating",
                    target="JPN",
                ),
                DiffOp(
                    op="diff",
                    id="n3",
                    meta=OpsMeta(nodeId="n3", inputs=["n1", "n2"], sentenceIndex=1),
                    field="rating",
                    targetA="ref:n1",
                    targetB="ref:n2",
                ),
            ]
        }

        plan = build_visual_execution_plan(ops_spec=schedule_ops_spec(ops_spec))
        steps = plan.get("steps") or []
        substeps = steps[0].get("substeps") or []

        self.assertEqual([substep.get("kind") for substep in substeps], ["run-op", "run-op", "run-op"])
        self.assertTrue(all(substep.get("surface", {}).get("surfaceType") == "source-chart" for substep in substeps))

    def test_keeps_scale_ref_on_source_chart(self) -> None:
        ops_spec = {
            "ops": [
                AverageOp(
                    op="average",
                    id="n1",
                    meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
                    field="rating",
                ),
                ScaleOp(
                    op="scale",
                    id="n2",
                    meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=1),
                    field="rating",
                    target="ref:n1",
                    factor=1.1,
                ),
            ]
        }

        plan = build_visual_execution_plan(ops_spec=schedule_ops_spec(ops_spec))
        steps = plan.get("steps") or []
        substeps = steps[0].get("substeps") or []

        self.assertEqual([substep.get("kind") for substep in substeps], ["run-op", "run-op"])
        self.assertEqual(substeps[0].get("surface", {}).get("surfaceType"), "source-chart")
        self.assertEqual(substeps[1].get("surface", {}).get("surfaceType"), "source-chart")

    def test_materializes_diff_when_ref_uses_synthetic_result(self) -> None:
        ops_spec = {
            "ops": [
                RetrieveValueOp(
                    op="retrieveValue",
                    id="n1",
                    meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
                    field="rating",
                    target="USA",
                ),
                RetrieveValueOp(
                    op="retrieveValue",
                    id="n2",
                    meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=1),
                    field="rating",
                    target="JPN",
                ),
                DiffOp(
                    op="diff",
                    id="n3",
                    meta=OpsMeta(nodeId="n3", inputs=["n1", "n2"], sentenceIndex=1),
                    field="rating",
                    targetA="ref:n1",
                    targetB="ref:n2",
                ),
            ],
            "ops2": [
                RetrieveValueOp(
                    op="retrieveValue",
                    id="n4",
                    meta=OpsMeta(nodeId="n4", inputs=[], sentenceIndex=2),
                    field="rating",
                    target="NLD",
                ),
                DiffOp(
                    op="diff",
                    id="n5",
                    meta=OpsMeta(nodeId="n5", inputs=["n4", "n3"], sentenceIndex=2),
                    field="rating",
                    targetA="ref:n4",
                    targetB="ref:n3",
                ),
            ],
        }

        plan = build_visual_execution_plan(ops_spec=schedule_ops_spec(ops_spec))
        steps = plan.get("steps") or []
        self.assertEqual(len(steps), 2)
        substeps = steps[1].get("substeps") or []

        self.assertEqual([substep.get("kind") for substep in substeps], ["run-op", "materialize-surface", "run-op"])
        self.assertEqual(substeps[0].get("surface", {}).get("surfaceType"), "source-chart")
        self.assertEqual(substeps[1].get("surface", {}).get("templateType"), "mixed-operands-chart")
        self.assertEqual(substeps[2].get("surface", {}).get("surfaceType"), "derived-chart")


if __name__ == "__main__":
    unittest.main()
