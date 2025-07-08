import os
import json
from app.models.plan_model import PlanData

DATA_DIR = os.path.join("data", "plans")
os.makedirs(DATA_DIR, exist_ok=True)

def save_plan(plan: PlanData):
    filename = f"{plan.name}.json"
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(json.dumps(plan.model_dump(), indent=2))

def load_plan(plan_name: str) -> PlanData:
    filepath = os.path.join(DATA_DIR, f"{plan_name}.json")
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"No saved plan found: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        data = f.read()
    return PlanData.parse_raw(data)
