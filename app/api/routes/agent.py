from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_agent_service
from app.schemas.agent import AgentRequest, AgentResponse
from app.services.agent_service import AgentLimitExceeded, AgentService

router = APIRouter(prefix="/agent", tags=["agent"])


@router.post("/run", response_model=AgentResponse)
async def run_agent(
    payload: AgentRequest,
    service: AgentService = Depends(get_agent_service),
) -> AgentResponse:
    try:
        return await service.run(payload.message, payload.max_steps)
    except AgentLimitExceeded as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
