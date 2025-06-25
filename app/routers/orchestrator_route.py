from fastapi import APIRouter
from app.agents.orchestrator import OrchestratorAgent

router = APIRouter()
orchestrator = OrchestratorAgent()

@router.post("/recommendation")
def get_recommendation(raw_input: dict):
    return orchestrator.run(raw_input)
