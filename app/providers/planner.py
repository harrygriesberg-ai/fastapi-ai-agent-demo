import json
from typing import Any, Protocol

from app.schemas.agent import FinalAnswer, PlannerEnvelope, ToolCall

PlannerDecision = ToolCall | FinalAnswer


class Planner(Protocol):
    async def decide(
        self,
        message: str,
        tools: list[dict[str, Any]],
        history: list[dict[str, Any]],
    ) -> PlannerDecision:
        ...


class MockPlanner:
    async def decide(
        self,
        message: str,
        tools: list[dict[str, Any]],
        history: list[dict[str, Any]],
    ) -> PlannerDecision:
        lower = message.lower()
        if history:
            return FinalAnswer(answer=f"Tool result received: {history[-1]['observation']}")
        if "weather" in lower:
            city = message.split("in ")[-1].strip(" ?.") if "in " in lower else "Sydney"
            return ToolCall(tool_name="weather", arguments={"city": city})
        if any(word in lower for word in ("add", "plus", "sum")):
            numbers = [float(token) for token in message.replace(",", " ").split() if token.replace('.', '', 1).isdigit()]
            if len(numbers) >= 2:
                return ToolCall(tool_name="calculator", arguments={"operation": "add", "a": numbers[0], "b": numbers[1]})
        return FinalAnswer(answer="I can answer directly, or use the calculator/weather demo tools when needed.")


class OpenAIPlanner:
    def __init__(self, api_key: str, model: str) -> None:
        try:
            from openai import AsyncOpenAI
        except ImportError as exc:
            raise RuntimeError(
                'Install the optional OpenAI dependency with: pip install -e \".[openai]\"'
            ) from exc
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model

    async def decide(
        self,
        message: str,
        tools: list[dict[str, Any]],
        history: list[dict[str, Any]],
    ) -> PlannerDecision:
        decision_schema = PlannerEnvelope.model_json_schema()
        response = await self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "system",
                    "content": (
                        "You are a tool-using planner. Decide whether to call one tool or return a final answer. "
                        f"Available tools: {json.dumps(tools)}. Prior observations: {json.dumps(history)}"
                    ),
                },
                {"role": "user", "content": message},
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "agent_decision",
                    "schema": decision_schema,
                    "strict": True,
                }
            },
        )
        envelope = PlannerEnvelope.model_validate(json.loads(response.output_text))
        if envelope.type == "tool":
            if not envelope.tool_name:
                raise ValueError("planner returned a tool decision without tool_name")
            return ToolCall(tool_name=envelope.tool_name, arguments=envelope.arguments)
        if not envelope.answer:
            raise ValueError("planner returned a final decision without an answer")
        return FinalAnswer(answer=envelope.answer)
