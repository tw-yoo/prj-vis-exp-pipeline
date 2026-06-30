from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic.types import constr

from .types import JsonValue


TaskId = constr(pattern=r"^o[0-9]+$")  # type: ignore[valid-type]


class OpTask(BaseModel):
    """
    An extracted "operation task" from the explanation text.

    - taskId is stable within a single request (o1, o2, ...)
    - op is one of op_registry.allowed_ops (validated later)
    - sentenceIndex is a legacy field name; it stores reasoning-chunk order
      and maps to chunk-layer groups ("ops", "ops2", ...)
    - paramsHint is a *flat* hint dict (no nested objects) to keep prompting stable
    """

    taskId: TaskId
    op: str = Field(..., min_length=1)
    sentenceIndex: int = Field(..., ge=1)
    mention: str = Field(..., min_length=1)
    paramsHint: Dict[str, JsonValue] = Field(default_factory=dict)

    model_config = ConfigDict(extra="forbid")


class OpInventory(BaseModel):
    tasks: List[OpTask] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)

    model_config = ConfigDict(extra="forbid")


class StepComposeOutput(BaseModel):
    pickTaskId: Optional[TaskId] = None
    op_spec: Dict[str, JsonValue] = Field(default_factory=dict)
    inputs: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)

    model_config = ConfigDict(extra="forbid")


class _OpSpecStrict(BaseModel):
    """op_spec sub-model used ONLY for Ollama structured-output schema generation.

    Declares op:str so Ollama's constrained sampler is forced to emit a string,
    not a bare object copy of the schema template ({op: {}, ...: {}}).
    Extra fields are allowed (filter.operator, diff.targetA, etc.).
    """

    op: str = Field(..., min_length=1)

    model_config = ConfigDict(extra="allow")


class _StepComposeOutputOllama(BaseModel):
    """Parallel schema for Ollama constrained-sampling only.

    Used as response_model in _complete_native so the JSON schema has
    op_spec.op: str enforced. After parsing, op_spec is serialized back to a dict
    and wrapped in StepComposeOutput for the rest of the pipeline.
    """

    pickTaskId: Optional[str] = None
    op_spec: _OpSpecStrict = Field(default_factory=lambda: _OpSpecStrict(op="__unset__"))
    inputs: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)

    model_config = ConfigDict(extra="forbid")

    def to_step_compose_output(self) -> StepComposeOutput:
        return StepComposeOutput(
            pickTaskId=self.pickTaskId,
            op_spec=self.op_spec.model_dump(),
            inputs=self.inputs,
            warnings=self.warnings,
        )
