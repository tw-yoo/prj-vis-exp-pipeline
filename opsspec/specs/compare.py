from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import ConfigDict

from ..core.types import JsonValue
from .base import BaseOpFields


class CompareOp(BaseOpFields):
    """Deprecated. compare op was removed; this permissive shim exists only so
    legacy test fixtures referencing CompareOp keep importing. It is NOT in the
    operation Union, registry, executor, or validator. Use DiffByValueOp instead.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    op: Literal["compare"] = "compare"
    # Permissive: any compare-era field (targetA, targetB, which, group, ...) is accepted.
    # Marked Any to bypass Pydantic strict validation for legacy data only.

    def __init__(self, **data: Any) -> None:  # type: ignore[no-untyped-def]
        super().__init__(**data)


class DiffByValueOp(BaseOpFields):
    """단일 scalar 기준값(V)과 차트의 모든 데이터 행을 비교해 delta 시퀀스를 반환.
    권장 조합A(literal 기준): `value` (scalar 숫자).
    조합B(ref 기준): `targetValue` ("ref:nX") - 이전 노드의 scalar 결과를 기준으로 사용.
    `value`와 `targetValue`는 둘 중 하나만 지정.
    """

    op: Literal["diffByValue"] = "diffByValue"
    value: Optional[float] = None  # literal 기준값
    targetValue: Optional[str] = None  # 'ref:nX' 형태 scalar 참조
    field: Optional[str] = None  # 비교 대상 수치 필드명(보통 y축)
    group: Optional[str] = None  # 전체 slice 제한용 group/series 이름
    signed: Optional[bool] = True  # True면 row.value - V 부호 유지


class CompareBoolOp(BaseOpFields):
    """두 값의 참/거짓 비교(Boolean 성격 결과).
    권장 조합: `targetA`, `targetB`, `operator`.
    조합B: `field` + `groupA/groupB` (+ `aggregate`) 후 operator 적용.
    """

    op: Literal["compareBool"] = "compareBool"
    field: Optional[str] = None  # 비교 대상 수치 필드명
    targetA: Optional[JsonValue] = None  # 값 A (literal 또는 "ref:nX")
    targetB: Optional[JsonValue] = None  # 값 B (literal 또는 "ref:nX")
    group: Optional[str] = None  # 전체 slice 제한용 group/series 이름
    groupA: Optional[str] = None  # 그룹 A 이름
    groupB: Optional[str] = None  # 그룹 B 이름
    aggregate: Optional[str] = None  # 슬라이스 집계 방식
    operator: Optional[str] = None  # 비교 연산자 (>, >=, <, <=, ==, !=)


class DiffOp(BaseOpFields):
    """두 값 차이 계산.
    권장 조합A(스칼라 차이): `targetA`, `targetB` (둘 다 필요), `signed`.
    조합B(슬라이스 차이): `field` + (`groupA`,`groupB`) 또는 `aggregate`.
    조건부: `targetA/B`를 넣으면 A/B 모두 필요, groupA/B는 보통 불필요.
    """

    op: Literal["diff"] = "diff"
    field: Optional[str] = None  # 차이를 계산할 수치 필드명
    targetA: Optional[JsonValue] = None  # 값 A (literal 또는 "ref:nX")
    targetB: Optional[JsonValue] = None  # 값 B (literal 또는 "ref:nX")
    group: Optional[str] = None  # 전체 slice 제한용 group/series 이름
    groupA: Optional[str] = None  # 그룹 A 이름
    groupB: Optional[str] = None  # 그룹 B 이름
    aggregate: Optional[str] = None  # 슬라이스 집계 방식
    signed: Optional[bool] = False  # True면 A-B 부호 유지
    mode: Optional[str] = None  # diff 변형 모드(엔진 정의에 따름)
    percent: Optional[bool] = None  # 백분율 차이 여부
    scale: Optional[float] = None  # 결과 스케일 배율
    precision: Optional[int] = None  # 반올림 자릿수
    targetName: Optional[str] = None  # 결과 레이블명(선택)


class LagDiffOp(BaseOpFields):
    """같은 그룹/시계열 내 인접 값 차이(행 리스트 반환).
    필수: `field` 권장.
    선택: `group`으로 series 제한, `order`로 정렬 방향, `absolute`로 절대값.
    """

    op: Literal["lagDiff"] = "lagDiff"
    field: Optional[str] = None  # 차이를 계산할 수치 필드명(보통 y축)
    group: Optional[str] = None  # group/series 이름
    order: Optional[Literal["asc", "desc"]] = None  # x축(시간) 순서 방향
    signed: Optional[bool] = None  # 절대값 차이로 변환할지


class PairDiffOp(BaseOpFields):
    """키(`by`)별로 groupA-groupB 차이 계산(행 리스트 반환).
    필수: `by`, `groupA`, `groupB`.
    조건부: `seriesField` 미지정 시 chart_context.series_field 사용.
    권장: `field`는 y축 수치 필드명 명시.
    """

    op: Literal["pairDiff"] = "pairDiff"
    by: str  # 결과 키 필드명 (예: City, Year 등 x축/차원 필드명)
    seriesField: Optional[str] = None  # groupA/B를 찾을 축 필드명 (예: Year, Country)
    field: Optional[str] = None  # 차이를 계산할 수치 필드명(보통 y축)
    groupA: str  # 비교값 A (seriesField 도메인의 실제 값)
    groupB: str  # 비교값 B (seriesField 도메인의 실제 값)
    signed: Optional[bool] = True  # True면 A-B 부호 유지
    absolute: Optional[bool] = False  # True면 abs(A-B)
    precision: Optional[int] = None  # 반올림 자릿수
    group: Optional[str] = None  # 상위 slice 제한용 group/series 이름
