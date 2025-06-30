from fastapi import APIRouter, Request
from pydantic import BaseModel
from input_interpreter import user_data
router = APIRouter()

class InputData(user_data):
    name: user_data[0]
    age: user_data[1]
    zip_code: user_data[2]

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
