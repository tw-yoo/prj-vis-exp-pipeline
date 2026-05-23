from __future__ import annotations

from typing import List, Literal, Optional, Union

from ..core.types import JsonValue
from .base import BaseOpFields


class RetrieveValueOp(BaseOpFields):
    """단일 값 조회.
    필수: `field`, `target`.
    값 규칙: `field`는 조회 기준 필드명, `target`은 해당 필드의 실제 데이터값.
    선택: `group`은 series/group 이름 제한.
    `targetAxis`로 조회 방향 제어:
      - `'x'` (default): forward — `target`이 x축 카테고리 라벨, 해당 row의 y값을 반환.
      - `'y'`: reverse — `target`이 numeric y값, 그 값과 일치하는 x 카테고리 row를 반환.
        multi-measure 차트에서는 `field`를 함께 지정해야 함.
    """

    op: Literal["retrieveValue"] = "retrieveValue"
    field: Optional[str] = None  # 필드명 (forward면 x축, reverse면 y measure 필드명)
    target: Optional[JsonValue] = None  # forward: 카테고리 라벨 / reverse: numeric y값
    group: Optional[str] = None  # group/series 이름 (예: "Commercial")
    targetAxis: Optional[Literal["x", "y"]] = None  # default 'x'


class AverageOp(BaseOpFields):
    """평균 계산(스칼라 반환).
    필수: `field`.
    값 규칙: `field`는 평균낼 y축 수치 필드명.
    선택: `group`은 특정 series/group만 대상으로 제한.
    """

    op: Literal["average"] = "average"
    field: Optional[str] = None  # 평균낼 수치 필드명 (보통 y축)
    group: Optional[str] = None  # group/series 이름


class SumOp(BaseOpFields):
    """합계 계산(스칼라 반환).
    필수: `field`.
    값 규칙: `field`는 합산할 y축 수치 필드명.
    조건부: `group`이 str이면 해당 group만, list면 규칙에 따라(예: stacked 예외) 전체/부분 합산.
    """

    op: Literal["sum"] = "sum"
    field: Optional[str] = None  # 합산할 수치 필드명 (보통 y축)
    group: Optional[Union[str, List[str]]] = None  # group/series 이름 1개 또는 여러 개


class CountOp(BaseOpFields):
    """개수 계산(스칼라 반환).
    필수: 보통 없음(`field` 생략 가능).
    값 규칙: `field`를 넣으면 해당 필드를 기준으로 count 의미를 명확화.
    선택: `group`은 특정 series/group 제한.
    """

    op: Literal["count"] = "count"
    field: Optional[str] = None  # count 해석 기준 필드명(선택)
    group: Optional[str] = None  # group/series 이름
