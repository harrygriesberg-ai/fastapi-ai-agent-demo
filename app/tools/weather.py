from pydantic import BaseModel, Field


class WeatherArgs(BaseModel):
    city: str = Field(min_length=2, max_length=100)


class WeatherTool:
    name = "weather"
    description = "Return deterministic demo weather for a city; no external network call is made."
    args_model = WeatherArgs

    async def execute(self, arguments: WeatherArgs) -> dict[str, str | int]:
        return {"city": arguments.city, "condition": "clear", "temperature_c": 22}
