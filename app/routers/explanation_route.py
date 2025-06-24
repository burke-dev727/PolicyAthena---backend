from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict

router = APIRouter()

class ExplanationRequest(BaseModel):
    plan: Dict[str, str]
    profile: Dict[str, str]

# Dummy route for generating an explanation
@router.post("/explain")
async def generate_explanation(data: ExplanationRequest):
    # Placeholder logic – eventually connect to ExplanationAgent
    return {
        "message": "Explanation generated.",
        "explanation": f"Plan {data.plan.get('plan_id')} is a good fit for the given profile."
    }
