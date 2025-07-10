import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.agents.plan_builder import PlanBuilderAgent
from app.services.plan_extractor import extract_plan_fields


router = APIRouter()
UPLOAD_TEMP = "temp_uploads"
os.makedirs(UPLOAD_TEMP, exist_ok=True)
agent = PlanBuilderAgent()

@router.post("/upload")
async def upload_plan(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_TEMP, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())

    plan_name = os.path.splitext(file.filename)[0]
    plan_data = agent.parse_and_save(file_location, plan_name)
    os.remove(file_location)
    return {"message": "Uploaded and parsed", "plan": plan_data.dict()}

@router.post("/extract-fields")
async def extract_fields(plan_name: str):
    path = f"data/extracted_text/{plan_name}.txt"
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    fields = extract_plan_fields(text)
    return {"fields": fields}


@router.get("/{plan_name}")
def get_plan(plan_name: str):
    try:
        return agent.get_plan(plan_name)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Plan not found")
