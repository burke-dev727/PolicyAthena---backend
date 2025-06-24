from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class ProfileData(BaseModel):
    age: int
    zip_code: str
    preferences: List[str]

@router.post("/match")
async def match_plans(profile: ProfileData):
   # Placeholder logic – eventually connect to matchAgent
    return {
        "message": "Plans matched successfully.",
        "matched_plans": [
            {"plan_id": "plan_001", "name": "Basic Health Plan"},
            {"plan_id": "plan_002", "name": "Premium Coverage Plan"}
        ]
    }
