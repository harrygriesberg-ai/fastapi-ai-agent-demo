from app.providers.planner import Planner
from app.schemas.agent import AgentResponse, FinalAnswer, ToolCall, TraceEntry
from app.tools.registry import ToolRegistry


class AgentLimitExceeded(RuntimeError):
    pass


class AgentService:
    def __init__(self, planner: Planner, registry: ToolRegistry) -> None:
        self.planner = planner
        self.registry = registry

    async def run(self, message: str, max_steps: int) -> AgentResponse:
        history: list[dict] = []
        trace: list[TraceEntry] = []

        for step in range(1, max_steps + 1):
            decision = await self.planner.decide(message, self.registry.descriptions(), history)
            if isinstance(decision, FinalAnswer):
                trace.append(TraceEntry(step=step, decision_type="final"))
                return AgentResponse(answer=decision.answer, steps_used=step, trace=trace)

            if isinstance(decision, ToolCall):
                observation = await self.registry.execute(decision.tool_name, decision.arguments)
                history.append(
                    {
                        "tool": decision.tool_name,
                        "arguments": decision.arguments,
                        "observation": observation,
                    }
                )
                trace.append(
                    TraceEntry(
                        step=step,
                        decision_type="tool",
                        tool_name=decision.tool_name,
                        arguments=decision.arguments,
                        observation=observation,
                    )
                )

        raise AgentLimitExceeded(f"agent exceeded the configured limit of {max_steps} steps")
