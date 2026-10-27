from fastapi import FastAPI

from app.api.routes.agent import router

app = FastAPI(
    title="FastAPI AI Agent Demo",
    version="1.0.0",
    description="A bounded agent loop with explicit planning, validated tools, and an inspectable trace.",
)
app.include_router(router, prefix="/api/v1")


@app.get("/health", tags=["system"])
async def health() -> dict[str, str]:
    return {"status": "ok"}
