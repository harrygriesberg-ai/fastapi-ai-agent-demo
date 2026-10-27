from typing import Any, Literal

from pydantic import BaseModel, Field


class AgentRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    max_steps: int = Field(default=4, ge=1, le=8)


class ToolCall(BaseModel):
    type: Literal["tool"] = "tool"
    tool_name: str
    arguments: dict[str, Any] = Field(default_factory=dict)


class FinalAnswer(BaseModel):
    type: Literal["final"] = "final"
    answer: str


class PlannerEnvelope(BaseModel):
    type: Literal["tool", "final"]
    tool_name: str | None = None
    arguments: dict[str, Any] = Field(default_factory=dict)
    answer: str | None = None


class TraceEntry(BaseModel):
    step: int
    decision_type: Literal["tool", "final"]
    tool_name: str | None = None
    arguments: dict[str, Any] | None = None
    observation: Any | None = None


class AgentResponse(BaseModel):
    answer: str
    steps_used: int
    trace: list[TraceEntry]
