from fastapi import APIRouter, Request
from pydantic import BaseModel

router = APIRouter(prefix="/userInput", tags=["userInput"])

class InputData(BaseModel):
    name: str
    age: int
    zip_code: str

@router.post("/input")
async def process_input(data: InputData):
  
    return {
        "message": "Input received successfully.",
        "parsed": {
            "name": data.name.upper(),
            "age": data.age,
            "zip_code": data.zip_code
        }
    }
