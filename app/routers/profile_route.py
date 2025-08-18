from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from app.agents.profile_builder import ProfileBuilderAgent

router = APIRouter()
builder = ProfileBuilderAgent()

class ParsedInput(BaseModel):
    name: str
    age: int
    email: str
    phone: str
    address: str
    location: str
    zip_code: str
    ssn: str

    is_employed: bool  
    employer_name: str
    is_employeroffers: bool  
    annual_income: int
    household_size: int
    preferences: List[str]
    
    class Config:
        arbitrary_types_allowed = True

@router.post("/profile")
def build_profile(input: ParsedInput):
    return builder.run(input.dict())