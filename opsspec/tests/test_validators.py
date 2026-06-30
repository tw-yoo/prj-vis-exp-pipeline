from __future__ import annotations

import unittest

from opsspec.core.models import ChartContext
from opsspec.specs.add import AddOp
from opsspec.specs.aggregate import AverageOp, CountOp, RetrieveValueOp, SumOp
from opsspec.specs.base import OpsMeta
from opsspec.specs.compare import DiffOp, LagDiffOp, PairDiffOp
from opsspec.specs.filter import FilterOp
from opsspec.specs.range_sort_select import FindExtremumOp
from opsspec.specs.scale import ScaleOp
from opsspec.specs.union import parse_operation_spec
from opsspec.runtime.op_registry import build_ops_contract_for_prompt
from opsspec.validation.validators import dimension_filter_for_group_op, validate_operation


class ValidatorsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.context = ChartContext(
            fields=["season", "category", "Revenue_Million_Euros"],
            dimension_fields=["season", "category"],
            measure_fields=["Revenue_Million_Euros"],
            primary_dimension="season",
            primary_measure="Revenue_Million_Euros",
            series_field="category",
            categorical_values={"category": ["Broadcasting", "Commercial"]},
        )

    def test_filter_membership_and_comparison_conflict_raises(self) -> None:
        op = FilterOp(
            op="filter",
            field="season",
            include=["2016/17"],
            operator=">",
            value=1,
        )
        with self.assertRaises(ValueError):
            validate_operation(op, chart_context=self.context)

    def test_filter_group_list_is_normalized_and_allowed(self) -> None:
        op = FilterOp(
            op="filter",
            field="season",
            include=["2016/17"],
            group=[" Broadcasting ", "Commercial", "Broadcasting"],
        )
        normalized, _ = validate_operation(op, chart_context=self.context)
        self.assertEqual(normalized.group, ["Broadcasting", "Commercial"])

    def test_filter_group_empty_list_raises(self) -> None:
        op = FilterOp(op="filter", field="season", include=["2016/17"], group=[])
        with self.assertRaises(ValueError):
            validate_operation(op, chart_context=self.context)

    def test_filter_group_list_with_empty_value_raises(self) -> None:
        op = FilterOp(op="filter", field="season", include=["2016/17"], group=["Broadcasting", ""])
        with self.assertRaises(ValueError):
            validate_operation(op, chart_context=self.context)

    def test_filter_group_outside_series_domain_raises(self) -> None:
        op = FilterOp(op="filter", field="season", include=["2016/17"], group=["Broadcasting", "Unknown"])
        with self.assertRaises(ValueError):
            validate_operation(op, chart_context=self.context)

    def test_filter_group_only_mode_is_allowed(self) -> None:
        op = FilterOp(op="filter", group=["Broadcasting", "Commercial"])
        normalized, _ = validate_operation(op, chart_context=self.context)
        self.assertEqual(normalized.group, ["Broadcasting", "Commercial"])

    def test_filter_membership_non_primary_categorical_field_is_allowed(self) -> None:
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
                ],
                "Race/Ethnicity": ["White", "Hispanic"],
            },
            field_types={
                "Frequency": "categorical",
                "Race/Ethnicity": "categorical",
                "Share of respondents": "numeric",
            },
            mark="bar",
            is_stacked=False,
        )
        op = FilterOp(op="filter", field="Frequency", include=["Occasionally (less than once a month)"])
        normalized, _ = validate_operation(op, chart_context=grouped_context)
        self.assertEqual(normalized.field, "Frequency")

    def test_filter_membership_numeric_field_raises(self) -> None:
        op = FilterOp(op="filter", field="Revenue_Million_Euros", include=[100])
        with self.assertRaises(ValueError):
            validate_operation(op, chart_context=self.context)

    def test_filter_comparison_without_field_raises(self) -> None:
        op = FilterOp(op="filter", operator=">", value=10, group="Broadcasting")
        with self.assertRaises(ValueError):
            validate_operation(op, chart_context=self.context)

    def test_filter_between_on_categorical_dimension_is_allowed(self) -> None:
        op = FilterOp(op="filter", field="season", operator="between", value=["2016/17", "2017/18"])
        normalized, _ = validate_operation(op, chart_context=self.context)
        self.assertEqual(normalized.operator, "between")

    def test_filter_between_requires_two_item_list(self) -> None:
        with self.assertRaises(ValueError):
            validate_operation(
                FilterOp(op="filter", field="season", operator="between", value="2016/17"),
                chart_context=self.context,
            )
        with self.assertRaises(ValueError):
            validate_operation(
                FilterOp(op="filter", field="season", operator="between", value=["2016/17"]),
                chart_context=self.context,
            )

    def test_filter_between_rejects_boundary_outside_domain(self) -> None:
        context_with_season_domain = self.context.model_copy(
            update={"categorical_values": {"category": ["Broadcasting", "Commercial"], "season": ["2016/17", "2017/18"]}}
        )
        with self.assertRaises(ValueError):
            validate_operation(
                FilterOp(op="filter", field="season", operator="between", value=["2010/11", "2017/18"]),
                chart_context=context_with_season_domain,
            )

    def test_filter_accepts_x_kind_hint(self) -> None:
        op = FilterOp(op="filter", field="season", include=["2016/17"], xKindHint="temporal")
        normalized, _ = validate_operation(op, chart_context=self.context)
        self.assertEqual(normalized.xKindHint, "temporal")

    def test_filter_rejects_invalid_x_kind_hint(self) -> None:
        with self.assertRaises(ValueError):
            FilterOp(op="filter", field="season", include=["2016/17"], xKindHint="date-like")

    def test_average_defaults_to_primary_measure(self) -> None:
        op = AverageOp(op="average", field=None)
        normalized, _ = validate_operation(op, chart_context=self.context)
        self.assertEqual(normalized.field, "Revenue_Million_Euros")

    def test_scale_accepts_ref_target(self) -> None:
        op = ScaleOp(op="scale", target="ref:n2", factor=2.0)
        normalized, _ = validate_operation(op, chart_context=self.context)
        self.assertEqual(normalized.factor, 2.0)

    def test_scale_rejects_non_ref_string_target(self) -> None:
        op = ScaleOp(op="scale", target="n2", factor=2.0)
        with self.assertRaises(ValueError):
            validate_operation(op, chart_context=self.context)

    def test_scale_parse_operation_spec(self) -> None:
        parsed = parse_operation_spec({"op": "scale", "target": "ref:n5", "factor": 2.0})
        self.assertEqual(parsed.op, "scale")

    def test_add_accepts_ref_and_numeric_literal(self) -> None:
        op = AddOp(op="add", targetA="ref:n2", targetB=3.5)
        normalized, _ = validate_operation(op, chart_context=self.context)
        self.assertEqual(normalized.op, "add")

    def test_add_rejects_invalid_ref_and_non_numeric(self) -> None:
        with self.assertRaises(ValueError):
            validate_operation(AddOp(op="add", targetA="n2", targetB="ref:n3"), chart_context=self.context)
        with self.assertRaises(ValueError):
            validate_operation(AddOp(op="add", targetA="abc", targetB="ref:n3"), chart_context=self.context)

    def test_pairdiff_accepts_valid_params(self) -> None:
        op = PairDiffOp(
            op="pairDiff",
            by="season",
            field="Revenue_Million_Euros",
            groupA="Broadcasting",
            groupB="Commercial",
            signed=True,
        )
        normalized, _ = validate_operation(op, chart_context=self.context)
        self.assertEqual(normalized.op, "pairDiff")

    def test_determine_range_is_not_registered_operation(self) -> None:
        contract = build_ops_contract_for_prompt()
        self.assertNotIn("determineRange", contract.get("allowed_ops", []))
        self.assertNotIn("determineRange", contract.get("op_contracts", {}))
        with self.assertRaises(Exception):
            parse_operation_spec({"op": "determineRange", "field": "Revenue_Million_Euros"})

    def test_pairdiff_rejected_for_simple_bar(self) -> None:
        simple_bar_context = ChartContext(
            fields=["season", "Revenue_Million_Euros"],
            dimension_fields=["season"],
            measure_fields=["Revenue_Million_Euros"],
            primary_dimension="season",
            primary_measure="Revenue_Million_Euros",
            series_field=None,
            categorical_values={"season": ["2016/17", "2017/18"]},
            mark="bar",
            is_stacked=False,
        )
        op = PairDiffOp(
            op="pairDiff",
            by="season",
            field="Revenue_Million_Euros",
            groupA="2016/17",
            groupB="2017/18",
        )
        with self.assertRaisesRegex(ValueError, 'op "pairDiff" is not allowed for chart_family="bar_simple"'):
            validate_operation(op, chart_context=simple_bar_context)

    def test_pairdiff_rejected_for_simple_line(self) -> None:
        simple_line_context = ChartContext(
            fields=["season", "Revenue_Million_Euros"],
            dimension_fields=["season"],
            measure_fields=["Revenue_Million_Euros"],
            primary_dimension="season",
            primary_measure="Revenue_Million_Euros",
            series_field=None,
            categorical_values={"season": ["2016/17", "2017/18"]},
            mark="line",
            is_stacked=False,
        )
        op = PairDiffOp(
            op="pairDiff",
            by="season",
            field="Revenue_Million_Euros",
            groupA="2016/17",
            groupB="2017/18",
        )
        with self.assertRaisesRegex(ValueError, 'op "pairDiff" is not allowed for chart_family="line_simple"'):
            validate_operation(op, chart_context=simple_line_context)

    def test_prompt_contract_excludes_pairdiff_for_simple_charts(self) -> None:
        simple_bar_context = ChartContext(
            fields=["season", "Revenue_Million_Euros"],
            dimension_fields=["season"],
            measure_fields=["Revenue_Million_Euros"],
            primary_dimension="season",
            primary_measure="Revenue_Million_Euros",
            series_field=None,
            categorical_values={"season": ["2016/17", "2017/18"]},
            mark="bar",
            is_stacked=False,
        )
        contract = build_ops_contract_for_prompt(chart_context=simple_bar_context)
        self.assertEqual(contract.get("chart_family"), "bar_simple")
        self.assertNotIn("pairDiff", contract.get("allowed_ops", []))
        self.assertIn("pairDiff", contract.get("unavailable_ops", {}))

        simple_line_context = simple_bar_context.model_copy(update={"mark": "line"})
        contract = build_ops_contract_for_prompt(chart_context=simple_line_context)
        self.assertEqual(contract.get("chart_family"), "line_simple")
        self.assertNotIn("pairDiff", contract.get("allowed_ops", []))
        self.assertIn("pairDiff", contract.get("unavailable_ops", {}))

    def test_pairdiff_rejects_same_groups(self) -> None:
        op = PairDiffOp(
            op="pairDiff",
            by="season",
            field="Revenue_Million_Euros",
            groupA="Broadcasting",
            groupB="Broadcasting",
        )
        with self.assertRaises(ValueError):
            validate_operation(op, chart_context=self.context)

    def test_pairdiff_parse_operation_spec(self) -> None:
        parsed = parse_operation_spec(
            {
                "op": "pairDiff",
                "by": "season",
                "field": "Revenue_Million_Euros",
                "groupA": "Broadcasting",
                "groupB": "Commercial",
            }
        )
        self.assertEqual(parsed.op, "pairDiff")

    def test_pairdiff_with_explicit_series_field_for_grouped_bar(self) -> None:
        grouped_ctx = ChartContext(
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
        op = PairDiffOp(
            op="pairDiff",
            by="City",
            seriesField="Year",
            field="Population in millions",
            groupA="2025",
            groupB="2010",
        )
        normalized, _ = validate_operation(op, chart_context=grouped_ctx)
        self.assertEqual(normalized.by, "City")

    def test_pairdiff_rejects_unknown_series_field(self) -> None:
        op = PairDiffOp(
            op="pairDiff",
            by="season",
            seriesField="unknown",
            field="Revenue_Million_Euros",
            groupA="Broadcasting",
            groupB="Commercial",
        )
        with self.assertRaises(ValueError):
            validate_operation(op, chart_context=self.context)

    def test_sum_allowed_on_line_chart(self) -> None:
        # line+sum은 이제 허용된다(프론트엔드에서 line→bar 전환 후 stack으로 시각화).
        line_context = self.context.model_copy(update={"mark": "line", "is_stacked": False})
        op = SumOp(op="sum", field="Revenue_Million_Euros")
        normalized, _ = validate_operation(op, chart_context=line_context)
        self.assertEqual(normalized.op, "sum")

    def test_sum_allowed_on_multiline_with_series_group(self) -> None:
        line_context = self.context.model_copy(update={"mark": "line", "is_stacked": False})
        op = SumOp(op="sum", field="Revenue_Million_Euros", group="Broadcasting")
        normalized, _ = validate_operation(op, chart_context=line_context)
        self.assertEqual(normalized.group, "Broadcasting")

    def test_sum_accepts_bar_chart_and_normalizes_group_list(self) -> None:
        bar_context = self.context.model_copy(update={"mark": "bar", "is_stacked": False})
        op = SumOp(op="sum", field="Revenue_Million_Euros", group=[" Broadcasting ", "Commercial", "Broadcasting"])
        normalized, _ = validate_operation(op, chart_context=bar_context)
        self.assertEqual(normalized.group, ["Broadcasting", "Commercial"])

    def test_sum_group_empty_list_raises(self) -> None:
        bar_context = self.context.model_copy(update={"mark": "bar", "is_stacked": False})
        op = SumOp(op="sum", field="Revenue_Million_Euros", group=[])
        with self.assertRaises(ValueError):
            validate_operation(op, chart_context=bar_context)

    def test_sum_group_outside_series_domain_raises(self) -> None:
        bar_context = self.context.model_copy(update={"mark": "bar", "is_stacked": True})
        op = SumOp(op="sum", field="Revenue_Million_Euros", group=["Unknown"])
        with self.assertRaises(ValueError):
            validate_operation(op, chart_context=bar_context)

    def test_filter_group_dimension_value_rewritten_to_include(self) -> None:
        # group="2016/17"은 season(dimension) 값이지 category(series) 값이 아니다 →
        # 거부 대신 season에 대한 include 필터로 in-place 변환되어야 한다.
        ctx = ChartContext(
            fields=["season", "category", "value"],
            dimension_fields=["season", "category"],
            measure_fields=["value"],
            primary_dimension="season",
            primary_measure="value",
            series_field="category",
            categorical_values={"season": ["2016/17", "2017/18"], "category": ["Broadcasting", "Commercial"]},
        )
        op = FilterOp(op="filter", group="2016/17")
        validated, warnings = validate_operation(op, chart_context=ctx)
        self.assertEqual(validated.field, "season")
        self.assertEqual(validated.include, ["2016/17"])
        self.assertIsNone(validated.group)
        self.assertTrue(any("rewrote group" in w for w in warnings))

    def test_filter_on_series_field_include_rewritten_to_group(self) -> None:
        # series 필드에 직접 filter(include) → 거부 대신 group 제한으로 변환 (B).
        op = FilterOp(op="filter", field="category", include=["Broadcasting"])
        validated, warnings = validate_operation(op, chart_context=self.context)
        self.assertIsNone(validated.field)
        self.assertEqual(validated.group, ["Broadcasting"])
        self.assertTrue(any("series restriction" in w for w in warnings))

    def test_filter_on_series_field_exclude_rewritten_to_complement_group(self) -> None:
        op = FilterOp(op="filter", field="category", exclude=["Broadcasting"])
        validated, _ = validate_operation(op, chart_context=self.context)
        self.assertEqual(validated.group, ["Commercial"])

    def test_filter_group_valid_series_value_not_rewritten(self) -> None:
        # 진짜 series 값(Broadcasting)이면 변환하지 않고 group으로 유지(회귀 방지).
        op = FilterOp(op="filter", group="Broadcasting")
        validated, _ = validate_operation(op, chart_context=self.context)
        self.assertEqual(validated.group, "Broadcasting")

    def test_diff_label_targets_allow_fewer_than_two_inputs(self) -> None:
        # executor가 dimension-label target("2019")을 데이터부모 슬라이스로 해석하므로,
        # 라벨 target이면 입력 노드 2개가 아니어도(0/1개) 유효해야 한다.
        op = DiffOp(op="diff", targetA="2019", targetB="2018",
                    meta=OpsMeta(nodeId="n1", inputs=[]))
        validated, _ = validate_operation(op, chart_context=self.context)
        self.assertEqual(validated.op, "diff")

    def test_diff_both_refs_still_require_exactly_two_inputs(self) -> None:
        # 둘 다 scalar ref이면 그 2개 노드가 정확히 필요(엄격 경로 유지).
        op = DiffOp(op="diff", targetA="ref:n1", targetB="ref:n2",
                    meta=OpsMeta(nodeId="n3", inputs=["n1"]))  # 1개뿐 → 거부
        with self.assertRaises(ValueError):
            validate_operation(op, chart_context=self.context)

    def test_find_extremum_rank_accepts_positive_int(self) -> None:
        op = FindExtremumOp(op="findExtremum", field="Revenue_Million_Euros", which="max", rank=2)
        normalized, _ = validate_operation(op, chart_context=self.context)
        self.assertEqual(normalized.rank, 2)

    def test_find_extremum_rank_rejects_zero_or_negative(self) -> None:
        with self.assertRaises(ValueError):
            validate_operation(
                FindExtremumOp(op="findExtremum", field="Revenue_Million_Euros", which="max", rank=0),
                chart_context=self.context,
            )
        with self.assertRaises(ValueError):
            validate_operation(
                FindExtremumOp(op="findExtremum", field="Revenue_Million_Euros", which="min", rank=-1),
                chart_context=self.context,
            )

    def test_find_extremum_rank_rejects_non_int_type(self) -> None:
        with self.assertRaises(Exception):
            parse_operation_spec({"op": "findExtremum", "field": "Revenue_Million_Euros", "which": "max", "rank": "two"})


class DimensionGroupFixADetectionTest(unittest.TestCase):
    """structural fix A 탐지 helper(dimension_filter_for_group_op)의 단위 테스트.

    series가 아닌 dimension 값이 비-filter 집계/선택 op의 group으로 들어온 경우만
    (dim_field, [values])를 반환하고, 그 외에는 보수적으로 None을 반환해야 한다.
    """

    def setUp(self) -> None:
        # season(dimension) 값과 category(series) 값이 서로 겹치지 않는 단순 컨텍스트.
        self.ctx = ChartContext(
            fields=["season", "category", "Revenue_Million_Euros"],
            dimension_fields=["season", "category"],
            measure_fields=["Revenue_Million_Euros"],
            primary_dimension="season",
            primary_measure="Revenue_Million_Euros",
            series_field="category",
            categorical_values={
                "season": ["2016/17", "2017/18"],
                "category": ["Broadcasting", "Commercial"],
            },
        )

    def test_detects_dimension_group_on_average(self) -> None:
        op = AverageOp(op="average", field="Revenue_Million_Euros", group="2016/17")
        self.assertEqual(dimension_filter_for_group_op(op, self.ctx), ("season", ["2016/17"]))

    def test_detects_dimension_group_on_count_retrieve_find_lagdiff(self) -> None:
        # 같은 series-restriction group 계열 op들은 모두 동일하게 탐지돼야 한다(일반화).
        for op in (
            CountOp(op="count", group="2016/17"),
            RetrieveValueOp(op="retrieveValue", field="season", target="2016/17", group="2017/18"),
            FindExtremumOp(op="findExtremum", field="Revenue_Million_Euros", which="max", group="2016/17"),
            LagDiffOp(op="lagDiff", field="Revenue_Million_Euros", group="2017/18"),
        ):
            with self.subTest(op=op.op):
                result = dimension_filter_for_group_op(op, self.ctx)
                self.assertIsNotNone(result)
                self.assertEqual(result[0], "season")

    def test_detects_dimension_group_list_on_sum(self) -> None:
        # sum의 group은 str 또는 list. dimension 값들의 list도 탐지돼야 한다.
        op = SumOp(op="sum", field="Revenue_Million_Euros", group=["2016/17", "2017/18"])
        self.assertEqual(
            dimension_filter_for_group_op(op, self.ctx),
            ("season", ["2016/17", "2017/18"]),
        )

    def test_valid_series_group_returns_none(self) -> None:
        # 진짜 series 값이면 정상적인 series 제한 → 삽입하지 않는다.
        op = AverageOp(op="average", field="Revenue_Million_Euros", group="Broadcasting")
        self.assertIsNone(dimension_filter_for_group_op(op, self.ctx))

    def test_no_group_returns_none(self) -> None:
        op = AverageOp(op="average", field="Revenue_Million_Euros")
        self.assertIsNone(dimension_filter_for_group_op(op, self.ctx))

    def test_filter_op_returns_none(self) -> None:
        # filter는 include를 직접 가질 수 있으므로 fix A 대상이 아니다(fix B 경로).
        op = FilterOp(op="filter", group="2016/17")
        self.assertIsNone(dimension_filter_for_group_op(op, self.ctx))

    def test_diff_family_out_of_scope_returns_none(self) -> None:
        # diff 계열은 group 의미/입력 개수 제약이 달라 fix A 대상에서 제외된다.
        op = DiffOp(op="diff", targetA="2016/17", targetB="2017/18", group="2016/17")
        self.assertIsNone(dimension_filter_for_group_op(op, self.ctx))

    def test_ambiguous_value_in_two_dimensions_returns_none(self) -> None:
        # 값이 두 dimension에 모두 존재하면 모호 → None(기존 검증 에러로 떨어짐).
        ctx = ChartContext(
            fields=["season", "region", "category", "Revenue_Million_Euros"],
            dimension_fields=["season", "region", "category"],
            measure_fields=["Revenue_Million_Euros"],
            primary_dimension="season",
            primary_measure="Revenue_Million_Euros",
            series_field="category",
            categorical_values={
                "season": ["A", "2017/18"],
                "region": ["A", "North"],
                "category": ["Broadcasting", "Commercial"],
            },
        )
        op = AverageOp(op="average", field="Revenue_Million_Euros", group="A")
        self.assertIsNone(dimension_filter_for_group_op(op, ctx))

    def test_value_in_both_series_and_dimension_returns_none(self) -> None:
        # series 도메인과 겹치면 series 제한으로 간주 → None.
        ctx = ChartContext(
            fields=["season", "category", "Revenue_Million_Euros"],
            dimension_fields=["season", "category"],
            measure_fields=["Revenue_Million_Euros"],
            primary_dimension="season",
            primary_measure="Revenue_Million_Euros",
            series_field="category",
            categorical_values={
                "season": ["Broadcasting", "2017/18"],
                "category": ["Broadcasting", "Commercial"],
            },
        )
        op = AverageOp(op="average", field="Revenue_Million_Euros", group="Broadcasting")
        self.assertIsNone(dimension_filter_for_group_op(op, ctx))

    def test_no_series_field_returns_none(self) -> None:
        ctx = ChartContext(
            fields=["season", "Revenue_Million_Euros"],
            dimension_fields=["season"],
            measure_fields=["Revenue_Million_Euros"],
            primary_dimension="season",
            primary_measure="Revenue_Million_Euros",
            series_field=None,
            categorical_values={"season": ["2016/17", "2017/18"]},
        )
        op = AverageOp(op="average", field="Revenue_Million_Euros", group="2016/17")
        self.assertIsNone(dimension_filter_for_group_op(op, ctx))

    def test_unmappable_group_still_raises_in_validate_operation(self) -> None:
        # dimension 어디에도 없는 group 값은 탐지 helper가 None → 기존 검증이 그대로 raise.
        op = AverageOp(op="average", field="Revenue_Million_Euros", group="NOPE")
        self.assertIsNone(dimension_filter_for_group_op(op, self.ctx))
        with self.assertRaises(ValueError):
            validate_operation(op, chart_context=self.ctx)


if __name__ == "__main__":
    unittest.main()
