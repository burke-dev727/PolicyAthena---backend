from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.agents.profile_builder import ProfileBuilderAgent

router = APIRouter()
builder = ProfileBuilderAgent()

class ParsedInput(BaseModel):
    age: int
    zip_code: str
    preferences: List[str]

@router.post("/profile")
def build_profile(input: ParsedInput):
    return builder.run(input.dict())
