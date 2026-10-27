from functools import lru_cache

from app.core.config import get_settings
from app.providers.planner import MockPlanner, OpenAIPlanner
from app.services.agent_service import AgentService
from app.tools.calculator import CalculatorTool
from app.tools.registry import ToolRegistry
from app.tools.weather import WeatherTool


@lru_cache

def get_agent_service() -> AgentService:
    settings = get_settings()
    if settings.planner_provider == "openai":
        if not settings.openai_api_key:
            raise RuntimeError("APP_OPENAI_API_KEY is required for OpenAI planner mode")
        planner = OpenAIPlanner(settings.openai_api_key, settings.openai_model)
    else:
        planner = MockPlanner()

    registry = ToolRegistry([CalculatorTool(), WeatherTool()])
    return AgentService(planner=planner, registry=registry)
