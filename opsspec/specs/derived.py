from __future__ import annotations

from typing import Literal, Optional

from .base import BaseOpFields


class RangeOp(BaseOpFields):
    """범위(max − min) 계산.
    필수: 없음.
    값 규칙: `field`는 비교할 수치 필드명(보통 y축, default=primary_measure).
    선택: `group`은 series/group 제한.
    Result: scalar one DatumValue with `{value: max - min}`; downstream
    annotation ops can re-locate the extremum rows by re-scanning.
    Replaces verbose `findExtremum(max) → findExtremum(min) → diff` chains
    when the semantic intent is "spread / variation / range".
    """

    op: Literal["range"] = "range"
    field: Optional[str] = None  # 비교할 수치 필드명 (기본: primary_measure)
    group: Optional[str] = None  # group/series 이름


class RollingWindowOp(BaseOpFields):
    """슬라이딩 윈도우 집계(sum / avg / min / max).
    필수: `window` (양의 정수).
    값 규칙: 시작 위치 i마다 길이 `window` 만큼 집계한 결과를 한 row씩 반환.
    선택: `aggregate` (default=avg), `orderField` (정렬 축, 보통 x축),
    `field` (집계 대상 수치), `group`.
    Use case: "3-year average", "5-consecutive-year window".
    Result: row list (N − window + 1 rows). Downstream `findExtremum`/`nth`
    가 best window를 고를 수 있다.
    """

    op: Literal["rollingWindow"] = "rollingWindow"
    window: int  # 슬라이딩 윈도우 크기 (정수, ≥1) — 필수
    aggregate: Optional[Literal["sum", "avg", "min", "max"]] = None  # 기본 'avg'
    field: Optional[str] = None  # 집계할 수치 필드명
    orderField: Optional[str] = None  # 슬라이딩 정렬 축 (보통 x축 필드)
    group: Optional[str] = None  # group/series 이름


class MonotonicRunOp(BaseOpFields):
    """단조 구간(monotonic run) 탐색.
    필수: 없음. 기본은 `direction='increasing'`, `mode='longest'`,
    `strict=true`, `minLength=2`.
    값 규칙:
      - mode='longest': 가장 긴 단조 구간을 row list로 반환.
      - mode='firstBreak': 첫 단조 시작 시점의 단일 row를 반환.
      - mode='all': 모든 적격 구간을 flatten하여 반환.
    Use case: "longest period of decrease", "year when it starts to
    decrease", "consecutive years of increase".
    """

    op: Literal["monotonicRun"] = "monotonicRun"
    direction: Optional[Literal["increasing", "decreasing"]] = None  # 기본 'increasing'
    strict: Optional[bool] = None  # 기본 true
    mode: Optional[Literal["longest", "firstBreak", "all"]] = None  # 기본 'longest'
    minLength: Optional[int] = None  # 최소 길이 (기본 2)
    field: Optional[str] = None  # 비교 수치 필드명
    orderField: Optional[str] = None  # 정렬 축 (보통 x축 필드)
    group: Optional[str] = None  # group/series 이름
