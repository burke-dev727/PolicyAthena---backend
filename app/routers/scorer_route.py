from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict

router = APIRouter()

class PlanData(BaseModel):
    plan_id: str
    attributes: Dict[str, str]

class PlansList(BaseModel):
    plans: List[PlanData]

# Dummy scoring route
@router.post("/score")
async def score_plans(data: PlansList):
    # Dummy logic – eventually connect to ScoringAgent
    scored = sorted(data.plans, key=lambda p: p.plan_id)  # placeholder sort
    return {
        "message": "Plans scored successfully.",
        "scored_plans": [{"plan_id": p.plan_id, "score": idx + 1} for idx, p in enumerate(scored)]
    }
