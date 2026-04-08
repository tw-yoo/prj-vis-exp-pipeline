from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class OpsMetaView(BaseModel):
    splitGroup: Optional[str] = None
    panelId: Optional[str] = None
    joinBarrier: Optional[bool] = None
    phase: Optional[int] = None
    parallelGroup: Optional[str] = None

    model_config = ConfigDict(extra="forbid")


class OpsMeta(BaseModel):
    nodeId: Optional[str] = None
    inputs: List[str] = Field(default_factory=list)
    sentenceIndex: Optional[int] = None
    view: Optional[OpsMetaView] = None
    source: Optional[str] = None

    model_config = ConfigDict(extra="forbid")


class BaseOpFields(BaseModel):
    op: str
    id: Optional[str] = None
    # meta is required for all ops (tree/DAG reconstruction), but we allow
    # producers to omit it and fill a default here. Canonicalization will
    # then enforce deterministic nodeId/inputs.
    meta: OpsMeta = Field(default_factory=OpsMeta)
    chartId: Optional[str] = None

    model_config = ConfigDict(extra="forbid", populate_by_name=True)
